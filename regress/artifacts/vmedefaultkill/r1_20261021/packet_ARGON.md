# `vmedefaultkill` (#568) -- THE REPAIR-DIFF PASS: review the repair the adjudication ordered, attack the first seat's answer, and ask the floor question of the shipped composite

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Check the premises, not just the derivations.  **THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/`'s
working tree, committed HEAD `86114a90`** (this round is uncommitted there: `src/devices/dev_vme.c`,
`regress/vme_default_probe.py`, the vme block of `regress/gate_arm.sh`, and `regress/artifacts/vmedefaultkill/`).
Another session's uncommitted edits sit in the same tree and are NOT part of this round: `src/devices/dev_pcc2.c`,
`dev_lca.c`, `dev_sh4.c`, `src/cpus/cpu_alpha_palcode.c`, `src/include/thirdparty/mvme_pcctworeg.h`, and several
`regress/` probes and gate scripts.  Three pristine-2021 copies of GXemul sit under the project root; line numbers off
by hundreds mean you are reading one.  **If you cannot read files that is expected** -- what you need is inlined; name
any premise you cannot settle from this packet.  READ-ONLY: write nothing to any project tree.  **VERDICT LINE FIRST.**

## 1. What this pass is, and the rule that stops it

Pass 2 of `#568` found ONE floor breach -- the population-2 announce arm's `if (writeflag == MEM_WRITE)` read as
`if (idata)` passed every row of the 34-row rev-2 probe, MEASURED 34/34, because every population-2 store the probe
made was non-zero -- plus records defects.  The adjudication pass (Fable 5.1, GPT-6 Astra, GLM 5.3, Grok 4.7; all
PROCEED WITH CHANGES) ordered a repair; it is built and measured (section 4).  **This is that repair's own pass (the
repair-chain rule).**  Review EFFORT is scoped to the repair diff -- settled design is not re-litigated.  The FLOOR
QUESTION -- does any one-edit mutant inside the fix's DEPENDS-ON enumeration still pass all 38 rows -- is asked of the
SHIPPED COMPOSITE (fix568b + probe rev 3).  **The chain CLOSES on the first pass that finds zero floor breaches
surviving adjudication, and the zero must carry its denominator: which predicates, lvalues and mutant shapes you
swept.**  A bare "no breaches" does not close it.

**One seat has already answered this pass: Fable 5.1, `VERDICT: CLOSE`, zero breaches over a stated denominator
(section 7).**  You are asked to ATTACK that answer, not to agree with it: a closing zero from one seat closes nothing
until the rest of the roster has tried to break it.

## 2. Settled (re-inlined)

