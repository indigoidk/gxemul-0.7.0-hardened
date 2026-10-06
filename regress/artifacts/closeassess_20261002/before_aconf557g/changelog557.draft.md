# `#557` (closeassess): the rows closed with no commit are audited -- 18 commits fields filled, 4 members added to `closeassessrows`, the parked `boilerplateprefix` repair landed with its comment corrected, one parked repair held

**Why.**  `#555` filed `closeassessrows`: a 2026-08-27 sweep closed rows on the adjudicator's note `CLOSE (assess)`,
which signs off the assess STAGE, and eight of them still named undone work.  The class draws from every row that is
`closed` with an empty `commits` field (47).  This unit reads the rest of that population and records what each is.

**How.**  grok read the 37 rows no seat had read, one line each with the lines it read
(`regress/artifacts/closeassess_20261002/grok/grok_closedcensus.txt`: 20 shipped, 14 nothing owed, 3 work still alive, 0 not determined, of 37 rows); GPT-6 Astra confirmed 34, overturned 3
and looked up every commit (`aconf_census/codex_aconf_census.txt`: 34 confirmed, 3 wrong, 0 not checked, of 37 rows; commits to fill: 9 confirmed of 9).  The three overturns are the point of a
second seat: `smhang` (its standing regression is deferred, not shipped), `gdromcontractresidual` (its corrections
are not at HEAD) and `boilerplateprefix` (grok had read the WORKING copy of the checker, where the repair sits
uncommitted; HEAD still had `PREFIX = 60`).  Every sha is re-checked by the staging script: the commit exists and
touches the file named or names the row or its round.

**What ships.**
* `tools/pipeline/ledger.json`, `matrix.html` -- 18 commits fields filled (17 of the census's twenty shipped rows, plus
  `xfamscope` from the ten rows read before it); `asanunbuildable` and `wiringshghost` left empty on purpose
  with a note (a populated field for work that did not ship is the opposite failure); 4 rows noted as members of
  `closeassessrows` (`cmtattr`, `gdromcontractresidual`, `smhang`, `unreadseats23`; the class row's note now lists 12); `boilerplateprefix` noted as landed.  AND what the
  gates demanded once the fields were filled (the 19:10 precheck, three hard fails): 3 witness fields added and 2
  re-shaped (section K), 8 regress holds with questions on `fbwitness`, `lcalenzerodrop`, `ledgerwitness`, `m88kexcrrtrapmode`, `nineseatreminder`, `scorehyphenfp`, `smhang`, `xfamscope` (section I), and `hrecordowed.commits = 1329d894`
  (section L: a pre-existing #556 leftover the same precheck found, not a consequence of the fills).  K's witness rule and
  I's missing-regress rule both key on the commits field, so a row closed with no commit escapes exactly those two;
  eighteen fills produced thirteen obligations (3 + 2 + 8), all discharged or held here.
* `tools/pipeline/fable_queue.md` -- committed as HEAD plus its GENERATED block regenerated from the staged ledger
  (`gen_codex_wall.py`), so the eight regress holds are named in the queue; the working copy's uncommitted prose is
  untouched and not committed.
* `tools/pipeline/check_boilerplate.py` -- the parked 2026-09-17 repair, landed: the comparison key is the whole
  seat note (`strip_seat(note, seat).casefold()`), `EXCERPT = 60` is display width only; three code lines, the rest
  comment.  Astra's review of the parked diff (`aconf_parked/codex_aconf_parked.txt`: boilerplateprefix HOLD; gdromcontractresidual HOLD) held it for its COMMENT:
  the quoted preamble is 81 characters, not 66; "on the day it landed" described a landing that never happened; the
  recall sentence overstated; the header promised a prefix comparison and said the check was outside the hard gate.
  All four corrected in place with what they said kept.  Controls re-run today on scratch copies of the working
  ledger: the untouched ledger `BOILERPLATE_PASS 54 archived, 0 new`; one identical paragraph injected across four seat
  cells after the cutoff `BOILERPLATE_FAIL` naming the row (`draft/boilerplate_controls_20261002.out`).
* `OUTSTANDING_BUGS.md` -- the `#557` section: the shipped rows with their shas, the 14 nothing-owed, the members,
  the two parked repairs.
* `regress/artifacts/closeassess_20261002/` -- 62 files: the census, its confirmation, the parked diffs, the
  controls, the briefs and the scripts.

**Held: the other parked repair.**  `regress/gdrom_default_probe.py`'s parked edit is not docstring-only: Astra found
two executable rows added and a third tightened (`row()` sites 54 -> 56; the gate pins 60, the working probe makes
62), a detector change that belongs to `M2_gdromnodatawidth` and `gdromacceptdmanum` and owes a round with a pass on
the diff, plus one claim that contradicts the `gdromdmasilent` record.  It stays uncommitted in the working tree, and
`gdromcontractresidual` is a member.

**Astra's closing checks of this unit.**  `aconf_557`: 6 things wrong (A: 2, B: 0, C: 3, D: 1) -- a deferral dated wrong (2026-08-19, not 08-30), a
commit described as a deletion when it recorded one, a stale artifact count, and `xfamscope`'s commits not looked up;
all repaired.  `aconf_557b`, on those: 2 things wrong -- `wiringshghost`'s field is left EMPTY after all (no commit shipped
the deletion), and a placeholder had moved.  `aconf_557c`, on those two: 1 things wrong -- the class row's note still said ONE
field left empty; it now derives its counts from the two census artifacts and names the two rows (`smhang`,
`boilerplateprefix`) that sit in both the shipped twenty and the alive five, and the message says the same.
`aconf_557d`, on that: CLOSES -- the repair is right and nothing else changed -- clean; then the precheck failed three hard sections (K and I on the filled rows, L on
`#556`'s `hrecordowed`) and the repairs went to `aconf_557e`: 4 things wrong -- a witness condition the commit did not record, the
queue block not regenerated, `hrecordowed`'s numbers, and the invisibility claim overstated; all four repaired, checked by
`aconf_557f`: 1 things wrong -- one clause ("owes nothing on paper") still overstated, qualified to "under those two rules";
`aconf_557g`: <OWED: aconf_557g>.

**Seats, by name.**  grok (grok-4.7 xhigh): the census.  GPT-6 Astra (codex, `ultra`): the confirmation, the git
log, the review of the parked repairs, the closing check; no wall, no refusal.  agy: not on this unit (its quota wall
lifted at 18:21 and it is auditing `#555`'s table).  The Fable and Opus agent seats were deliberately not fired
(owner instruction, 2026-10-02); kimi down; Ollama not fired.

**Not done, and where it goes.**  Re-opening any member is one decision per member, for the owner or the flagship.
The parked probe edit: its own round.  This commit touches no `src/`; the next one owes it no pass-2 receipt.

