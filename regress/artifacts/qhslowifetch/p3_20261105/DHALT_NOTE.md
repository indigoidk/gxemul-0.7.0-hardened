# qhslowifetch pass 3 -- glm-5.3's finding (A), measured (2026-11-04 23:2x local)

(A): the failure test widened to `!cpu->memory_rw(...) || !cpu->running` (call first).  glm: green on all 62 rows because every
measured SUCCESSFUL fetch runs with running == 1; distinguishing state = a successful slow-path fetch with running == 0, which glm
said a "data-halt-then-successful-fetch session" would produce with the existing probe.
MEASURED (dhalt_witness.py, base build, -E pmppc unmodified, -T, read-ahead disabled by a far breakpoint; dhalt_witness.out and
dhalt_base_{ld,st}.txt): `lwz r3,0(r4)` and `stw r3,0(r4)` with r4 = 0x02040000 (past RAM) each print ONE halt report and leave pc
at 0x2000 -- the faulting instruction.  The `addi` at 0x2004 is never fetched: a -T data halt ends the run AT the load or store,
so these shapes do not produce the state (A) needs.  No other producer of running == 0 before a successful fetch was found
(bad: parks next_ic on nothing_call; a read-ahead halt breaks the read-ahead loop, and the next fetch is the failing one).
So (A) is EQUIVALENT on every measured shape -- the same disclosure class as glm's (B)-(F), not a rowable cell.  For the ruling.
