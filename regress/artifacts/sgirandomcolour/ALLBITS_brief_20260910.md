# #519 sgirandomcolour -- READ-ONLY CHECK of the new `allbits' class-closure rows before their table runs

Nonce: CODEX_519_ALLBITS_20260910.  Open with `VERDICT: GO | NO-GO (n items)` and echo the nonce.

**Please do not simply ratify.**  Your previous audit (`regress/artifacts/sgirandomcolour/codex_pretable6_20260910.txt`)
said one session can prime all twelve other warn bits before the colour decline and gave a sequence.  That
sequence is now IN the instrument as three rows, and the question is whether it does what the rows claim
ON THIS TREE.  Check the premises against the source, not the prose.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`; ignore any other `src/` under the project root.

## Files
* `regress/sgi_re_colourdefault_probe.py` -- the block after the anchor `CLASS CLOSURE on the latch-collision axis`
  (helpers: `def store`, `def load`, `def loadop`, `def setup_put`, `def run_ops`, `class Addr`, `def session`).
* `src/devices/dev_sgi_re.c` -- the thirteen latch sites (grep `d->warned & SGIRE_W_`), `DEVICE_ACCESS(sgi_re)`,
  `DEVICE_ACCESS(sgi_de)`, `draw_primitive`, `horrible_getputpixel`.
* `regress/sgi_re_width_probe.py` -- the precedent (anchor `CLASS CLOSURE ON THE LATCH-COLLISION AXIS`, `SETUP_LIT`,
  `row("tex xbit"`), whose priming sequence the new block copies in a different helper idiom.

## Settled premises
* `fatal()` returns.  The fix under review: PUT default arm `ok = 0`, once-latched announce on `SGIRE_W_BADCOLOR =
  1 << 12`, store guarded by `if (ok)`.  ANN in the probe is the substring `unimplemented colour type in
  horrible_getputpixel`.
* The probe's `store(A, addr, val, op=OP_SW_T0_A3)` takes the VALUE positionally and the opcode by keyword (the
  width probe's helper is the other way round; the width probe's own comment records the day that bit it).
* The colour probe runs `-E sgi -e ip32 -M 64` with a dummy image at 0x80001000; the DE/RE window base is
  0xb5001000 (KSEG1 of 0x15001000).

## Questions (verdict line first; cite by grep anchor)
1. For each of the twelve priming accesses in the block, name the arm of `dev_sgi_re.c` it reaches and the bit
   it sets, by reading the dispatch (`relative_addr` ranges, the `len` tests, the `writeflag`).  Which of the
   twelve, if any, does NOT reach the site the comment says -- for example a byte store that is served rather
   than declined, or an access that dies?  A priming access that fires nothing leaves a hole that
   `allbits primed` should expose: does its `PRIME_LIT` list carry the EXACT text each site prints (case,
   spacing, the ` -- declined.` suffix), so a miss reds the row rather than passing it?
2. Does anything in the priming sequence disturb the YCRCB PUT that follows?  In particular: the byte store
   to the LINEAR_A window (0xb5001700) before `setup_put()` re-programs `re_linear_a[0]`; the LIN_B rectangle
   (bit 10) leaving DE state that the later `setup_put(MODE_YCRCB)` does not rewrite; the 64-bit TEX read.
   If the YCRCB PUT could fail to reach the default arm, `allbits announce` reads 0 on the FIX and the row is
   mis-cut.
3. The row's oracle is `t_all.count(ANN) == 1`.  Under a mutant that latches BADCOLOR on some other existing
   bit, is the count 0 for EVERY one of the twelve bits (i.e. is every bit set by the time the colour decline
   runs)?  Name any bit for which the order of accesses leaves it CLEAR at that moment.
4. `session()` is called with `spin=4.0` for this long session; the other sessions use the default 1.6.  Read
   `def session` and `rd()`: is there any way the transcript could be cut before the final `print v0` and the
   row read `absent`/`died` while the emulator is healthy?  Say what the load sensitivity is.
5. Anything else that would make one of the three rows green on a mutant it names, or red on the fix.

Do not run builds or probes (another table is using the scratch clones); no product-code proposals.
