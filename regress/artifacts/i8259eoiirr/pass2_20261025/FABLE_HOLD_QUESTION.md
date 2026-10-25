# i8259eoiirr (#574) PASS 2 -- the Fable 5.1 seat is HELD (owner hold of 2026-10-21); its question

Fable 5.1 is DELIBERATELY NOT FIRED on this pass.  The question it would be asked, kept so the hold carries it:

On the diff in packet.md (the acknowledge helper; the one-shot poll; the GT IACK read; the hybrid specific EOI that
consumes only when the line is not in service; the lowest-ISR-bit non-specific EOI): is the hybrid the right contained
form for the machines whose vector read acknowledges nothing, is lowest-numbered the right "highest priority" without
rotation, can the two-slave-request sequence leave a request pending with the CPU line low now that the manual fold is
gone, and which of the 77 rows is vacuous by construction?
