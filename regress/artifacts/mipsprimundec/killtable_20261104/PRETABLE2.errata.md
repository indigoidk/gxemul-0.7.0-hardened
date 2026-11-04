# PRETABLE2.out -- errata (2026-11-04, the landing)

PRETABLE2.out stays as written: its mtime is the order proof.  One line of it rests on a premise measured false afterwards:

* `D31_r5900_false ... red: NONE -- no R5900 session (disclosed)`.  The R5900 was never tested when this was written, and it
  constructs on `-E testmips` (`d31_20261104/r5900_probe.out`: exit 0, the prompt reached, 0x1e stops with "UNIMPLEMENTED
  instruction").  Cloud Fable's follow-up (`../adj_20261104/ADJ2_D31_FABLE.md`) ruled D31 ROW-OWED; the row `r59 mdmx notRI`
  was predicted in `d31_20261104/PRETABLE_D31.out` before its run and measured red under D31 (`d31_20261104/SCORES_D31.txt`).
  The prediction "red: NONE" was right about the 121-row probe (D31 121/121) and wrong about why.
