# T36 (`m88kbuserrregs`, round `#570`) -- pass-1 design review: rulings (main loop, 2026-10-23 ~21:50; HEAD 7fca7187 at firing)

Evidence basis: FOUR reviewing seats answered -- GPT-6 Astra as reviewer (`codex_t36p1.txt`, 21,458 b), Grok 4.7
(`grok_t36p1.txt`, 32,125 b), GLM 5.3 (`ollama_glm_t36p1_Q12.txt` 15,200 b + `_Q34.txt` 10,620 b), DeepSeek
(`ollama_deepseek_t36p1_Q12.txt` 8,062 b + `_Q34.txt` 6,054 b).  All six files were read whole (not the verdict lines);
every verdict is READY WITH CHANGES.  Gemini 4 Argon: NOT FIRED (`argon.NOT_FIRED.txt`, a seat failure, not agreement).
Fable 5.1: HELD by the owner (`fable5.HELD.txt` carries the question).  agy, kimi, minimax, Opus-as-seat: DELIBERATELY
NOT FIRED by roster (`roster_NOT_FIRED.txt`).  **These rulings are PROVISIONAL until GPT-6 Astra adjudicates them from
`adj/packet.md` (section E below is appended from that answer).**  Line refs `<seat>:<n>` are lines of the answer files.

Three facts the main loop MEASURED while ruling (reads of HEAD, 2026-10-23 ~21:45):
* `src/debugger/debugger_cmds.c:1302` -- `pause <cpuid>` TOGGLES `m->cpus[cpuid]->running`.  On mvme187 `-n 2` it
  STARTS cpu 1, which `dev_mvme187.c:136-149` never gave a CMMU (both attach to `cpus[bootstrap_cpu]`), and
  `memory_m88k.c:130-132` translates for a NULL CMMU as physical = virtual.  So Astra's P4 reachability claim
  (codex:15) HOLDS and the three seats that called the NULL cell unreachable (grok:20-22, glm-Q12:10, deepseek-Q12:18)
  reasoned from "only the bootstrap cpu is started", which is a startup fact (`emul.c:747-748`), not an invariant.
* `src/devices/dev_m8820x.c:108` dereferences `cpu->cd.m88k.cmmu[d->cmmu_nr]->reg` for the ACCESSING cpu, while
  `:250-252` use `cpus[d->cpu_nr]`.  A CMMU register access by a running CMMU-less cpu is therefore a host NULL
  dereference today (a pre-existing hazard, C5) and the B5c session must keep cpu 1 off the CMMU window.
* `regress/artifacts/m88kbuserrregs/witness_20261023/` holds exactly one `.py` (`m88k_buserr_probe.py`); the helpers
  are `*.py.txt` / `*.sh.txt`.  GLM-Q34:14's "stored as .py.txt" concern is moot; grok:141 read it right.

## A. The repair -- SETTLED by all four seats, with ONE addition (A6) and one licence upgrade (A3)

* **A1 selector.** `cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]` -- correct for every caller that reaches
  the arm (guest ld/st/xmem -> data; the fetch and the step pre-read -> instruction; NO_EXCEPTIONS callers never reach
  the selector).  codex:9-11, grok:8-14, glm-Q12:6, deepseek-Q12:11.  Multi-cpu luna consistent for the rowed cpu-0
  cells; `-n 2..4` stays NOT CLAIMED.
* **A2 values.** PFSR = `CMMU_PFSR_BERROR << 16` = `0x00030000`; PFAR = `(uint32_t) orig_paddr`, UNMASKED (upstream's
  form; the `(uint32_t)` cast kept, grok:32).  P2 (bits 1:0) is UNKNOWN -- no MC88200 manual on disk; the MC88100 P-bus
  note is about the bus (codex:13, grok:16, glm-Q12:8, deepseek-Q12:15).  Transferred warrant recorded as such; a
  sub-word row is clause (e), not owed.
* **A3 NULL check around the two writes only; `m88k_exception`, the `!no_exceptions` guard, the `debug()` line and
  `return MEMORY_ACCESS_FAILED` outside and unchanged** (all four).  LICENCE UPGRADED: the NULL cell is REACHABLE on an
  unmodified machine through the cold debugger (the measured fact above), so the check is load-bearing (a host NULL
  dereference without it) and is licensed by MEASUREMENT, not only by upstream's warrant.  Consequence in B5c.
