# Codex farm (2026-09-26) -- FINAL dispositions, batch by batch

Owner 2026-09-18/-26: "push codex extremely hard"; 2026-09-24: "Have Fable and Astra adjudicate findings".  Each batch
is: the farmed codex answers (`codex_<job>.txt`; the four f1a answers and the three f1b kill-row answers are from the
`gpt-daybreak-blue-latest` fallback at ultra after GPT-6 Astra refused the briefs at the content filter -- recorded by
their actual model) -> the Fable seat's adjudication (`adjudication/fable_f1*.md`, claude-fable-5-1, verified by
`agent_models.py`) -> GPT-6 Astra's confirmation (`adjudication/codex_astraconfirm_farm_f1*.txt`, gpt-6-astra at
ultra, no refusal).  A disposition is FINAL here only when both have ruled; Astra's amendments are applied below, and
where Astra overturned a Fable ruling the Fable position is kept beside it in its own words (never false unanimity).
Nothing is fixed by this record; every "next action" is a round of its own, with its own panels.

---

## f1a -- sgirekills, pcc2widthkills, pcc2c040kill, vmedefaultkill (Daybreak answers)
## Fable: 1 adopt, 3 adopt-with-changes.  Astra: 0 of 4 wrong, 2 amended.

* `sgirekills` -- ADOPT, HIGH.  Re-scope to the FIVE reachable MTE command exits in `dev_sgi_re.c` (six active
  `exit(1)` at HEAD, one of them the dead third width arm owned by `sgimtewidth`).  Next: the rung-3 witness first, one
  session per site on unmodified `-E sgi -e ip32`, starting with STIPPLE (`sw 0x400`, state-independent); then the
  design brief with `do_mte_transfer()` inlined.  Fable's additions: two UNLATCHED guest-drivable `fatal()`s (floods,
  LOW), the de-escalation ACCEPT rows owed for the LINEAR arm, and a gate home for `sgi_mte_fill_probe.py` (unwired).
* `pcc2widthkills` -- ADOPT WITH CHANGES, LOW (no guest-visible defect at HEAD; an L2-class detector obligation).  Pass
  14 must include its OWN valid pass 2; gate pin to 269 in both halves with the 18 names; records (commits field,
  retitle to the direction split, `gate_arm.sh` "ten of twelve" comment, OUTSTANDING_BUGS in-place corrections);
  downgrade `sev` on retitle.  Missed: `pcc2_width_probe.py`'s `c040ok()` stale comment; the pass-14 draft
  `fix_pcc2_p15.py` has no recorded path.
* `pcc2c040kill` -- ADOPT WITH CHANGES; the CLOSE is held to five conditions, each landing in the closure commit:
  (1) file the GENCTL read-only-bits defect as its own MED row first (fix shape `(old & 0x78) | (idata & 0x87)`);
  (2) record or fire `pcc2c040ctlq`'s owed pass 2; (3) name the open descendants by id -- AMENDED (Astra): "five existing
  unresolved rows plus the newly filed mask row -- six total", not "five open descendants"; (4) the records L4s,
  including the false `dev_pcc2.c:374-378` sentence, which must be corrected first or in the same commit;
  (5) AMENDED (Astra): `check_stage_panels.py` covers only `assess`/`research`/`review` (its stage list, `:65`, and the
  loop at `:190`), so it cannot settle the DESIGN stage's seat coverage -- reconcile that separately.
* `vmedefaultkill` -- ADOPT WITH CHANGES, HIGH (one aligned guest load on an in-tree machine ends the process, no
  diagnostic).  Next: the rung-3 witness in BOTH directions, free-running, with the controls; then the design brief
  carrying the population split.  The population-2 decision (FAULT vs BACKED ACCEPT) goes to the OWNER with Fable's
  evidence: the in-tree OpenBSD 2.2 guest source's `vme2chip_init()` reads uncased `0x28` at attach, so blanket FAULT
  turns today's host kill into a guest panic at attach, while BACKED ACCEPT lets attach proceed.  AMENDED (Astra):
  upstream's `doc/machine_mvme88k.html` 4.4 transcript is HISTORICAL, not a run at HEAD, and does not show the driver's
  accesses are exhaustively the cased ones -- "Backing the identified registers would remove those particular MMIO
  refusals; successful attachment or boot remains unmeasured.  Stock-boot reachability at HEAD remains unsettled."
  Also: population 3 is 30 lanes if "implemented" means "cased"; commit the untracked `regress/artifacts/
  vmedefaultkill/` files before anything cites them again; OUTSTANDING_BUGS.md "a machine this project actively boots"
  -> "constructs and probes".

