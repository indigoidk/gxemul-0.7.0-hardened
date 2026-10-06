# `#558` (idlessaudit): agy's read-only audit of `#555`'s committed table -- 16 flags; one opens three MB89352 host-stop rows (HIGH), the rest change nothing; `boilerplateprefix`'s commits field filled

**Why.**  The owner's instruction of 2026-10-02 is to keep agy on read-only audits and to CHECK its flags.  `#555`
(`c29a5fd3`) was the largest records commit of the week -- 40 new rows, 104 pointed passages, 22 kept entries -- and
had been read by grok and Astra but by no third reader.

**How.**  Six briefs generated from the committed tables (`regress/artifacts/idlessaudit_20261002/briefs/`,
`mk_agy_idless2.py.txt`), run through the agy pack runner at MAXJ 2.  Five answered; `icite2_2` walled on launch
(`error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 101h48m29s.`) and the runner, which would have slept until the stated reset, was stopped.  agy flagged 16 items; each was
checked by the main loop against `IDLESS_TABLE2.tsv` and the ledger at `c29a5fd3` (`AGY_FLAGS_DISPOSITION.md`), the
disposition was put to GPT-6 Astra as "which of the sixteen is wrong?" (1 of 16 dispositions wrong), Astra's one finding went to grok for a
ruling (the owner's arrangement: grok rules Astra's findings, Astra confirms), and Astra confirmed the ruling against
the source (CONFIRMED WITH CHANGES (3) -- correct reachability explanations, qualify carrier/title scope, and label evidence as source-only; retain three HIGH rows).

**What the flags were.**  5 PARTLY: the `ifiled2` briefs listed, per passage, the id `#555` POINTS it at; where
`#555` also FILED a new row on the same lines, the pointer alone was listed, so agy correctly found the pointer partial.
For four, the new rows carry every "left-out" item (`armcp15cp14exits`, `qhnetxlog`, `qhppciphack`, `qhscifssr`, `qhslowifetch`).  For the fifth -- queue passage 2616, "dev_mb89352
fatal errors" -- `qhm88kstops` names ONE of the device's ten `cpu->running = 0` sites, and no row names the rest.
11 OWED: the `ikeep2` brief asked for OWED on any KEEP-AS-IS entry whose work is undone, "whatever the ruling
says"; the eleven are exactly the entries `#555` kept because an existing row records the open work in its own text
(`armbfiwidth`, `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`).  Nothing is owed by `#555` for them.  (The disposition's first draft called them "clause-(e) debt under a live
row, which owes nothing"; Astra corrected that framing -- clause (e) distinguishes a declared exclusion from a breach,
and a live row exempts nothing -- and v2 states the test that was actually applied.)

**What ships.**  `tools/pipeline/ledger.json`, `matrix.html` -- three new rows after `qhm88kstops` (`qhmbphasestops`, `qhmbunimplstops`, `qhmbbufendstops`, HIGH,
open; sites, reaching paths, carriers and fix shapes in their notes, reachability marked as a reading); ten entries on
`idlesslow` (one per agy brief including the wall, Astra's check, grok's ruling, Astra's confirmation, the main-loop
disposition); `boilerplateprefix.commits = e1871fa5` plus its regress hold (the field `#557`'s post step filled in the working ledger and
left to this commit for the committed one).  `OUTSTANDING_BUGS.md` -- the `#558` section with the three rows.
`regress/artifacts/idlessaudit_20261002/` -- 27 files: the briefs, the five answers, the wall's `.err` (kept because
it is the whole answer), the disposition (v2), Astra's check, grok's ruling, Astra's confirmation, the generator, the
runner's results.

**Seats, by name.**  agy: five of six (one WALLED, a seat failure).  GPT-6 Astra: two checks and a confirmation; no
wall, no refusal.  grok: one ruling.  Fable and Opus agent seats deliberately not fired (owner, 2026-10-02); kimi down;
Ollama not fired.  No `src/` touched; no pass-2 receipt owed.

