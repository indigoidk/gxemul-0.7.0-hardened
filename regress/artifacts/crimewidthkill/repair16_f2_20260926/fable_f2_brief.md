# #529 -- THE FLAGSHIP ADJUDICATION OF THE F2 PASS (repair 15's pass-2 findings; repair 16)

Liveness first: begin with the token FABLE5_F2ADJ_ALIVE_0926 and quote verbatim the first line of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`.

You adjudicate LAST: every other seat has answered the F2 packet.  GPT-6 Astra confirms your ruling afterwards,
and nothing commits before #549 does.  This is ordinary test-coverage review of an emulator device model: which
of the main loop's dispositions stand, which rows (if any) are still owed before the chain can close, and what
the contract text must say.  Please be hardest on the rulings that follow your own earlier answers.

## THE EVIDENCE (read-only; every path verified to exist when this brief was written)

* the F2 packet (as sent): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\f2_packet.md`
* table 16's scoring: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\table16_20260926\check16.out`
* POSTTABLE16: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\table16_20260926\POSTTABLE16.out`
* PRETABLE16: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\table16_20260926\PRETABLE16.out`
* the repair-16 probe (frozen): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\table16_20260926\crime_width_probe.table16.py`
* the repair-16 diff: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\probe_r16.diff`
* agy (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\agy.txt`
* grok panel seat (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\grok.txt`
* glm (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\ollama_glm.txt`
* kimi-k3:cloud (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\ollama_kimi.txt`
* minimax (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\ollama_minimax.txt`
* deepseek (F2): `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\ollama_deepseek.txt`
* the dedicated grok job (F2): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\grok_dedicated_f2.txt`
* the Opus measuring seat (F2): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\opus5_f2.md`
* codex / GPT-6 Astra (F2, after 07:01): `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\codex_f2.txt`
* your own pass-2 answer: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair15_pass2_20260926\fable5_r15p2.md`

## WHAT THE F2 PASS PRODUCED -- the disagreements, in the seats' own positions

**Undisputed by every answering seat:** F1 (the HARD_RESET residue cell, L2) and repair 16's `ctlrst`/`rst … msg` rows as
its repair; table 16's 25 legs as scored (CHECK16_PASS); D1 (the TIME rows' s1 is small); F5/F14 settled on the row list.

**X1 -- F20, the residue VALUE (a clear skipped only when another bit of the written value is set).**  glm and kimi-k3:
overturn "disclosed" -- take the zero-session value anchor (`unimplemented control 0x0000000000000001`), since the
contract's "closes the channel as a class" is otherwise false on the value axis, and the `ctldog` note ("the twin's")
claims a witness the count does not verify.  The grok panel seat: disclosed is right; if anchored, BESIDE the prefix
count, not instead of it.  The dedicated grok job: the same bit-conditioned form exists for ALL THREE clears
(`if (!(idata & 1)) idata &= ~CRIME_CONTROL_HARD_RESET;` passes all 226 rows: every accepted reset store is exactly
0x0800), so F20's disclosure names only one of three.

**X2 -- F2/D4, the ENDIANESS counts.**  minimax and deepseek: the counts that carry ENDIANESS are unlicensed scope growth
(your pass-2 answer called them "not owed").  The grok panel seat: keep the counts, but ENDIANESS stays clause (e) -- the
count is a strengthening and a side effect of the count of 4, not a member of the tested-bit class.

**X3 -- F4/D3, the latch-gated clears.**  The grok panel seat: overturn -- "the arm reads no latch" IS the clause-(e)
test and the right grade; the rows may stay as a strengthening, but the clause-(e) sentence must not be deleted.

**X4 -- the aggregate counts.**  The grok panel seat: `rearm ctl msg` cannot say WHICH clear failed (`L_dogclr` and
`E_noendianclear` both read 6), and the contract's "a residue-count row in BOTH latch states" is, for DOG-latch-SET and
both ENDIANESS states, one shared count over ten writes, not a row of its own.  agy: the same channel coupling; plus two
stale labels in the F2 packet (a 222-row / 1534bc9e header on E7 and E10), corrected in the codex copy.

**X5 -- D2, the eight INTSTAT/INTMASK width x direction x latch cells.**  Every answering seat that ruled: disclosed, the
header scoped (grok panel, grok dedicated, and the main loop).  The Opus seat's pass-2 point, that the probe's own
precedent rowed a width narrowing at INTSTAT, is answered by the dedicated grok job: those 2-byte rows are latch-SET cells
already killed by M6/M7.

**X6 -- D5, the state/value cells (F18, F19, F20).**  Disclosed by every answering seat; the grok seats name zero- or
one-store carriers if they are rowed as strengthenings, and note F19's "nothing watches the fall" is too broad (`p istw
mid` watches an accepted fall).

**X7 -- found by the pass, outside the three clears:** `CRIME_CONTROL_SOFT_RESET` (0x0400) is neither tested nor cleared by
the arm, and no row writes it (grok panel).

**X8 -- the Opus measuring seat's F2 answer (opus5_f2.md; verified claude-opus-5-5; eight new mutants, each predicted in
writing before its batch, all as predicted):**
* the value anchor, if added, must sit BESIDE the prefix count, never replace it: an anchored count alone stays at 1 under
  `H_noresetclear` (the `ctlrst` twin 0x0001 carries no HARD_RESET bit) -- its own repair-15 wording ("rather than the
  prefix") is the disposition it overturns first;
* the class closure holds for the text COUNT, not for the PRINT CHANNEL: `M_ctldebug` (the CONTROL arm's `fatal()` made a
  `debug()`) scores 226/226, because every counting session single-steps and `debug()` prints while stepping; one
  free-running session would carry it -- disclose, or row as a strengthening;
* `ctlrst sw halt` had no measured kill in table 16; `S_rst4clr` (224/226, with `sw08 halts`, CONTROL=FAIL) is one now;
* the halt rows' comment overclaims -- a build where the 0x0001 twin itself halts reads identically (`T_halttwin`), so
  the halt proves a halt, not that the 0x0800 reached the arm: fix the comment, not the rows;
* wrong records: every ACCEPTS entry in `rearm` runs with the latch SET (a refused `lb +0x07` precedes the loop -- the
  comment says "after the first entry"); F19's "nothing watches the fall" should read "no REFUSAL row watches the fall";
  F14's "the single-axis latch-CLEAR cells are rowed" should read "label-only"; PRETABLE16's "every refusal in this
  session is at +0x06" (the first is +0x07; no prediction changes);
* D2, D3, D4: clause (e) / licensed / licensed -- it withdraws its own precedent argument for D2.

**X9 -- codex / GPT-6 Astra (codex_f2.txt, its first look at this round; answered cleanly after the 07:01 reset):**
"UPHOLD REPAIR 16'S BOUNDED COUNT COVERAGE; CORRECT THE SESSION COUNT AND QUALIFY THE ROW-VALIDATION CLAIM" -- F24 as
written is wrong the other way (repair 15's census shows SIX latch-SET TIME sessions, not two: a record correction, not
a breach); in table 16 only SEVEN of the eight new rows have a failing leg (`ctlrst sw halt` has none there -- the Opus
seat's `S_rst4clr` supplies it); an exact-value check that REPLACED the prefix count would lose the reset-clear
detection; D2 clause (e), D3 a licensed strengthening, D4 clause (e) legitimately strengthened.  The dedicated codex
coverage check (codex_f2ded.txt): the contract sentence is TRUE as written; not covered are the printed residue VALUE
and a nonzero residue printed after a HARD_RESET stop (every accepted reset store is exactly 0x0800).

## THE QUESTIONS

1. **Rule on X1-X7**: for each, UPHOLD the main loop / OVERTURN / REFINE, one line with the reason.
2. **Is the chain closed?**  The stop condition you set: zero floor breaches on a VALID pass (roster complete or its misses
   named, the zero carried with its denominator).  Name any floor breach that survives, or say none does and why.
3. **What must the contract text say** before the probe enters the tree -- in particular the latch joints (X3), ENDIANESS
   (X2), the aggregate counts (X4) and the bit-conditioned clears (X1)?  (Text edits change the probe's bytes; the main
   loop will re-run the base leg on the final bytes before the gate pin cites it.)
4. **Which rows, if any, are still OWED** before closure -- as opposed to optional strengthenings to FILE?

VERDICT LINE FIRST.  Write your answer to
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\fable5_f2_adjudication.md`
(the only file to write) and return it as your final message.
