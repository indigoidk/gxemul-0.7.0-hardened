# #529's records drafts, RENDERED VERBATIM from the scratchpad drafts at 2026-10-02 10:41:28 (render_drafts.py)
#
# Earlier versions of this file were assembled by hand and went stale against the drafts (the flagship's final
# ruling, item D.2, and the grok seat's reading, item D, both found that); this one is a byte copy of each draft
# file, re-run after every edit.  Placeholders <OWED-...> are filled at assembly and are owed, not claims.
# History of the drafts: GPT-6 Astra's first audit (09-26, eleven sentences) and second audit (09-28, eight
# sentences) applied; crimectllane HIGH (09-28); r19 (09-30 a.m.) and r20 (the flagship's final ruling, 09-30)
# retargeting; the known-wrong-records note from the grok seat's reading (09-30).

================ CHANGELOG #529 block (changelog529.md) ================
# `#529` (crimewidthkill): a guest byte or halfword access to the SGI IP32's CRIME ended the emulator -- declined now and announced once, defended by a 226-row detector whose review chain ran sixteen repairs and closed on repair 16's F2 pass

**The defect, witnessed at rung 3.**  `DEVICE_ACCESS(crime)` in `src/devices/dev_sgi_ip32.c` served lengths 4 and 8 and
called `fatal(); exit(1);` on any other, so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000) ended
the emulator process.  `regress/artifacts/crimewidthkill/crime_width_witness_20260913.py` on the unmodified `-E sgi -e
ip32`: the committed build 3/15 -- every refusal row red, the three controls green (`witness_committed.out`) -- and the
fix 15/15 (`witness_fix.out`).

**What ships.**
* `src/devices/dev_sgi_ip32.c` -- unchanged since 2026-09-13 (md5 8c1d1545; `est/` byte-identical; the build trees
  cleared -- run 2026-10-02 09:44, not asserted: `cmp` clean against SEC in `build/`, `build-asan/`, `est/` and WSL
  `/tmp/gxsec-build`, and the binary newer than the source in all three build trees (`build/` 09-27 18:02:51 over
  18:01:54; `build-asan/` 09-25 13:53:09 over 09-13 03:58:19; `/tmp/gxsec-build` 09-27 18:03:34 over 18:02:52);
  `est/` is a source tree, part 2 N/A; no `.MUTANT` sentinel anywhere).  The width arm DECLINES: one latched announce, `[ crime: unimplemented len=%i at 0x%x --
  declined.  (once) ]`, through a new per-instance `warned` field, then `goto crime_declined` -- the function's common
  tail (the HARDINT restore, the INTSTAT recompute, the read-back, `return 1`) -- past the register switch.  Option-set
  member 3, the `#498` sgi_de shape.