* **A4** nothing else in the arm moves (codex:19, grok:24, glm-Q12:12, deepseek-Q12:21).
* **A5 LUNA case** `case 0x3ffffff0:` -> `return 0;`, its PFSR write at `dev_luna88k.c:626` deleted, the case KEPT
  (deleting it reaches `default:`, which stops the cpu).  Path confirmed by all four: `:591-592` does not fire, `res`
  0 -> -1, data CMMU, vector 3, the skipped common tail is inert for a failing access.  A store takes the same path;
  an instruction fetch at that address takes cmmu[0] / vector 2 and then R1 (codex:21, grok:26-28, glm-Q12:14,
  deepseek-Q12:24-26).  NOTE glm-Q12:14: HEAD's case writes cmmu[1] even for an instruction access -- a second wrong the
  fix removes; record it in the CHANGELOG.
* **A6 THE FOURTH PRODUCT FILE.** `#include "thirdparty/m8820x.h"` in `src/cpus/cpu_m88k.c`, placed AFTER the existing
  `#include "thirdparty/m8820x_pte.h"` at `:53` (order matters: `m8820x.h`'s `NBSG` uses `PDT_BITS`/`PG_BITS`,
  grok:32).  Without it the ruled repair does not compile -- the arm is compiled inside `cpu_m88k.c`'s translation
  unit via `tmp_m88k_tail.c:38-40`, and the three macros live only in that header (all four seats; upstream's own
  hunk, `trunk_src.diff:1917-1922`).  GLM-Q12:16's alternative (`#ifdef MEM_M88K` include at the top of
  `memory_rw.c`) REJECTED: upstream's placement is the transferred warrant and keeps `memory_rw.c` arch-neutral.
  `cpu_m88k.c` joins the edit set, the est/ propagation and the two-part clearance; the witness's "three files"
  baseline row is stale (B1).
* **A7 records in product code (P9).** `dev_m8820x.c` becomes a COMMENT-ONLY fifth... fourth-and-comment-only edit
  site: `:293-294` ("writes only PFSR and PFAR (memory_m88k.c:382-405)"), `:325-327` (cites `dev_luna88k.c:614`;
  the write is at `:626` and goes away), `:500-501` ("written at :382-405"), and `:453`'s "only at memory_m88k.c"
  (grok:36-43, codex:25).  The `memory_rw.c:615-619` TODO is replaced by the writes (its minus lines, 3.4).
* **A8 what the records may claim (Q1(h)).** "Metadata for CLAIMED, REFUSED, unsuppressed device accesses that pass the
  running-transition check, plus LUNA's probe case routed into that path" (codex:27).  Must DISCLAIM: unclaimed
  addresses (zeros, no exception, no CMMU write -- R3); on luna-88k every other device refusal still stops the cpu
  before the arm; free-running instruction-fetch refusals (R1); NO_EXCEPTIONS callers; translation-fault semantics
  unchanged; sub-word PFAR without a local warrant; CMMU-less machines unchanged (grok:45-47, glm-Q12:20,
  deepseek-Q12:35).  Never "every 88K bus error now carries PFSR and PFAR".
* **A9 sibling CMMU: `kept` (P3)** -- all four (codex:29, grok:51, glm-Q12:22, deepseek-Q12:38).  The records must NOT
  say "no guest can observe the sibling" (snapshots and diagnostics can differ, codex:29); the hardware latch
  semantics are UNKNOWN.
* **A10 option set (Q1(j)).** Two unnamed members surfaced and both are REJECTED: installing `dev_unreadable` at the
  single address (codex:33, grok:57 -- same outcome by another device; the address is interior to the luna device
  window) and the luna house-style `cpu->running = 0; return 0;` (glm-Q12:24 -- the twin of (4), halts).  (2) stands.
