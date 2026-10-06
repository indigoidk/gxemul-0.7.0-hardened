
## 2026-10-02 -- GXEMUL [087a90]: `#558` -- agy's audit of `#555`'s id-less table: 16 flags; one opened THREE MB89352 emulated-CPU-stop rows, the rest changed nothing

**What this is.**  `#555` gave ids to the prose entries of this file and committed its tables under
`regress/artifacts/idless_20261002/`.  The owner's standing instruction (2026-10-02) is to keep agy busy on read-only
audits and to take its FLAGS as facts to check while giving its agreement no weight.  Six briefs were generated from the
committed tables (`regress/artifacts/idlessaudit_20261002/briefs/`; generator `mk_agy_idless2.py.txt`): two on the
citations of the forty `#555` rows, three on the 104 passages `#555` points at an existing id, one on the 22 entries it
ruled KEEP-AS-IS or UNSETTLED.  Five answered; `icite2_2` WALLED on launch (`error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.`).

| brief | agy's verdict | flagged items |
|---|---|---|
| `icite2_1` | 0 of 20 rows flagged, 0 not checked | -- |
| `icite2_2` | SEAT WALLED (agy quota: Resets in 101h48m29s) | -- |
| `ifiled2_1` | 4 of 35 passages flagged, 0 not checked | 15, 24, 26, 27 |
| `ifiled2_2` | 0 of 35 passages flagged, 0 not checked | -- |
| `ifiled2_3` | 1 of 34 passages flagged, 0 not checked | 28 |
| `ikeep2` | 11 of 22 entries flagged, 0 not checked | 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 |

**The 16 flags, read against the committed table** (`AGY_FLAGS_DISPOSITION.md`, v2; v1 was checked by GPT-6 Astra,
`aconf_agyflags/codex_aconf_agyflags.txt`: 1 of 16 dispositions wrong -- the one wrong disposition is #27 below, and v1's framing of the
eleven OWED flags as "clause-(e) debt that a live row exempts" was also wrong and is corrected):
* **5 PARTLY** -- a passage pointed at an id that covers only part of it.  For four, the "left-out" item is
  carried by a row the brief did not name: three filed by `#555` on the SAME queue lines (`qhscifssr`, `qhnetxlog`,
  `qhslowifetch`) and one filed by `#554` from queue lines 18721-18722 (`armcp15cp14exits`, for #28's lines
  16997-17000); the brief had named only the POINTER id, so agy read the pointer, found it partial, and said so --
  correctly, of the pointer.  **The fifth (#27, passage 2616,
  "dev_mb89352 fatal errors") is a real gap**: `qhm88kstops` carries ONE of the device's nine `cpu->running = 0` assignments (ten stop
  messages: EXBF's write and read logging share one assignment).
* **11 OWED** -- a KEEP-AS-IS entry whose work is not done at `c29a5fd3`.  All eleven are the entries `#555` kept
  because an existing row already records the open work, in those words, in its own queue text; the carriers
  (`armbfiwidth`, `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`) are open or in work.  `#555` dropped nothing; whether a carrier owes its work is the carrier's question.

**The three rows this opens** -- Astra's finding (`aconf_agyflags`), grok's ruling (`grok/grok_mbstops.txt`: CONCEDE IN
PART), Astra's confirmation against the source at `c29a5fd3` (`aconf_mbstops/codex_aconf_mbstops.txt`: CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).  Of the
nine `cpu->running = 0` assignments in `src/devices/dev_mb89352.c`, `:146` is `qhm88kstops`, `b120` carries the unknown-CDB producer omission and its empty-status
consequence at `:176`, `:290` is dead; the rest, three fix shapes, three rows, each HIGH by the `qhm88kstops` grade, each saying that its reachability
is established by source inspection at `c29a5fd3`; no runtime witness was measured:

#### `qhmbphasestops` (HIGH, filed by #558) -- An MB89352 data-register access, with a transfer object and a nonzero count, in a phase unsupported for the access direction stops the emulated CPU
SITES (c29a5fd3, src/devices/dev_mb89352.c): :169 (DREG read, phase outside DATAIN/STAT/MSGIN) and :235 (DREG write, phase outside DATAOUT/CMD).  :290 (the end-of-write default:) is UNREACHABLE: the first switch returns only for unsupported phases, and DATAOUT/CMD break, reach the second switch with no intervening phase change, and exhaust its supported cases.  PREREQUISITES: every DREG helper call needs a NONZERO count before decrement (a zero-count access only warns) and these guards additionally need a transfer object -- 'unconditional' means independent of the abort flag, nothing more.  REACHED BY (by reading, not measured): SCMD/PCTL give the guest control of the phase.  FIX SHAPE: keep the CPU running while KEEPING the helper's early return (:170 / :236) -- the treatment #186 gave the XFR command at :507.
#### `qhmbunimplstops` (HIGH, filed by #558) -- An MB89352 access with a non-byte length, an unhandled SCMD write, or the EXBF register stops the emulated CPU while mb89352_abort_on_unimplemented_stuff is fixed true
SITES (c29a5fd3, src/devices/dev_mb89352.c): :312 (len != 1: a halfword or word callback access), :533 (an SCMD WRITE outside {0x00, 0x20, 0x84, 0x8c, 0xc0} unless bit 0x10 rewrites it to BUS_REL -- an SCMD read does not execute this switch), and EXBF, register index 15: WRITE logging at :676 and READ logging at :683 converge on the ONE assignment at :690.  All gated by const bool mb89352_abort_on_unimplemented_stuff = true (:61), so live; the shared fixed-true policy is what groups them.  REACHED BY (by reading, not measured): those accesses from the guest's register interface.  FIX SHAPE: the warning branch the flag already selects; clearing the flag leaves all five live unconditional DREG assignments (:146, :169, :176, :235, :242; :290 is dead) intact.  NOT mb89352halt's stop: that dropped row's record names the disk dispatcher's CDB default: and the controller's status-length guard, not :533.
#### `qhmbbufendstops` (HIGH, filed by #558) -- An MB89352 data-register access at or past the end of the selected buffer, in a phase supported for the access direction, stops the emulated CPU
SITES (c29a5fd3, src/devices/dev_mb89352.c): :176 (DREG read, transfer_bufpos >= len against the selected DATAIN, STAT or MSGIN buffer -- read completion changes phase WITHOUT resetting the cursor, so a subsequent nonempty buffer can meet this guard, not only the original DATAIN buffer) and :242 (DREG write: reachable through empty or unprepared outgoing-buffer states; an exact fill runs completion and can change phase so a further write reaches :235 instead).  PREREQUISITES: a transfer object and a nonzero count, as for the phase guards (the count prerequisite applies to every DREG helper call; the :146 stop is the case with NO transfer object).  CARRIERS OF THE REST: b120 carries the unknown-CDB producer omission and its empty-status consequence; this row's residual is every OTHER empty-buffer path and every nonempty-buffer case.  FIX SHAPE: keep the bounds protection and refuse the access or handle phase completion -- removing the guard exposes the indexed accesses at :180 / :246 -- a CONTROLLER fix; b120 remains the PRODUCER fix.

**What else changes: nothing in the queue text or the other ledger rows.**  The brief generator's defect -- a passage
with both a pointer and a new row listed with the pointer alone -- is recorded and not re-run: agy is walled until
2026-10-07 by its own message and the fix is one column.  `icite2_2`'s twenty rows (the ones the first agy set had not
reached) are unaudited by agy; Astra's own passes read the whole table before `#555` shipped (`ifile_04`: 128/128
rows), so the gap is a missing second reader.

**Also in this commit:** the committed ledger's `boilerplateprefix` commits field, left for "the next commit" by
`#557`'s post step, is filled with `e1871fa5`, and -- the row being closed WITH commits from then on -- it gets the
regress `[HELD AWAITING SEAT: fable5]` entry and `hold_question` that section I's rule 3 asks for (found by `#557`'s
post-commit check of the working ledger).

**Seats, by name.**  agy (gemini-3.8-flash-high): five of six briefs, one WALLED.  GPT-6 Astra (codex, `ultra`): the
check of the disposition, the confirmation of grok's ruling.  grok (grok-4.7 xhigh): the ruling on Astra's finding.
The Fable and Opus agent seats were deliberately not fired (owner instruction, 2026-10-02); kimi down; Ollama not fired.