* `regress/crime_width_probe.py` (NEW, 226 rows) -- real guest loads and stores through real address decode and
  `memory_rw` on the unmodified machine, in stepped and free-running sessions (the `<RUN>' sessions `continue`, and the
  `free ... said' rows need that difference); LIVENESS and DEVICE-SIGNATURE controls.  Its module docstring is the
  CONTRACT (clause (e)): every edit it is designed to catch, each measured in a named table, and what it discloses.
* `regress/gate_arm.sh` -- gate 14 runs it: parse before score, controls OK, exit 0, rows run / correct / emitted
  pinned at 226, none failed.
* `tools/pipeline/check_probe_wiring.py` -- the probe as a gated DETECTOR (its description said 141 rows and pin 141),
  and 93 MANIFEST lines -- derived by `manifest529.py` from the `.py` files under `regress/artifacts/crimewidthkill/` at
  staging time, one per file no line named yet (`stage529/MANIFEST.txt` carries the count; it was 92 when staged for r21,
  and r22's archived probe adds one) -- for the round's preserved
  instruments and scripts (RESEARCH or TOOL, using extracted docstring text where available and `(no docstring)`
  otherwise); `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 31 -> 32; `tools/pipeline/
  check_score_claims.py` -- the hyphen fix (`scorehyphenfp`, whose ledger row said closed with no commit): HEAD's checker
  read the probe's ordinal `entries-4/8` as a stale score claim.
* `regress/artifacts/crimewidthkill/table16_20260926/POSTTABLE16.out` -- the F2 ruling's Q3 item 13, the records outside
  the probe, appended as a dated CORRECTIONS section (the table's own text is kept): the `ctlrst sw halt' kill it did not
  list (the Opus seat's `S_rst4clr`, 224/226 with exactly `sw08 halts` and `ctlrst sw halt` red and CONTROL=FAIL because
  `sw08 halts` is a CONTROL row), the PRETABLE's `+0x06 -> +0x07` slip, and the packet's stale E7/E10 labels (the frozen
  probe is 5f770991, 226 rows); F14's "single-axis" is "label-only" and F24's six TIME sessions are repair 15's (two
  before it).  PRETABLE16 is not edited.
* `regress/artifacts/crimewidthkill/flagship_20260918/` -- the flagship's 2026-09-18 answer, which lived only in its
  transcript (87 claude-fable-5-1 turns, 0 refusals), preserved with its brief; ledger entry [154]'s evidence pointed at
  the brief in `_scratchpad/` and now points here (the 09-25 re-ruling's confirmation asked for both).
* The carrier (the project-root `CLAUDE.md`; its tracked copy stays uncommitted by standing constraint): the Q3
  disjunct in JOINT CELLS -- replaced in place by the codex seat's 2026-09-26 rewrite
  (`codexfarm_20260926/codex_carrierq3.txt`), adopted with the flagship's three corrections of 2026-09-30
  (`fable5_final.md` item E: M7/M8 recorded as measured DETECTED, M3/M5 as holes CLOSED by repair 15, and the sentence
  that an OFFSET within one label is not an axis unless the body distinguishes it), graded RIGHT by GPT-6 Astra's
  confirmation; the clause opens `AND A GUARD THAT SUPPRESSES A DISPATCH ADDS A THIRD DISJUNCT TO THE 2026-09-09 LABEL
  CLAUSE`, and the tracked copy carries the identical bytes (`cmp` clean 2026-10-02).

**THE CHAIN.**  2026-09-13 to 2026-09-26 (the review of its text and records ran to 2026-10-02).  Pass 1 on the design (`panel_20260913_000135`), then review panels through
closing pass 8 (`panel_20260913_022247` .. `panel_20260916_194735`), repair 14's pass 1 (`_scratchpad/
panel_20260916_234606`) and its adjudication (`panel_20260917_004011`) -- each finding escapes that the next repair
closed in-round.  The detector grew 40 -> 71 -> 85 -> 111 -> 121 -> 131 -> 141 -> 157 -> 188 -> 204 rows across
eleven kill tables (`killtable_20260913/` .. `killtable11_20260916/`) and table 12 (`repair14_20260916/`); the ctl0c
pair was discharged by a measured kill (`ctl0c_discharge_20260917/`: `M_ctl0c_decline` reds exactly `acc ctl0c` and
`p acc ctl0c`, as predicted -- an earlier CHANGELOG block still listed it OWED).  **Two roster gaps are part of that
history and are named here:** repair 14's only pass 2 was grok alone (`grok_pass2_20260917.txt`, ledger [151]) -- the
09-25 re-ruling made roster validity an explicit part of the stop condition because of it; and minimax stayed DOWN on
closing pass 3 (a timeout, then HTTP 500), while closing passes 4 and 5 timed out first and answered on retry (their
first `SEATS.txt` files are stale, not final status).  **Three rulings credited to the flagship seat were written by
claude-opus-4-8 after refusals** (the C3 and C5 adjudications and repair 14's ruling -- `agent_models.py`); the ledger
now tags them `[NOT A SEAT ANSWER]` and each file carries a dated provenance note.  **The flagship re-ruled first-hand
on 2026-09-25** (`rerule_20260925/fable5_rerule_529_20260925.md`): C3 STANDS, D7 FLOOR (the latch is a floor axis), Q3
ADOPT (into the carrier), STOP RATIFY with roster validity as a fourth part; GPT-6 Astra confirmed it with changes
(`codex_astra529rerule.txt`).  Then: **table 13a** measured the INTMASK and CONTROL-write label swaps (CHECK13A_PASS:
base 204/204, both 201/204 -- no carrier owed); **repair 15** rowed the TIME and REV decline carriers and the entries
13-and-17 DOG pair (table 14, CHECK14_PASS, 18 legs exact: base 218/218, `M3_timelatch` and `M5_revlatch` 214/218 -- the
two escapes the whole chain had carried); its **full-roster pass 2** (`panel_20260926_021621`) found the HARD_RESET
clear's residue unrowed -- the dedicated grok job's BREAK, measured an escape in table 15a (218/218), graded L2 by the
flagship; **repair 16** pinned the CONTROL arm's residue-text count for each of its three clears in both latch states
(table 16, CHECK16_PASS, 25/25 legs exact on 226 rows); and its **F2 pass** (`panel_20260926_053828`, every seat's
findings consolidated with dispositions) closed the enumeration: the flagship (`repair16_f2_20260926/
fable5_f2_adjudication.md`), **"THE CHAIN CLOSES ON THIS PASS -- zero floor breaches survive adjudication on a valid,
full-roster pass; ... NO row is owed"**, CONDITIONAL on its Q3 text corrections, a base leg on the final bytes, the
`S_rst4clr` attribution kept durable, GPT-6 Astra's confirmation and `#549`-first ordering; X1 and X3 graded clause (e).

**The final text.**  **r17** (`final529r17_20260926/`) applies the F2 ruling's Q3 items 1-12, four corrections the
resumption dossier listed (the table range, the HARD_RESET rows missing from NOW ROWED, the ctl0c discharge, a heading
that still called the decline-suppression face open), the separate `13/17` wording correction (section U would have read
it as a stale score), and Astra's two qualifications (the split widths unreachable only CONDITIONALLY on
`DEV_CRIME_LENGTH == 0x280`; decode translations disclosed, none measured).  **r18** (`final529r18_20260926/`) adds GPT-6 Astra's audit of r17 (`final529r17_20260926/codex_jobs/codex_r17audit.txt`: eight false or
unsupported docstring sentences -- "one `step' at a time" of every access; TIME "66-990" twice, where TIME is a small
multiple of 66 and zero in 42 of 800 logged cells; TIME's upper word equivalent only while it is zero; "any selection
shows" only for selections that reach the returned bytes; CONTROL bit 0 IS written by accepted rows; the host bucket's
"missing two" and repair 13's three-write count, both inside the ACCEPTS block) and **the ACCEPTS-46 enumeration**: the
Opus seat MEASURED every one of the 92 entry x latch-state cells with a silent-decline mutant against predictions
written before any run, 92 of 92 exact (`final529r17_20260926/opus_accepts46.md`, logs in `opus_acc46/`), and an
independent codex reading reached the same partition (`codex_jobs/codex_accepts46twin.txt`).  It names every member of
repair 13's buckets (the two unnamed host-diagnostic members are entries 11 and 15, the six unnamed equivalent members
12, 13, 16, 17, 43 and 44), retires repair 13's counts -- 31 guest-visible, 4 rowed on the CONTROL text in both latch
states, 1 host-diagnostic only (entry 40), 10 equivalent -- and finds **entry 34 (`sd +0x40`) unrowed with the latch
CLEAR** (both of its latch-CLEAR drivers store 0 into a slot that holds 0): clause (e), not floor, by the flagship's final
ruling (item C: the {default label, 8-byte store, latch CLEAR} cell is HELD at +0x278; the unobserved +0x40 slot is
disclosed coverage debt), GPT-6 Astra confirming -- the k34C decline escapes 226/226 on S55 as a measured
non-observation, so the cheap row (seed a nonzero `sd +0x40` in the two value sessions, re-want `acc 40 sw` /
`p acc 40 sw`) is FILED as `crimecontroldebt` item 8 with its replay cost, not owed.  **CODE-IDENTICAL to repair
16** but for three row notes: the r16-to-r17 diff changes three row-note strings, comments and the module docstring
(`mk_r17.py` compares the ASTs after normalising every eligible row-note argument, not only the three edited ones --
GPT-6 Astra's second records audit), and `mk_r18.py` refuses unless r18's AST less the module docstring equals
r17's.  **r19** (`final529r19_20260930/`) is r18 with ONE docstring sentence corrected -- "NetBSD's +0x0c write does nothing", where the write stores the low word and reaches the default arm's diagnostic (GPT-6 Astra's second records audit, `codexpack_20260928/rec529audit2/`); `mk_r19.py` refuses unless r19's AST less the docstring equals r18's.  **r20** (`final529r20_20260930/`) is r19 plus the flagship's final
ruling (`final529r18_20260926/fable5_final.md`, SHIP WITH CHANGES, 2026-09-30): the comment at ACCEPTS entry 21 said
the cell was "BLIND IN BOTH LATCH STATES ... all three [sessions] oracle-less" -- a wrong record, since session 19's
accepted `lw +0x10` reasserts and `istat ctl` reads IP2 (k21S 224/226 in `opus_acc46/SUM46.out`; the probe's own
ACCEPTS block listed entry 21 as pinned post-latch); only the 4-byte VALUE was unobserved.  Corrected and dated in
place, and the ACCEPTS block's "every one of the 92 cells MEASURED" now says which two sessions (`rearm *`, `latch *`)
were served by derivation from the inertness capture -- for the 31 guest-visible entries; they were rerun for the
other 15 (`opus_accepts46.md`, RAN 4).  `mk_r20.py` refuses unless r20's AST less the docstring equals
r19's.  The ruling named r20 the CLOSING text revision; **GPT-6 Astra's confirmation OVERTURNED that exemption** under the
late-dissent rule ("WRONG RECORD -> L4, correct in place") and found item 6's "no row seeds TIME's upper word" FALSE --
the grok seat's reading of the packet: the gapped sessions plant an `sw` of `t0=0x0a0b0c0d` at TIME, which the 4-byte
arm stores in the UPPER word -- so **r21** (`final529r21_20260930/`; `mk_r21.py`, AST-checked
against r20) corrects that clause, item 8's wording ("bits the CONTROL arm does not individually test or clear"; its
clause-(e) classification stands), the "66-990" comment at r20:955 and the derivation qualifier's scope.  **r22** (`final529r22_20261002/`, the committed
bytes) -- r22 is r21 plus ONE docstring qualifier: this commit's first precheck (2026-10-01) was refused by the hook's score-claim check -- the ACCEPTS note for entry 40 quoted closing pass 7's 157/157 without the `157-row` marker it requires of a historical score (mk_r22.py, AST-identical to r21) -- and by its NUL check (eight NUL bytes in a 2026-09-13 seat answer, replaced by `<NUL>` with a note beside it).  Base leg on r22 against table 16's base binary (2026-10-02, WALL 1235 s): 226/226, CONTROL OK; 21 differing row pairs against table 16's base log -- 15 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r22_20261002/probe_base_r22.raw`).  The r20-to-r22 text delta was put to GPT-6 Astra
(`final529r22_20261002/codex_astra_r22.txt`): "CONFIRM WITH CHANGES (8) -- the five probe edits stand, but eight records claims need correction."  All eight are applied with its replacement texts -- item 8's
filing provenance and its unrowed-slot classification, the ledger's slot/cell wording, a stale mode line, "timing-dependent"
for "free-running" TIME values in eleven places, the MANIFEST count for r22, and the `(no docstring)` entries -- and no
probe text changed, so r22 stands (`fix529_astra_r22.py`).
Base leg on r21 against table 16's base binary (2026-10-01, WALL 1233 s): 226/226, CONTROL OK; 23 differing row pairs against table 16's base log -- 17 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r21_20260930/probe_base_r21.raw`).
Base leg on r20 against table 16's base binary (2026-09-30, WALL 1229 s): 226/226, CONTROL OK; 27 differing row pairs against table 16's base log -- 21 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 4 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r20_20260930/probe_base_r20.raw`).  **Provenance of r21's corrections:** the grok seat's reading of the final packet (`final529r18_20260926/seats_20260930/grok_529final.txt`) found item 6's closing clause false and the residual "66-990" comment; the flagship's ruling had filed both as known wrong records under a closing-revision exemption, which the confirmation rejected, so they are corrected in r21 rather than recorded as known.  The generator note `final529r20_20260930/mk_r20.py.txt:5` says the cached rearm/latch sessions do not hold the accesses -- false (they do; the derivation rests on their unchanged scored outputs), recorded beside it in `mk_r20.py.CORRECTION.txt`.  Base leg on r19 against table 16's base binary (2026-09-30): 226/226, CONTROL OK, 24 differing row pairs against table 16's base log -- 18 timing-dependent TIME values and the six rows of the three rewritten notes -- and no want, got or verdict column differs (`final529r19_20260930/probe_base_r19.raw`, WALL 1235 s; r18's leg, `final529r18_20260926/`, gave the same 226/226).

**The panel.**  Every stage full-roster from the 09-25 re-ruling on: pass 2 and its F2 each fired all eight scriptable
transports, a dedicated grok job, the Opus measuring seat (claude-opus-5-5 by its transcript) and the flagship LAST
(claude-fable-5-1; its first pass-2 answer was an opus-4-8 fallback, relabelled, and the resumed agent answered
first-hand).  **Two further failures in the review chain, named so "full-roster" reads as it was:** the
09-25 re-ruling's first answer fell back to opus-4-8 after two refusals before the resumed agent answered first-hand
(`rerule_20260925/fable5_rerule_529_20260925.md`), and the final packet's first firing on 2026-09-26 hit the seat's
session limit before answering; the ruling that stands is the fresh agent's of 2026-09-30 (claude-fable-5-1 by its
transcript).  **Codex was walled on both panels** (usage limit to 07:01) -- a seat failure -- and answered the F2 pass
after the reset (`codex_f2.txt`, plus a dedicated job, `codex_f2ded.txt`).  **The kimi CLI returned "403 ... subscription
does not have access to Kimi Code"** on both; the seat was COVERED by `kimi-k3:cloud`.  **Dissents recorded, not
absorbed:** deepseek's REJECT on pass 2 (Q1(b)'s timing); on the F2 pass deepseek's and minimax's OVERTURN of F2 (the
ENDIANESS rows as unlicensed scope growth -- minimax would overturn it FIRST), ruled a licensed strengthening by the
flagship; glm's and kimi-k3's F20 overturn (take the value anchor) -- ruled clause (e), the value anchor FILED.  After
the F2 pass, GPT-6 Astra (codex at `ultra`) audited r17 (above), the records drafts (`codex_rec529audit.txt`: eleven
false or unsupported sentences; their substantive corrections are incorporated in this block and the ledger, and a
second audit on 2026-09-28, `codexpack_20260928/rec529audit2/`, found eight more, corrected the same day) and the commit tooling
(`codexfarm_20260926/codex_scripts529.txt`: seventeen defects; the commit ran through a rewritten, controlled tool).
**Astra (GPT-6 Astra, pointer form) on the ruling and the final text: GPT-6 Astra's confirmation of the final ruling (2026-09-30, `final529r18_20260926/codex_astraconfirm_final.txt`): 2 of its dispositions overturned -- item 6's "no row seeds TIME's upper word" is FALSE (the gapped sessions' `sw` of `t0=0x0a0b0c0d` at TIME lands in the upper word; grok was right) and the closing-revision exemption for later wrong records contradicts the late-dissent rule ("WRONG RECORD -> L4, correct in place"), so an r21, comment/docstring-only with its own base leg, is required and r20 stays as history; 4 wording changes (TIME "after any update is a multiple of 66" does not survive an arbitrary stored value; item 8 says "bits not individually tested or cleared", its clause-(e) classification standing; the codex twin's reading was also measured independently; "all four drafts" -> the revision-bearing records); HIGH for `crimectllane` and the carrier's Q3 clause RIGHT; C's clause (e), F's diff and the r20 receipt (27 pairs: 21 TIME, 6 notes) verified independently..**

