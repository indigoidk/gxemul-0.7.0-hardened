# #549 fbctrlportkill -- THE CLOSING PASS on the repair the F2 adjudication produced (a repair owes its own pass)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`**; other copies of
GXemul under the project root are not this fork.  If you read files, read ONLY `src/devices/dev_fbctrl.c`,
`src/include/testmachine/dev_fb.h`, `regress/fbctrl_port_probe.py`, `regress/gate_mips_folds.sh`, and this round's
`regress/artifacts/fbctrlportkill_20260924/closing/` and `.../table3/` -- nothing else under `regress/artifacts/`, and
not `tools/pipeline/ledger.json`.  If you cannot read files that is expected: everything you need is inlined, and a
premise you cannot settle from the packet should be NAMED, not guessed.
**VERDICT LINE FIRST**: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. SETTLED PREMISES (re-inlined; do not re-derive)

* **`fatal()` PRINTS AND RETURNS; only an explicit `exit(1)` ends the process** (`src/core/debugmsg.c`: `fatal()` has
  no early-out and no exit).
* **The fix** (unanimous in pass 1, unchanged through pass 2 and F2 except one comment sentence): the PORT arm refuses
  `idata >= 8` compared on the full `uint64_t`, keeps the previous selector, and announces once per device through
  the struct member `warned_port` with the marker `(once)`; the DATA arm's range check and its `exit(1)` are KEPT as a
  tripwire.  The command default (`fbctrl_command()`, any command other than 0-2) and the offset default (any offset
  other than 0x00/0x10) still end the process: OUT OF SCOPE, filed as `fbctrlcmdkill` and `fbctrloffkill`.
* **The §F2 adjudication** (nine seats, the dedicated codex "Astra" and grok jobs, then Fable 5.1 on 8 of 9 seats, then
  a fresh Opus 5.5 seat that MEASURED every corrected row): the detector was changed, the fix was not.  Rulings adopted:
  record reconciliation in the gate (a log with a row deleted passed); the probe exits nonzero on a red row; D2 as
  `sd 0x8000000000000000` after PORT=5 (the proposed `0x8000000000000005` was vacuous: its int conversion IS 5);
  D3 as a guest `lw` of PORT inside the free-run (printing an unloaded GPR was vacuous: cpu_new() zero-fills it); D7
  with a NON-ZERO predecessor before each zero-selector store; D9 with the count sampled after the twelfth refusal;
  D10 keeping the broad announce counter and adding a separate first-value check; D11 NOT owed as a kill row and
  added as a CONTROL extension; the A-silence row and `sd 8` (both measured as the only rows killing their edits); the
  docstring's `r` prefix dropped so the score checker can read it.  **The two-machine config (`gxemul @config` with
  two testmips machines) was MEASURED to work by the Opus seat and ruled FILED by Fable** -- a new launcher with an
  unmeasured console interaction -- as `fbctrltwoinst`; the contract says the latch is per instance by construction
  and untested across two machines.

## 2. WHERE THE NINTH SEAT (Opus, measured) AND THE ADJUDICATOR (Fable) DIFFERED -- my dispositions, for you to check

* `sh 0` accepted after PORT=5: Fable "disclose"; Opus measured that an sh-only edit escapes without the row.
  **ADOPTED as a row**, and the whole width x boundary class CLOSED: pass 2 found a width-conditioned escape (D7) and
  F2 found another (`sd 8`), which is two consecutive passes of one class, so every cell {0, 7 accepted; 8 refused} x
  {sb, sh, sw, sd} is rowed and each new cell has its own one-edit target in the kill table.
* Y1 (D11): **added as a CONTROL** (inside the device-signature control), as Fable ruled, not as a kill row.
* D4 (re-arm by DATA/NOP traffic): **its own session R**, because Opus measured that inside session P an edit accepting
  8 ends the session and blanks fourteen P rows.
* Two-machine: **FILED**, per Fable; Opus's recipe goes into the filing.

## 3. WHAT CHANGED SINCE F2 -- every file, disclosed

    git diff --numstat (vs HEAD f4f601c4), the round's files:
      src/devices/dev_fbctrl.c        18 / 5   INLINED (§4a: only the comment sentence changed since F2)
      regress/fbctrl_port_probe.py    new, 471 lines   INLINED as the diff from the 41-row probe F2 reviewed (§4b)
      regress/gate_mips_folds.sh      55 / 0   INLINED as the diff from the block F2 reviewed (§4c)
      regress/gate_hygiene.sh          2 / 2   NOT SHOWN -- two census pins (74/25), unchanged since pass 2
      tools/pipeline/check_probe_wiring.py, tools/precommit_check.sh -- SUMMARIZED: one MANIFEST line classifying
          fbctrl_port_probe.py as a detector, and SCORE_CLAIMS_MANIFEST 30 -> 31; unchanged since pass 2

## 4. THE REPAIR DIFF
