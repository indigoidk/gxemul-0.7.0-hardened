ID-LESS TABLE CHECK -- part 05: are the repairs of your part 04 right, and is what was added since then right?

Open with the token `ASTRAIFILE_05_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing added since part 04 is wrong`
`VERDICT: <n> things wrong (A: <a>, B: <b>, C: <c>, D: <d>)`

This is a RECORDS check: whether statements in a queue file, a ledger and a changelog match the committed code and the
documents they cite.  No new defect hunting is asked for.  Write nothing, build nothing, run no emulator.

Please do not simply ratify.  A repair is new material and can be wrong in its own way; so can a ruling that
conceded to you.  Be harder on the two things that went your way (the F12 resolution you accepted, and grok's
concessions of your part D) than on the rest: is the concession applied correctly, and is it actually right?

**Where things are.**  The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; ignore any other `src/` under
the project root.  Read committed files with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is
`1202d342`); the working tree carries another session's uncommitted edits in five `src/` files.  The queue as the scan
saw it: `git ... show db8b1a33:OUTSTANDING_BUGS.md`.  The manuals are extracted text in
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\` (outside the git tree).  Everything else below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_ifile04.diff` -- unified diffs of the four tables and the five draft texts,
from what part 04 read (kept in `before_ifile04_repairs\`) to what stands now.  29 hunks.  If you find a change that is
none of the things listed below, that is a finding (part D).

**Part A -- your eleven findings of part 04, and what was done with each.**
* C8, C11, C12 (RESULT fields misapplied): repaired in `mk_itable2.py.txt` (search `ifile_04`).  `qhcmdabort`'s queue
  field is `4839-4848 and 4953-4954`; `armthumbabortkill` is pointed at by 2614-2615 "in part: the Thumb half only";
  `loadfragile` by 5262-5266, and 4289-4294 is no longer pointed at it.
* The premise of A2(5): returned to grok, which conceded (`grok\grok_grok_irule_d.txt`, item 6).  3042-3063 is pointed
  at `sh4sqexpevt` only.
* B (a note between two logical rows of a wrapped table): the note for 12136-12140 is now inside the last cell of the
  `#265` row; `apply555.py.txt` treats a wrapped row as one row and refuses a note that stands alone in a table.
* D (four passages pointed only at closed rows that still record open work): ruled by grok -- part B.1 below.
* E1 ("41 passages done or closed"): reworded in the section, the changelog and the message as a count of sentences,
  5 of which name the id that carries what stays open.
* E2 ("no refusal"): the seats paragraph of the changelog now says what your first message said and that you
  withdrew it.  Is that account accurate?
For each: `<finding> | REPAIRED / NOT REPAIRED: <what is still wrong, path:line>`.  Report only the ones not repaired.

**Part B -- material you have not seen.**
1. **grok's ruling D** (`grok\grok_grok_irule_d.txt`; brief `briefs\grok_irule_d.md`): 5 conceded, 2 conceded in
   part.  It concedes your four D findings.  Three of those rows (`m8latch`, `gcsections`, `ns16550`) were closed on
   2026-08-27 by one sweep that executed the adjudicator's note `CLOSE (assess)` as a row closure; my reading, which
   grok conceded in part, is that the note signs off the assess STAGE (seven rows carry it while held or in work).
   The result: ONE new class row, `closeassessrows` (MED), with the EIGHT members grok found undone -- `m8latch`,
   `gcsections`, `ns16550`, `pcchalt`, `wdcstandby`, `rtcnarrow`, `scunbacked`, `m437multi` -- a note on each
   member's ledger row (state unchanged; `draft\ledger555.draft.txt`), the three passages pointed at it as well as at
   the closed row they name, and nothing re-opened.  Your fourth passage, 10412-10418, gets `gdromtailcov` (LOW).
   The sentence at 5607-5615 gains a clause saying `rtcnarrow` is closed and what of it is live (item 7).
   Check first-hand, against HEAD:
   (a) each of the eight members -- is the work the row names really not done, and carried by no other open row?
   (b) the three grok left out (`m8sarseq`: carried by open `m8sarrows`; `xfamscope`: edits made; `m437rtmp`: owes
   no code) -- is leaving each out right?
   (c) is one class row a "live carrying disposition" in your sense, and consistent with your "do not justify
   duplicate defect IDs"?  If you would rather each of the three be re-opened here, say why a records round may
   overturn the adjudicator's closure without the adjudicator.
   (d) the class row's text in `draft\section555.draft.md` (search `closeassessrows`) and the two rows "read by no
   seat" (`ledgerwitness`, `cmtattr`) -- is anything said there that the ledger does not support?
   One line each: `B1a <member> | CONFIRMED / WRONG: <why, path:line>` (only the wrong ones), then `B1b`, `B1c`, `B1d`.
2. **The manuals.**  Three UNSETTLED entries said a manual was unopened or absent.  grok read the local manuals
   (`..\idlessread_20261002\grok\grok_grok_iunsettled.txt`: 1 settled, 2 still unsettled).  5655-5661 (`lwarx` /
   `stwcx.`) is settled and gets a sentence in place with the manual lines; 2947-2948 (`FSCA`) and 5650-5654 (`lvx` /
   `stvx`) stay unsettled with what was read since.  Check: the quoted manual lines exist and say what is claimed
   (`ppc_pem_32and64_2005.txt:9321`, `:25024`, `:32823`, `:9338`, `:10683`; `ppc_vea_book2_v201.txt:1288-1290`;
   `ppc_oea_book3_v201.txt:3371-3372`); the committed `src/cpus/cpu_ppc_instr.c:2342-2362` does what the sentence
   says; `FSCA` is absent from both SH texts and `lvx` / `stvx` are defined in none of the five PowerPC texts.  Is the
   closing sentence for 5655-5661 a fair reading -- in particular "the alignment exception is permitted rather than
   owed"?  `B2 | CONFIRMED / WRONG: <why>`.
3. **A mechanical addition.**  Two sentences cite this same file by line (`OUTSTANDING_BUGS.md:4747-4748`, `:6695`);
   the notes inserted above those lines move them, so each citation now carries "(numbered as of `db8b1a33`)".
   `B3 | FINE / WRONG`.

**Part C -- the texts as they now stand** (`draft\changelog555.draft.md`, `draft\section555.draft.md`,
`draft\msg555.draft.txt`).  Any sentence that is false, and any number the tables do not give (`draft\MANIFEST.txt`
has the derived numbers: 130 rows -- 7 HIGH, 29 MED, 94 LOW --, 43 sentences, 104 passages, 8 carried only by
closed or dropped rows, 4 unsettled, 37 ledger rows added, 8 member notes).  The line
`<OWED: GPT-6 Astra's verdict on the repairs>` is where your verdict line goes.

**Part D -- anything else.**  A change in `draft\REPAIRS_since_ifile04.diff` that none of the above explains, or a
place where a repair broke something that part 04 had found right.

End with `DENOMINATOR: A <findings checked> of 11; B1 <members read> of 8, <left-out rows read> of 3; B2 <manual
lines read> of 7; C <texts read> of 3; D <hunks read> of 29`.
