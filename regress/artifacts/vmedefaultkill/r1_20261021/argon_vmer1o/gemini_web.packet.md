# Reading task: vmedefaultkill probe oracle audit (Argon) (Gemini web; 2026-10-21)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-VMER1O-d4df` on a line of its own.

# vmedefaultkill -- audit the ORACLES of an emulator regression probe: can any row pass when it should fail?

**Format:** open with the token `ARGON_VMER1O_20261021`, then ONE line `VERDICT: ORACLES SOUND | ORACLE DEFECTS FOUND | CANNOT SETTLE --
<one line>`, then your findings.  Every FLAG is a line of its own starting `FLAG:`, citing `<label>:<n>`.  Facts and flags
only; agreement is not wanted.

**This is a reading task on the ATTACHED file `argon_bundle_1.txt` (read it to the end) and this message only.**  The
probe drives an emulator through its debugger: STEPPED sessions feed commands on stdin, FREE-RUNNING sessions drive a pty,
place a breakpoint and `continue'.  Each row prints `<name>  <got> ... ok|FAIL`, and a gate counts the `ok' lines by name.

**The question.**  Find any row whose oracle can report `ok' when the behaviour it claims to pin is ABSENT -- in
particular the rows revision 3 added or changed: `p2 zero wr', `p2 nw rd 2', `p2 nw wr 2', `p1 quiet', the two lane-0
accesses in `p1 widths', and the CONTROL split (`CONTROL_ROWS').  For each candidate, which shape it is:
  (a) an expected value computed from the output it checks;
  (b) a row that passes on a session that died, timed out, or never reached its breakpoint;
  (c) a count that can be satisfied by zero matching lines, or a zero accepted without proof the run happened;
  (d) a pattern that also matches another row's line, another session's text, or the echoed command;
  (e) a timeout or a missing line read as the wanted value.
Name the row, the shape, the line(s), and the smallest emulator behaviour under which it would wrongly print `ok'.  If you
find none, say which rows you checked and against which of (a)-(e).  Anything you cannot settle from this material is
UNSETTLED: name what would settle it.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`VMER1O: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
