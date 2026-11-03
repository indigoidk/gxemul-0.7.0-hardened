# ADJUDICATION PASS (F2) -- `jazzvecdeassert` (#578, OB-22): the pass-2 findings with my dispositions, and the repair's own review

Please do not simply ratify.  A recent panel had seven of nine seats confirm a premise this project's brief stated wrongly; CHECK THE
PREMISES, not just the derivations.  The load-bearing question is section 5's Q1: which of my accepted dispositions is WRONG?  I accepted
twenty-three findings in some form; a round that accepted everything has either had a good panel or has stopped arguing, and only a seat can
tell which.  If you cannot settle a point from this packet, say "not checkable from the packet" and name the fact that would settle it.

The tree under review is `GXEMUL-SEC/src/` (HEAD `50f9c601`; `src/` and `regress/` are unchanged since `987cb596` -- every commit since is
records).  Ignore any other `src/` under the project root (`./src/` and two copies under `_archive/` are pristine 2021 upstream).  The fix is
NOT committed: the shipping product diff is `GXEMUL-SEC/regress/artifacts/jazzvecdeassert/killtable3_20261102/product_c.diff` (inlined in
section 1), the repaired detector `_scratchpad/w578/jazz_vector_probe.py` (as run by table 3: `killtable3_20261102/jazz_vector_probe.ASRUN.py`,
md5 7b3e17e7d3f0), the gate section `_scratchpad/w578/gate_mips.NEW2.sh`.  Packet-fed seats cannot read files: everything load-bearing is
inlined below.

VERDICT LINE FIRST, in this form: `F2 VERDICT: RATIFY | RATIFY WITH CHANGES (n) | NOT RATIFY`, then the body.  Mark each claim you make
READ (from this packet), REASONED, or MEASURED (you ran something).

## SETTLED PREMISES (recorded resolutions; a question below depends on each)

* S1. `dev_jazz.c`'s `DEVICE_ACCESS(jazz_jazzio)` (HEAD :657-702) ended every access with `INTERRUPT_DEASSERT(d->mips_irq_3)` under the
  comment "This is needed by Windows NT during startup".  Guest-visible: a vector read with a second JAZZ line pending dropped the CPU's IRQ3
  (OB-22).  Witness: rung 3, unmodified `-V -e pica`, `witness_20261102/` 11/13 on HEAD, 13/13 fixed.
