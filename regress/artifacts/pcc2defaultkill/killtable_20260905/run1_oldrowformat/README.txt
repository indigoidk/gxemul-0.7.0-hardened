Run 1 of the #501 kill table (04:12-04:25, frozen default probe md5 c76e053a): six of six mutants killed, the summary
counts (PCC2D_RESULT) correct.  Its row PRINT format put the status before the note, so gate 14 -- which counts rows by
`^<name>  .*ok$` and ` ok$` -- counted ZERO of 23 rows while the probe said DONE (gate14_501_FAIL_rowformat.log).
Fixed in-round (L1, pre-ship construction): status last, as the width probe prints.  Run 2 at the top level of this
directory measured the same six mutants on the fixed-format instrument; PRETABLE_501.out (never edited) predicts both.
