ASTRA CONFIRMATION of the grok seat's RULING on id-less queue entries -- slice 02a (57 dispositions)

Open with the token `ASTRACONF_IDLESS_02A_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 57 dispositions wrong (<m> more need a change of wording, id or severity)`

**Context.**  `OUTSTANDING_BUGS.md` names most queue rows by a short backticked id; some entries record an OPEN defect,
an owed measurement or an owed correction in prose only.  GPT-6 Astra scanned the file for those (slice 02a:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\idless_02\codex_idless_02.txt`), the agy seat verified each row (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\agypack_20261001\idlessverify_02\agy_idlessverify_02.txt`), and the grok seat -- a third model family -- then RULED every entry
first-hand from the committed files:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\grok\grok_ruleidless_02a.txt`
(its verdict: "33 NEW, 0 FILED, 6 CLOSE-RECORD, 6 KEEP-AS-IS, 10 UNSETTLED, of 55 claimed entries (+2 missed entries ruled)").  The project owner ruled on 2026-10-02 that the working seats are GPT-6 Astra, agy and grok:
the grok seat's ruling is the proposed disposition and YOU confirm or overturn it before any id is assigned or any
entry is closed.  Nothing is fixed here; this decides what the queue will say.

**Please do not simply ratify -- and mind which half is yours.**  Your family wrote the scan, so the ruling agreeing
with the scan is not evidence of anything: be hardest exactly where grok AGREES with the scan, and say so where grok
changed the scan and was wrong to.  Check each disposition against the committed tree
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`, the revision whose line numbers the ruling uses; never `git status` or `git diff`;
ignore every other `src/` under the project root).  The errors that matter:
- a `NEW` whose defect ALREADY HAS AN ID -- in `OUTSTANDING_BUGS.md` at `db8b1a33` (search by the file's basename and the
  entry's own words, not only by the proposed id), in the retro campaign's rulings `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md`, in the harness rulings
  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md`, or in the table of 495 rows about to be filed from those two, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING.tsv` (read these three from disk; they
  are untracked artifacts).  That is `FILED <id>`, and it is the commonest error: several of these prose entries are
  the same defects the retro review found from the source side;
- two rows of the ruling that are ONE defect under two ids (see the ruling's own section (b));
- a `CLOSE-RECORD` where the source at `db8b1a33` does NOT show the fix, or whose replacement sentence is itself false of
  the code -- a wrong closure hides an open defect, so this is the costly direction;
- a `KEEP-AS-IS` on text that records owed work;
- an `UNSETTLED` that a reading of the committed files settles; a severity that does not follow the rule (HIGH --
  guest-controlled input ends the emulator process, makes a memory access leave a buffer's bounds, or stops it making
  progress; MED -- guest-visible behaviour differs from the hardware documentation; LOW -- diagnostics, latent code,
  records, test coverage);
- a proposed id that already exists anywhere: the three files above, or the ledger (`git show HEAD:tools/pipeline/ledger.json`, the `"id"` fields).

**For each disposition you overturn or amend, one block:**
`<line range> | grok said <X> | should be <Y> | the evidence (path:line at db8b1a33, or the artifact line) | confidence`
Then list the line ranges you checked and found right, and end with
`DENOMINATOR: checked <c> of 57 dispositions against the source`.

Read-only: write nothing, build nothing, run nothing that changes a file.