* **A11 P8 -- the LUNA boot is OWED and MEASURED in this round**: before/after boot-to-`login:` of the luna rig image
  (present on this machine) with the base and the fixed binary (`gate_ab.sh:214`'s boot check shape).  If the
  post-fix boot fails, STOP and report (grok:53).  The injected-program rig run is not that measurement (codex:31).

## B. The detector -- SETTLED on shape, pins and gate; the FLOOR has THREE more cells than the witness holds

* **B1 base.** The witness probe moves to `regress/m88k_buserr_probe.py` (the frozen witness copy stays where it is
  for the ledger term).  Header edits BEFORE the move: the `no_exceptions` NOT-CLAIMED sentence gets the right reason
  (B5b; the current "never reach a DM_DEFAULT handler" is wrong-reason -- the arm IS reached, its `!no_exceptions`
  conjunct is what keeps the body out, grok:92, codex:59); the VA != PA sentence must not say the session cannot
  translate (a programmed BATC separates them, grok:94); the edit set names FOUR product files; the claim limit of A8;
  the `icmmu` wants stay `kept`; the variant table is marked DATED PREDICTIONS until the legs run (glm-Q34:10);
  "the cmmu[0] cell is the round's to build" becomes the outcome (B5a).
* **B2 clause (a).** The witness (16/24, eight symptom reds, controls green) is clause (a).  OWED: the same FROZEN
  script post-fix = 24/24 `SYMPTOM=ABSENT`; and the FINAL detector's own pre-fix/post-fix pair (codex:37).
* **B3 clause (b)** at every fixed site, two legs: ARM reinstated / case fixed -> predicted 16/24 (uld/ust/vme pfsr+pfar,
  `luna pfsr`, `luna pfar`; `luna route` green); CASE reinstated / arm fixed -> predicted 22/24 (`luna route`,
  `luna pfar`; `luna pfsr` green).  All four seats concur with the prediction (codex:39-46, grok:63-68, glm-Q12:30,
  deepseek-Q12:52).  The MEASURED scores are what the record carries.
* **B4 clause (c).** Null medium = an exit-1 non-emulator stub (plus the absent-binary shape).  Record form NOW:
  `(c): measured at <artifact>` -- no gate pin exists yet, so by-construction is not available at pass 1 (codex:52,
  grok:70, glm-Q12:32).  Predicted from the source: exit-1 stub -> **1/24** (`neg apparatus` passes by design),
  `CONTROL=FAIL`, `SYMPTOM=MIXED`, exit 1, sentinel printed; absent binary -> `FileNotFoundError`, NO sentinel, no row
  score (grok:72-78, codex:50).  DeepSeek-Q12:55's "0/24, no sentinel" is the wrong prediction for the exit-1 stub.
  **Do not write 0/24 anywhere; write the measured number.**  GLM-Q12:32's "build without dev_m8820x.c" alternative
  NOT adopted (ambiguous medium).
* **B5 clause (d) -- the floor, cell by cell.**  The carrier's DEPENDS-ON rule enumerates the predicates DOMINATING
  the edited lines (not only the ones the diff adds) crossed with the device-state lvalues the repair path reads,
  for cells that are JOINTLY REACHABLE; a cell is FLOOR when its reachability is measured.  Three cells meet that:
  * **B5a P5 instruction label -- FLOOR, rows OWED** (Astra codex:71,77; GLM-Q12:34,46; DeepSeek-Q12:59 -- against
    Grok:90, clause (e)).  The fix ADDS the selector; its (d) weakening (always-data) is a plausible edit; the cell is
    REACHED on HEAD (the witness's `INFO ifetch` line: `path=v2 SXIP=0xfff46013`, the instruction CMMU keeping its
    seeds).  Rows: `ifetch route` (v2, SXIP 0xfff46013), `ifetch pfsr` (0x00030000; RED on HEAD), `ifetch pfar`
    (0xfff46010; RED on HEAD), `ifetch dcmmu` (data seeds kept) -- the INFO line scored, on the mvme187 `unreadable`
    window.  DISCLOSED in the contract and the row comments: the channel is the step loop's pre-read (R2); when R2
    is fixed the rows red for an unrelated reason (the step's own fetch then hits R1's halt) and are re-rooted when
    R1/R2 land (glm-Q34:24).  Grok's fragility objection is answered by that disclosure, not by dropping the rows.
  * **B5b P6 `no_exceptions`-set -- FLOOR, one row OWED** (Astra codex:72; DeepSeek-Q12:60; GLM-Q34:30's cheap row --
    against Grok:92 and GLM-Q12:34).  `!no_exceptions` at `memory_rw.c:603` DOMINATES the writes; dropping that
    conjunct is the least-restrictive weakening, and the set cell is reachable on an unmodified machine by any
    debugger read of a refusing address (`debugger_cmds.c:716-717` passes `CACHE_NONE | NO_EXCEPTIONS`).  GLM-Q12:34's
    "already killed by `ok regs`" is wrong: `ok regs` is a SERVED access (`res = 1`) and never exercises that conjunct.
    Row `dbg noexc`: in an existing mvme187 session, after the seeds, a debugger `dump` of the `unreadable` window;
    wants: zeros returned, all four seeds unchanged, no vector taken, cpu running.  Kills "`!no_exceptions` dropped"
    (the seeds would change to 0x30000/the address and an exception would be raised from a debugger read).
  * **B5c P4 NULL CMMU -- FLOOR, two rows OWED** (Astra codex:70 -- against Grok:20-22, GLM-Q12:10, DeepSeek-Q12:18,
    whose unreachability premise the `pause` fact above refutes).  Session: mvme187 `-n 2`; both cpus start at one
    pc (`emul.c:742-745`), so the probe's program begins with a RAM-flag dispatcher -- cpu 0 (the only running cpu
    until `pause 1`) sets the flag and takes the seeded path of the existing `uld` session; then `pause 1` +
    `continue`: cpu 1 sees the flag, sets its own VBR, performs the refused load from the `unreadable` window, and
    its handler stores a HANDLED marker to RAM while the fall-through after the load stores a FELL marker.  cpu 1
    must NOT touch the CMMU window (`dev_m8820x.c:108`, C5).  Rows: `null surv` (the session is alive -- kills "NULL
    check removed", a host NULL dereference) and `null route` (HANDLED set, FELL clear -- kills "exception moved
    inside the NULL check").  `-n 2` is a documented command-line option of an in-tree machine, not a machine edit;
    the ladder's clause (iii) is met.  The adjudicator is asked to be HARDER on this cell than on the others (D1).
  * **P7 VA != PA, P10 LUNA store, P2 sub-word -- CLAUSE (e)**, disclosed with corrected reasons (all four: codex:73-75,
    grok:85-88,94, glm-Q12:34, deepseek-Q12:61-64).  P7's reason: `vaddr` is not an operand the m88k arm reads (the
    MEM_MIPS block is compiled out), and the sessions leave the APR invalid -- NOT "the session cannot translate".
