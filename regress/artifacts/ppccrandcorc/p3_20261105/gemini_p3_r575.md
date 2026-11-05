# Gemini 4 Argon (gemini web proxy) -- job `p3_r575`, banked by the main loop at 2026-11-05 08:54Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p3_r575/gemini_web.out (mtime 2026-11-05 02:27:41 local, 2466 bytes)
* sender verdict line: GWEBP3RFIVE: 15 ATTACKS 0 BROKEN 15 HOLDS 0 UNSETTLED DRAFTABLE:YES
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---

VERDICT: CLOSE.

1. **THE CLOSURE:**
The enumeration in section 3 is complete for the bound. There are no in-bound single edits outside the enumerated 239 cells that keep all 66 rows green. 
The four EQUIVALENT cells are precisely equivalent:
*   `crandc BA read mask &3`: The condition evaluates `ba & !bb`. Because `bb` is masked to `& 1`, `!bb` evaluates strictly to `1` or `0`. A bitwise AND against `1` masks out everything except the low bit (the 1-bit) of `ba`, meaning `ba & 3` and `ba & 1` produce identical outputs.
*   `crandc BA read mask &7`: The same logic applies; `ba & !bb` strips the 2 and 4 bits entirely, making `ba & 7` equivalent to `ba & 1`.
*   `crandc set |= -> ^=`: The unconditional clear `cpu->cd.ppc.cr &= ~(1 << (31-bt));` executes immediately before the conditional set, guaranteeing the destination bit is `0`. Setting a zeroed bit via `0 | 1` or `0 ^ 1` yields `1` either way.
*   `crorc set |= -> ^=`: Identical logic to `crandc`; the unconditional clear guarantees the XOR and OR operations behave identically on the zeroed bit.
Your DENOMINATOR stands verified: 6 clear + 15 cond + 12 decode + 186 mask + 8 read + 8 rmask + 4 set = 239 cells.

2. **THE DIFF:**
Each new row precisely catches what its note and the closure claim:
*   `64 crandc bbmask`: Pre-setting the bit EQUAL to the result (1) ensures that if the condition fails, the clear leaves it at 0 (detected). The uniform seed successfully traps BB aliases and `BB<-BT` reads (since CR[BT=16]=1 != CR[BB=31]=0).
*   `64 crandc order`: The inverse pre-set combined with `BT=BB=9` ensures an early clear changes the BB read from 1 to 0, which flips the evaluated condition and sets the result to 1 (caught). 
*   `64 crorc bamask`: Pre-setting EQUAL to 0 effectively traps BA mask aliasing and `BB<-BT` reads, and correctly exposes the clear->toggle substitution (which toggles the 0 to a 1).
*   `64 crorc bbmask`: With BT=BB=31, an early clear mutates the BB read from 1 to 0, flipping the NOR condition and exposing the timing violation.
No sentence in the new records or errata is false against sections 1-4. Pass 2's false records (F4-F7 in errata; F1-F3 in the probe docstring) were fully corrected, and the four R5 predictions were supplied and mapped out with accurate execution traces.

3. **VERDICT:**
CLOSE. Zero floor breaches, zero false records, full denominator swept.

P-GWEBP3RFIVE-4e47
GWEBP3RFIVE: 15 ATTACKS 0 BROKEN 15 HOLDS 0 UNSETTLED DRAFTABLE:YES