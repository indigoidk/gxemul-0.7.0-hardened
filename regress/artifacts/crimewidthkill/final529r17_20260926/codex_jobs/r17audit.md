You are an independent reviewer for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file.

The test probe `regress\artifacts\crimewidthkill\final529r17_20260926\crime_width_probe.r17.py` (226 rows) is about to be
committed as `regress/crime_width_probe.py`.  Its module docstring is a CONTRACT: it says which edits of the device code
(`src\devices\dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)`) the rows catch, cites measurements under
`regress\artifacts\crimewidthkill\`, and discloses what it does not cover.

AUDIT THE DOCSTRING AGAINST THE EVIDENCE.  FIRST LINE: `VERDICT: <N> false or unsupported sentences`.  Then:
1. Every sentence that says MEASURED, names a score, a count, a table, a row or an artifact path: open the artifact
   (each table directory has `PRETABLE*.out`, `POSTTABLE*.out`, a `check*.out` and `logs\probe_<leg>.raw`) and say
   whether it supports the sentence.  List only the ones that do NOT, with the file and line that contradicts them.
2. Every row name the docstring cites: confirm it exists in the probe's `row(...)` calls (names are sometimes built
   with `%` formats -- expand them).
3. Every path cited: confirm it exists.
4. Any disclosure that is stated as unconditional but holds only under a condition you can name from the source.
5. The one question you would most want answered before this commits that the docstring does not raise.
Say what you read and what you inferred; line numbers everywhere.
