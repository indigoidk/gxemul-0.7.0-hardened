<!-- ================================================================================
     DRAFT ROUND BLOCK -- NOT THE SHIPPED CHANGELOG TEXT.  #519 IS HELD.

     Rescued out of the session scratchpad (Windows Temp, volatile) on 2026-09-10.

       1. THE RECORDS AUDIT IS AT NO-GO.  codex_records_20260910.txt returned
          `VERDICT: NO-GO (13 items)', undisposed.  It did independently CONFIRM several of the
          draft's numbers against the artifacts (the hunk and line counts, the nibble and warn-bit
          counts, the four functions using d->warned, nine original sessions, the 03:51 / 04:00:19 /
          04:06 ordering metadata, and that M11's saved pre-fix file and HEAD's blob hash equal).

       2. TWO MUTANTS SWEEP THE INSTRUMENT CLEAN, and they are clause-(d) operand swaps on the
          guarded body's own read set.  The Opus measuring seat built them itself, after every
          planned mutant had been killed:
              M13_widthdecline   `ok = 0;' -> `if (bufdepth == 4) ok = 0;'   14/14 AND 19/19
              M14_lineardecline  `ok = 0;' -> `if (linear) ok = 0;'          14/14 AND 19/19
          Every declined-type row drives a 32-bit LIN_A mode, so the exempted joint cells
          {declined type} x {bufdepth != 4} and {declined type} x {tiled} are entered by no row.
          Both axes ARE exercised elsewhere in the probe, at a SUPPORTED type where `ok' is never
          cleared -- so the axes are covered and their JOINT with the decline is not.  Reachable:
          mode 0x10f0 reaches the arm at bufdepth 1, one hex digit from the row's own constant.
          THE ROUND IS HELD ON THIS.  The seat did not grade it; row demand and the L1/L2
          disposition are the round's call, and the joint space it names is
          {declined type} x {bufdepth 1,2,4,8} x {tlb_mode 0,1,2,4}, of which today's rows occupy
          one cell.  Closing only at bufdepth 1 is the `#499' repaired-at-the-mutant's-address trap.

     THE INLINE `*** OWED ***' MARKERS BELOW ARE SUPERSEDED BY THIS BLOCK.  Every score is read
     from a log ending `SGICOLOUR_DONE'.

     TABLE 1 -- Opus seat, FROZEN 14-row instrument + frozen baseline, /tmp/gxopus519,
     killtable_20260910/TABLE1.out and 19 .raw logs:
         BASE 14/14   (HEAD 6/14, null medium 6/14, fix 14/14)
         M1_reinstate       6/14 (b)      M2_noguard          9/14 (d)
         M3_zerofill       10/14 (d)      M4_okinlatch       13/14 (d)
         M5_nolatch        13/14          M6_sharedbit       13/14
         M7_silent         10/14          M8_declineall      10/14  reds live/ci8/rgb/abgr
         M9_dropcase_ci    13/14          M10_dropcase_abgr  13/14
         M11_null           6/14 (c)      M12_prefix_reworded 13/14
         M13_widthdecline  14/14 *** TOTAL ESCAPE ***
         M14_lineardecline 14/14 *** TOTAL ESCAPE ***
     M8's reds independently CONFIRM the PRETABLE 6.a correction: the all-declined mutant reds
     `live', not `live silent'.

     TABLE 2 -- 16-row instrument, main loop, /tmp/gx519, t2/SCORES2.txt:
         BASE 16/16;  M13_okorx 15/16 and M14_okory 15/16, each killed by `ycrcb x4y1' ALONE --
         the row grok's one-token edit demanded;  M15_texrd 16/16, the PREDICTED escape, measured
         rather than disclosed as a prediction.

     TABLE 2b -- 19-row instrument on the bracket-edited source:
         BASE_final 19/19;  M16_dropcase_rgb 18/19 (rgb put);  M17_dropcase_rgba 17/19 (live,
         live silent).  The two accept rows that had only the all-declined mutant now have their own.

     TABLE 2c -- 19-row instrument, the latch-collision CLASS CLOSURE:
         BASE_19 19/19;  M15_texrd_19 18/19 and M18_sharedbit_tlba 18/19, BOTH killed by
         `allbits announce'.  The mutant that escaped table 2 is killed by the closure, which is
         the measurement the disclosure was replaced with.

     The clone was restored from SEC, rebuilt, and its sentinel cleared.
================================================================================ -->

# `#519` sgirandomcolour: the colour-type PUT default wrote four host-PRNG bytes into guest memory, and a DOCUMENTED colour type reached it

