OPUS_SEAT_ALIVE_20260925_549v6

`# CHECKPOINT -- 2026-09-25 ~19:35 (087a90 sections rewritten; the peer's sections below are untouched)`

VERDICT: SHIP

Measured in a fresh clone `/tmp/gxo549v6`: before any run `dev_fbctrl.c` (129694b8) and the v6 probe (a9a2be3d) matched the working tree; the rebuilt base is b5b99e6d = `build/gxemul` and scores 117/117 rc=0 with `session B SURVIVED 224/224 once=1`. Every mutant built fresh, the clone was restored to SEC and md5-checked, the sentinel cleared, no `/tmp` leftovers. Outputs in `opus549_measured/v6/` (`TABLE_v6floor.out`, `unset_witness.out`, `logs/`, `INPUTS_v6.md5`).

**1 & 2. Floor question / is B's aggregate enough — no new breach (measured).** Denominator I built and scored against v6, none in table 6:
- `WB_sh32` (accept 2^5 only by sh) → **116/117 RED**, B's sh row. Width×bit is caught: B walks every bit at every width, and an accepted value sticks through the later refusals to the one read.
- `LB_set16` (accept 2^4 only when the latch is set) → **109/117 RED**. Latch-set×bit caught (B + P).
- `SN_signed` (signed compare) → 111/117 RED; `MK_b*`, `MKB_*`, `MKW_*` in table 6 all red. Every plausible narrowing of `idata >= 8` — bit-ignore, width, sign, boundary — is caught. This is what B was added for, and it holds.
- `EQ_shift3` (`(idata>>3)!=0`) → 117/117, behaviourally equivalent (denominator anchor, not a breach).
- **117/117 escapes, all the already-disclosed accept-a-value-no-row-pins class:** `MB_v18` (accept 0x18), `MB_pc4` (accept any 4-bit value), `PB_prev3_16` (accept 16 at previous 3), and `LB_unset16` (accept 16 when the latch is unset). I checked whether these are new: they are the same family as `A1_not10` (accept 10), which has been GREEN 117/117 and disclosed since table 5. Accepting an out-of-range value stores it, and the **kept DATA-arm `exit(1)` (NOT CLAIMED (2)) is the tripwire** — I witnessed `LB_unset16` HOST-DIED on a fresh device whose first PORT write is 16, then a DATA read (`unset_witness.out`); the fix survives. So the PORT detector does not pin these, by design, and the tripwire catches the symptom. Not a floor breach.
- The one thing worth naming (Q6): B refuses single bits only with the latch **set** (after its own first 2^3); the only single bits refused as a *first* refusal anywhere are 2^3 (P/B/W) and 2^8 (X7). So the "latch-unset × single-bit" cell is open for 2^4–2^7, 2^9–2^30 — a two-axis cell under NOT CLAIMED (0), whose symptom is the restored exit caught by the tripwire. It is disclosed coverage debt, not a breach, and closing it would need a fresh device per value (the unbounded growth the floor forbids).

**3. V1–V20: all UPHELD (V11 refined); 0 overturned.** V1 (my finding) UPHELD — every compare-narrowing now red, v5's bit-range escapes closed by B; I was hardest here and it holds. V2, V3, V6, V7, V8, V9 confirmed by measurement (EQ_* 117/117, K has no PORT read, etc.). V14/V15 REJECTs UPHELD — `accept selector 7 written by sd` (A) and `refuse 8 (sw)` (P) both exist in the fix output, so those cells are held and W's text is right. V16 (CELL_rd_s5 kills via the command-default exit) and V17 (class warrant false) UPHELD — my measurements. V20 NO-CHANGE UPHELD — R samples its count only after its second refusal, so it is not a first-announce holder; holder lists don't claim exhaustiveness. V11 REFINE: B's 108 refusals make B_mod12 RED, correctly overtaking the old "period twelve" disclosure.

**4. Header sentences.** All check out (B SESSIONS text, the new holders, (3)/(4)/(5)/(8)). One imprecision in LIMITS OF A ROW: it says a B width row "prints the last one's stored int" — if a *middle* bit is accepted and later bits refused, the row prints that accepted middle value (kept through the later refusals), not the last store's. The row still reds; the wording is just narrow.

**5. Channel.** Table 6 shows every `MKB_*`/`MKW_*` red on exactly the predicted B width rows; I reproduced the mechanism (`WB_sh32` reds only the sh row). The extra non-B reds on MKB_03/04/08/32 are expected — those bit values coincide with other sessions' fixed refusals (2^3, 2^8=0x100, 2^32 wides).

The fix is unchanged and correct; session B closes the v5 breach; every plausible compare-narrowing is caught; the residual 117/117 edits are the standing, disclosed accept-a-value class whose exit is caught by the kept DATA tripwire. This is a valid zero with its denominator — the chain closes. Commit remains gated on Astra per the 2026-09-25 owner ruling; nothing I measured blocks it.

---
*Recorded by the main loop: agent aabc7b9d2fb013ad5 (resumed for v6's own pass), final text by claude-opus-4-8 -- A FALLBACK (the seat was asked for opus-5-5; three refusal events, then opus-4-8 wrote this and ran the v6 measurements), kept for the record and NOT counted as the Opus seat at 2026-09-26T00:39:54.616Z, extracted verbatim from the agent transcript.  Badge s.*
