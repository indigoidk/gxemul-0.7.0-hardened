# RULINGS -- packet C (records and harness), 2026-10-16

Consolidated by the main loop (Opus 5.5, 087a90) from three independent adjudications of `packet_C_records.md`:

| seat | answer | verdict |
|---|---|---|
| GPT-6 Astra (ultra) | `astra/C_records/codex_adjC.txt` (rc 0, launch.log) | UPHOLD WITH CHANGES (5 changed) |
| Grok 4.7 (xhigh, plan mode; `git show` was blocked in its seat) | `grok/C_records/grok_adjC.txt` (rc 0, 581 s) | UPHOLD WITH CHANGES (8 changed) |
| Fable 5.1 (agent_models.py: clean claude-fable-5-1; one refusal turn at 11:48 CDT, the run continued on Fable) | `fable5/fable5_adj_C_records.md`, receipts `fable5/meas_C/` | UPHOLD WITH CHANGES (7 refined, none overturned) |

Roster: 3 of 3 answered.  Nothing was overturned outright by any seat; every change is a refinement.  Where the seats
differ, the ruling below follows the argument, not the count, and names it.

## Final rulings

**F1 `cxlaunchquotation` -- UPHELD (3/3): land the production rule into tracked `tools/cxlaunch.sh`.**
- Premise MEASURED by Fable (`fable5/meas_C/launchlog_census.txt`): 387 launch lines; 362 rc 0 with stdout, 25 rc 1
  with empty stdout, ZERO off-diagonal.  So N4 (rc 1 with an answer) and Grok's rc-0-empty-with-quoted-wall case have
  no instance on record.
- CORRECTION to the packet: "has run every Astra job since 2026-09-26" is FALSE (Astra: the 10-09 receipt
  `fablequeue8n_20261009/astra_confirm/cxlaunch_asicconverge_stdout.txt` shows an rc-0, 10,466-byte answer WALLED --
  that run did not use the production launcher).  Cite the 09-28 dossier receipt
  (`codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log`) as the real Daybreak-fallback evidence, separately
  from the classifier fixtures.
- The landed comment states the actual condition (`rc != 0` OR empty stdout), not "only a failed run" (Grok).
- ADD the ANSI strip before the `^ERROR:` anchor (Fable): 7 of 453 panel.sh `codex.txt` files carry ANSI-coloured
  `ERROR:` lines (`fable5/meas_C/ansi_census.txt`; 0 of 593 launcher `.err`), and under the production rule a coloured
  real wall reads exit 6 "seat down" (Fable's Q3, `meas_C/cxctl_fable/`).  Licensed by a transferred warrant (real codex
  output of that shape), with Q3 as its control.
- Controls for the landing: the six RECEIPT.txt fixtures, Fable's Q1-Q3, plus two named residuals recorded, not fixed:
  N4 (rc 1 with an answer and quoted wall text -> exit 8) and its refusal twin (a quoted `flagged for possible
  cybersecurity` line on rc != 0 -> Daybreak re-run and the answer renamed `.refused.*`, Grok).
- WITHDRAWN: the packet's parked "read only codex's final `ERROR:` line" refinement (Grok: the final `ERROR:` line in
  N4 is itself a quotation, so it still walls; Astra: ownership of the last line is not established).
- MERGE the prior filing `cxlaunchwallfp` (OUTSTANDING_BUGS.md:22494-22503, 2026-09-26, no ledger row) into this
  landing (Fable); correct OB:24714-24716 and ledger :62489 to this rule; closes `cxlaunchdaybreak` (ultra + Daybreak
  ride along).
- NEW, from Astra: the launcher prints the model it RAN but `ANSWERED_BY` is the model it ASKED for -- the "a wrong name is
  a SEAT FAILURE" comment is unenforced.  File as a rider on the landing (compare the `^model:` header to the request).

**F2 / D2 `dashokclass` -- UPHELD with the class re-keyed (Grok and Fable independently; Astra agrees on the semantics).**
- Every mechanical sweep stays withdrawn (3/3).
- The legacy class is keyed on the DOMAIN, not the spelling: every explicit `d` outside the four glyphs renders as one
  residue class, labelled "legacy -- verdict unclassified" (adapted from Astra's "legacy OK — verdict unclassified";
  this said "Astra's wording" until the 2026-10-17 dashokclass landing -- Fable 5.1 and GPT-6 Astra, adjudication pass),
  text kept, notes and hold/record precedence
  preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at e483d931, where it was
  measured -- 5,167 at c64445fa, which committed this file, Fable 5.1, v4 pass; 5,177 at the landing's HEAD, 8bf8b5a1).
  Keyed on `OK` alone
  it would leave 958 of 1,397 off-domain entries in the false `pend` class (Fable, `meas_C/okdomain_census.txt`: OK 439,
  other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7).
- The forward domain check keeps Astra's four completeness conditions; a date-only cutoff cannot stop a back-dated or
  undated new entry, so the check also defines grandfathering against the existing entries and the missing-date case.
- Its rendering control must show `OK` NOT rendered as approval, canonical approvals still ✓, and semantic holds/records
  unchanged.  Note the denominator: 439 stored entries, 365 displayed cells (Astra).

