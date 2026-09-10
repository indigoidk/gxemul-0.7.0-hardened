# `#519` sgirandomcolour — PASS 2 ON THE REAL DIFF: the colour-type PUT default wrote four host-PRNG bytes into guest memory; it now declines the store once-announced

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like

## §C0 — HAS THIS ROUND SHIPPED?  NO.
HEAD is `1ce8296`. The diff below is the UNCOMMITTED working set of `GXEMUL-SEC/src/devices/dev_sgi_re.c`
(`git diff -- src/devices/dev_sgi_re.c`, 2 hunks, 58 changed lines) plus a NEW file
`regress/sgi_re_colourdefault_probe.py` (untracked; the witness half was built by the agy seat, the detector
half is inlined below). Ordinary bounds-correctness work on a drawing-engine pixel helper; plain language.

## §C — SETTLED PREMISES, RE-INLINED (say which you cannot settle from this packet)
S1. THE DEFECT. `horrible_getputpixel()` in `dev_sgi_re.c`: the PUT branch switches on
    `color_mode = mode & DE_MODE_TYPE_MASK` (0xf0). Four cases (CI 0x00, RGB 0x10, RGBA 0x20, ABGR 0x30 --
    `crmfbreg.h:328-331`); the `default:` arm assigned `buf[0..3] = random()`, called an UNLATCHED per-pixel
    `fatal()` (which RETURNS: `debugmsg.c:384`, no exit), and fell through to the common
    `cpu->memory_rw(... buf, bufdepth, MEM_WRITE ...)`. Twelve of sixteen nibbles reach it, `DE_MODE_TYPE_YCRCB`
    (0xf0, documented) among them.
S2. WITNESS (rung 3, agy seat, unmodified `-E sgi -e ip32`, DE rectangle PUT through LIN_A at a physical tile,
    destination pre-painted 0x11223344, fg 0xaabbccdd): on HEAD `SGICOLOUR_RESULT=2/5` -- the YCRCB PUT read
    0x56e8857a (run 1) / 0x38abc4e1 (run 2), the reserved-type 0x50 PUT likewise, neither the paint nor any
    packing of the colour, different across runs because `main.c` seeds `random()` per process; attribution
    text `[ put: color mode = 0xf0 ]` present. On the fix, 5/5 with the same script; with the nine detector
    rows below, 14/14 on the fix and 6/14 on HEAD (`regress/artifacts/sgirandomcolour/witness_20260910/`,
    `fix_20260910/`).
S3. DESIGN (pass-1 panel 2026-09-08, five seats; codex DESIGN2 reading; flagship ruling 2026-09-09): option-set
    member 3, candidate (b) -- SKIP THE STORE for an unsupported type (a one-local `ok` guard around the single
    store, never an early `return`: the common tail is that store), delete the random() fills and the per-pixel
    fatal, announce ONCE per device instance on an INDEPENDENT latch bit. Rejected: (a) zero-fill-and-store
    (publishes a colour the guest never asked for). The GET default arm is a SEPARATE row (`sgirebufuninit`)
    and is untouched. The old literal `[ put: color mode = 0x%x ]` is kept as the announce's prefix because the
    witness attributes on it.
S4. THE LATCH: `SGIRE_W_BADCOLOR = 1 << 12`, added as the LAST enumerator with the enum's own "next free bit"
    sentence moved to it and the previous holder's copy demoted (the convention every entry in that enum
    records). `SGIRE_W_BADMODE` (1 << 10) is the same function's TLB/mode-switch decline (`#504`) -- a different
    event with a different text.
S5. PRE-TABLE CHECK written before any table (`killtable_20260910/PRETABLE.out`, inlined at the end).

## THE DIFF (src/devices/dev_sgi_re.c, verbatim)
```diff
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 4d4f356..b8844f7 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -146,13 +146,27 @@ enum {
 	    has a row for exactly this (`tex xbit', which fires all six width
 	    latches before reading).
 
