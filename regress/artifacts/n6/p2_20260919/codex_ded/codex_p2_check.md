# Dedicated codex reading, n6/#539 PASS 2 -- verify the shipped diff against the tree, row by row

## READING SCOPE AND FORM
Read the pass-2 packet `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\p2\brief_n6_p2_BUILT.md` (it inlines the full
diff, the kill table, and the enclosing function) and then the WORKING-TREE files it names under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (HEAD a11eaac + uncommitted #539 edits): `src/devices/dev_footbridge.c`,
`regress/footbridge_sites_probe.py`, `regress/fbpending_drain_probe.py`, `regress/fbpending_witness.py`,
`regress/gate_arm.sh` (footbridge section only, around the `FBLOG=` line).  Scope your reading to
`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py` plus that one gate section; do not read `regress/artifacts/`,
`tools/pipeline/ledger.json`, CHANGELOG.md or OUTSTANDING_BUGS.md.  Read-only; run nothing.  Ordinary engineering
language (terminating calls, error handling).  VERDICT LINE FIRST; READ (file, anchor) / REASONED / NOT CHECKED;
counts with denominators.  Do not construct edits or programs; the candidate weakenings are SUPPLIED and your job
is to say which the shipped rows catch and which are equivalent to one another.

## QUESTIONS
1. Verify the inlined diff IS the working tree: for each of the five files, does the packet's diff match
   `git diff HEAD -- <file>` (state any hunk that differs, e.g. from a later edit)?  Confirm
   `est/src/devices/dev_footbridge.c` is byte-identical to SEC's.
2. Arm E register plan: walk the ENABLE word list (offset, word, expected disassembly, destination register)
   against the ARM encodings and the emulator's disassembler spellings you can find in
   `src/cpus/cpu_arm_instr.c` / `cpu_arm.c` (the `ldrh`/`ldrb`/`add` immediate printers).  For each of the 13
   words: encoding correct (READ the bitfields), spelling plausible, register not clobbered before the dump.
3. The seven `row()` calls and the two E-arm controls: do they read the registers the words write; is `E4`'s
   oracle `not E["fatals"]` + exit 0 (not a text match); is `ctrl_ok` correctly extended?
4. The two pending probes' new `close()` (drain to EOF, close, blocking reap) and `survived()`: does every
   session-return path carry `exit`/`signal`; is any row's predicate now vacuous or over-strict; does the CRLF
   drain file's diff contain only content hunks?
5. `gate_arm.sh`: the three new `check` regexes against the probe's printf formats (quote both); the excerpt grep
   `E[A-Z]?[0-9]`.
6. Candidate weakenings, against the FIXED code plus the shipped rows -- for each say CAUGHT BY (row), ESCAPES, or
   EQUIVALENT TO (another candidate): (m) `odata = d->irq_enable ^ 0x2000`; (n) `odata = ~d->irq_enable`;
   (o) the P/Q RAM words never planted; (p) the K word left at +0x188 in one probe only; (q) the K row ignoring
   `exit`; (r) `if (len == 4) odata = d->irq_enable;`.  Plus the packet's (j): is there a step-visible channel the
   contract's disclosure misses?
7. Citations: every `dev_footbridge.c` construct name the diff introduces -- unique in the file (grep count each)?
8. Standing licence: anything else you found while verifying.
End with: model, files read (with the working-tree md5 of each), nothing run.
