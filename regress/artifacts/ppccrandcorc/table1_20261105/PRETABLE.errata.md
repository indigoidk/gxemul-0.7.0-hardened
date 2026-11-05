# PRETABLE.errata.md -- corrections to ../table1_20261105/PRETABLE.out (#575 ppccrandcorc), dated 2026-11-05 (round 2)

PRETABLE.out is a historical record and is NOT rewritten; its timestamps stand.  The corrections below come from pass 2
(p2_20261105/codex_codex_r575_p2.txt F4, F5, F7 and section 3; p2_20261105/ollama_glm.txt section 3) and were checked against
table1/SCORES.txt, the file mtimes and the simulator r2_20261105/v575b.py (`errata62').

## F4 -- the absent-binary null medium

PRETABLE.out lines 5-6 say: "Null media (/bin/true, an absent binary, /bin/false): CONTROL=FAIL."

Correction: /bin/true (5/62) and /bin/false (1/62) score CONTROL=FAIL.  An absent binary does NOT reach a CONTROL record: the
probe's first `subprocess.run` raises FileNotFoundError before any row (table1/probe_null_absent.out, last line), so there is no
RESULT, no CONTROL and no sentinel.  SCORES.txt line 4 records it correctly: `null_absent [62 rows] none CONTROL=none DONE=0`.  The
gate's first check (the completion sentinel) is what reds it.

## F5 -- "its mtime precedes every file in table1/"

PRETABLE.out lines 1-2 say: "Written BEFORE table 1 runs (its mtime precedes every file in table1/)."

Correction: one file in table1/ is older.  table1/probe62_frozen.py was copied first (2026-11-05 01:36:56.192 local, 07:36:56.192Z);
PRETABLE.out was written 86 ms later (01:36:56.278 local, 07:36:56.278Z).  Every other file in table1/ (MD5.txt 01:37:08 onward,
SCORES.txt 01:38:59) is later than PRETABLE.out.  The claim that matters -- the predictions were written before any variant was
built or run -- holds.  table1/VERDICT.md line 6 already states this exception.

## F7 -- "rows reading the debugger ... are predicted green on every variant"

PRETABLE.out lines 3-4 say: "rows reading the debugger, the disassembler or mfcr are predicted green on every variant."

Correction: every semantic row reads CR through the debugger too (the probe seeds CR with `cr=' and reads it back with `reg'), and
PRETABLE's own HEAD prediction lists ten of them red.  The sentence meant the APPARATUS CONTROLS: `ctl session`, `ctl live`,
`ctl seed holds`, `ctl cr seed`, `ctl mfcr`, `neg apparatus`, and the `* session`, `* mfcr` and `* disasm` rows of each table session
(no variant of either table touches the debugger, the disassembler or mfcr).  The `* others` rows are COMPUTED, not assumed green:
t1/t2 red `64 others`, `32 others` and `edge others`.  r2_20261105/PRETABLE_2.out uses the corrected wording.

## The four R5 bt-substitution predictions the pass-1 ruling required (predicted, not built)

adj_p1_20261105/MYTHOS_local.md R5: "Clause 2 bt-substitutions (`bt & !bb`, `ba & !bt`, `bt | !bb`, `ba | !bt`) each red an
existing row by enumeration ...; list them in PRETABLE as predicted, not built."  PRETABLE.out omitted them.  Their exact red sets on
the 62 rows, computed by r2_20261105/v575b.py (`errata62'; the same simulator reproduces table 1's 17 legs exactly):

    r5a crandc `if (bt & !bb)`   3 red: 64_crandc_10, 64_crandc_hi, 32_crandc_10
    r5b crandc `if (ba & !bt)`   3 red: 64_crandc_10, 64_crandc_hi, 32_crandc_10
    r5c crorc  `if (bt | !bb)`   3 red: 64_crorc_01,  64_crorc_hi,  32_crorc_01
    r5d crorc  `if (ba | !bt)`   2 red: 64_crorc_00,  32_crorc_00

(Here `bt` is the BT field index, 0..31: `bt & !bb` is bt's low bit when b = 0 -- 0 for BT 10 and 20, red where the want is 1;
`!bt` is 1 only at BT = 0, which no crandc/crorc truth or hi row uses, so `ba & !bt` is 0 and `ba | !bt` is a.)  codex's pass-2
derivation (section 3) lists the same four sets.  The ruling's parenthetical "the owed rows stay green under all nine" is also
false: `64 crandc hi` / `64 crorc hi` are red under c and under d1-d4 (SCORES.txt lines 8-12), as table 1 measured and VERDICT.md
reports; see table1/VERDICT.errata.md.  Their red sets on the round-2 66 rows are in r2_20261105/PRETABLE_2.out ("PREDICTED ONLY").
