FILING TABLE CHECK -- part 11 (closing): three rows the table had missed, and agy's own verdicts on the disputed rows

Open with the token `ASTRAFILE_11_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 14 overlay lines wrong; <r> records sentences wrong; <m> further rows of the same shape missing`
-- and, if all three numbers are 0, the single word `CLOSES` on the next line.

**Context.**  Your part-10 answer closed the chain on what it was shown
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_10\codex_afile_10.txt`).  Two
things were found afterwards, by work given to the other two seats, and both change what is filed.  Everything below
is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\` unless a full path is given;
the blocks that made the changes are `fix_agy2.py.txt` and `fix_file3ids.py.txt`.

**Please do not simply ratify.**  Read committed source with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`; read the artifacts from disk.  The tree under
review is `GXEMUL-SEC`; ignore any other `src/` under the project root.  Write nothing, build nothing, run nothing
that changes a file.

**A. Three rows were MISSING from the table** (`FILING_OVERLAY.tsv` lines 122-124: `ramspaninval`, `tcpdebugopts`,
`jazzlbmask`).  The retro rulings wrote `CONFIRMED-FILED <id>` for findings `memoryrw:F3`, `netip:F1` and `devjazz:F4`
(`...\astraretro_20260926\DISPOSITIONS.md:824`, `:870`, `:881`; the rulings are
`...\astraretro_20260926\adjudication\grok_20261002\grok_rule3g.txt:13-14` and `grok_rule3f.txt:37-38`, `:70-71`).
Each ruling says the defect is in the queue's PROSE with no short id and PROPOSES the id; your own confirmation of
batch 3g says so in terms (`...\adjudication\codex_astraconfirm_3g.txt:8`: "`ramspaninval` does not exist as an ID").
The table derived "nothing to file" from the word FILED, your parts 01-04 checked the table against the same word, and
so three ids that later dispositions cite as filed existed nowhere.  A mechanical check found them
(`chk_filed_exist.py.txt`: every id a disposition calls filed must be a ledger row at HEAD, a backticked id in the
queue file at HEAD, or a row this unit files).  The grok seat then read the three rows first-hand
(`briefs\grok_file3ids.md` -> `grok\grok_file3ids.txt`): one true as drafted, one needing a condition, one whose first
title was not true; the titles in lines 122-124 are the corrected ones, and the main loop read
`src/cpus/memory_rw.c:186`, `:757-775`, `src/devices/dev_jazz.c:138-147`, `:677-684` and
`src/include/thirdparty/pica.h:117` at `7440e129` before writing them.
One line per failure: `<id> | overlay says <X> | should be <Y> | the line (file:line) | confidence`.
1. For each of the three: is the TITLE true of the source at `7440e129`, no wider and no narrower than grok's reading?
   Is the GRADE right under the campaign's rule (HIGH: guest-controlled input ends the process, leaves a buffer's
   bounds or stops progress; MED: wrong guest-visible behaviour)?  `tcpdebugopts` is HIGH on a stated condition (NET
   debug verbosity on) -- is the condition the right one and is it in the title?
2. Is the KIND right -- "an id for an entry the queue already carries in prose" (`OUTSTANDING_BUGS.md:2727-2732` at
   `db8b1a33`), rather than a NEW row?
3. THE QUESTION THAT MATTERS MOST: is any OTHER disposition of this shape still missing?  `chk_filed_exist.py.txt` now
   reports 0 of 268 mentions.  I believe -- check it -- that its blind spots are (a) a `FILED-BY-PROSE` disposition
   that proposes NO id, and (b) an id spelt so that its pattern does not match.  Read the two dispositions files for
   either, and for any other way a finding ruled "filed" could be recorded nowhere.  Name each one you find:
   `<finding key> | <dispositions file:line> | why it is filed nowhere`.

**B. Eleven overlay lines gained agy's own verdicts** (lines 99-108 and 121).  After your part 10, agy -- the author
of the fact table -- was asked whether the ten per-row clauses state what its lines say
(`briefs\agy_highfacts2.md` -> `agy\agy_highfacts2.txt`): it flagged four as one-sided (`sgilwreadzero`,
`diagdivunaryop`, `diagdivchained`, `diagdivtruncarg`: each clause leaves out its line's Q1 verdict).  Nothing was
removed: each of the ten notes keeps the text you passed in part 10 and ends with one more sentence,
`agy's own verdicts on that line (agy/agy_highfacts.txt:<n>), verbatim: "Q1: ... | Q2: ... | Q3: ..." -- Q1 the check
on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.`, cut from agy's line by
`agy_verdicts()` in `mk_overlay.py.txt`.  Line 121 (`gdromcondhow`) gained the verdicts agy gave for rows R1b/R2b in
`agy\agy_highfacts2.txt:16`.  One line per failure, as in A:
1. For each of the eleven: are the three quoted verdicts exactly agy's, from the right line of the right file?
2. Is the gloss of Q1, Q2 and Q3 a fair summary of the questions agy was asked (`briefs\agy_highfacts.md:22-31`)?
3. Does the added sentence change the meaning of the note you passed -- in particular your rules (ii) and (iii)?

**C. The records text**, regenerated: `draft\changelog554.draft.md` (118 lines), `draft\section554.draft.md` (1031
lines), `draft\msg554.draft.txt` (37 lines), `draft\REGRADES.txt`.  `DRY-ASTRA11` stands where this answer's verdict
will go.  One line per false or unsupported sentence: `<file>:<line> | says <X> | should say <Y> | why`.
1. The new text: `changelog554.draft.md:66-70` (part 10 closing its chain; agy's four flags) and `:72-78` (the three
   missing rows -- is "the table read that as nothing to file" and "found exactly these three" a fair account?);
   `:101-107` (the seats, by name); `msg554.draft.txt:18-26`; `draft\REGRADES.txt:15` (the `ptywaitstatus` re-grade's
   note now quotes agy's verdicts for the two sites, `agy\agy_highfacts2.txt:17-18`).
2. The three new rows as printed: `section554.draft.md:178` (`tcpdebugopts`), `:463` (`ramspaninval`), `:466`
   (`jazzlbmask`).
3. The totals, which changed -- each is derived: 510 open rows = 456 NEW + 26 test coverage + 28 ids; 54 HIGH = 37
   retro + 17 harness; 12 disputed HIGH rows and one disputed re-grade; 224 ledger rows added = 221 individual + 2
   class rows + `nineseatreminder` closed; 13 re-grades, 11 headings; 123 overlay lines.

End with `DENOMINATOR: checked <a> of 14 overlay lines; read <b> of the two dispositions files for part A.3; read <c>
of the three records drafts in full`.
