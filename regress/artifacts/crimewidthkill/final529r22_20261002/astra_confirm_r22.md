#529 (crimewidthkill) -- CONFIRMATION OF THE TEXT DELTA r20 -> r22 AND OF THE RECORDS CORRECTIONS (GPT-6 Astra)

Open your answer with the token `ASTRACONFIRM_529R22_ALIVE` on its own line.  Second line, exactly one of:
`VERDICT: CONFIRM -- <one clause>` / `VERDICT: CONFIRM WITH CHANGES (<n>) -- <one clause>` / `VERDICT: REJECT -- <one clause>`.

**Please do not simply ratify.**  You confirmed this round's final ruling on 2026-09-30
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r18_20260926\codex_astraconfirm_final.txt`)
and overturned two of its dispositions: item 6's "no row seeds TIME's upper word" was FALSE, and the "r20 is the closing
revision" exemption contradicted the late-dissent rule, so an r21 with its own base leg was required.  Everything below
was written AFTER that confirmation and no seat has read it.  Nothing commits until you have.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git), HEAD `db8b1a33`.  This round's product file is in the
WORKING TREE, not at HEAD: `src\devices\dev_sgi_ip32.c`, md5 `8c1d1545` (HEAD's copy is the pre-fix file -- do not read
HEAD's for this).  Read-only: write nothing, build nothing, run nothing.  Cite `path:line` for every claim.  Ignore
every other `src/` under the project root.

**What changed, exactly** (each generator refuses unless the module AST minus its docstring is identical to its
predecessor's, so these are comment and docstring edits only):
* r20 -> r21, four find/replace pairs: `...\crimewidthkill\final529r21_20260930\mk_r21.py.txt` (the `PAIRS` list).
* r21 -> r22, one pair: `...\crimewidthkill\final529r22_20261002\mk_r22.py.txt`.  The precommit hook's score-claim
  check refused r21 because one docstring line quoted a historical `157/157` without the `157-row` marker.
* The committed bytes: `...\crimewidthkill\final529r22_20261002\crime_width_probe.r22.py` (md5 `a3188007`).
* The records as they will be committed, re-rendered after every edit:
  `...\crimewidthkill\final529r18_20260926\records_drafts.md` (the CHANGELOG block, the OUTSTANDING_BUGS section, the
  commit message, the ledger script).  It still carries ONE placeholder, `<OWED-ASTRA-R22>`: that is where your verdict
  on THIS brief goes -- ignore it.

**Q1 -- the four r21 fixes.**  For each pair in `mk_r21.py.txt`: does the new text say what your confirmation
required, and is every NEW sentence true of `dev_sgi_ip32.c` (working tree) and of the probe's own sessions?  Be
hardest on pair (1): it now says the gapped write sessions plant an `sw` of `t0=0x0a0b0c0d` at TIME, that the 4-byte arm
stores it in the UPPER word, that "the update may truncate it at once", and that "those rows do not establish a
persistent nonzero upper word at a refused-read observation".  Check each clause against the TIME arm and against the
gapped sessions in the probe.

**Q2 -- the r22 line.**  Is the `157/157` at the ACCEPTS note for entry 40 a score measured on the 157-row instrument
of closing pass 7 -- i.e. is "on the 157-row test" TRUE there, or did the qualifier get added to a number that is not
that instrument's?  (`opus_close7_20260915/` holds that pass.)

**Q3 -- your six records corrections of 2026-09-30.**  In `records_drafts.md`, is each applied, and applied correctly?
(a) entry 34's filing as `crimecontroldebt` item 8 in the OUTSTANDING_BUGS section AND in the ledger script's FILED
list, with its above-floor disposition and replay cost; (b) the `astra()` ledger event dated 2026-09-30 and describing
that confirmation, not the earlier one; (c) the state note's revision history through the committed revision; (d) the
MEASURED/derived qualifier scoped to the 31 guest-visible entries; (e) the known-wrong-records paragraph replaced by
correction provenance; (f) "two further failures in the review chain".  Name any that is missing or wrong, with the
line in `records_drafts.md`.

**Q4 -- new wrong records.**  The retargets moved "the committed text" from r20 to r21 to r22 and the commit date to
2026-10-02 (the chain closed on 2026-09-26; the review of its text ran on).  Is any sentence in `records_drafts.md` now
false -- a revision named as committed that is not r22, a base-leg figure attached to the wrong revision, a date that
claims a commit on a day it did not happen, a count that does not match its source?  The base legs: r19, r20, r21 and
r22 each have a `final529r<NN>_*/probe_base_r<NN>.raw` and an `MD5.txt` naming the probe bytes and the base binary.

**Q5 -- anything else that should stop this commit.**  Wrong records only: the chain is closed and no row is owed, so
a new row proposal is out of scope; a false sentence is in scope however small.

Answer Q1-Q5 in order.  For every change you require give the exact replacement text.  End with
`DENOMINATOR: <pairs checked> of 5 pairs; <corrections checked> of 6 corrections; <sentences of the r22 docstring and of records_drafts.md read>`.
