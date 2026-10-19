# `fbctrlcmdkill` (`#567`) -- the ADJUDICATION PASS (F2) on pass 2, and the pass on its REPAIR

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You answered pass 2 blind to the other seats.  Below is EVERY seat's finding, numbered, with my disposition and what I
changed; the disagreements in each side's own words; and the repair those dispositions produced, with its measurements.
**A ruling in your favour is the one you are least likely to test -- be harder on your own findings, and check that my
FIX for each is right, not merely that your finding was.**  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, its
working tree; ignore every other `src/`.  If you cannot read files, everything you need is inlined.  READ-ONLY.
**VERDICT LINE FIRST.**

Seats: GPT-6 Astra (`codex_fbcmdp2.txt`), Grok 4.7 (`grok_p2.txt`), GLM 5.3 (`glm_p2.txt`, packet-fed); all three
SHIP WITH CHANGES.  Fable 5.1 walled (HTTP 429, `fable5_p2_WALL.txt`) -- a seat failure, held, not agreement.  Opus 5.5,
agy, kimi, deepseek and minimax deliberately not fired (the owner's 2026-10-17 roster).

## What changed after pass 2

The PRODUCT (`src/devices/dev_fbctrl.c`) is UNCHANGED.  The DETECTOR changed: `regress/fbctrl_cmd_probe.py` v1 (95 rows)
-> v2 (99 rows), and gate 16's block (`regress/gate_mips_folds.sh`) checks every row by name.  Before changing anything,
the unbuilt mutants pass 2 named were MEASURED on v1 (kill table 2a): three escaped.  After the repair, kill table 2
re-ran ALL 25 mutants on v2: every one red.  Both diffs and every table are inlined below.

## F1..F20 -- every finding, my disposition, and what changed

* **F1** [Astra; Grok contra] A 16-BYTE store reaches DATA: `testppc` (via `default_test()`) installs this device;
  `X(stvx)` passes `memory_rw` a 16-byte buffer; DATA at `+0x10` in a `0x20` window is not truncated; and
  `memory_readmax64()` shifts all 16 bytes into a `uint64_t`, keeping the LOW half on a big-endian guest.  So a 128-bit
  value whose low half is 0-2 is accepted and runs.  **ACCEPTED as a fact (verified by reading the three sites).  NOT
  repaired in this round -- disclosed as the probe's NOT CLAIMED (6) and FILED as `fbctrlvec128`, with `#549`'s PORT
  arm, which shares it.**  See D1.
* **F2** [Astra] The accept side across widths: every accepted COMMAND write was `sw`, so `(idata > 2 || len != 4)`
  would pass.  **MEASURED: E13 escaped v1, 95/95.  REPAIRED: A:nop by `sd`, A:set by `sh`, A:get by `sb` (L keeps
  `sw`) -- E13 is 89/99 on v2.**
* **F3** [Astra Q5, Grok's first FLAG] `nosmall` cannot see a SET at a valid size: under `B_gateoff`, `R:w1` runs
  SET_RESOLUTION at 123x77 and `nosmall`, `x1` and `y1` all stay green; the contract's "executes nothing" was false for
  SET.  **REPAIRED: `ref * noset` counts SET's `changing resolution` debug() line, which prints while stepping;
  `acc set res` (1 on the fix) shows that channel live.  `ref w1 noset` is now red under B_gateoff, D1, E10 and E11.
  The contract now claims "no GET (X1/Y1 kept) and no SET (noset)", and says a NOP is not claimed.**
* **F4** [Astra Q4, Grok Q4] The DIRECTION cell had no mutant.  **MEASURED on v1: E6 (dispatch on a read) killed,
  70/95; E12 (the gate's `else if` made `if`, so a read falls into the store branch and stores 0 after returning)
  ESCAPED, 95/95.  REPAIRED: M1 reads COMMAND twice and X1 twice -- E12 is 97/99 on v2.**  See D3.
* **F5** [Astra] The accepted path's dispatch guard (`if (current_port == COMMAND)`) had no mutant.  **MEASURED: E7
  (dispatch on every port write) killed, 71/95 on v1 -- the seed's X1/Y1 writes re-run the GET.  No repair needed.**
* **F6** [Astra Q6] The gate block's SUBSTITUTION hole: a row replaced by an unrelated unique green row kept every count.
  **REPAIRED: the block checks all 99 expected names, each green exactly once; a substituted log now reds it
  (`wiring_20261019/GATE16_REPLAY_v2.out`, `neg_substituted`).**
* **F7** [Astra Q6] The child-exit gap: several sessions' exit status was read by no row.  **REPAIRED: `sessions
  clean` -- all 22 sessions SURVIVED and exited 0, pinned to the literal 22 (not a count computed from the list).**
* **F8** [GLM Q2(b), Grok Q2] The latch SET crossed with a WIDE value: `&& (!warned_cmd || idata <= 0xffffffff)`
  restores both defects once the latch is set.  **MEASURED: E14 escaped v1, 95/95.  REPAIRED at no row cost: T2's
  third refusal is `sd 0x100000005` with the latch set -- E14 is 97/99 on v2 (`two cmd` and `sessions clean` red).**
  The narrower carve-out -- exempt only the ALIASES of 0-2 under the latch -- stays NOT CLAIMED (0).  See D2.
* **F9** [GLM Q4] The latch pre-set (E8), the announce's argument (E9) and the compare's operand (E10) had no mutant.
  **MEASURED: killed, 84, 90 and 36 of 95 on v1.  No repair needed.**
* **F10** [Grok Q4] The `(int)` cast had no mutant, and "E5 closes the sign axis" overstated: E5 is SIGNED 64-BIT.
  **MEASURED: E11 `(int) idata` killed, 78/95 on v1 (m1w and m1d die).  The records say E5 = signed 64-bit, E11 = int.**
* **F11** [GLM Q5] Under D9 four rows (`devsig`, `acc get x1`, `acc get y1`, `latch get x1`) are green for the wrong
  reason (the X1/Y1 seeds themselves are refused); and `ref w2 cmd`'s aliasing applies under `B_gateoff` too.
  **ACCEPTED as records: both go into the kill-table comparison notes.  No row change -- each mutant is killed by others.**
* **F12** [GLM] The brief's `gate_hygiene.sh` numstat said 13/6 against a 14/6 diff.  **ACCEPTED: the numstat predated
  a one-line rewrap; corrected.**
* **F13** [Grok] Clause (b) "at every fixed site" overstated: `B_gateoff` restores the one BEHAVIOURAL site, while the
  unread `warned_cmd` field and the `default:` comment stay.  **ACCEPTED: the records say "the one behavioural site".**
* **F14** [Astra, Grok, GLM] The census repair belongs in its OWN commit, landed first.  **ACCEPTED, all three: commit A
  repairs `#564`'s stranded pins alone (`EXPECT_PTY_PROBES` 74 -> 75, the grandfathered name, the comment), derived with
  `fbctrl_cmd_probe.py` moved aside; commit B (`#567`) then moves 75 -> 76 and `EXPECT_CONVERTED` 25 -> 26.**
* **F15** [Grok, GLM; Astra: "defensible temporary organizational debt"] Gate 16 placement.  **ACCEPTED as DEBT, not
  fit: the gate comment says so, attributing Grok's "not fine" and GLM's hard stop (the split before a third device
  probe enters gate 16); `gatedevicesplit`'s row gains that stop.**  See D5.
* **F16** [GLM Q6] No timeout fences the probe launch: a wedged probe hangs gate 16 (a visible hang, not a false pass;
  `#549`'s block is the same).  **FILED, not repaired here (it is both blocks' shape, a harness round).**
* **F17** [GLM Q2(a), Grok Q2] Value carve-outs (`&& idata != 6`, `!= 0x100000004`) pass every row.  **ACCEPTED as
  disclosed: NOT CLAIMED (2) now names the shape.  A relational compare's generating set is its regions; no finite row
  set closes every carve-out.**
* **F18** [Grok Q6] The replay injected `fcrc` and never exercised the launch line; a `0/0` trailer with no rows fails
  only the two equality pins.  **NOTED: the pins are present and the new per-name checks red it too.  No change.**
* **F19** [GLM, Astra] Premise 1a (the compare sees the full value): GLM upheld it for sb/sh/sw/sd, pinned behaviourally;
  Astra falsified it for 16-byte stores.  **Both stand: F1 is the exception, scoped and filed.**
* **F20** [GLM Q1b, Grok] "No other writer of COMMAND": GLM could not settle it from the packet; Grok read the whole file
  -- two stores into `port[]`, `memset` in `DEVINIT(fbctrl)`.  **Settled TRUE by Grok's reading.**

## D1..D5 -- the disagreements, in each side's words

* **D1 (F1, the 16-byte store).**  Astra: *"Handle oversized COMMAND writes before conversion and add a vector-store
  regression."*  Grok: *"Those dropped prefix bytes are also absent from the int store, which assigns that same idata.
  They cannot place a command other than 0, 1 or 2 in the cell."*  **My ruling: FILE, not this round.**  Warrant:
  closing it needs a new oracle -- a PowerPC session issuing `stvx` -- and the reopening rule admits a second site only
  under the SAME detector with no new oracle; and Grok is right that no host kill follows.  But Astra is right that it is
  the round's own class -- a wide value run as its low part -- one width up, so the filing names it as that, for both
  arms.  **Astra and Grok: adjudicate this between you.**
* **D2 (F8, latch x wide).**  GLM: *"it is not merely un-rowed, it is exploitable -- it needs a row more than a mutant."*
  Grok: *"That is NOT CLAIMED (0), and it passes 95/95."*  **My ruling: closed anyway, at no row cost (T2's third write),
  on the measured delta -- not as a floor obligation; the house grading of latch x a value class as clause (e) (`#549`'s
  latch x bit) is unchanged.**
* **D3 (F4, E12).**  Grok predicted *"`rdcmd val` would catch it"*; table 2a measured an ESCAPE (95/95): a read returns
  its value before the store, and no v1 session read one port twice.  **Settled by measurement.**
* **D4 -- none on the census (F14): all three agreed.**
* **D5 (F15, placement).**  Astra: *"defensible temporary organizational debt"*.  Grok: *"The arm can land.  The sentence
  that this placement is fine should not."*  GLM: *"CONTEST ... Accept only with a hard stop."*  **My ruling: land it in
  gate 16, recorded as debt with GLM's stop.**

## What is still OWED, and where I may be fooling myself

* F1 is SOURCE-DERIVED: no `testppc` witness has been built.
* The `noset` channel rests on `debug()` printing while stepping.  `acc set res` shows it live; if a verbosity change ever
  silenced it, that row would go red, not pass.
* Two of my table-2 predictions missed rows (E6 reached `acc set ran` and `latch set ran`; E14's `two once` stays green
  because the announce prints before T2 dies).  The kills held; the reach was mispredicted.
* Tables 1, 1b and 2a are history on v1.  Table 2 is the measurement of what ships.
* Commit A (the census) and the records are not written yet; nothing is committed.

## Questions

1. Adjudicate F1..F20 and D1, D2, D3, D5: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or repaired fourteen findings, filed two (F1, F16), and
   left four as records or no-change (F11, F17, F18, F20).  Fourteen accepted in a row is a suspicious number.
3. **The repair is new floor-bound material: does a clean-sweep mutant exist for the SHIPPED COMPOSITE (the fix + probe
   v2 + gate block v2)?**  Name it, the edit exactly, and the row you expect to stay green.
4. **What did all of us miss?**

If, while verifying a claim, you found something ELSE -- say so.

**Answer format:** your token, then `VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>`, then `FLAG:` lines
(evidence: a grep anchor or a construct name), then answers 1-4.
