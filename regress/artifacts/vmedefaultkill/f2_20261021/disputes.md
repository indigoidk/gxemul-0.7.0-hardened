**D1 -- the read announce's format (F5).**
* ALIGN to `0x%llx` / `(unsigned long long) odata` -- GL [F6]: *"the adjudication is the ruling artifact -- a silent
  code/record divergence is exactly the drift this process polices ... the contract itself contemplates a later
  vmewidthlanes fix composing a 64-bit odata ... under `%x` that future compose prints a truncated lie."*  AX [F4]:
  *"restoring the agreed form removes unexplained drift and accommodates a future composed 64-bit read."*
* KEEP `0x%x` and amend D2's record -- FB [F10] (D2 was FB's own pass-1 ask): *"the printed value is UNOBSERVABLE today
  -- M_SERVED0 (a literal 0 in its place) survives 34/34 ... a format-only edit now changes the fix md5 the table measured
  and invalidates the find-strings of two legs ... What may not ship is the current state -- a record that says `0x%llx`
  beside code that says `0x%x` with no reason anywhere."*  GK [F4]: *"changing this string now does not change a
  guest-visible bit ... A later vmewidthlanes edit that builds a real 64-bit odata owes its own format row."*
* **My ruling: ALIGN.**  FB's cost argument was the deciding one, and F1 removes it: rev 3 re-runs the whole table on a
  regenerated leg set anyway, so the format change costs no extra measurement.  What remains is GK's "no guest-visible
  bit", which is true and is equally an argument for either form -- so the adjudicated record decides.  **FB and GK:
  does that hold, or is there a reason to keep `%x` that is not about the re-run?**

**D2 -- when to reclassify the CONTROL rows (F8).**  AX: before shipping.  GK: *"Leave the tuple alone in this ship:
moving it changes VME_DEFAULT_CONTROL and unfreezes the measured instrument."*  FB: at the next revision.  GL: at the
next instrument revision.  **My ruling: in rev 3** -- rev 3 IS the next revision, and it re-measures everything.

**D3 -- the "(FAILED FOR SOME OTHER REASON)" text (F9).**  AX: change before shipping (*"its asserted causal exclusion is
not [accurate]. The oracle cannot know the reason is unrelated to the mutation."*).  GL, GK: keep (accurate from the
row's vantage; the miss note is the place).  FB: keep the dependent rows' text, change the non-word session's stop text
at the next revision.  **My ruling: rev 3 adopts AX's neutral wording on all of them, rows stay red** -- same reason as
D2.  GL and GK: is there a reason the neutral wording is WORSE, beyond the re-run cost that rev 3 pays anyway?

**D4 -- the ask-again's coverage debt (F10): FILE or take in-round.**  FB filed (a) and (b) as clause (e) (*"`len` is
PRINTED, not TESTED, by the body and is not device state, so this is outside the (d) floor -- FILE as coverage debt, or
take it under L1"*); GL put (c) in the `vmewidthlanes` round (*"closing it costs one probe line"*).  **My ruling: take
(a), (b), (c) under L1 in rev 3, FILE (d), (e)** -- because each is one or two accesses inside an existing session and
rev 3 re-tables anyway.  **The risk I see in my own ruling:** every added row is new floor-bound material for the repair
pass to review, and this project's `#499` chain grew one cell per pass.  If you think taking them now lengthens the chain
more than it closes, say FILE and say why.

**D5 -- the typedef (F2): a shared macro for the shift operand, or reword the comment.**  AX [F1]: *"Use a shared
mask-operand definition in both shifts and the capacity check, then verify its narrowing fails compilation."*  FB [F1]:
*"take the reword now and file the macro"* (because the macro invalidates the latch legs' find-strings -- moot under rev
3).  GL [F5]: reword to claim the field only.  **My ruling: reword + delete the tautological conjunct + measure
M_ONENARROW**, NOT the macro: the addition licence asks for a measured delta, and the macro's only delta is moving
detection of a narrowed literal from run time (where rev 3's announce rows should catch it -- M_ONENARROW will say) to
compile time.  If M_ONENARROW ESCAPES rev 3, the macro gains its measured delta and I adopt it.  AX: is that the right
test of your proposal?
