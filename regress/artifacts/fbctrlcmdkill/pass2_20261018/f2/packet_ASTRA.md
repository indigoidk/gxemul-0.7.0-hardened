**Your token: `ASTRA_FBCMD_F2_20261019`** -- open your answer with it.  You raised F1-F7 and part of F19: be HARDER on them -- and on whether each FIX is right -- than on anyone's.

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

# THE ARTIFACTS, VERBATIM

## A. The repair -- probe v1 -> v2 (`regress/fbctrl_cmd_probe.py`), the whole diff

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlcmdkill/pass2_20261018/frozen/fbctrl_cmd_probe.py.txt
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlcmdkill/pass2_20261018/f2/frozen/fbctrl_cmd_probe.v2.py.txt
@@ -13,20 +13,21 @@
   C    controls: PORT=5, DATA=0x2a, read back (LIVENESS); PORT=1, DATA=123, PORT=0, DATA=2 (GET_RESOLUTION, headless:
        zeroes X1/Y1), PORT=1, read (DEVICE-SIGNATURE: 0 where RAM would keep 123).
   R:v  one REFUSAL per class, on a device seeded with COMMAND = 2 (by a GET), X1 = 123, Y1 = 77: PORT=0, DATA=v, then
-       read COMMAND, X1, Y1.  Classes: 3, 4, 5 and 0xffffffff by sw; 3 by sb and 4 by sh (the gate never tests len,
+       read COMMAND, X1, Y1; no SET's resolution-change line may print.  Classes: 3, 4, 5 and 0xffffffff by sw; 3 by sb and 4 by sh (the gate never tests len,
        so `&& len >= 4' would let a byte or halfword command through --
        regress/artifacts/fbctrlcmdkill/draft_20261018/PRETABLE.out, section 1); 0x100000003, 0x100000000, 0x100000001,
        0x100000002 and 0xffffffffffffffff by sd.  The wide aliases of ACCEPTED commands are the width pin: a compare on
        the stored int would run NOP (COMMAND reads 0), SET_RESOLUTION (COMMAND reads 1) or GET_RESOLUTION (X1/Y1 read 0).
-  A:n  ACCEPT, latch clear: NOP after COMMAND 2 (COMMAND reads 0, X1 keeps 123); SET_RESOLUTION with X1 = Y1 = 0
-       (dev_fb_resize() prints `size too small (0 x 0); ignored.` -- a fatal() that returns; COMMAND reads 1);
-       GET_RESOLUTION after X1 = 123, Y1 = 77 (both read 0; COMMAND reads 2).  No command announce in any of them.
+  A:n  ACCEPT, latch clear, one width each: NOP by sd after COMMAND 2 (COMMAND reads 0, X1 keeps 123); SET_RESOLUTION by sh with X1 = Y1 = 0
+       (dev_fb_resize() prints `size too small (0 x 0); ignored.` -- a fatal() that returns; COMMAND reads 1; and the resolution-change debug() line
+       prints -- the noset rows' channel, shown live); GET_RESOLUTION by sb after X1 = 123, Y1 = 77 (both read 0; COMMAND reads 2).  No command announce in any of them.
   L    ACCEPT with the latch SET: refuse 3 first, then GET (X1 123 -> 0), NOP (COMMAND 0), SET at 0 x 0 (the resize line
        once, COMMAND 1) -- one command announce in the whole session.
-  M1   a READ of COMMAND does not execute it: COMMAND = 2 by a GET, X1 = 123, PORT=0, read DATA (2), PORT=1, read X1
-       (still 123: a re-executed GET would zero it).
+  M1   a READ of COMMAND does not execute it: COMMAND = 2 by a GET, X1 = 123, PORT=0, read DATA twice (2, 2), PORT=1,
+       read X1 twice (123, 123): a re-executed GET would zero X1, and a read that STORED would zero the second read.
   M2   a DATA write of 3 to a NON-COMMAND port (PORT=3, X2) is ordinary storage: reads back 3, no announce.
-  T2   two refusals, 3 then 5: ONE command announce, naming 0x3; COMMAND keeps its power-on 0.
+  T2   three refusals -- 3, 5, then sd 0x100000005 with the latch SET: ONE command announce, naming 0x3; COMMAND
+       keeps its power-on 0.
   P1   selector refused first (PORT=9, #549's announce), then command 4 refused: one announce of each kind.
   P2   the reverse order: command 4, then selector 9: one of each.
   F    FREE-RUNNING: PORT=0, DATA=3, then continue to a breakpoint -- the announce must print: under free-running
@@ -35,36 +36,52 @@
 
 CONTRACT (clause e) -- AN ENUMERATION.
 THE FLOOR.  The fixed DATA arm's refusal branch tests the access direction, the port (`current_port == COMMAND`), the
-written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits) and the latch (`!warned_cmd`); the accept
-branch stores the value and, at COMMAND, dispatches it.  Every cell of those is held:
+written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits the device receives) and the latch
+(`!warned_cmd`); the accept branch stores the value and, at COMMAND, dispatches it.  Every cell of those is held:
   the value  at the bound, 2 (A:get, and every seed); below it, 1 (A:set) and 0 (A:nop); past it, 3 (R:3, R:sb3, L,
              T2, F -- rule D2's B+1 edge), 4 (R:4, R:sh4, P1, P2), 5 (R:5, T2), 0xffffffff (R:m1w) and all-ones (R:m1d)
-  its width  sb (R:sb3), sh (R:sh4), sw (R:3, R:4, R:5, R:m1w), sd (R:w3, R:w0, R:w1, R:w2, R:m1d) -- the four wide
-             values whose low word is 0..3 are the width pin: a compare on the low word accepts w0-w2
+  its width  refused: sb (R:sb3), sh (R:sh4), sw (R:3, R:4, R:5, R:m1w), sd (R:w3, R:w0, R:w1, R:w2, R:m1d, T2);
+             accepted: sb (A:get), sh (A:set), sd (A:nop), sw (L, every seed).  The four wide values whose low word
+             is 0..3 are the width pin: a compare on the low word accepts w0-w2
   the port   COMMAND (every R and A session, L, T2, P1, P2, F) and not COMMAND (M2: 3 at X2 is data)
   the latch  clear (the first refusal of every R session, L, T2, P1, P2, F) and set (L's three accepts, T2's second
-             refusal); the selector's latch apart from it, in both orders (P1, P2)
-  direction  a write (all) and a read (M1: a read of COMMAND returns it and runs nothing)
+             refusal and its third, a WIDE one); the selector's latch apart from it, in both orders (P1, P2)
+  direction  a write (all) and a read (M1: COMMAND and X1 each read twice -- a read returns the cell, runs nothing
+             and stores nothing)
 EFFECTS, each held by the sessions named:
   a refused command keeps COMMAND's previous value -- 2 (every R class), 0 (T2)
-  a refused command executes nothing -- X1 and Y1 kept with a GET in COMMAND (every R class); no resize line (nosmall)
-  the first refusal announces once, naming the full value -- every R class, T2 (0x3, then 5 silent), P1 and P2 (beside
-      #549's selector announce), F (free-running: fatal() prints where debug() would not)
-  an accepted command is stored and runs -- NOP (A:nop, L), SET_RESOLUTION (A:set, L: the resize line), GET_RESOLUTION
-      (A:get, L, C), with the latch clear (A) and set (L)
-Measured: the eleven edits of kill table 1 (regress/artifacts/fbctrlcmdkill/killtable1_20261018/) are all red -- the
-gate removed (the pre-#567 arm: 36/95, row for row the pre-fix leg), the compare narrowed to 32 bits, the bound moved
-down by one, two and three, the gate qualified by width, the latch shared with the selector's or never set, the
-announce demoted to debug(), the refused value stored, and the port test dropped.
-On a dead binary 15 rows read green -- the eleven `nosmall' rows and four announce counts, which read 0 on a session
-that never started -- so gate 16 requires FBCMD_CONTROL=OK and pins the score by equality (kill table 1's null media).
-NOT CLAIMED (disclosed).  (0) A joint cell: the latch SET crossed with a wide alias -- no row refuses w0-w2 after a
-first refusal, and the gate does not read the latch.  (1) A refusal that STORES a value aliasing the previous COMMAND:
-w2 truncates to 2 and its `cmd' row cannot vary; ten classes and T2 pin the store (table 1, D8).  (2) Values and bits
+  a refused command executes nothing -- no GET (X1 and Y1 kept, with a GET in COMMAND: every R class) and no SET (no
+      resolution-change line: every R class's `noset' row; A:set's `acc set res' shows that channel live).  A NOP has
+      no observable effect and is not claimed.
+  the first refusal announces once, naming the full value -- every R class, T2 (0x3; then 5 and a wide value silent),
+      P1 and P2 (beside #549's selector announce), F (free-running: fatal() prints where debug() would not)
+  an accepted command is stored and runs -- NOP (A:nop, L), SET_RESOLUTION (A:set, L: the resize line),
+      GET_RESOLUTION (A:get, L, C), at every width (A: sd, sh, sb; L: sw), with the latch clear (A) and set (L)
+  every session survives and exits 0 -- `sessions clean', pinned to the literal 22
+Measured (regress/artifacts/fbctrlcmdkill/): kill table 2 re-ran every mutant built -- 25 -- on this 99-row probe, and
+every one is red (killtable2_20261019/): the gate removed (the pre-#567 arm, 38/99), the compare narrowed to 32 bits, to
+`int' or made signed, its bound moved down by one, two and three or up by one, its operand swapped for the resident
+cell, the gate qualified by width (byte and halfword escaping, or every non-word access refused), the latch shared,
+never set, set by an accept, or bypassed for wide values once set, the announce demoted to debug() or its argument
+truncated, the refused value stored, the port test dropped, a NOP or a SET refused alone, the dispatch hoisted out of
+the store branch, made unconditional on the port, or added to the read path, and the read path falling into the store
+branch.  Tables 1, 1b and 2a (killtable1_20261018/, killtable1b_20261018/, killtable2a_20261019/) measured them on the
+95-row v1, where three escaped -- the reason this probe has 99 rows.
+On a dead binary 15 rows read green -- the eleven `noset' rows and four announce counts, which read 0 on a session that
+never started; `acc set res' and `sessions clean' are among the red -- so gate 16 requires FBCMD_CONTROL=OK, pins the
+score by equality and checks every row by name (kill table 2's null media).
+NOT CLAIMED (disclosed).  (0) The latch SET crossed with a wide ALIAS of an accepted command (w0-w2): T2's third
+refusal is a wide non-alias (0x100000005), which pins the latch-set x wide cell; an edit exempting only the aliases of
+0-2 once the latch is set is a value carve-out, (2).  (1) A refusal that STORES a value aliasing the previous COMMAND:
+w2 truncates to 2 and its `cmd' row cannot vary; ten classes and T2 pin the store (table 2, D8).  (2) Values and bits
 not listed: the compare is relational, so its generating set is its regions, held at their edges; single-bit coverage
-like #549's session B is not claimed.  (3) A second fbctrl instance (#549's fbctrltwoinst, filed): warned_cmd is per
-device and the probe drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5) fbctrl_command()'s
-default:, kept as a tripwire: unreachable while the arm refuses, so no row reaches it on the fixed device.
+like #549's session B is not claimed, and an edit refusing every listed value but exempting one unlisted (`&& idata
+!= 6') passes.  (3) A second fbctrl instance (#549's fbctrltwoinst, filed): warned_cmd is per device and the probe
+drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5) fbctrl_command()'s default:, kept as a
+tripwire: unreachable while the arm refuses, so no row reaches it on the fixed device.  (6) A 16-BYTE store: testppc's
+stvx/stvxl reach this arm with len 16, and memory_readmax64() keeps 64 bits, so a 128-bit value whose low half is 0, 1
+or 2 is accepted -- the device never sees the rest.  This MIPS probe cannot issue one; filed with #549's PORT arm, which
+shares it, as fbctrlvec128.
 FILL (3) and COPY (4) are refused because nothing implements them (the header lists them under a TODO); a round that
 implements one moves its rows from the refusal list to the accept list.
 
@@ -88,6 +105,7 @@
 PORT_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
 SMALL_RE = re.compile(r"dev_fb_resize\(\): size too small \(0 x 0\); ignored\.")
 UNIMPL_RE = re.compile(r"fbctrl_command: Unimplemented command")
+RES_RE = re.compile(r"\[ dev_fbctrl: changing resolution to ")   # a debug() line: prints while stepping
 REG = dict(zr=0, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15, s0=16, s1=17, s2=18, s3=19, s4=20, s5=21,
            s6=22, s7=23)
 OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)
@@ -247,13 +265,14 @@
             st = None
     code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
     cmd = CMD_RE.findall(buf)
-    print("  session %-6s %-9s steps=%d/%d exit=%s cmd_once=%d port_once=%d small=%d unimpl=%d" % (
+    print("  session %-6s %-9s steps=%d/%d exit=%s cmd_once=%d port_once=%d small=%d res=%d unimpl=%d" % (
         label, status, steps, len(prog), code, len(cmd), len(PORT_RE.findall(buf)), len(SMALL_RE.findall(buf)),
-        len(UNIMPL_RE.findall(buf))))
+        len(RES_RE.findall(buf)), len(UNIMPL_RE.findall(buf))))
     for b in badis:
         print("      DISASSEMBLY MISMATCH: %s" % b)
     return {"status": status, "exit": code, "badis": badis, "vals": vals, "cmd": cmd,
-            "port": len(PORT_RE.findall(buf)), "small": len(SMALL_RE.findall(buf)), "buf": buf}
+            "port": len(PORT_RE.findall(buf)), "small": len(SMALL_RE.findall(buf)),
+            "res": len(RES_RE.findall(buf)), "buf": buf}
 
 
 RESULTS, CONTROL = [], [True]