* **B6 variants -> rows.** Grok:98-111's table is adopted as the PRETABLE's CHANNEL column, with Astra's CHANNEL
  corrections (codex:112-118: a read-only repair changes `ust pfsr/pfar`, not `ust route`/`ust icmmu`; a device-keyed
  repair changes the excluded device's metadata rows, not its route/sibling rows; a global widening can fail a
  PREREQUISITE before the named channel -- the header names the channel actually available; `luna pfsr`'s unique
  variant is "write deleted while still served"; FIVE route rows, four green on HEAD).  Each named variant reds at
  least one row; the (e) variants (NULL removed / exception inside NULL -- now B5c; PFAR := vaddr; sub-word) are
  recorded with their disposition.
* **B7 accept controls.** `ok route` + `ok regs` are the served cell (P11); no population-2 row (that is `#568`'s 38,
  unchanged); no translation-fault row (P12; `memory_m88k.c` is not edited) -- all four.  `ok regs` is the right
  channel for "a served access writes no metadata".
* **B8 anchor and D2.** R11 discharged by the three absolute PFAR pins (0x10/0x90/0x0 device-relative vs absolute);
  a +4 shift reds `uld pfar`, `vme pfar`, `luna route` (glm-Q12:40).  D2: the one compare the fix depends on is
  `res <= 0` with 0 mapped away (served = `ok` rows, refused = every refused row) -- discharged; the LUNA window
  compares cannot jointly reach `addr == 0x3ffffff0` -- record that discharge, add no boundary rows (codex:126).
