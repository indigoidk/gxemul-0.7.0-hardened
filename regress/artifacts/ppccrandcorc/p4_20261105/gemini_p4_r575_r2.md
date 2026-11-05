# Gemini 4 Argon (gemini web proxy) -- job `p4_r575_r2`, banked by the main loop at 2026-11-05 09:03Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p4_r575_r2/gemini_web.out (mtime 2026-11-05 03:03:06 local, 5040 bytes)
* sender verdict line: (none -- the answer did not end in the requested line, so the sender scored it exit 1; it is a reading, read in full: its first line says CLOSE)

---

VERDICT: VALID (0 breaches surviving adjudication) / DENOMINATOR 453.

**Section 1: Handler Logic and State Conservation**
*   **Claim (`1:2735`):** `if (ba & !bb) /* CR[BA] & ~CR[BB] */` implements the `crandc` Book I v2.01 specification.
    *   *Test:* From `1:2732` and `1:2733`, `ba` and `bb` are right-shifted and masked with `& 1`, guaranteeing they strictly hold the value `0` or `1`. The logical NOT `!bb` maps `1 -> 0` and `0 -> 1`. Therefore, `ba & !bb` performs `1 & 1 == 1` only when `ba == 1` and `bb == 0`. This strictly matches PowerPC Book I v2.01 `CR[BA] & ~CR[BB]`. The claim is true.
*   **Claim (`1:2762`):** `if (ba | !bb) /* CR[BA] | ~CR[BB] */` implements the `crorc` Book I v2.01 specification.
    *   *Test:* Following the same masking guarantee from `1:2759` and `1:2760`, `ba | !bb` correctly evaluates to `1` when `ba == 1` OR `bb == 0`. This strictly matches `CR[BA] | ~CR[BB]`. The claim is true.
*   **State Conservation:** The step edits at `1:2734-2736` and `1:2761-2763` correctly clear the target bit via `cpu->cd.ppc.cr &= ~(1 << (31-bt));` and conditionally set it via `cpu->cd.ppc.cr |= (1 << (31-bt));`. This operation acts safely in-place on the CR register field. It does not invoke unbounded memory operations, does not write to memory, and strictly leaves alone every other state the emulator's CPU struct can save (e.g., GPRs, PC, memory, other status flags).

**Section 2a: Row Value Calculations**
*   **Claim (`2a:286`):** `64 crorc baread` with `crorc 17,31,5` over seed `0xFFFFFFFE` expects `0xFFFFBFFE`.
    *   *Test:* `0xFFFFFFFE` has bit 31 (LSB) as `0`. Bit 5 (in the second nibble `1111`) is `1`. Operation: `CR[17] = CR[31] | ~CR[5] = 0 | ~1 = 0 | 0 = 0`. Original CR[17] in `0xFFFFFFFE` is `1` (the fifth nibble is `F` = `1111`). Setting bit 17 to `0` changes the fifth nibble to `1011` = `B`. Result: `0xFFFFBFFE`. The claim is true.
*   **Claim (`2a:287`):** `64 crorc bbread` with `crorc 30,30,31` over seed `0xFFFFFFFC` expects `0xFFFFFFFE`.
    *   *Test:* `0xFFFFFFFC` ends in `1100`, so bit 30 = `0`, bit 31 = `0`. Operation: `CR[30] = CR[30] | ~CR[31] = 0 | ~0 = 0 | 1 = 1`. Original CR[30] is `0`. Setting bit 30 to `1` changes the final nibble from `C` (`1100`) to `E` (`1110`). Result: `0xFFFFFFFE`. The claim is true.
*   **Claim (`2a:288`):** `64 crandc setbits` with `crandc 31,30,31` over seed `0x00000002` expects `0x00000003`.
    *   *Test:* `0x00000002` ends in `0010`, so bit 30 = `1`, bit 31 = `0`. Operation: `CR[31] = CR[30] & ~CR[31] = 1 & ~0 = 1 & 1 = 1`. Original CR[31] is `0`. Setting bit 31 to `1` changes `0010` to `0011` (`3`). Result: `0x00000003`. The claim is true.
*   **Claim (`2a:289`):** `64 crorc setbits` with `crorc 31,0,31` over seed `0x00000000` expects `0x00000001`.
    *   *Test:* `0` means CR[0] = `0` and CR[31] = `0`. Operation: `CR[31] = CR[0] | ~CR[31] = 0 | ~0 = 0 | 1 = 1`. Original CR[31] is `0`. Setting it to `1` yields `1`. Result: `0x00000001`. The claim is true.

**Section 2d & 3: Arithmetic and Denominator Claims**
*   **Claim (`2d: R4`):** `m10 crandc BB & 17` (10001) removes values 2, 4, and 8.
    *   *Test:* The full field mask is `31` (11111 in binary). Subtracting 17 (10001) yields 14 (01110). 14 is equal to the sum of 8 + 4 + 2. The claim is true.
*   **Claim (`0`, `3`):** 54 single-constant edits kept all rows green (k = 2..30 (29), BA read `& 0x8001` (1), crandc set literals 7, 9, 11..30 (22), crorc set literals k = 26, 27 (2)).
    *   *Test:* Enumerate:
        2..30: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 (29 cells)
        `& 0x8001`: 1 cell
        7, 9, 11..30: 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 (22 cells)
        26, 27: 26, 27 (2 cells)
        Sum: 29 + 1 + 22 + 2 = 54. The claim is true.
*   **Claim (`3`):** Denominator is 453 cells = 6 clear + 15 cond + 12 decode + 186 mask + 8 read + 8 rmask + 136 rmask3 + 4 set + 62 setlit + 16 struct.
    *   *Test:* Enumerate the sum: 6 + 15 + 12 + 186 + 8 + 8 + 136 + 4 + 62 + 16 = 453. The claim is true.
*   **Claim (`4a`):** Test-variant table 3 has 70 rows total.
    *   *Test:* Enumerate the manifest blocks: ctl (6), 64 (12), s64 (24), edge (6), 64 crandc hi (1), 64 crorc hi (1), 64 crandc bbmask (1), 64 crandc order (1), 64 crorc bamask (1), 64 crorc bbmask (1), 64 crorc baread (1), 64 crorc bbread (1), 64 crandc setbits (1), 64 crorc setbits (1), 32 (12).
        Sum: 6 + 12 + 24 + 6 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 12 = 70. The claim is true.
*   **Claim (`0`):** Table 3 (section 4): all 53 predicted lines exact, 0 misses.
    *   *Test:* Section 4a (`PRETABLE_3.out`) cuts off at `m4_crorc_mask`, displaying only 14 variants before truncation. It is physically impossible to verify the total count of 53 lines from this packet alone. UNSETTLED. File to settle: `regress/artifacts/ppccrandcorc/table3_20261105/SCORES.txt` or the fully expanded `PRETABLE_3.out`.

P-GWEBP4RFIVER-109e
Review complete.