-	    THE NEXT FREE BIT IS 1 << 12, AND THIS IS THE LAST ENUMERATOR --
-	    which is where that claim belongs, per the convention two comments
-	    up.  A maintainer adding a bit BELOW this line must move this
-	    sentence with it and demote the copy here, exactly as #513 had to
-	    demote SGIRE_W_BADMODE's.
+	    (This comment used to end "THE NEXT FREE BIT IS 1 << 12, AND THIS
+	    IS THE LAST ENUMERATOR".  #519 added SGIRE_W_BADCOLOR = 1 << 12
+	    BELOW this line and moved the sentence with it, as this comment
+	    itself instructed.  Demoted, not deleted, for the same reason as
+	    the two demotions above it.)
 	 */
 	SGIRE_W_TEX_RD    = 1 << 11,
+
+	/*  #519 (sgirandomcolour): the colour-type PUT decline in
+	    horrible_getputpixel() gets its OWN bit, per the rule every entry
+	    above records: the helper is per-pixel, the struct is shared by
+	    four handlers, and a latch shared with any other site is silenced
+	    by that site's ordinary traffic.  SGIRE_W_BADMODE (1 << 10) is the
+	    TLB/mode switch's decline in the same function and is a different
+	    event with a different text; sharing it would collapse the two.
+
+	    THE NEXT FREE BIT IS 1 << 13, AND THIS IS THE LAST ENUMERATOR --
+	    which is where that claim belongs, per the convention above.  A
+	    maintainer adding a bit BELOW this line must move this sentence
+	    with it and demote the copy here.  */
+	SGIRE_W_BADCOLOR  = 1 << 12,
 };
 
 struct sgi_re_data {
@@ -306,6 +320,7 @@ void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
 
 	uint8_t buf[8];		/* #100: bufdepth can be 8 = 1<<((mode>>8)&3) */
 	if (put) {
+		int ok = 1;	/*  #519: cleared by the default arm below  */
 		switch (color_mode) {
 		case DE_MODE_TYPE_CI:
 			buf[0] = *color;
@@ -328,16 +343,36 @@ void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
 			buf[2] = *color >> 16;
 			buf[3] = *color >> 24;
 			break;
-		default:buf[0] = random();
-			buf[1] = random();
-			buf[2] = random();
-			buf[3] = random();
-			// TODO.
-			fatal("[ put: color mode = 0x%x ]\n", color_mode);
+		default:/*  #519 (sgirandomcolour): this arm was `buf[0..3] = random()'
+			    and an UNLATCHED per-pixel fatal(), after which the common
+			    store below wrote four HOST-PRNG bytes into guest memory.
+			    Twelve of the sixteen type nibbles reach here, the documented
+			    DE_MODE_TYPE_YCRCB among them.  MEASURED at rung 3
+			    (regress/sgi_re_colourdefault_probe.py): a destination
+			    pre-painted 0x11223344 read 0x56e8857a and 0x38abc4e1 on two
+			    runs -- neither the paint nor any packing of the colour, and
+			    different each run because main.c seeds random() per process.
+
+			    NOW DECLINED, member 3: the STORE IS SKIPPED, so the
+			    destination keeps what the guest had -- not a zero fill, which
+			    would publish a colour the guest never asked for (random() with
+			    the entropy stripped) -- and the announce is latched on its own
+			    bit because this helper is per-pixel.  The old literal is kept
+			    as the prefix: the witness attributes on it.  A declined PUT
+			    never reads buf, so the width question (sgirebufuninit) is a
+			    separate row, and the GET default below is untouched.  */
+			ok = 0;
+			if (!(d->warned & SGIRE_W_BADCOLOR)) {
+				d->warned |= SGIRE_W_BADCOLOR;
+				fatal("[ put: color mode = 0x%x ] sgi_re: unimplemented "
+				    "colour type in horrible_getputpixel, x=%i y=%i; store "
+				    "declined (once) ]\n", color_mode, x, y);
+			}
 		}
 
-		cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
-		    buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
+		if (ok)	/*  #519: a declined type stores nothing  */
+			cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
+			    buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
 	} else {
 		cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
 		    buf, bufdepth, MEM_READ, NO_EXCEPTIONS | PHYSICAL);
```

## THE DETECTOR ROWS APPENDED TO regress/sgi_re_colourdefault_probe.py (verbatim; the five witness rows above them are unchanged)
```python
# ================================================================ #519 DETECTOR ROWS
#  The five rows above are the WITNESS (2/5 on HEAD 1ce8296 -- both unsupported-type PUTs landed host
#  PRNG bytes -- and 5/5 on the fix with the same script).  The rows below DEFEND the fix.
#
#  CONTRACT (clause (e)).  Designed to catch: (b) the verbatim arm reinstated (random fills + an
#  unlatched fatal, the store still taken -- `ycrcb put', `reserved put', `announce text'); (d) the
#  `ok' guard REMOVED (the store taken with an unassigned buf -- `ycrcb put'); the decline turned
#  into a ZERO FILL and a store (`ycrcb put' reads 0); `ok = 0' MOVED INSIDE THE LATCH so only the
#  first declined PUT skips its store (`two declined'); the latch REMOVED (`once' reads 2); the latch
#  SHARED with SGIRE_W_BADMODE (`latch indep' reads 0 after a bad TLB mode fired that bit); the
#  announce SILENCED (`announce text' reads 0); a supported type dropped from the switch (its accept
#  row); the accept side announcing (`live silent').  NOT rowed, disclosed: the GET default arm (a
#  separate row, sgirebufuninit); 16-bit depth (the PUT arms assign four bytes and a 16-bit store
#  takes two -- the same row's question); `x`/`y` in the announce (format only); per-instance latching
#  (one RE instance exists); the YCRCB/reserved values other than 0xf0/0x50 (twelve nibbles reach the
#  arm; two are driven, and the arm does not read the nibble's value).
#
#  The destination word is read big-endian (ip32): byte 0 of the tile is the word's top byte.

ANN = "unimplemented colour type in horrible_getputpixel"     # the post-fix announce, distinctive part
DECL = "store declined (once)"
MODE_CI8  = 0x1000            # LIN_A | BUFDEPTH_8  | TYPE_CI   -- one byte stored
MODE_RGB  = 0x1210            # LIN_A | BUFDEPTH_32 | TYPE_RGB
MODE_ABGR = 0x1230            # LIN_A | BUFDEPTH_32 | TYPE_ABGR
MODE_LINB_RGBA = 0x1620       # LIN_B | BUFDEPTH_32 | TYPE_RGBA -- the TLB/mode switch's own default (BADMODE)

#  ---- accept rows: the other three supported types land their packing (de-escalation) -----------
A = Addr(CODE)
t_ci, alive_ci = session(setup_put(A, MODE_CI8) + load(A, DST_KSEG1) + ["print v0"])
row("ci8 put", printed(t_ci, "v0") if alive_ci else "died", "0xdd223344",
    "CI at 8 bpp stores ONE byte (fg & 0xff) over the paint's top byte")
A = Addr(CODE)
t_rgb, alive_rgb = session(setup_put(A, MODE_RGB) + load(A, DST_KSEG1) + ["print v0"])
row("rgb put", printed(t_rgb, "v0") if alive_rgb else "died", "0xaabbcc00",
    "RGB stores [R,G,B,pad]: three channels and a zero pad (#505's authoritative arm)")
A = Addr(CODE)
t_abgr, alive_abgr = session(setup_put(A, MODE_ABGR) + load(A, DST_KSEG1) + ["print v0"])
row("abgr put", printed(t_abgr, "v0") if alive_abgr else "died", "0xddccbbaa",
    "ABGR stores the register word byte-reversed")
row("live silent", t_live.count(ANN) if alive_live else "died", 0,
    "the RGBA accept session carries NO colour-type announce (the accept side stays silent)")

#  ---- the announce: present once, with the post-fix text, in the witness's ycrcb session --------
row("announce text", t_ycrcb1.count(DECL) if alive_ycrcb1 else "died", 1,
    "the declined PUT announces with the post-fix text ONCE (a reinstated arm or a silenced decline reads 0)")

#  ---- two declined PUTs in ONE process: the second also skips its store, and one announce -------
A = Addr(CODE)
t_two, alive_two = session(setup_put(A, MODE_YCRCB) + setup_put(A, MODE_RESERVED)
                           + load(A, DST_KSEG1) + ["print v0"])
row("two declined", printed(t_two, "v0") if alive_two else "died", "0x%08x" % DST_PAINT,
    "YCRCB then RESERVED in one process: the SECOND declined PUT leaves the paint too (`ok = 0' inside the latch would store)")
row("once", t_two.count(ANN) if alive_two else "died", 1,
    "two declined PUTs announce EXACTLY ONCE -- the (once) latch")

#  ---- the latch bit is its own: a BADMODE decline first, then a colour decline still announces --
A = Addr(CODE)
t_ind, alive_ind = session(setup_put(A, MODE_LINB_RGBA) + setup_put(A, MODE_YCRCB)
                           + load(A, DST_KSEG1) + ["print v0"])
row("latch indep", t_ind.count(ANN) if alive_ind else "died", 1,
    "LIN_B fires SGIRE_W_BADMODE first; the colour decline still announces once (a shared bit reads 0)")
row("indep paint", printed(t_ind, "v0") if alive_ind else "died", "0x%08x" % DST_PAINT,
    "and neither declined PUT stored (LIN_B returns before the store; YCRCB skips it)")

```

## THE PRE-TABLE CHECK (verbatim)
```
#519 sgirandomcolour -- PRE-TABLE CHECK, written 2026-09-10 ~04:2x BEFORE table 1 runs (mtime is the proof).
Instrument: regress/sgi_re_colourdefault_probe.py -- 5 witness rows (agy, 2/5 on HEAD 1ce8296, 5/5 on the
fix) + 9 detector rows appended by the main loop.  Diff under review: src/devices/dev_sgi_re.c
(scratchpad/patch_sgirc.py, 58 changed lines): SGIRE_W_BADCOLOR = 1 << 12 as the last enumerator, an `ok'
local in the PUT branch, the default arm declining (ok = 0, once-latched announce keeping the old
`[ put: color mode = 0x%x ]' literal as its prefix), the store guarded by `if (ok)'.  Product code
otherwise untouched; the GET default arm is NOT in scope (sgirebufuninit).

1. SIBLING PARITY
   The PUT default arm's sibling is the GET default arm in the same function (reads raw, announces
   per pixel, unlatched) -- NOT touched here; its row is sgirebufuninit and it is DISCLOSED in the
   contract.  The TLB/mode switch's default (SGIRE_W_BADMODE, #504) is the nearest de-fatalised
   sibling: latched, returns before any store.  Channels there: announce once, `*color' untouched.
   Channels here: announce once (its OWN bit -- `latch indep' rows the independence), destination
   untouched (`ycrcb put', `reserved put', `two declined', `indep paint').  ASYMMETRY: #504's arm
   RETURNS; this one falls through to the common tail with the store skipped -- deliberate (the
   sketch rule: the tail's memory_rw is the only thing after the switch, and it is what the guard
   skips), and the `two declined' row is what pins "skipped" rather than "returned early" for the
   second PUT.
2. CLAIM -> ROW
   "the STORE IS SKIPPED, so the destination keeps what the guest had"     -> ycrcb put, reserved put,
                                                                              two declined, indep paint
   "not a zero fill"                                                        -> ycrcb put (0 would red)
   "announce is latched on its own bit"                                     -> once, latch indep
   "the old literal is kept as the prefix: the witness attributes on it"   -> ycrcb attrib (unchanged),
                                                                              announce text
   "A declined PUT never reads buf"                                          -> no row: not observable
                                                                              (no store); SENTENCE.
   "Twelve of the sixteen type nibbles reach here"                          -> two driven (0xf0, 0x50);
                                                                              the arm does not read the
                                                                              value; SENTENCE (contract).
   "main.c seeds random() per process"                                      -> the witness's determinism
                                                                              row measured it; no fix row.
3. GUARD FIELD vs BODY FIELD
   Guard: color_mode (a local from `mode').  Body: `ok', d->warned.  The shared field d->warned now
   has thirteen bits; the disagreeing state the rule asks for is another site's bit set first --
   built in-session by `latch indep' (SGIRE_W_BADMODE fired by a LIN_B PUT, then the colour decline).
   `ok' is a local written only by the default arm: its disagreeing state is "second declined PUT in
   the same process with the latch already set", built by `two declined'.
4. CHANNEL -- per row, the mutant it kills and the observable that differs
   ycrcb put / reserved put   (b) reinstatement (random fills + store); M_noguard (`if (ok)' removed:
                              stores an unassigned buf); M_zerofill (buf = 0, ok = 1)     -> word != paint
   two declined               M_okinlatch (`ok = 0' moved inside the latch condition)      -> word != paint
   once                       M_nolatch (latch guard removed)                              -> count 2
   latch indep                M_sharedbit (SGIRE_W_BADMODE used instead of BADCOLOR)       -> count 0
   indep paint                M_sharedbit does not vary this; (b) does (LIN_B returns; YCRCB stores) -> word
   announce text              (b) (old text only) ; M_silent (announce removed)             -> count 0
   live silent                M_declineall (ok = 0 for every type) ; M_announceall            -> count 1 / word
   ci8 / rgb / abgr put       M_dropcase_X (the case removed -> falls to default -> paint)  -> word
   VACUOUS-BY-CONSTRUCTION CHECK: `indep paint' is fixed under M_sharedbit (both PUTs skip their
   store either way) -- it is a CONTROL for `latch indep', named as such; every other row's channel
   varies under its named mutant.
5. THE (d) ENUMERATION FOR TABLE 1 (bounded to the diff's hunks):
   dominating predicates: `put' (unchanged), `switch (color_mode)' (each supported type its own
   case; the default is one cell), `if (ok)' (introduced), the latch test (introduced).  Cells:
   {default declines / stores} x {latch kept / removed / shared} x {store guard kept / removed /
   inside-latch} x {supported types kept / one dropped}.  Planned mutants, one edit each:
   M1_reinstate (b)   M2_noguard   M3_zerofill   M4_okinlatch   M5_nolatch   M6_sharedbit
   M7_silent          M8_declineall   M9_dropcase_ci   M10_dropcase_abgr   M11_null (the pre-fix
   file wholesale)    M12_announce_prefix_dropped (the old literal removed from the text: kills
   `ycrcb attrib' -- an L4-shaped mutant; recorded because the prefix is load-bearing for the witness)
   ACCEPT rows: live (RGBA), ci8 put, rgb put, abgr put; growth mutants M9/M10 (a case dropped) and
   M8 (everything declined).
```

## THE QUESTIONS — VERDICT LINE FIRST, then answer extensionally
Q1. THE PREMISE AUDIT, as questions. (a) Does `ok` really gate the ONLY store in the PUT branch, and does the
    GET branch remain byte-identical? (b) With `ok == 0`, is `buf` read anywhere before the function returns?
    (c) Is 1 << 12 free in `enum` (no other user of bit 12 of `d->warned` anywhere in `dev_sgi_re.c`)?
    (d) Does keeping the old literal as a prefix leave any OTHER probe or gate that keyed on the old
    per-pixel text now silent (grep `regress/` for `color mode =`)? (e) `ci8 put` wants 0xdd223344: is the
    ip32 word read big-endian so byte 0 is the top byte, and does an 8 bpp PUT store exactly one byte?
Q2. THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES ALL 14 ROWS. Name the row you expect to stay green.
Q3. OPTION-SET COMPLETENESS at this arm: is there a member the design did not name? (member 7 IMPLEMENT
    YCRCB was refused for want of a packing spec -- is that still right?)
Q4. THE FLOOR: cells {default declines / stores} x {latch kept / removed / shared} x {guard kept / removed /
    inside-latch} x {supported types kept / one dropped}. Which cell has NO row whose channel varies? Say
    "none" with the denominator if that is the answer.
Q5. ACCEPT-ROW FAILABILITY: for `live`, `ci8 put`, `rgb put`, `abgr put`, name the growth mutant that reddens
    each.
Q6. CLAIM -> ROW: quote any added comment sentence asserting an observable consequence that has no row and
    no sentence in PRETABLE §2.
If, while verifying a claim, you found something ELSE — say so. State what you read versus what you took
from this packet.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
