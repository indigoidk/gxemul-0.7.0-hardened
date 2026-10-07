Harness record corrections: 27 key verdicts by a read-only helper -- which are wrong?

Open with the token `ASTRAHREC_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- all 27 verdicts right`
`VERDICT: <n> of 27 verdicts wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `96a44fe3`; read
with `git -C <tree> show HEAD:<path>` (the working tree has another session's uncommitted edits -- judge HEAD).

The table: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\adjudicate_rrec\ADJ_HREC.md` (27 keys: CURRENT verdict,
REPLACEMENT verdict, corrected replacement where the ruled one does not fit).  The ruled sources:
`GXEMUL-SEC\regress\artifacts\recordfix_20261002\HRECORD.tsv`, `HREC_TEXT_OVERLAY.tsv`, `HREC_VERIFIED.tsv`.

For EVERY key: `<key> | RIGHT / WRONG: <why, path:line>`.  Be hardest on (a) the eight new replacements (keys 1, 2, 3,
7, 11, 18, 19, 25) -- new text nobody else has checked; (b) key 11's claim that the false text is in
`tools/propagate_all_trees.sh:9-16`, not `tools/precommit_check.sh:1037`; (c) key 10's corrected citation
`OUTSTANDING_BUGS.md:6453-6472`; (d) key 17's unsettled number.
End with `DENOMINATOR: <n> of 27 keys checked against files`.
