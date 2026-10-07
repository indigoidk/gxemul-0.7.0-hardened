Record corrections: 36 previously-unsettled place verdicts by two read-only helpers -- which are wrong?

Open with the token `ASTRAUNSET_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- all 36 verdicts right`
`VERDICT: <n> of 36 verdicts wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; records reviewed at
`1329d894`, HEAD `96a44fe3`; read with `git -C <tree> show <rev>:<path>` (the working tree has another session's edits).

Tables: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\adjudicate_rrec\ADJ_UNSET_A.md` (places 2-26, 19 rows) and
`ADJ_UNSET_B.md` (places 28-44, 17 rows).  Packets: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\jobs_20261006_i\gx_rrecNN_r1\gemini_web.packet.md`.
Ruled texts: `GXEMUL-SEC\regress\artifacts\recordfix_20261002\` (DISPOSITIONS.md, arrec_0*).

For EVERY row: `<table>/<place> | RIGHT / WRONG: <why, path:line>`.  Hardest on: the ten corrected replacements
(A: 11, 12, 26; B: 28, 31, 32, 33, 39, 42, 43) -- new text nobody else has checked; any count; and B's two
"same error elsewhere" claims (`regress/sh_iprbcd_probe.py:293`, `CHANGELOG.md:19574` vs `:19558`).
End with `DENOMINATOR: <n> of 36 rows checked against files`.