* Census: 10 cased offsets; 26 population-2 registers (the header's word starts 0x04..0x8c minus the cased); 988
  population-1 word starts 0x90..0xffc; every sub-word start inside a population-1 or population-2 word faults; a
  sub-word access at a CASED base is serviced by that arm (population 4, `vmewidthlanes`, filed).
* The m88k load/store path delivers naturally-aligned accesses only; `ld.d`/`st.d` is ONE len-8 call; the debugger's
  NO_EXCEPTIONS callers never reach the handler; a second fault while PSR.SFRZ is set becomes ERROR.
* `fatal()` prints and RETURNS; `debug()` is silent while free-running at verbosity 0.  A free-running population-1 fault
  prints NO host line at all -- MEASURED (8 faults, 0 `[ vme:`, 0 DATA_ACCESS lines; the stepped run prints 8).
* M_IDATA measured 34/34 on frozen rev 2 (PRETABLE_IDATA.txt written before the build); 37/38 on rev 3 (section 4).

## 2b. The rules this pass applies (verbatim excerpts, so a seat that cannot read the rule file has them)

* **DEPENDS ON (clause d)** enumerates exactly two things: "(1) the predicates DOMINATING the diff's edited lines,
  walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees or callers; and (2) for operand-swap forms,
  swaps drawn ONLY from fields the guarded BODY reads."  A (d) mutant keeps the guard and nulls its repair -- a
  predicate weakened to "the least-restrictive form that still reads like the same check", or an existing guard's
  operand swapped for a field the guarded body reads.  Not deletion.
* **Joint cells (2026-09-04):** "DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues
  EXACTLY WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM ... A value or combination the body never tests as a case
  (`idata == k`; a byte no conditional distinguishes ...) is DISCLOSED under clause (e)."  And: "At each floor cell,
  every idata bit the guarded body TESTS is written both clear and set."  **"TESTS" means MASKS OR COMPARES AS A CASE**,
  not "depends on" (2026-09-25).
* **Clause (e), the contract:** the probe header names which edits it is designed to catch; an escape outside it is
  "outside the contract", inside it "a breach".  **EXHAUSTED / SAMPLED** (2026-10-09): "SAMPLED = driven at two or more
  values, with the untested slices and their derived or measured sweeps named.  A disclosure vocabulary can never
  demand a row."
* **A filter can reject or repair a row; it can never demand a new one.**  Rows are owed per enumerated mutant, never
  per refusing state.

## 3. The repair, verbatim

### 3a. The fix: fix568 -> fix568b (`src/devices/dev_vme.c`, 4 hunks)

```diff
--- fix568/src/devices/dev_vme.c
+++ fix568b/src/devices/dev_vme.c
@@ -59,12 +59,12 @@
 	uint64_t	warned_unimpl;
 };
 
-/*  #568: narrowing warned_unimpl, or the 1ULL below, would shift past bit
-    VME2_MISC >> 2; make that a compile error (dev_pcc2.c's
-    pcc2_w_fits_in_warned shape).  */
-typedef char vme_warned_fits[((VME2_MISC >> 2) <
-    8 * sizeof(((struct vme_data *)0)->warned_unimpl)
-    && (VME2_MISC >> 2) < 8 * sizeof(1ULL)) ? 1 : -1];
+/*  #568: a warned_unimpl narrower than VME2_MISC >> 2 + 1 bits would
+    leave MISC's announce bit outside the field; make that a compile error
+    (dev_pcc2.c's pcc2_w_fits_in_warned shape).  The 1ULL in the shifts
+    below is not checked here.  */
+typedef char vme_warned_fits[(VME2_MISC >> 2) <
+    8 * sizeof(((struct vme_data *)0)->warned_unimpl) ? 1 : -1];
 
 
 DEVICE_ACCESS(vme)
@@ -149,10 +149,12 @@
 
 	/*  #568 (vmedefaultkill): registers the header names but this model
 	    does not implement.  Each ended the emulator in default: below.
-	    The in-tree OpenBSD 2.2 guest reaches six of them: vme2chip_init()
-	    reads MASTERCTL and writes it back and writes MASTER3, MASTER4 and
-	    MASTER4MOD; vme2abort() reads IRQSTAT (served 0, it reports "irq
-	    not set" and returns before writing IRQCLR).  A bus error here
+	    OpenBSD 2.2's mvme88k driver (sys/arch/mvme88k/dev/vme.c) has
+	    access sites at six of them.  Its attach reaches four:
+	    vme2chip_init() reads MASTERCTL and writes it back and writes
+	    MASTER3, MASTER4 and MASTER4MOD.  The other two, IRQSTAT and
+	    IRQCLR, are in vme2abort(), the ABORT-switch interrupt handler,
+	    and this model raises no VME2 interrupt.  A bus error here
 	    would panic that guest's attach, so these DECLINE: a read is served
 	    the word preloaded above, which is 0 because nothing writes these
 	    words of d->reg[] (odata is deliberately not forced to 0, so a store
@@ -196,9 +198,9 @@
 				    (unsigned long long) idata);
 			else
 				fatal("[ vme: unimplemented read from register "
-				    "0x%x (len %d) -- served 0x%x.  (once) ]\n",
+				    "0x%x (len %d) -- served 0x%llx.  (once) ]\n",
 				    (unsigned) relative_addr, (int) len,
-				    (unsigned) odata);
+				    (unsigned long long) odata);
 		}
 		break;
 
@@ -210,10 +212,11 @@
 			    "0x%x ]\n", (int)relative_addr, (int)idata);
 		/*  #568 (vmedefaultkill): an offset this model does not service:
 		    no header-named register, or the inside of one (a sub-word
-		    start).  Refuse the access -- memory_rw then raises the m88k
-		    data-access exception, the bus error a badaddr() probe
-		    expects -- instead of exit(1), which ended the emulator with
-		    no visible reason (debug() is silent at default verbosity).  */
+		    start).  Refuse the access -- for a guest data load or store,
+		    memory_rw then raises the m88k data-access exception, the bus
+		    error a badaddr() probe expects -- instead of exit(1), which
+		    ended the emulator with no visible reason (debug() is silent
+		    at default verbosity).  */
 		return 0;
 	}
```

**The object comparison** (`killtable2_20261021/OBJDUMP_fix568_vs_fix568b.txt`, GCC 15.2.1 -O3, x86-64): the objects
differ BEYOND the read announce's format string -- the added comment lines move DEVINIT's `__LINE__` (231 -> 234, via
`CHECK_ALLOCATION`'s `FAILURE()`), and the `(unsigned long long)` cast changes `-O3`'s layout of `dev_vme_access`
(registers, padding, two branches, the read-announce call duplicated; `.text` 1890 -> 1970 bytes).  Behaviour is what
table 2 measured.  fix568b is NOT "comment-only".

### 3b. The probe, rev 3 (38 rows): its ROW CONTRACT, verbatim from its header

(The rev2 -> rev3 diff is 13 hunks / 38 KB; the file-reading seats get it whole.  You get the contract every row is
graded against -- each row, the mutant it is designed to catch, and the channel that differs under it.)

```text
ROWS, each with the mutant it is DESIGNED to catch and the channel that differs under it.  The rev-2 descriptions
are DATED PREDICTIONS (2026-10-20); tables 1 and 1b measured them on the 34-row rev 2 and table 2 measures rev 3.
  CONTROL rows -- DEFINITION: a row whose UNIQUE role is an apparatus or medium proof; a row a product edit can red
  is scored, never CONTROL.  CONTROL=FAIL means a PREREQUISITE of the scored rows failed and claims NO cause:
  `vbr reset' and `free neg ctl' also depend on product behaviour, and an edit to DEVINIT's VBR seed reds `vbr reset'.
    neg apparatus  a bogus subtype: the liveness oracle MUST go red (it is failable)
    session / live the control session runs to `quit'; an or-immediate reads back
    vbr reset      DEVICE SIGNATURE: DEVINIT's VBR seed (RAM or a device-less build answers 0)
    free neg ctl   GCSRCTL's debug() line: PRESENT in the stepped cased census, ABSENT in the free run -- the
                   run was free at verbose 0, so the fatal-vs-debug channel of the announce rows can vary
    unasm          every placed word re-read by the disassembler
  cased rows (scored: product edits red them -- M_DROPTCTL, M_DROPIRQEN and M_T1CMPWRDROP in tables 1 and 1b)
    t1cmp rt       cased T1CMP stores and reads back (and is the null medium's second discriminator)
    cased census   one ld at each of the ten cased offsets, ONE session, sentinel-seeded, PC + liveness after:
                   a cased label dropped FAULTs that offset and every later load keeps its sentinel
    free ctl       FREE-RUNNING T1CMP round trip to a breakpoint
    free quiet     ...that run prints NO vme text at all (a cased access never announces)
    tctl rt        TCTL stores a word and reads it back
    vbr rt         VBR stores a word and reads it back, then is restored to the seed and read back again
    t1count inc    T1COUNT stores a word; two reads give it and it + 100 (the read arm's `+= 100')
    cased wr       a word store to each of the six NON-storing cased arms (0x00, GCSRCTL, TCR, IRQEN, IRQL3,
                   IRQL4): no fault, PC + liveness after
    (`tctl rt', `vbr rt' and `t1count inc' share ONE stepped session: a fault at its first store reds all three --
    table 1's M_DROPTCTL -- so two of those reds are DEPENDENT, not own-channel kills.)
  population 2 (decline)
    p2 rd census   26 ld: all 0, no fault, PC + liveness after; a label dropped FAULTs (HEAD: the host dies)
    p2 wr census   26 st of 0xa5a5a5a5, a liveness or (checked: a FAULTING store stops it), then the 26 ld:
                   all 0.  A decline that STORES reads back non-zero -- visible because the fix does NOT force
                   odata = 0; a decline conditioned on direction FAULTs
    p2 ld widths   ld.bu + ld.hu at 0x28, ld.d at 0x08 (BOTH r6 and r7): 0, no fault -- a decline conditioned
                   on len FAULTs one of them
    p2 st widths   st.b + st.h at 0x28, st.d at 0x08, a liveness or, then read 0x28, 0x08, 0x0c back: all 0
  announce (FREE-RUNNING; full tail literals; every offset exactly once)
    p2 ann rd      each of the 26 READ then immediately WRITTEN: exactly 26 read-form lines, 0 write-form
    p2 ann rd 2    the same pairs again in the same session: 0 lines, PC at the breakpoint, liveness proof
    p2 ann wr      each WRITTEN then immediately READ: exactly 26 write-form lines `(len 4): 0xa5a5a5a5'
    p2 ann wr 2    the same pairs again: 0 lines, PC at the breakpoint, liveness proof
                   -- together 26 labels x {read, write} x {latch clear, set}.  Rev 2's dated predictions, and what
                   table 1 MEASURED for each: read- or write-branch fatal -> debug (0 lines: M_RDEBUG, M_WDEBUG), a
                   shared latch (1 line: M_LATCHONE), a never-set latch (52 lines: M_LATCHNOSET), a latch cleared
                   by a write (pass 2 re-announces, 26 lines: M_LATCHCLRW and M_LATCHCLRW_POST), a dropped `(once)'
                   (no exact match: M_NOONCE).  NEVER BUILT: a per-direction latch (52), a latch set at one
                   constant bit (51).
    p2 nw rd       pass 1, FIRST access to three untouched registers by ld.bu / ld.hu / ld.d: `(len 1)',
                   `(len 2)', `(len 8) -- served 0x0.' -- an announce that fires only for 4-byte accesses gives 0
    p2 nw wr       pass 1, FIRST access by st.b / st.h / st.d: `(len 1): 0xd4', `(len 2): 0xc3d4',
                   `(len 8): 0x1122334455667788' -- a 32-bit truncation of the 64-bit value fails the match
    p2 nw rd 2     NEW.  Pass 2 IN THE SAME PROCESS (a new gxemul memsets the latch, so a separate process would be
                   green): the three non-word reads again -> 0 read-form lines.  Kills M_LATCHLEN4 (the latch SET
                   conditioned on len == 4: non-word accesses announce but never latch, so pass 2 re-announces 3).
                   A zero is accepted only from a pass that reached its breakpoint with its liveness proof, and only
                   when pass 1 announced reads at all (`pass 1 silent' otherwise)
    p2 nw wr 2     NEW.  The same for the three non-word stores -> 0 write-form lines (M_LATCHLEN4: 3)
    p2 zero wr     NEW.  Its OWN free-running session (inside the announce pair it would change a 26-count literal):
                   `st r0,r3,0x30' -- a ZERO-valued first store to an untouched register (DMACTL); nothing is
                   seeded into r0 (the m88k core stops the CPU when r0 holds a non-zero value).  Wants the exact
                   WRITE-FORM literal `(len 4): 0x0 -- declined.' and one `[ vme:' line.  Kills M_IDATA (the
                   direction test swapped for `if (idata)': a zero store takes the READ form).  A count of `[ vme:'
                   lines alone would accept the read-form line, so the literal is the oracle.  One width is enough:
                   the swapped test reads idata's zero-ness and the body tests nothing on len
  population 1 (fault)
    p1 fault lo / hi / mid   ld at 0x90 / 0xffc / 0x94: PC 0x18, DMA0, DMT0 (word load into r4), host alive;
                   `return 0' -> `break' serves the read (PC advances); exit(1) reinstated kills the host
    p1 fault wr    st at 0x90: PC 0x18, DMA0, DMT0 (the word-store form)
    p1 p2 edge     ld 0x8c declines (0), then ld 0x90 faults: the label set's last member dropped faults at
                   0x8c instead; a label added AT 0x90 declines it
    p1 census      FREE-RUNNING: all 988 population-1 word starts, faults counted: a label added at ANY of them
                   gives 987; `return 0' -> `break' gives 0
    p1 widths      FREE-RUNNING: ld.bu 0x93, ld.hu 0x96, ld.d 0x98, st.b 0x9d, st.h 0xa2, st.d 0xa8, and NEW the
                   two LANE-0 accesses ld.hu 0xb0 (into r8, sentinel-seeded) and st.b 0xb4 -- eight faults: a FAULT
                   narrowed to word accesses (or to one direction) declines some of them; `if (len == 2 &&
                   (relative_addr & 3) == 0) break;' (M_LANE0H) declines the ld.hu (seven faults, r8 loses its
                   sentinel) and its `len == 1' twin (M_LANE0B) the st.b (seven faults) -- two legs, two accesses
    p1 quiet       NEW.  `[ vme:' lines in the continue text of the free-running p1 census run AND the p1 widths
                   run, each wanting 0: `default:''s debug() is silent free-running and fatal() is not, so a
                   debug -> fatal PROMOTION prints -- read side (M_DFATAL) 988 census lines, write side
                   (M_DFATALW) four widths lines (the census stores nothing).  Free-running at verbose 0 is what
                   lets it vary: in a stepped session it would be red on the fix itself
  interims -- NAMED channels of `vmewidthlanes': that round reds these and re-derives them
    p3 interim     ld.bu 0x51 (inside cased T1CMP): fault, DMA0 0xfff40050 -- also `if (len != 4) break;' in
                   `default:' (Fable) declines it
    p2 int byte    ld.bu 0x29 (inside population-2 MASTERCTL): fault, DMA0 0xfff40028
    p2 int half    ld.hu 0x2a (inside MASTERCTL): fault, DMA0 0xfff40028

CONTRACT (clause e).  DESIGNED to catch: the mutants named above, by the channels named above; tables 1, 1b and 2
measure which.  PREMISE, stated because two designs rest on it: the decline-and-announce arm and `p1 quiet''s
channel need fatal() to PRINT AND RETURN -- it does not exit (src/core/debugmsg.c) -- and the green tables are that
premise's measurement.  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  * populations 3 and 4 and population-2 sub-word starts beyond the three interim pins (one byte at 0x51, one
    byte at 0x29, one halfword at 0x2a);
  * population 4 -- a cased base at len != 4 -- is SERVICED by its cased arm with the `vmewidthlanes' lane defect;
    it does NOT fault;
  * ld.d / st.d at the cased bases 0x00, 0x60 and 0x88, whose second word is a population-2 register (0x04,
    0x64, 0x8c): the device sees ONE access to the cased label;
  * cased-word ld.d / st.d lane placement (population 4: a 32-bit register served into, or stored from, the
    wrong half of an 8-byte access);
  * word-aligned narrow and double accesses at the population-2 registers no non-word row touches;
  * population-2 non-word offsets, cross-width latch reuse and store-data patterns are SAMPLED, not exhausted --
    the zero store is one width (len 4), the non-word rows one register per width;
  * the fault rows pin `return 0', DMA0 and DMT0, NOT the text of `default:''s two debug() lines;
  * DELETION of `default:''s two debug() calls: `p1 quiet' wants 0 lines and a deleted call also prints 0 -- the
    row sees a debug -> fatal promotion, never a deletion;
  * `default:''s write debug prints `(int)idata', a pre-existing truncation in host-debug text;
  * the typedef's compile-time guard: its negative control (the field narrowed) is a failed BUILD, recorded in the
    kill table -- a neutered typedef has no runtime row;
  * an unsampled population-1 interior added as a label (`case 0x91:');
  * NO_EXCEPTIONS callers -- the debugger's put/dump/unassemble never reach the handler (silent zero fill);
  * instruction fetch from the window (a population-1 fetch takes vector 2 and halts; a population-2 fetch
    declines);
  * xmem (declines twice at population 2 -- the store silently; its load faults at population 1);
  * per-instance latch isolation: mvme187 attaches ONE vme device per process;
  * the guest's abort-handler path (IRQSTAT, IRQCLR): vme2abort() is the ABORT-switch interrupt handler and this
    model raises no VME2 interrupt;
  * population-1 accesses other than the 988 word loads, the four stepped faults and the eight width faults;
  * a served value other than 0 in the read announce (no population-2 word is ever non-zero);
  * anything about the real VMEchip2 (its register chapter is not on disk).
DESIGN NOTE: a sub-word start inside a population-2 word maps onto that register's own latch bit (0x29 >> 2 == 10
== MASTERCTL's), so if `vmewidthlanes' later services such starts through the arm, one latch per register still
holds.
ORDER DEPENDENCE: a latch shift that loses its 64-bit literal (`1ULL' -> `1u') is undefined behaviour at MISC's bit
35, so what it does is the compiler's choice.  This paragraph said "on this x86-64 build it lands on bit 3,
SLAVELMOD2's (0x0c) ... so MISC's announce is silenced"; that was PRETABLE2's prediction, and kill table 2 measured
the alternative PRETABLE2 named instead: GCC 15.2.1 -O3 specialised the MISC case and folded the shift to 0, so
MISC never latches -- 27 lines in pass 1 and 2 in pass 2, red `p2 ann rd', `p2 ann wr' and both `2' rows
(killtable2_20261021/obj/M_ONENARROW_codegen.txt).  The masked-count shape (bit 3, MISC silenced behind 0x0c in
POP2 order, so a reorder of POP2 could move the kill) was not built.  No portable claim.
```

### 3c. The gate-14 block, verbatim (`regress/gate_arm.sh`)

```sh
#  ------------------------------------------------------------ vmedefaultkill (#568)
#  dev_vme.c's default: ended the emulator (exit(1), announced only by debug() -- silent while
#  free-running) on any VME2 offset the switch did not name.  Now: the 26 header-named registers
#  the model does not implement DECLINE (reads served the preloaded word, writes dropped, one
#  latched fatal() per register); every other unmatched offset returns 0, and for a guest data load
#  or store memory_rw raises the m88k data-access exception.  The rung-3 witness
#  (regress/artifacts/vmedefaultkill/witness_20261020/, 7 of 7 guest sites rc 1 on 5dbc000e) is NOT
#  run here; this is its detector.  Needs only the binary: the probe constructs mvme88k/mvme187 with
#  -M 64 and a 4-byte dummy image at 0x10000 -- no PROM image.  Kill tables:
#  regress/artifacts/vmedefaultkill/killtable1_20261020/ (rev 2) and killtable2_20261021/ (rev 3).
VMEDLOG=$LOGDIR/vme_default.log
python3 -u vme_default_probe.py "$PMAX" gate > "$VMEDLOG" 2>&1 || true
if ! grep -q "VME_DEFAULT_PROBE_DONE" "$VMEDLOG"; then
    check "vme default probe completed" "no" "yes"
else
    check "vme default probe completed" "yes" "yes"
    vres=$(sed -n 's/^VME_DEFAULT_RESULT=//p' "$VMEDLOG")
    check "vme_default rows run"     "${vres#*/}" 38
    check "vme_default rows correct" "${vres%/*}" "38"
    check "vme default controls" "$(grep -c '^VME_DEFAULT_CONTROL=OK$' "$VMEDLOG")" "1"
    for v in "neg apparatus" "session" "live" "vbr reset" "t1cmp rt" "cased census" "free ctl" "free quiet" "free neg ctl" "tctl rt" "vbr rt" "t1count inc" "cased wr" "p2 rd census" "p2 wr census" "p2 ld widths" "p2 st widths" "p2 ann rd" "p2 ann rd 2" "p2 ann wr" "p2 ann wr 2" "p2 nw rd" "p2 nw wr" "p2 nw rd 2" "p2 nw wr 2" "p2 zero wr" "p1 fault lo" "p1 fault hi" "p1 fault mid" "p1 fault wr" "p1 p2 edge" "p3 interim" "p2 int byte" "p2 int half" "p1 census" "p1 widths" "p1 quiet" "unasm"; do
        check "vme default row: $v" "$(count "$VMEDLOG" "^$v  .*ok$")" "1"
    done
    check "vme default rows emitted" "$(( $(count "$VMEDLOG" " ok$") + $(count "$VMEDLOG" " FAIL$") ))" "38"
    check "vme default rows green"   "$(count "$VMEDLOG" " ok$")"   "38"
    check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"
fi
```

### 3d. Applied AFTER table 2, comment-only: the first seat's one L4 correction (CHECK IT -- a correction is not safer than what it corrects)

The shipped probe's ORDER DEPENDENCE paragraph stated PRETABLE2's prediction (a bit-3 collision) as this build's
behaviour, while table 2 measured the other shape (section 4's MISS note).  No code line changed; the frozen copy table 2
ran keeps the old text because it is the text that ran.

```diff
--- rev3 as table 2 ran it (md5 ddcebfe3)
+++ rev3 as shipped now (md5 346c7813)
@@ -195,5 +195,8 @@
 ORDER DEPENDENCE: a latch shift that loses its 64-bit literal (`1ULL' -> `1u') is undefined behaviour at MISC's bit
-35; on this x86-64 build it lands on bit 3, SLAVELMOD2's (0x0c), and `p2 ann rd' / `p2 ann wr' reach 0x0c before
-0x8c in POP2 order, so MISC's announce is silenced -- a reorder of POP2 can move that kill (table 2 records the
-host and the row).
+35, so what it does is the compiler's choice.  This paragraph said "on this x86-64 build it lands on bit 3,
+SLAVELMOD2's (0x0c) ... so MISC's announce is silenced"; that was PRETABLE2's prediction, and kill table 2 measured
+the alternative PRETABLE2 named instead: GCC 15.2.1 -O3 specialised the MISC case and folded the shift to 0, so
+MISC never latches -- 27 lines in pass 1 and 2 in pass 2, red `p2 ann rd', `p2 ann wr' and both `2' rows
+(killtable2_20261021/obj/M_ONENARROW_codegen.txt).  The masked-count shape (bit 3, MISC silenced behind 0x0c in
+POP2 order, so a reorder of POP2 could move the kill) was not built.  No portable claim.
 
@@ -247,3 +250,4 @@
 ZERO_OFF = 0x30             # `p2 zero wr': DMACTL -- its own session; not MISC (0x8c) and not SLAVELMOD2 (0x0c),
-                            # the pair a 32-bit latch shift collides on x86-64, and no non-census session touches it
+                            # the pair a 32-bit latch shift could collide (undefined; see ORDER DEPENDENCE), and no
+                            # non-census session touches it
 LANE0_HU = 0xb0             # `p1 widths': a word-aligned (lane-0) halfword start no other access there uses
```

## 4. Kill table 2, measured (frozen rev 3, fix568b, a fresh clone of `git archive 1a59a47e` -- the same src tree as HEAD 86114a90)

```text
KILLTABLE2_VS_PRETABLE2 -- #568 (vmedefaultkill) REPAIR 1, kill table 2, measured 2026-10-21 by the measuring seat
(Opus 5.5).  Fix: rev3/dev_vme.fix568b.c (md5 beb120eae1be112b682bd528f103191c).  Detector: probe REVISION 3, frozen as
rev3/vme_default_probe.rev3.frozen.py (md5 ddcebfe3257d3370f3c16b0bee79a4be, 38 rows) -- that copy alone ran every leg
(the PROBE_MD5 in every raw's first line: 37 of 37).
Clone: WSL /tmp/gxkt568t2 from `git archive 1a59a47e', configure + make -j4; each leg = ONE exact find/replace on fix568b
(mk_legs568t2.py; legs/<LEG>.diff; the table-1/1b legs regenerated with their intent unchanged -- only M_NOONCE's and
M_SERVED0's find-strings moved, onto fix568b's D1 lines).  dev_vme.o + machine_mvme88k.o + gxemul removed before every
build, `[ gxemul -nt <source> ]' after it (RUNLOG.txt, build/*.build.log); legs run ONE AT A TIME.
ORDER: PRETABLE2.out written 01:15:27; the table's first build log 01:16:55 -- PRETABLE2 FIRST.
MATCH = the measured red set equals PRETABLE2's predicted set and CONTROL is as predicted; MISS otherwise.

== REFERENCE RUNS ==
BASE        | 38/38 | CONTROL=OK | red(0): - | predicted 0 red, CONTROL=OK | MATCH
HEAD        | 14/38 | CONTROL=OK | red(24): p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr, p2 nw rd 2, p2 nw wr 2, p2 zero wr, p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths, p1 quiet | predicted 24 red, CONTROL=OK | MATCH
NULL        | 5/38 | CONTROL=FAIL | red(33): vbr reset, t1cmp rt, cased census, free ctl, free neg ctl, tctl rt, vbr rt, t1count inc, cased wr, p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr, p2 nw rd 2, p2 nw wr 2, p2 zero wr, p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths, p1 quiet | predicted 33 red, CONTROL=FAIL | MATCH
BASE_FINAL  | 38/38 | CONTROL=OK | red(0): - | predicted 0 red, CONTROL=OK | MATCH
NULL per class (PRETABLE2 section 6): CONTROL red vbr reset, free neg ctl; CONTROL green neg apparatus, session, live, unasm; scored red 31; scored green free quiet.
BASE binary c19d673fc82f821409eb5a17286b21ce, BASE_FINAL binary c19d673fc82f821409eb5a17286b21ce: byte-identical.

== THE TABLE (one line per leg: LEG | score | CONTROL | measured red rows | PRETABLE2 predicted | MATCH/MISS) ==
M_EXIT            | 27/38 | CONTROL=OK | red(11): p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths, p1 quiet | predicted red(11) | MATCH
M_DROPMCTL        | 30/38 | CONTROL=OK | red(8): p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2 | predicted red(8) | MATCH
M_DROPMISC        | 31/38 | CONTROL=OK | red(7): p2 rd census, p2 wr census, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p1 p2 edge | predicted red(7) | MATCH
M_ADD94           | 35/38 | CONTROL=OK | red(3): p1 fault mid, p1 census, p1 quiet | predicted red(3) | MATCH
M_LATCHONE        | 33/38 | CONTROL=OK | red(5): p2 ann rd, p2 ann wr, p2 nw rd, p2 nw wr, p2 nw wr 2 | predicted red(5) | MATCH
M_LATCHNOSET      | 32/38 | CONTROL=OK | red(6): p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd 2, p2 nw wr 2 | predicted red(6) | MATCH
M_LATCHRDSET      | 36/38 | CONTROL=OK | red(2): p2 ann wr, p2 nw wr 2 | predicted red(2) | MATCH
M_LATCHCLRW       | 34/38 | CONTROL=OK | red(4): p2 ann rd, p2 ann rd 2, p2 ann wr 2, p2 nw wr 2 | predicted red(4) | MATCH
M_LATCHCLRW_POST  | 34/38 | CONTROL=OK | red(4): p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw wr 2 | predicted red(4) | MATCH
M_WDEBUG          | 33/38 | CONTROL=OK | red(5): p2 ann wr, p2 ann wr 2, p2 nw wr, p2 nw wr 2, p2 zero wr | predicted red(5) | MATCH
M_RDEBUG          | 34/38 | CONTROL=OK | red(4): p2 ann rd, p2 ann rd 2, p2 nw rd, p2 nw rd 2 | predicted red(4) | MATCH
M_ANNLEN4         | 34/38 | CONTROL=OK | red(4): p2 nw rd, p2 nw wr, p2 nw rd 2, p2 nw wr 2 | predicted red(4) | MATCH
M_TRUNC           | 37/38 | CONTROL=OK | red(1): p2 nw wr | predicted red(1) | MATCH
M_WRFAULT         | 27/38 | CONTROL=OK | red(11): p2 wr census, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr, p2 nw rd 2, p2 nw wr 2, p2 zero wr | predicted red(11) | MATCH
M_LENFAULT        | 32/38 | CONTROL=OK | red(6): p2 ld widths, p2 st widths, p2 nw rd, p2 nw wr, p2 nw rd 2, p2 nw wr 2 | predicted red(6) | MATCH
M_STORE           | 36/38 | CONTROL=OK | red(2): p2 wr census, p2 st widths | predicted red(2) | MATCH
M_ODATA0          | 38/38 | CONTROL=OK | red(0): - | predicted red(0) | MATCH
M_SERVED0         | 38/38 | CONTROL=OK | red(0): - | predicted red(0) | MATCH
M_FLTBREAK        | 28/38 | CONTROL=OK | red(10): p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths | predicted red(10) | MATCH
M_FLTLEN          | 34/38 | CONTROL=OK | red(4): p3 interim, p2 int byte, p2 int half, p1 widths | predicted red(4) | MATCH
M_FLTWR           | 36/38 | CONTROL=OK | red(2): p1 fault wr, p1 widths | predicted red(2) | MATCH
M_NOONCE          | 36/38 | CONTROL=OK | red(2): p2 ann rd, p2 nw rd | predicted red(2) | MATCH
M_DROPTCTL        | 34/38 | CONTROL=OK | red(4): cased census, tctl rt, vbr rt, t1count inc | predicted red(4) | MATCH
M_CAPNARROW       | BUILD FAILED | - | 68:dev_vme.c:66:14: error: size of array 'vme_warned_fits' is negative | predicted: BUILD FAILS | MATCH
M_DROPIRQEN       | 36/38 | CONTROL=OK | red(2): cased census, cased wr | predicted red(2) | MATCH
M_T1CMPWRDROP     | 36/38 | CONTROL=OK | red(2): t1cmp rt, free ctl | predicted red(2) | MATCH
M_ADD90           | 33/38 | CONTROL=OK | red(5): p1 fault lo, p1 fault wr, p1 p2 edge, p1 census, p1 quiet | predicted red(5) | MATCH
M_IDATA           | 37/38 | CONTROL=OK | red(1): p2 zero wr | predicted red(1) | MATCH
M_LATCHLEN4       | 36/38 | CONTROL=OK | red(2): p2 nw rd 2, p2 nw wr 2 | predicted red(2) | MATCH
M_DFATAL          | 37/38 | CONTROL=OK | red(1): p1 quiet | predicted red(1) | MATCH
M_DFATALW         | 37/38 | CONTROL=OK | red(1): p1 quiet | predicted red(1) | MATCH
M_LANE0H          | 37/38 | CONTROL=OK | red(1): p1 widths | predicted red(1) | MATCH
M_LANE0B          | 37/38 | CONTROL=OK | red(1): p1 widths | predicted red(1) | MATCH
M_ONENARROW       | 34/38 | CONTROL=OK | red(4): p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2 | predicted red(2) | MISS (unpredicted red: p2 ann rd 2, p2 ann wr 2)

== SURVIVORS (legs scoring 38 of 38) ==
M_ODATA0          38/38 CONTROL=OK -- predicted SURVIVOR (equivalent today: no population-2 word is ever non-zero).  Diagnosis: the TARGET is equivalent today (no population-2 word is ever non-zero, so
                  a read serves 0 and its announce prints 0x0 with or without the edit) -- not a mis-built leg (legs/M_ODATA0.diff is
                  the one edit) and not a mis-cut row; the contract discloses it.
M_SERVED0         38/38 CONTROL=OK -- predicted SURVIVOR (equivalent today).  Diagnosis: the TARGET is equivalent today (no population-2 word is ever non-zero, so
                  a read serves 0 and its announce prints 0x0 with or without the edit) -- not a mis-built leg (legs/M_SERVED0.diff is
                  the one edit) and not a mis-cut row; the contract discloses it.

== MISS NOTES ==
M_ONENARROW  measured red: p2 ann rd (27/26/26), p2 ann rd 2 (2), p2 ann wr (27/26/26), p2 ann wr 2 (2).
  PRETABLE2's PRIMARY prediction (p2 ann rd + p2 ann wr, 25 lines each: a runtime-masked 32-bit shift landing on
  SLAVELMOD2's bit 3) MISSED; the shape measured is the ALTERNATIVE PRETABLE2 section 7 named in the same paragraph
  -- `a build whose shift yields 0 would red all four ann rows (MISC never latches: 27 lines in pass 1, 2 in
  pass 2)' -- exactly.  Cause: neither the leg (one edit, legs/M_ONENARROW.diff) nor the rows -- the COMPILER.
  The leg's object (obj/M_ONENARROW.dev_vme.o, disassembled after the run: obj/M_ONENARROW_codegen.txt) shows
  GCC specialising the MISC case and constant-folding the undefined `1u << 35' to 0 there (no latch test, no
  set), while every other register uses a runtime `shl %cl,%edx'.  KILLED either way, by different rows; no
  portable claim (D5).

== PER-ROW KILL CENSUS (legs of table 2 that red each row) ==
neg apparatus  CONTROL   0  -- no leg reds it
session        CONTROL   0  -- no leg reds it
live           CONTROL   0  -- no leg reds it
vbr reset      CONTROL   0  -- no leg reds it
t1cmp rt                 1  M_T1CMPWRDROP
cased census             2  M_DROPTCTL, M_DROPIRQEN
free ctl                 1  M_T1CMPWRDROP
free quiet               0  -- no leg reds it
free neg ctl   CONTROL   0  -- no leg reds it
tctl rt                  1  M_DROPTCTL
vbr rt                   1  M_DROPTCTL
t1count inc              1  M_DROPTCTL
cased wr                 1  M_DROPIRQEN
p2 rd census             2  M_DROPMCTL, M_DROPMISC
p2 wr census             4  M_DROPMCTL, M_DROPMISC, M_WRFAULT, M_STORE
p2 ld widths             2  M_DROPMCTL, M_LENFAULT
p2 st widths             4  M_DROPMCTL, M_WRFAULT, M_LENFAULT, M_STORE
p2 ann rd                9  M_DROPMCTL, M_DROPMISC, M_LATCHONE, M_LATCHNOSET, M_LATCHCLRW, M_RDEBUG, M_WRFAULT, M_NOONCE, M_ONENARROW
p2 ann rd 2              8  M_DROPMCTL, M_DROPMISC, M_LATCHNOSET, M_LATCHCLRW, M_LATCHCLRW_POST, M_RDEBUG, M_WRFAULT, M_ONENARROW
p2 ann wr                9  M_DROPMCTL, M_DROPMISC, M_LATCHONE, M_LATCHNOSET, M_LATCHRDSET, M_LATCHCLRW_POST, M_WDEBUG, M_WRFAULT, M_ONENARROW
p2 ann wr 2              8  M_DROPMCTL, M_DROPMISC, M_LATCHNOSET, M_LATCHCLRW, M_LATCHCLRW_POST, M_WDEBUG, M_WRFAULT, M_ONENARROW
p2 nw rd                 6  M_LATCHONE, M_RDEBUG, M_ANNLEN4, M_WRFAULT, M_LENFAULT, M_NOONCE
p2 nw wr                 6  M_LATCHONE, M_WDEBUG, M_ANNLEN4, M_TRUNC, M_WRFAULT, M_LENFAULT
p2 nw rd 2               6  M_LATCHNOSET, M_RDEBUG, M_ANNLEN4, M_WRFAULT, M_LENFAULT, M_LATCHLEN4
p2 nw wr 2              10  M_LATCHONE, M_LATCHNOSET, M_LATCHRDSET, M_LATCHCLRW, M_LATCHCLRW_POST, M_WDEBUG, M_ANNLEN4, M_WRFAULT, M_LENFAULT, M_LATCHLEN4
p2 zero wr               3  M_WDEBUG, M_WRFAULT, M_IDATA
p1 fault lo              3  M_EXIT, M_FLTBREAK, M_ADD90
p1 fault hi              2  M_EXIT, M_FLTBREAK
p1 fault mid             3  M_EXIT, M_ADD94, M_FLTBREAK
p1 fault wr              4  M_EXIT, M_FLTBREAK, M_FLTWR, M_ADD90
p1 p2 edge               4  M_EXIT, M_DROPMISC, M_FLTBREAK, M_ADD90
p3 interim               3  M_EXIT, M_FLTBREAK, M_FLTLEN
p2 int byte              3  M_EXIT, M_FLTBREAK, M_FLTLEN
p2 int half              3  M_EXIT, M_FLTBREAK, M_FLTLEN
p1 census                4  M_EXIT, M_ADD94, M_FLTBREAK, M_ADD90
p1 widths                6  M_EXIT, M_FLTBREAK, M_FLTLEN, M_FLTWR, M_LANE0H, M_LANE0B
p1 quiet                 5  M_EXIT, M_ADD94, M_ADD90, M_DFATAL, M_DFATALW
unasm          CONTROL   0  -- no leg reds it

== COUNTS ==
legs: 34 (27 regenerated from tables 1 and 1b, 7 new); MATCH 33 (31 killed as predicted, incl. M_CAPNARROW's build failure; 2 predicted survivors); MISS 1; survivors 2.
VERDICT: TABLE 2 DONE -- 34 legs, 31 red as predicted, 1 misses, 2 survivors
```

## 4b. Measured since table 2

* **Table 2b, ONE clause-(e) leg** (`killtable2_20261021/table2b/`; the prediction `PRETABLE2B.txt` written 02:12:02,
  the build 02:12:53): M_IDATABIT1 -- in the population-2 arm, `if (writeflag == MEM_WRITE)` ->
  `if (writeflag == MEM_WRITE && !(idata & 2))` -- scored **38/38, CONTROL=OK, as predicted**: every population-2 store
  the probe makes carries bit 1 clear (0x0, 0xa5a5a5a5, 0xd4, 0xc3d4, 0x1122334455667788).  The first seat named this
  leg OWED-OPTIONAL and graded it clause (e); the grading is question 4.  Restore verified: source `cmp`-clean against
  the working tree, rebuilt binary byte-identical to the fix build.
* **Gate 14's #568 block alone, both ways, on a CLEAN clone** (`git archive HEAD 86114a90`, built twice in WSL
  `/tmp/gx568g3`, no other session's uncommitted edits): HEAD's binary **FAIL, 27 of 45 checks** (14/38 rows; the 24 red
  rows are exactly table 2's HEAD set; CONTROL OK); HEAD + fix568b **PASS, 45 checks** (38/38).  Probe md5 346c7813 (the
  section-3d text).
* **A records defect found on the way, and disclosed here rather than buried:** the rev-2 FULL gate-14 run (PASS, 1264
  checks) used `build/gxemul`, which carries the other session's uncommitted `dev_pcc2.c` and `mvme_pcctworeg.h` -- the
  PCCchip2 on the same `mvme187` machine, and gate 14 has pcc2 blocks.  The rev-3 full gate will run on the clean
  clone's binary instead (PMAX override), and the record will say which binary each run used.

## 5. Questions (two records questions are put only to the seats that can open the files; you get these three)

2. **THE FLOOR QUESTION, on the composite -- attack the first seat's zero.**  Its enumeration (104 label x direction x
   latch cells; operand swaps of the direction and latch tests; `default:`'s {read, write}) and sweep table are in
   section 7.  Using the fix diff (3a), the arm as the diff shows it, and the row contract (3b), name **a one-edit mutant
   inside the DEPENDS-ON enumeration (section 2b) that its table misses and that would pass all 38 rows**, or **a row it
   credits with a kill that would NOT red under the named edit**.  Give your own denominator.  In particular: is the
   zero-store row enough for the `if (idata)` CLASS, or does another data-dependent swap of the direction test, the latch
   test or the label dispatch pass 38/38?
4. **A grading question, settled by the rules in section 2b.**  M_IDATABIT1 (section 4b) qualifies the direction test by
   a store-data bit and measured 38/38.  The first seat graded it clause (e): the arm's body tests no bit and no value of
   idata, so under the joint-cell rule and the "tests means masks or compares as a case" pin it is outside the floor, and
   the probe already discloses store-data patterns as SAMPLED.  **Is that grading right, or is this a floor breach?**  If
   (e): must the SAMPLED disclosure name the five sampled values and the low-word bits clear in all of them (the first
   seat lists 1, 11, 19, 20, 25, 27 -- check that list against the five values)?
5. Anything else you found.

## 6. Answer format

Your token first (`ARGON_VME_R1_20261021`), then ONE line `VERDICT: CLOSE | REPAIR AGAIN | CANNOT SETTLE -- <one line>`, then your answers by
number.  Every proposed escaping mutant as a ONE-LINE diff of `dev_vme.c`, marked OWED (it will be built and measured
before anything is decided).  Facts and flags only.

## 7. The first seat's answer (Fable 5.1, file-reading) -- ATTACK IT

Its verdict line, verbatim:

> VERDICT: CLOSE -- zero floor breaches in the DEPENDS-ON enumeration of fix568b + rev 3 (104 label x direction x latch cells, the operand-swap closure of the direction test and the latch test, default:'s {read, write}; 34 legs measured, the remainder by reading, denominator in Q2); the repair implements every adjudicated item except D5's "do not assert the UB outcome" in the SHIPPED probe's docstring, whose ORDER DEPENDENCE paragraph states the bit-3 collision as this build's behaviour while table 2 measured constant-folding to zero at MISC (L4, comment-only, correct in place); SCORE_CLAIMS_MANIFEST 36 -> 37, the check_probe_wiring entries and gate 14's rev-3 runs are still owed by the coordinator before the commit.

Its Q2, verbatim -- the part to break:

## Q2 -- the floor question, on the composite fix568b + rev 3

**Enumeration (DEPENDS-ON, walked to the function boundary).**  The fix's edited lines are the population-2 arm (dev_vme.c :166-205), `default:`'s `return 0` (:220), the typedef and the struct field.
* Dominating predicates of the arm: P1 the switch label (26 members; the selector flows into the latch index, so a FLOOR axis); P2 the latch test `!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))`; P3 the direction test `writeflag == MEM_WRITE`.
* Body-read lvalues and the partition the BODY induces on each: `writeflag` {READ, WRITE} (tested); the latch bit {clear, set} (tested); `relative_addr` (dispatched and indexed: the 26 labels); `len` -- printed only, NO partition; `idata` -- printed in the write form only, NO partition; `odata` -- printed in the read form only, NO partition; `d->warned_unimpl` -- tested and set, writers: the arm's `|=` and DEVINIT's memset only (PRETABLE2 section 3 greps).
* `default:`: no predicate of its own; its body tests `writeflag` {READ, WRITE} for the `debug()` choice and nothing else.

**The floor** is therefore label(26) x direction(2) x latch(2) = **104 cells**, all rowed by the announce pair (each label read-then-written and written-then-read, pass 1 clear and pass 2 set, every pass-1 line pinned by its full literal and every offset "exactly once"), plus the clause-(2) operand swaps of P3 and P2 drawn from the body-read set, plus `default:`'s {READ, WRITE} x {refuse}.

**Sweep, with the row that reds each shape** (M = measured in table 2; R = my reading of the probe):

| predicate | edit shape (one edit) | row that reds it | how |
|---|---|---|---|
| P1 | any one label dropped | `p2 rd census` (the stepped session faults at that label: pc=0x18, sentinels), plus the ann pair | M for MASTERCTL and MISC; R for the other 24 -- every label is loaded in that session, same code path |
| P1 | a label added at a population-1 word start | `p1 census` (987/988) + the fault row at that offset, + `p1 quiet` 1/0 (second channel) | M (ADD90, ADD94) |
| P3 | operand swapped for idata's zero-ness | `p2 zero wr` 0/1 | M (M_IDATA) |
| P3 | operand swapped for idata's NON-zero-ness (the negation) | `p2 ann rd` (every read prints the write form: 26/0/0) | R |
| P3 | operand swapped for odata, either polarity | odata is 0 at every population-2 access, so one polarity prints the write form everywhere (`p2 ann rd` 0 exact) and the other the read form everywhere (`p2 ann wr` 0 exact) | R |
| P3 | operand swapped for len (== 4 or != 4) | word accesses all take one form: `p2 ann rd` or `p2 ann wr`; non-word: `p2 nw rd` / `p2 nw wr` | R |
| P3 | operand swapped for any relative_addr-derived test | splits the 26 labels into two wording classes; the ann pair pins all 26 in both directions by literal | R |
| P3 | operand swapped for the latch state | always true after the set: every announce is write-form, `p2 ann rd` | R |
| P3 | qualified `&& len == 4` | `p2 nw wr` (non-word stores print the read form: 0/0) | R; its latch twin M_ANNLEN4 is M |
| P3 | qualified `&& (idata & M)` for ANY non-zero M | `p2 zero wr` (0 & M = 0: the zero store prints the read form) | R -- this is the half of the zero row's value that goes beyond M_IDATA itself |
| P2 / the set | index derivation changed (shift count, mask, the literal's width) | collisions or orphaned bits: `p2 ann rd` / `p2 ann wr` counts, or pass-2 re-announces | M for the constant index (LATCHONE) and the 32-bit literal (ONENARROW: four rows); R for `>> 3`, `>> 1`, `& 31` |
| P2 / the set | the set conditioned on writeflag / len / idata / odata / one label | reads never latch -> `p2 ann rd 2` 26; non-zero writes never latch -> `p2 ann wr 2`; non-word never latch -> `p2 nw rd 2` / `wr 2`; one label never latches -> `p2 ann rd 2` >= 1 | M for RDSET, LATCHLEN4, NOSET, CLRW, CLRW_POST; R for idata/odata/label |
| P2 | the test's polarity dropped | `p2 ann rd` 0 lines on a first access | R |
| P2 / the set | the latch field swapped for `d->reg[]`, odata or idata | never latches (always-announce) -> `p2 ann rd 2`; a `d->reg[] |=` additionally shows in `p2 rd census` read-backs | R |
| preamble | `idata = memory_readmax64(...)` conditioned on len | `p2 nw wr` literal (`0x0` where `0xd4` is wanted) | R |
| preamble | `odata = d->reg[...]` dropped | `t1cmp rt`, `vbr reset` (cased reads return 0) | R |
| tail | `return 1` -> `return 0` | everything faults: `p2 rd census`, `t1cmp rt`, ... | R |
| default: | `return 0` -> `break` / `exit(1)` | the ten fault rows | M (FLTBREAK, EXIT) |
| default: | refusal conditioned on writeflag | `p1 fault wr`, `p1 widths` 4/8 | M (FLTWR) |
| default: | refusal conditioned on len / lane / an address range | `p1 widths`, the interims, `p1 census` (any range narrowing drops the 988 pin or `p1 fault hi`/`lo`) | M for FLTLEN, LANE0H, LANE0B; R for ranges |
| default: | refusal conditioned on idata (serve zero stores and all reads, or serve non-zero stores) | `p1 fault lo` (idata is 0 on reads) or `p1 fault wr` + `p1 widths` (0xa5a5a5a5 and the NARROW stores are non-zero) | R |

**Equivalents, not breaches:** `odata = 0` in the arm and a literal 0 in the read announce (M: 38/38 both, predicted, disclosed); the tail's `memory_writemax64` conditioned on len or on the window (the device read buffer is pre-zeroed by memory_rw's `#95` memset, so a skipped write-back serves the same 0) -- equivalent today for every row and NOT CLAIMED by the contract's "a served value other than 0" line.

**Floor breaches found: ZERO.**  Denominator: the 104 cells; 8 operand-swap shapes of P3; 5 index derivations, 5 conditioning operands, 1 polarity and 3 field swaps at P2; 4 preamble/tail edits; `default:`'s {READ, WRITE} and 4 narrowing families -- 34 of these measured by table 2 (31 red as predicted, M_CAPNARROW's build failure, 2 predicted equivalents; the ONENARROW miss is a different-row kill, not a survival), the rest by reading the probe's rows against the handler.

**The `if (idata)` class, answered directly.**  The zero-store row is enough for the OPERAND-SWAP cell -- the thing the floor's clause (2) names -- and it also kills every `&& (idata & M)` qualification.  What it cannot see, and what no row sees, is a qualification of the direction test (or of the latch test) that EXEMPTS a store value or bit the rows never drive.  By reading, the five sampled store values are 0, 0xa5a5a5a5, 0xd4, 0xc3d4 and 0x1122334455667788; the low-word bits every one of them leaves CLEAR are 1, 11, 19, 20, 25 and 27 (and most bits above 31 outside the st.d's pattern).  So `if (writeflag == MEM_WRITE && !(idata & 2))` -- or `&& idata != <any unsampled value>` -- is predicted to pass 38/38.  This is NOT a floor cell: the shipped body tests no bit and no value of idata, so under the 09-04 body-tested-partition rule and the 09-25 "tests means masks or compares as a case" pin it is clause (e), and the contract already discloses "store-data patterns are SAMPLED".  Two consequences: (i) the SAMPLED vocabulary (7n-5) requires naming the untested slice and its derived sweep, and the rev-3 contract names neither -- the contract should list the five sampled values and the bit set above; (ii) **OWED-OPTIONAL, clause (e):** one leg, the direction test qualified by `&& !(idata & 2)` -- predicted 38/38 -- to make that disclosure a measured sweep rather than a derived one.  If it reds, the contract sentence is wrong and that is worth knowing; if it survives, it is filed as coverage debt beside the other clause-(e) items, never repaired in-round.  The label dispatch has no one-edit data-dependent form (a `case` label is a constant); the data-dependent latch forms are either killed by the ann pair (idata is 0 on every read, non-zero on every ann-wr store) or fall into the same value/bit-exemption class.

Two further clause-(e) cells I name because the rows were built for the axis in question: `default:` serving (len 1, lane 0, READ) or (len 2, lane 0, WRITE) -- the width row drives only `ld.hu` at lane 0 and `st.b` at lane 0, so the other two direction x width cells at lane 0 are unrowed; covered by the contract's "population-1 accesses other than ... the eight width faults" line, but worth naming since F10(c) was about lane 0 specifically.  And the zero store at the three non-word widths (one width sampled), which the contract already discloses.
