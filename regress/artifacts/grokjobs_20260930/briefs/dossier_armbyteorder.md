DOSSIER AUDIT -- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\dossier_armbyteorder\codex_dossier_armbyteorder.txt`

Open your answer with the token `GROKJOBS_DOSSIER_ARMBYTEORDER_ALIVE`.  Second line: `VERDICT: <N> false or unsupported sentences`.

**The tree.**  `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul machine emulator, C99.  Read
COMMITTED files at `db8b1a33` (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`, numbered with
`awk '{print NR": "$0}'` or `grep -n`); the WORKING TREE carries other people's uncommitted work -- do not read source
from disk.  Never read `C:\DocumentNoSnc\CC\GXEMUL\src\` (a pristine 2021 upstream copy).  Read nothing under
`regress/artifacts/` except the files this brief names.  Hardware manuals: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt`.
Write nothing; run nothing; return text.  Cite `path:line` at `db8b1a33` for every claim; say "not checked" rather
than guess.  Where a claim is arithmetic, enumerate the values.

**Context.**  The file above is a DESIGN DOSSIER written by a reviewing model for a correction round that has not
started: items 1-7 (the finding's truth, who can reach it, what the hardware does, siblings, the option set, what a
regression check would observe, records).  A round will build on it; a false sentence in it becomes a wrong fix.
Audit EVERY factual sentence against the committed source at `db8b1a33` (the product file it studies, its callers, the
machine files it names), the hardware manuals on disk it cites, and `OUTSTANDING_BUGS.md` at `db8b1a33` for every
"recorded"/"not recorded" claim.  For each false or unsupported sentence: the sentence (quoted), where it is, the
evidence against it (`path:line`), the corrected sentence.  Then: **(a)** the dossier's chosen disposition member --
is it right, and is its machinery really present on this CPU (an exception it proposes to deliver must have delivery
code; name the lines)?  **(b)** siblings the dossier missed in the same files; **(c)** DENOMINATOR: sentences checked
versus taken on trust.
