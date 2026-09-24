Read-only code review task (bash and Python test tooling of the GXemul emulator project).  Do NOT edit, build or
write anything; reading and in-memory evaluation are fine.

Tree: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c3_frozen\ -- read ONLY these frozen copies:
  census_tokens.py (md5 029fba36) and census_tokens.c2.py (662ce35a, the previous version),
  gate_hygiene.sh (4220b6ee) and gate_hygiene.c2.sh (6a9cb517),
  derive_hygiene_pins.sh (f9533e22) and derive_hygiene_pins.c2.sh (cbb8488d).
The probe files the census reads are C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\*.py (read as needed).
Ignore every other copy of GXemul under C:\DocumentNoSnc\cc\GXEMUL (./src/ and _archive/ are upstream 2021).

Background, one paragraph: census_tokens.py classifies test probes by Python tokens.  This change (1) keeps NEWLINE
tokens so a match cannot span two statements, (2) requires a "." before the method name so a function definition
under that name is not counted as a call, (3) catches ValueError on a path.  derive_hygiene_pins.sh now refuses a
`--ruling` containing any control character or fewer than 16 non-blank characters of reason, quotes its name lists,
refuses names holding whitespace or glob characters, and removes names from the grandfathered list by exact match.

TASK 1 -- for each of the three census_tokens.py changes, find any input where the NEW behaviour is wrong: a real
single-statement method call that is no longer counted (check line continuations, calls split inside brackets,
lambdas, comprehensions, decorators, `str.<method>(buf, ...)`), or a non-call that is still counted.  Say, for each,
whether the probe would then be listed without a readiness test (the gate's names row goes red) or silently kept.

TASK 2 -- derive_hygiene_pins.sh: can a ruling still put a line into gate_hygiene.sh that is not a comment, or
authorise a ruling-gated pin change with a blank or malformed reason?  Can `--grandfather` or `--release` be made to
accept a name the space-separated list cannot hold, or refuse a name it can hold?  Give the exact input.

TASK 3 -- quote any comment sentence in the three current files that the code contradicts, with the file line.

TASK 4 -- name one question about this change the tasks above did not ask.

Answer format: start with one line `VERDICT: <one sentence>`, then TASKS 1-4.  No "no findings" without the
denominator you checked.  End with what you read.