* **B9 PRETABLE corrections** (records, no rows): include the translation-success/early-return conditions, the outer
  device-range check, the device match and the LUNA early-window exclusions in the partition; row 3 is "running
  before and stopped after"; call / suppression / normalised result are coupled; device names are SAMPLES, not a
  body partition; instruction x write is unreachable; alignment residues per width (codex:56-62).  Row 10 relabelled:
  `paddr` is read by the arm's `debug()` outside the guard -- legitimate extra coverage, not a body-read swap
  (glm-Q34:30).  S16's wording: the arm compiles as part of `tmp_m88k_tail.c`, included into `cpu_m88k.c`'s unit
  (deepseek-Q34:52).  Section 7's floor sentence is replaced by B5.
* **B10 gate home: GATE 14** (`gate_arm.sh`), placed AFTER `arm_flags_probe.py` in `#568`'s position, dummy 4-byte
  LUNA image shape (the rig shape measured identical) -- all four; gate 11 would make an image-independent detector
  hostage to the rig image.  Pins in `#568`'s form: the row list held in the gate, each name once via
  `count "$LOG" "^$v  .*ok$"` (names carry spaces; the `%-16s` format and the 15-char assert keep it satisfiable),
  rows run = N and rows correct = N by LITERAL equality where N is the FINAL count (24 + the B5 rows), red = 0,
  `M88K_BUSERR_CONTROL=OK` x1, `M88K_BUSERR_SYMPTOM=ABSENT` x1, sentinel `M88K_BUSERR_PROBE_DONE` x1; no `check_min`;
  the controls are inside the identity list (all four; codex:153-155, grok:143, glm-Q34:16, deepseek-Q34:24).
* **B11 MANIFEST** (`tools/pipeline/check_probe_wiring.py`): `CLASS_DETECTOR` for `regress/m88k_buserr_probe.py`
  (gate home + pin count in the line), `CLASS_WITNESS` for `artifacts/m88kbuserrregs/witness_20261023/
  m88k_buserr_probe.py` (the directory's only `.py`).  Read the peer-edited checker at HEAD when editing.
* **B12 ledger witness term** `probe:regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` (rung 3;
  it must not imply instruction-fetch or boot coverage, codex:157).
* **B13 gates and stay-green set.** Gate 1 (build), GATE 14 (the new block), GATE 11 (its probes sit over the edited
  `dev_m8820x.c` and `dev_luna88k.c`; the luna rig image is present, so it runs here -- glm-Q34:20), `grep 3ffffff0`
  over committed probes, `vme_default_probe.py` measured 38/38 (pin unchanged), the A11 boot A/B.
* **B14** one ask-again after a clean table; no second ask-again.

## C. Findings outside the diff -- FILED as rows in T36's landing

* **C1 R1** (MED, guest-cpu-stop / wrong-result): a refused m88k instruction fetch takes vector 2, then
  `cpu_m88k_instr.c:2989-2993` reaches the dyntrans `bad:` tail (`cpu_dyntrans.c:1983-2014`), which stops the FAULTING
  cpu and requests the debugger before the handler runs.  Multi-cpu unmeasured; the transcript's "All machines
  stopped" is a one-cpu machine.  Prerequisite for a FREE-RUNNING instruction row only (all four).  Carries T36's
  stepped `ifetch` rows as the re-root obligation.
* **C2 R2** (LOW, debugger changes guest-visible state): the step loop's disassembly pre-read is `CACHE_INSTRUCTION`
  without `NO_EXCEPTIONS` (`cpu_dyntrans.c:287-290`); scope includes tracing and the delay-slot display (codex:165).
  No committed probe's SCORED rows depend on it (grok:153; `#568`'s vector-3 pins would shift under a firing
  pre-read, glm-Q34:26).
* **C3 R3** (research, doc-gated): an unclaimed physical address raises no bus error on m88k (`memory_rw.c:662-713`,
  upstream TODOs at `:682`, `:709-710`); whether real MVME187/LUNA hardware asserts BERR* there is a board question
  (`vmesbcp2.txt:341-348` headings; body not located).  Not a fix round; T36's contract disclaims the path.
* **C4 Astra's additional finding** (LOW, host NULL dereference under a documented option): `dev_mvme187.c:136-149`
  attaches the CMMUs to `cpus[bootstrap_cpu]` but registers the register windows with `addr2=0/1`, so
  `dev_m8820x.c:542-543` decodes `cpu_nr = 0`; with the random-bootstrap option (`emul.c:510-511`, set at
  `main.c:450`) and `-n >= 2`, the decoder's `cpus[0]->cd.m88k.cmmu[..]` is NULL and `:251` dereferences it
  (codex:169).  Reading, unmeasured; filed by name.