* S2. The fix is the DELETION of that statement (not pass 1's conditional).  Invariant I: IRQ3 is kept EQUAL to
  `(int_asserted & 0x7fff) && (int_enable_mask & R4030_EXT_IP3)` by its only three writers -- `jazz_interrupt_assert()` (:144),
  `jazz_interrupt_deassert()` (:154) and the EXT_IMASK arm (:467/:469, transitions only); `mips_irq_3` appears nowhere else in the file but
  the declaration, the mask arm, the deleted tail and the connect; the MIPS `mtc0 Cause` arm writes IP0/IP1 only (`cpu_mips_coproc.c:949-954`).
  Census run by the main loop at pass 1 and by the Opus and Grok seats at pass 2 (READ for you; MEASURED by them).
* S3. Equivalence of the conditional and the deletion was MEASURED (M_del 13/13 on the witness; M_cond 22/22 on table 2; M_cond 26/26 on
  table 3) -- and, as the Opus seat said, that is ENTAILED by I rather than independent of it: the rows cannot reach an I-violating state.
* S4. `est/src/devices/dev_jazz.c`'s `jazz_jazzio` body is byte-identical to SEC's (its tail at :661-662), so the same applier lands in both;
  est keeps the pre-#69 predicate `int_asserted & int_enable_mask & 0x7fff` in ITS assert (:120), deassert (:130) and mask arm (:430-440),
  so est has no `R4030_EXT_IP3` and the conditional's text would not compile there.  est has NO binary (source tree).
* S5. Healing on HEAD: a dropped IRQ3 came back when `jazz_interrupt_assert()` ran again -- a fresh line assert, `DEVICE_TICK(ns16550)`
  re-asserting a still-enabled UART (`dev_ns16550.c:92-97`), `DEVICE_TICK(jazz)` asserting the timer line (:294-308, once `interval_start >
  0` or `jazz_timer_value != 0`; the assert tests the WHOLE pending set, so the timer line's own bit being outside 0x7fff does not matter)
  -- or on an EXT_IMASK TRANSITION into the pending-and-enabled state (:466-469); a same-value mask rewrite heals nothing.  Severity LOW for
  OpenBSD (its `pica_iointr` loops on the vector until 0 and its timer is armed); NT unmeasured.
* S6. The `fatal()` in the `default:` arm (:685-693) PRINTS AND RETURNS (`debugmsg.c:384-391`); the tail runs after it.  It is unlatched and
  guest-drivable (every byte access to offsets 1 and 3 prints a line) -- out of this round's scope, filed (F18 below).
* S7. The gate's `count()` is `grep -ac` in BASIC regex (`regress/lib.sh:326-330`); the probe prints `%-14s ` so a 13-character name is
  followed by exactly two spaces; the gate anchors `^name  .*ok$`.
* S8. The repair chain rule: a repair made in response to a pass 2 owes its own pass, scoped to the repair diff, closing on the first VALID
  pass that finds zero floor breaches (the diff delivered, the roster's misses named, the zero carried with its denominator).  The ask-again
  is SPENT on this detector (table 2 was clean; pass 2 was the one ask; table 3 is clean).  So anything new a seat names now is FILED
  with its predicted score unless it is a FLOOR breach of the repaired detector, which is L2 and repaired in-round.

## 0. The pass-2 findings (pass2_20261102/: opus5.md SHIP WITH CHANGES (5); grok.txt SHIP WITH CHANGES (3); ollama_glm-5.3 SWC (3);
## ollama_deepseek-v4-pro SWC (3); ollama_minimax-m3 SWC (3); ollama_kimi-k3 SWC (2); codex: SEAT WALLED, gpt-6-astra on the hotmail
## login "try again at Nov 3rd 01:10", 0-byte answer) and my dispositions

Every seat held the deletion.  Every seat found the detector's contract false and its (d) enumeration incomplete.  Dispositions:

* **F1 (all six seats): the (default, WRITE) label cell was unrowed while the contract said every label is rowed, read and write.**
  ACCEPTED -- L4 wrong record AND a floor cell under the joint-cell reading (the body tests both partitions; the cell is guest-reachable
  by `sb` to VEC+1/VEC+3).  Repaired in-round: row `jz ip dfltw` (`st8(VEC+3, 0x5a)`); mutant M_dfltw (`relative_addr != 0 &&
  relative_addr != 2 && writeflag == MEM_WRITE`) predicted 24/26 (dfltw red, com1 inherits), MEASURED 24/26.
* **F2 (Opus C2, Grok, GLM, DeepSeek, minimax, kimi): `idata` was driven at 0 only; `if (idata != 0)` escapes and drops IRQ3 on OpenBSD's
  own `out16(PICA_SYS_LB_IE, mask)` path.**  ACCEPTED -- `jz ip lbiew` now stores 0x0f (and as a HALFWORD, F3); M_idnz 23/26 and M_id0
  19/26, both as predicted.  Graded clause (e) debt closed for free, not floor (`idata` is stored, never tested by the body).
* **F3 (Opus, Grok, GLM, kimi): `len == 2` was never driven; PICA_SYS_LB_IE is a 16-bit register.**  ACCEPTED -- the lbiew store is `sh`
  (one more one-instruction stub, 0xa4220000); M_len2 25/26 as predicted.
* **F4 (Opus): `jazz_timer_value` was held at 0 for the whole run, and the header's reason ("so the Linux? tick arm stays unarmed") was
  wrong -- that arm asserts only on `pending_timer_interrupts > 0`, a count produced by a `timer_add` callback (`timer_tick`, :273-277,
  `timer_add(100.0, ...)` :786) that the debugger stops while interacting, so it is inert under `step`.**  ACCEPTED -- 0x0f from lbiew
  on; M_lbnz 21/26 as predicted; the header now says why the arm is inert.
* **F5 (Grok): OpenBSD's `pica_iointr` reads the vector with `inb(PVIS)` -- a BYTE -- and no row read offset 0 as a byte, so
  `if (relative_addr == 0 && len == 1)` kept 22/22 while restoring the named defect on the real guest's own access.**  ACCEPTED -- this is
  the one conjunction the real guest exercises, and the generic "conjunctions are disclosed" sentence would have DISCLOSED the live defect
  path.  Rows `jz vec byte` (ld8(VEC) == 0x24, the device signature at len 1) and `jz ip vecb`; M_vecb 25/26 as predicted.  Other
  conjunctions stay disclosed by name (contract).
* **F6 (Grok): `if (relative_addr == 3)` -- the page's other default byte -- escaped.**  ACCEPTED -- `dfltw` writes offset 3 while `dflt`
  reads offset 1, so both default offsets of the 4-byte page are driven; M_off3 24/26 as predicted.  (Offsets 1 and 3 are ONE cell of the
  body's partition; this is the unrowed-slot class closed because it cost nothing.)
* **F7 (Opus C3, Grok, GLM, DeepSeek, minimax, kimi): the product comment over-narrowed ("a vector read ... with a second line pending";
  "until some line was asserted anew") and over-claimed ("recompute ... on every change"; "as in the tree's other interrupt controllers" --
  Grok: `dev_algor.c`'s P5064_PCIINT deasserts mips_irq_3 on a read).**  ACCEPTED -- the shipped comment is section 1's.  It says "on
  every access", "while JAZZ lines were still pending", "until a line was asserted anew or EXT_IMASK re-enabled IP3", "kept equal to", and
  makes no claim about other controllers.  The ticks are "a line asserted anew" (they re-assert a UART or the timer line) -- see D1.
* **F8 (Opus C4): a timed-out `set_reg`/`step` left `exec_stub` returning a value as if the store had happened, and a skipped store
  reads exactly like a fixed build on every IP3 row after it.**  ACCEPTED -- `Emu.bad` is set by any command that dies or times out and
  by `exec_stub` when any of its four commands returned None; the probe prints `JAZZVEC_DRIVER=ok|bad` and the gate checks it.  FOUND AND
  FIXED while building it: `quit` ends the session without a prompt and set the flag on every run (dryrun26/: 26/26 with DRIVER=bad);
  `close()` now saves the flag around the quit (dryrun26/fixedb2.out: 26/26, DRIVER=ok; every table-3 leg DRIVER=ok except the null
  medium, where it is correctly `bad`).  Recorded in `killtable3_20261102/ASRUN_NOTE3.txt`.
* **F9 (Opus C4): the gate did not set `JAZZVEC_LOG`, so each run left `/tmp/jazzvec_<pid>.log` behind; and it checked `JAZZVEC_RESULT=`
  rather than the completion sentinel.**  ACCEPTED -- `JAZZVEC_LOG="$LOGDIR/gate_jazz_vector.pty"`; the completion check greps
  `JAZZVEC_DONE`; a `jazz_vector driver completed every command` check reads `JAZZVEC_DRIVER`.
* **F10 (Opus C5, GLM change 3, minimax): "invariant I" is SEC's; est's writers keep IRQ3 equal to est's OWN predicate.**  ACCEPTED as
  a record: est's assert raises iff `int_asserted & int_enable_mask & 0x7fff`, its deassert lowers iff not, its mask arm acts on that
  predicate's transitions (S4) -- the same induction over a different predicate, so the deletion is equivalent in est too; est's copy is
  UNMEASURED (no binary; and the probe as written could not measure it: under est's per-line predicate EXT_IMASK=0x2 masks lines 8/9 out).
  GLM's worry -- that est's assert might raise under a WEAKER condition and leave a state the old tail cleaned -- is answered by the quoted
  arms: est's three writers are as closed as SEC's.
* **F11 (Opus): "M_b: the unconditional deassert reinstated verbatim" -- the STATEMENT is verbatim, the comment is not (the mutator keeps
  the #578 comment).**  ACCEPTED -- records say "the removed statement reinstated"; floor (b) is satisfied behaviourally.
* **F12 (Opus Q5; its own addendum refutes the first hypothesis): M_b's binary md5 differs from HEAD's in every table.**  Opus's
  build-directory hypothesis is refuted by #577 (its M_b, built in another directory with a twelve-line comment kept, has HEAD's md5);
  its second hypothesis (`CHECK_ALLOCATION` at :712 embeds `__LINE__`, which the comment's line shift changes) is UNMEASURED.  DISPOSITION:
  "cause not established" stays in the record; I ran `strings` on HEAD's and the fixed binary and they differ in code, which is the wrong
  comparison (the fix deletes an instruction sequence) -- the settling check is `strings` on HEAD's binary against a rebuilt M_b, not run.
* **F13 (minimax, Grok): "self-heals on any booted OS" overclaims; LOW stands only for a guest that arms a heal path.**  ACCEPTED --
  records say "a guest that arms a heal path (an interval timer, a still-enabled UART, a nonzero LB_IE write); OpenBSD does; NT unmeasured".
* **F14 (Opus Q2): of the ruling's five warrants, (ii) measured equivalence is entailed by I and (iii) the est-compile fact is a
  convenience (est could take a conditional in its own predicate); (i) and (v) carry.**  ACCEPTED as the record's wording.  minimax's
  point that (iii) rejects the exact text, not the concept, is the same correction.
* **F15 (Opus Q2): the NT-startup risk -- if NT relied on the blanket deassert as a stand-in for LB_IE masking -- falls on the conditional
  and the deletion equally (neither fires with lines pending and enabled); only modelling LB_IE as a mask keeps that case.**  ACCEPTED --
  a note under `jazzlbmask`, which is where that risk is carried.
* **F16 (Grok): OB-22 has SIX carriers in OUTSTANDING_BUGS.md, not three: :2037, :2509-2512, :2605-2606, :2869, :2926, :2965 (at HEAD
  50f9c601).**  ACCEPTED -- all six marked fixed in place, with the :2965 "until next edge/mask write" wording corrected (a same-value mask
  write heals nothing; S5 names the heal paths).  minimax's demand that each be mapped to a file/tree before marking: all six are prose
  in this fork's bug file about `GXEMUL-SEC/src/devices/dev_jazz.c`; none names the pristine `./src/`.
* **F17 (GLM, minimax): "self-contained" is proved for the probe; the ledger's witness `jazz_vector_witness.py` imports
  `_scratchpad/gxprobe.py`.**  ACCEPTED as wording -- the witness is the pass-1 rung-3 witness built with the harness library and
  committed as an artifact (CLASS_WITNESS); the shipped, gated detector is the self-contained probe; the ledger's `witness` field names the
  former and the detector line the latter.
* **F18 (kimi, Opus): the `default:` arm's `fatal()` is unlatched and guest-drivable; `jazz_20`/`jazz_a0` have the same shape.**  FILED
  as `jazziodfltflood` (LOW, floodclass; house idiom `(once)`); out of this round's scope (the round deletes a statement after that arm and
  changes nothing in it).
* **F19 (DeepSeek Q4): the 20 s prompt wait is load-sensitive.**  NOTED -- it can only false-FAIL (None -> FAIL), never false-pass (F8
  closes the one false-pass direction); the battery runs alone by owner directive.
* **F20 (GLM Q4a): could the `default:` arm's print interleave with the prompt wait?**  MEASURED -- the transcripts show the print, then
  `GXemul>`; `jz ip dflt` is green on the fixed build in the witness, table 2 and table 3.
* **F21 (kimi Q1): lowering line 8 with line 9 still pending does not re-raise a dropped IRQ3, so "recompute on every change" overstated.**
  ACCEPTED via F7 ("kept equal to" -- the deassert handler lowers on the predicate's falling edge and does nothing else; the state kimi
  describes is reachable only through the deleted tail).
* **F22 (Opus): `M_c_absent.raw` said "binary newer than dev_jazz.c: yes" for `/bin/true`.**  FIXED in table 3's driver (prints N/A when
  no source tree sits beside the binary).
* **F23 (Opus, Grok): nothing stronger than "expected invisible" for OpenBSD until gate 4's boot runs with the fix.**  ACCEPTED -- the gate
  (arc boot 13/13, then this probe) runs end to end on the propagated tree before the landing commit; the record will cite that run.

## 1. The repair diff (the material this pass reviews)

### 1a. The product comment (apply_fix578b.py -> apply_fix578c.py; the deleted statement is unchanged; `product_c.diff`, +7 -2)

```
-	/*  This is needed by Windows NT during startup:  */
-	INTERRUPT_DEASSERT(d->mips_irq_3);
+	/*  #578: no deassert here.  This tail used to deassert the CPU's IRQ3
+	    on every access ("needed by Windows NT during startup"), dropping
+	    a level interrupt while JAZZ lines were still pending until a line
+	    was asserted anew or EXT_IMASK re-enabled IP3 (OB-22).  The CPU
+	    line is kept equal to "a line 0-14 pending and EXT_IMASK.IP3 set"
+	    by jazz_interrupt_assert()/_deassert() and the EXT_IMASK arm; an
+	    access to this register no longer touches it.  */
```

### 1b. The detector (jazz_vector_probe.py, 22 -> 26 rows; `repair_probe.diff`, docstring hunks condensed to the row list and contract)

Rows added or changed (the full row sequence is in the probe; `reheal()` = com0 IER 0 then 2, re-raising IRQ3 on every build):
```
 row("jz vec again", ld32(VEC), (8 + 1) << 2)
+reheal()
+row("jz vec byte", ld8(VEC), (8 + 1) << 2)
+row("jz ip vecb", ip3(), IP3)
 reheal(); st32(VEC, 0)
 row("jz ip vecw", ip3(), IP3)
 reheal(); ld8(VEC + 2)
 row("jz ip lbie", ip3(), IP3)
-reheal(); st8(VEC + 2, 0)
+reheal(); st16(VEC + 2, 0x0f)
 row("jz ip lbiew", ip3(), IP3)
+row("jz lbie rb", ld8(VEC + 2), 0x0f)
 reheal(); ld8(VEC + 1)
 row("jz ip dflt", ip3(), IP3)
+reheal(); st8(VEC + 3, 0x5a)
+row("jz ip dfltw", ip3(), IP3)
 st8(COM0 + IER, 0x00)
 row("jz vec com1", ld32(VEC), (9 + 1) << 2)
```
Driver: `STUBS` gains `"sh": 0xa4220000`; `st16()`; `Emu.bad` set on a dead pty, a failed write, a prompt timeout, or any None inside
`exec_stub` (which then returns None instead of reading v0); `close()` saves the flag around `quit`; the probe ends with
`JAZZVEC_RESULT=n/N`, `JAZZVEC_DRIVER=ok|bad`, `JAZZVEC_DONE`.  The new contract paragraph (verbatim):

> CONTRACT (clause (e)): the rows drive lines 8 and 9 only and the mask values 0x2 and 0 only; a re-introduction of the removed deassert
> keyed to a line this table does not drive (0-7, 10-14: `if (!(int_asserted & 0x0300)) ...`), to the timer line, or to a mask value other
> than those two, is disclosed, not rowed.  Every access-label cell of the enclosing function's own tests -- {0, 2, default} x {read,
> write}, six cells -- is rowed with lines pending (vec/vecb/after/onevec/com1, vecw, lbie, lbiew, dflt, dfltw), so a re-introduction
> keyed to `relative_addr` and/or `writeflag` reds; both default offsets of the 4-byte page are driven (1 read, 3 written); the function's
> other inputs are each driven at two or more values with a pending-lines row on each side -- `len` 1 (vec byte, lbie, dflt, dfltw), 2
> (lbiew), 4 (vec, vecw); `idata` 0 (vecw) and nonzero (lbiew, dfltw); `jazz_timer_value` 0 (rows before lbiew) and 0x0f (rows after) --
> so a re-introduction keyed to any ONE of them reds, and the one CONJUNCTION the real guest exercises, offset 0 read as a byte
> (`relative_addr == 0 && len == 1`, the inb(PVIS) path), is rowed by `jz ip vecb` (measured: table 3).  Any other conjunction of two or
> more inputs that selects no rowed cell (e.g. `len == 2 && relative_addr == 0`, `idata != 0 && relative_addr == 2 && len == 1`) is
> clause-(e) debt, disclosed.  Names stay at 13 characters or fewer (`%-14s`; the gate anchors `^name  .*ok$` with two spaces).  Ends with
> JAZZVEC_RESULT=n/N, JAZZVEC_DRIVER=ok|bad and JAZZVEC_DONE.

The docstring's mechanism sentence now reads "kept EQUAL to ... the assert handler raises it when that predicate becomes true, the deassert
handler lowers it when the predicate becomes false, and the mask arm acts on the predicate's TRANSITIONS (a same-value rewrite moves
nothing)"; the lbiew note explains why the "Linux?" tick arm is inert under step (F4).

### 1c. The gate section (gate_mips.sh, new block before "Publish the raw pty logs for gate 6"; `repair_gate.diff`)

```
 JVLOG=$LOGDIR/gate_jazz_vector.log
-python3 -u "$HERE/jazz_vector_probe.py" "$ARC_RIG/gxsec-gxemul" "$ARC_RIG/bsd" > "$JVLOG" 2>&1 || true
-if ! grep -q "JAZZVEC_RESULT=" "$JVLOG"; then
+JAZZVEC_LOG="$LOGDIR/gate_jazz_vector.pty" python3 -u "$HERE/jazz_vector_probe.py" "$ARC_RIG/gxsec-gxemul" "$ARC_RIG/bsd" > "$JVLOG" 2>&1 || true
+if ! grep -q "JAZZVEC_DONE" "$JVLOG"; then
...
+    jvdrv=$(grep -o "JAZZVEC_DRIVER=[a-z]*" "$JVLOG" | tail -1 | cut -d= -f2)
+    check "jazz_vector driver completed every command" "${jvdrv:-missing}" "ok"
     jvres=$(grep -o "JAZZVEC_RESULT=[0-9]*/[0-9]*" "$JVLOG" | tail -1 | cut -d= -f2)
-    check "jazz_vector rows run"     "${jvres#*/}" 22
+    check "jazz_vector rows run"     "${jvres#*/}" 26
     check "jazz_vector rows correct" "${jvres%/*}" "${jvres#*/}"
-    for v in <22 names>; do
+    for v in "jz imask" "jz com0 mcr" "jz com0 ier" "jz ip one" "jz ip both" "jz vec" "jz ip after" "jz vec again" "jz vec byte" "jz ip vecb" "jz ip vecw" "jz ip lbie" "jz ip lbiew" "jz lbie rb" "jz ip dflt" "jz ip dfltw" "jz vec com1" "jz ip com1" "jz ip onevec" "jz ip reheal" "jz ip maskoff" "jz vec masked" "jz ip maskon" "jz ip none" "jz vec none" "jz ip nt"; do
         n=$(count "$JVLOG" "^$v  .*ok$")
         check "  $v" "$n" 1
     done
```
The 26 names in the loop equal the probe's 26 `row()` names (diffed); all are 13 characters or fewer.  The pin is EQUALITY on purpose.

## 2. The pre-table block and table 3 (`regress/artifacts/jazzvecdeassert/killtable3_20261102/`)

`PRETABLE3.out` (mtime 21:06:01) precedes `base_head.raw` (21:07:50); the table ran 21:07:38-21:09:06 from a frozen copy of the driver,
in scratch clones of the HEAD tree (`/tmp/gxdivw`, dev_jazz.c cmp-identical to HEAD's) with a `.MUTANT` sentinel per clone; each `<leg>.raw`
names its binary, md5, freshness and the instrument's md5.  Every prediction matched -- score AND red set:

```
    leg         pred   got    red rows (IP3 read 0 where 0x800 wanted)
    base_head   17/26  17/26  after, vecb, vecw, lbie, lbiew, dflt, dfltw, com1, onevec          (a)
    fixedc      26/26  26/26  DRIVER=ok
    M_c_absent   0/26   0/26  every row None, DRIVER=bad                                           (c) null medium: no emulator
    M_b         17/26  17/26  the same nine                                                        (b) the removed statement reinstated
    M_offs0     21/26  21/26  after, vecb, vecw, com1, onevec
    M_offsne0   21/26  21/26  lbie, lbiew, dflt, dfltw, com1
    M_rd        20/26  20/26  after, vecb, lbie, dflt, com1, onevec
    M_wr        22/26  22/26  vecw, lbiew, dfltw, com1
    M_offs2     24/26  24/26  lbie, lbiew
    M_cond      26/26  26/26  EQUIVALENT (S3)
    M_uart      26/26  26/26  DISCLOSED (lines the rows do not drive)
    M_dfltw     24/26  24/26  dfltw, com1                     <- F1, the pass-2 escape, closed
    M_idnz      23/26  23/26  lbiew, dfltw, com1              <- F2
    M_id0       19/26  19/26  after, vecb, vecw, lbie, dflt, com1, onevec
    M_lbnz      21/26  21/26  lbiew, dflt, dfltw, com1, onevec  <- F4
    M_len2      25/26  25/26  lbiew                           <- F3
    M_vecb      25/26  25/26  vecb                            <- F5, the guest's own path, closed
    M_off3      24/26  24/26  dfltw, com1                     <- F6
```
"com1" red beside another row = the stacked-drop mechanism: a drop just before `st8(COM0+IER, 0)` is not healed by lowering line 8 while
line 9 stays pending (HEAD's own `jz ip com1`; `PRETABLE2_CORRECTION.out`).  The repair's forms are the forms the seats named; the
mutator inserts each one as `if (<predicate>) INTERRUPT_DEASSERT(d->mips_irq_3);` right after the #578 comment (presence pin: the
comment's last line, unique in the file).

## 3. Disagreements, both sides in their own words

* **D1 -- the comment's heal clause.**  Grok: "widen the healing clause ... `DEVICE_TICK(ns16550)` re-asserting a UART ... `DEVICE_TICK(jazz)`
  asserting `jazz_timer_irq`"; DeepSeek: "until some line was asserted anew, a mask transition, or the next timer tick".  Opus: "The timer
  tick and the UART tick are both 'a line asserted anew', so they are covered by the existing words.  The mask transition is not."  My
  ruling: Opus's wording (shipped, 1a) -- a tick re-asserts a LINE, and the comment should not enumerate device ticks that may change.
* **D2 -- F2's grading.**  Opus and kimi: `idata != 0` is clause-(e) debt (the body never tests `idata`); the main loop closed it anyway
  because it cost one constant.  kimi: "a smaller, more guest-visible escape than M_uart ... inside (d)'s own enumeration space (`idata` is a
  local of the enclosing function)".  My ruling: debt, closed -- the floor is the body-TESTED partition, and `idata` is stored, not tested;
  the DEPENDS-ON bound forbids promoting every local to a floor axis.  Nothing turns on the grade now that it is measured.
* **D3 -- the (0, len 1) conjunction.**  My pass-2 packet's contract called every conjunction clause-(e) debt; Grok showed that sentence would
  have disclosed the real guest's own access.  My ruling: the one conjunction the real guest exercises is ROWED and the rest stay disclosed by
  name -- is that the right line, or does the rule want every two-input conjunction over the driven values rowed (which is unbounded)?

## 4. What this pass is NOT asked to re-litigate

The deletion (S2, S3), the witness, tables 1 and 2, severity (S5 as corrected by F13), and the records items F10-F17 beyond checking their
wording are settled; review EFFORT goes to the repair diff (section 1); the FLOOR QUESTION is asked of the shipped composite (section 5 Q2).

## 5. Questions

* **Q1.** Of the twenty-three accepted dispositions in section 0 and the three rulings in section 3, WHICH IS WRONG?  Name it and the fact.
* **Q2.** The floor question, asked of the shipped composite: over the enclosing function's own tests (`relative_addr` {0, 2, other} x
  `writeflag` {R, W}) and the single-input families the contract names, is there a re-introduction of the deleted deassert that keeps all
  26 rows green and changes a guest-visible IRQ3?  Give the one-line predicate and your predicted score.  Per S8 it is FILED unless it is a
  floor cell of that enumeration -- say which you think it is.
* **Q3.** Is the shipped comment (1a) wrong anywhere -- a claim the code does not make true?
* **Q4.** The repair chain closes on this pass if it finds zero floor breaches.  Does it?  If you say zero, carry the denominator: which
  cells and which shapes you swept.
