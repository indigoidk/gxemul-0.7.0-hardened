You are the second ADJUDICATOR (with the flagship seat) for a records-only change in a C hardware emulator project (the
GXemul hardened fork; the tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`, ignore any other `src/`).  Read-only:
change no file.

Three reviewer answers arrived AFTER three changes had been committed (#550 04500deb, #551 f5e155ac, #549 8ea26abb).
The main loop wrote a packet of eleven proposed dispositions; the flagship seat has ruled on it.  Nothing is committed
until you confirm.  Read, in this order:
1. `regress\artifacts\latecodex_20260926\latecodex_packet.md` (the eleven dispositions, L1-L11, and its addendum);
2. `regress\artifacts\latecodex_20260926\fable5_latecodex.md` (the flagship's ruling, with EXACT replacement texts for
   `regress/diff_wdc_identify.c`, `tools/pipeline/check_probe_wiring.py` and `OUTSTANDING_BUGS.md`, and draft record
   lines for the three CHANGELOG blocks);
3. the three late answers it rules on (paths in the packet) and the committed files, via
   `git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show HEAD:<path>`.

FIRST LINE: `VERDICT: <CONFIRM | CONFIRM WITH CHANGES | DO NOT CONFIRM>`.  Then: (1) which of the flagship's rulings
you would overturn, and why; (2) every replacement text or record line in the ruling that is false against the
committed files or the artifacts (file:line); (3) whether any late finding names a measurement that would make it a
floor breach (L2) rather than wording or a filing; (4) whether a separate records commit before the next code change
is right.  Say what is a reading and what is a measurement.