@@ -274,7 +293,11 @@
     return "alive" if S["status"] == "SURVIVED" and S["exit"] == 0 else "%s/%s" % (S["status"], S["exit"])
 
 
+ALL = []
+
+
 def track(S):
+    ALL.append(S)
     if S["badis"]:
         CONTROL[0] = False
     return S
@@ -318,19 +341,20 @@
     row("ref %s x1" % name, hx(S["vals"].get("t3")), "0x7b", "X1 keeps 123 (a GET would zero it)")
     row("ref %s y1" % name, hx(S["vals"].get("t4")), "0x4d", "Y1 keeps 77")
     row("ref %s once" % name, ",".join(S["cmd"]) or "-", "0x%x" % shown, "one announce, the full value")
-    row("ref %s nosmall" % name, S["small"], 0, "no resize attempted")
+    row("ref %s noset" % name, S["res"], 0, "no SET ran: no resolution-change line")
 
-A0 = track(session("A:nop", SEED + [put("zr")] + READ3, BASE_REGS, ["t2", "t3", "t4"], stub))
-row("acc nop cmd", hx(A0["vals"].get("t2")), "0x0", "NOP is stored: COMMAND reads 0")
+A0 = track(session("A:nop", SEED + [put("zr", "sd")] + READ3, BASE_REGS, ["t2", "t3", "t4"], stub))
+row("acc nop cmd", hx(A0["vals"].get("t2")), "0x0", "NOP by sd is stored: COMMAND reads 0")
 row("acc nop x1", hx(A0["vals"].get("t3")), "0x7b", "NOP touches nothing else")
 row("acc nop quiet", len(A0["cmd"]), 0, "no command announce")
