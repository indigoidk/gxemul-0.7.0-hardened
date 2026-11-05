# STAGED_DIFFS_memc213.md -- what the mvme187memcoob landing commits for each shared file, against HEAD and the working copy

HEAD edb3213f.  Round number #581 (derived: max round heading in HEAD's CHANGELOG.md (#580) + 1).  Built by the landing kit's build_staged_memc.py from `git show HEAD:<path>`, the working copy and `regress/artifacts/mvme187memcoob/r7_20261105/gate_memc_block.new`, at 2026-11-05 10:28 local.

## src/devices/dev_mvme187.c (staged == the working copy, byte for byte; no tree swap)

HEAD 4664 bytes md5 ebf853425a584a7a68aac850f36690ad; working copy = staged 6920 bytes md5 97e983872a72d159fbaaf54d8694ba49, the md5 table 5 measured (`regress/artifacts/mvme187memcoob/r5_20261105/table5/MD5.txt`) and the one repair 6 names as unchanged (`regress/artifacts/mvme187memcoob/r7_20261105/IMPL_NOTE.md`).

HEAD's `struct mvme187_data` spans lines 47-49 and `DEVICE_ACCESS(mvme187_memc)` lines 52-97; every hunk lies inside one of them:

* HEAD line 49: 0 line(s) -> 7 line(s), inside struct mvme187_data
* HEAD line 57: 1 line(s) -> 4 line(s), inside DEVICE_ACCESS(mvme187_memc)
* HEAD line 68: 2 line(s) -> 15 line(s), inside DEVICE_ACCESS(mvme187_memc)
* HEAD line 72: 2 line(s) -> 6 line(s), inside DEVICE_ACCESS(mvme187_memc)
* HEAD line 77: 0 line(s) -> 1 line(s), inside DEVICE_ACCESS(mvme187_memc)
* HEAD line 78: 3 line(s) -> 12 line(s), inside DEVICE_ACCESS(mvme187_memc)
* HEAD line 84: 7 line(s) -> 17 line(s), inside DEVICE_ACCESS(mvme187_memc)

### working copy (= staged) vs HEAD: the commit's whole change to this file

7 hunk(s):