**F3 -- UPHELD (3/3).** Both 2026-10-16 agy probes exit 1 with empty stdout (`agyprobe_rc/`).  They do not establish the
2026-10-13 exit statuses retroactively.

**F4 `agyselfupdate` -- FILE, low (3/3), causation INFERRED.**  The rc-127 launch failure is measured; the self-update
as its cause is inferred (the `.old` suffix decodes to the rename time, 11:21 today; the `.old` file's own mtime is
2026-10-13 22:33).  The row owes: rc 127 / "No such file" = LAUNCH FAILURE, re-fire once, with a control that an
ANSWERED job is never re-fired (Fable); the PRE-FLIGHT path (Astra: `agylaunch.sh:28`'s `agy models` failure becomes
"model absent", exit 5, which stops the whole pack -- capture its status and distinguish inventory failure from absence);
and one serial `agy models` in the pack runner before any concurrent launch (Fable).

**F5 -- UPHELD in part; the `armbdt` line correction is REJECTED (3/3).**  `:5796` (VERDICT), `:6206` / `:6346`
(`codex` headers) are the physical lines on both copies; Astra v2's +9 comes from counting form-feed characters
(`splitlines()`), so record the dual count rather than replacing a true citation (Grok).  The other corrections stand:
C3 is 19 bytes; seven controls become six after C3's withdrawal; "none was found when it was written" sharpened to the
mtimes (none at 21:44 when the control ran; a durable receipt at 22:06:57, before v1 was final -- Fable); the kimi
count is 11 under "substitute answered" (18 under a loose grep -- state the criterion); 48/49 remains a reading that
owes a post-repin run.

**F6 `seatverdictrefusal` -- FILE (3/3), carrying Astra's N3 correction.**  Under v3 (`v2/sv_v3.py`), a substantive
answer that quotes a STRONG wall phrase inside the last 4,000 bytes and carries no recognised verdict scores WALLED
(`is_walled = ... and not v` -- the verdict gate, not the window, rescues the other fixtures).  Disclose it as the
STRONG-phrase class's standing behaviour and add the format-miss negative control; specify the terminal test so it
accepts the real 284-byte kimi wall's one-line `See log:` trailer (Grok).  "Zero verdict changes" reads "zero
verdict-ONLY changes" (15 verdict fields clear alongside class changes).

**F7 `wdczerolendatain` -- FILE (3/3)**, bounded: the source establishes the presentation (zero-length allocation ->
DATAIN with DRQ and no bytes); any guest/driver consequence owes a rung-3 attempt.

**F8 -- the #560/#561 edit list STANDS; the execution procedure is CHANGED (Fable; Grok concurs on the peer file).**
- Staging a comment hunk from HEAD's blob into a file whose working copy carries the PEER's uncommitted edits
  (`src/devices/dev_pcc2.c`, `src/cpus/cpu_alpha_palcode.c`) would be silently REVERTED by the peer's next commit of that
  file.  RULING: HOLD those two files' hunks until the peer commits them (do not edit the peer's working files); land
  the rest.
- Before staging the #560 `dev_pcc2.c` replacement, diff it against the peer's working-tree paragraph that already marks
  the old sentence false with a 14/16 KILLED measurement (Grok).
- Astra v1's four UNCHECKABLE clauses (#561 places 2, 29, 39, 40) stay out of the landed comments until checked (Grok).
- Fold in E53 (place 14's text cites OB:14809-14812, now :14821) and E54 (an erratum: `est/` has no `regress/`, so the
  "regress edits owe est/ identity" sentence in the 10-13 adjudication and HARVEST is wrong) (Fable).
- `regress/diff_ieee_store.c` gains precommit E's `[IDENTITY]` row in the same commit (3/3).

**F9, F10 -- UPHELD (3/3).**  The owner's three rule questions stay the owner's.

## What all three found that the packet missed

1. **`wiringcliff` -- ACT FIRST.**  `ip30_abort_probe.py`'s wiring exemption in `tools/pipeline/check_probe_wiring.py`
   is dated `2026-10-15` (HEAD :3097, working tree :3112); the check is `elif d < today:` and precommit section R runs it
   without `--today` -- so from 2026-10-16 section R refuses EVERY commit, in both sessions (Fable; the records and
   audits pre-screens found it independently).  Next expiries: 10-22 (two probes), 10-23, 10-26, 10-27.  Precedent:
   owner ruling 2026-09-24 ("re-date all ten individually").
2. **`panel.sh` scores a content-filter-REFUSED codex as "answered"** (`SEATS.txt` in `close_20261013/
   panel_20261013_003110/` and in both 10-13 pass-2 panels): `check()` greps the whole file for a verdict token and the
   tally counts any non-thin file.  v3 fixes `seat_verdicts.py` only.  FILE a held `panel.sh` sibling (never-commit
   hold); until it lands, `SEATS.txt` is not a refusal authority (Astra, Grok; records pre-screen S11).
3. **The codex launcher's model identity is reported, not enforced** (Astra) -- rider on F1.

## Owed actions (none done by this adjudication)

- Records commit: F1 landing (+ controls), F2 renderer + domain check (+ controls), filings `seatverdictrefusal`,
  `wdczerolendatain`, `agyselfupdate`, the `panel.sh` sibling, F5/F8 corrections, E53/E54.  It cannot pass precommit until
  `wiringcliff` is resolved.
