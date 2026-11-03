# PANEL PASS 2 -- `shblreset` (#577): the real diff, the detector, the pre-table check and the measured kill table

Fired 2026-11-02 18:4x.  HEAD `987cb596`.  Roster (owner 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3, Argon (Gemini web), Grok 4.7.
Astra is on its weekly wall (hotmail, "try again at Nov 8th"); glm-5.3 is DOWN (the Ollama cloud endpoint answers 403/1010 to every
model); both are recorded as seat failures, not agreement.  The owner holds every commit until Astra answers; this pass and the F2
adjudication run now and the round then waits.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `987cb596`.**  The diff below lives in a scratch clone (`/tmp/gxfix577`, WSL); no
project tree is edited.  File-reading seats: compare against `git show HEAD:<path>`, never the working tree (its `dev_sh4.c` carries
uncommitted comment lines that shift line numbers by about 126 -- a pass-1 seat read `:1304` for the multiple-hit raiser that HEAD has at
`:1178-1179`) and never `./src/`.  **Packet-fed seats: everything you need is inlined.**  Every number names its artifact.  **VERDICT
LINE FIRST AND LAST**: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP`.

## 0. Pass 1 and what changed (F1..F10, with dispositions)

Pass 1 (`w577/pass1_20261102/`): Argon PROCEED; Grok 4.7 PROCEED WITH CHANGES (3); Fable 5.1 PROCEED WITH CHANGES (3); glm DOWN;
Astra WALLED.  All three answering seats: the constant and the one exemption are the right patch.

| # | finding | raised by | disposition |
|---|---|---|---|
| F1 | the proposed row names (15 and 16 characters) overflow the probe's `%-14s` column and the gate's two-space anchor `^$v  .*ok$` can then never match (the padded-column trap; the gate's own comment caps names at 13) | Grok, Fable | ACCEPTED: `tlbm bl trapa` (13), `tlbm bl mhit` (12), `tlbm bl ldmis` (13), `tlbm trapa` (10) |
| F2 | add a BL-set row at a second general code from a different raise site -- a misaligned longword load (`SH_ALIGN_CHECK_LD`, H'0E0) -- so a rewrite keyed to TRAPA alone, and the sub-H'100 half of the `< 0x100` form, are caught | Grok, Fable | ACCEPTED: `tlbm bl ldmis` (`mov.l @r1,r2` with r1 odd, want H'020); measured: it is the ONLY row that reds M_trapaonly and one of two that red M_lt100 |
| F3 | commit the witness's BL-clear TRAPA control (H'160) as a row | Grok | ACCEPTED: `tlbm trapa`; pin 6 -> 10 |
| F4 | the fix comment cited `:678-681`, the manual's REVISION-HISTORY table; the normative text is 5.6.1 (2) Manual Reset `:12376`, `:12383-12384` ("Exception code H'020 is set in EXPEVT") | Fable | ACCEPTED: comment rewritten (section 2) |
| F5 | the user-break sentence should say the UBC SUPPRESSES a break under BL (`:41448-41452`), so no arm here will ever need a user-break case | Fable | ACCEPTED (section 2) |
| F6 | the brief's reason for "interrupts do not reach the block" was wrong: an interrupt delivered with BL set would NOT latch a code, because the `intevt > 0` branch (`:945-947`) sets the local `expevt = -1` and never stores EXPEVT; the dyntrans gate is load-bearing for "held pending", not for EXPEVT | Fable, Grok | ACCEPTED: comment and record carry the true reason |
| F7 | "the only raiser is at `dev_sh4.c:1304-1305`, not `:1178`" | Grok | REJECTED: HEAD has it at `:1178-1179` (`git show HEAD:src/devices/dev_sh4.c`); `:1304` is the WORKING-TREE offset from this session's uncommitted comment lines in that file |
| F8 | the brief's candidate (e) "`< 0x100`" is a FAILING mutant (0x140 is not below 0x100), not "every reset-category code exempted" | Grok | ACCEPTED: built as `M_lt100`; measured 8/10 (see section 5 and the sibling correction) |
| F9 | the unlatched `fatal()` at `:911` stays with the held `floodclass` row; a `(once)` latch here would be a second behaviour and would owe its own row and channel | Fable, Grok | ACCEPTED: not ridden; recorded under `floodclass` |
| F10 | found while checking: SLEEP under BL never wakes in this tree (the manual accepts interrupts in sleep with BL=1, `:13170-13171`), and the #457 comment at `cpu_sh.c:985-989` becomes unconditionally true with this fix | Fable | FILED (SLEEP) / RECORDED (one clause in the round block) |

## 1. The product diff (`/tmp/gxfix577` vs the HEAD clone; applied by `apply_fix577.py`, the same text that will land in
##    `GXEMUL-SEC/src/cpus/cpu_sh.c` and byte-identically in `est/`)

```diff
--- /tmp/gxdivw/src/cpus/cpu_sh.c	2026-10-25 16:35:18.000000000 -0500
+++ /tmp/gxfix577/src/cpus/cpu_sh.c	2026-11-02 18:11:03.422929869 -0600
@@ -910,11 +910,20 @@
 	if (cpu->cd.sh.sr & SH_SR_BL) {
 		fatal("[ sh_exception(): BL bit already set. ]\n");
 
-		/*  This is actually OK in two cases: a User Break,
-		    or on NMI interrupts if a special flag is set?  */
-		/*  TODO  */
-
-		expevt = EXPEVT_RESET_POWER;
+		/*  #577: a general exception taken with BL set is a MANUAL
+		    reset: sh7750_hardware.txt 5.5.3 (:12302-12304) and 5.6.1
+		    (2) Manual Reset, :12376 and :12383-12384 -- "Exception code
+		    H'020 is set in EXPEVT" -- not a power-on reset (H'000),
+		    which is what stood here.  The two TLB multiple-hit
+		    exceptions are reset-category in their own right (Table
+		    5.2, :12006 and :12010; code H'140, :12461) and keep their
+		    code.  A user break under BL is suppressed at the UBC
+		    (:41448-41452) and never reaches here; EXPEVT_BREAK has no
+		    raiser in this tree.  An interrupt cannot latch a code here
+		    either: cpu_dyntrans.c delivers none while BL is set, and
+		    the intevt path below discards expevt before storing it.  */
+		if (expevt != EXPEVT_RESET_TLB_MULTI_HIT)
+			expevt = EXPEVT_RESET_MANUAL;
 	}
 
 	if (cpu->is_halted) {
```

## 2. The block AFTER the edit (`src/cpus/cpu_sh.c:910-927` in the fixed clone; the common code at `:941-955` and the shared reset arm,
##    now `:1024-1030`, are untouched)

```c
    910  	if (cpu->cd.sh.sr & SH_SR_BL) {
    911  		fatal("[ sh_exception(): BL bit already set. ]\n");
    912
    913  		/*  #577: a general exception taken with BL set is a MANUAL
    914  		    reset: sh7750_hardware.txt 5.5.3 (:12302-12304) and 5.6.1
    915  		    (2) Manual Reset, :12376 and :12383-12384 -- "Exception code
    916  		    H'020 is set in EXPEVT" -- not a power-on reset (H'000),
    917  		    which is what stood here.  The two TLB multiple-hit
    918  		    exceptions are reset-category in their own right (Table
    919  		    5.2, :12006 and :12010; code H'140, :12461) and keep their
    920  		    code.  A user break under BL is suppressed at the UBC
    921  		    (:41448-41452) and never reaches here; EXPEVT_BREAK has no
    922  		    raiser in this tree.  An interrupt cannot latch a code here
    923  		    either: cpu_dyntrans.c delivers none while BL is set, and
    924  		    the intevt path below discards expevt before storing it.  */
    925  		if (expevt != EXPEVT_RESET_TLB_MULTI_HIT)
    926  			expevt = EXPEVT_RESET_MANUAL;
    927  	}
```

## 3. The detector diff -- `regress/sh_tlbmulti_probe.py` (session() gains `program`/`steps`; four rows; the docstring note becomes
##    history) and `regress/gate_sh_rounding.sh` (pin 6 -> 10, four names).  Both against HEAD's copies.

```diff
--- /dev/fd/63	2026-11-02 18:08:36.000000000 -0600
+++ sh_tlbmulti_probe.NEW.py	2026-11-02 18:08:36.022039200 -0600
@@ -52,9 +52,10 @@
 
   * The exception flips `SR.RB`, so `r0-r7` are the other bank afterwards.  Anything
     read back across the fault uses `r8-r15`, which are unbanked.
-  * `cpu_sh.c` rewrites ANY expevt to `EXPEVT_RESET_POWER` when `SR.BL` is set, before
-    the assignment.  This tree resets with BL clear, so the path is live -- but a
-    BL-set guest silently latches `0x000` instead.
+  * `cpu_sh.c` USED TO rewrite ANY expevt to `EXPEVT_RESET_POWER` when `SR.BL` is set
+    (a BL-set guest silently latched `0x000`, the multiple hit included).  #577 makes it
+    `EXPEVT_RESET_MANUAL` with the multiple-hit code exempt; the BL rows at the end of
+    this file pin both halves.
 """
 import os
 import pty
@@ -88,11 +89,13 @@
           % (name, got, want, "#457", "ok" if ok else "FAIL"))
 
 
-def session(pre=(), entry1_vpn=VPN_A, settle=8.0, trigger=True):
+def session(pre=(), entry1_vpn=VPN_A, settle=8.0, trigger=True, program=None, steps=None):
     """Install two UTLB entries then do the associative write. Returns (regs, died).
 
     `pre` runs before the trigger -- used to pre-set SR so the reset transition's
     SR update is observable.
+    #577: `program` (a list of 16-bit words placed at CODE) and `steps` replace the
+    three-store multiple-hit program for the BL rows; the default is that program.
     """
     pid, fd = pty.fork()
     if pid == 0:
@@ -122,14 +125,18 @@
     #  defect and reported DEAD on the committed build -- a control failing for the
     #  very reason it exists to rule out.  Rule 4: did it fail for the reason under
     #  test?  It did not.
-    cmds = list(pre) + ([] if not trigger else [
-        "r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0,
-        "r4=0x%08x" % entry1_vpn, "r5=0x%x" % ENTRY1,
-        "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC,
-        "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),
-        "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R4_AT_R5),
-        "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R6_AT_R7),
-        "pc=0x%x" % CODE, "step 3"]) + [
+    if program is None:
+        trig = ["r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0,
+                "r4=0x%08x" % entry1_vpn, "r5=0x%x" % ENTRY1,
+                "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC,
+                "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),
+                "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R4_AT_R5),
+                "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R6_AT_R7),
+                "pc=0x%x" % CODE, "step 3"]
+    else:   # #577: an arbitrary short program; the caller seeds registers through `pre`
+        trig = ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(program)]
+        trig += ["pc=0x%x" % CODE, "step %d" % (steps if steps is not None else len(program))]
+    cmds = list(pre) + ([] if not trigger else trig) + [
         #  `registers` does not exist as a command, and a bare dump would not show
         #  these anyway: cpu_sh.c prints expevt/vbr only under `coprocs & 2`.
         #  `print <name>` reads them through CPU_SETTINGS_ADD_REGISTER32.  Established
@@ -191,4 +198,33 @@
 t3, died3 = session(entry1_vpn=VPN_B)
 row("tlbm single", "died" if died3 else reg(t3, "expevt"), "0x00000000")
 
+
+#  ---- #577: a general exception taken with SR.BL set is a MANUAL reset -----------
+#  sh7750_hardware.txt 5.5.3 (:12302-12304): with BL set, a general exception other than a
+#  user break performs a manual reset; EXPEVT is H'020 (:678-681).  Table 5.2 (:12006,
+#  :12010) lists the two TLB multiple-hit exceptions as reset-category in their own right,
+#  code H'140 (:12461), so the BL rule must not touch them.  HEAD's sh_exception() rewrote
+#  EVERY code to EXPEVT_RESET_POWER (H'000) when BL was set; #577 makes it EXPEVT_RESET_MANUAL
+#  with the multiple-hit code exempt.  Rows run under sr = MD|BL (0x500000f0, RB clear so the
+#  bank-0 seeds are the ones the program uses); `tlbm trapa' is the BL-CLEAR control that pins
+#  the general vector's own code.  Contract: TRAPA (H'160) and a misaligned load (H'0E0) are
+#  the two general codes driven; a re-introduction of the rewrite keyed to a code this table
+#  does not drive (a TLB miss, a reserved instruction) is clause-(e) disclosure.  The identity
+#  medium for this predicate round is the BL block DELETED: `tlbm bl trapa' and `tlbm bl ldmis'
+#  then read their own codes (red); `tlbm bl mhit' reads H'140 either way and cannot carry it.
+#  Names stay at 13 characters or fewer: row() prints `%-14s' and the gate anchors `^$v  .*ok$'
+#  with TWO spaces (Grok, pass 1 -- the padded-column trap).
+SR_MD_BL = 0x500000f0
+SR_MD = 0x400000f0
+TRAPA_1 = 0xc301            # trapa #1  : 1100 0011 0000 0001
+MOV_L_AT_R1_R2 = 0x6212     # mov.l @r1,r2 : 0110 0010 0001 0010
+t5, died5 = session(pre=["sr=0x%08x" % SR_MD_BL], program=[TRAPA_1], steps=1)
+row("tlbm bl trapa", "died" if died5 else reg(t5, "expevt"), "0x00000020")
+t6, died6 = session(pre=["sr=0x%08x" % SR_MD_BL])
+row("tlbm bl mhit", "died" if died6 else reg(t6, "expevt"), "0x00000140")
+t7, died7 = session(pre=["sr=0x%08x" % SR_MD_BL, "r1=0x%08x" % (CODE + 1)], program=[MOV_L_AT_R1_R2], steps=1)
+row("tlbm bl ldmis", "died" if died7 else reg(t7, "expevt"), "0x00000020")
+t8, died8 = session(pre=["sr=0x%08x" % SR_MD], program=[TRAPA_1], steps=1)
+row("tlbm trapa", "died" if died8 else reg(t8, "expevt"), "0x00000160")
+
 print("SH_TLBMULTI_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
```

```diff
--- /dev/fd/63	2026-11-02 18:41:00.000000000 -0600
+++ gate_sh_rounding.NEW.sh	2026-11-02 18:08:36.042456200 -0600
@@ -251,9 +251,11 @@
     tmctrl=$(grep -o "SH_TLBMULTI_CONTROL=[A-Z]*" "$TMLOG" | tail -1 | cut -d= -f2)
     check "sh_tlbmulti control proves it measures" "${tmctrl:-missing}" "OK"
     tmres=$(grep -o "SH_TLBMULTI_RESULT=[0-9]*/[0-9]*" "$TMLOG" | tail -1 | cut -d= -f2)
-    check "sh_tlbmulti rows run"     "${tmres#*/}" 6
+    #  #577: 6 -> 10 (three BL rows + the BL-clear TRAPA control; see the probe).  EQUALITY on purpose.
+    check "sh_tlbmulti rows run"     "${tmres#*/}" 10
     check "sh_tlbmulti rows correct" "${tmres%/*}" "${tmres#*/}"
-    for v in "tlbm alive" "tlbm expevt" "tlbm pc" "tlbm vbr" "tlbm sr" "tlbm single"; do
+    for v in "tlbm alive" "tlbm expevt" "tlbm pc" "tlbm vbr" "tlbm sr" "tlbm single" \
+             "tlbm bl trapa" "tlbm bl mhit" "tlbm bl ldmis" "tlbm trapa"; do
         n=$(count "$TMLOG" "^$v  .*ok$")
         check "  $v" "$n" 1
     done
```

The gate's working copy holds three unrelated uncommitted hunks (old :530/:590/:822) and round #576's two staged hunks (not yet
committed; #576 is held for Astra); this round's hunk is staged from a HEAD-based copy and the two rounds' copies are reconciled at
whichever lands second.

## 4. The witness (rung 3, the same script on both builds) -- `regress/artifacts/shblreset/witness_20261102/`

`witness_head.out` RESULT=2/4 on HEAD: `bl trapa expevt` 0x00000000 (want 0x020) and `bl multihit` 0x00000000 (want 0x140), both
FAILED-FOR-THE-REASON-UNDER-TEST; `bl trapa pc` 0xa0000000 ok (liveness); `nobl trapa expevt` 0x160 ok (control).  `witness_fixed.out`
RESULT=4/4 on the fixed clone (built 17:47, and rebuilt 18:11 with the final comment; binary fresh both times).

## 5. The pre-table check and the kill table -- `regress/artifacts/shblreset/killtable_20261102/`

`PRETABLE.out` (mtime 18:10:13; the base leg started 18:11:05 per `KILLTABLE.log`, so the order is proved by the artifacts this time)
and its SIBLING correction, both verbatim:

```
PRETABLE -- #577 shblreset, written before table 1 (the HEAD base leg) runs; HEAD 987cb596.  Detector = four rows appended to
regress/sh_tlbmulti_probe.py (w577/sh_tlbmulti_probe.NEW.py), gate pin `sh_tlbmulti rows run` 6 -> 10.  A correction, if one is
needed after the table, goes to the SIBLING file PRETABLE_CORRECTION.out so this file's mtime keeps proving the order (#576's lesson).

SIBLING PARITY: the three reset-category codes share one arm (cpu_sh.c:1015-1021); the fix changes which code the BL block latches
  and nothing in the arm.  `tlbm pc' / `tlbm vbr' / `tlbm sr' already pin the arm on the multiple-hit path; no new arm row is owed.
CLAIM -> ROW: the added comment claims (1) a BL-set general exception latches H'020 -> `tlbm bl trapa', `tlbm bl ldmis';
  (2) the multiple hit keeps H'140 -> `tlbm bl mhit'; (3) the user-break exemption has no raiser and interrupts do not reach the
  block -> no row (both are absence claims, checked by grep: EXPEVT_BREAK appears only in the define; cpu_dyntrans.c:247 gates on BL).
GUARD FIELD vs BODY FIELD: the dominating predicate of the edited lines is `cpu->cd.sh.sr & SH_SR_BL' (reads sr); the body reads
  `expevt' (the parameter) and, after the fix, tests it against EXPEVT_RESET_TLB_MULTI_HIT.  Partition the body induces on expevt:
  {== 0x140, != 0x140}.  Floor cells = {BL set} x {multi-hit, other}: both rowed (`tlbm bl mhit'; `tlbm bl trapa'/`tlbm bl ldmis').
  sr and expevt are written at different sites (sr by the guest / the exception entry; expevt by the raiser), but the body's test is
  on expevt alone, so no disagreeing-state row is owed.  Partition on sr beyond BL: none tested by the body.
CHANNEL, per row (mutant it kills -> observable that differs):
  tlbm bl trapa   M_b (0x000), M_c (0x160: the block gone), M_power (0x000), M_trapaonly? NO (green: TRAPA is the keyed code) -> EXPEVT readback
  tlbm bl ldmis   M_b (0x000), M_c (0x0e0), M_power (0x000), M_trapaonly (0x0e0 -- the row Grok asked for) -> EXPEVT readback
  tlbm bl mhit    M_b (0x000), M_noex (0x020), M_wrongex (0x020), M_lt100 (0x020: 0x140 is not below 0x100 so it is rewritten) -> EXPEVT
  tlbm trapa      the BL-clear control: M_c? no (0x160 either way); it reds a mutant that rewrites with BL CLEAR (none built; disclosed)
  Vacuous-by-construction check: `tlbm bl mhit' cannot see M_c (0x140 either way) -- stated in the contract; carried by the two general
  rows.  `tlbm trapa' sees no built mutant: it is a CONTROL (the general vector's own code) and is recorded as such, not as a kill row.
PREDICTIONS (predictions, not scores):
  base (HEAD)  7/10  -- the three BL rows red (0x000 each), `tlbm trapa' and the six committed rows ok
  fixed       10/10
  M_b          7/10 (bl trapa, bl ldmis, bl mhit)      M_c          8/10 (bl trapa 0x160, bl ldmis 0x0e0)
  M_noex       9/10 (bl mhit 0x020)                    M_wrongex    9/10 (bl mhit 0x020; bl trapa reads 0x160? NO -- `!= TRAPA' leaves TRAPA
                                                                      at 0x160 -> ALSO red: predict 8/10)
  M_lt100      9/10 (bl mhit 0x020)                    M_trapaonly  9/10 (bl ldmis 0x0e0)      M_power 8/10 (bl trapa, bl ldmis 0x000)
```
```
PRETABLE_CORRECTION -- #577, written after the table (sibling file; PRETABLE.out's own mtime, 18:10:13, is untouched and precedes
the base leg at 18:11:05 in KILLTABLE.log).  Quoting what it refutes: PRETABLE.out predicted "M_lt100  9/10 (bl mhit 0x020)".
MEASURED 8/10: `tlbm bl mhit' red (0x140 >= 0x100, so the multiple hit is rewritten to 0x020) AND `tlbm bl ldmis' red -- the
misaligned-load code 0x0e0 is BELOW 0x100, so that form exempts it and it stays 0x0e0 where 0x020 is wanted.  The prediction had the
direction of the exemption wrong for the sub-0x100 general codes; the row Grok asked for is what saw it.  Every other prediction
matched (base 7/10; fixed 10/10; M_b 7; M_c 8; M_noex 9; M_wrongex 8, corrected in-line before the table; M_trapaonly 9; M_power 8).
```

Measured (`<leg>.raw`, each header naming the binary, md5 and freshness; the instrument the table ran is preserved as
`sh_tlbmulti_probe.ASRUN.py`, byte-identical to the shipped copy):

| leg | what the block does | SH_TLBMULTI_RESULT | red rows |
|---|---|---|---|
| base_head | HEAD 987cb596 | 7/10 | bl trapa, bl mhit, bl ldmis (each 0x000) |
| fixed | the diff above | 10/10 | none |
| M_b | `expevt = EXPEVT_RESET_POWER;` verbatim (b) | 7/10 | bl trapa, bl mhit, bl ldmis |
| M_c | the block deleted: no rewrite (c, identity for a predicate round) | 8/10 | bl trapa (0x160), bl ldmis (0x0e0) |
| M_noex | exemption removed: always MANUAL (d) | 9/10 | bl mhit (0x020) |
| M_wrongex | exemption on TRAPA instead of the multiple hit (d) | 8/10 | bl trapa (0x160), bl mhit (0x020) |
| M_lt100 | rewrite only codes >= 0x100 (d / F8) | 8/10 | bl mhit (0x020), bl ldmis (0x0e0) |
| M_trapaonly | rewrite only TRAPA (e) | 9/10 | bl ldmis (0x0e0) |
| M_power | exemption kept, constant POWER (d) | 8/10 | bl trapa, bl ldmis (0x000) |

Floor: (a) 7/10; (b) 7/10; (c): measured at `M_c.raw` -- carried by `tlbm bl trapa` and `tlbm bl ldmis` (`tlbm bl mhit` reads 0x140
either way and cannot carry it, as the contract says); (d) the fix ADDS one predicate (`expevt != EXPEVT_RESET_TLB_MULTI_HIT`) and
changes one constant: M_noex, M_wrongex, M_lt100 and M_power weaken or re-key them, all red; (e) the contract names TRAPA and the
misaligned load as the general codes driven and discloses the rest (a rewrite keyed to a code the table does not drive escapes:
M_trapaonly is the measured instance of that class, caught only because F2 added the second code).  `tlbm trapa` is a CONTROL and sees
no built mutant (disclosed).  No dead session in any leg.

## 6. Records that ship with the fix (drafts; correct them)

* CHANGELOG round block `#577 shblreset`: defect (both halves, H'000 for the general code and the clobbered H'140), witness 2/4 -> 4/4,
  fix, detector (4 rows, pin 6 -> 10), the table, the sibling correction, F1-F10, "assessed, not changed": the `fatal()` flood
  (`floodclass`), the unmodelled module reset (`shresetinit`), SPC/SSR, H-UDI; the #457 comment clause; the SLEEP-under-BL filing.
* `OUTSTANDING_BUGS.md`: the `shblreset` entry (:24063) -> fixed by #577; a filing for SLEEP under BL.
* ledger: `shblreset` closed, witness `probe:regress/artifacts/shblreset/witness_20261102/sh_blreset_witness.py`, detector rows named;
  the SLEEP row opened.
* `regress/sh_tlbmulti_probe.py`'s docstring note (the stale "rewrites ANY expevt") reworded to history (in the diff above).

## 7. Questions

**Q1, the diff.**  Is the edit right and complete?  Does the comment state anything the code does not do?  (The comment's :12376 and
:12383-12384 citations: check them.)

**Q2, the floor.**  Is any floor cell open?  The dominating predicate is `sr & SH_SR_BL`; the body tests `expevt` as {== H'140, != H'140}.
Name a form that keeps all ten rows green and changes a guest-visible EXPEVT, with the input at which it first differs.

**Q3, the ask-again (one, capped).**  The smallest edit to the FIXED block that keeps all ten rows green and still changes guest-visible
behaviour; the row that would catch it, or the clause-(e) sentence that already discloses it.

**Q4, the records.**  Is each sentence of section 6 true of the artifacts and the code?  Is F7's rejection right?

**Q5, the roster.**  Two seats are missing (Astra walled, glm down).  Should anything here hold beyond the owner's standing hold?

**If, while verifying a claim, you found something ELSE -- say so.**  End with `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP`.