* **C5** (LOW, host NULL dereference, pre-existing): `dev_m8820x.c:108` dereferences the ACCESSING cpu's
  `cmmu[d->cmmu_nr]` without a NULL test, so a CMMU register access by a running CMMU-less cpu (the `pause 1`
  configuration of B5c) dies.  Measured by reading while designing B5c; filed by name; B5c's session avoids it.

## D. What the builder owes -- `BUILD_SPEC.md` (written after section E lands)

The repair of section A (four product files, est/ propagation, two-part clearance on build/, build-asan/,
/tmp/gxsec-build; est/ is a source tree), the detector of section B (24 + 7 rows: `ifetch route/pfsr/pfar/dcmmu`,
`dbg noexc`, `null surv`, `null route`), the PRETABLE written BEFORE table 1 with B6/B9, the legs (a) frozen-witness
post-fix, (a) final detector pre/post, (b) two reinstatements, (c) exit-1 stub + absent binary, (d) the enumerated
variants in the kill table from a frozen copy in a WSL scratch clone, the gate-14 block and MANIFEST lines, gates 1 /
14 / 11 / the 38-row pin, the A11 boot A/B, and the records (CHANGELOG `#570` block, OUTSTANDING_BUGS, ledger).

## E. ADJUDICATED by GPT-6 Astra, 2026-10-23 ~21:55 (`adj/codex_t36p1adj.txt`, 12,342 b): VERDICT AMEND -- "retain the
## repair, withdraw C5, correct several rationales, and close the missing instruction/NULL joint cell before certifying
## the row budget".  Evidence basis: FOUR reviewing seats (Astra-as-reviewer, Grok, GLM 5.3, DeepSeek); Argon NOT FIRED
## (seat failure); Fable HELD.  Sections A-D above are the PRE-adjudication record; where E differs, E rules.

**UPHELD:** A1, A2, A4, A5, A8-A11; B2, B4, B5b, B7, B11-B14; C1-C3.  Astra's least-certain upholds: A2/A9 (hardware
semantics rest on the transferred warrant, the MC88200 manual being absent) and B5c (the session is unmeasured); A11 is
an OWED measurement, not an existing receipt.

**AMENDED (each confirmed by the main loop reading the cited lines before this edit):**
* **C5 -- REJECTED, WITHDRAWN.**  `m8820x_command(struct cpu *cpu, ...)` at `dev_m8820x.c:106-108` is called at `:284` with
  `c`, the OWNING cpu selected at `:250` (`cpus[d->cpu_nr]`); the parameter is not the accessing cpu.  No accessor-NULL
  dereference follows.  The B5c prohibition "cpu 1 never touches the CMMU window" is withdrawn with it; keeping cpu 0's
  seeded state isolated from cpu 1 is a separate design concern.  (A reading error of the main loop's, caught by the
  adjudicator: the function boundary was not read.)
* **A3** -- the licence stays "transferred warrant" until the B5c rows MEASURE the delta; source inspection establishes
  reachability, not a measured delta (the addition rule).
