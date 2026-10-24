# ADJUDICATION of T36 (`m88kbuserrregs`, round `#570`) PASS 1 -- for GPT-6 Astra (adjudicator; owner roster 2026-10-23)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You adjudicate the pass-1 design review of one regression-testing round in the GXemul hardened fork (a correctness fix
to the m88k memory model: two CMMU fault-status registers never written on a refused device access, and the regression
rows it owes).  The main loop has read all six seat answers and written its dispositions in `PASS1_RULINGS.md` (same
directory as this packet's parent).  **Your job is to find which of those dispositions is WRONG**, settle the four
disputes below by argument and by the source (you may open every file named here and the tree at HEAD `7fca7187`;
read the four peer-edited working-tree files -- `src/devices/dev_pcc2.c`, `src/include/thirdparty/mvme_pcctworeg.h`,
`regress/gate_offline.sh`, `tools/pipeline/check_probe_wiring.py` -- via `git show HEAD:<path>`), and be HARDER on the
positions that adopted YOUR OWN pass-1 claims than on the others: a ruling in your favour is the one you are least
likely to test.  Do not build or run anything; do not propose reproduction recipes; dispositions by id.

All paths are under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\m88kbuserrregs\pass1_20261023\` unless
absolute.  The brief the seats answered is `packet.md` (FULL) / `packet_compact.md` (what GLM and DeepSeek saw, split
Q1-2 / Q3-4).  The witness is `..\witness_20261023\` (`WITNESS_REPORT.md`, `m88k_buserr_probe.py`,
`WITNESS_headbin.out`).

## 1. The seats and where their answers are

| seat | file | verdict | class |
|---|---|---|---|
| GPT-6 Astra (you, as reviewer) | `codex_t36p1.txt` | READY WITH CHANGES | file-reading |
| Grok 4.7 (xhigh, plan mode, cwd GXEMUL-SEC) | `grok_t36p1.txt` | READY WITH CHANGES | file-reading (WORKING tree) |
| GLM 5.3 | `ollama_glm_t36p1_Q12.txt`, `ollama_glm_t36p1_Q34.txt` | READY WITH CHANGES | packet-fed |
| DeepSeek v4-pro | `ollama_deepseek_t36p1_Q12.txt`, `ollama_deepseek_t36p1_Q34.txt` | READY WITH CHANGES | packet-fed |
| Gemini 4 Argon | `argon.NOT_FIRED.txt` | SEAT FAILURE (transport), not fired | -- |
| Fable 5.1 | `fable5.HELD.txt` | HELD by the owner, with its question | -- |
| agy, kimi, minimax, Opus-as-seat | `roster_NOT_FIRED.txt` | DELIBERATELY NOT FIRED by roster | -- |

The main loop's own checks: `CHECKS_mainloop.md` (10 items, each with its refuter).  The drafter's inconsistency list:
`drafter_NOTES.md`.

## 2. The dispositions under test -- `PASS1_RULINGS.md` sections A (A1-A11), B (B1-B14), C (C1-C5): THIRTY

Read them there; this section only names what each rests on, so you can aim.

* A1-A5, A7-A10: unanimous across the four seats; the main loop ACCEPTED all of them.  **Which accepted disposition
  is wrong?**  Thirty were accepted; a round that accepts everything has either had a very good panel or has stopped
  arguing.
* A6 (the `m8820x.h` include in `cpu_m88k.c`, after `m8820x_pte.h`): unanimous; GLM's `memory_rw.c` alternative
  rejected by the main loop.
* A3's LICENCE UPGRADE and B5c rest on a fact the main loop MEASURED: `src/debugger/debugger_cmds.c:1302` --
  `pause <cpuid>` toggles `running`, so on mvme187 `-n 2` it starts a cpu that `dev_mvme187.c:136-149` gave no CMMU and
  that `memory_m88k.c:130-132` translates as identity.  That fact came from YOUR pass-1 answer (codex:15).
* A11 (the luna boot A/B is measured in-round): Grok and you; GLM/DeepSeek said "gate 7 / battery".
* B5a/B5b/B5c (three floor cells with rows): the disputes D1-D3 below.
* B4 (clause (c) record form and the exit-1 stub's 1/24): you, Grok, GLM against DeepSeek's 0/24.
* B10/B11/B12 (gate 14 after `arm_flags_probe.py`, `#568`'s row-identity form, two MANIFEST lines, the `probe:` term):
  unanimous.
* C1-C3 (R1 MED, R2 LOW, R3 research): unanimous on filing; C4 is YOUR additional finding (adopted -- test it
  harder); C5 is the main loop's own reading of `dev_m8820x.c:108`.

## 3. The disputes -- each side in its own words, then the main loop's ruling

**D1 -- the NULL-CMMU cell (P4).**
* Astra (codex:15): "P4 is false as stated.  MVME187 allocates CMMUs only to its bootstrap CPU, but its existing
  debugger can activate another existing CPU.  Such a secondary CPU shares the installed refusing devices while its
  CMMU pointers remain NULL ... Startup's 'only bootstrap running' condition is not a lifetime invariant."  (codex:70:
  FLOOR, "reachable secondary-MVME187 configuration; added predicate".)
