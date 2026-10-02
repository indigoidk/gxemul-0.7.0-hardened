DRAFT CHECK -- retro batch 3f: 24 findings in 5 answers, and a codex DRAFT of their dispositions

Open your answer with the token `GROKJOBS_DRAFTCHECK_3F_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul machine emulator, C99.  Read
COMMITTED files at `db8b1a33` (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`, numbered with
`awk '{print NR": "$0}'` or `grep -n`); the WORKING TREE carries other people's uncommitted work -- do not read source
from disk.  Never read `C:\DocumentNoSnc\CC\GXEMUL\src\` (a pristine 2021 upstream copy).  Read nothing under
`regress/artifacts/` except the files this brief names.  Hardware manuals: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt`.
Write nothing; run nothing; return text.  Cite `path:line` at `db8b1a33` for every claim; say "not checked" rather
than guess.  Where a claim is arithmetic, enumerate the values.

**Context.**  A reviewing model (GPT-6 Astra) read this fork's accumulated changes to several source files at commit
`8ea26abb` (identical to `db8b1a33` under `src/`; the record files CHANGELOG.md and OUTSTANDING_BUGS.md moved by one
records-only commit, so read THOSE at `db8b1a33`) and reported findings; then a sibling of it drafted a disposition per
finding: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\draft_3f\codex_draft_3f.txt`.
The Fable seat adjudicates next, first-hand, and spends its budget where the draft is doubtful.  Your job is to tell it
where: CHECK EVERY DRAFT DISPOSITION against the source and the queue file.
The answers:
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_net\codex_bundle_net.txt`
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devjazz\codex_devjazz.txt`
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devne2000\codex_devne2000.txt`
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\net\codex_net.txt`
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\netip\codex_netip.txt`
Earlier batches' final rulings (ids already assigned; duplicates must point at them): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md`.

One line per finding:
`<job>:F<n> | draft: <its disposition, short> | RIGHT / WRONG: <should be> / WORDING: <change> | <the lines you read>`
Be hardest on: a FILED whose id does not exist at `db8b1a33` or names a different defect; a FILED-BY-PROSE whose quoted
lines do not describe this defect; a NEW whose defect the queue already records in prose (grep by function name,
diagnostic text and basename); a RECORD replacement text that is itself false; a severity the source does not support
(HIGH: input under the guest's control ends the process, makes a memory access leave a buffer's bounds, or stops
progress; MED: differs from the hardware documentation; LOW: records, diagnostics, coverage); a DUPLICATE that points
at the wrong row.  Then **(a)** the findings themselves that are wrong or overstated; **(b)** what both the reviewer
and the draft missed in those files; **(c)** DENOMINATOR.
VERDICT line (second line): `VERDICT: <r> of 24 draft dispositions right, <w> wrong, <m> wording`.
