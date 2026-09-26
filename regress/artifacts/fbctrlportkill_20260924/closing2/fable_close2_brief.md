# #549 -- the CLOSING §F2 ADJUDICATION, flagship seat (Astra, the codex GPT-6 job, confirms after its reset)

Open with `FABLE549C2_ALIVE`, then `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, numbered rulings, and **the
count of my dispositions you change**, under ~1200 words.  READ-ONLY under `C:\DocumentNoSnc\cc\GXEMUL\`; measure only
in WSL `/tmp` if at all.  Owner ruling 2026-09-25: codex (Astra) is walled until 2026-09-26 07:01; you adjudicate on
the seats that answered, Astra confirms after the reset, and nothing is committed before that.

## Evidence (under `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/`)

* `closing2/f2_brief.md` -- the closing pass's findings C1-C20, my dispositions, the 73->94 class closure, table 4.
* The closing-F2 seats: `_scratchpad/panel_20260925_151610/` (agy SHIP; grok, glm, minimax, kimi-k3:cloud SHIP WITH
  CHANGES; deepseek DO NOT SHIP; codex walled; the kimi CLI walled and covered), `panels/grok_dedicated_close2.txt`
  (SHIP WITH CHANGES), and `opus5_close2.md` (the Opus 5.5 measuring seat, SHIP WITH CHANGES: 11 one-axis edits at
  94/94 -- cells 1-7 and COMMAND = 1 as state; C16 wrong).
* The earlier passes, if you need them: `fable5_f2.md`, `opus5_close.md`, `closing/closing_brief.md`.

## What the closing-F2 seats found, converging

* **The enumeration mis-holds a cell it claims (grok, grok ded.; MY OWN DESIGN FLAW):** X3 refuses `0x100000003`
  after selector 3, and that value truncates to 3 as an int -- so a store at selector 3 reads back 3 either way;
  "previous 3" is claimed and not held (`M_store`, `M_revert`, `M_clamp` leave X3's keep row green in table 4).
  C8's wide-value witness vacated C1's selector-3 witness.
* **The value named is unchecked for X7's first refusal, 0x100 (grok ded.).**
* **COMMAND = 1 (SET_RESOLUTION) is held by no row (deepseek, grok, Opus):** refusal, read and announce each qualified
  by `port[COMMAND] != 1` score 94/94.  The enumeration lists COMMAND as an axis and holds only 0 and 2.
* **Cells 1-7 as state axes are not enumerated (Opus, measured):** refusal skipped when `port[COLOR_B] == 0` -- that
  one restores the process exit -- and when `port[Y1] == 0` or `port[COLOR_R] != 0x55`; a read falling into the write
  path when `port[COLOR_B] == 0`; announce suppressed for bit-63 first values; effect-4 cell writes conditioned on
  `len == 2`, on selector 5, or on COMMAND 0 (cells are read back only in V and K).
* **The wording "COMMAND 0 and 2 (V)" mis-cites a session (grok, Opus).**

## My proposed disposition (please rule on EACH)

1. **Not a floor breach, any of it.**  The repair path reads `idata` and `warned_port`; the floor (the joint-cell
   ruling) is the dominating predicates x those lvalues plus the generating set, and table 4 holds it.  Selector,
   COMMAND and cell values are coverage BEYOND the floor, which the class closure claimed -- so what is wrong is the
   CLAIM (L4), and the chain CLOSES on this pass under the stop condition (zero floor breaches), after the repair below.
2. **Repair the claimed cells (L1/L4), cheaply:** X3's value becomes `0x100000005` (wide; truncates to 5, not 3); every
   X session gets its "announce names the value" row (0x9, 0x9, 0x9, 0x100, 0x100000005); a new session Y puts
   COMMAND = 1 (SET_RESOLUTION with X1 = Y1 = 0, which `dev_fb_resize` ignores with a message and returns -- no exit),
   then its FIRST refusal after PORT=5: keeps 5, announces once, and its PORT read sees COMMAND 1; and the Opus seat's
   measured row -- a PORT read right after V's last refusal, "V PORT keeps 7 after its later refusals" (it killed the
   COLOR_B, Y1 and COLOR_R refusal edits and the COLOR_B read edit, 95/95 on the fix).  94 -> 101 rows.
3. **State the enumeration's axes exactly and DISCLOSE the rest:** COMMAND's three implemented values {0, 1, 2} held
   for refusal, announce and read; the data cells' VALUES are not an enumerated axis -- an edit conditioned on a cell's
   value is caught only where a row holds that state (V after its later refusals holds cells 1-7 at 0x11*p) -- NOT
   CLAIMED; effect 4 (a refusal leaves every cell alone) is claimed only for the cells, widths, selectors and COMMAND
   values V and K hold, and says so.
4. **Then table 5** -- table 4's 101 edits plus every closing-F2 edit (grok's store-at-selector-3, the 0x100 name
   mangle, the three COMMAND = 1 qualifiers, the Opus seat's 11) -- predictions first; gate 16; the records.  No further
   panel pass: this pass closes the chain.
5. deepseek's DO NOT SHIP rests on the COMMAND = 1 omission, which 2 repairs; C19 (KEEP) and C20 (REJECT) stand -- the
   Opus seat measured C19's row as the only holder of the "COMMAND non-zero and latched" joint cell.

**Be hardest on 1** -- it is the ruling that lets me stop, and a stop rule that favours the author is the one to test.
Is anything here actually a floor breach?  Is closing the chain after an unreviewed repair right, or does the repair
owe its own pass?  If, while verifying a claim, you found something ELSE -- say so.