```
@@ insert  HEAD-side line 49 (0 lines) -> other side line 49 (7 lines)
+     /*  mvme187memcoob: once-per-device announce latches.
+         DEVINIT memsets this struct, so they start at 0.  Keep
+         them directly after memcreg: regress/mvme187_memc_probe.py
+         detects a return of the old indexed read by reading these
+         bytes back at +0x7c (rows R3 and R8).  */
+     int            warned_memconf;
+     int            warned_default;
@@ replace  HEAD-side line 57 (1 lines) -> other side line 64 (4 lines)
-     // TODO: not used yet
+     /*  Controller 1 (offsets 0x100-0x1ff) presents the same
+         register image as controller 0: DEVINIT derives one size
+         code from RAM/2 for both, and the model keeps one image.
+         The number is reported in the notices below.  */
@@ replace  HEAD-side line 68 (2 lines) -> other side line 78 (15 lines)
-     odata = ((uint8_t*)&d->memcreg)[relative_addr];
- 
+     /*  mvme187memcoob: struct memcreg is 124 bytes, but after the
+         fold relative_addr is 0..0xff.  The old code indexed the
+         struct with it before the switch for every access: for
+         0x7c..0xff an out-of-bounds read in the C source, whose
+         value the exiting default arm never used, so the compiler
+         could omit it (no AddressSanitizer report on the old build
+         at -O3).  Once the exit was removed it forwarded whatever
+         byte sits at that offset in the device struct: at
+         +0x7c..+0x83 the two announce latches, and beyond the
+         struct's end, memory outside the allocation (measured on an
+         x86_64 host with the indexed read reinstated: after a
+         memconf store, a load of +0x7c returns 0x1, the first byte
+         of warned_memconf).  No indexed read remains: the three
+         served arms read their own fields and the default arm
+         reads none.  */
@@ replace  HEAD-side line 72 (2 lines) -> other side line 95 (6 lines)
-     case 0x00:    /* chipid */
-     case 0x04:    /* chiprev */
+     case 0x00:    /*  chipid  */
+         odata = d->memcreg.memc_chipid;
+         break;
+ 
+     case 0x04:    /*  chiprev  */
+         odata = d->memcreg.memc_chiprev;
@@ insert  HEAD-side line 77 (0 lines) -> other side line 104 (1 lines)
+         odata = d->memcreg.memc_memconf;
@@ replace  HEAD-side line 78 (3 lines) -> other side line 106 (12 lines)
-             fatal("mvme187_memc: Write to relative_addr %i (controller %i) not yet"
-                 " implemented!\n", (int)relative_addr, controller);
-             exit(1);
+             /*  Bits 0-2 hold the size code that DEVINIT fixes
+                 from the configured RAM; no other bit of this
+                 register is modelled, so a store has nothing to
+                 change and is not kept: the register keeps the
+                 value DEVINIT gave it.  Announced once per
+                 device; it used to end the emulator.  */
+             if (!d->warned_memconf) {
+                 fatal("[ mvme187_memc: memconf write 0x%x"
+                     " (controller %i) ignored, not modelled"
+                     " (once) ]\n", (int)idata, controller);
+                 d->warned_memconf = 1;
+             }
@@ replace  HEAD-side line 84 (7 lines) -> other side line 121 (17 lines)
-     default:fatal("[ mvme187_memc: unimplemented %s offset 0x%x",
-             writeflag == MEM_WRITE? "write to" : "read from",
-             (int) relative_addr);
-         if (writeflag == MEM_WRITE)
-             fatal(": 0x%x", (int)idata);
-         fatal(" ]\n");
-         exit(1);
+     default:
+         /*  No register is modelled at this offset.  A read
+             returns 0, which is also the value DEVINIT leaves in
+             every byte of the image other than chipid, chiprev
+             and memconf; a write is not kept.  Announced once
+             per device; it used to end the emulator.  */
+         if (!d->warned_default) {
+             fatal("[ mvme187_memc: unimplemented %s offset 0x%x"
+                 " (controller %i)", writeflag == MEM_WRITE ?
+                 "write to" : "read from", (int)relative_addr,
+                 controller);
+             if (writeflag == MEM_WRITE)
+                 fatal(": 0x%x", (int)idata);
+             fatal(" (once) ]\n");
+             d->warned_default = 1;
+         }
+         break;
```

### the four trees (landing_20261105/TREES_memc.txt)

```
est                                      part 1 PASS: cmp == the SEC working copy; part 2 N/A (source tree, no binary); .MUTANT absent
build                                    part 1 PASS: cmp == the SEC working copy; part 2 PASS: binary newer (gxemul 2026-11-05 10:03:39, source 2026-11-04 18:58:36); .MUTANT absent
build-asan                               part 1 PASS: cmp == the SEC working copy; part 2 PASS: binary newer (gxemul 2026-11-05 10:04:13, source 2026-11-04 18:59:12); .MUTANT absent
//wsl.localhost/Gentoo/tmp/gxsec-build   part 1 PASS: cmp == the SEC working copy; part 2 PASS: binary newer (gxemul 2026-11-05 10:04:20, source 2026-11-04 19:01:29); .MUTANT absent
```

## regress/gate_arm.sh

HEAD 155139 bytes md5 ce5da7331a993a3d92162255a57af751; staged 160898 bytes md5 cbb9d843cffdcdd903a5a5310e706416; working copy 166210 bytes md5 79474569408581ff6eba5fda5bdb7125 (READ only).  The staged block is `regress/artifacts/mvme187memcoob/r7_20261105/gate_memc_block.new` (md5 879188828478233735072f2b14a68c5b, 36 lines, pin 213) with its header's `(#NNN)` set to `(#581)`; the working copy's own memc block (33 lines, pin 206) is NOT used.  `bash -n` is run by the pretest.