* Grok (grok:20-22): "No guest-reachable claimed refusal on a running CPU with a NULL `cmmu[]` slot exists on the
  default in-tree machines ... `-n 2` creates CPU 1 with NULL slots and does not run it ... Removing it, or moving
  `m88k_exception` inside it, reds no row ... Disclose it.  Do not row it."  GLM-Q12:10 and DeepSeek-Q12:18 agree
  with Grok.
* RULING (B5c): FLOOR, two rows (`null surv`, `null route`) in a two-cpu mvme187 session started by `pause 1`, with a
  RAM-flag dispatcher because both cpus start at one pc, cpu 1 kept off the CMMU window (C5).  Questions for you:
  (i) is `-n 2` + `pause 1` admissible under the witness ladder's clause (iii) (machine description and dispatch
  unmodified; a documented command-line option is not a machine edit)?  (ii) does anything in the main loop's
  cpu scheduling stop a `pause`-started cpu from executing (name the file if so)?  (iii) is the session design sound
  -- the dispatcher, cpu 1 setting its own VBR, the HANDLED/FELL markers, the breakpoint that ends the session?
  (iv) is a row that kills a HOST NULL DEREFERENCE ("NULL check removed") a floor row or a survival control -- and
  does the distinction change anything?  Be harder on this than on the rest: it adopted your claim.

**D2 -- the instruction label (P5).**
* Astra (codex:71,77): FLOOR; "a stepped row can cover the selector through R2, but must explicitly identify that
  debugger-path dependency.  Clause-(e) disclosure alone does not discharge the reachable selector floor."  GLM-Q12:34,
  46: "FLOOR AND OWED ... the stepped instruction row in the round's one diff.  Its wants are already in the packet".
  DeepSeek-Q12:59: FLOOR, owed.
* Grok (grok:90): "Disclose the instruction label under clause (e).  Do not row it through a stepped session (i):
  that channel is the debugger pre-read (R2), and a later fix of R2 removes it, so the row would go green for the
  wrong reason ... The weaken-to-always-data mutant has no free-running guest channel, because R1 stops the CPU before
  the handler.  That is a disclosure, not a floor breach."
