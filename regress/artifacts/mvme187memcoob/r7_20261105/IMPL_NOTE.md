# mvme187memcoob REPAIR 6 (r7_20261105) -- implementation note, 2026-11-05 (Opus 5.5 implementer)

From regress_20261105/REG_MYTHOS_local.md section 2(d) and DISPOSITION.md.  The probe goes from 206 to 213 rows; no emulator code
changed (src/devices/dev_mvme187.c md5 97e983872a72d159fbaaf54d8694ba49 before and after; regress/gate_arm.sh not edited).

## Order of work, each step's artifact

1. **Step 1, the eight on the 206-row probe** (step1_memc7.sh, run from step1_memc7.run.sh; step1_run.log).  Scratch clone /tmp/gxmemc7
   (cp -a of build/), clone-local .MUTANT, baseline named and cmp'd (SEC's dev_mvme187.c; step1/probe206_frozen.py = the probe
   before repair 6, md5 647d0d5e6c1c87d4527370b272539b23), baseline rebuilt after rm src/cpus/*.o (step1/FRESHNESS.txt: gxemul and the
   device object newer than the source).  base 206/206; all eight 206/206 (step1/SCORES.txt:1-9; applied diffs step1/diff_*.txt).
2. **R18 written** (regress/mvme187_memc_probe.py; backup mvme187_memc_probe.py.pre_r7).  Words: ST_B(5,3,0x18) x2, ST_B(0,3,0x18),
   LD_BU(2,3,0x18), ST_B(5,3,0x08) x2, ST_B(0,3,0x08), LD_BU(4,3,0x08); r5 = 0x01, r2/r4 = SENT.  Seven rows, wants derived from
   dev_mvme187.c: `R18 session` exit0 (no exit path); `R18 18 r2` 0x0 (odata 0 at :61, the default arm sets none, :121-137);
   `R18 08 r4` 0x3 (memconf reads DEVINIT's size code, :104, :162-172 with -M 64; no store kept, :105-118); `R18 pc` CODE + 32 (eight
   accesses, each returns 1, :143); `R18 lines` "2" (one notice per category, :112-117, :127-136); `R18 def line` "unimplemented
   write to offset 0x18 (controller 0): 0x1 (once) ]" (:128-134); `R18 cnf line` "memconf write 0x1 (controller 0) ignored, not
   modelled (once) ]" (:113-115).  The session row is the probe's style for every multi-access session; the review listed six rows.
   Names at most 12 characters (limit 16, asserted).  The probe enforces no input-size cap; R18's stdin is 333 bytes, the largest
   session's (R16) 1,874.  base 213/213 on the clone's restored baseline (base213/probe_base213.out; R18 transcript
   base213/sessions_R18/R18.txt).
3. **PRETABLE_6.out** (12:41:39Z; memc_pretable_6.py, machine form table6/PRED_MAP_6.txt, variant list table6/VARS_6.txt) before
   table 6 started (12:42:44Z).  The model's calibration against table 5's measured legs and 665: 0 mismatches.  The first generation
   had a parser bug of mine (a bare `RED=` matched inside `PRED=`), caught by that calibration before the table ran; its outputs are
   kept as PRETABLE_6.out.parsebug and table6/PRED_MAP_6.txt.parsebug.
4. **Table 6** (table6_memc.sh from table6_memc.run.sh; table6_run.log; table6/VERDICT.md).  Clone /tmp/gxmemc8, legs then the eight
   then the other 657.  ONE MISS: the B3 leg reddened R17 f3 r2 as well as its four predicted rows (0xd8; a byte 111 bytes past the
   device struct's allocation under B3).  b3repeat_memc7.sh (clone /tmp/gxmemc9): one B3 binary, three runs, 0x66, 0x34, 0x15 -- run
   to run.  Everything else matched: the eight each 212/213 on R18 lines alone; 24 of the 665 red, 641 green, exact sets.
5. **Records** -- the nine findings of REG_MYTHOS section 5, each checked first:
   1. UPHELD.  COVERED claimed L_DT_D_idat_W.D red; it was 206/206 and in no family.  Now red in table 6; the CONTRACT cites table 6.
   2. UPHELD.  PRETABLE_5.out:7789-7798 holds four ungated `^= idata` representatives, not one.  The CONTRACT's L_ME_M_xori_any
      clause is deleted (it is red in table 6); FILING item 6's title: ERRATA_r7_20261105.md 4(b).
   3. UPHELD (an omission).  No filed remedy rows the set-latch group; the model confirms R19 reddens only L_ME_M_xori_any and
      L_DA_D_xori_any of the eight.  ERRATA 4(c); R18 is the remedy (measured).
   4. TARGET WRONG, SUBSTANCE UPHELD.  The F1(b) sentence's subject is the 411 UNOBSERVED groups; the eight are NOCHANGE and outside
      it.  What they contradict is the ruling's verdict (:3), :12 and :28.  ERRATA 1-3, plus two inheritors the review did not name
      (r6 ERRATA_PRETABLE_5 item 5; FILING :6-7) and the probe's own "NO surviving cell" sentence (replaced in the probe).
   5. UPHELD, count 97 (single-bit-gated NOCHANGE keeps; the other two NOCHANGE keeps are NB4's).  Disclosed as CONTRACT family (6),
      every NOCHANGE cell except the representatives table 6 measured red, rather than with the review's "nonvacuously" wording.
   6. UPHELD, not fixed here: landing_20261105/ does not exist; the citations are in _scratchpad/wmemc/landing/REGRESS_memc.md:96,
      :1246, :1273 (its :34-35, which the review also cites, name block H1 but not the directory).  DISPOSITION.md routes it to the
      landing-kit agent.
   7. UPHELD (packet wording, REGRESS_memc.md:61).  The four pins' failability is now shown by a REPLAY: SIM_GATE_MEMC.out's
      synthetic legs red "probe completed", "sentinel once", "rows run" and "rows emitted".  *Corrected 2026-11-05
      (regress_20261105/REG2_MYTHOS_local.md item D): this said "now MEASURED".  SIM_GATE_MEMC.out replays the block's text over
      synthetic logs with re-typed helpers (sim_gate_memc.py:42-46); it does not run gate 14.  The measurement is the in-situ
      223-check run at landing.*
   8. UPHELD in form.  The probe now records `Clause (c): measured at r7_20261105/table6/SCORES.txt:3-5 (binary media ...); a build
      without the device was not run`.  The review's "reds ctl * r2 by construction" was not adopted: it rests on an unmeasured
      premise about an access with no device.
   9. UPHELD.  "in its old spelling" is in gate_memc_block.new and in the probe's sibling sentence.
   Also corrected because R18 changed them: CONTRACT family (2)'s parenthetical "1 ^ v is truthy for every store value the rows use"
   (deleted -- R18 stores 0x01), family (4)'s first-store values and family (2)'s clearing-store list (R18 added), FILING item 4's
   ":84" (ERRATA 4(e)), and the session-name collision with FILING's R18/R19 sketches (ERRATA 4(d)).  Edits: apply_r7_records.py,
   apply_r7_records_b.py, two whitespace re-wraps; TEXTONLY_PROOF_r7.txt (AST-equal to table 6's instrument; final md5
   7b31613c414aa3283165cd16e9c977f3); final213/probe_final213.out 213/213 on the restored baseline.
6. **Gate block** gate_memc_block.new (replaces the block from the `mvme187memcoob (#NNN)` banner to the `no indexed read` check;
   supersedes r6_20261105/gate_memc_comment.patch): 213 rows, R18's seven pins, the r6 comment patch folded in without its
   "every one in a debt family ... zero floor cells survive" clause.  Row list = the probe's 213 names in order (checked).
   SIM_GATE_MEMC.out (sim_gate_memc.py): base 223 checks, 0 fails; every leg, the eight and four synthetic logs red; the HEAD-source
   leg red on the source check alone.
7. **Clean-up**: /tmp/gxmemc7, /tmp/gxmemc8, /tmp/gxmemc9 each restored, cmp'd clean against GXEMUL-SEC, binary newer than source,
   sentinel cleared by its own script, then removed.  build/, build-asan/, est/ and /tmp/gxsec-build were not touched.  Side effect:
   importing memc_variants_5.py rewrote its bytecode caches in r5_20261105/__pycache__/ (the script itself is unchanged).

## Model-only results (memc_variants_5.py's device; NOT measured)

* MEMBERS_213.txt (memc_members_213.py): of table 5's 4,299 green cells, R18 turns 328 red; none of the 3,971 that stay green has the
  repair path's own shape (own-arm position, own target, gate `any` or direction/own latch only).
* FILING item 6's R19 sketch against the eight (item 3 above): two of eight.

## For the main loop

* Pass 2 on this repair.  The owner flag stands: under codex's narrower bound the eight are debt; the measurement holds either way.
* est/ does not carry the regress/ edits (propagate at landing, as before).  gate_memc_block.new must be applied by whoever holds
  gate_arm.sh; the landing kit's staged gate block and its 216-check dry run are now stale (223 checks).

## REG2 follow-up, 2026-11-05 (regress_20261105/REG2_MYTHOS_local.md items B, C, D; backups *.pre_reg2)

* B: the walker shows the family-(2) clause "lands on a set latch" is still load-bearing -- 25 UNOBSERVED toggles (18 of them
  representatives table 6 measured green) land on a set latch that the probe later observes, all from a position that does not
  read that latch (MODEL: REG2_CHECK.txt B, memc_reg2_check.py).  The clause is qualified to that, naming L_DT_M_xori_ib0c.
* C: family (6) now excludes the 16 measured-red representatives and the 15 own-shape members of their groups (each with its
  representative's 213-row trace: MODEL, REG2_CHECK.txt C2, memc_reg2_c2.py).  Excluding the whole groups would have dropped the
  disclosure of 378 members the model keeps green, none of them of the repair path's own shape (REG2_CHECK.txt C).
* D: item 7 above corrected in place.  Probe edits text-only: TEXTONLY_PROOF_reg2.txt.
