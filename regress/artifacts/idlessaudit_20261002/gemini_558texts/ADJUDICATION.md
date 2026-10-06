# Gemini-web readings of #558's drafts -- adjudication (#559, 2026-10-06)

Adjudicator: the main loop (Claude Opus 5.5), against the committed text at `4c9c06d2`.  Owner, 2026-10-06: "if there
is anything that opus (5.5) can adjudicate ... proceed with that".  The readings were of the DRAFTS (queued before
#558 committed), so each finding was re-checked against what actually shipped.

| # | finding | readings | disposition | why |
|---|---|---|---|---|
| 1 | Astra count: CHANGELOG "two checks and a confirmation" vs OUTSTANDING_BUGS "the check of the disposition, the confirmation" | r2 | **HOLDS** | both undercount; Astra answered ten times (`aconf_agyflags`, `aconf_mbstops`, `aconf_558` .. `aconf_558h`).  Corrected in both places. |
| 2 | `aconf_558`/`aconf_558b` (and, at HEAD, through `aconf_558h`) have no ledger entry | r2 | **HOLDS** | `idlesslow`'s codex entries at `4c9c06d2` cite only `aconf_agyflags` and `aconf_mbstops`.  One codex entry added naming all eight. |
| 3 | passage 2616's PPC carrier `qhppciphack` named in the ledger, omitted from SECTION / CHANGELOG / MSG | r1 (noted, "not a contradiction"), r2 (BROKEN) | **HOLDS as an omission** | the texts are not false, but the OUTSTANDING_BUGS account of the passage is incomplete where the ledger is not.  One clause added there; the CHANGELOG and message summaries are left as summaries. |
| 4 | "LEDGER:17 cuts off mid-sentence; the JSON is broken" | r1 (its only BROKEN), r2 | **DISMISSED** | the PACKET truncated that ledger note; the committed `ledger.json` parses and passed precommit.  A defect of the packet generator, recorded. |

Checked and found consistent by both readings (no action): the brief/answer counts (6 / 5 / 1 walled), the 104 = 35+35+34
passages, the 22 = 18+4 entries, the 16 = 5+11 flags and their per-brief split, the nine assignments / ten messages, and
the three new rows' sites and ids.  The "10 entries / 43 files" figures they checked were the drafts'; #558 shipped 11
entries and 73 files, and its own text says so.

Weight: both readings were Gemini 3.8 Flash, packet-fed (they cannot read the repository); every HOLD above was
settled by reading the committed files, not by the readings' agreement.
