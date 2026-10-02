` are zero — lb answers `0x00`, lh answers `0x0000`, exactly the fix's answer. In the dog session `reg[CRIME_DOG/8]` is never written, so it reads 0 too. No other row refuses a read at 0x10/0x18/0x30. `imask/istat once`, the cause rows, and `dog once` are unaffected by odata.
  - This is not in DISCLOSED. The unnamed-offset bullet explicitly scopes added-effect debt to offsets the switch does **not** name and asserts "item 9 rows the READ answer at every named label". The mutant is the same one-line shape as codex's measured `if (relative_addr == CRIME_REV) odata = 1;` — it escapes only where the session's register content has zero low bytes. REV (0x11), CONTROL (ENDIANESS = 0x0100, low halfword nonzero), TIME (66–990, and `time lh v0` is certain since TIME < 65536) and the far block (0x08) are genuinely pinned; INTSTAT/INTMASK/DOG are not.

  Same root cause, second member — a low-byte **landing** at INTMASK also escapes:

  ```c
  		if (relative_addr == CRIME_INTMASK)
  			d->reg[CRIME_INTMASK / sizeof(uint64_t)] |= idata;
  ```

  The brief claims "imask ctl one at INTMASK" catches landings there. It catches only slot-overwrite landings (which clear bit 28 → IP2 stays low). A `|=` landing leaves `INTMASK = 0x100000ff`; the reassert masks `0x10000000 & 0x100000ff ≠ 0`, IP2 sets either way, and no row reads INTMASK's value (the accepted `lw +0x18` reads into `v0`, which is never printed). Item 7's landing floor at this named label is therefore shape-dependent, contrary to the DISCLOSED sentence.

  Repair is cheap and fully determined: (a) set `BIT = 0x10000001` in the imask/istat sessions (low byte nonzero → the v0 oracles go live; the reassert path is unaffected since the CRIME irq is one line) and seed DOG nonzero with an accepted `sd` before the refused `lb` in the dog session (the warm session's own pattern); (b) add an accepted-read row of INTMASK after the refused stores to pin low-byte landings; (c) re-run the three label-keyed answer mutants and the affected-table sessions.

  ## Q2 — Is the repair diff sound? Yes, with effort scoped as stated

  - Row count: I count exactly 111 rows in the shipped probe; `probe_first6_fix.out` shows 111/111, `CRIMEP_CONTROL=OK`, all new rows green.
  - Every new oracle varies under its named change. I re-derived the headline mutant counts from the session code and all match POSTTABLE: `o_rearm4 → rearm once 10` (1 + 4 four-byte + 5 lw-arm re-arms — exact), `wst_mc/o_wst_mc2 → hi keeps 0xffff` (both refused stores hit slot 0x4f, sh lands last), `o_rd_hi → top rd v0 0x8` (low byte of 0x0102030405060708), `lt_rng → hi once 3`, `lt_ctl → sh08b once 4`, `c_endian → sh08b run SENT` with `sh08b msg` staying 0 (0x0900 stops the CPUs before the later stores), `o_pre4 → top said 0 / latch x5 0`.
  - Controls are fail-closed: `gate hardint`/`gate line` entering the `control` set means a broken MACE latch invalidates the run rather than painting it green; the gate arithmetic checks out (`HARDINT = 0x28`, measured raw 32).
  - The TIME timing restatement (first tick fires because `ticks_till_next` starts at 0; window runs through the sampling read; IRQ-row tick risk is false-red-only) is internally consistent with `dev_crime_tick` and `CRIME_TICKSHIFT 14`.
  - `check_pred.out` verifies: `exact=57 differs=0 of 57`; 47 NEW + 10 T3INSTR in `table4.out`; all 57 raw logs end `CRIMEP_DONE`; the T3INSTR scores match the brief line-for-line (nine 85/85, `lt_par` 84/85).
  - Shipped-vs-frozen instrument: exactly 6 changed lines, all inside the docstring (the "5 + 1" claim), and 77 `row()` call sites (78 grep hits minus `def row(`). The repair diff in the brief is verbatim against the two instruments.

  ## Q3 — Which statements are wrong

  1. Probe header item 9 / DENOMINATOR: "the answer of a refused read at REV, CONTROL, INTSTAT, INTMASK, DOG, TIME and the far block" is pinned — wrong for register-answering mutants at INTSTAT, INTMASK, DOG (Q1). The DISCLOSED bullet's "(item 9 rows the READ answer at every named label)" is the false sentence.
  2. Same bullet: "imask ctl one at INTMASK" — false for non-clearing landing shapes (Q1, second member).
  3. Stale: DISCLOSED still says "ACCEPT cells at offsets other than +0x30, +0x210 and +0x278 … is not seen" — +0x00 is now rowed (`acc8 near`, `devsig`, `devsig hi`); the list should read "other than +0x00, +0x30, +0x210 and +0x278". Cosmetic, but this is a closing document.

  ## What I could not check

  - I did not rebuild or re-run anything (per the operational rule); all "measured" claims above are verified against the artifacts (`check_pred.out`, `table4.out`, the 57 logs' sentinels), not fresh execution. My escaping edits are argued from the code paths (`memory_writemax64` truncation, the sessions' register contents), not run — running them is the named measurement that would confirm 111/111.
  - I did not read the two mutant-generator scripts line by line; the mutant shapes behind counts like `lt_par`'s are taken as logged.
  - The ast-hash identity claim (`5da8e15ff1`) I did not recompute; the weaker claim behind it (docstring-only diff) I verified directly.
  - `free said`'s premise (debug() silent while free-running) is accepted as table-1-measured; I did not re-derive it from debug()'s implementation.

  ## Verdict

  By the brief's own rule the chain closes only on a pass with zero floor breaches, and I have a concrete, undisclosed breach with an exact edit — so this is `GAP`, not `CLOSES`. But the device fix reads correct, the repair diff and its kill table verified end-to-end against the artifacts, and the breach is three oracle cells plus one landing channel with a determined, small repair (`BIT = 0x10000001`, a DOG seed, one accepted-read row, two sentence corrections, then a re-measure of the three answer mutants). The foundation is sound; the 111-row instrument as shipped must not be declared closed.

  **GO-WITH-CHANGES**

To resume this session: kimi -r session_41e9957c-f491-42b8-933b-bc1021de8b9d
