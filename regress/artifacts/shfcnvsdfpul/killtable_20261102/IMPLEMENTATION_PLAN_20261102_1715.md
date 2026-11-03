# #576 shfcnvsdfpul -- implementation plan (prepared during pass 1; NOT applied until pass 1 converges and Fable + Astra adjudicate)

HEAD 987cb596.  Round number #576.  Witness: regress/artifacts/shfcnvsdfpul/witness_20261102/ (RESULT=3/6 on HEAD, the three FPUL
rows red for the reason under test).  Pass-1 answers so far (w576/pass1_20261102/): Argon PROCEED (14/14 HOLDS); glm-5.3 PROCEED
WITH CHANGES (4); Grok 4.7 PROCEED WITH CHANGES (4); Fable 5.1 and GPT-6 Astra pending (Astra walled until 17:27, re-fire 17:28).

## 1. Product edit (one site, shared file -> byte-identical in GXEMUL-SEC and est/, then propagated to build/, build-asan/,
##    /tmp/gxsec-build with the two-part clearance: cmp clean AND binary newer than source, per tree)

`src/cpus/cpu_sh_instr.c`, X(fcnvsd_fpul_drn), HEAD lines 3056-3057:

    -	ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);
    -	cpu->cd.sh.fpul = (int32_t) op1.f;
    +	ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);
    +	/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt
    +	    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into
    +	    fpul here -- the FTRC store, mis-copied -- so a guest reading FPUL
    +	    after an FCNVSD saw a truncated integer.  Removed; nothing else
    +	    in this handler changes.  */

Settled wording (glm, Grok): #297 GUARDED the FTRC casts (3016, 3038) behind a range ladder; it did not remove them.  Any text
saying "removed" owes a correction (the scoping note; the bug-file entry at OUTSTANDING_BUGS.md:24069 -- re-grep).

## 2. Detector: extend VECTORS in regress/sh_rounding_probe.py (the committed vehicle; working copy is clean)

