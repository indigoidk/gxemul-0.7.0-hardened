Read-only code review task (bash and Python test tooling of the GXemul emulator project).  Do NOT edit, build or
run anything that writes; reading and in-memory evaluation are fine.

Tree: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c2_frozen\ -- read ONLY these frozen copies:
  gate_hygiene.sh (md5 6a9cb517; a test gate; the part under review is the "readiness" census rows),
  census_tokens.py (md5 662ce35a; NEW -- a Python-tokenizer helper the gate now calls),
  derive_hygiene_pins.sh (md5 cbb8488d; a tool that re-derives the gate's pinned numbers and rewrites them),
  gate_hygiene.f2in.sh (md5 4cfc4a65) and derive_hygiene_pins.f2in.sh (md5 3feb2a43) -- the versions before this change.
The probe files the census reads are in C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\*.py (read them as needed).
Ignore every other copy of GXemul under C:\DocumentNoSnc\cc\GXEMUL (./src/ and _archive/ are upstream 2021).

Background, one paragraph: the gate counts, over the regression probes that drive the emulator through a
pseudo-terminal, which spellings of a prompt-readiness test they use, and which probes have none (those are pinned by
name in GRANDFATHERED_PROMPTLESS).  The change under review moved the "has a readiness test" classification and the
whole-buffer site count (`<name ending in buf>.rstrip().endswith("GXemul>")`) from line greps to Python tokens
(census_tokens.py), built the probe list by path relative to regress/, and changed the deriver: an approval to move
certain pins is now `--ruling "YYYY-MM-DD: text"` and is written into the gate as a comment line; a duplicate name is
refused; EXPECT_BARE is written when it falls.  Measured today: the gate passes on the real tree (bare 0, unknown 0,
73 probes, 43 without a readiness test = the 43 listed names, whole-buffer 3 = arm_bdt_probe.py:1 arm_flags_probe.py:2,
the three #392 counts 24 each).

TASK 1 -- census_tokens.py: for each behaviour its docstring claims (comments, strings and docstrings are not code;
spacing between tokens ignored; either quote; counted per occurrence; an unreadable or untokenizable file is listed as
having no readiness test), say whether the code does it, and name any input where the code and the docstring disagree.

TASK 2 -- derive_hygiene_pins.sh: list every refusal the code can print (the exact condition for each) and every
refusal its header comment promises.  Name any refusal in one list and not the other, and any way `--write` can move a
pin that the header says needs a ruling without one.

TASK 3 -- find the smallest edit to one probe file (a real regress/*.py that forks a pseudo-terminal) that changes a
prompt-readiness test's behaviour while every readiness row in gate_hygiene.sh keeps its value.  Exclude these known
cases, which are already filed: another variable name than one ending in `buf`; `strip()` for `rstrip()`; a slice or
`re.search` comparison; extra parentheses around the receiver or the call; `rstrip("\r\n")`; a helper function in a
module outside the probe population; `os.forkpty`; `buf.endswith (">")` with a space; the #37 form as a slice.

TASK 4 -- quote any comment sentence in the three current files that the code contradicts, with the file line.  Check
especially every sentence that calls the census "closed-world" or says a count "cannot be evaded".

Answer format: start with one line `VERDICT: <one sentence>`, then TASKS 1-4.  No "no findings" without the
denominator you checked.  End with what you read.