## f1b -- armmsrmodekill, fbctrlcmdkill, armthumbabortkill, ppcrlwhighhalf, pit8253lsbnotimer
## Fable: 2 adopt, 3 adopt-with-changes.  Astra: 1 of 5 wrong, 2 amended.

* `armmsrmodekill` -- ADOPT WITH CORRECTED CHANGES, HIGH (Astra overturned one of Fable's changes).  The shared atomic
  mode validator before Save at the three transition sites, the two `default:` arms kept as LATCHED `(once)`
  tripwires, and one added SPSR-return witness session (SVC32, `MSR SPSR_c,#0x14`, `MOVS pc,lr`) BEFORE the first run.
  OVERTURNED (Astra): Fable's item 3 said the `bdt_load: unimplemented mode` halt (`cpu_arm_instr.c:1795-1799`) "stays
  unreachable after the fix -- no edit, one sentence".  It is LIVE and the validator cannot protect it: `:1612-1618`
  clears `s_bit` for USR32 and still sets `return_flag` when the list holds r15, and the mode switch at `:1784-1799`
  has no USR32/SYS32 case, so a user-mode `LDM ... {..., pc}^` halts the emulator BEFORE Save at `:1806`.  Record it as
  a live sibling (the absent-SPSR case: USR/SYS have no SPSR) -- a candidate row of its own, not a sentence.  Also
  AMENDED: the SA110/SA1110 architecture argument covers the reviewed vehicle only; `machine_androidarm.c:148` selects
  a Cortex-A5 (SnapdragonS2), so "every in-tree ARM CPU" is false.
* `fbctrlcmdkill` -- ADOPT, HIGH.  Member 3 with its own latch (`warned_command`).  The round owes two rows the answer
  stated but did not list: the COMMAND cell holds the refused value after the decline, and one announce per DEVICE
  across two different unknown opcodes, independent of `warned_port` in both directions.  Widths sb/sh/sw/sd in scope.
  Witness first on unmodified `-E testmips` (`sw 3` to `+0x10`).
* `armthumbabortkill` -- ADOPT WITH CHANGES, HIGH (weakest of the three).  Delete the halt CONDITIONED on the abort
  having been delivered (else fall through so `pc += 2` runs), latched `fatal()`s, keep the fetch-site halt on the
  no-exception branch, FILE `:1557`'s CACHE_INSTRUCTION-on-a-data-load as its own row, add a refusing-device control
  cell, records corrections; reopen the witness attempt on cold CATS.
* `ppcrlwhighhalf` -- ADOPT, MED.  Recover MB/ME from `iword`; the answer's accept-side row set.  AMENDED (Astra):
  delete "PPC970 is the bare/test default only" -- `machine_macppc.c:182` selects PPC970 for the G5 subtype
  (registered at `:210-211`); OS-boot reachability remains unestablished.
* `pit8253lsbnotimer` -- ADOPT WITH CHANGES, MED.  The one-byte write ARMS conditioned on the programmed format; the
  shared completion helper; latch `:198`/`:200` in the same diff; fix together with `i8253zero`.  AMENDED (Astra): the
  shared-format dependency is `pitmodebyteshared` (OUTSTANDING_BUGS.md:20787), NOT `pitclobber` -- the ledger
  (`ledger.json:47119`) distinguishes them; `pitclobber` is the different latch-command defect.

## f1c -- agentrefusal, crimectllane, ledgerstates
## Fable: 3 adopt-with-changes.  Astra: 3 of 30 dispositions wrong, 4 amended.

* `agentrefusal` -- ADOPT WITH CHANGES.  A harness round: port `_scratchpad/agent_models.py` to a tracked
  `tools/pipeline/check_agent_credit.py` (one structured `agent: <id>` field; two rendered states -- transcript root
  absent = loud UNVERIFIABLE, soft; root present and the agent missing or mismatched = FAIL), wired above the
  clean-tree exit, forward-only, with six controls; `seat_scorecard.py` excludes NOTSEAT entries.  L4 now:
  `hygienecensus[24]` gains `[NOT A SEAT ANSWER]`; the witness text and OB:22010 counts corrected.  AMENDED (Astra):
  the NOTSEAT token is what section H reads (through `stage_tokens`, `check_stage_panels.py:184-188`), NOT G --
  `check_seats_read.py:117-125` collects citations with no token filter.  The provenance-receipt schema is an OWNER
  decision.
* `crimectllane` -- ADOPT WITH CHANGES.  The lane model does not wait on driver evidence (the width arm already maps
  `+0x08` to bits 63:32 and `+0x0c` to 31:0); the witness is a two-row addition to R17; the fix lands only AFTER #529
  commits.  AMENDED (Astra): the low CONTROL bytes are covered by "+0x0c at length 4, or +0x08 at length 8" (Fable
  had `+0x08` at length 4).  OVERTURNED (Astra), SEVERITY: **HIGH, not MED** -- a 32-bit write of `0x800` to `+0x08`
  (reserved high-word bits on the header's model) stops all CPUs (`dev_sgi_ip32.c:337-343`) and in ordinary execution
  `emul.c:1052-1059` ends emulation and `main.c:807-821` returns from the process; "the existing legitimate full-width
  reset does not exempt this unintended termination".  Fable's MED argument, kept in its words: "the lane defect grants
  a guest no capability it lacks through the modelled 64-bit HARD_RESET (a reset the guest may legitimately request);
  what it produces is guest-visible behaviour contrary to the header".  Adopted: HIGH, by the severity rule both
  applied (HIGH = a guest can end the emulator process); the MED argument bears on REACHABILITY RANKING, not severity.
  **The #529 records file this row as MED and are corrected to HIGH before #529 commits.**
* `ledgerstates` -- ADOPT WITH CHANGES.  Of the codex's eleven: `exitcensus`, `mapledmaaddr`, `ppcrldimimask`,
  `ppcrlwimiwidth`, `xscaleinten` close on their records with mechanical companions (`closure.by`, superseded notes);
  `alphaswpctxreg`, `otherkilldeath` (FIXED by #499, not "superseded"), `ip30abortkill`, `sgirekills` close on named
  conditions; `adjudglmtag` must NOT close (live at HEAD: `tools/adjudicate.sh:89` fires `glm-5.3:cloud`, `:103`
  checks `glm-5.3-flash`; the fix is uncommitted).  AMENDED/OVERTURNED (Astra):
  - `adjudglmtag`: keep `open`, not `in work` -- no current claimant is recorded (`ledger.json:47654`, `:47668`,
    definitions `:54769-54771`).
  - `gxprobepccache`: **KEEP OPEN** (Fable said close with a note) -- `fix_20260831/WHY_THIS_COPY_EXISTS.md:25` calls
    the committed copy inactive evidence and `:30-33` files the TRACKING question under this row; preserving the
    repair does not discharge it.  An owner question.
  - `sgirekills`: transfer only the FIVE exits into a HIGH child if ownership is split; the dead width arm is
    DUPLICATE `sgimtewidth` (OB:14735-14740), not part of the child.
  - `ip30abortkill`: retain the hold, but the current instrument is 33 rows (CL:2360;
    `ip30abortkill/killtable5_20260918/base.raw:36`), and the historical 28-row pre-fix obligation (OB:21502) must be
    resolved explicitly.
  Fable's own finding (kept): `untrackeddetectors` entry [2] says both detectors were staged; `crime_width_probe.py` is
  untracked again at HEAD -- #529's commit discharges it.

---

Cross-batch notes: every f1 answer was checked against HEAD `8ea26abb` by both seats; nothing was built or run by
either.  The rows above that name a "next action" are CANDIDATE ROUNDS, ranked HIGH first: `sgirekills`,
`vmedefaultkill` (owner decision owed), `armmsrmodekill` (+ the live USR-mode `LDM ^` sibling), `fbctrlcmdkill`,
`armthumbabortkill`, `crimectllane` (after #529).