**THE DEFECT.** `horrible_getputpixel()` in `src/devices/dev_sgi_re.c` packs one pixel for the drawing
engine's PUT by switching on the destination mode's TYPE nibble. Four of the sixteen nibbles are
implemented (CI, RGB, RGBA, ABGR); the `default:` arm did `buf[0..3] = random()` and an UNLATCHED per-pixel
`fatal()`, after which the common store below wrote the buffer into the destination. `fatal()` returns
(`src/core/debugmsg.c`, `void fatal(`: no early-out, no exit), so the fill was live. Twelve nibbles reach
the arm, `DE_MODE_TYPE_YCRCB` (0xf0) -- a mode `crmfbreg.h` documents -- among them, so a guest driving a
documented mode received the HOST's PRNG output in its framebuffer, per pixel, differently on every run.
Filed 2026-09-06 by the grok seat on the `sgirandompixel` (#504) design panel as the same class at a second
site ("`default:` of the COLOUR-mode switch still does `buf[n] = random()` and then writes those bytes"),
verified by reading before filing; nobody else on that panel saw it.

**WITNESSED AT RUNG 3 BEFORE ANY EDIT** (`regress/sgi_re_colourdefault_probe.py`, unmodified `-E sgi -e ip32`,
built by agy as the INDEPENDENT-TRANSPORT FALLBACK while both Anthropic seats were walled -- HTTP 429
"session limit, resets 3am" on the Agent tool, the shared-transport class; `regress/artifacts/sgirandomcolour/
WITNESS_brief_agy_20260910.md`, transcript `agy_witness_20260910.md`): a guest programs the DE for a LIN_A
32-bpp destination at physical 0x10000 (`re_linear_a[0] = 0x10`), pre-paints the word 0x11223344, fires one
RECT PUT at (0,0) with type YCRCB and again with a reserved nibble (0x50), and reads the word back through
KSEG1. On HEAD `1ce8296` BOTH unsupported-type PUTs replaced the paint with bytes that are neither the paint
nor any packing of the colour (0x56e8857a and 0x38abc4e1 on two runs -- `witness_20260910/HEAD_run1.out`,
`HEAD_run2.out`), the `determinism` row differs across runs, and the supported RGBA control lands
0xaabbccdd: **2/5**, liveness and device-signature controls green. **5/5** on the fix with the same script
(`fix_20260910/FIX519_run1.out`).

**THE DESIGN, adjudicated 2026-09-09 on the five-seat pass-1 panel plus codex's separate DESIGN2 reading
(`regress/artifacts/sgirandomcolour/panel_design_20260908/`, ledger entry RULING-DESIGN): MEMBER 3, DECLINE +
LATCHED ANNOUNCE, in grok's candidate (b).** For an unsupported colour type, SKIP ONLY THE `memory_rw` STORE --
a one-local `ok` guard around the single store statement, never an early `return` (the sketch rule: the
helper's common tail must still run) -- so the destination keeps what the guest had; delete the four
`random()` assignments and the per-pixel `fatal()`; announce ONCE per device instance on an INDEPENDENT latch
bit. Five of five seats chose member 3 and four of five chose (b) over (a) zero-fill-and-store (glm); (a)
publishes a colour the guest did not ask for -- "random() with the entropy stripped" (grok). Member 7,
IMPLEMENT YCRCB, was named and refused: no packing specification, and a guessed packing publishes wrong
colour data. `sgirebufuninit` -- the GET default arm and the depth-8 buffer tail -- stays a SEPARATE round.

**THE FIX** (`src/devices/dev_sgi_re.c`, 3 hunks, 48 additions of which 3 blank, 13 deletions -- 61 changed
lines by `diff | grep -cE '^[<>]'`, against HEAD `1ce8296`'s file -- the pre-fix copy the null-medium
mutant M11 restores is byte-identical to it, `cmp` verified): `int ok = 1` at the top of the
PUT branch; the `default:` arm sets `ok = 0` and announces once on its OWN bit `SGIRE_W_BADCOLOR = 1 << 12`
(the enum's last-enumerator convention followed: the "NEXT FREE BIT" sentence moved with it and the copy
above demoted, per that comment's own instruction); the store is `if (ok) cpu->memory_rw(...)`. The announce
keeps the old literal `[ put: color mode = 0x%x ]` as its PREFIX because the witness attributes on it, and
carries the vertex (`x=%i y=%i`); its stray second closing bracket (grok "cosmetic", minimax) was fixed to
two bracketed units mirroring the BADMODE sibling's shape -- ONE TOKEN in a string literal, after table 1
had started on its frozen baseline, and no row or mutant reads the bracket. `random()` is gone from
executable code in the file (grok, by reading). The GET default arm is untouched.

**THE DETECTOR, shipped with the fix in the same probe: 19 rows.** *** OWED: the final BASE score on the
final source and instrument (`killtable_20260910/t2/BASE_19.raw`). *** Contract (clause (e), in the probe
header): (b) the verbatim arm reinstated; (d) the `ok` guard removed, the decline turned into a zero fill,
`ok = 0` moved inside the latch, the latch removed, the latch SHARED with ANY of the twelve other warn bits
(`allbits announce`, one session priming every other latch first, the class closure
`sgi_re_width_probe.py`'s `tex xbit` row established -- see the repair chain), the announce silenced, a
supported type dropped from the switch (its accept row), the accept side announcing, the guard qualified on
the vertex (`ycrcb x4y1`: linear-path `ofs = x & 4095`, so a (4,1) PUT reaches the second pre-painted word).
NOT rowed, disclosed: the GET default arm (`sgirebufuninit`); 16-bit and depth-8 store widths; vertices
other than (0,0) and (4,1); per-instance latching (one RE instance); the ten undriven type nibbles (the
decision does not depend on the nibble's value; the announce prints it); and `two declined` does NOT
distinguish the skipped store from an early `return` -- after the PUT switch the guarded store is the only
statement, so the guard's form is a readability choice, not an observable (grok, minimax).

**THE PRE-TABLE CHECK** (`killtable_20260910/PRETABLE.out`, sections 1-5 written 03:51, BEFORE table 1's
baseline copy at 04:06 -- the order is proven by the verbatim copy inside `PASS2_brief_20260910.md` at
04:00:19, NOT by the file's mtime, which four appended subsections have since moved; the header's own
"~04:2x ... mtime is the proof" clause was a guessed time and is withdrawn in 6.i). It found the sibling
asymmetry (#504's BADMODE arm RETURNS; this one falls through with the store skipped), mapped every added
comment sentence to a row or a sentence, and named per row the mutant and the channel -- and two of its
sentences were WRONG and are corrected in 6.a-6.i: `M_declineall` reds `live`, not `live silent` (the
announce sits in the default arm only), and "`two declined` pins skipped rather than returned early" is
false.

**PASS 2 ON THE REAL DIFF** (`regress/artifacts/sgirandomcolour/pass2_20260910/`, brief
`PASS2_brief_20260910.md` with the diff, the detector block and PRETABLE 1-5 inlined). SIX of SEVEN scriptable
transports answered -- the kimi CLI on its weekly 403 wall and COVERED by `kimi-k3:cloud`; agy DELIBERATELY
NOT FIRED (measurement reserve; it had built the witness); the Opus seat holding table 1; the main loop as
Fable adjudicating. In the seats' own words: codex **"REVISE the detector and coverage claims. The submitted
store guard is correct, but 'all 14 rows pass' does not establish the claimed floor"**; grok **"NOT RATIFY the
detector as complete; the product fix is sound"**; glm "the fix as displayed is semantically sound ... but two
of the brief's own meta-premises fail packet-internal audit"; deepseek "No self-contradiction ... Q4:
none/36"; minimax "mostly sound. Two real defects"; the kimi substitute "the guarded-decline logic itself is
sound". **THE FIX STOOD -- no seat found a defect in the product change.** Every detector finding was
pre-ship (L1) or a wrong record (L4) and all were repaired in round:

* **Two ONE-TOKEN escapes of the 14-row instrument** (grok, from the tree; codex confirmed): `if (ok)` ->
  `if (ok || x)` -- every PUT sat at vertex (0,0) -- and `SGIRE_W_BADCOLOR` -> `SGIRE_W_TEX_RD` -- the
  independence row fired BADMODE only. Rowed: `ycrcb x4y1` + `x4y1 announce` (a YCRCB PUT at (4,1); the
  first cut used (1,0) and claimed `ofs = 1 * bufdepth`, WRONG for the linear path, which computes
  `ofs = x & 4095` -- corrected before any table ran on it), and the all-bits closure below.
* **The brief's own defects** (the packet-fed seats): "2 hunks, 58 changed lines" against three hunk headers
  in the same packet (glm, codex: 3 hunks, 61 lines, 58 non-blank); the five witness rows referenced but not
  inlined (minimax) -- a section-C2 brief defect, recorded.
* **Wrong records in the contract and PRETABLE** (codex, grok, minimax): skip-vs-return; "the PUT arms assign
  four bytes" (CI assigns one); "the arm does not read the nibble" (the announce prints it); "four host-PRNG
  bytes" without its width qualifier (one at 8 bpp, four at 32, four plus an unassigned tail at depth 8);
  `indep paint` claimed to observe both declined PUTs while `setup_put()` re-paints before the second.
* **Accept-row failability** (minimax: `M_dropcase_rgb` absent from the plan; grok: two accept rows had only
  the all-declined mutant): M16_dropcase_rgb and M17_dropcase_rgba added.
* **One packet-fed claim was wrong and is recorded**: deepseek's "M8_declineall makes `live silent` read 1" --
  it does not; the announce is in the default arm only (6.a).
* **The one seat that asked for a warrant got one**: "the struct is shared by four handlers" -- `d->warned` is
  used in exactly four functions (awk over the file); "the two demotions above it" are PRIM_OP's and
  BADMODE's.

**THE REPAIR CHAIN -- four cuts, then the class closure that codex's records audit forced.** Cut 1 added the
(1,0) row; cut 2 re-cut it to (4,1) on the linear-path arithmetic, with the second-word paint emitted ONLY for
a non-origin vertex so the nine pre-existing sessions' command streams are byte-unchanged (codex verified:
"No old session's commands differ") and table 1's per-row kills carry over; cut 3 fixed the contract sentences
and the bracket and added M16/M17; cut 4 came from a farmed codex RECORDS AUDIT of the repair record
(`codex_pretable6_20260910.txt`, NO-GO, six items, all disposed in PRETABLE 6.i): the shared-latch-bit class
had been DISCLOSED on the premise that rowing the eleven non-BADMODE bits costs one session per bit, and codex
refuted the premise from the tree -- ONE session primes every other latch (byte stores to the six RE windows
and the DE window, a store to and a load from the straggler offset, an unimplemented drawing op, a LIN_B
rectangle, a 64-bit TEX read), the sequence `sgi_re_width_probe.py`'s `tex xbit` row had already proved. So
`allbits primed` (12/12, the row proves its own setup), `allbits announce` (a latch sharing ANY existing bit
reads 0) and `allbits paint` close the class, and the expected escape became an expected kill. The same audit
corrected four more sentences of the repair record (sessions vs rows; the overlapping byte is word 1's MOST
significant byte and an overlap is a possible change, not a guaranteed red; the chronology; the two
demotions) and withdrew a partition justification of mine for the vertex row in favour of the contract's own
"the `ok` guard REMOVED" sentence -- for a guest, a vertex-qualified guard IS the guard removed.

**THE TABLES** (`killtable_20260910/`; scratch clones, frozen instruments, every score read from a log ending
`SGICOLOUR_DONE`):
* Table 1 (Opus seat, 14-row frozen instrument `sgi_re_colourdefault_probe.FROZEN.py`, frozen baseline
  `BASELINE_FIX519.c`, `/tmp/gxopus519`, mutator `mut519.py`): *** OWED: BASE 14/14 (`BASE.raw`), M1_reinstate
  6/14, M2_noguard 9/14, M3_zerofill 10/14, M4_okinlatch 13/14, M5_nolatch 13/14 measured so far; M6..M12 and
  the seat's report. *** Its baseline differs from the shipped source by the one-token bracket edit.
* Table 2 (main loop, 16-row instrument `t2/sgi_re_colourdefault_probe.REPAIRED16.asrun.py`, `/tmp/gx519`
  restored from SEC and rebuilt fresh at the end, `t2/SCORES2.txt`, 04:30-04:48): BASE **16/16**
  (`t2/BASE.raw`); M13_okorx **15/16** and M14_okory **15/16**, each killed by `ycrcb x4y1` alone
  (`t2/M13_okorx.raw`, `t2/M14_okory.raw`) -- the row grok's one-token edit demanded, and the y form with it;
  M15_texrd **16/16, THE PREDICTED ESCAPE** (`t2/M15_texrd.raw`) of the 16-row instrument, measured before
  the class closure rather than disclosed as a prediction, and re-measured on the 19-row instrument in table 2c.
* Table 2b (`t2/`): *** OWED: BASE_final on the bracket-edited source, M16_dropcase_rgb, M17_dropcase_rgba. ***
* Table 2c (19-row instrument): *** OWED: BASE_19, M15_texrd_19 (expected KILLED by `allbits announce`),
  M18_sharedbit_tlba_19. ***

**The repair chain owes its own pass**: *** OWED: the closing pass on the repair diff (the instrument against
the frozen 14-row copy, plus the one-token product edit) with the table-2/2b/2c scores as its denominator. ***

*** OWED: propagation of `dev_sgi_re.c` to `est/` and the three build trees with the two-part clearance RUN
(`propagate519.out`); at the time of writing `build/` deliberately still carries HEAD's `dev_sgi_re.c`, which is
what the HEAD detector runs measured. *** Witness: `probe:regress/sgi_re_colourdefault_probe.py` (rung 3, agy;
2/5 -> 5/5 -> 16/16 `FIX519_detector_run3.out` -> 19/19 OWED).
