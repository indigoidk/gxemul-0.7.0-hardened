# #519 sgirandomcolour -- RECORDS AUDIT of the draft CHANGELOG round block (read-only)

Nonce: CODEX_519_RECORDS_20260910.  Open with `VERDICT: GO | NO-GO (n items)` and echo the nonce.

**Please do not simply ratify.**  Your audit of the #518 draft found 27 wrong sentences (numbers with no log,
a check that could not fail, roster and scope errors).  This is the same kind of read on the #519 draft.
`*** OWED ***` markers are EXPECTED -- the kill tables are still running -- and are not findings; a number or
claim stated as fact that no artifact supports IS a finding.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`; ignore any other `src/` under the project root.

## The draft
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\codex_in\changelog_519.md` (a copy of the session draft; read it whole).

## The artifacts it must agree with (all under `regress/artifacts/sgirandomcolour/`)
* `witness_20260910/HEAD_run1.out`, `HEAD_run2.out`, `fix_20260910/FIX519_run1.out` -- the witness runs.
* `fix_20260910/FIX519_detector_run3.out` (16-row instrument on the fix), `HEAD_detector_run2.out` (16-row on HEAD),
  `HEAD_detector_run3.out` (19-row on HEAD, if present yet).
* `killtable_20260910/PRETABLE.out` (sections 1-6.i), `killtable_20260910/*.raw` (the Opus table 1, in progress),
  `killtable_20260910/t2/SCORES2.txt` and `t2/*.raw` (tables 2/2b/2c, in progress -- read whatever is there).
* `pass2_20260910/` -- the six seat answers (`codex.txt` streams its reasoning; the answer is at the end),
  `SEATS.txt`, `kimi.txt` (the CLI's 403).
* `panel_design_20260908/` -- the pass-1 design panel; `codex_pretable6_20260910.txt` -- your section-6 audit.
* `agy_witness_20260910.md` / `.out` -- the fallback measuring seat's transcript.
* The source: `src/devices/dev_sgi_re.c` (grep `SGIRE_W_BADCOLOR`, `int ok = 1`, `if (ok)`), HEAD `1ce8296`.
* The instrument: `regress/sgi_re_colourdefault_probe.py` (19 rows; count `row(` sites -- one is a helper).

## Questions (verdict line first; one numbered item per finding; cite by grep anchor and file)
1. Every NUMBER in the draft that is not inside an OWED marker: which artifact produces it, and does the artifact
   say that?  (2/5, 5/5, 16/16, 6/16, 3 hunks / 48 / 13 / 61 / 58, twelve nibbles, four functions, 04:00:19 /
   04:06 / 03:51, "nine pre-existing sessions", 19 rows.)  Name each that has no artifact or disagrees.
2. Every QUOTED seat verdict: is it verbatim from the seat file named?  Name any paraphrase presented as a quote.
3. The roster sentence ("SIX of SEVEN scriptable transports answered ... agy DELIBERATELY NOT FIRED ... the Opus
   seat holding table 1"): check it against `pass2_20260910/SEATS.txt` and the files present.
4. The design paragraph: does the pass-1 panel dir support "five of five seats chose member 3 and four of five
   chose (b)" and "member 7 was named and refused"?  Read the seat files, not the ledger note.
5. Claims about the FIX's shape and about what `random()` still appears in: check against the source.
6. Anything the draft says the instrument DOES that the instrument does not do, or vice versa (the contract
   paragraph vs the probe header; the "allbits" description vs the probe block).
7. Anything else that is a wrong record: an ordering claim, a provenance claim, a seat attributed the wrong finding.

Do not propose product-code changes and do not run anything.