* RULING (B5a): FLOOR, four stepped rows (`ifetch route/pfsr/pfar/dcmmu`) scoring the witness's `INFO ifetch`
  observation, with the R2 dependency and the re-root obligation disclosed.  Question: Grok says a fixed R2 turns the
  row GREEN for the wrong reason; GLM-Q34:24 says it turns RED for an unrelated reason (the step's own fetch then hits
  R1's halt).  Which is right, and does either change the ruling?

**D3 -- the `no_exceptions`-set cell (P6).**
* Astra (codex:72): FLOOR -- "suppressed accesses reach the guard even when they skip the callback".  DeepSeek-Q12:60:
  FLOOR.  GLM-Q34:30 offers the discharge: "a stepped `dump` at 0xfff46010 asserting 0 returned, seeds and SXIP
  unchanged, cpu running, no vector ... kills the dropped-`!no_exceptions` mutant under either reading".
* Grok (grok:92): "It is the complement of a guard the diff does not add, so under R4/R7 it is clause (e), not a floor
  row.  `ok regs` already pins the served conjunct."  GLM-Q12:34: "the only mutant it would additionally kill is
  already killed by ok regs -- disclosed, not owed."
* RULING (B5b): FLOOR, one row `dbg noexc`.  The carrier's DEPENDS-ON clause enumerates "the predicates DOMINATING the
  diff's edited lines ... never only the ones the diff adds" (the 2026-08-24 correction, INTRODUCED -> DEPENDS ON);
  `!no_exceptions` at `memory_rw.c:603` dominates the writes; and the main loop holds GLM-Q12:34's "`ok regs` kills
  it" to be FALSE (`ok regs` is a served access, `res = 1`; dropping the conjunct changes nothing on it).  Question:
  is that refutation right, and is the one-row cost justified?

**D4 -- clause (c)'s predicted dead-run score.**  You, Grok and GLM: exit-1 stub -> 1/24 (`neg apparatus` passes by
design), `CONTROL=FAIL`; absent binary -> no sentinel.  DeepSeek-Q12:55: 0/24, no sentinel.  RULING (B4): record the
MEASURED number; never write 0/24 from prediction.  Confirm from `m88k_buserr_probe.py`'s `run_piped` / `row` /
scoring (lines ~424-435, 468-475, 580-605).

**D5 -- include placement.**  GLM-Q12:16: `#ifdef MEM_M88K` + include at the top of `memory_rw.c` keeps three files.
RULING (A6): upstream's placement in `cpu_m88k.c` after `m8820x_pte.h` (Grok's ordering reason, grok:32).  Confirm or
overturn.

## 4. The questions -- VERDICT LINE FIRST (`VERDICT: UPHOLD | AMEND | REJECT -- <one line>`), then by id

Q1. Of the THIRTY accepted dispositions (A1-A11, B1-B14, C1-C5), which are WRONG, and why (file:line)?  Name at least
    the ones you are least sure of even if you uphold them.
Q2. D1-D5: rule each, in your own words, against the source and the quoted rule text (the carrier's clause (d)
    DEPENDS-ON bound, its 2026-08-24 correction, the floor's "jointly reachable" condition, the witness ladder's
    clause (iii)).  For D1, answer (i)-(iv).
Q3. The row budget: 24 + 7 (`ifetch route/pfsr/pfar/dcmmu`, `dbg noexc`, `null surv`, `null route`) = 31.  Is any of
    the seven vacuous by construction (its channel cannot vary under its named mutant)?  Is any owed row MISSING from
    the floor as you enumerate it?  Does the gate pin (N by literal equality) need anything else?
Q4. Your own pass-1 claims that the rulings ADOPTED: P4's reachability (codex:15), the CHANNEL corrections
    (codex:112-118), the partition corrections (codex:56-62), the additional MVME187 owner-mismatch finding
    (codex:169).  Scrutinise each MORE than the others; say which you would now weaken or withdraw.
Q5. The build spec's order of operations, by pointer to the ruling ids: anything that must happen BEFORE something
    the rulings put after it (e.g. the PRETABLE before table 1; the frozen-witness post-fix run before the detector
    gains rows; the luna boot A/B before or after the kill table)?

## 5. Seats not in the evidence basis

Gemini 4 Argon was NOT FIRED (its transport failed four controls earlier today; dropped by owner ruling until the
account is checked).  Fable 5.1 is HELD by the owner (hold question in `fable5.HELD.txt`).  Neither is agreement; say
in your verdict line that the basis is FOUR reviewing seats.