### staged vs HEAD (the commit's whole diff of this file: repair 6's memc block plus two blank lines, after the #570 block)

1 hunk(s):

```
@@ insert  HEAD-side line 2063 (0 lines) -> other side line 2063 (38 lines)
+ #  ------------------------------------------------------------ mvme187memcoob (#581)
+ #  dev_mvme187.c's memory controller ended the emulator (fatal() + exit(1)) on a memconf store and on any unnamed offset, and indexed
+ #  its 124-byte register struct with the folded offset before the switch.  Now each served offset reads its own field, controller 1
+ #  folds onto the same image, a memconf store and any other offset's access are not kept, and each category is announced once per
+ #  device.  The rung-3 witness (regress/artifacts/mvme187memcoob/witness_20261104/) is NOT run here; this is its detector: 213 rows,
+ #  the witness's 21 plus sixteen multi-access sessions -- R3 to R18: several accesses in one emulator lifetime, one
+ #  register per load (the latch rows, and R8's twelve bytes past memcreg).  A source check beside it: no `memcreg)[' and no
+ #  `[relative_addr]' may appear in dev_mvme187.c, the layout-free guard against the old indexed read in its old spelling (R8
+ #  covers it at run time only while the latches sit just after memcreg).  Needs only the binary: mvme187 -M 64 with a 4-byte
+ #  dummy image at 0x10000.
+ #  Test-variant tables: regress/artifacts/mvme187memcoob/det_20261104/table1/ (the then 56-row probe), table2/ (the 74-row probe),
+ #  r3_20261105/table3/ (the 118-row probe), r4_20261105/table4/ (the 148-row probe), r5_20261105/table5/ (the 206-row probe: 3,575
+ #  variants, 665 green) and r7_20261105/table6/ (this probe, the record: the legs and table 5's 665 green variants re-run; the
+ #  probe's header carries the counts, the CONTRACT and the disclosures); sanitizer legs: .../det_20261104/asan/ (offline evidence;
+ #  MVME187_MEMC_ASAN is informational and not checked here).
+ #  Like #568's and #570's blocks above, it runs only if none of this gate's earlier skip points fired.
+ MEMCLOG=$LOGDIR/mvme187_memc.log
+ python3 -u mvme187_memc_probe.py "$PMAX" gate > "$MEMCLOG" 2>&1 || true
+ if ! grep -q "MVME187_MEMC_PROBE_DONE" "$MEMCLOG"; then
+     check "mvme187 memc probe completed" "no" "yes"
+ else
+     check "mvme187 memc probe completed" "yes" "yes"
+     check "mvme187 memc sentinel once" "$(grep -c '^MVME187_MEMC_PROBE_DONE$' "$MEMCLOG")" "1"
+     mcres=$(sed -n 's/^MVME187_MEMC_RESULT=//p' "$MEMCLOG")
+     check "mvme187_memc rows run"     "${mcres#*/}" 213
+     check "mvme187_memc rows correct" "${mcres%/*}" "213"
+     check "mvme187 memc controls" "$(grep -c '^MVME187_MEMC_CONTROL=OK$' "$MEMCLOG")" "1"
+     check "mvme187 memc symptom absent" "$(grep -c '^MVME187_MEMC_SYMPTOM=ABSENT$' "$MEMCLOG")" "1"
+     for v in "neg apparatus" "ctl chipid sess" "ctl chipid r2" "ctl chipid pc" "ctl chiprev sess" "ctl chiprev r2" "ctl chiprev pc" "ctl memconf sess" "ctl memconf r2" "ctl memconf pc" "ctl ctl1id sess" "ctl ctl1id r2" "ctl ctl1id pc" "rd 0x0c session" "rd 0x0c prompt" "rd 0x7c session" "rd 0x7c prompt" "rd 0xff session" "rd 0xff prompt" "wr cnf session" "wr cnf prompt" "R3 session" "R3 cnf r2" "R3 7c r4" "R3 108 r9" "R3 cnf0 r11" "R3 00 r12" "R3 04 r13" "R3 pc" "R3 lines" "R3 cnf line" "R3 7c line" "R3 no 0x5" "R3 no 0x0" "R4 session" "R4 00 r7" "R4 04 r8" "R4 0c" "R4 7c" "R4 ff" "R4 10c" "R4 pc" "R4 lines" "R4 line text" "R5 session" "R5 r2" "R5 00 r7" "R5 04 r8" "R5 08 r9" "R5 08b r11" "R5 pc" "R5 lines" "R5 line text" "R5 cnf line" "R6 session" "R6 00" "R6 04" "R6 08" "R6 100" "R6 104" "R6 108" "R6 pc" "R6 lines" "R7 session" "R7 r2" "R7 108 r4" "R7 10c r6" "R7 108b r7" "R7 pc" "R7 lines" "R7 line text" "R7 cnf line" "R8 session" "R8 7c r4" "R8 7d r5" "R8 7e r6" "R8 7f r7" "R8 80 r8" "R8 81 r9" "R8 82 r10" "R8 83 r11" "R8 84 r12" "R8 85 r13" "R8 86 r14" "R8 87 r15" "R8 pc" "R8 lines" "R9 session" "R9 108 r2" "R9 08 r4" "R9 00 r6" "R9 04 r7" "R9 10c r8" "R9 08b r9" "R9 lines" "R9 no wide" "R9 cnf line" "R9 def line" "R9 pc" "R10 session" "R10 118 r6" "R10 18 r7" "R10 08 r8" "R10 00 r9" "R10 04 r10" "R10 lines" "R10 line text" "R10 pc" "R11 session" "R11 180 r4" "R11 01 r5" "R11 0a r6" "R11 101 r7" "R11 102 r8" "R11 120 r9" "R11 140 r10" "R11 20 r11" "R11 40 r12" "R11 line text" "R11 lines" "R11 pc" "R12 session" "R12 cnf line" "R12 00 r2" "R12 04 r4" "R12 m08 r13" "R12 100 r10" "R12 104 r11" "R12 w00 r6" "R12 h08 r7" "R12 08 r8" "R12 0c r12" "R12 0cb r14" "R12 08b r15" "R12 0c line" "R12 lines" "R12 pc" "R13 session" "R13 line text" "R13 00 r2" "R13 04 r4" "R13 08 r6" "R13 08b r8" "R13 10c r9" "R13 cnf line" "R13 lines" "R13 pc" "R14 session" "R14 line text" "R14 00 r2" "R14 04 r4" "R14 08 r5" "R14 0c r6" "R14 lines" "R14 pc" "R15 session" "R15 00 r2" "R15 04 r4" "R15 08 r7" "R15 cnf line" "R15 def line" "R15 lines" "R15 pc" "R16 session" "R16 cnf line" "R16 def line" "R16 lines" "R16 100 r2" "R16 00 r4" "R16 104 r7" "R16 04 r8" "R16 08 r10" "R16 108 r11" "R16 100b r12" "R16 00b r13" "R16 104b r14" "R16 04b r15" "R16 08b r16" "R16 108b r17" "R16 100c r18" "R16 00c r19" "R16 104c r20" "R16 04c r21" "R16 08c r22" "R16 108c r23" "R16 83 r24" "R16 10c r25" "R16 1c r26" "R16 08d r27" "R16 pc" "R17 session" "R17 def line" "R17 cnf line" "R17 lines" "R17 f3 r2" "R17 10c r4" "R17 100 r7" "R17 00 r8" "R17 104 r10" "R17 04 r11" "R17 08 r12" "R17 108 r13" "R17 7c r14" "R17 7d r15" "R17 08b r16" "R17 pc" "R18 session" "R18 18 r2" "R18 08 r4" "R18 pc" "R18 lines" "R18 def line" "R18 cnf line"; do
+         check "mvme187 memc row: $v" "$(count "$MEMCLOG" "^$v  .*ok$")" "1"
+     done
+     check "mvme187 memc rows emitted" "$(( $(count "$MEMCLOG" " ok$") + $(count "$MEMCLOG" " FAIL$") ))" "213"
+     check "mvme187 memc rows green"   "$(count "$MEMCLOG" " ok$")"   "213"
+     check "mvme187 memc rows red"     "$(count "$MEMCLOG" " FAIL$")" "0"
+ fi
+ check "mvme187 memc no indexed read" "$(grep -cE 'memcreg\)[[:space:]]*\[|\[relative_addr\]' ../src/devices/dev_mvme187.c)" "0"
+ 
+ 
```

### staged vs the working copy

11 hunk(s): 7 inside the memc block's range (repair 6's 213-row block against the working copy's 206-row block, which the working tree has not taken yet), and:

* not this round's: working-copy replace at its line 1083 (1 -> 1 lines; grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-)
* not this round's: working-copy replace at its line 1126 (3 -> 4 lines; #  stand in for a missing id -- pass 2), and the probe's own total by )
* not this round's: working-copy insert at its line 1166 (0 -> 22 lines; #  #NNN fbsdrampair: a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_B)
* not this round's: working-copy insert at its line 2119 (0 -> 31 lines; )

## regress/mvme187_memc_probe.py (new file; only this round's)

Staged = the working copy with 4 docstring hunk(s).  landing_20261105/PROBE_IDENTITY_memc213.md: tree minus docstring equal: True; string-normalised tree equal to table 6's frozen instrument: True.

### staged vs the working copy

4 hunk(s):

```
@@ replace  HEAD-side line 8 (1 lines) -> other side line 8 (1 lines)
- THE FIX (#NNN).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
+ THE FIX (#581).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
@@ replace  HEAD-side line 46 (1 lines) -> other side line 46 (1 lines)
- L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D and L_DT_D_idat_W.D: 206/206 each in table 5 (r5_20261105/table5/
+ L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D and L_DT_D_idat_W.D: 206 of 206 each in table 5 (r5_20261105/table5/
@@ replace  HEAD-side line 81 (1 lines) -> other side line 81 (1 lines)
- L_ME_M_idat_nC 201/206 against :2999 L_ME_M_idat_W.nC 206/206) -- whose clearing stores -- the 0x00 controller-0 stores of R3, R7,
+ L_ME_M_idat_nC 201 of 206 against :2999 L_ME_M_idat_W.nC 206 of 206) -- whose clearing stores -- the 0x00 controller-0 stores of R3, R7,
@@ replace  HEAD-side line 115 (1 lines) -> other side line 115 (1 lines)
- table-4 variant red again; 3,518 variants PRED=match, 56 PRED=atleast-ok, one PRED=MISS (D7_fold, detected 175/206: a stale
+ table-4 variant red again; 3,518 variants PRED=match, 56 PRED=atleast-ok, one PRED=MISS (D7_fold, detected 175 of 206: a stale
```

## tools/precommit_check.sh

HEAD md5 81d10dfc8e952cbedc8412d6dc3afd9b (SCORE_CLAIMS_MANIFEST=46); staged md5 538bb143d2b108f10d550bfba2c85076 (=47).  Written fresh against HEAD: the working copy's raises -- qhslowifetch, mvme187memcoob (naming a stale 74-row pin), pvrrenderexit -- are not carried.

### staged vs HEAD

1 hunk(s):

```
@@ replace  HEAD-side line 376 (1 lines) -> other side line 376 (3 lines)
-     SCORE_CLAIMS_MANIFEST=46
+     #  RAISED 46 -> 47 ON 2026-11-05, DELIBERATELY.  One newly gated probe: mvme187_memc_probe.py
+     #  (#581 mvme187memcoob, pinned UNQUOTED in gate_arm.sh at 213 rows under the stem mvme187_memc; its docstring is checked).
+     SCORE_CLAIMS_MANIFEST=47
```
