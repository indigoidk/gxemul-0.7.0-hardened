#557 -- the precheck failed three hard sections on the rows whose commits fields it fills; the repairs: right?

Open with the token `ASTRA557E_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`; committed files with `git -C ... show HEAD:<path>`, history with `git -C ... log`.  Everything else
is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.  Please do not simply ratify:
the witness strings below were written by me from commit messages, and a guessed witness is worse than an absent one.

**What happened after your `aconf_557d` (CLOSES).**  The stage was run for real and the pre-commit hook was run on it
(`draft\precheck_19h10_FAIL.out`): THREE hard sections failed, all on rows this unit had just given a commits field --
K (a row closed with commits names its witness): 3 rows with no witness field, 2 with `harness: ` (a space, which
`check_witness.py`'s `SHAPE` regex `harness:\S` rejects); I (a closed row that changed code owes a regress review or a
queued hold): 8 rows never reviewed or held; L (the ledger names the work that shipped): `hrecordowed`, filed by `#556`
(`1329d894`) with an empty field.  The eighteen rows had escaped K and I for as long as their fields were empty.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf557d.diff` (7 hunks; the ledger draft now prints the witness, the
hold_question and the last entry of every changed row).  Anything there beyond the repairs below is a finding.

**The repairs** (generator: `draft\prep557.py.txt`, `edit_ledger`; each population is DERIVED from the staged ledger by
the gate's own rule and asserted equal to the names the hook printed, so the script refuses on drift):
1. K -- `fbwitness`, `ledgerwitness`, `xfamscope` get `harness:<what proved it>`, each written from the closing commit's
   own message (`6014b7e7`, `aa10c9f1`, `636c0239` + `a4c86f11`).  **Does each string claim ONLY what that commit's
   message records?**  Open the messages.  A number, a control or a result in a witness that the message does not
   carry is a finding.  Is `harness:` the right term for each (the ladder admits it only when the round's subject is the
   test apparatus)?
2. K -- `lcalenzerodrop` and `nineseatreminder`: `harness: ` -> `harness:`, text otherwise unchanged (the ledger draft
   shows both).  Right, and is the note's reason (the SHAPE regex) what `tools\pipeline\check_witness.py` says?
3. I -- the eight (`fbwitness`, `lcalenzerodrop`, `ledgerwitness`, `m88kexcrrtrapmode`, `nineseatreminder`,
   `scorehyphenfp`, `smhang`, `xfamscope`) each gain a regress-phase entry `[HELD AWAITING SEAT: fable5]` (the live
   marker the tools read) and a `hold_question` (prepended where the row already had one).  Is this the established
   form -- compare `fbsmlane`'s regress hold of 2026-09-19 in the committed ledger -- and does the hold text say anything
   false about any of the eight?  Note `alphatbinegsel` is NOT among them although it is a filled row with no regress
   entry: it is named in the generated block of `tools\pipeline\fable_queue.md`, so section I counts it as queued.  Is
   that reading of `check_fable_queue.py` right?
4. L -- `hrecordowed.commits = 1329d894` with a note saying `#556` placed 65 of 92 corrections and filed the row for 27.
   Do those numbers match `#556`'s CHANGELOG block (`git show HEAD:CHANGELOG.md`, the `#556` block at the top)?
5. The section, changelog, message and the class row's note each gained a paragraph on this ("filling eighteen fields
   produced thirteen obligations": 3 + 2 + 8, and L).  Is the arithmetic right, and is "a row closed with no commit is
   invisible to every check that keys on the commits field" true of K, I and L as the checkers are written?
6. The chain paragraph now reads: `aconf_557d` clean, then the precheck's three fails, then `aconf_557e` = this check
   (`<OWED: aconf_557e>` is filled at staging).  Accurate?

All four checkers were re-run against the repaired staged ledger before this brief was written: `WITNESS_PASS`,
`FABLE_QUEUE_PASS`, `ATTRIBUTION_PASS 0 hard`, `STAGE_PANELS_PASS` -- the full hook runs again at the next precheck.

`<n> | RIGHT / WRONG: <why, path:line or commit>`.  End with `DENOMINATOR: <h> of 7 hunks read; <c> of 4 commit messages read`.
