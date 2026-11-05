# pvrrenderexit -- reading of the pass-8 record corrections (main loop, 2026-11-05)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_pvr_recp8.txt; `CODEXRECP8PVR: 6 ACCEPTED 2 TO FIX VERDICT:FIX`).  All six
corrections are TRUE and consistent with the gate block: 12 FLOOR, (c) +39 DEBT, and table 7's 208 = 207 full + 1 partial.  Two more
locations of the same family were found, and the main loop corrected both with the accepted wording:
r7_20261105/pvr_cells_7.py's docstring (copy .pre_recp8; still parses) and regress_20261105/DISPOSITION.md, with a dated correction
section that supersedes its count and source set.  A grep for "16 FLOOR" across the probe and the round's records now finds only
errata quoting the old sentence and the superseded lines.  The records then go to the REGRESS follow-up, which re-reads them on the
164-row detector as it will ship.
