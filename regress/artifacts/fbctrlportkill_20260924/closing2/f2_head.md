# #549 fbctrlportkill -- THE CLOSING §F2 PASS: every closing-pass finding, my disposition on each, and the repair (measured)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Check the premises, not just the derivations.  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`**;
other copies of GXemul under the project root are not this fork.  If you read files, read ONLY
`src/devices/dev_fbctrl.c`, `src/include/testmachine/dev_fb.h`, `regress/fbctrl_port_probe.py`,
`regress/gate_mips_folds.sh`, and this round's `regress/artifacts/fbctrlportkill_20260924/{closing2,table4,table4b}/`.
If you cannot read files that is expected: everything you need is inlined, and a premise you cannot settle from the
packet should be NAMED, not guessed.  **FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`**, then
numbered findings.  **The load-bearing question: WHICH OF MY DISPOSITIONS BELOW IS WRONG?  Name the count.**  If you
raised a finding, be HARDER on it than on anyone else's, including whether the repair I made for it is right.

## 1. SETTLED PREMISES (re-inlined; do not re-derive)

* `fatal()` PRINTS AND RETURNS; only an explicit `exit(1)` ends the process.
* The fix is unchanged since pass 1 except one comment sentence (narrowed in F2): the PORT arm refuses `idata >= 8` on
  the full `uint64_t`, keeps the previous selector, announces once per device through the struct member `warned_port`
  with the marker `(once)`; the DATA arm's range check and `exit(1)` are KEPT as a tripwire.  The command default and
  the offset default still end the process: out of scope, filed (`fbctrlcmdkill`, `fbctrloffkill`).
* The closing pass (panel_20260925_141420: agy, grok, glm, deepseek, minimax SHIP WITH CHANGES, kimi-k3:cloud SHIP;
  codex WALLED -- usage limit until 2026-09-26 07:01 -- a seat failure; the kimi CLI on its weekly wall, covered) plus
  the dedicated grok job (SHIP WITH CHANGES) and the Opus 5.5 measuring seat (SHIP WITH CHANGES: ten 73/73 escapes
  MEASURED inside the DEPENDS-ON enumeration, one restoring the process exit).
* Owner ruling 2026-09-25: while codex is walled, Fable adjudicates on the seats that answer and Astra confirms after
  the reset; nothing is committed before Astra confirms.

## 2. WHY THE REPAIR IS A CLASS CLOSURE, NOT MORE ROWS

Pass 2 found a width-conditioned escape; F2 found another; the closing pass found edits conditioned on the previous
selector, the COMMAND cell and the read width -- the same class three passes running.  The carrier's rule: when two
consecutive passes find breaches of one class, the next repair ENUMERATES the class from the function's own inputs,
closes every cell in ONE diff, and writes into the contract which cells are covered and which are deliberately not.
So the probe's header is now an ENUMERATION: for each effect (a refusal keeps the selector; the first refusal announces
once and the rest are silent; a PORT read returns the selector; a refusal leaves every cell alone; an accepted selector
is stored) EVERY value of EVERY single axis (width, value class, previous selector 0-7, latch, COMMAND cell, the traffic
between refusals) is held by some row, and joint (two-axis) cells are disclosed as clause (e).

## 3. THE FINDINGS AND MY DISPOSITIONS (each "ROWED" one is MEASURED red in table 4, §5)

* **C1 (Opus E_ref_p1..p4; grok, kimi, grok ded. G1):** refusal skipped or rewritten after selectors 1-4 -> ROWED: V
  reads PORT right after its first refusal (selector 1, COMMAND holding 2); X2 X3 X4 are fresh devices refusing after 2,
  3, 4.
* **C2 (Opus E_ref_cmd -- restores the process exit):** refusal skipped while COMMAND != 0 -> ROWED (V).
* **C3 (Opus E_rd_w4, E_rd_cmd):** PORT read qualified by width / by COMMAND -> ROWED: lb and lh of PORT (W); a PORT
  read with COMMAND holding 2 (V).
* **C4 (Opus E_ann_w4/p1/cmd, E_cmdset; grok ded.):** the announce suppressed by width, previous selector or COMMAND,
  or the latch SET by a command -> ROWED: counts in V (first refusal at selector 1 with COMMAND 2) and W (first refusal
  by sb), and five fresh X devices whose FIRST refusal is by sh/sd/sw/sb/sh after 2/3/4/6/7.
* **C5 (glm; grok ded. G2 G3):** the latch re-armed by a DATA READ, a non-NOP command, GET_RESOLUTION -> ROWED: R's
  traffic between its refusals now includes a DATA read and a GET_RESOLUTION.
* **C6 (glm L1):** a re-announce keyed to a value only W refuses -> ROWED (W's count after its five refusals).
* **C7 (grok ded. G4):** the padding stores (16 by sb/sh) accepted unobserved -> ROWED (P reads both back).
* **C8 (minimax, grok ded. G6):** the announced value truncated to 32 bits -> ROWED: X3's FIRST refusal is
  0x100000003 by sd, and its announce must name that value.
* **C9 (grok ded. G8):** COMMAND's cell cleared only on a refused 8 -> ROWED (V now refuses 8 before reading the cells).
* **C10 (grok ded. G5a, G5b):** the DATA check blinded without deleting it (only `exit(1)` removed; its operand swapped)
  -> DISCLOSED, NOT CLAIMED (2) widened: any edit of the kept check is unreachable while the PORT arm refuses.
* **C11 (grok ded. G7; agy):** joint cells (`ld` sets bit 32 except at selector 5; 3 refused only by sb) -> DISCLOSED,
  NOT CLAIMED (0), new: an edit on TWO axes at once is caught only where a row holds that pair.
* **C12 (agy, deepseek, kimi, glm, grok):** `idata != 10`; a period of twelve -> DISCLOSED, NOT CLAIMED (3), unchanged.
* **C13 (grok):** the gate does not pin row identity (a row replaced by a copy of another keeps every count) ->
  REPAIRED: a row-names-unique check; its fixture MEASURED red only on that check (§5).
* **C14 (grok):** A's "accept selector 0 written by sw" cannot see an ignored store (power-on is 0) -> LIMITS note; the
  cell is held by W's row after PORT=5.
* **C15 (grok, deepseek, minimax):** "each new cell has its own one-edit target" was false -> the targets T_W_sd7,
  T_W_sw8, T_W_sb0 were BUILT (red), and the sentence is replaced by the enumeration.
* **C16 (grok ded., agy, glm):** contract claims true only as measured ("cleared by DATA or command traffic", "a PORT
  read that sets a high bit (by lw and by ld)", "an announce naming another value", "a refusal that writes a port
  cell") -> the contract is REWRITTEN as the enumeration; each claim now names the cells it covers.
* **C17 (grok ded.):** the gate comment's "M_revert ... every refusal row red" was false (V's rows stay green) ->
  rewritten ("51/94 here").  **C18 (deepseek):** "the 8 it discloses" read as exhaustive -> rewritten (14, by category).
* **C19 (the R keeps row; agy/grok keep, grok ded. drop, Opus redundant-but-keep):** KEPT -- with R's traffic now
  including a DATA read and a GET_RESOLUTION it is the keeps-after-command-traffic cell, and Opus's two-part edit
  (R_partAB) reds it (with V's rows).
* **C20 (grok ded.): "R's own session because an edit accepting 8 ends P" is false** -> REJECTED: the header says an
  edit accepting 8 cannot blank P's rows, which is the design reason (R's DATA traffic would end the process inside P
  under M_gt, as the Opus F2 seat measured when D4 sat in P); true as written.

## 4. THE REPAIR DIFF (the closing pass reviewed the 73-row probe; this is 73 -> 94, and the gate block)
