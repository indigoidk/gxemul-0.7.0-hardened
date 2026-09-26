# #549 fbctrlportkill -- THE §F2 ADJUDICATION PASS: every seat's pass-2 findings, my disposition on each

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree is `GXEMUL-SEC/` (ignore any other `src/`).  **FIRST LINE:**
`VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  **The load-bearing question: WHICH OF MY
DISPOSITIONS BELOW IS WRONG?  Name the count.**  If you raised a finding, be HARDER on it than on anyone else's --
including whether the FIX I propose for it is right.  If you cannot read files, everything you need is inlined.

## SETTLED PREMISES (re-inlined; do not re-derive)

* **`fatal()` PRINTS AND RETURNS; only an explicit `exit(1)` ends the process** (`src/core/debugmsg.c`: `fatal()` has no
  early-out and no exit; the DATA arm is `fatal(...); exit(1);`).  The pass-2 brief failed to restate this, and deepseek's
  DO NOT SHIP rested on it -- the defect was the BRIEF's, not the seat's.
* The fix: the PORT arm refuses `idata >= 8` on the full `uint64_t`, keeps the previous selector, announces once per
  device (`warned_port`, `(once)` marker); the DATA arm's check and `exit(1)` are kept as a tripwire.  Unanimous in pass 1.
* Kill table 2: 25 variants, 22 red, `M_revert` (HEAD's arm) 25/41, `M_static` and `M_noguard` 41/41 (disclosed).
* Gates on the working tree: gate 16 PASS (23 checks), gate 4 PASS (6), gate 6 PASS (36) with the re-derived pins.
* The command default and the offset default still end the process; they are out of scope and filed.

## PASS-2 SEATS (panel_20260924_113037 + dedicated jobs; durable copies under panels/)

agy, grok, glm, codex (panel), codex (dedicated), grok (dedicated), Opus 5 (measuring, 14 new variants BUILT):
SHIP WITH CHANGES.  minimax: SHIP.  deepseek: DO NOT SHIP (see D1).  kimi: DOWN on both transports (CLI weekly wall;
`kimi-k3:cloud` HTTP 502, re-fired).

## FINDINGS AND MY DISPOSITIONS

**R -- records (false or overstated sentences), all FIX before commit (L4):**
* R1 (grok x2, codex dedicated, agy): the history sentences in `dev_fbctrl.c` and the gate-16 comment say every
  out-of-range store ended the process at the next DATA access.  FALSE for wide values: HEAD stores `(int)idata`, so
  `0x100000003` became port 3 and `0x200000000` port 0 and were SERVICED (`table2/M_revert.raw`).  -> rewrite both to the
  stored-int scope: "a selector whose int conversion is out of range (e.g. `sw 9`) ...".
* R2 (grok, codex dedicated): "every machine installs ONE fbctrl" -> "the probe's `-E testmips` session has one fbctrl".
  AND codex (dedicated) says a second instance IS reachable without adding a device: two unmodified machines in one
  process via a config file (`emul_add_machine`).  -> disclose it as the untested route rather than claim impossibility;
  FILE a two-machine latch row (`fbctrltwoinst`).
* R3 (Opus, grok): the gate comment and the probe contract cite "kill table 1: 20 of 20" -> cite table 2.
* R4 (codex dedicated): "every row fails only on its own value" is still false -- register reads happen only after the
  whole session survives, so a later death blanks earlier rows -> reword to "no row inherits another row's selector".
* R5 (codex dedicated): session F's text says a refused write "then `continue`" -- the write executes INSIDE `continue`
  -> reword.  And the debug()-suppression explanation holds for this invocation's verbosity (`-V`, no `-v`); say so.
* R6 (grok): "those are filed" is true only if the two filings land in the SAME commit -> they will
  (`fbctrlcmdkill` HIGH, `fbctrloffkill` MED, drafted).

**P -- probe/gate apparatus:**
* P1 (Opus measured, grok): the probe exits 0 on a red score, so the "probe exit status" row fires only on a Python
  crash -> make `main()` exit 1 unless CONTROL is OK and every row is green; keep the row.
* P2 (grok dedicated): the gate's NUMERATOR pin is quoted (`"41"`), so `check_score_claims.py` watches only the
  denominator -> DISPOSITION: leave the pin form alone (the checker's rule is the one-token unquoted DENOMINATOR, by
  design); P1 makes the exit row a second catcher of a red score.  Tell me if that is wrong.
* P3 (codex, grok, deepseek): probe self-edits (`ok = True`, a constant 8 -> 9) keep every pin green -> DISCLOSED as
  "edits to the instrument's own logic are reviewed, not rowed" (the house form, cf. #548's fbharnessedits); not rowed.

**D -- device edits outside table 2 that score 41/41 (BUILT by Opus or derived by the grok/codex seats):**
Rows owed per ENUMERATED edit.  I propose adding these rows now (L1: the detector is pre-ship), no new oracle:
* D2 (grok ded.): mask bit 63 before the compare -> add `refuse 0x8000000000000005 (sd), PORT keeps 5`.
* D3 (grok ded.): a refusal that stores only when the previous selector is 0 (power-on) -> session F reads PORT back
  after the free-run and requires 0.
* D4 (Opus N_datarearm, grok ded.: latch cleared on a DATA write / inside `fbctrl_command()`) -> in P, a DATA write to
  port 5 AND a NOP command (PORT=0, DATA=0) between two refusals; announce count still 1.
* D5 (Opus N_clobcell / N_clobcmd / N_runcmd: the refusal stores into a port cell or runs a command) -> after the
  refusals, read back every port's DATA cell against a known fill; set X1=123 after a GET_RESOLUTION and require it
  still 123 after a refusal.
* D6 (grok ded.: PORT read ORs bit 32) -> one `ld` of PORT requiring exactly 5.
* D7 (codex ded., grok ded.: selector 0 refused for `sb` / for `sd`) -> accept selector 0 via `sb` and via `sd`.
* D8 (codex ded.: `current_port |= 1` in the refusal) -> covered by D5's readback after a refusal from an EVEN
  previous selector: make the "after PORT=7" row a pair, previous 7 AND previous 6.
* D9 (codex ded.: announce only for the value 9; `% 10` re-announce; `serial_nr == 1`) -> the first refusal in P becomes
  8 (not 9) and P does twelve refusals; `serial_nr` joins R2's filed two-machine row.
* D10 (codex ded.: diagnostic prints 0 not the value) -> ONCE_RE requires the refused value `0x9` / `0x8` exactly.
* D11 (codex ded.: GET_RESOLUTION leaves Y1 at 1) -> the signature control reads Y1 too.
* DISCLOSED, not rowed (clause e): an exception for one untested value (`idata != 10`, codex/grok/deepseek -- the value
  space is 2^64; no finite row set closes "except value k"); the DATA check weakened `>=` -> `>` (grok ded.; unreachable
  on a correct PORT arm, the same class as M_noguard); `printf` for `fatal` (codex ded.; indistinguishable in output).
* OUT OF SCOPE (Opus): DATA-path width narrowing -> for the command-default round.
* D1 (deepseek DO NOT SHIP): overruled on the settled premise above.

Then kill table 3 on the revised probe: all 25 table-2 variants plus the D-edits as built variants; predictions first.

## QUESTIONS
1. Which of my dispositions is wrong -- name the count.  Especially: is any D-row NOT owed, is any owed row missing,
   and is P2 (leave the numerator pin quoted) acceptable?
2. Is R2's two-machine route real (a config file with two `-E testmips` machines in one process), and should its row
   be built NOW rather than filed?
3. Anything in these fixes that would itself be wrong once written?
If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