**FILED** (OUTSTANDING_BUGS 2026-10-02): `crimectllane` (HIGH -- the CONTROL lane: a 32-bit store to the high word stops
every CPU; graded HIGH by GPT-6 Astra over the Fable seat's MED; one probe comment and `gate_arm.sh` had called it
filed since 09-13 and it was filed nowhere), `crimebankorder` (LOW -- a second probe comment called IT filed; the
resumption dossier found neither filing), `crimecontroldebt` (LOW -- the eight strengthenings filed rather than owed: seven by the F2 adjudication and entry 34's row by the final ruling, each with its kill and re-run cost).  Existing and still open:
`crimesplitwidth`, `crimeramexit`, `crimectlflood`.  The next commit owes `#529`'s pass-2 receipt (`dev_sgi_ip32.c` is
`src/`).

================ OUTSTANDING_BUGS section (bugs529.md) ================

## 2026-10-02 — GXEMUL [087a90]: `#529` crimewidthkill CLOSES (its chain closed 2026-09-26; the review of its text and records ran to 2026-10-02); what that review files

Evidence: `regress/artifacts/crimewidthkill/` -- the panels (durable copies beside each pass), the Opus records, the
dedicated jobs, the flagship rulings (the first-hand 09-25 re-ruling in `rerule_20260925/`; repair 15's pass 2 and
repair 16's F2 adjudication), GPT-6 Astra's confirmations, and every kill table with its PRETABLE.

### `crimectllane` (HIGH, device) — CRIME_CONTROL acts on the raw value of whatever width reaches the exact label 0x08

`dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)`, `case CRIME_CONTROL:` (0x008) matches the EXACT label and acts on the RAW
`idata` of the access that reached it.  So a 32-bit `sw 0x800` to `+0x08` -- the HIGH half of the 64-bit register on this
big-endian machine -- carries bit 11 into `CRIME_CONTROL_HARD_RESET` and stops every CPU, while a 32-bit write to
`+0x0c`, the lane that holds bit 11 and the offset NetBSD 1.6.2 writes (the arm's own TODO says so), performs the
register store and reaches the default arm's log, bypassing CONTROL's reset and watchdog handling.  MEASURED by `#529`'s
pass-1 Opus seat (`crimewidthkill/opus_pass1_20260913/out/rows_base.out`: `sw CTL+08 0x800` halted; `sw CTL+0c 0x800`
did not halt, `dflt=1`).  (A draft of this entry said the `+0x0c` write "does nothing" -- GPT-6 Astra's records audit.)  `#529`'s detector USES this defect as a channel
(`sw08 halts`, `sw08 msg ctl`, the `sh08` rows) and says so; a round that fixes the lane owes those rows' re-derivation.
Needs a guest witness of what a real driver writes (the PROM's reboot path; NetBSD's watchdog) before choosing a lane
model.  **A probe comment and `gate_arm.sh` have called this row "filed" since 2026-09-13 (a second probe comment called
`crimebankorder` filed); the resumption dossier found neither filing, and the flagship's 09-25 re-ruling listed both.**  **Graded HIGH, not MED:** stopping
every CPU ends the emulation in ordinary single-machine execution without `debugger_enter_at_end_of_run` (`emul.c`
enters the debugger instead when it is set) and the process returns, so a guest store that on the header's
model reaches only reserved high-word bits ends the emulator -- the severity rule's HIGH.  GPT-6 Astra's confirmation of
the codex farm's adjudication (`codexfarm_20260926/adjudication/codex_astraconfirm_farm_f1c.txt`) overturned the Fable
seat's MED; that seat's argument -- the guest gains no capability it lacks through the legitimate 64-bit HARD_RESET --
bears on reachability ranking, not on severity.

### `crimebankorder` (LOW, device) — the CRIME prelude writes the bank-control registers contiguously; the header interleaves them

The prelude's bank loop writes `d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + bank]` -- CONTIGUOUS offsets
0x208..0x240 -- while `src/include/thirdparty/crimereg.h:141-148` defines the bank control registers INTERLEAVED (CTRL0
0x208, CTRL1 0x218, CTRL2 0x210, CTRL3 0x228, CTRL4 0x220, CTRL5 0x238, CTRL6 0x230, CTRL7 0x248; raised by the codex
pass-1 seat on 2026-09-13, re-read 2026-09-26).  If the header is right, banks 1..7 are reported at the wrong offsets
and a guest sizing memory from them reads the wrong layout.  **But the header is itself suspect:** CTRL7 (0x248) is the
same offset as `CRIME_MEM_REFRESH_CNTR` (`:149`), and no bank register sits at 0x240.  Needs a boot witness (the IP32
PROM's memory report, or NetBSD's or OpenBSD's own sizing) before any edit -- the header, not the code, could be wrong.
`#529`'s `top8 anchor` row pins the model's CURRENT layout and says a round re-ordering the banks owes its
re-derivation.  **Called "filed" in the probe since 2026-09-13; filed nowhere until now.**

### `crimecontroldebt` (LOW, detector) — the eight strengthenings `#529`'s review filed rather than owed

The flagship's F2 ruling (`crimewidthkill/repair16_f2_20260926/fable5_f2_adjudication.md`, Q4) closed the chain with NO
row owed and FILED items 1-7; its final ruling (`crimewidthkill/final529r18_20260926/fable5_final.md`, C) added item 8.
Each is filed with its measured or derived kill and its re-run cost:
1. a value anchor BESIDE the prefix count in `ctldog`/`ctlrst` -- kills `D_dogbit0` (226/226 today); re-runs
   `D_nodogclear`'s red set.  (An anchor IN PLACE of the count loses `H_noresetclear`: `opus_f2/replay_ctl.out`.)
2. a latch-SET `sh 0x0201` in `sh08b` -- kills `P_ctl2wrc_set`; re-runs M8 and M1.
3. one free-running accepted `sw 0x0001` session -- kills `M_ctldebug` (the arm's `fatal()` demoted to `debug()`, which
   every stepped session prints either way: `opus_f2/disc_f2.out`).
4. an `lb` appended after the first refusal in the `istat`/`imask` sessions -- kills `W_istlb`/`W_imklb` (226/226,
   table 16, as predicted); re-runs M6 and M7.
5. six latch-CLEAR first-refusal sessions at INTSTAT/INTMASK -- kill the `C_` variants.
6. a refused `lb +0x10` while the interrupt line is asserted -- kills `P_istprev_set`.
7. an `sw 0x0801` last-store session -- the HARD_RESET x bit-0 member of the bit-conditioned family, only if (1) is taken.
8. entry 34 of the ACCEPTS-46 enumeration (`sd +0x40`, latch CLEAR): both of its latch-CLEAR drivers store 0 into a
   slot that holds 0, so a silent decline of that one access moves no row (k34C 226/226) -- clause (e), the
   unrowed-slot class, by the flagship's final ruling (2026-09-30), GPT-6 Astra confirming.  The cheap row: seed a
   nonzero value in the two value sessions' `sd +0x40` and re-want `acc 40 sw` / `p acc 40 sw`; its cost: S55 and S58
   carry entries 8-11, 14, 15, 19, 21, 23, 24, 30, 31 and 34-37, so every recorded kill touching them re-runs.
All are above-floor strengthenings: items 1, 2 and 4-7 cover state/value joints (the CONTROL arm reads no latch and
does not individually test or clear bit 0; the remaining joints are not distinguished by the decline); item 8 belongs
to the unrowed-slot class, with the {default label, 8-byte store, latch CLEAR} cell held at +0x278; item 3,
`M_ctldebug`, is separately a DIAGNOSTIC-TRANSPORT change in upstream code the fix does not touch (the ruling's X8).  (A draft called all
seven of the F2 items "joints" -- GPT-6 Astra's records audit; item 8 was ordered by the final ruling.)  Rank below any live defect in `dev_sgi_ip32.c`.

================ commit message (msg529.txt) ================
#529 crimewidthkill: a guest byte or halfword access to the SGI IP32's CRIME ended the emulator -- declined now and announced once, with a 226-row rung-3 detector whose review chain closed on repair 16's F2 pass, gated

DEVICE_ACCESS(crime) served lengths 4 and 8 and called fatal() then exit(1) on any other, so one guest
lb/lbu/lh/lhu/sb/sh anywhere in CRIME ended the emulator.  Witnessed at rung 3 on the unmodified -E sgi -e ip32
(regress/artifacts/crimewidthkill/crime_width_witness_20260913.py: committed build 3/15, every refusal row red and
the controls green; the fix 15/15).

- src/devices/dev_sgi_ip32.c (unchanged since 2026-09-13): the width arm DECLINES -- one latched announce through a
  new per-instance warned field, marked (once), then a goto to the common tail past the register switch (option
  member 3, the #498 sgi_de shape).  est/ byte-identical.
- regress/crime_width_probe.py (new, r22): 226 rows of real guest loads and stores on the unmodified machine, in
  stepped and free-running sessions, controls, and a contract header (clause (e)) naming every edit it catches and
  what it discloses.
- regress/gate_arm.sh: gate 14 runs it -- parse before score, controls, exit 0, 226 rows pinned (run, correct,
  emitted), none failed.
- tools/pipeline/check_probe_wiring.py: the probe as a gated DETECTOR and the round's preserved scripts
  (RESEARCH/TOOL); tools/precommit_check.sh: SCORE_CLAIMS_MANIFEST 31 -> 32; tools/pipeline/check_score_claims.py:
  the hyphen fix the probe's docstring needs (scorehyphenfp).
- regress/artifacts/crimewidthkill/: every table, panel and ruling of the chain; table16's POSTTABLE16.out gains the
  F2 ruling's item-13 corrections (appended, dated); flagship_20260918/ preserves the flagship's 2026-09-18 answer,
  which lived only in its transcript.
- regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md, FABLE_C5_RULING_20260915.md: dated provenance notes --
  both were written by claude-opus-4-8 after refusals, not by the flagship seat whose identity line they carry.

The chain: pass 1, then review panels through closing pass 8 and repair 14 (the detector 40 -> 204 rows over eleven
kill tables and table 12; repair 14's only pass 2 was grok alone); the flagship's first-hand re-ruling of 2026-09-25
(three earlier "fable5" rulings were opus-4-8 fallbacks), confirmed by GPT-6 Astra; table 13a; repair 15 (the TIME
and REV decline carriers; table 14); its full-roster pass 2 (the HARD_RESET residue, table 15a); repair 16 (the
CONTROL arm's residue-text count; table 16, 25/25 legs exact); and repair 16's F2 pass, which closed the enumeration
with no row owed, on conditions.  The committed text is r22: repair 16's code (identical by AST but for three row
notes) with the ruling's corrections, GPT-6 Astra's r17 audit (eight false sentences), the ACCEPTS-46
enumeration the Opus seat measured cell by cell (92 of 92 predictions exact; a codex reading agreed), one
docstring sentence corrected after Astra's second records audit (2026-09-28), and the flagship's final ruling
(2026-09-30): one comment at ACCEPTS entry 21 corrected (the SET-state decline was observable all along) and the
ACCEPTS block's MEASURED claim qualified (two sessions served by derivation); and GPT-6 Astra's confirmation of that
ruling (two text dispositions overturned: a row DOES seed TIME's upper word, and no closing-revision exemption), applied
as r21 -- that clause, item 8's wording, the "66-990" comment and the qualifier's scope.  r22 is r21 plus ONE docstring qualifier: this commit's first precheck (2026-10-01) was refused by the hook's score-claim check -- the ACCEPTS note for entry 40 quoted closing pass 7's 157/157 without the `157-row` marker it requires of a historical score (mk_r22.py, AST-identical to r21) -- and by its NUL check (eight NUL bytes in a 2026-09-13 seat answer, replaced by `<NUL>` with a note beside it).  Base leg on r22 against table 16's base binary (2026-10-02, WALL 1235 s): 226/226, CONTROL OK; 21 differing row pairs against table 16's base log -- 15 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r22_20261002/probe_base_r22.raw`).  r21's leg:
Base leg on r21 against table 16's base binary (2026-10-01, WALL 1233 s): 226/226, CONTROL OK; 23 differing row pairs against table 16's base log -- 17 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r21_20260930/probe_base_r21.raw`).  r20's leg:
Base leg on r20 against table 16's base binary (2026-09-30, WALL 1229 s): 226/226, CONTROL OK; 27 differing row pairs against table 16's base log -- 21 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 4 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r20_20260930/probe_base_r20.raw`).  Base leg on r19 against table 16's base binary (2026-09-30): 226/226, CONTROL OK, 24 differing row pairs against table 16's base log -- 18 timing-dependent TIME values and the six rows of the three rewritten notes -- and no want, got or verdict column differs (`final529r19_20260930/probe_base_r19.raw`, WALL 1235 s; r18's leg, `final529r18_20260926/`, gave the same 226/226).

Records: CHANGELOG #529; OUTSTANDING_BUGS (crimewidthkill and scorehyphenfp closed in place; filed crimectllane,
crimebankorder, crimecontroldebt); ledger -- crimewidthkill CLOSED (four fallback entries tagged NOT A SEAT ANSWER;
entry [154]'s evidence repaired); matrix.html regenerated.  The carrier (not tracked here) gained the Q3 clause.
The next commit owes #529's pass-2 receipt.

Review: pass 2 and the F2 pass each full-roster -- eight scriptable transports, a dedicated grok job, the Opus
measuring seat, the flagship last; codex walled on both panels and answered the F2 pass after the reset; the kimi CLI
refused (subscription), covered by kimi-k3:cloud.  After the F2 pass GPT-6 Astra (codex, ultra) audited the final
text, the records drafts and the commit tooling.  GPT-6 Astra's confirmation of the final ruling (2026-09-30, `final529r18_20260926/codex_astraconfirm_final.txt`): 2 of its dispositions overturned -- item 6's "no row seeds TIME's upper word" is FALSE (the gapped sessions' `sw` of `t0=0x0a0b0c0d` at TIME lands in the upper word; grok was right) and the closing-revision exemption for later wrong records contradicts the late-dissent rule ("WRONG RECORD -> L4, correct in place"), so an r21, comment/docstring-only with its own base leg, is required and r20 stays as history -- r21 was built after
this confirmation (mk_r21.py, AST-identical to r20), as was r22 (the r20-to-r22 text delta was then put to GPT-6 Astra, 2026-10-02:
"CONFIRM WITH CHANGES (8) -- the five probe edits stand, but eight records claims need correction", final529r22_20261002/codex_astra_r22.txt; all eight applied before this commit, no probe text changed); the 2026-09-30 confirmation also made 4 wording changes (TIME "after any update is a multiple of 66" does not survive an arbitrary stored value; item 8 says "bits not individually tested or cleared", its clause-(e) classification standing; the codex twin's reading was also measured independently; "all four drafts" -> the revision-bearing records); HIGH for `crimectllane` and the carrier's Q3 clause RIGHT; C's clause (e), F's diff and the r20 receipt (27 pairs: 21 TIME, 6 notes) verified independently.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>

================ ledger_529.py, complete (the ledger changes as code) ================
#!/usr/bin/env python3
"""Ledger records for #529 (crimewidthkill: the row CLOSES) and its three filings.

Modes (LEDGER_PATH names the file; default the working tree's):
  records               the provenance corrections the flagship's 09-25 re-ruling ordered (entries crediting three
                        opus-4-8 fallback files to fable5 -> [NOT A SEAT ANSWER]); the re-ruling and GPT-6 Astra's
                        confirmation of it; tables 13a/14/15a/16 (main-loop measurement records); every seat entry of
                        repair 15's pass 2 (panel_20260926_021621) and repair 16's F2 pass (panel_20260926_053828),
                        the dedicated jobs, the Opus measuring seat and the flagship; the state_note; the closure;
                        the filed rows.  REFUSES if the row already cites panel_20260926_021621.
  opus <grade> <ev>     the Opus seat's ACCEPTS-46 enumeration (after it lands).
  astra <verdict> <ev>  GPT-6 Astra's 2026-09-30 confirmation of the final ruling and r20 text, with r21 required.
  sha <sha>             crimewidthkill.commits (and scorehyphenfp's, whose fix ships in the same commit).
  setcommits <row> <sha>  another row's commits (the previous round's pending record).
CRLF on disk, json.dumps(indent=1, ensure_ascii=False), no trailing newline -- round-trip verified before any write.
"""
import io
import json
import os
import re
import subprocess
import sys

P = os.environ.get("LEDGER_PATH", r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\tools\pipeline\ledger.json")
SEC = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC"
A = "regress/artifacts/crimewidthkill/"
R15 = A + "repair15_pass2_20260926/"
R16 = A + "repair16_f2_20260926/"
P15 = R15 + "panels/panel_20260926_021621/"
P16 = R16 + "panels/panel_20260926_053828/"
RR = A + "rerule_20260925/"
DISP = "CHANGELOG #529 and regress/artifacts/crimewidthkill/repair16_f2_20260926/ (the F2 packet and the flagship ruling)"


def load():
    raw = open(P, "rb").read()
    L = json.loads(raw.decode("utf-8"))
    if dump(L) != raw:
        sys.exit("REFUSED: the ledger does not round-trip byte-identical; its format changed")
    return L


def dump(L):
    return json.dumps(L, indent=1, ensure_ascii=False).replace("\n", "\r\n").encode("utf-8")


def save(L):
    open(P, "wb").write(dump(L))


def row(L, rid):
    r = [x for x in L["rows"] if x["id"] == rid]
    if len(r) != 1:
        sys.exit("REFUSED: row %s found %d times" % (rid, len(r)))
    return r[0]


def ent(phase, seat, date, grade, ev, note):
    return {"phase": phase, "seat": seat, "date": date, "grade": grade, "grader": "", "ev": ev, "note": note}


def size(rel):
    return os.path.getsize(os.path.join(SEC, *rel.split("/")))


#  The three fallback files, read with _scratchpad/agent_models.py (p529/resume_dossier.md section 2e).
FALLBACKS = [
    ("FABLE_C3_RULING_20260914.md", "ae169fa9758283eaf", "2026-09-14T16:22:26Z", "16:29:48Z", "OPUS-4-8 READING"),
    ("FABLE_C5_RULING_20260915.md", "a06935485cd6d5125", "2026-09-16T19:35:00Z", "19:50:12Z", "OPUS-4-8 READING"),
    ("repair14_20260916/FABLE_RULING_20260917.md", "a2bba4bc2896433b4", "2026-09-17T06:17:21Z", "06:25:19Z", None),
]
REANCHOR = (RR + "fable5_rerule_529_20260925.md (the first-hand fable5 ruling of 2026-09-25, entered below; it "
            "re-anchors C3, D7, Q3 and STOP)")


def tag_fallbacks(r):
    n = 0
    for e in r["entries"]:
        if e.get("seat") != "fable5" or (e.get("note") or "").startswith("[NOT A SEAT ANSWER]"):
            continue
        for fname, agent, refused, wrote, grade in FALLBACKS:
            if fname in (e.get("ev") or "") or ("FABLE_RULING_20260917.md" in fname and
                                                 "FABLE_RULING_20260917.md" in (e.get("ev") or "")):
                verif = "SEAT VERIFIED AS FABLE" in (e.get("note") or "")
                if verif:
                    pre = ("[NOT A SEAT ANSWER] *** WRONG RECORD, corrected 2026-09-26: this verification rested on the "
                           "answer's own `MODEL: claude-fable-5-1' line -- a SELF-REPORT, a check that cannot fail.  The "
                           "subagent transcript (per-message `model' and `stop_reason'; _scratchpad/agent_models.py) shows "
                           "the file was WRITTEN BY claude-opus-4-8 at %s (agent %s), after claude-fable-5-1 ended a turn "
                           "with stop_reason \"refusal\" at %s.  The first-hand ruling is %s. ***  "
                           % (wrote, agent, refused, REANCHOR))
                    e["grade"] = "WRONG RECORD"
                else:
                    pre = ("[NOT A SEAT ANSWER] *** WRONG RECORD, corrected 2026-09-26: MEASURED from the subagent "
                           "transcript (per-message `model' and `stop_reason'; _scratchpad/agent_models.py), the answer "
                           "this entry credits to fable5 was WRITTEN BY claude-opus-4-8 at %s (agent %s) -- "
                           "claude-fable-5-1 ended a turn with stop_reason \"refusal\" at %s and the Agent tool re-ran the "
                           "rest on opus-4-8, keeping the seat's identity line.  Kept as an opus-4-8 READING, not a fable5 "
                           "answer; the file carries a dated provenance note since 2026-09-26; the first-hand ruling is "
                           "%s. ***  " % (wrote, agent, refused, REANCHOR))
                    e["grade"] = grade or "OPUS-4-8 READING"
                e["note"] = pre + (e.get("note") or "")
                n += 1
                break
    if n != 4:
        sys.exit("REFUSED: expected 4 fallback-credited entries, tagged %d" % n)


def panel(p, date, label, verdicts, kimi_note):
    """one entry per scriptable transport, from the durable panel copy."""
    E = []
    E.append(ent("review", "codex", date, "WALLED (seat failure)", p + "codex.txt",
                 "%s (%s).  codex (FILE-READING, GPT-6 Astra max, %d bytes): the CLI's usage-limit notice (reset 2026-09-26 "
                 "07:01) -- a SEAT FAILURE, not agreement; %s.  Dispositions: %s."
                 % (label, p.rstrip("/").split("/")[-1], size(p + "codex.txt"), verdicts["codex"], DISP)))
    desc = {"agy": "agy (FILE-READING, gemini-3.8-flash-high)", "grok": "grok (FILE-READING, grok-4.7 xhigh, plan mode)",
            "glm": "glm (PACKET-FED, glm-5.3:cloud)", "deepseek": "deepseek (PACKET-FED, deepseek-v4-pro:cloud)",
            "minimax": "minimax (PACKET-FED, minimax-m3:cloud)"}
    files = {"agy": "agy.txt", "grok": "grok.txt", "glm": "ollama_glm.txt", "deepseek": "ollama_deepseek.txt",
             "minimax": "ollama_minimax.txt"}
    for seat in ("agy", "grok", "glm", "deepseek", "minimax"):
        v = verdicts[seat]
        lab = ("an EXCERPT -- the file is the record; GPT-6 Astra's records audit found earlier 'verbatim' labels here "
               "trimmed or annotated" if v.lstrip().startswith(('"', "VERDICT", "**")) else
               "a SUMMARY in the recorder's words, not the seat's -- the file is the record; the second records audit "
               "found this labelled an excerpt")
        E.append(ent("review", seat, date, v[:60], p + files[seat],
                     "%s.  %s, %d bytes.  Its verdict (%s): %s  Dispositions: %s."
                     % (label, desc[seat], size(p + files[seat]), lab, v, DISP)))
    kv = verdicts["kimi"]
    klab = "an EXCERPT" if kv.lstrip().startswith(('"', "VERDICT", "**")) else "a SUMMARY in the recorder's words, not the seat's"
    E.append(ent("review", "kimi", date, kv[:60], p + "ollama_kimi.txt",
                 "%s.  kimi (PACKET-FED, kimi-k3:cloud, %d bytes) -- %s.  Its verdict (%s): %s  Dispositions: %s."
                 % (label, size(p + "ollama_kimi.txt"), kimi_note, klab, kv, DISP)))
    return E


KIMI_CLI = ("the kimi CLI returned \"403 Your current subscription does not have access to Kimi Code right now\" "
            "(kimi.txt, 284 bytes): its seat is COVERED by this substitute transport, not lost")


def records():
    L = load()
    r = row(L, "crimewidthkill")
    if any("panel_20260926_021621" in (e.get("ev") or "") for e in r["entries"]):
        sys.exit("REFUSED: crimewidthkill already cites panel_20260926_021621 -- records has run")
    tag_fallbacks(r)
    # -- ledger [154]: the flagship's 2026-09-18 answer cited only its brief, in _scratchpad/ (volatile); the answer
    #    lived in the transcript.  Both are now durable (the re-ruling confirmation's request).
    e154 = r["entries"][154]
    if e154.get("date") != "2026-09-18" or e154.get("seat") != "fable5" or "fable_flagship_20260918" not in (e154.get("ev") or ""):
        sys.exit("REFUSED: crimewidthkill entry [154] is not the 2026-09-18 flagship entry: %r" % (e154.get("ev"),))
    e154["ev"] = ("regress/artifacts/crimewidthkill/flagship_20260918/fable5_flagship_20260918_answer.txt (the answer, "
                  "extracted from transcript agent-a2865c082138f4cf6; its brief beside it)")
    e154["note"] = ("[EVIDENCE REPAIRED 2026-09-26 by #529: this entry cited `_scratchpad/fable_flagship_20260918.md (brief)`, "
                    "a volatile brief, while the answer lived only in the transcript -- 87 claude-fable-5-1 turns, 0 "
                    "refusals, a genuine seat answer.]  " + (e154.get("note") or ""))
    E = []
    # -- the re-ruling, 2026-09-25 ------------------------------------------------------------------------------------
    E.append(ent("review", "fable5", "2026-09-25", "C3 STANDS / D7 FLOOR / Q3 ADOPT / STOP RATIFY",
                 RR + "fable5_rerule_529_20260925.md",
                 "#529 THE FLAGSHIP'S FIRST-HAND RE-RULING of the three rulings opus-4-8 fallbacks had written (C3, C5, "
                 "repair 14): claude-fable-5-1 by agent_models.py, after an opus-4-8 fallback on its first firing (kept as "
                 "opus48_FALLBACK_rerule_20260925.md, below).  Verbatim head: \"C3: STANDS  D7: FLOOR  Q3: ADOPT  STOP: "
                 "RATIFY\".  It re-anchors D7 (the latch is a floor axis), Q3 (the suppressing-guard clause, into the "
                 "carrier) and STOP (roster validity as an explicit fourth part) and lists what #529 owed."))
    E.append(ent("review", "fable5", "2026-09-25", "", RR + "opus48_FALLBACK_rerule_20260925.md",
                 "[NOT A SEAT ANSWER] The re-ruling's first firing was written by claude-opus-4-8 after a refusal by "
                 "claude-fable-5-1 (agent_models.py); kept as evidence, relabelled, never counted as the seat."))
    E.append(ent("review", "codex", "2026-09-26", "CONFIRM WITH CHANGES", RR + "codex_astra529rerule.txt",
                 "#529 ASTRA -- GPT-6 Astra (codex, tools/cxlaunch.sh, pointer form) confirming the flagship's 09-25 "
                 "re-ruling, after the 07:01 reset.  Verbatim: \"VERDICT: CONFIRM WITH CHANGES\".  Changes: the Q3 clause "
                 "states the latch interlock and keeps the one-dispatch bound and the one-device flag; the split widths "
                 "3/5/6/7 are unreachable only CONDITIONALLY (DEV_CRIME_LENGTH == 0x280); translations disclosed; the "
                 "eight unlisted bucket members need an L4 enumeration with justified dispositions, NOT filing."))
    # -- the tables (main-loop measurement records) --------------------------------------------------------------------
    for date, d, text in (
            ("2026-09-25", "table13a_20260925/", "TABLE 13a (the INTMASK and CONTROL-write label swaps the stop condition "
             "required MEASURED): CHECK13A_PASS -- base 204/204, M7_intmasklatch 201/204, M8_ctllatch 201/204, each "
             "exact against PRETABLE13a.out.  No INTMASK or CONTROL carrier owed."),
            ("2026-09-26", "table14_20260926/", "TABLE 14 (repair 15: the TIME and REV decline carriers, the entries "
             "13-and-17 pair): CHECK14_PASS, 18 legs exact -- base 218/218 on probe f5e915f6; M3_timelatch and "
             "M5_revlatch 214/218 (were 204/204 escapes); M6/M7/M8 215/218; D_nodogclear 216/218."),
            ("2026-09-26", "table15a_20260926/", "TABLE 15a (pass 2's finding): H_noresetclear and E_noendianclear "
             "218/218, both escapes AS PREDICTED -- the HARD_RESET clear's residue had no row; ENDIANESS disclosed."),
            ("2026-09-26", "table16_20260926/", "TABLE 16 (repair 16: the CONTROL arm's residue-text count for each "
             "clear in both latch states): CHECK16_PASS, 25/25 legs exact on probe 5f770991 (226 rows) -- H_noresetclear "
             "and E_noendianclear now detected; W_istlb and W_imklb 226/226 as predicted (disclosed)."),
    ):
        E.append(ent("assess", "fable5", date, "", A + d + ("POSTTABLE" + d.split("_")[0][5:] + ".out"),
                     "[NOT A SEAT ANSWER] #529 main loop, GXEMUL [087a90]: " + text + "  PRETABLE written before the "
                     "table (mtime order); scratch clone /tmp/gxopus_r14 restored cmp-clean, no .MUTANT."))
    # -- repair 15's pass 2 --------------------------------------------------------------------------------------------
    E += panel(P15, "2026-09-26", "#529 REPAIR 15's PASS 2 (the full roster on the repair diff)", {
        "codex": "not re-fired on this pass: codex answered repair 16's F2 pass, which consolidated these findings",
        "agy": "**VERDICT: GO**",
        "grok": "VERDICT: PASS.",
        "glm": "The adjudicated floor itself is CLOSED -- every {observable label} x {latch SET} cell has a kill in the "
               "inlined table 14 ... but three of the brief's own claims fail audit",
        "deepseek": "VERDICT: REJECT / NOT RATIFY -- Q1(b) is false from the inlined session timing; Q1(d) is unsupported.",
        "minimax": "VERDICT: REPAIR 15 IS SOUND. THE 218-ROW COMPOSITE CLOSES THE FLOOR FOR THE DECLINE-SUPPRESSION CLASS "
                   "AT THE FIVE GUEST-OBSERVABLE LABELS.",
        "kimi": "The repair-15 diff is sound as cut -- row arithmetic closes (204+14=218), all 18 legs match their "
                "pre-registered red sets exactly ... but the closing claim"}, KIMI_CLI)
    E.append(ent("review", "grok", "2026-09-26", "DEDICATED: BREAK FOUND", R15 + "grok_dedicated_r15p2.txt",
                 "#529 repair 15's pass 2: the DEDICATED adversarial grok job.  Verbatim: \"**BREAK FOUND.**\" -- deleting "
                 "the CONTROL arm's HARD_RESET clear escapes the 218-row probe (measured in table 15a; graded L2 by the "
                 "flagship; closed by repair 16).  Dispositions: " + DISP + "."))
    E.append(ent("review", "opus5", "2026-09-26", "THE RULED FLOOR IS CLOSED; THE CONTRACT'S CLAIM IS NOT",
                 A + "opus_r15p2_20260926/opus5_r15p2.md",
                 "#529 repair 15's pass 2: the Opus 5 MEASURING seat (Agent tool; claude-opus-5-5 by agent_models.py; "
                 "every run in /tmp).  Verbatim: \"THE RULED FLOOR IS CLOSED; THE CONTRACT'S CLAIM IS NOT\".  Badge s."))
    E.append(ent("review", "fable5", "2026-09-26", "DO NOT CLOSE", R15 + "fable5_r15p2.md",
                 "#529 repair 15's pass 2: the FLAGSHIP seat, LAST (claude-fable-5-1 by agent_models.py, on its RESUMED "
                 "agent after an opus-4-8 fallback, below).  Verbatim: \"DO NOT CLOSE. Repair 15's rows and table 14 are "
                 "sound and exact, but one DERIVED floor escape (delete `idata &= ~CRIME_CONTROL_HARD_RESET;`) is graded "
                 "L2 like its DOG twin\" -- measured in table 15a, repaired by repair 16."))
    E.append(ent("review", "fable5", "2026-09-26", "", R15 + "opus48_FALLBACK_r15p2.md",
                 "[NOT A SEAT ANSWER] The flagship's first answer on repair 15's pass 2 was written by claude-opus-4-8 "
                 "after two refusals by claude-fable-5-1 (agent_models.py); relabelled, never counted as the seat."))
    # -- repair 16's F2 pass -------------------------------------------------------------------------------------------
    E += panel(P16, "2026-09-26", "#529 REPAIR 16's F2 PASS (the adjudication pass: every seat's pass-2 findings, "
               "consolidated with dispositions)", {
        "codex": "RE-FIRED after the reset as codex_f2.txt (the next entry)",
        "agy": "**VERDICT: GO-WITH-CHANGES.**",
        "grok": "\"VERDICT: F4 is the wrong disposition.\" (the verdict follows a preamble)",
        "glm": "\"UPHOLD every disposition except F20 -- the residue-VALUE cell.\"",
        "deepseek": "it would overturn D4/F2, arguing that the ENDIANESS coverage is unlicensed scope growth",
        "minimax": "it largely upholds the dispositions but would overturn F2 FIRST, on the ENDIANESS scope objection",
        "kimi": "it would overturn F20 first and take the value anchor, citing the F4/F2 precedent and the existing "
                "row-note overclaim"}, KIMI_CLI)
    E.append(ent("review", "codex", "2026-09-26", "UPHOLD REPAIR 16'S BOUNDED COUNT COVERAGE", R16 + "codex_f2.txt",
                 "#529 repair 16's F2 pass: the codex SEAT, re-fired after the 07:01 reset (GPT-6 Astra max, cxlaunch.sh "
                 "pointer form, the label-corrected packet f2_packet_codex_v2.md).  Verbatim: \"VERDICT: UPHOLD REPAIR "
                 "16'S BOUNDED COUNT COVERAGE; CORRECT THE SESSION COUNT AND QUALIFY THE ROW-VALIDATION CLAIM.\""))
    E.append(ent("review", "codex", "2026-09-26", "DEDICATED: TRUE AS WRITTEN", R16 + "codex_f2ded.txt",
                 "#529 repair 16's F2 pass: the DEDICATED codex job.  Verbatim: \"VERDICT: TRUE as written: every clear "
                 "has a residue-count check in both latch states. Residue-value and combined reset/print coverage remain "
                 "incomplete.\""))
    E.append(ent("review", "grok", "2026-09-26", "DEDICATED: OVERTURN THE CLOSURE HALF OF F1", R16 + "grok_dedicated_f2.txt",
                 "#529 repair 16's F2 pass: the DEDICATED adversarial grok job.  Verbatim: \"**OVERTURN the closure half "
                 "of F1.**\" -- the bit-conditioned family (HARD_RESET and ENDIANESS members, derived to escape); the "
                 "flagship graded it clause (e), disclosed as a family in r17."))
    E.append(ent("review", "opus5", "2026-09-26", "REPAIR 16'S ROWS ARE RIGHT", R16 + "opus5_f2.md",
                 "#529 repair 16's F2 pass: the Opus 5 MEASURING seat (claude-opus-5-5 by agent_models.py; runs in "
                 "opus_f2/).  Verbatim: \"REPAIR 16'S ROWS ARE RIGHT, AND ONE ADOPTED OPTION OF MINE IS WRONG AS FRAMED.\"  "
                 "It measured S_rst4clr (the `ctlrst sw halt' kill), M_ctldebug and T_halttwin.  Badge s."))
    E.append(ent("review", "fable5", "2026-09-26", "THE CHAIN CLOSES ON THIS PASS", R16 + "fable5_f2_adjudication.md",
                 "#529 repair 16's F2 pass: the FLAGSHIP seat, LAST (claude-fable-5-1 by agent_models.py; one mid-run "
                 "refusal event, recovered on the same model -- the answer and the final text are fable-5-1).  Verbatim: "
                 "\"THE CHAIN CLOSES ON THIS PASS -- zero floor breaches survive adjudication on a valid, full-roster "
                 "pass; repair 16's rows all stand; NO row is owed.\"  X1 and X3 graded clause (e); its Q3 items 1-12 "
                 "applied as r17, item 13's records outside the probe landing with #529's commit, r18 adding GPT-6 "
                 "Astra's r17 audit and the ACCEPTS-46 enumeration, r19 one docstring sentence from Astra's "
                 "second records audit (2026-09-28), and r20 the final ruling's comment correction at ACCEPTS entry 21 "
                 "plus the MEASURED/derived qualifier (2026-09-30), r21 the four text fixes of Astra's confirmation "
                  "of that ruling, and r22 one docstring qualifier the precommit hook's score-claim check required (the committed text)."))
    E.append(ent("regress", "fable5", "2026-09-26", "THE CHAIN CLOSES", R16 + "fable5_f2_adjudication.md",
                 "#529 FINAL, the FLAGSHIP seat (regress is fable5-only): the enumeration closed on repair 16's F2 pass "
                 "with its denominator (the ruling's Q2), CONDITIONAL on the text corrections (r17, r18, r19, r20, r21, then r22 -- the committed text), a base leg "
                  "on the final bytes (final529r22_20261002/probe_base_r22.raw: Base leg on r22 against table 16's base binary (2026-10-02, WALL 1235 s): 226/226, CONTROL OK; 21 differing row pairs against table 16's base log -- 15 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r22_20261002/probe_base_r22.raw`).; r21's leg, final529r21_20260930/probe_base_r21.raw: Base leg on r21 against table 16's base binary (2026-10-01, WALL 1233 s): 226/226, CONTROL OK; 23 differing row pairs against table 16's base log -- 17 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 0 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r21_20260930/probe_base_r21.raw`).; r20's leg, final529r20_20260930/: Base leg on r20 against table 16's base binary (2026-09-30, WALL 1229 s): 226/226, CONTROL OK; 27 differing row pairs against table 16's base log -- 21 timing-dependent TIME values and the 6 rows of the three rewritten notes -- and 4 row pair(s) differing only in column padding after normalising those; no want, got or verdict column differs (`final529r20_20260930/probe_base_r20.raw`).; the r18 and r19 legs, "
                 "final529r18_20260926/ and final529r19_20260930/, 226/226 each), the S_rst4clr attribution kept durable "
                 "(opus_f2/), GPT-6 Astra's confirmation and #549-first ordering; no row was ordered.  The final probe is "
                 "code-identical to repair 16 but for three row notes (final529r17_20260926/mk_r17.py.txt, "
                 "final529r18_20260926/mk_r18.py.txt, final529r19_20260930/mk_r19.py.txt, final529r20_20260930/mk_r20.py.txt, "
                  "final529r21_20260930/mk_r21.py.txt, final529r22_20261002/mk_r22.py.txt)."))
    r["entries"] += E
    old = r.get("state_note") or ""
    r["state_note"] = ("*** STATUS 2026-10-02 (GXEMUL [087a90]): CLOSED by #529.  The fix is unchanged since 2026-09-13 "
                       "(dev_sgi_ip32.c 8c1d1545); the detector is repair 16's 226 rows with the F2 adjudication's text "
                       "(r17), GPT-6 Astra's r17 audit and the measured ACCEPTS-46 enumeration (r18), one sentence from "
                       "Astra's second records audit (r19), the flagship's final ruling (r20) and Astra's confirmation of "
                       "it (r21) and one docstring qualifier the precommit hook required (r22, the committed text); the chain closed on repair 16's F2 pass, and the final ruling of "
                       "2026-09-30 was confirmed the same day with two text dispositions overturned.  The note below said "
                       "\"NOTHING MEASURED ... Next: fire table 12\" -- stale from 2026-09-17 08:53, when table 12 "
                       "completed. ***\n\n" + old)
    r["state"] = "closed"
    r["witness"] = ("probe:regress/artifacts/crimewidthkill/crime_width_witness_20260913.py -- rung 3 on unmodified "
                    "-E sgi -e ip32: committed build 3/15 (every refusal row red, the three controls green: "
                    "witness_committed.out), fix 15/15 (witness_fix.out)")
    r["closure"] = {"by": "fable5-mainloop", "badge": "A", "note": (
        "#529 CLOSES.  A guest lb/lbu/lh/lhu/sb/sh to the IP32 CRIME ended the emulator; the width is declined with one "
        "(once) announce and a goto to the common tail.  The detector, regress/crime_width_probe.py, reached 226 rows "
        "through sixteen repairs and sixteen kill tables; the chain closed on repair 16's F2 pass (the flagship: zero "
        "surviving floor breaches with the denominator; no row owed), GPT-6 Astra confirming.  Three earlier 'fable5' "
        "rulings were opus-4-8 fallbacks, re-ruled first-hand on 2026-09-25.  Filed: crimectllane, crimebankorder, "
        "crimecontroldebt.  Badge A: the main loop adjudicated its own round's records.")}
    file_rows(L)
    L["updated"] = "2026-10-02"
    save(L)
    print("records: crimewidthkill +%d entries, 4 fallback entries tagged, CLOSED; 3 filed rows" % len(E))


FILED = [
    ("crimectllane", "HIGH", "dev_sgi_ip32.c's CRIME_CONTROL arm matches the exact label 0x08 and acts on the raw idata of "
     "any width: a 32-bit sw 0x800 to +0x08 (the HIGH half on this big-endian machine) stops every CPU, while the +0x0c "
     "write NetBSD makes stores the low word and reaches the default arm's log, bypassing CONTROL's reset/watchdog "
     "handling -- #529's sw08/sh08 rows use it as a channel and owe re-derivation when the lane model is fixed"),
    ("crimebankorder", "LOW", "the CRIME prelude writes CRIME_MEM_BANK_CTRL0/8 + bank at CONTIGUOUS offsets while "
     "crimereg.h defines the bank registers INTERLEAVED -- and the header itself collides CTRL7 with REFRESH_CNTR; needs a "
     "boot witness before any edit"),
    ("crimecontroldebt", "LOW", "the eight strengthenings #529's review FILED rather than owed -- seven by the F2 adjudication (a value anchor "
     "beside the CONTROL prefix count; a latch-SET sh 0x0201; one free-running accepted sw; an lb after the first refusal "
     "at INTSTAT/INTMASK; six latch-CLEAR first-refusal sessions; a refusal while the line is asserted; an sw 0x0801 "
     "last store) and entry 34's seeded sd +0x40 row from the final ruling (clause (e): its latch-CLEAR +0x40 slot is unrowed while the default-label "
     "8-byte-store cell is held at +0x278; re-runs S55/S58's kills), each with its measured or derived kill and its "
     "re-run cost"),
]


def file_rows(L):
    ids = {x["id"] for x in L["rows"]}
    for rid, sev, title in FILED:
        if rid in ids:
            sys.exit("REFUSED: %s already exists" % rid)
        L["rows"].append({"id": rid, "title": title, "sev": sev, "state": "open", "opened": "2026-10-02", "commits": "",
                          "witness": "", "hold_question": "",
                          "entries": [ent("assess", "fable5", "2026-10-02", "", A,
                                          "[NOT A SEAT ANSWER] Filed by GXEMUL [087a90] (main loop) from #529's review -- "
                                          "the finding, its seats and its evidence are in OUTSTANDING_BUGS.md "
                                          "(2026-10-02 section) and regress/artifacts/crimewidthkill/.")]})


def opus(grade, ev):
    L = load()
    row(L, "crimewidthkill")["entries"].append(ent(
        "review", "opus5", "2026-09-26", grade, ev,
        "#529 the Opus 5 MEASURING seat on the contract's ACCEPTS-46 buckets (GPT-6 Astra's confirmation of the 09-25 "
        "re-ruling asked for an L4 enumeration with justified dispositions).  Verbatim verdict: %s.  Badge s." % grade))
    save(L)
    print("opus", grade)


def astra(verdict, ev):
    L = load()
    row(L, "crimewidthkill")["entries"].append(ent(
        "review", "codex", "2026-09-30", verdict, ev,
        "#529 ASTRA -- the confirming seat (GPT-6 Astra ultra, pointer form) on the flagship's FINAL ruling of 2026-09-30 "
        "and the r20 text (owner rulings 2026-09-25/-30: Fable adjudicates, Astra confirms).  Two dispositions overturned "
        "(item 6's \"no row seeds TIME's upper word\" is false -- the gapped sessions seed it; the closing-revision "
        "exemption contradicts the late-dissent rule, so r21 and its own base leg were REQUIRED), four wording changes, "
        "HIGH and the carrier clause right.  r21 and r22 were built and measured AFTER this confirmation; the r20-to-r22 text delta was put to GPT-6 Astra on "
        "2026-10-02 (final529r22_20261002/codex_astra_r22.txt), a second ledger entry.  "
        "Its verdict, verbatim: %s."
        % verdict))
    row(L, "crimewidthkill")["entries"].append(ent(
        "review", "codex", "2026-10-02", "CONFIRM WITH CHANGES (8)",
        "regress/artifacts/crimewidthkill/final529r22_20261002/codex_astra_r22.txt",
        "#529 ASTRA on the r20-to-r22 TEXT DELTA and the records corrections (GPT-6 Astra ultra, pointer form; brief "
        "final529r22_20261002/astra_confirm_r22.md).  Verbatim: 'CONFIRM WITH CHANGES (8) -- the five probe edits stand, "
        "but eight records claims need correction.'  All four r21 pairs and the r22 qualifier confirmed -- pairs 1-3 "
        "against dev_sgi_ip32.c and the probe's sessions, pair 4 and the qualifier against the preserved measurement "
        "records (opus_accepts46.md; closing pass 7's scripts and F3 log); its six corrections of 2026-09-30 found applied; eight further "
        "records corrections applied with its replacement texts before the commit (fix529_astra_r22.py); no probe "
        "text changed.  DENOMINATOR, its own: 5 of 5 pairs; 6 of 6 corrections; every sentence of the r22 docstring "
        "and of records_drafts.md read."))
    save(L)
    print("astra", verdict)


def sha(s):
    L = load()
    row(L, "crimewidthkill")["commits"] = s
    sh = row(L, "scorehyphenfp")
    if sh.get("commits") in ("", [], None):
        sh["commits"] = s
    save(L)
    print("sha", s)


def setcommits(rid, s):
    L = load()
    row(L, rid)["commits"] = s
    save(L)
    print("setcommits", rid, s)


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else ""
    if m == "records" and len(sys.argv) == 2:
        records()
    elif m == "opus" and len(sys.argv) == 4:
        opus(sys.argv[2], sys.argv[3])
    elif m == "astra" and len(sys.argv) == 4:
        astra(sys.argv[2], sys.argv[3])
    elif m == "sha" and len(sys.argv) == 3:
        sha(sys.argv[2])
    elif m == "setcommits" and len(sys.argv) == 4:
        setcommits(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)

