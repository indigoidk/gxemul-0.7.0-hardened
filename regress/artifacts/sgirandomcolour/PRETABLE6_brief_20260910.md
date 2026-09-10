# #519 sgirandomcolour -- RECORDS AUDIT of the pass-2 repair (read-only; ordinary regression-instrument engineering)

Nonce: CODEX_519_PRETABLE6_20260910.  Open with the verdict line `VERDICT: GO | NO-GO (n items)` and echo the nonce.

**Please do not simply ratify.**  Your previous audit of this round (`regress/artifacts/sgirandomcolour/`
answers) found that PRETABLE §4 mis-assigned a mutant to a row, that the diff description was the non-blank
count, and that a width claim lacked its qualifier.  All three are now disposed in an APPENDED section 6 of
`regress/artifacts/sgirandomcolour/killtable_20260910/PRETABLE.out` (sections 1-5 are unedited; §6 is
new).  Check the premises of §6, not only its arithmetic.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` -- ignore any other `src/` you find
under the project root (there are three pristine-upstream copies; a file whose line numbers disagree
with these by hundreds is one of them).

## Files (read these; do not rely on this brief's paraphrase)
* `regress/artifacts/sgirandomcolour/killtable_20260910/PRETABLE.out` -- §6 is the object under audit.
* `regress/sgi_re_colourdefault_probe.py` -- the repaired 16-row instrument (working file; its frozen
  pre-repair 14-row copy is `regress/artifacts/sgirandomcolour/killtable_20260910/sgi_re_colourdefault_probe.FROZEN.py`).
  The repair is the diff between those two.
* `src/devices/dev_sgi_re.c`, function `horrible_getputpixel` (grep anchor: `int linear = tlb_mode > 3;`)
  and `draw_primitive` (grep anchor: `CRIME_DE_X_VERTEX_0 - 0x2000`).
* `regress/artifacts/sgirandomcolour/killtable_20260910/t2/mut519x.py` -- the three table-2 mutants, if
  it exists yet (it is copied there when table 2 starts); otherwise the same file in the session scratchpad
  is not reachable to you -- say so and audit the mutant descriptions in §6.f instead.

## Settled premises (re-inlined so nobody re-derives them)
* `fatal()` returns (`src/core/debugmsg.c`, grep `void fatal(`): no early-out, no exit.
* The fix (uncommitted, in the working tree): the PUT branch's `default:` arm sets `ok = 0`, announces once on
  its own latch bit `SGIRE_W_BADCOLOR = 1 << 12`, and the store is `if (ok) cpu->memory_rw(...)`.  Product
  code otherwise untouched.  HEAD for this file is commit `1ce8296`.
* Table 1 (the Opus seat, 14-row frozen instrument, `killtable_20260910/*.raw`) is still running; its
  scores are NOT claimed here.  Table 2 (16-row instrument, `t2/`) has not started.
* The instrument drives the LINEAR destination path: `DE_MODE_DST = 0x12f0` etc. (LIN_A `0x1000`, 32 bpp
  `0x200`), with `re_linear_a[0] = 0x10` so tile 0 maps to physical `0x10000`.

## Questions (verdict line first; one numbered item per finding; cite by grep anchor, not line number)
1. **§6.f's offset claim.**  For a PUT at vertex (4,1) in LIN_A mode at 32 bpp, does `horrible_getputpixel`
   compute the destination as physical `0x10000 + 4` -- i.e. is `ofs = x & 4095` with y ignored the path
   actually taken (`case 4:` of the `tlb_mode` switch), and is `tileptr` what §6 says?  If the (4,1) PUT
   would land somewhere else, the new row `ycrcb x4y1` reads the wrong word and is vacuous by construction.
2. **§6.g's byte-identity claim.**  The repair adds a `vertex` parameter to `setup_put()` and emits an extra
   store only when `vertex` is non-zero.  Read `setup_put`, `store`, `run_ops` and the `Addr` allocator:
   is every pre-existing session's debugger command stream (the list of `put w` / register / `step` lines)
   unchanged by the repair?  Name any session whose commands differ.  This claim is what lets table 1's
   per-row kills carry over instead of re-running twelve mutants.
3. **§6.a's mutant-to-row reassignment.**  Under `int ok = 0` (every type declined), which rows red on the
   16-row instrument, by reading the instrument: is it `live` (and the three other accept rows `ci8 put`,
   `rgb put`, `abgr put`), with `live silent` unchanged at 0?  State the full expected red set.
4. **§6.f's disclosure.**  A mutant latching on `SGIRE_W_TEX_RD` instead of `SGIRE_W_BADCOLOR` is expected
   to escape all 16 rows and is DISCLOSED rather than rowed, on the ground that the body tests exactly one
   bit and the other-bit cells are values the body never distinguishes.  Is there a CHEAPER row than one
   session per bit that would catch the whole class (for example a row that fires some other latch site
   first through a path the instrument already has), or is the disclosure the right disposition?  If a row
   exists, name the exact guest access sequence.
5. **Anything else in §6 that is a wrong record** -- a number, a count, a name, a claim about order.  The
   appended section claims sections 1-5 are unedited: they are, but check that §6 does not silently
   contradict a sentence in §1-5 without saying so.

Do not propose product-code changes; the fix is not under review here.  Do not run builds or probes
(read-only sandbox; another seat's table is using the scratch clones).
