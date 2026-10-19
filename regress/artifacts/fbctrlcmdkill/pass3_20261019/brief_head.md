# `fbctrlcmdkill` (`#567`) -- PASS 3: the repair's own pass.  The detector grew 99 -> 106 -> 123 rows after F2; this pass VERIFIES ITS ENUMERATION

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, its WORKING TREE (nothing of this round is
committed).**  Ignore every other `src/` under the project root (pristine 2021 upstream copies).  The working tree also
carries UNRELATED uncommitted edits (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`regress/diff_wdc_identify.c`, `regress/gate_offline.sh` and others) -- not this round; ignore them.  Frozen copies of
this pass's files are in `regress/artifacts/fbctrlcmdkill/pass3_20261019/frozen/` -- cite those.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.  **Where this brief states an arithmetic claim -- a count of rows, a set of cells
-- ENUMERATE it rather than reasoning about it**, and enumerate the right domain: ask what the producer of a value can
actually emit before walking it.

**VERDICT LINE FIRST**, so your answer survives truncation.  READ-ONLY: write nothing to any project tree.

## Why this pass exists, and what would close it

F2 (the adjudication pass on pass 2) converged three ways -- GPT-6 Astra, Grok 4.7, GLM 5.3 -- on two gaps in the 99-row
detector: WIDTH x BOUND EDGE (the only accepted `sd` was an effect-free NOP; only `sb` and `sw` held both edges of the bound) and
the latch's PERSISTENCE (no refusal after an accept or a read).  The repair is new floor-bound material, so it owes its
own pass (the repair-chain rule).  **Two consecutive passes breached one class -- width -- so by the class-closure
amendment this repair closes the WHOLE class in one diff from an explicit enumeration, and THIS PASS VERIFIES THAT
ENUMERATION rather than hunting cells one at a time.**  It closes on a VALID pass that finds zero floor breaches surviving
adjudication, with the zero carried with its denominator (which cells, which mutant shapes were swept).

The PRODUCT (`src/devices/dev_fbctrl.c`) is UNCHANGED since pass 2.  Only the DETECTOR and its gate block changed.

<<NUMSTAT>>

## SETTLED PREMISES -- recorded resolutions, re-inlined so nobody spends an answer re-deriving them

* **`fatal()` prints and RETURNS** (`src/core/debugmsg.c`'s `fatal()`: no early-out, no exit).  Every refusal row rests
  on it.
* **Pass 1** (`pass1_20261018/ADJUDICATION_p1.md`): member 3 -- refuse every 64-bit DATA value other than 0, 1 and 2 at
  COMMAND BEFORE the store, COMMAND unchanged, one `warned_cmd` latch, one `(once)` announce naming the full value.
* **The witness** (rung 3, unmodified `-E testmips`, HEAD's binary): 2/12; 12/12 on the fix
  (`pass1_20261018/WITNESS_headbin.out`).
* **Pass 2 and F2** (`pass2_20261018/`, `pass2_20261018/f2/F2_DISPOSITIONS.md`, inlined below): all three seats SHIP WITH
  CHANGES at each pass; their findings and my dispositions are in the F2 record.
* **The arm never tests `len`.**  `memory_readmax64(cpu, data, len)` consumes it to build the 64-bit `idata` before the
  switch; nothing after that reads `len` except `memory_writemax64()` on the read path.  So a width-conditioned edit is an
  ADDED test, and it can hide in any cell held at one width only -- which is why the enumeration crosses every partition
  with width.
* **Floor clause (c)** is recorded `(c): measured at <artifact>` or `(c): by construction via <row/pin>, leg not run`;
  for a runtime probe the null medium is an absent or non-emulator binary.
* **Rule D2**: a compare against a constant bound B is pinned by the rows at the bound's two edges -- here 2 (accepted)
  and 3 (refused) -- and a far row never pins the bound.
* **The 16-byte store** (testppc `stvx`/`stvxl`): the callback receives all 16 bytes and `memory_readmax64()` drops the
  prefix before the compare -- disclosed as NOT CLAIMED (6) and filed as `fbctrlvec128` (F2's G3: the earlier wording,
  "the device never sees the rest", was wrong and is corrected).
* **Not fired, by the owner's 2026-10-17 roster:** Opus 5.5, agy, kimi, deepseek, minimax.  Fable 5.1 is tried once per
  pass; it walled at pass 2 and F2 (HTTP 429), recorded as a seat failure and held, never as agreement.
