# Gemini 4 Argon -- job `p4_r575`, a LATER RE-SEND (the sender re-sends a job whose answer lacked a verdict line), banked 2026-11-05 10:08Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p4_r575/gemini_web.out (mtime 2026-11-05 03:57:51 local, 3484 bytes); the earlier answer is gemini_p4_r575.md (also kept in the job's prev_* directories)

---

VERDICT: VALID AND CLOSES (0 breaches surviving on denominator 453).

**1. The Emulator C Code Changes (`crandc` and `crorc`)**
*   **Claim/Step:** The C code uses `if (ba & !bb)` to implement Book I's `CR[BA] & ~CR[BB]` (1:2735) and `if (ba | !bb)` to implement `CR[BA] | ~CR[BB]` (1:2762).
*   **Attempted Refutation:** Bitwise `~` is not identical to logical `!`. 
*   **Test:** The operands `ba` and `bb` are strictly extracted as 1-bit integers via `(cr >> ...) & 1` (1:2732-2733 and 1:2759-2760). Their domain is exactly `{0, 1}`. Over this domain, logical `!bb` yields `{1, 0}`, which is identical to the lowest bit of the bitwise NOT `~CR[BB]`. The refutation fails; the step is mathematically correct.
*   **State Preservation:** The state mutations `cpu->cd.ppc.cr &= ~(1 << (31-bt));` (1:2734) and `|= (1 << (31-bt));` (1:2736) apply a strict bitmask targeting solely the `31-bt` bit. No other bits of the Condition Register are written to, and no other machine state is accessed or modified by this assignment. It safely leaves alone every un-targeted state. 

**2. The Python Test Probe Additions**
*   **Claim/Step:** `64 crorc baread` uses seed `0xFFFFFFFE` to yield `CR[31] = 0` and `CR[5] = 1` (2a:+286).
*   **Test:** Section 1b establishes `CR[i]` is `(cr >> (31-i)) & 1`. For `CR[31]`, the shift is `0`, masking the LSB. The LSB of `0x...FE` (binary `...1110`) is `0`. For `CR[5]`, the shift is `26`; all bits above the LSB in the seed are `1`, so it evaluates to `1`. Refutation fails; correct. 
*   **Claim/Step:** `64 crorc bbread` uses seed `0xFFFFFFFC` to yield `CR[30] = 0` and `CR[31] = 0` (2a:+287).
*   **Test:** The lowest byte `0xFC` is binary `1111 1100`. Bit 30 (second from right) and bit 31 (LSB) are both strictly `0`. Refutation fails; correct.
*   **Claim/Step:** `64 crandc setbits` uses seed `0x00000002` to yield `CR[30] = 1` and `CR[31] = 0` (2a:+288).
*   **Test:** The lowest byte `0x02` is binary `0000 0010`. The LSB (`CR[31]`) is `0`, and the next bit (`CR[30]`) is `1`. Refutation fails; correct.
*   **Claim/Step:** `64 crorc setbits` uses seed `0x00000000` to yield `a = b = 0` at index `0` and `31` (2a:+289).
*   **Test:** A zero integer provides `0` at all bit indices. Refutation fails; correct.
*   **State Preservation:** These additions append execution targets to the host script via pure Python invocations (`session()`, `row()`). They strictly read outputs and assert comparisons without mutating live environment variables outside the tester bounds. 

**3. The Shell Gate Counter Updates**
*   **Claim/Step:** The loop bound and test checks move from `66` to `70` rows (2c:+25, 2c:+31, 2c:+32).
*   **Test:** The baseline state of the suite had 66 rows. The diff in 2a inserts exactly 4 discrete instances of `cr_row(...)`. Enumerable arithmetic proves `66 + 4 = 70`. Refutation fails; the shell assertions correctly cover the new length.

**4. Errata and Denominator Arithmetic**
*   **Claim/Step:** The cell enumeration expands to a denominator of exactly `453` cells (3:DENOMINATOR).
*   **Test:** The text establishes a baseline of `239` cells from round 2 (3:ENUMERATION). The additions listed are: `34` mask values at `4` read sites = `136`; `31` literal constants at `2` handlers = `62`; plus `16` structural cells. Summing the new cells: `136 + 62 + 16 = 214`. Summing the total denominator: `239 + 214 = 453`. Refutation fails; the stated arithmetic is exact.

P-GWEBP4RFIVE-f013
All claims evaluated and verified.