-A1 = track(session("A:set", [sel("zr"), put("s1"), get("t2")], BASE_REGS, ["t2"], stub))
-row("acc set cmd", hx(A1["vals"].get("t2")), "0x1", "SET_RESOLUTION is stored")
+A1 = track(session("A:set", [sel("zr"), put("s1", "sh"), get("t2")], BASE_REGS, ["t2"], stub))
+row("acc set cmd", hx(A1["vals"].get("t2")), "0x1", "SET_RESOLUTION by sh is stored")
 row("acc set ran", A1["small"], 1, "dev_fb_resize() ran: `size too small (0 x 0)` once")
+row("acc set res", A1["res"], 1, "the SET's resolution-change line prints while stepping: the noset channel")
 row("acc set quiet", len(A1["cmd"]), 0, "no command announce")
-A2 = track(session("A:get", [sel("s1"), put("t5"), sel("s2"), put("t6"), sel("zr"), put("s2")] + READ3,
+A2 = track(session("A:get", [sel("s1"), put("t5"), sel("s2"), put("t6"), sel("zr"), put("s2", "sb")] + READ3,
                    BASE_REGS, ["t2", "t3", "t4"], stub))
-row("acc get cmd", hx(A2["vals"].get("t2")), "0x2", "GET_RESOLUTION is stored")
+row("acc get cmd", hx(A2["vals"].get("t2")), "0x2", "GET_RESOLUTION by sb is stored")
 row("acc get x1", hx(A2["vals"].get("t3")), "0x0", "and runs: X1 123 -> 0")
 row("acc get y1", hx(A2["vals"].get("t4")), "0x0", "and Y1 77 -> 0")
 row("acc get quiet", len(A2["cmd"]), 0, "no command announce")
@@ -346,16 +370,20 @@
 row("latch set ran", L["small"], 1, "and still runs (the resize line once)")
 row("latch once", ",".join(L["cmd"]) or "-", "0x3", "one command announce in the session")
 
-M1 = track(session("M1", [sel("zr"), put("s2"), sel("s1"), put("t5"), sel("zr"), get("t2"), sel("s1"), get("t3")],
-                   BASE_REGS, ["t2", "t3"], stub))
+M1 = track(session("M1", [sel("zr"), put("s2"), sel("s1"), put("t5"), sel("zr"), get("t2"), get("t4"),
+                          sel("s1"), get("t3"), get("t6")],
+                   BASE_REGS, ["t2", "t4", "t3", "t6"], stub))
 row("rdcmd val", hx(M1["vals"].get("t2")), "0x2", "a read of COMMAND returns it")
+row("rdcmd again", hx(M1["vals"].get("t4")), "0x2", "and a second read still does: a read stores nothing")
 row("rdcmd noexec", hx(M1["vals"].get("t3")), "0x7b", "and does not execute it (X1 keeps 123)")
+row("rdx1 again", hx(M1["vals"].get("t6")), "0x7b", "X1 read twice: a read stores nothing")
 M2 = track(session("M2", [sel("s3"), put("s3"), get("t2")], BASE_REGS, ["t2"], stub))
 row("x2 three", hx(M2["vals"].get("t2")), "0x3", "3 at X2 is ordinary storage")
 row("x2 quiet", len(M2["cmd"]), 0, "no command announce")
 
-T2 = track(session("T2", [sel("zr"), put("s3"), put("s5"), get("t2")], BASE_REGS, ["t2"], stub))
-row("two once", ",".join(T2["cmd"]) or "-", "0x3", "two refusals, one announce, the first value")
+T2 = track(session("T2", [sel("zr"), put("s3"), put("s5"), put("s7", "sd"), get("t2")],
+                   BASE_REGS + [("s7", 0x100000005)], ["t2"], stub))
+row("two once", ",".join(T2["cmd"]) or "-", "0x3", "3, 5, then sd 0x100000005 with the latch set: one announce")
 row("two cmd", hx(T2["vals"].get("t2")), "0x0", "COMMAND keeps its power-on 0")
 P1 = track(session("P1", [sel("s6"), put("s4"), get("t2")], BASE_REGS, ["t2"], stub))
 row("p1 port", P1["port"], 1, "the refused selector announced once")
@@ -368,6 +396,9 @@
 row("free alive", F["status"], "SURVIVED", "free-running past the refusal to the anchor")
 row("free once", ",".join(F["cmd"]) or "-", "0x3", "fatal() prints while free-running (debug() would not)")
 
+row("sessions clean", sum(1 for S in ALL if S["status"] == "SURVIVED" and S["exit"] == 0), 22,
+    "all 22 sessions ran to the end and exited 0")
+
 try:
     os.unlink(stub)
 except OSError:
```

## B. The repair -- gate 16's block v1 -> v2 (`regress/gate_mips_folds.sh`), the whole diff

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlcmdkill/pass2_20261018/frozen/gate16_block567.txt
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlcmdkill/pass2_20261018/f2/frozen/gate16_block567_v2.txt
@@ -6,14 +6,32 @@
 #  value before the store (COMMAND keeps its value, nothing runs) and announces once per device.
 #  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd/lw on an unmodified testmips, like the
 #  #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is its header.
-#  Kill table 1 (regress/artifacts/fbctrlcmdkill/killtable1_20261018/) built eleven edits, each
-#  red, and two null media: on a binary that runs nothing, 15 absence rows read green and the
-#  record still parses -- so this block requires CONTROL=OK and pins the score by EQUALITY.
-#  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate: recorded, not hidden.
+#  Kill table 2 (regress/artifacts/fbctrlcmdkill/killtable2_20261019/) re-ran all 25 mutants built
+#  for this round on its 99 rows -- every one red -- and two null media: on a binary that runs
+#  nothing, 15 absence rows read green and the record still parses, so this block requires
+#  CONTROL=OK, pins the score by EQUALITY, and checks EVERY row by name (pass 2: a row swapped for
+#  an unrelated unique green one keeps every count).
+#  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate.  That is debt, not a
+#  fit: pass 2 asked that it not be called fine (Grok 4.7), and that the split land before a third
+#  device probe enters this gate (GLM 5.3).
 #  The probe prints a row's status AFTER got/want, unlike the #549 probe, so every row count below
-#  uses one anchored pattern, FCROW; it counted 95 rows in each of kill table 1's fourteen logs.
+#  uses one anchored pattern, FCROW; it counts 99 rows in each of kill table 2's 28 logs.
 FCLOG=$LOGDIR/fbctrl_cmd_probe.log
 FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
+FCNAMES=("live" "devsig" "ref 3 alive" "ref 3 cmd" "ref 3 x1" "ref 3 y1" "ref 3 once" "ref 3 noset"
+         "ref 4 alive" "ref 4 cmd" "ref 4 x1" "ref 4 y1" "ref 4 once" "ref 4 noset" "ref sb3 alive"
+         "ref sb3 cmd" "ref sb3 x1" "ref sb3 y1" "ref sb3 once" "ref sb3 noset" "ref sh4 alive" "ref sh4 cmd"
+         "ref sh4 x1" "ref sh4 y1" "ref sh4 once" "ref sh4 noset" "ref 5 alive" "ref 5 cmd" "ref 5 x1"
+         "ref 5 y1" "ref 5 once" "ref 5 noset" "ref m1w alive" "ref m1w cmd" "ref m1w x1" "ref m1w y1"
+         "ref m1w once" "ref m1w noset" "ref w3 alive" "ref w3 cmd" "ref w3 x1" "ref w3 y1" "ref w3 once"
+         "ref w3 noset" "ref w0 alive" "ref w0 cmd" "ref w0 x1" "ref w0 y1" "ref w0 once" "ref w0 noset"
+         "ref w1 alive" "ref w1 cmd" "ref w1 x1" "ref w1 y1" "ref w1 once" "ref w1 noset" "ref w2 alive"
+         "ref w2 cmd" "ref w2 x1" "ref w2 y1" "ref w2 once" "ref w2 noset" "ref m1d alive" "ref m1d cmd"
+         "ref m1d x1" "ref m1d y1" "ref m1d once" "ref m1d noset" "acc nop cmd" "acc nop x1" "acc nop quiet"
+         "acc set cmd" "acc set ran" "acc set res" "acc set quiet" "acc get cmd" "acc get x1" "acc get y1"
+         "acc get quiet" "latch get x1" "latch nop cmd" "latch set cmd" "latch set ran" "latch once"
+         "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three" "x2 quiet" "two once" "two cmd"
+         "p1 port" "p1 cmd" "p2 cmd" "p2 port" "free alive" "free once" "sessions clean")
 fcrc=0
 python3 -u fbctrl_cmd_probe.py "$PMAX" > "$FCLOG" 2>&1 || fcrc=$?
 if [ "$(grep -cx 'FBCMD_DONE' "$FCLOG")" != "1" ] ||
@@ -32,8 +50,8 @@
     check "fbctrl command probe exit 0 (nonzero: a crash or a red row)" "$fcrc" "0"
     fcres=$(sed -n 's/^FBCMD_RESULT=//p' "$FCLOG")
     #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin (as #549's).
-    check "fbctrl_cmd rows run" "${fcres#*/}" 95
-    check "fbctrl_cmd rows correct" "${fcres%/*}" "95"
+    check "fbctrl_cmd rows run" "${fcres#*/}" 99
+    check "fbctrl_cmd rows correct" "${fcres%/*}" "99"
     check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
     #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
     check "fbctrl_cmd rows emitted match the trailer total" \
@@ -43,5 +61,11 @@
     check "fbctrl_cmd row names are unique" \
           "$(grep -E "${FCROW}(ok|FAIL)  " "$FCLOG" | sed -E 's/^  (.*[^ ]) +got=.*/\1/' |
              sort | uniq -d | wc -l)" "0"
+    #  And EVERY expected row by NAME, green exactly once: counts and uniqueness cannot tell an expected
+    #  row from an unrelated unique one put in its place (pass 2, GPT-6 Astra).
+    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 99
+    for v in "${FCNAMES[@]}"; do
+        check "  fbctrl_cmd row: $v" "$(grep -cE "^  ${v} +got=[^ ]* +want=[^ ]* +ok  " "$FCLOG")" "1"
+    done
 fi
 
```

## C. Kill table 2a -- the unbuilt mutants, measured on v1 (`killtable2a_20261019/KILLTABLE2A_VS_PRETABLE.out`)

```
#567 fbctrlcmdkill -- KILL TABLE 2a against PRETABLE_ADDENDUM_t2a.out (mtime 05:16:47; the table ran 05:17:52-05:24:14,
SCORES.txt; same frozen 95-row instrument as tables 1/1b, md5 be58950a...; the clone restored to the fix, both parts,
sentinel cleared).  Written 2026-10-19 ~05:3x from the logs in this directory.

mutant          predicted                                           measured                         verdict
E6_readdisp     23 red -> 72/95 (ref * x1/y1, rdcmd noexec)         70/95: those 23 + `acc set ran'  KILLED; 2 rows more
                                                                    and `latch set ran' (2 each)     than predicted
E7_anyport      24 red -> 71/95                                     71/95, the same 24 rows           HELD EXACTLY
E8_latchpre     11 red -> 84/95 (ref * once)                        84/95, the same 11 rows           HELD EXACTLY
E9_argtrunc     5 red -> 90/95 (the five wide once rows)            90/95, the same 5 rows            HELD EXACTLY
E10_operand     36/95 (nothing refused; scores as B_gateoff)        36/95                             HELD EXACTLY
E11_intcast     17 red -> 78/95                                     78/95, the same 17 rows           HELD EXACTLY
E12_elseif      ESCAPE 95/95 (Grok predicted `rdcmd val' red)       95/95, rc 0                       ESCAPE -- as this
                                                                                                      addendum predicted
E13_lenne4      ESCAPE 95/95                                        95/95, rc 0                       ESCAPE
E14_latchwide   ESCAPE 95/95                                        95/95, rc 0                       ESCAPE

E6's two extra rows: in A:set and in L the session READS COMMAND after its SET, and under E6 that read re-runs the SET,
so the `size too small (0 x 0)' line prints twice.  The prediction traced only the GET re-runs.

THE THREE ESCAPES ARE THE CELLS PASS 2 NAMED, NOW MEASURED, ON THE UNSHIPPED INSTRUMENT (so L1, pre-ship construction):
  E12 -- the DIRECTION cell's channel: M1 reads COMMAND once and X1 once, and a read that STORES (0, after returning
         the value) is invisible to a single read.  The repair reads each twice.
  E13 -- the ACCEPT side across widths: every accepted COMMAND write is a `sw', so a refusal grown to every non-word
         access refuses no accept the probe makes.  The de-escalation clause owes the accept rows; the repair moves
         A:nop to `sd', A:set to `sh' and A:get to `sb' (L keeps `sw').
  E14 -- the latch SET crossed with a WIDE value: no session refuses a wide value after a first refusal.  The house
         grading puts that joint under clause (e) (`#549''s latch x bit), but it is closable at no row cost and the
         escape is a measured delta: T2 gains a third refusal, `sd 0x100000005', with the latch set.
```

## D. Kill table 2 -- all 25 mutants on v2 (`killtable2_20261019/KILLTABLE2_VS_PRETABLE.out`)

```
#567 fbctrlcmdkill -- KILL TABLE 2 against PRETABLE_ADDENDUM_t2.out (mtime 05:27:37; the table ran 05:28:08-05:45:24,
SCORES.txt).  INSTRUMENT: probe v2, 99 rows (probe.v2.frozen.py.txt, md5 31d85336...; built by mk_probe_v2.py.txt from
the 95-row shipped-candidate probe).  BASELINE: the fix, 99/99 (base.raw).  Its legs before the table: the fix 99/99,
HEAD's binary 38/99 (v2leg_FIX.out, v2leg_HEAD.out).  The clone restored to the fix, both clearance parts, sentinel cleared.

RESULT: ALL 25 MUTANTS RED -- tables 1, 1b and 2a's, re-run on the new instrument -- and both null media red (15/99,
CONTROL=FAILED).  The three table-2a escapes are killed by the rows their repairs added.

mutant        v1 (95 rows)   v2 (99 rows)      mutant        v1 (95 rows)   v2 (99 rows)
B_gateoff     36             38                E3_setref     90             93
D1_u32        88             91                E4_hoist      73             77
D2_gt1        64 (FAILED)    67 (FAILED)       E5_signed     90             93
D3_gt0        60 (FAILED)    62 (FAILED)       E6_readdisp   70             72
D4_ge0        60 (FAILED)    62 (FAILED)       E7_anyport    71             74
D5_len4       85             88                E8_latchpre   84             88
D6_shared     93             97                E9_argtrunc   90             94
D7_debug      94             98                E10_operand   36             38
D8_store      84             88                E11_intcast   78             80
D9_anyport    55 (FAILED)    58 (FAILED)       E12_elseif    95 ESCAPED     97
D10_nolatch   94             98                E13_lenne4    95 ESCAPED     89
E1_gt3        76             79                E14_latchwide 95 ESCAPED     97
E2_nopref     92             96                null media    15 (FAILED)    15 (FAILED)
((FAILED) = FBCMD_CONTROL=FAILED; every v1 score is from tables 1, 1b and 2a, every v2 score from this table.)

PREDICTIONS
* every mutant red .............................................................. HELD
* E12: rdcmd again, rdx1 again -> 97/99 ........................................ HELD EXACTLY
* E13: the ten A-session rows -> 89/99 .......................................... HELD EXACTLY
* E14: two once, two cmd, sessions clean -> 96/99 ............................... MISSED ONE ROW: 97/99 -- `two once'
  stays green, because the one announce (0x3) prints before T2 dies in default: on the third write.  `two cmd' and
  `sessions clean' (21) are red; the kill holds.
* sessions clean red exactly under B_gateoff, D5, E1, E5, E10, E11, E14 ............ HELD EXACTLY (9, 20, 17, 21, 9,
  20, 21; 22 under the other eighteen; 0 on both null media)
* ref w1 noset red under B_gateoff and D1 ........................................ HELD, and INCOMPLETE: it is also red
  under E10 and E11, where w1 is likewise stored as 1 and SET_RESOLUTION runs -- the channel `nosmall' lacked
* null media: CONTROL=FAILED, 15/99, `acc set res' and `sessions clean' red ......... HELD EXACTLY

THE NEW CHANNEL, SHOWN LIVE AND MEASURED: `acc set res' reads 1 on the fix (the SET's resolution-change debug() line
prints while stepping), and `ref w1 noset' reads 1 wherever SET runs in R:w1 -- B_gateoff, D1, E10, E11.  The v1 row in
its place, `ref w1 nosmall', read 0 under all four (pass 2: GPT-6 Astra Q5, Grok 4.7's first FLAG).
```

## E. The v2 gate block replayed on every table-2 log (`wiring_20261019/GATE16_REPLAY_v2.out`)

```
#567 gate 16 v2 block REPLAYED offline, 2026-10-19 05:47:56: the block's own lines from regress/gate_mips_folds.sh (FCROW= .. fi, minus the probe launch and its fcrc=0 initializer), sourced with a stub check() against every kill-table-2 log, fcrc = that leg's recorded exit status; then four hand-made negative controls.
B_gateoff          fcrc=1 checks=109 red=64  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 61]
C_absent           fcrc=1 checks=109 red=88  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 84]
C_bintrue          fcrc=1 checks=109 red=88  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 84]
D10_nolatch        fcrc=1 checks=109 red=4  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 1]
D1_u32             fcrc=1 checks=109 red=11  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 8]
D2_gt1             fcrc=1 checks=109 red=36  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 32]
D3_gt0             fcrc=1 checks=109 red=41  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 37]
D4_ge0             fcrc=1 checks=109 red=41  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 37]
D5_len4            fcrc=1 checks=109 red=14  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 11]
D6_shared          fcrc=1 checks=109 red=5  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 2]
D7_debug           fcrc=1 checks=109 red=4  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 1]
D8_store           fcrc=1 checks=109 red=14  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 11]
D9_anyport         fcrc=1 checks=109 red=45  fbctrl command probe controls;fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl [named-row reds: 41]
E10_operand        fcrc=1 checks=109 red=64  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 61]
E11_intcast        fcrc=1 checks=109 red=22  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 19]
E12_elseif         fcrc=1 checks=109 red=5  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 2]
E13_lenne4         fcrc=1 checks=109 red=13  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 10]
E14_latchwide      fcrc=1 checks=109 red=5  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 2]
E1_gt3             fcrc=1 checks=109 red=23  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 20]
E2_nopref          fcrc=1 checks=109 red=6  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 3]
E3_setref          fcrc=1 checks=109 red=9  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 6]
E4_hoist           fcrc=1 checks=109 red=25  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 22]
E5_signed          fcrc=1 checks=109 red=9  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 6]
E6_readdisp        fcrc=1 checks=109 red=30  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 27]
E7_anyport         fcrc=1 checks=109 red=28  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 25]
E8_latchpre        fcrc=1 checks=109 red=14  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 11]
E9_argtrunc        fcrc=1 checks=109 red=8  fbctrl command probe exit 0 (nonzero: a crash or a red row);fbctrl_cmd rows correct;fbctrl_cmd rows failed [named-row reds: 5]
base               fcrc=0 checks=109 red=0   [named-row reds: 0]
neg_duprow.log     fcrc=0 checks=109 red=3  fbctrl_cmd row names are unique [named-row reds: 2]
neg_nodone.log     fcrc=0 checks=1 red=1  fbctrl command probe output parses [named-row reds: 0]
neg_rowgone.log    fcrc=0 checks=109 red=3  fbctrl_cmd rows emitted match the trailer total;fbctrl_cmd ok rows match the trailer count [named-row reds: 1]
neg_substituted.log fcrc=0 checks=109 red=1   [named-row reds: 1]
neg_nodone = base.raw without FBCMD_DONE; neg_rowgone = without 'ref 3 x1'; neg_duprow = 'ref 4 cmd' renamed 'ref 3 cmd'; neg_substituted = 'ref 4 cmd' renamed 'ref 4 cmdX' (an unrelated unique name, every count intact).
GATE16_REPLAY_V2_DONE
```

## F. The FIX -- unchanged since pass 2 (`src/devices/dev_fbctrl.c`, the whole diff against HEAD)

```diff
diff --git a/src/devices/dev_fbctrl.c b/src/devices/dev_fbctrl.c
index eab10df8..2013d66e 100644
--- a/src/devices/dev_fbctrl.c
+++ b/src/devices/dev_fbctrl.c
@@ -50,6 +50,7 @@ struct fbctrl_data {
 	int		current_port;
 	int		port[DEV_FBCTRL_NPORTS];
 	int		warned_port;	/* #549: the refused-selector announce */
+	int		warned_cmd;	/* #567: the refused-command announce */
 };
 
 
@@ -98,6 +99,9 @@ static void fbctrl_command(struct cpu *cpu, struct fbctrl_data *d)
 
 	/*  TODO: Block copy and fill.  */
 
+	/*  #567: unreachable while the DATA arm refuses every command
+	    other than these three; kept as a tripwire for a later edit
+	    that lets one in, as #549 kept the selector's.  */
 	default:fatal("fbctrl_command: Unimplemented command %i.\n", cmd);
 		exit(1);
 	}
@@ -146,7 +150,24 @@ DEVICE_ACCESS(fbctrl)
 
 		if (writeflag == MEM_READ)
 			odata = d->port[d->current_port];
-		else {
+		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
+		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
+			/*  #567: a command other than NOP, SET_RESOLUTION and
+			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
+			    keeps its previous value and nothing executes.  It used
+			    to reach fbctrl_command()'s default: and end the
+			    emulator, FILL (3) and COPY (4) included -- the header
+			    names them under a TODO and gives them no ports.  The
+			    compare is on all 64 bits: the cell is an int, so a
+			    wide 0x100000001 used to be stored as 1 and run
+			    SET_RESOLUTION.  Announced once per device.  */
+			if (!d->warned_cmd) {
+				fatal("[ fbctrl: command 0x%llx is not supported; "
+				    "the command port is unchanged (once) ]\n",
+				    (unsigned long long) idata);
+				d->warned_cmd = 1;
+			}
+		} else {
 			d->port[d->current_port] = idata;
 			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
 				fbctrl_command(cpu, d);
```

## G. F1's three sites, verbatim (numbered from each file's line 1)

```c
/* src/cpus/cpu_ppc_instr.c */
3872: X(stvx)
3873: {
3874: 	uint8_t data[16];
3875: 	MODE_uint_t addr = reg(ic->arg[1]) + reg(ic->arg[2]);
3876: 	int rs = ic->arg[0];
3877: 	uint64_t hi = cpu->cd.ppc.vr_hi[rs], lo = cpu->cd.ppc.vr_lo[rs];
3878: 
3879: 	data[0] = hi >> 56;
3880: 	data[1] = hi >> 48;
3881: 	data[2] = hi >> 40;
3882: 	data[3] = hi >> 32;
3883: 	data[4] = hi >> 24;
3884: 	data[5] = hi >> 16;
3885: 	data[6] = hi >> 8;
3886: 	data[7] = hi;
3887: 	data[8] = lo >> 56;
3888: 	data[9] = lo >> 48;
3889: 	data[10] = lo >> 40;
3890: 	data[11] = lo >> 32;
3891: 	data[12] = lo >> 24;
3892: 	data[13] = lo >> 16;
3893: 	data[14] = lo >> 8;
3894: 	data[15] = lo;
3895: 
3896: 	cpu->memory_rw(cpu, cpu->mem, addr, data,
3897: 	    sizeof(data), MEM_WRITE, CACHE_DATA);
3898: }

/* src/core/memory.c */
53:  *  This function should not be called with cpu == NULL.
54:  */
55: uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
56: {
57: 	int i, byte_order = cpu->byte_order;
58: 	uint64_t x = 0;
59: 
60: 	if (len & MEM_PCI_LITTLE_ENDIAN) {
61: 		len &= ~MEM_PCI_LITTLE_ENDIAN;
62: 		byte_order = EMUL_LITTLE_ENDIAN;
63: 	}
64: 
65: 	/*  Switch byte order for incoming data, if necessary:  */
66: 	if (byte_order == EMUL_BIG_ENDIAN)
67: 		for (i=0; i<len; i++) {
68: 			x <<= 8;
69: 			x |= buf[i];
70: 		}
71: 	else
72: 		for (i=len-1; i>=0; i--) {
73: 			x <<= 8;
74: 			x |= buf[i];
75: 		}
76: 

/* src/include/testmachine/dev_fb.h */
15: #define	DEV_FBCTRL_ADDRESS		0x12f00000
16: #define	DEV_FBCTRL_LENGTH		      0x20
24: #define	DEV_FBCTRL_PORT			      0x00
25: #define	DEV_FBCTRL_DATA			      0x10

/* src/machines/machine_test.c (testppc calls default_test(), which installs fbctrl at its line 337) */
440: MACHINE_SETUP(testppc)
441: {
442: 	machine->machine_name = strdup("PPC test machine");
443: 
444: 	default_test(machine, cpu);
445: }
```
