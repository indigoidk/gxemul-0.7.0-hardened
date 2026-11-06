# fbsdrampair -- two variants settled by measurement (main loop, 2026-11-05; the offline pipeline's first project use)

`_scratchpad/pipe/mutmeasure.py`, job `job.json` here, run `runs/fbs_settle_1`; SCORES.txt and SUMMARY.txt copied here.
* `b_exitkept_offset` (exit(1) kept after the OFFSET announce): 51/56, RED = O1, O2, B1, B2, B3 -- exactly the set the probe's
  contract had marked DERIVED (codex pass 2, R3; Gemini 4 Argon's reading of the record fixes called it unsettled).  The contract
  sentence now cites this measurement; the probe's code is unchanged (AST minus docstring SAME as table 1's probe56_frozen.py).
* `d_latchafter_mask` (the latch set after the announce instead of before; proposed by Gemini 4 Argon's draft review): 56/56,
  EQUIVALENT as predicted -- fatal() returns, and nothing reads the latch between the two statements.
