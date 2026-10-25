# Reading task: T18 lecsrmask #573 T18F2B_B (Gemini web; 2026-10-25)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-T18F2B_B-ae25` on a line of its own.

# T18 / `lecsrmask` (#573) -- F2b: THE ADJUDICATION PASS OF PASS 2 (the diff review's shared findings)

**Please do not simply ratify.** This packet consolidates every finding of the six pass-2 answers (GPT-6 Astra, Grok 4.7, GLM 5.3 x2, DeepSeek x2) with the main loop's DISPOSITION of each, then lists the DISAGREEMENTS with both sides in their own words. The load-bearing question is **"WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?"** -- of the 44 findings below, 33 are ACCEPTED (applied or planned), 9 are CONFIRMED or SETTLED by a check, 1 is NOT ADOPTED (F37) and 1 is a correction of this round's own premise (F39). A round that accepted nearly everything has either had a very good panel or has stopped arguing; only a seat can tell which. Check the premises in section 0, not just the derivations.

**The tree under review is `GXEMUL-SEC/src/` at HEAD `2956c32d`; ignore any other `src/` you find** (the project root carries a pristine 2021 upstream copy). The edit exists ONLY in scratch copies: the diff below is regenerated from HEAD's `src/devices/dev_le.c` with the corrected patch. Reading scope for file-reading seats: `regress/artifacts/lecsrmask/pass2_20261025/` (the six answers), `regress/artifacts/lecsrmask/pass1_20261025/final_045716/` (the banked legs), `regress/artifacts/lecsrmask/killtable_20261025/PRETABLE.out`, `regress/artifacts/lecsrmask/pass1_20261025/PASS1_RULINGS.md`, `src/devices/dev_le.c`, `regress/lib.sh` (`count()` at :326), `tools/pipeline/check_score_claims.py`, `tools/pipeline/check_stage_panels.py`, `tools/pipeline/check_commit_attribution.py`. Packet-fed seats cannot read files: everything a question depends on is inlined; name any premise you cannot settle from the packet as NOT CHECKABLE rather than guessing. Do not build or run anything; do not propose reproduction recipes.

## 0. Settled premises (re-inlined per packet; each with its warrant)

