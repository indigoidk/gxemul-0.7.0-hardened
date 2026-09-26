OPUS550F2_ALIVE

**VERDICT: SHIP WITH CHANGES.** I would change five of your dispositions: R2, R6, R7, R9 and S4. S1 stands, with one date to check. S2 (file it) stands, but its header sentence needs widening. The rest stand.

**Measurement basis:** everything I ran was in my scratch dir or WSL `/tmp/opus550`. Nothing under the project was written. I stopped all of my own processes at the end; a peer session's #549 table was left alone.

1. **R6, my own finding: your restatement is wrong (read).** "Must first stop waiting out a 12 s poll" turns a cost into a precondition, and meeting it means changing the oracle.
   - `session()` scores any exit as `alive=False`, so adding `quit` would read every surviving session as DEAD.
   - Shortening the poll brings back the false green the probe's own comment records (a SIGABRT arriving 0.6 s later, read as alive).
   - Either change needs its own kill table.
   - Suggested wording: "gate_arm.sh hosts seven sgi cold-debugger probes of this shape; about 570 s per run, because each surviving session waits out the 12 s death poll."

2. **R7 is still false as restated (read).**
   - 4bit and sig already run any number of `tag=binary` legs, including one. What they lack is a single-leg oracle: their key cells are `want None`, "recorded, not predicted".
   - The filed row `wdcaltoffleg` (OUTSTANDING_BUGS.md:18455) already lists what each probe owes. The parent's line is correct: its `ok` needs both legs (`b_hit and f_hit`), and it exits 0 whatever the result. 4bit owes an oracle choice (the fix-side absolute). sig owes a redesign, because its oracle cannot tell the outcomes apart.
   - sig's "ciR: CD-ROM rig the battery does not build" is false. The probe adds the `ciR:` prefix itself (lines 75 and 140), and gate 10 already carries `$IMAGES/wdc-scratch-64m.img`.
   - **I retract my pass-1 "undercounts" finding.** The import brings in the encoder and `Emu`, not a leg mode, so no sibling shares one.

3. **R9 names the wrong queue row (read).** `wdcaltoffleg` and `wdcsingleleg` (lines 18467 and 18478) each say their exemption "is re-dated naming THIS row". Name those two, not `wiringcliff`.

4. **S4 misses a file (measured).**
   - `tools/precommit_check.sh` also has a parked hunk: `SCORE_CLAIMS_MANIFEST` goes from 30 to 32, from #529 and #549.
   - The hook runs that file from disk, and #550 edits it. If its blob is staged from disk, the committed tree pins 32 against 30 gated probes, and every later commit fails with "COVERAGE DROPPED".
   - Swap both files, not just the checker.
   - The first two wirings hit the same problem: `ppc_rldicl_probe.py` (10-08) has its parked hunk (measured inert), and `gate_arm.sh` (ip30's host, 10-15) has #529's 59-line hunk. Make the swap a rule for every file with a parked hunk.

5. **R2 overcorrects "stale" (measured).**
   - `chk()` does carry 24 calls, added by #484.
   - But the nine row functions the old paragraph names still exist, with 16 call statements.
   - A sentinel on `chk()` alone leaves those unguarded, the way sh4_tmu's 12-of-18 is. So the paragraph is half-stale.
   - #551 should either move those functions onto `chk()` or list wdc_identify as non-uniform COVERED.

6. **R8 holds (measured).**
   - All four probes set `MACH = "alphabook1"`, and the parked palcode diff sits inside an existing comment.
   - On a copy of `build/gxemul`, which carries #540's parked `PHYSICAL` change: alpha_tbi 15/15, lca_badval 75/75, lca_widewrite 13/13.
   - lca_isalane is incomplete: it had 80 rows ok and 0 FAIL when I stopped it at 484 s, because a peer's #549 table was running on the same machine.

7. **S1 is right in shape (measured).**
   - Built into a scratch checker, it expires exactly one entry per week (1 problem on 10-09, up to 10 on 12-11), and the selftest stays at 22/22.
   - Every date is a Thursday. HEAD has only three other dated lists (SC, SM and AB_EXEMPT, on 09-27, 11-30 and 2099-01-01), and no S1 date matches them.
   - One date to check: 11-26 is US Thanksgiving, and the commits carry -0500, so 4bit would go red on the holiday Friday.
   - The last entry now falls due 23 days later than in pass 1; that is the owner's call.
   - The "2026-10-08 to 2026-11-17" range is written in both the checker header and `precommit_check.sh`, so change both.

8. **S2: filing is right, but widen the header sentence (read).**
   - The strongest reason to file is that the check would turn a one-time ruling into a permanent ban on two entries sharing a date. That is the owner's call.
   - But S1's "none on any other list's date" is a cross-list property the proposed check cannot see, and R4's collision was cross-list. Say so in the header.
   - Note in the filed row that a cross-list version would go red immediately, because AB_EXEMPT holds 12 entries on one date.

9. **R3, R4, R5, S3 and R10 stand.** R3's "nine" is exact as a count of `== 0` terms. But dozens of inline comparisons feed those counters, and that is the refactor's real size.

---
*Recorded by the main loop: agent a8c6fd47a6c9c37ac (resumed), `agent_models.py` = clean, opus-5-5 throughout.  "A
peer session's #549 table" in its first paragraph is this main loop's own kill table 4, which it correctly left alone.*
