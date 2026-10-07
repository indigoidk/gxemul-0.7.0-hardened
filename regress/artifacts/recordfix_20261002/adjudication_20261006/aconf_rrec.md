Record corrections: 36 place verdicts by three read-only helpers -- which are wrong?

Open with the token `ASTRARREC_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- all 36 verdicts right`
`VERDICT: <n> of 36 verdicts wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; the records were reviewed
at commit `1329d894`, HEAD is `96a44fe3`.  Read files with `git -C <tree> show <rev>:<path>`.  Ignore any other src/.

The three tables: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\adjudicate_rrec\ADJ_01_03.md`, `ADJ_04_06.md`,
`ADJ_07_09.md`.  Each row is one sentence of the project's records: whether its CURRENT text is false, whether the
ruled REPLACEMENT fits (and, where not, a corrected replacement), and whether HEAD already fixed it.  The packets
they came from: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\jobs_20261006\gx_rrecNN_r1\gemini_web.packet.md`.

For EVERY row: `<table>/<place> | RIGHT / WRONG: <why, path:line>` -- check the CURRENT verdict and the REPLACEMENT
verdict (and any corrected replacement) against the files.  Be hardest on the corrected replacements: they are new
text that no one else has checked.
End with `DENOMINATOR: <n> of 36 rows checked against files`.