* **A6** -- placement upheld (after `m8820x_pte.h` in `cpu_m88k.c`); the "order matters" rationale is withdrawn
  (`NBSG`'s macro replacement list does not require its names to be defined first).  GLM's guarded include is viable but
  not chosen; the substantive issue is the missing definitions.
* **A7** -- exactly FOUR product files, `dev_m8820x.c` comment-only; `:453` does not literally say "only" -- correct the
  incomplete writer citation without inventing a quotation.
* **B1** -- edit the PROMOTED copy; the frozen witness stays byte-identical.
* **B3** -- the 16/24 and 22/24 predictions belong to the 24-row witness instrument, not to the expanded detector's
  denominator.
* **B5a / B6 -- `ifetch route` is VACUOUS against the always-data metadata selector**: the exception-vector expression at
  `memory_rw.c:620-622` reads `cache` independently of the selector the fix adds (confirmed), so the route row cannot
  vary under that mutant.  It is kept as an attribution CONTROL (v2 / SXIP) with a named variant of its own (the
  exception dropped or mis-routed); `ifetch pfsr` / `ifetch pfar` carry the selector mutant.
* **B5c -- the INSTRUCTION x NULL JOINT CELL IS OWED.**  {data, instruction} x {CMMU present, absent}: the existing rows
  hold data/present, B5a instruction/present, B5c-as-drafted data/absent; instruction/absent is source-reachable (the
  same NULL translator and the same arm) and unobserved.  Closed CONJUNCTIVELY by the two NULL rows: cpu 1 performs the
  refused DATA load first (handler -> HANDLED marker), then JUMPS INTO the refusing window (an instruction-fetch refusal:
  the arm with `cache == CACHE_INSTRUCTION` and `cmmu[0] == NULL`, vector 2, then R1's tail halts cpu 1 and returns to
  the debugger).  `null surv` = the session reaches that point alive with both markers readable; `null route` = HANDLED
  set, FELL clear.  Termination made explicit: breakpoints belong to the machine (`cpu_dyntrans.c:1802-1804, 1846-1848`),
  so cpu 0 parks in a self-loop after its handler and must not end cpu 1's observation; the markers are initialised,
  attributable to cpu 1, and read after completion under either outcome.  A survival control with a real channel
  discharges the floor obligation; the label does not change its evidentiary value.  One more leg: the NULL check
  CONDITIONED on the data label (the `#499` shape) -> `null surv` red only if cpu 1 reaches its instruction fetch.
* **B8** -- the anchor is the DIRECT REGISTER WRITE (model) versus the GUEST DECODER (probe): a shifted decoder fails the
  PFAR observations.  GLM's +4 argument (glm-Q12:40) is withdrawn -- it moves the probe's addresses, not the product's
  decode, and a moved window base can leave the interior access and `orig_paddr` unchanged.
* **B9** -- name the body being enumerated: `paddr` is read INSIDE the outer refusal guard (`:603-607`, `debug()`) and
  outside only the proposed inner NULL guard; distinguish PFAR-VALUE corruption from a guard-OPERAND swap.
* **C4** -- upheld CONDITIONALLY: the owner mismatch exists when the selected bootstrap cpu is NONZERO; the random option
  alone does not guarantee it.  Source-derived, unmeasured.

**D1-D5 RULED:** D1 reachability UPHELD (admissible under clause (iii): a cpu-count option plus a debugger command change
configuration and execution state, not the machine description or dispatch; `machine.c:707-711` executes every
`running` cpu); D2 UPHELD -- GLM's "RED for an unrelated reason" is right and Grok's "GREEN" is wrong (with R2 fixed the
real fetch reaches R1's failure path and the handler prerequisite at probe `:433-434` fails); D3 UPHELD -- `ok regs`
(`res = 1`) cannot see the dropped conjunct; the new row must observe preservation before a later fault overwrites the
evidence; D4 UPHELD -- 1/24 exit-1 stub (`neg apparatus` accepts `exit1/absent` at probe `:492-495`), absent binary =
uncaught `FileNotFoundError`, no sentinel (`run_piped()` catches timeouts only, `:333-348`); D5 placement UPHELD.

**Q3 -- what literal N additionally needs:** the DISASSEMBLY CENSUS re-derived for the new sessions (the frozen
`115/115` covers five scored sessions; the instruction INFO is excluded at probe `:556, :572-576`); prerequisites for
every newly scored session; the disclosure that gate 14's earlier skips (`gate_arm.sh:100-105`) can prevent reaching the
new pins -- a downstream equality pin does not prove execution, and B4's measured leg is not a claim about every gate
invocation.  The bounded exclusions (VA != PA, sub-word PFAR, LUNA store, translation-fault semantics) stand; the joint
cell does not license cpu-number, address-value or device-name products.

**Q5 -- ORDER:** (1) the corrected PRETABLE, with the joint cell and the actual CHANNEL assignments, before the first
table; (2) the frozen witness's same-script post-fix receipt; the expanded detector developed as a separate copy with
its own pre/post pair; (3) every reinstatement / null-medium / weakening result tied to the exact instrument revision
and denominator, the instrument frozen before its table; (4) the LUNA boot A/B BEFORE the mutation work (a failure
stops the round; no rule mandates the order, prudence does); (5) identities, counts, census and MANIFEST finalised
from the completed detector; the single ask-again on the clean table.