All eight rows carry PR (Grok change 1: the manual's defined operation is the PR=1 arm) and seed BOTH halves of DR2 with the
sentinel (Grok change 2: registers the seed omits stay at reset; DR0 would make weakening (g) green).  Encodings: fcnvsd fpul,dr2 =
0xf2ad; sts fpul,r2 = 0x025a; mov.l r2,@r1 = 0x2122; nop = 0x0009; fmov.s fr2,@r1 = 0xf12a; fmov.s fr3,@r1 = 0xf13a.  The FPUL rows
are three-instruction rows (second word (0x0009 << 16) | 0x2122); the DRn rows are two-instruction rows.  Names stay under 28
characters and no name is a prefix of another (the gate greps `^$v.*ok$`).

    name                  fpscr   seed                                   word                     want (RN == RZ)
    fcnvsd fpul 1.5       PR      fpul 3fc00000, fr2/fr3 deadbeef         (0x025a<<16)|0xf2ad      0x3fc00000
    fcnvsd fpul -1.5      PR      fpul bfc00000                           same                     0xbfc00000
    fcnvsd fpul 0.1       PR      fpul 3dcccccd                           same                     0x3dcccccd
    fcnvsd fpul -0        PR      fpul 80000000                           same                     0x80000000
    fcnvsd fpul inf       PR      fpul 7f800000                           same                     0x7f800000
    fcnvsd fpul nan       PR      fpul 7fc00000                           same                     0x7fc00000
    fcnvsd dr hi          PR      fpul 3dcccccd, fr2/fr3 deadbeef         (0xf12a<<16)|0xf2ad      0x3fb99999
    fcnvsd dr lo          PR      fpul 3dcccccd, fr2/fr3 deadbeef         (0xf13a<<16)|0xf2ad      0xa0000000
    (adjudication item) fcnvsd fpulDN0 1.5   NODN|PR, single mode RN  -- the DN-clear leg glm says clause (d) owes and Grok
                        says is a disclosure.  One session.  DECIDE IN PASS-1 ADJUDICATION.

Gate (regress/gate_sh_rounding.sh at HEAD; the working copy holds three UNRELATED 09-17 hunks at old :530/:590/:822 that must not
ride -- stage from a HEAD-based copy, #548 recipe):
    :64  check "vector-mode pairs run" "$want" 36      -> 52  (54 is wrong: 8 rows x 2 modes = 16; +1 = 53 if the NODN row is adopted)
    :72  "vectors that discriminate the two modes" 9   -> 9 (unchanged: every new row wants the same value in both modes)
    :78  for v in ... add "fcnvsd fpul 1.5" "fcnvsd fpul -1.5" "fcnvsd fpul 0.1" "fcnvsd fpul -0" "fcnvsd fpul inf"
         "fcnvsd fpul nan" "fcnvsd dr hi" "fcnvsd dr lo"   (each checked for count 2; a NODN row is count 1 and needs its own check)

## 3. PRETABLE.out (mandatory, written BEFORE table 1 runs; its mtime proves the order) -- content
* SIBLING PARITY: sibling X(fcnvds_drm_fpul) writes FPUL by design (manual 9.28 :10759); the witness's `fcnvds ctl` row pins that
  channel live; no asymmetry owed beyond the control.
* CLAIM -> ROW: the added comment claims "reads FPUL and writes DRn only" -> the six FPUL rows (reads) and the two DRn rows (writes).
* GUARD FIELD vs BODY FIELD: the only dominating predicate is FLOATING_POINT_AVAILABLE_CHECK (sr.FD); body reads fpul, writes
  fr[r8], fr[r8+1]; no field the predicate reads differs from one the body reads, so no disagreeing-state row is owed.  Partition the
  body induces: none (the body tests nothing).  Clause (d) for a pure deletion = the removed store re-introduced under a DIFFERENT
  predicate (M_f, M_g below); DN and the destination index are not fields the fix depends on, so those legs are clause-(e)
  disclosure unless the adjudication adopts the NODN row.
* CHANNEL per row: fpul rows kill M_b/M_f(when DN clear)/M_h and observe the FPUL readback word; dr hi/lo kill M_c (identity) and
  M_i (swapped halves) and observe the DRn halves; `-0` kills a store-zero-on-zero form; `inf`/`nan` kill a specials-only form.

## 4. Kill table (scratch clones only; /tmp/gxdivw = HEAD base already built; a fixed clone built beside it; sentinel discipline)
    base (HEAD)     expect the six FPUL rows RED (3 measured in the witness), DRn rows green            -- clause (a)
    fixed           expect 52/52 (or 53/53)                                                             -- the detector's green
    M_b  reinstate line 3057 verbatim                                                                   -- clause (b): FPUL rows red
    M_c  identity body: decode and retire, write nothing (the handler's body replaced by the FD check only) -- clause (c): dr hi/lo red
    M_f  reinstate under `if (!(cpu->cd.sh.fpscr & SH_FPSCR_DN))`                                       -- (d) form f: green unless the NODN row exists
    M_g  reinstate under `if (ic->arg[0] != (size_t)&cpu->cd.sh.fr[0])`                                 -- (d) form g: FPUL rows red (DR2 is used)
    M_h  after the store: `cpu->cd.sh.fpul = (uint32_t) ieee;`                                          -- the low half: `fpul 0.1` red (0xa0000000)
    M_i  the two reg() stores exchanged                                                                  -- `dr lo`/`dr hi` red
    M_z  `if (op1.f == 0.0) cpu->cd.sh.fpul = 0;`                                                       -- `fpul -0` red
  Record each score with its artifact path under regress/artifacts/shfcnvsdfpul/killtable_20261102/; the (c) line in the form
  "(c): measured at <path>".

## 5. Records
* CHANGELOG round block #576; OUTSTANDING_BUGS.md entry update (filed -> fixed, with the #297 wording correction); ledger row
  `shfcnvsdfpul` -> closed with witness `probe:regress/artifacts/shfcnvsdfpul/witness_20261102/sh_fcnvsd_witness.py` and detector
  rows named; matrix.html regenerated; scoping note correction.
* Pass-2 packet: the real diff + the full handler after the edit + the detector diff + PRETABLE.out + the kill-table scores, to the
  same five seats; then the §F2 adjudication pass (Fable + Astra adjudicate; all five share findings).