* **The ruled design (pass-1 F2, PASS1_RULINGS.md):** CSR3-only narrowing, form A -- an explicit `case 3:` storing `x & 0x0007`; `default:` keeps CSR1 and CSR2 stored whole as the model's retained behaviour (an interpreted reading, filed as `lecsr12readback`); the two STOP comments corrected as L4 records; D2 overturned (the selector labels are the floor, kept/dropped bits are clause-(e) contract coverage); D3 refined (same file, not same function); D4 refined (`csr3 hi` owed, now a row).
* **HEAD and the measured base.** HEAD is `2956c32d`. The base clone is a git-archive export of `0b09e7b6`; `git diff --stat 0b09e7b6 2956c32d` touches exactly `CHANGELOG.md` and `regress/gate_hygiene.sh` (nothing under `src/`), so the base binary's product tree IS HEAD's. `src/devices/dev_le.c` md5 `3eab9c96d4823113941271ad415daf5d` at HEAD, in the working tree and in the clone (RUN_IDENTITY below).
* **Single call path (grep of `src/devices/dev_le.c` at HEAD):** `le_register_write(d, d->reg_select, idata);` at :1002 is the only call; `d->reg_select = idata & (N_REGISTERS - 1);` at :1015 is the only writer of `reg_select`; `N_REGISTERS` is 4, so `r` reaches the switch as 0..3 and `default:` serves exactly 1 and 2 after the patch. `le_chip_init` (:179-182) consumes `(d->reg[1] & 0xffff)` and `((d->reg[2] & 0xff) << 16)`; `SRAM_SIZE` is 128*1024, so bit 0 of `reg[1]` survives into `init_block_addr`. No other reader of `reg[3]` exists (`grep -n 'reg\[3\]'` matches nothing; the indexed RDP read `odata = d->reg[d->reg_select]` is the one reader).
* **The manuals, by line (`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/lance/`):** TM1986.txt:1734 CSR3 bits 15:03 "Reserved and read as 0" (page footer 1-22); :1695 `15:08 RES Reserved.` (CSR2); :1745-1749 CSR1 bit `00` ... `Must be zero.`; :1511-1516 "Because setting the stop bit clears CSR3, this register must be reprogrammed unless default values are used for BCON, ACON, and BSWP. CSR1 and CSR2 must be reloaded when the STOP bit is set."; :2853-2857 "CSR1 and CSR2 are normally not affected when the Stop bit is set in CSR0. (When the Stop bit is set, CSR3 is cleared and CSR0 is set to 0004 Hex, Stop bit set.) However, it is recommended to reload CSR1 and CSR2 whenever the Stop bit is set." am79c90_bitsavers.txt:1123-1126 (CSR1) and :1146-1149 (CSR2) "READ/WRITE: Accessible only when the STOP bit of CSR0 is a ONE ... The C-LANCE preserves the contents of CSR1/CSR2 after STOP."; :1222-1226 CSR3 reserved "Read as zeroes. Write as zeroes."; :1161-1163 CSR2 reserved bits read as zero; :1138-1142 CSR1 bit 0 "Must be zero"; :3411 Table B-1 `b) CSR1 and CSR2 contents are preserved` (LEFT column, the Am79C90) versus `b) CSR1 and CSR2 are not preserved when` (RIGHT column, the Am7990); :3686-3687 "Preservation of CSR1 and CSR2: The LANCE device does not preserve the contents of CSR1 and CSR2".
* **The row kinds, from the probe's `build_rows()` (code, not prose):** control = `ram:csr0/csr3/csr2/csr1`, `csr0 reset`, `rap mask`, `csr3 bits`, `csr2 lo`, `csr1 even`, `csr1 top`, `stable:csr0/csr3/csr2/csr1` (14 rows); symptom = `csr3 all`, `csr3 hi`, `csr3 mix` (3); contract = `csr2 all`, `csr1 all`, `csr1 odd` (3). `run_leg()`: a red row of ANY kind counts in the leg's failures; only `kind == "control"` (plus a bad word encoding or a breakpoint pc that is not the halt address) fails CONTROL. So a red SYMPTOM or CONTRACT row fails the leg but never CONTROL; a red kept-bits or stable row fails BOTH.
* **The vacuity floor, stated plainly (the pass-2 brief's sentence was ambiguous -- F38):** a detector is above the floor when it REDS on each of (a) the pre-fix build, (b) a verbatim reinstatement of the removed defect at every fixed site, (c) a null medium. **Clause (d), the null-repair red (DEPENDS-ON, bounded to the enclosing function), IS a floor clause in the carrier ("IT IS A FLOOR CLAUSE, so a breach is L2")** -- the pass-2 brief called it "separate", which understated it (F39). Here (d) is UNMEASURED and recorded as OWED under the owner's post-classifier-stop rule (the #567 "land with filed debt" precedent); the record claims no (d) measurement and no (d) breach. (e) is the contract in the header.
* **The banked measurement set** (`regress/artifacts/lecsrmask/pass1_20261025/final_045716/`, RUN_IDENTITY verbatim):

```
final_045716 -- the FINAL detector revision's legs (lecsrmask #573), 2026-10-25 05:09:21
probe       le_csrmask_probe.frozen.py.txt  md5 6259ce546ddb88fbd1c27be5d091348d  538 lines
base        /tmp/gxt17/base/gxemul md5 6c27af7b04742d72385426e304633c99 (git-archive export of HEAD 0b09e7b6; dev_le.c md5 3eab9c96d4823113941271ad415daf5d)
fix         /tmp/gxt18/fix/gxemul  md5 a82cd71fdfd5b3f20bdd9afe5131c21c (base + patch_formA; dev_le.c md5 29e9c2c3773d9af1f7443d5153fc58c9, binary newer than source: yes)
HEAD column base, witness mode:        LE_CSRMASK_CONTROL_base=OK LE_CSRMASK_RESULT_base=20/20 
L0 pre-fix GATE (FIX column):          LE_CSRMASK_CONTROL=OK LE_CSRMASK_RESULT=17/20 
L3 null medium /bin/false GATE:        LE_CSRMASK_CONTROL=FAIL LE_CSRMASK_RESULT=0/20 
L1 fix GATE (FIX column):              LE_CSRMASK_CONTROL=OK LE_CSRMASK_RESULT=20/20 
L2 two legs base/HEAD + fix/FIX:       LE_CSRMASK_CONTROL_base=OK LE_CSRMASK_RESULT_base=20/20  LE_CSRMASK_CONTROL_fix=OK LE_CSRMASK_RESULT_fix=20/20 
run dirs    /tmp/gxt18/det20_045716  /tmp/gxt18/fixlegs_050651
(c): measured at regress/artifacts/lecsrmask/pass1_20261025/final_045716/RESULTS_L3_nullmedium.txt
```

  The red rows on L0 are exactly `csr3 all` (got 0xffff, fix want 0x0007), `csr3 hi` (0x0008 -> 0x0000), `csr3 mix` (0x0015 -> 0x0005); L1 reads 0x0007 / 0x0000 / 0x0005. L3 prints every capture as `??`, CONTROL=FAIL, `LEG gate VERDICT: FAIL`.
* **The 17-row witness** (`regress/artifacts/lecsrmask/witness_20261025/`, RUN_IDENTITY verbatim):

```
RUN_IDENTITY -- T18 lecsrmask WITNESS (rung 3: guest instructions on the UNMODIFIED pmax -e 3100, before any product edit)
run dir        /tmp/gxt18/witness_034758   (2026-10-25 03:49:18)
binary         /tmp/gxt17/base/gxemul  md5 6c27af7b04742d72385426e304633c99  built 2026-10-25 03:47:49.519713686
sources        a git-archive export of HEAD 0b09e7b6 (top-level files, src, experiments, man, doc, demos, test), ./configure && make -j4 in WSL Gentoo
dev_le.c       md5 3eab9c96d4823113941271ad415daf5d  (the default-arm store 'd->reg[r] = x;' present x1)
probe          le_csrmask_probe.frozen.py.txt  md5 df5ab57408d1db812d66bb0b42564fb0  482 lines (kept as .py.txt until the landing's MANIFEST entry names it)
result         LE_CSRMASK_RESULT_base=17/17  LE_CSRMASK_CONTROL_base=OK
```

* **The probe revision this packet inlines is COMMENT-ONLY different from the measured one.** Since pass 2 the docstring and one code comment were corrected (F8-F12 below); the code is AST-identical to the frozen `6259ce54` revision (checked with Python's `ast` module, module docstring excluded). **It will be re-frozen and EVERY leg re-measured in the final cycle before landing** (the fix clone is also rebuilt from the corrected comment-only patch), so the landed md5 and the landed `final_<stamp>` are those of that cycle, not `6259ce54` / `final_045716`. Nothing below cites a number from the final cycle.

## 1. The diff as it now stands (regenerated from HEAD with the corrected patch; two hunks, 28 added, 9 removed; LF)

```diff
--- src/devices/dev_le.c (HEAD 2956c32d)
+++ src/devices/dev_le.c (patched; the scratch copy dev_le.c.dry)
@@ -881,8 +881,25 @@
 		d->reg[r] |= (x & LE_INEA);
 		break;
 
+	case 3:
+		/*
+		 *  #573: CSR3 is BSWP|ACON|BCON; bits 15:3 are "Reserved and read
+		 *  as 0" (Am7990 Technical Manual, 1986, p. 1-22; the Am79C90
+		 *  datasheet says the same).
+		 */
+		d->reg[r] = x & 0x0007;
+		break;
+
 	default:
-		/*  CSR1, CSR2, and CSR3:  */
+		/*
+		 *  This model stores CSR1 and CSR2 whole.  The Am7990 manual leaves
+		 *  their read-back unspecified (CSR1 bit 0 "Must be zero", CSR2 bits
+		 *  15:8 "Reserved" -- constraints on the host's writes); the later
+		 *  Am79C90 (C-LANCE) reads CSR2's reserved bits as zero and says only
+		 *  "Must be zero" for CSR1 bit 0; another emulator keeps both writable
+		 *  on the Am7990 for a board diagnostic's sake.  An interpreted
+		 *  reading, recorded as one: see the #573 record.
+		 */
 		d->reg[r] = x;
 	}
 }
@@ -984,20 +1001,23 @@
 			    "%02x", d->reg_select, (int)odata);
 
 			/*
-			 *  A read from csr1..3 should return "undefined"
-			 *  result if the stop bit is set.  However, Ultrix
-			 *  seems to do just that, so let's _not_ print
-			 *  a warning here.
+			 *  #573: CSR1..3 are accessible only while the STOP bit
+			 *  is SET (a read with STOP clear is "undefined" on the
+			 *  chip).  The old comment reported that Ultrix seems to
+			 *  read them with STOP set -- the in-spec case.  The model
+			 *  answers in either state; gating on STOP is filed, not
+			 *  implemented, and nothing is announced either way.
 			 */
 		} else {
 			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 			    "WRITE to register 0x%02x: 0x%02x",
 			    d->reg_select, (int)idata);
 			/*
-			 *  A write to from csr1..3 when the stop bit is
-			 *  set should be ignored. However, Ultrix writes
-			 *  even if the stop bit is set, so let's _not_
-			 *  print a warning about it.
+			 *  #573: a write to CSR1..3 with STOP CLEAR is the one
+			 *  the chip ignores; writes with STOP set are the normal
+			 *  case (the old comment reported Ultrix writing them with
+			 *  STOP set).  The model accepts both -- gating on STOP is
+			 *  filed, not implemented.
 			 */
 			le_register_write(d, d->reg_select, idata);
 		}
```

## 2. The probe header as it now stands (verbatim; the ROWS table, CONTRACT, USAGE)

```
le_csrmask_probe.py -- rung-3 WITNESS and DETECTOR for ledger row `lecsrmask` (devices/dev_le.c):
until #573 the LANCE model (the Am7990, as used in DECstations) stored all sixteen bits a guest wrote
to CSR3, where the chip implements only BSWP|ACON|BCON and reads bits 15:3 as zero; #573 masks that
store to 0x0007.  CSR1 and CSR2 are stored whole BY DESIGN (see THE EVIDENCE) and this probe pins
that too.

SITES (src/devices/dev_le.c; grep anchors):
  * `le_register_write():` -- `case 0:` handles CSR0 bit by bit; before #573 one `default:` arm
    (`/*  CSR1, CSR2, and CSR3:  */`) stored the whole value for r = 1..3: `d->reg[r] = x;`
    (uint16_t reg[N_REGISTERS], N_REGISTERS 4).  #573 adds `case 3:` storing `x & 0x0007` and leaves
    `default:` (now CSR1 and CSR2 only) storing the whole value.
  * `DEVICE_ACCESS(le)` -- `case 0:` RDP (read: d->reg[d->reg_select]; write: le_register_write),
    `case 4:` RAP (read: reg_select; write: `idata & (N_REGISTERS - 1)`, so RAP masks to 0..3).
  * `dev_le_init():` registers the register window at `baseaddr + 0x100000` with DM_DEFAULT (the
    debugger's `dump`/`put` do NOT reach it, so this probe drives it with GUEST instructions) and
    sets `d->reg[0] = LE_STOP` (0x0004) at reset.
  * src/machines/machine_pmax.c, the MACHINE_DEC_PMAX_3100 arm: `dev_le_init(machine, mem,
    KN01_SYS_LANCE, ...)`, KN01_SYS_LANCE = 0x18000000 (src/include/thirdparty/dec_kn01.h), so on the
    UNMODIFIED `-E pmax -e 3100` machine RDP is KSEG1 0xb8100000 and RAP is 0xb8100004, 16-bit.

THE EVIDENCE (the design rests on it; sources on disk under C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/lance/):
  * CSR3: the Am7990 Technical Manual (AMD 1986), TM1986.txt line 1734, bits 15:03 "Reserved and
    read as 0", bits 2:0 BSWP/ACON/BCON; the Am79C90 (C-LANCE) datasheet, am79c90_bitsavers.txt
    1222-1226, "Reserved. Read as zeroes. Write as zeroes."  Mask 0x0007 -- SETTLED by both manuals.
  * CSR1 bit 0 and CSR2 bits 15:8: the Am7990 manual says only "Must be zero" (1749) and "Reserved."
    (1695) -- constraints on the host's WRITES, no read-back statement.  The C-LANCE datasheet reads
    CSR2's reserved bits as zero (1161-1163) but says only "Must be zero" for CSR1 bit 0 too
    (1138-1142): CSR1 bit 0's read-back is unspecified on BOTH chips, CSR2's only on the Am7990.
    MAME's am79c90.cpp stores CSR1 whole on both chips and CSR2 whole on the Am7990 (masked only on
    the Am79C90), its comment citing a MIPS RS2030 diagnostic that needs the bits writable and
    "assuming this is older device behaviour".  Upstream rpajarola e108b54 masks all three for a 3MIN
    port this fork does not carry, with no chip named.  So this model stores CSR1 and CSR2 whole --
    an interpreted reading, recorded as one -- and the rows below PIN that as a contract; a later
    per-chip model variant re-pins them under the oracle-correction order (research row
    regress/artifacts/research_20261022/A_github_forks.md row 26; the F2 adjudication of 2026-10-25).
  * (The witness revision of this docstring said "no LANCE datasheet is on disk" and the pass-1
    revision claimed CSR1 & 0xfffe / CSR2 & 0x00ff; both are corrected here.)

TEMPLATE: regress/wdc_lba_probe.py (#572) -- its pty session driver, prompt handling, MIPS encoders,
disassembler self-check (CONTROL 0: every emitted WORD checked against the emulator's own disassembly;
the mnemonic-rendering count printed beside it is informational), raw transcript per session and the
row/verdict/sentinel protocol are copied; its guest-code idioms are reduced to lui/ori/sh/lhu/beq.
Each session: write RAP, write RDP, read RDP (and RAP) back into capture registers, halt at a
breakpoint, read the registers with `print`.

ROWS (one fresh emulator per session; every CSR want is a literal; the stable rows want the value the
same session read first):
  row          session  stimulus                                  HEAD want     FIX want
  ram:<s>      every    sh/lhu round-trip of 0x5a5a via KSEG0 RAM  0x5a5a        0x5a5a
  csr0 reset   csr0     RAP = 0, read RDP                         0x0004        0x0004  (STOP at reset:
                                                                   a DEVICE SIGNATURE, RAM reads 0)
  rap mask     csr0     write 0x13 to RAP, read RAP               0x0003        0x0003  (masks to 0..3)
  csr3 all     csr3     RAP = 3, write 0xffff, read               0xffff        0x0007  SYMPTOM
  csr3 bits    csr3     RAP = 3, write 0x0005, read               0x0005        0x0005  (kept bits, bit 0 set)
  csr3 hi      csr3     RAP = 3, write 0x0008, read               0x0008        0x0000  SYMPTOM (the dropped
                                                                   boundary bit alone, bit 0 CLEAR)
  csr3 mix     csr3     RAP = 3, write 0x0015, read               0x0015        0x0005  SYMPTOM (kept bits 0,2 with
                                                                   a dropped bit 4: a saturating clamp and a mask
                                                                   conditioned on bit 3 both read it wrong)
  csr2 all     csr2     RAP = 2, write 0xffff, read               0xffff        0xffff  CONTRACT (stored whole)
  csr2 lo      csr2     RAP = 2, write 0x00a5, read               0x00a5        0x00a5
  csr1 all     csr1     RAP = 1, write 0xffff, read               0xffff        0xffff  CONTRACT (stored whole)
  csr1 odd     csr1     RAP = 1, write 0x1235, read               0x1235        0x1235  CONTRACT (bit 0 stored)
  csr1 even    csr1     RAP = 1, write 0x1236, read               0x1236        0x1236
  csr1 top     csr1     RAP = 1, write 0x8000, read               0x8000        0x8000  (top-edge insurance)
  stable:<s>   every    the first RDP value of the session read   == first      == first
                        again at once
The three SYMPTOM rows are red on the pre-fix build against the FIX column; every other row has the
same want in both columns.  CONTROL = every control-kind row (the four ram: rows, csr0 reset, rap mask,
the kept-bits rows csr3 bits / csr2 lo / csr1 even / csr1 top, and the four stable: rows) + every
session's word encodings + every halt breakpoint (pc verified), as in the template; a red SYMPTOM or
CONTRACT row fails the leg (the model changed) but does not by itself fail CONTROL.  SESSION ORDER IS LOAD-BEARING: each
of the CSR1, CSR2 and CSR3 sessions writes 0xffff first and the other values after it in one emulator, so a
store that accumulates with OR instead of assigning is caught by the later rows (csr3 bits / hi / mix read
0x0007 under it); in a fresh session starting from the reset value 0 it would not be.

CONTRACT (what this detector catches -- by construction from the rows' stimuli and wants; the variant
classifications are derived predictions, and the variant table's measurements are OWED, not made):
  CATCHES: any change to the CSR3 mask constant in its low 16 bits (csr3 all); a CSR3 store that ignores the written
    value (csr3 bits, csr3 hi, csr3 mix); a CSR3 mask conditioned on any single bit of the written
    value (csr3 hi and csr3 mix together: no one bit is set in every CSR3 stimulus and clear in none);
    a saturating clamp in place of the mask (csr3 mix); the CSR3 mask moved to another register's arm
    (csr3 all/hi/mix, csr2 all/lo); a CSR1 or CSR2 mask introduced (csr1 all/odd, csr2 all); the CSR3
    store reverted to the whole value.
  OUTSIDE: the mask applied at the RDP read instead of the store (reg[3] has no reader but the RDP
    read, so no observable differs); a mask conditioned on STOP (every row runs with STOP set -- the
    probe never writes STRT or INIT); a mask conditioned on access width (every write is a 16-bit
    `sh`); the CSR0 arm; INIT and init_block_addr; the big-endian emulated machines (the model's SRAM
    byte order); a mask conditioned on two or more bits of the written value at once; retention of
    one register across a write to another (each register has its own fresh session) and retention
    over time (the stable rows show immediate repeatability only).
  ANCHOR: csr0 reset and rap mask pin the two ports by the reset value and the RAP masking -- a
    one-word shift of the register window lands one port's access on the other port and the other
    on an unimplemented offset, a one-halfword shift lands both on unimplemented offsets; either way
    both signature rows red.  The park control checks the breakpoint banner's pc against the halt
    address, not merely that a breakpoint fired.

USAGE: le_csrmask_probe.py <base_bin> <fix_bin | GATE | -> <outdir>
    <base> -   <outdir>   WITNESS: base leg only, judged against the HEAD column.
    <base> <fix> <outdir> two legs: base vs HEAD, fix vs FIX; LE_CSRMASK_RESULT_base= / _fix=,
                          LE_CSRMASK_CONTROL_base= / _fix=.
    <bin>  GATE <outdir>  ONE leg vs the FIX column: LE_CSRMASK_CONTROL=OK|FAIL, LE_CSRMASK_RESULT=p/n,
                          then the sentinel.  Exit 0 iff p == n and control OK.
The output ends with the sentinel LECSRMASK_PROBE_DONE once; raw transcripts under <outdir>/raw/.
```

The one code-comment change (in `build_rows()`, beside the `stable:` rows): the repeated read is of the session's FIRST RDP value (the reset value in csr0, the ALL value elsewhere), "the want is the observation, not a literal". Code unchanged.

## 3. The gate block as it now stands (verbatim), with its dry-run

```bash
#  ---- lecsrmask: the LANCE model's CSR3 store mask (#573).
#
#  WHAT THIS PROTECTS.  `le_register_write()` stored every bit a guest wrote to CSR3; the Am7990
#  implements BSWP|ACON|BCON there and reads bits 15:3 as zero (Am7990 Technical Manual 1-22;
#  the Am79C90 datasheet says the same), so a read-back returned bits the chip never holds.  The
#  fix masks the CSR3 store with 0x0007.  CSR1 and CSR2 stay stored whole ON PURPOSE (their
#  reserved-bit read-back is unspecified by the Am7990 manual and another emulator keeps them
#  writable for a board diagnostic's sake), and three CONTRACT rows pin that so a later per-chip
#  change must re-pin them with the oracle-correction order.
#
#  The probe is BOTH the rung-3 WITNESS (artifacts/lecsrmask/witness_20261025/, 17 rows, the
#  committed build before any edit, with the HEAD column showing the stored bits) and the DETECTOR
#  (20 rows; its own pre-fix legs under artifacts/lecsrmask/floor_20261025/ and the 20-row
#  re-measure under pass1_20261025/).  It drives the UNMODIFIED `pmax -e 3100` with guest sh/lhu
#  through the real address decode -- no rig image, no disk -- which is why it lives here: this
#  gate has become the tree's general DEVICE-probe gate by accretion (see the #497 block above:
#  "it has become the tree's general DEVICE-probe gate"), it already runs image-free `"$PMAX" gate`
#  probes for a foreign CPU family, and `gate_mips.sh` is a rig-boot gate with no probe
#  infrastructure; a new gate script would move GATE_MANIFEST, a bigger claim than one probe.
#  The #497 block's own criterion -- "the NEXT device probe wired into this gate converts
#  `gatedevicesplit` from filed to OWED" -- fired at #498 and that row is OWED; this is one
#  more device probe on this gate, recorded here rather than compounded silently (the split
#  stays a harness round owing its own controls).
#
#  The `rap mask` signature row writes 0x13 to RAP on purpose and the device WARNS about it on
#  every run; THIS BLOCK's checks score the sentinel, the control line and the named rows only, so
#  that WARNING line is never counted as red here (other gates do count their own diagnostics).
LELOG=$LOGDIR/le_csrmask.log
python3 le_csrmask_probe.py "$PMAX" GATE > "$LELOG" 2>&1 || true

#  SENTINEL FIRST.  A preserved log is verified by its completion sentinel, never by its
#  existence: a killed run loses every row and looks exactly like a run that produced none.
if ! grep -q "LECSRMASK_PROBE_DONE" "$LELOG"; then
    check "le_csrmask probe completed" "no" "yes"
else
    check "le_csrmask probe completed" "yes" "yes"
    check "le_csrmask controls" "$(count "$LELOG" '^LE_CSRMASK_CONTROL=OK$')" "1"
    #  `count' is grep -ac, a BASIC regex: `  *' is the one-or-more-spaces form (a `+' there is a
    #  literal plus and matched NOTHING in the dry run against the measured fix leg).
    for v in "ram:csr0" "ram:csr3" "ram:csr2" "ram:csr1" "csr0 reset" "rap mask" "csr3 all" "csr3 bits" "csr3 hi" "csr3 mix" "csr2 all" "csr2 lo" "csr1 all" "csr1 odd" "csr1 even" "csr1 top" "stable:csr0" "stable:csr3" "stable:csr2" "stable:csr1"; do
        check "le_csrmask row: $v" "$(count "$LELOG" "^  $v  *0x.* ok$")" "1"
    done

    #  DENOMINATORS, pinned to LITERALS: `rows run' is the probe's own count (RESULT's denominator,
    #  the pin check_score_claims.py reads; SCORE_CLAIMS_MANIFEST 40 -> 41), `rows green' its
    #  numerator; `rows emitted' is the row lines the log carries, summed ARITHMETICALLY from the
    #  ok and FAIL row lines so a LOST row and a FAILING row read differently.  A row line carries a
    #  `want ' or `head ' token (a dead run prints `want ??'); the probe's `  LEG gate VERDICT: FAIL'
    #  line carries neither, which keeps it out of these two counts (dry-run on the banked legs: the
    #  fix leg twenty ok and none red, the pre-fix leg seventeen and three, the null medium none and
    #  twenty -- written in words on purpose: a fraction here would read as a score claim).
    leres=$(grep -ao '^LE_CSRMASK_RESULT=[0-9]*/[0-9]*' "$LELOG" | tail -1); leres=${leres#*=}
    leok=$(count "$LELOG" '^  .* \(want\|head\) .* ok$')
    lebad=$(count "$LELOG" '^  .* \(want\|head\) .* FAIL$')
    check "le_csrmask rows run"     "${leres#*/}" 20
    check "le_csrmask rows green"   "${leres%/*}" 20
    check "le_csrmask rows emitted" "$((leok + lebad))" "20"
    check "le_csrmask rows red"     "$lebad" "0"
fi
```

Dry-run of these matchers against the banked legs (`grep -ac`, the same call `count()` makes): fix leg -- all 20 named rows matched once, rows run 20, green 20, emitted 20, red 0, control line 1; pre-fix leg -- 17 rows matched, `csr3 all` / `csr3 hi` / `csr3 mix` absent, green 17, emitted 20, red 3, control 1; null medium -- 0 rows matched, green 0, emitted 20, red 20, control 0. `bash -n` on the block passes; the `for v in` list holds 20 names. **The first form of the row matcher, `"^  $v +0x.* ok$"`, matched ZERO rows**: `count()` is `grep -ac` in BASIC regex, where `+` is a literal plus (F24). `SCORE_CLAIMS_MANIFEST` moves 40 -> 41 in the same commit for the new `rows run` pin (F22).

## 4. The findings, numbered, with the main loop's disposition of each

APPLIED = already made in the scratch copies above; PLANNED = goes into the landing records (CHANGELOG block, ledger, OB section); CONFIRMED = checked true, nothing to change; SETTLED = a NOT-CHECKABLE premise settled by a measurement inlined in section 0; NOT ADOPTED = rejected, with the reason.

**The diff (H1/H2 comments)**
- **F1** (GLM Q12; Astra Q1): the `default:` comment had no subject -- the ruling specified "this MODEL stores them whole". **APPLIED**: "This model stores CSR1 and CSR2 whole."
- **F2** (GLM Q12): "says no more about CSR1 bit 0" could be heard as silence. **APPLIED**: "says only \"Must be zero\" for CSR1 bit 0" (am79c90:1138-1142).
- **F3** (GLM Q12; Astra Q1): the read comment dropped the old "seems to" hedge, and "Ultrix does exactly that" stated an observation the round never made. **APPLIED**: both comments attribute the observation to the old comment ("The old comment reported that Ultrix seems to read them with STOP set"; "(the old comment reported Ultrix writing them with STOP set)").
- **F4** (GLM Q12): the read comment lacked the accepts-both / gating-filed clause its write twin carries. **APPLIED**: "The model answers in either state; gating on STOP is filed, not implemented, and nothing is announced either way."
- **F5** (GLM Q12, NOT CHECKABLE): the "CSR2 bits 15:8" range. **SETTLED TRUE**: TM1986.txt:1695 `15:08 RES Reserved.`
- **F6** (grok Q1): the `case 3:` comment does not promote the C-LANCE's "Write as zeroes" into a store rule (pass-1 F22). **CONFIRMED.**
- **F7** (grok Q1, NOT CHECKABLE): the working tree's `dev_le.c` identity with `2956c32d` and `0b09e7b6`. **SETTLED**: md5 `3eab9c96` in all three; `git diff --stat 0b09e7b6 2956c32d` = CHANGELOG.md + regress/gate_hygiene.sh only. The records will word the base as "built from 0b09e7b6, whose src/ tree is identical to HEAD 2956c32d".

**The probe (header and comments; L1 construction -- the file is unshipped)**
- **F8** (Astra Q2): "each csrN session" -> "each **CSR1-CSR3** session". **APPLIED** ("each of the CSR1, CSR2 and CSR3 sessions").
- **F9** (Astra Q2; grok Q2b): "CONTROL is reserved for the apparatus" is wider than the code -- the kept-bits rows and the four `stable:` rows are `kind == "control"` and DO fail CONTROL. **APPLIED**: the CONTROL sentence now enumerates the control-kind rows from `build_rows()` and says a red SYMPTOM or CONTRACT row fails the leg but not CONTROL (D3).
- **F10** (Astra Q2; grok Q2b; GLM Q12): "by its variant table" treated the clause-(d) table as evidence. **APPLIED**: "by construction from the rows' stimuli and wants; the variant classifications are derived predictions, and the variant table's measurements are OWED, not made."
- **F11** (Astra Q4): the `build_rows()` comment called the repeated observation the "last" value. **APPLIED** (the FIRST value read again; the want is the observation).
- **F12** (grok Q2b): the opening and the SITES paragraph described HEAD's pre-fix shape as current ("stores all sixteen bits"; "`default:` ... stores the whole value") -- false in the commit that lands them. **APPLIED**: "until #573 ... stored ...; #573 masks that store to 0x0007"; SITES rewritten as before/after.
- **F13** (GLM Q34 "else" B; GLM Q12 joint-consistency): the `ram:` rows must bypass the write path and the `stable:` rows must be relative, or the header contradicts L1's 20/20. **CONFIRMED by the header and the code**: `ram:` = a `sh`/`lhu` round-trip through KSEG0 RAM; `stable:` want = the session's first read (`first`), so `stable:csr3` wants 0xffff pre-fix and 0x0007 post-fix.
- **F14** (GLM Q12; DeepSeek Q12): the docstring was not inlined. **APPLIED** (section 2).
- **F15** (DeepSeek Q12 versus Astra Q2, grok Q2a, GLM Q12): clause (b) via L0. **DISAGREEMENT D1** -- disposition: build and measure the reinstatement leg L4 in the final cycle (the fix clone with `d->reg[r] = x & 0x0007;` -> `d->reg[r] = x;` inside the new `case 3:`, rebuilt, binary newer than source, GATE mode); until measured the record says "(b): leg OWED, built in the final cycle", never that L0 measured (b). The equivalence argument is kept as corroboration only.
- **F16** (GLM Q12; GLM Q34 a): "committed build" is dev_le.c-scoped unless the trees are compared. **SETTLED** as F7 (tree-scoped by `git diff --stat`); the records word it that way.
- **F17** (GLM Q12): no md5 tie between the fix clone's `dev_le.c` and the banked `dev_le.c.fix.txt`. **SETTLED for the banked set** (RUN_IDENTITY: the clone's file md5 `29e9c2c3`; the banked copy's md5 `29e9c2c3`); the final cycle re-ties them the same way, and the landing generator REFUSES unless md5(patch(HEAD's dev_le.c)) == md5(the banked fix source).
- **F18** (GLM Q12): the sole-call-path premise. **SETTLED** by grep (section 0); grok READ the same.

**The `probe:` term, closure and records**
- **F19** (GLM Q34 a): the term cited L2 (two green legs); clause (i)'s same-script evidence is L0 (symptom) + L1 (green); pin the directory, not a `final_*` glob. **APPLIED (planned text)**: `probe:regress/le_csrmask_probe.py -- rung 3, unmodified pmax -e 3100: the 17-row witness regress/artifacts/lecsrmask/witness_20261025/ (17/17 vs the HEAD column at 03:49, before any edit, the symptom rows reading back the stored bits); the final 20-row instrument RED pre-fix (L0, GATE mode, csr3 all/hi/mix) and GREEN post-fix (L1) with the same frozen script, plus L2 (two legs), L3 (null medium) and L4 (reinstatement) under regress/artifacts/lecsrmask/pass1_20261025/final_<stamp of the final cycle>/` -- the stamp and the scores are written at landing from that cycle's RUN_IDENTITY.
- **F20** (GLM Q34 a; DeepSeek Q34 a): ORDER evidence not inlined. **APPLIED** (section 0 inlines both RUN_IDENTITY files; the witness dir keeps RESULTS_base.txt, raw/ and RUN_IDENTITY -- only the script copy is renamed `.frozen.py`).
- **F21** (grok Q3b; Astra Q3b; GLM Q34 b; DeepSeek Q34 b): close NARROWED -- but not while a `[HELD AWAITING SEAT: ...]` marker is live (section H's CLOSED-WHILE-HELD). **DISAGREEMENT D2 on timing** -- disposition: the row lands `held` with a `state_note` and a `hold_question` (the #569 precedent, commit 66920157: "state `held` for Fable 5.1"), closes NARROWED when the Fable hold is discharged or the owner rules; never `closed` while a hold is live.
- **F22** (grok Q3d, U): `SCORE_CLAIMS_MANIFEST` is 40; a `rows run` pin makes it 41 and fails the commit unless raised in the same commit. **APPLIED**: the block carries the house-idiom pin (`check "le_csrmask rows run" "${leres#*/}" 20`); `tools/precommit_check.sh:368` moves 40 -> 41 in the landing commit (added to the landing generator and its spec).
- **F23** (grok Q3d, U): a gate comment naming the stem and citing a fraction fails unless "N-row" is on the line. **CHECKED**: the block's comments carry no fraction (the dry-run numbers are written in words on purpose).
- **F24** (Astra Q3d): "ensure the named-row matcher accepts the probe's leading spaces". **CHECKED AND FOUND WORSE**: the first matcher matched ZERO rows under `count()` (BRE `+`); corrected to `"^  $v  *0x.* ok$"` and the emitted/red counts anchored on the row's `want `/`head ` token so the probe's `  LEG gate VERDICT: FAIL` line is excluded; dry-run in section 3.
- **F25** (grok Q3c; Astra Q3c; GLM Q34 c; DeepSeek Q34 c): the CHANGELOG must distinguish the model's retained behaviour from silicon; "read-back-only" is true of the CSR3 store and false of a CSR1 mask (init_block_addr); quote both Am7990 preservation sentences (TM1986 :1511-1516 and :2853-2857); the STOP change is comment-only, no gating added, Ultrix not called out of spec; attribute the PMAD-AA reading to Grok; the variant table OWED, never "measured"; no "demonstrated driver impact". **PLANNED** (the block's sentences are listed in section 4b).
- **F26** (grok Q3c): Appendix B's non-preservation cell is the Am7990 (RIGHT column), the Am79C90 preserves; the pass-1 rulings' shorthand "C-LANCE Appendix B non-preservation" would reverse it. **SETTLED TRUE** (am79c90:3411, :3686-3687); the records say "the Am79C90 preserves CSR1/CSR2 across STOP (Table B-1 item 12, left column); the Am7990 does not (right column)"; where the pass-1 shorthand is quoted it is corrected in place.
- **F27** (grok Q3c): must not say CSR2 bits 15:8 feed `init_block_addr`. **ACCEPTED** (`(d->reg[2] & 0xff) << 16`).
- **F28** (grok Q3c; Astra Q3c; GLM Q34 c-iv; DeepSeek Q34 c): the #572 census sentence must match the tree. **ACCEPTED, from the deriver run read-only today**: `EXPECT_PTY_PROBES` 78 got / 78 pinned, promptless 46 / 46, `lca_isaphys_probe.py` UNTRACKED and counted; so 78 = 77 tracked + 1 untracked at HEAD, and after #573 the pins read 79 and 47 (78 tracked + 1 untracked). The committed grandfather list already carries `wdc_lba_probe.py` (2956c32d) and `lca_isaphys_probe.py`.
- **F29** (grok Q3d, F): section F reads the PREVIOUS src-touching commit's receipt (`0901b388`, #572 -- its line exists); this round's receipt is appended keyed to the landing SHA in the follow-up records commit (the #569-#572 precedent). **CONFIRMED.**
- **F30** (grok Q3d: P, L, W, H, R, O): every new open row in both files; the ledger naming the commit (follow-up); W's state_note; H's nine recorded seats or a live hold with a question; R's MANIFEST lines (the checker's selftest pin 22 untouched); O's distinct seat notes. **ACCEPTED**: the generator writes both files; the pretests (R, L, H, O, W, U, P, F) run on the staged copies before the commit; `check_commit_attribution.py`'s closure regex is `\b(closed|closes|closing)\b` on the SUBJECT, so the subject uses "narrowed", not "closed".
- **F31** (grok Q4-1; Astra Q4-1; GLM/DeepSeek Q34-1): `py_code()`/`probe_code()`/`pty_driving()` exclude `artifacts/` (`! -path "$HERE/artifacts/*"`, gate_hygiene.sh:151); the `.frozen.py` copy needs only its CLASS_WITNESS MANIFEST line. **CONFIRMED**; today's census did not count the banked copies.
- **F32** (all six, Q4-2): `csr3 mix` 0x0015 on the pre-fix build is MEASURED (RESULTS_L0_prefix_gate.txt line 36), not predicted. **CONFIRMED.**
- **F33** (Astra Q4-3; grok Q4-3; GLM/DeepSeek Q34-3): the RAP WARNING line `[ le register select: WARNING! register 19 (max is 3) ]` is in the raw csr0 transcripts (19 = `%i` of 0x13, the `lediagfmt` filing); no check in the new block counts WARNING lines; "no gate counts WARNING lines" would be false of other gates. **APPLIED**: the block's sentence is scoped to THIS block's checks.
- **F34** (Astra Q4): PRETABLE's "all four labels driven" overstated coverage. **APPLIED** (PRETABLE.out: the CSR1-CSR3 write arms are exercised; CSR0 gets its reset read and the RAP masking only; the CSR0 arm's coverage is NOT claimed).
- **F35** (GLM Q34 d-4): the plan's list omitted `floor_20261025/`, `killtable_20261025/`, `pass1_20261025/`. **CONFIRMED COVERED**: the commit adds the whole `regress/artifacts/lecsrmask` tree; every `.py` under it is `.py.txt` except the one renamed witness copy, which the MANIFEST names.
- **F36** (GLM Q34 d-1): no md5 pin between the landed `dev_le.c` and the measured copy. **CONFIRMED COVERED** (F17: the generator's refusal).
- **F37** (GLM Q34 minor): grep the gate's expected RESULT strings exactly ("20/20", "0/20") rather than a "20/20/0" shorthand. **NOT ADOPTED as a literal grep**: the block pins `rows run` 20, `rows green` 20, `rows emitted` 20 and `rows red` 0 as four equality checks (the ip30 idiom); "20/20/0" was the plan's prose, not a check, and is gone.
- **F38** (GLM Q12): the brief's floor sentence ("a detector that fails (a)(b)(c) is above the floor") was ambiguous. **APPLIED** (section 0 restates it as "reds on each of").
- **F39** (GLM Q12, NOT CHECKABLE: "if the 2026-08-23 ruling folded (d) into the vacuity floor, the answer flips"): **SETTLED, AND IT CORRECTS THIS ROUND'S OWN PREMISE** -- the carrier's clause (d) text ends "IT IS A FLOOR CLAUSE, so a breach is L2"; the pass-2 brief called (d) "separate", which every seat took as given. The disposition does not flip: an UNMEASURED floor clause honestly recorded as OWED is not a breach and not an L4 (the carrier: "a claimed-but-unmeasured floor clause is L4 exactly when the record asserts a MEASUREMENT or a NUMBER that was not made"), and the licence to land with it owed is the owner's post-classifier-stop rule (#567), not (d)'s rank. The CHANGELOG and README say exactly this.
- **F40** (grok Q2c; Astra Q2; GLM Q12; DeepSeek Q12): "I do not read the carrier as forbidding a (d)-owed landing". **ACCEPTED with F39's correction of the warrant.**
- **F41** (GLM Q34 c-iv): the #572 census claim must name its population and not extrapolate. **ACCEPTED** (F28's numbers are the population).
- **F42** (grok Q3c): do not say one STOP-preservation reading was implemented. **ACCEPTED**: the model has no STOP-clear / preserve logic at all (`lecsr3stopclear` filed; both Am7990 sentences quoted, neither implemented).
- **F43** (Astra Q3c): attribute the PMAD-AA reading to its reporting seat. **ACCEPTED** (Grok, pass-1 F2, web-sourced).
- **F44** (grok Q1c; GLM Q34 c-ii): bit 0 of `reg[1]` survives the SRAM mask and the INIT path consumes `reg[1]`/`reg[2]`, which is why a CSR1 mask would be functional rather than read-back-only. **CONFIRMED** (section 0).

### 4b. The CHANGELOG block's load-bearing sentences (so a seat can check them before they are written)
1. The CSR3 store is masked to BSWP|ACON|BCON (0x0007); both AMD manuals read bits 15:3 as zero (TM1986 1-22; Am79C90 datasheet). Guest-visible effect: the CSR3 read-back only (no other reader of `reg[3]`).
2. CSR1 and CSR2 stay stored whole as THIS MODEL's retained behaviour under an interpreted reading -- the Am7990 manual leaves their read-back unspecified (host-write constraints only); the Am79C90 reads CSR2's reserved bits as zero and says only "Must be zero" for CSR1 bit 0; MAME keeps both writable on the Am7990 for a MIPS RS2030 diagnostic. NOT a claim about Am7990 silicon. A CSR1 mask would change `init_block_addr` (bit 0 reaches it); CSR2's upper byte is masked at the consumer.
3. The STOP comments are corrected as records (both manuals: accessible only while STOP is set; the old comments inverted it); the model's acceptance of either state is unchanged (`lestopgate`); no gating added; Ultrix's reported STOP-set accesses are the in-spec case. The two Am7990 sentences on CSR1/CSR2 across STOP are quoted (:1511-1516 "must be reloaded"; :2853-2857 "normally not affected ... recommended to reload"); neither is implemented (`lecsr3stopclear`). Appendix B: the Am79C90 preserves CSR1/CSR2, the Am7990 does not.
4. The measurements name their artifacts (the final cycle's `final_<stamp>/RUN_IDENTITY.txt` and RESULTS files; the witness dir); the clause-(d) table is OWED (killtable_20261025/README.txt, PRETABLE.out before it), recorded under the owner's #567 rule; (b) is the measured L4 leg; (c) measured at the L3 file.
5. The #572 follow-up addendum: 78 pinned = 77 tracked + 1 untracked (`lca_isaphys_probe.py`) at HEAD; #573 moves the pins to 79 / 47.
6. Seats: pass 1 (Astra, Grok, GLM x2, DeepSeek x2, Argon by the web route x2), its F2 (Astra adjudicating; Grok, GLM x2, DeepSeek x2); pass 2 (Astra, Grok, GLM x2, DeepSeek x2); this F2b; Argon a SEAT FAILURE on pass 2 and F2b (meter 0 of 2400, reset 07:30:45 CDT -- re-fired after the reset, answers filed in the records commit); Fable 5.1 HELD by the owner with its question; kimi, minimax and the Opus review seat DELIBERATELY NOT FIRED by roster. The PMAD-AA reading is Grok's.

## 5. The disagreements, both sides verbatim

**D1 -- clause (b) and the pre-fix build.** DeepSeek Q12: *"clause (b) is NOT discharged by L0 as worded -- the patch adds a `case 3` branch rather than altering an existing assignment, so there is no 'verbatim reinstatement of `d->reg[r] = x;` at the one fixed site' that produces the pre-fix build; L0 only ran the actual base, not a reverted branch."* Astra Q2: *"L0 also discharges (b) because restoring the sole H1 store produces the pre-fix behavior; this is equivalence, not a separately measured revert build."* Grok Q2a: *"Reinstating `d->reg[r] = x` there is the pre-fix binary, which L0 already ran (F6, C13). There is no second revert object file; the record already says the pre-fix build is that reinstatement."* GLM Q12: *"Clause (b) via L0 is sound ... This holds only because the whole patch is displayed and accounted (35/35); it does not hold on trust in 'one site' alone."* **Main loop:** the carrier settles disagreements empirically, so L4 -- the reinstatement built inside the new structure -- is measured in the final cycle and becomes the (b) record; DeepSeek's wording point stands until then (the record says OWED, not measured); the equivalence reading is corroboration.

**D2 -- closure timing.** Grok Q3b: *"Section H forbids `closed` while a live `[HELD AWAITING SEAT: ...]` remains (CLOSED-WHILE-HELD) ... Sequence it: `in work` is invisible to W and can carry a live hold; close NARROWED only after that hold is discharged. Argon's owed answers and a still-live Fable hold are that constraint. They are not a reason to keep the CSR3 question open."* Astra Q3b: *"Close NARROWED after landing and grading: CSR3 fixed; CSR1/CSR2's proposed masks withdrawn and transferred to `lecsr12readback`."* GLM Q34 b: *"the state stays held until grading, as the plan already says."* **Main loop:** compatible once sequenced -- `held` at landing (the #569 form), NARROWED closure when the Fable hold is discharged or the owner rules.

**D3 -- what CONTROL means.** Grok Q2b: *"'CONTROL is reserved for the apparatus' is wider than the code: `csr3 bits`, `csr2 lo`, `csr1 even`, `csr1 top`, and the four `stable:` rows are `kind == "control"` and do fail CONTROL. The three contract rows do not, which is the F14 rule, and that part is implemented."* Astra Q2 asked for *"a CONTRACT failure 'does not by itself fail CONTROL'"*. **Main loop:** both adopted in the docstring (the enumeration plus "by itself"); the kinds are NOT changed in code -- a re-kinding would alter the measured revision for a labelling gain, and the kept-bits rows being control-kind means an accept-side regression also reds the control line, which is disclosed, not hidden.

**THIS FIRING ANSWERS D1-D3 (section 5) AND QUESTIONS 2 AND 3 ONLY.**  F1-F44 went to a separate firing of this same packet; treat their dispositions as given and do not re-adjudicate them.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

## 6. The three questions (answer format at the end)

**Q1. Which of the ACCEPTED dispositions above (the APPLIED / PLANNED / ACCEPTED ones -- 33 of 44) are WRONG?** Name them by F-number with the reason; a disposition that applied the wrong fix, or accepted a finding that was itself false, counts. Also say whether F37's NOT ADOPTED is right.

**Q2. D1.** Is building and measuring L4 (the reinstatement inside `case 3:`, GATE mode, same frozen script) the right discharge of clause (b) for this round, and until it is measured is "(b): leg OWED, built in the final cycle" the right record wording? If L4 reds (expected; the number is not written anywhere until measured), does "(b): measured at final_<stamp>/RESULTS_L4_reinstatement.txt" complete the floor record, with (d) OWED and disclosed as in F39?

**Q3. D2 and the records.** (a) Is `held` with a `state_note` and a `hold_question` the right landing state, with NARROWED closure deferred until the Fable hold is discharged or the owner rules? (b) Is the `probe:` term in F19 the right text (L0 + L1 as clause (i)'s evidence, the directory pinned, the witness named for ORDER)? (c) Is F39's correction right -- that the licence to land with (d) OWED is the owner's #567 rule, and that the pass-2 brief's "(d) is separate from the floor" was a wrong premise that the seats inherited?

**Answer format.** VERDICT line first: `RATIFY` | `RATIFY WITH CHANGES` | `NOT RATIFY`, then one `WRONG:` line naming the F-numbers of the dispositions you find wrong (or `none`). Then Q1, Q2, Q3 in order. Label every claim READ (you opened the file), DERIVED (from the packet's text), or NOT CHECKABLE (name the one fact that would settle it). Count the arguments, not the seats. A seat reviewing its own pass-2 position should be HARDER on it, not easier; a ruling that adopted your position gets MORE scrutiny from you, not less.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`T18F2B_B: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
