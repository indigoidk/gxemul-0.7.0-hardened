# Reading task: vmedefaultkill repair pass (Argon) (Gemini web; 2026-10-21)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-VMER1-d5b0` on a line of its own.

# vmedefaultkill (repair pass) -- an emulator's VME bus-controller model: try to break a closing "no escapes" claim

**Format:** open with the token `ARGON_VMER1_20261021`, then ONE line `VERDICT: CLOSE | REPAIR AGAIN | CANNOT SETTLE -- <one line>`,
then Q1 and Q2.  Every FLAG is a line of its own starting `FLAG:`, citing `<label>:<n>`.  Facts and flags only; agreement
is not wanted.

**This is a reading task on the ATTACHED file `argon_bundle_1.txt` (read it to the end) and this message only.**  D is the
device as the fix ships it; R is the 38-row regression probe's row contract; K is the measured mutation table (34
one-edit variants of D, plus one more); F is another reviewer's claim that NO one-edit variant inside the bound below
escapes the probe.  Anything you cannot settle from this material is UNSETTLED: name what would settle it.

**The bound** (the only variants that count): (1) the conditions that control the fix's edited lines -- the
population-2 `case` labels, the latch test `if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2))))` and its set, the
direction test `if (writeflag == MEM_WRITE)` inside it, and `default:`'s `return 0` -- walked only to the end of the
function; and (2) swaps of a condition's operand for another value the guarded code itself reads (`writeflag`,
`relative_addr`, `len`, `idata`, `odata`, `d->warned_unimpl`).  A condition weakened to a form that still reads like the
same check counts; deleting it does not.  A value the guarded code never tests as a case (a particular store value, a
single bit of idata) is OUTSIDE the bound -- that is disclosed, not owed.

Q1. Walk F's table row by row against D and R.  List each ONE-EDIT change to D inside the bound that would keep all 38
    rows green and is NOT among K's legs, and each row F credits with a kill that would NOT go red under the edit F
    names.  For each: the edit as a one-line diff, the row(s) you expect to stay green, and why that row's check cannot
    see it.  Cite D:<n>, R:<n>, F:<n>.  If you find none, say so and list what you swept.
Q2. K's M_IDATABIT1 adds `&& !(idata & 2)` to the direction test and scored 38/38.  Is it rightly OUTSIDE the bound (the
    guarded code tests no bit of idata), or is it an escape that counts?  And F lists the low-word bits that are clear in
    all five store values the probe uses (0x0, 0xa5a5a5a5, 0xd4, 0xc3d4, 0x1122334455667788) as 1, 11, 19, 20, 25, 27:
    check that list.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`VMER1: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
