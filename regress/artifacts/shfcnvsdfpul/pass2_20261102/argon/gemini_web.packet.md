# Reading task: pass 2: shfcnvsdfpul (Argon) (Gemini web; 2026-11-02)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBP2SHFCNVSD-0acb` on a line of its own.

# PANEL PASS 2 -- `shfcnvsdfpul` (#576): the real diff, the detector, the pre-table check and the measured kill table

Fired 2026-11-02 17:3x.  HEAD `987cb596` (unchanged since pass 1).  Roster (owner 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3,
Argon (Gemini web), Grok 4.7.  Astra's PASS 1 was walled until 17:27 and re-fired at 17:28; its pass-2 answer will follow in its next
window and the round HOLDS its commit for it (an adjudication short of the roster is provisional on its face).

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `987cb596`.**  The diff below has NOT been applied to any project tree; it lives
in a scratch clone (`/tmp/gxfix576`, WSL) where it was built and measured.  File-reading seats: compare against `git show HEAD:<path>`,
never the working tree (it carries other sessions' uncommitted edits) and never `./src/` (a pristine 2021 upstream copy).
**Packet-fed seats: everything you need is inlined below.**  Check the premises, not just the derivations; where a number is stated,
it names the artifact that produced it.  **VERDICT LINE FIRST**: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP`, repeated as
your last line.

## 0. What pass 1 said and what changed (F1..F9, with dispositions)

Four of five seats answered pass 1 (`w576/pass1_20261102/`): Argon PROCEED (14/14 HOLDS); glm-5.3 PROCEED WITH CHANGES (4); Grok 4.7
PROCEED WITH CHANGES (4); Fable 5.1 PROCEED WITH CHANGES (4).  Findings and dispositions:

| # | finding | raised by | disposition |
|---|---|---|---|
| F1 | `#297` GUARDED the FTRC casts (still at :3016/:3038 behind a range ladder); it did not remove them; the bug file at `OUTSTANDING_BUGS.md:8240` says "removed" | glm, Grok, Fable, Argon | ACCEPTED: L4 correction in place, quoting the old wording (section 6) |
| F2 | every detector row must run under PR (the manual's defined arm); the inherited FPUL readback shape had extra bits 0 | Grok | ACCEPTED: all eight rows carry PR |
| F3 | encode DR2 and seed BOTH halves of the destination with the sentinel; DR0 alone would make weakening (g) green | Grok | ACCEPTED (fr2/fr3 = 0xdeadbeef on every DR2 row) |
| F4 | spread the FPUL rows over two destinations, one DR0, so the destination-keyed form is seen from both sides | Fable | ACCEPTED: `fcnvsd fpul 0.1` targets DR0 (0xf0ad); measured M_g 42/52 and its mirror M_gm 50/52 |
| F5 | one FPUL row must run with DN clear or the DN-keyed form (f) escapes | glm (a row is owed), Fable (NODN marker at zero cost), Grok (disclose, do not add rows) | ACCEPTED in Fable's form: `fcnvsd fpul -0` carries NODN, zero added sessions; measured M_f 50/52, caught by that row alone |
| F6 | 0x7fc00000 is a SIGNALING NaN under the SH-4 convention (fraction MSB = 1, manual :4980-4989); label it `snan` and write NaN classing into the contract | Fable | ACCEPTED: row renamed `fcnvsd fpul snan`; contract text in the probe comment |
| F7 | disclose in the contract the classes with no row: finite abs(v) >= 2^31 other than -2^31, -Inf, a quiet NaN, a subnormal input, +0 (the fixed point) | Fable, Grok | ACCEPTED: written into the probe's #576 comment |
| F8 | drop `fcnvsd fpul inf` (sole carrier of nothing) to 14 sessions | Fable | REJECTED for now: Grok measured 16 sessions proportionate against a 36-session section; `inf` is the only row in the +Inf class and stands for it in the contract.  Seats: say which you prefer |
| F9 | SH NaN RESULTS use the shared encoder's all-ones pattern, which SH-4 classes as signaling where hardware emits quiet (`0x7fbfffff` / `0x7ff7ffff...`); the MIPS model canonicalises (#255), SH does not | Fable (found while checking) | FILED as a new LOW class row (not this round); the `ftrcS-nan qNaN+` label in the existing probe is wrong by the same convention (records) |

Also settled by measurement since pass 1: the pre-fix value of the `inf`/`snan` rows is `0x80000000` (the host's indefinite), which
Fable had listed as an unsettled premise (`base_head.raw`).

## 1. The product diff (scratch clone `/tmp/gxfix576` vs the HEAD clone `/tmp/gxdivw`; this is the diff that will be applied to
##    `GXEMUL-SEC/src/cpus/cpu_sh_instr.c` and byte-identically to `est/`)

```diff
--- /tmp/gxdivw/src/cpus/cpu_sh_instr.c	2026-10-25 16:35:18.000000000 -0500
+++ /tmp/gxfix576/src/cpus/cpu_sh_instr.c	2026-11-02 17:17:00.083312437 -0600
@@ -3054,7 +3054,11 @@
 	FLOATING_POINT_AVAILABLE_CHECK;
 
 	ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);
-	cpu->cd.sh.fpul = (int32_t) op1.f;
+	/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt
+	    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into
+	    fpul here -- the FTRC store, mis-copied -- so a guest reading FPUL
+	    after an FCNVSD saw a truncated integer.  Removed; nothing else in
+	    this handler changes.  */
 
 	/*  Store double-precision result:  */
 	ieee = ieee_store_float_value(op1.f, IEEE_FMT_D);
```

## 2. The full handler AFTER the edit (`src/cpus/cpu_sh_instr.c:3049-3067` in the fixed clone; the sibling `X(fcnvds_drm_fpul)`
##    immediately below it is untouched)

```c
   3049  X(fcnvsd_fpul_drn)
   3050  {
   3051  	struct ieee_float_value op1;
   3052  	int64_t ieee;
   3053
   3054  	FLOATING_POINT_AVAILABLE_CHECK;
   3055
   3056  	ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);
   3057  	/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt
   3058  	    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into
   3059  	    fpul here -- the FTRC store, mis-copied -- so a guest reading FPUL
   3060  	    after an FCNVSD saw a truncated integer.  Removed; nothing else in
   3061  	    this handler changes.  */
   3062
   3063  	/*  Store double-precision result:  */
   3064  	ieee = ieee_store_float_value(op1.f, IEEE_FMT_D);
   3065  	reg(ic->arg[0]) = (uint32_t) (ieee >> 32);
   3066  	reg(ic->arg[0] + sizeof(uint32_t)) = (uint32_t) ieee;
   3067  }
```

The only exit path before the conversion is `FLOATING_POINT_AVAILABLE_CHECK` (sr.FD set: raise the FPU-disable exception and
`return`), unchanged.  The handler has no common tail; `reg()` is a direct store into `cpu->cd.sh.fr[]`.

## 3. The detector diff -- `regress/sh_rounding_probe.py` (eight rows appended to VECTORS) and `regress/gate_sh_rounding.sh`
##    (pin 36 -> 52, eight names).  Both diffs are against HEAD's copies.

```diff
--- /dev/fd/63	2026-11-02 17:24:47.000000000 -0600
+++ _scratchpad/w576/sh_rounding_probe.NEW.py	2026-11-02 17:16:50.615889300 -0600
@@ -205,6 +205,42 @@
     ("subn fdiv 2ulp/1ulp", NODN, {"fr0": 0x00000002, "fr1": 0x00000001},
      instr(0xf013, 0),                       # fdiv fr1,fr0
      {RN: 0x40000000}),
+
+    # ---- #576: FCNVSD FPUL,DRn reads FPUL and writes DRn only (sh4_programming.txt 9.29,
+    #  :10866-10871).  HEAD also stored (int32_t) op1.f into FPUL -- upstream residue, the FTRC
+    #  store mis-copied -- so a guest reading FPUL after an FCNVSD saw a truncated integer.  The
+    #  six FPUL rows read FPUL back through the guest's own `sts fpul,r2 ; mov.l r2,@r1' (the ftrc
+    #  shape); the two DRn rows read the converted halves with fmov.s and are the identity-medium
+    #  carriers (a handler that writes nothing leaves FPUL alone and only they go red).  Every row
+    #  runs under PR, the manual's defined arm.  `-0' carries NODN so the table has a DN=0 leg;
+    #  `0.1' targets DR0 (0xf0ad) while the others target DR2 (0xf2ad), so a destination-keyed
+    #  re-introduction of the store is seen from both sides; both halves of the destination pair
+    #  are seeded with the sentinel.  0x7fc00000 is a SIGNALING NaN under the SH-4 convention
+    #  (fraction MSB = 1, manual :4980-4989), hence `snan'.  Disclosed, not rowed: finite
+    #  |v| >= 2^31 other than -2^31 (an undefined cast on HEAD), -Inf, a quiet NaN, a subnormal
+    #  input, and +0 (the one fixed point of the removed cast, which no row can observe).
+    ("fcnvsd fpul 1.5",  PR, {"fpul": 0x3fc00000, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0x025a << 16) | 0xf2ad, {RN: 0x3fc00000, RZ: 0x3fc00000},
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd fpul -1.5", PR, {"fpul": 0xbfc00000, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0x025a << 16) | 0xf2ad, {RN: 0xbfc00000, RZ: 0xbfc00000},
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd fpul 0.1",  PR, {"fpul": 0x3dcccccd, "fr0": 0xdeadbeef, "fr1": 0xdeadbeef},
+     (0x025a << 16) | 0xf0ad, {RN: 0x3dcccccd, RZ: 0x3dcccccd},        # DR0
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd fpul -0",   NODN | PR, {"fpul": 0x80000000, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0x025a << 16) | 0xf2ad, {RN: 0x80000000, RZ: 0x80000000},        # DN = 0 leg
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd fpul inf",  PR, {"fpul": 0x7f800000, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0x025a << 16) | 0xf2ad, {RN: 0x7f800000, RZ: 0x7f800000},
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd fpul snan", PR, {"fpul": 0x7fc00000, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0x025a << 16) | 0xf2ad, {RN: 0x7fc00000, RZ: 0x7fc00000},
+     (0x0009 << 16) | 0x2122),
+    ("fcnvsd dr hi",     PR, {"fpul": 0x3dcccccd, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0xf12a << 16) | 0xf2ad, {RN: 0x3fb99999, RZ: 0x3fb99999}),
+    ("fcnvsd dr lo",     PR, {"fpul": 0x3dcccccd, "fr2": 0xdeadbeef, "fr3": 0xdeadbeef},
+     (0xf13a << 16) | 0xf2ad, {RN: 0xa0000000, RZ: 0xa0000000}),
 ]
 
 
```

```diff
--- /dev/fd/63	2026-11-02 17:24:48.000000000 -0600
+++ _scratchpad/w576/gate_sh_rounding.NEW.sh	2026-11-02 17:20:13.799309300 -0600
@@ -61,7 +61,9 @@
 # tie-band witness) + #303's two single-mode subnormal-operand rows (RN pinned; DN
 # STRIPPED by their NODN marker -- a DN=1 numeric expectation would bless a value
 # real silicon flushes; committed bytes 0x32000001 / 0x3f800001 measured live).
-check     "vector-mode pairs run"                  "$want" 36
+#  #576: 36 -> 52.  Eight FCNVSD rows (six FPUL readbacks + the two DRn halves) at two modes each; see the
+#  probe's #576 block.  EQUALITY on purpose: a row that silently vanishes reds here instead of passing a floor.
+check     "vector-mode pairs run"                  "$want" 52
 check     "vector-mode pairs correct"              "$got"  "$want"
 # EXACTLY 9 of the 17 vectors discriminate between the two modes: the 7 from #296 plus
 # the #299-fixed fsub band row and the #300-fixed D-division row (each a PIN until its
@@ -77,7 +79,9 @@
 # and the tie's RN arm).
 for v in "fdiv" "float" "fadd " "fmac " "fmactie" "fipr" "ftrv" "fmul" \
          "fsub band" "faddinf" "Ddiv" "ftrcS-inf" "ftrcS-ovf" "ftrcS-nan" "ftrcS-edge" \
-         "ftrcD-2p31" "ftrcD-neghalf"; do
+         "ftrcD-2p31" "ftrcD-neghalf" \
+         "fcnvsd fpul 1.5" "fcnvsd fpul -1.5" "fcnvsd fpul 0.1" "fcnvsd fpul -0" \
+         "fcnvsd fpul inf" "fcnvsd fpul snan" "fcnvsd dr hi" "fcnvsd dr lo"; do
     n=$(grep -c "^$v.*ok$" "$LOG")
     check "  $v: both modes correct" "$n" 2
 done
```

The gate file's WORKING copy holds three unrelated uncommitted hunks of this session's 09-17 work (old :530/:590/:822); the commit
stages the gate from a HEAD-based copy carrying only the hunks above (the project's #548 recipe).

## 4. The witness (rung 3, the SAME script on both builds)

`regress/artifacts/shfcnvsdfpul/witness_20261102/`: `witness_head.out` RESULT=3/6 on HEAD (the three FPUL rows red with exactly the
truncated integer; liveness and the FCNVDS control ok); `witness_fixed.out` RESULT=6/6 on the fixed clone.  Clause (i) of the witness
rule is met with one script and two builds.

## 5. The pre-table check and the kill table (`regress/artifacts/shfcnvsdfpul/killtable_20261102/`)

PRETABLE.out was written 17:18, before the base leg ran; its text, including the one prediction it got wrong (corrected in place):

```
PRETABLE -- #576 shfcnvsdfpul, written 2026-11-02 before table 1 (the HEAD base leg) runs; HEAD 987cb596; detector = the 8 rows
appended to regress/sh_rounding_probe.py (file w576/sh_rounding_probe.NEW.py), gate pin 36 -> 52, disc 9 unchanged.

SIBLING PARITY: the de-fatalised-arm form does not apply (no arm is de-fatalised; the edit deletes a store).  The sibling handler
  X(fcnvds_drm_fpul) writes FPUL by design (manual 9.28 :10759) and the witness's `fcnvds ctl' row measured that channel live on
  HEAD (0x3fc00000).  No asymmetry owed; the control is recorded in the witness artifact, not in the detector (scope: Fable Q4,
  Grok Q4 -- an FCNVDS row here would be scope growth).
CLAIM -> ROW: the added comment claims "FCNVSD reads FPUL and writes DRn only".  Reads: the six FPUL rows (1.5, -1.5, 0.1, -0,
  inf, snan).  Writes: `fcnvsd dr hi' / `fcnvsd dr lo'.  No other sentence in the diff asserts an observable.
GUARD FIELD vs BODY FIELD: the only predicate dominating the edited line is FLOATING_POINT_AVAILABLE_CHECK (sr.FD, cpu_sh_instr.c:57-66);
  the body reads cd.sh.fpul and writes fr[r8], fr[r8+1]; the predicate reads sr only, so no field disagreement state is owed.
  Partition the body induces on its lvalues: NONE (the body tests nothing; sh_dn()'s DN test and fpclassify live in callees, outside
  the DEPENDS-ON bound).  Clause (d) for a pure deletion = the removed store re-introduced under a DIFFERENT predicate: forms (f) DN
  and (g) destination are clause-(e) material by the rule's letter; both are caught anyway at zero cost (one NODN row, one DR0 row).
CHANNEL, per row (mutant it kills -> observable that differs):
  fcnvsd fpul 1.5    M_b verbatim, M_g (DR2 form), M_h low-half, M_e(RZ-only, toward-zero leg) -> FPUL readback word 0x3fc00000 vs 0x00000001 / 0x00000000
  fcnvsd fpul -1.5   M_b, M_g, M_h -> 0xbfc00000 vs 0xffffffff / low half
  fcnvsd fpul 0.1    M_b, M_h (0xa0000000), M_c? no (FPUL unchanged on identity), M_g-mirror (== DR0 form) -> 0x3dcccccd vs 0 / 0xa0000000
  fcnvsd fpul -0     M_b, M_z (store 0 on zero), M_f (DN-clear form; this row runs DN=0) -> 0x80000000 vs 0x00000000
  fcnvsd fpul inf    M_b, M_d (specials -> 0x80000000) -> 0x7f800000 vs 0x80000000 (host indefinite; the pre-fix value is a measurement)
  fcnvsd fpul snan   M_b, M_d -> 0x7fc00000 vs 0x80000000 (same caveat)
  fcnvsd dr hi       M_c identity body, M_i halves exchanged -> 0x3fb99999 vs 0xdeadbeef / 0xa0000000
  fcnvsd dr lo       M_c identity body, M_i -> 0xa0000000 vs 0xdeadbeef / 0x3fb99999
  Vacuous-by-construction check: no row's channel is invariant under its named mutant.  The identity medium (clause (c)) is carried
  by the two DRn rows ONLY; every FPUL row is green on it by construction (stated in the probe comment and the contract).
PREDICTIONS (to be compared with the table, per the frozen-number rule these are predictions, not scores):
  base (HEAD): 40/52 -- the six FPUL rows red in both modes (12 red lines), everything else ok.  `inf'/`snan' pre-fix values are
               the host's indefinite 0x80000000 by reading (Fable unsettled premise; this leg settles it).
  fixed:       52/52.
  M_b 40/52; M_c 48/52 (dr hi/lo both modes); M_f 50/52 (`-0' both modes); M_g 50/52 (`0.1' both modes, the DR0 row); M_h 40/52;
  M_i 48/52; M_z 50/52; M_d 48/52 (inf, snan).

CORRECTION 2026-11-02 17:2x, after the table (left in place, quoting what it refutes): the prediction line above said
"M_g 50/52 (`0.1' both modes, the DR0 row)".  MEASURED M_g = 42/52 with the FIVE DR2 rows red and the DR0 row GREEN: under
`!= &fr[0]' the store happens for every destination except DR0, so the DR0 row is the one that stays green.  The prediction
had the direction inverted.  The MIRROR (`== &fr[0]', built as M_gm after the table) measured 50/52 with ONLY the DR0 row
red -- which is the cell the DR0 row was added for (Fable pass 1, change 3).  Every other prediction matched.
```

Measured scores (`<leg>.raw`; each header names the binary, its md5 and its freshness; `KILLTABLE.log` is the driver's log):

| leg | what the handler does | SH_ROUND_RESULT | red rows (both modes) |
|---|---|---|---|
| base_head | HEAD 987cb596 | 40/52 | all six FPUL rows |
| fixed | the diff above | 52/52 | none |
| M_b | the removed store reinstated verbatim (clause (b)) | 40/52 | all six FPUL rows |
| M_c | identity body: decode and retire, write nothing (clause (c), the null medium) | 48/52 | `dr hi`, `dr lo` |
| M_d | store 0x80000000 only for Inf/NaN | 48/52 | `inf`, `snan` |
| M_f | store only when FPSCR.DN is clear | 50/52 | `-0` (the NODN row) |
| M_g | store for every destination except DR0 | 42/52 | the five DR2 rows |
| M_gm | store only for DR0 (M_g's mirror) | 50/52 | `0.1` (the DR0 row) |
| M_h | the result's low half stored into FPUL after the DRn store | 40/52 | all six FPUL rows |
| M_i | the two DRn halves exchanged | 48/52 | `dr hi`, `dr lo` |
| M_z | store 0 when the operand is zero | 50/52 | `-0` |

Floor record: (a) base 40/52; (b) M_b 40/52; (c): measured at `killtable_20261102/M_c.raw` (identity body, 48/52, carried by the two
DRn rows only, as the contract says); (d) the fix is a pure deletion, so (d) is the removed store re-introduced under a different
predicate: M_f, M_g, M_gm and M_z are all red; (e) the contract is the probe's #576 comment; (f) does not apply (no address decode is
pinned).  No dead session in any leg (no `FAIL(no-readback)` anywhere).

## 6. Records that ship with the fix (drafts; correct them)

* CHANGELOG round block `#576 shfcnvsdfpul`: defect, fix, witness (3/6 -> 6/6), detector (8 rows, pin 36 -> 52), the table above, the
  F1 correction, the F9 filing, and "assessed, not changed": FCNVDS (writes FPUL by design), the PR=0 reserved-encoding class (filed once
  as a class per pass 1), the DN=1 subnormal input (#303's named gap), the DRn NaN pattern (F9).
* `OUTSTANDING_BUGS.md`: the `shfcnvsdfpul` entry (:24069) -> fixed by #576; the prose row at :8240 corrected in place: "the same UB
  `(int32_t)` cast `#297` removed from FTRC" -> "the same `(int32_t)` cast that `#297` GUARDED in FTRC behind a range ladder (the casts
  remain at :3016 and :3038)".
* ledger: `shfcnvsdfpul` closed, witness `probe:regress/artifacts/shfcnvsdfpul/witness_20261102/sh_fcnvsd_witness.py`, detector rows
  named; a new LOW row for F9 (title written from Fable's finding).
* `scope_sh_20261030/SCOPING.md` and the pass-1 draft: the same `#297` wording correction.

## 7. Questions

**Q1, the diff.**  Is the edit right and complete?  Read the handler after the edit (section 2): does deleting the store change any
other observable (the DRn value, FPSCR, exception behaviour)?  Does the comment state anything the code does not do?

**Q2, the floor.**  With the table in section 5: is any floor cell OPEN?  The fix depends on one dominating predicate (sr.FD, whose only
reachable cell at the body is FD = 0) and the body tests nothing; the (d) forms built are DN, destination (both directions) and
zero-operand.  Name a nulled-repair form that escapes all 52 rows, if you can, with the input at which it first differs from the fixed
handler.

**Q3, the ask-again (one, capped).**  What is the smallest edit to the FIXED handler that keeps every one of the 52 rows green and still
changes guest-visible behaviour?  Name the row that would catch it, or say that it is clause-(e) disclosure already written in the
contract.

**Q4, the records.**  Is each sentence in section 6 true of the artifacts and the code?  Is the F1 correction worded right?  Is F8
(keeping `inf`) the right call?

**Q5, the roster.**  Astra's pass-2 answer arrives in its next window.  Say whether anything above should HOLD the commit for it beyond
the standing rule, or whether the four-seat pass 2 plus Astra's later answer suffices.

**If, while verifying a claim, you found something ELSE -- say so.**  End with `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBP2SHFCNVSD: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
