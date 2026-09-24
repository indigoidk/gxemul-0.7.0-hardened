Read-only code review task (bash + Python, GXemul hardened fork).  Do NOT edit, build or run any gate; read-only Python
or grep over the files is fine.

Tree: C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\ -- read regress/gate_hygiene.sh, tools/derive_hygiene_pins.sh and the
regress/*.py files at the top level of regress/ (NOT regress/artifacts/).  Ignore every other copy of GXemul under
C:\DocumentNoSnc\cc\GXEMUL (./src/ and _archive/ are 2021 upstream).

Background: gate_hygiene.sh keeps a static census of the pty-driving Python probes in regress/.  Today's change made
its "promptless" classifier read CODE instead of raw text: `code_has() { grep -v '^[[:space:]]*#' "$1" | grep -q
"$2"; }`, and a probe is "promptless" when `code_has "$f" 'endswith('` is false.  It was changed because a COMMENT line
containing `endswith(` had hidden a probe with no prompt check.  The whole-buffer rows now use
`WHOLE_RE="buf.rstrip().endswith([\"']GXemul>[\"'])"` and pin each file with its count.

TASK 1 -- the same hiding by another road.  The filter strips only FULL-LINE `#` comments.  Using Python's own
tokenizer or ast (not grep), find every top-level regress/*.py file that contains `pty.fork` and whose ONLY
occurrences of the text `endswith(` are inside a docstring, a string literal, or a TRAILING comment (after code on the
same line).  For each, say whether it has a real prompt-readiness wait (and what it is), i.e. whether the census
counts it as prompt-detecting for the wrong reason.  Report N such files of M pty-driving files checked.

TASK 2 -- for each of these SUPPLIED one-line changes, work out BY READING which gate_hygiene.sh readiness row (if any)
goes red, naming the row and the got/want it would print; if none does, say whether the change re-opens the
whole-buffer race (#392's "whole buffer ends with the prompt" readiness test) or is harmless:
  V1  a new code line in an allowlisted file:  `if self.buf.rstrip( ).endswith("GXemul>"): return True`
  V2  a new code line in luna_absentcpu_probe.py:  `if self.buf.rstrip().endswith("GXemul>" ): return True`
  V3  a new code line in luna_absentcpu_probe.py:  `if (self.buf.rstrip()).endswith("GXemul>"): return True`
  V4  a new module-level docstring line in a grandfathered promptless probe that mentions `x.endswith("GXemul>")`
  V5  the same text as V4 but as a trailing comment after a code line
  V6  `export WHOLE_FULL_RULING=1` left in the shell that runs `tools/derive_hygiene_pins.sh --write`
  V7  a grandfathered name written twice in GRANDFATHERED_PROMPTLESS
  V8  a new pty probe placed at regress/sub/new_probe.py (a subdirectory; no such directory exists today)

TASK 3 -- name at least one question about this change that the task list above did not ask.

Answer format: first line `VERDICT: <one sentence>`, then TASK 1 with its denominator, then TASK 2 as an eight-row
table (variant, row that goes red or "none", got/want or "re-opens"/"harmless"), then TASK 3.  No "no findings"
without the denominator you checked.  End with what you read and what you ran.
