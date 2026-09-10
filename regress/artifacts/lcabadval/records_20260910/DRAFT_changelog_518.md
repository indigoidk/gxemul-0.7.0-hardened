<!-- ================================================================================
     DRAFT ROUND BLOCK -- NOT THE SHIPPED CHANGELOG TEXT.  #518 IS HELD.

     Rescued out of the session scratchpad (Windows Temp, volatile) on 2026-09-10 so the
     draft survives the session.  Two things must be true before any of this lands in
     CHANGELOG.md, and neither is true today:

       1. THE RECORDS AUDIT IS AT NO-GO.  codex_audit2_20260910.txt, the SECOND audit of this
          rewritten block, returned `VERDICT: NO-GO (17 items)'.  The first audit
          (codex_audit_20260910.txt) returned NO-GO (27 items) and drove this rewrite.  A
          correction is not safer than the thing it corrects; the 17 are undisposed.

       2. THREE MUTANTS ESCAPE THE SHIPPED 67-ROW INSTRUMENT.  Measured, table 4, below.
          Disposition (floor breach under clause (d), or filed coverage debt) is OWED.

     THE INLINE `*** OWED ***' MARKERS BELOW ARE SUPERSEDED BY THE MEASURED BLOCK HERE.
     Every score is read from a log that ends in its sentinel `LCABADVAL_DONE'.

     TABLE 3 -- 64-row instrument, main loop, the two seats' scratch clones against their frozen
     baselines, killtable_20260910/t3/SCORES3.txt, finished 05:42:30:
         BASE                  64/64
         M20_def_echo          64/64   EQUIVALENT BY CONSTRUCTION (odata = idata on a read of 0)
         M25_conf_widen        62/64   conf widen, conf 6
         M26_base_widen        63/64   wbase0 widen
         M27_mask_widen        63/64   wmask0 widen
         M28_field_idata       63/64   wmask0 hif
         M29_tbena_nostore     63/64   tbena clear
         M30_nolatch_mask1     62/64   wmask1 indep, wmask1 once
         M31_nolatch_defr      63/64   def r
         M32_shared_conf_wen   62/64   wen base0, all wen
         M33_shared_m0_defw    63/64   all defw
         M34_conf_dropbit0     63/64   conf live
         M35_tbena_dropten     61/64   tbena live, tbena stored, tbena b1
         M36_nolatch_defw      63/64   def w
         M37_base0_nonzero     63/64   wbase0 zero
         M38_wen_base1_off     63/64   wen base1
         M39_wen_base0_off     62/64   wen base0, all wen
         M40_conf_ann_bit0     61/64   all conf, conf silent, conf ann6
         M41_mask_raw_store    62/64   wmask0 widen, wmask0 hif
         M42_def_allones       63/64   def read0
         M43_mask1_widen       64/64   ESCAPED at 64 rows
         M44_mask1_field_idata 64/64   ESCAPED at 64 rows
         M45_base1_nosg        64/64   ESCAPED at 64 rows
         M46_conf_ann_wide     63/64   conf silent
         M47_base1_widen       64/64   ESCAPED at 64 rows
     The four escapes are what round four's rows were written for.

     TABLE 4 -- the final 67-row instrument, killtable_20260910/t4/SCORES4.txt, finished 06:22:14.
     Baseline is the CURRENT SEC dev_lca.c; it differs from table 2's frozen copy by 2 lines, the
     round-four comment-only edits, and the driver records that diff itself:
         BASE                  67/67
         M43_mask1_widen       67/67   *** STILL ESCAPES ***
         M44_mask1_field_idata 67/67   *** STILL ESCAPES ***
         M45_base1_nosg        66/67   wbase1 sg          <- round four's row kills it
         M46_conf_ann_wide     66/67   conf silent
         M47_base1_widen       67/67   *** STILL ESCAPES ***
         M48_wen_perreg        66/67   wen once           <- PRETABLE 4's own prescribed mutant
         M49_def_narrow        66/67   def width
     All four rows round four added carry a measured kill.  THREE MUTANTS DO NOT DIE:
     M43 and M44 weaken W_MASK1, M47 weakens W_BASE1 -- the SECOND window's register pair, whose
     rows were added late and are thinner than BASE0/MASK0's.  That is the `#499' shape: a repair
     made at the address the mutant used, leaving the symmetric cell open.  It is a clause-(d)
     question and it is OWED, not answered.

     The clone was restored from SEC, rebuilt, and its sentinel cleared; both project build trees
     and the arc tree read part1=CLEAN part2=FRESH at the end of table 3.
================================================================================ -->

# `#518` lcabadval: six chipset-register guards ended the emulator on values the LCA manual makes legal, one of which the manual REQUIRES the boot ROM to write

**THE DEFECT.** `DEVICE_ACCESS(lca_ioc)` in `src/devices/dev_lca.c` had six write arms of one shape -- store the
value, then `fatal(); exit(1)` unless it equalled a tiny hard-coded set -- plus a `default:` arm that ended
the process on any offset the switch does not list, in either direction. The accepted sets, enumerated
from the predicates: `IOC_CONF` {0, 1}; `IOC_TB_ENA` {0, 0x80}; `W_BASE0` {0, 0x300800000}; `W_MASK0`
{0x700000}; `W_BASE1` {0x240000000}; `W_MASK1` {0x3ff00000}. **The guards were WRONG, not merely harsh, and
the manual is what says so** (Alpha 21066/21066A HRM, local since 2026-09-08 as `_scratchpad/21066_66a_hrm.txt`
at the project root; every cited line opened by the codex records audit as well as by the loop): Table 6-6
(`:9586-9598`) lists THIRTEEN legal `W_MASK<31:20>` encodings, of which each register accepted one; S6.4.14
item 3 (`:10791-10792`) REQUIRES SROM to write ZERO to both `W_BASE` registers, and `W_BASE1` ended the
process on zero -- the value it also reads back before anyone touches it, so writing back what you just read
was fatal; Table 6-13 (`:10443`, `:10453`) makes every `TB_ENA` bit but TEN reserved type X, and the legend
(`:985-988`) says X bits are IGNORED ON WRITE -- `0x81` differs from the accepted `0x80` in one bit the
hardware is documented to ignore; Table 6-10 (`:10246-10254`) makes `IOC_CONF<1:0>` a writable two-bit FIELD
(only encodings 00 and 01 are PCI configuration-cycle types; 2 is a legal register value, not a cycle type),
of which the guard accepted half. Figure 6-9 (`:10556-10560`) gives `W_BASE` as base `<31:20>`, SG `<32>`, WEN
`<33>`, agreeing with `alpha_lcareg.h`. S6.4 (`:10180-10181`; `:10175` is the section heading) makes the
accesses quadword.

**WITNESSED AT RUNG 3 BEFORE ANY EDIT** (`regress/lca_badval_probe.py`, unmodified `-E alpha -e alphabook1`,
built by the Opus measuring seat on the one-invocation ask the lifecycle mandates): on the committed build the
six `<arm> legal` rows are RED, **14/20** (`regress/artifacts/lcabadval/witness_20260909/HEAD_74daefd.out` and
`HEAD_74daefd_run2.out` -- two runs, row-identical, differing in timestamp and in the HEAD their banner
records, 74daefd and 54a2eb4, with `dev_lca.c` identical across those commits), each death carrying its own
arm's diagnostic and none landing in `default:`; the no-guard sibling `W_T_BASE0` survives the value that
kills at `W_MASK0`. Values: `CONF` 2, `TB_ENA` 0x81, `W_BASE0` 0x280000000 (WEN + an aligned base), `W_MASK0`
0x100000, `W_BASE1` 0, `W_MASK1` 0xfff00000. The witness also **measured a prior panel claim false**:
`FIXDESIGN_brief.md` had recorded `TB_ENA` as "NOT a functional defect -- 0/2"; the `0x81` row is red, and the
count was right about the TEN field and wrong about the register. `#516` (74daefd) had removed the confound
the design phase worried about: until then the ISA interrupt stubs ended the process with the same status.

**THE FIX, and its SCOPE, which grew on the measurement.** The 2026-09-09 flagship ruling named FOUR arms
(the window bases and masks), assigned `IOC_CONF` to option-set member 4 (ACCEPT the field) and assessed
`TB_ENA` out of the round. The witness then measured `TB_ENA`'s reserved bit and `CONF`'s reserved bits as
live kills, and the implementation covers all SIX arms: `IOC_CONF` stores `& 0x3` (member 4) and announces
once when bit 1 is set -- CFG AD<1:0> encodings 10/11, which are not configuration-cycle types (bit 0 is the
type-1 select `#515` models; the first draft of this diff called bit 1 that, and the grok seat read
`lca_pci_conf` and corrected it); `TB_ENA` stores `& TEN` (member 4, reserved ignored); `W_BASE0/1` store
`base | SG | WEN` with no whitelist (member 4) and announce once, on one shared bit, when any window is
ENABLED (translation is not modelled); `W_MASK0/1` validate the field -- `f = (idata & 0xfff00000) >> 20;
(f & (f + 1)) == 0` is exactly Table 6-6's thirteen contiguous low-ones encodings, enumerated over all 4096
field values by the glm seat and by codex -- and **store only when valid** (the old arms stored BEFORE they
checked), declining once per register otherwise with the previous value kept (member 3); the default arm
declines a write with **no IOC register-value change** (the announce latch is the only state that moves) and
answers a read with zero, once per direction (member 3). One helper, `lca_ioc_announce()`, and six new
`d->warned` bits beside `#516`'s two. `fatal()` prints and returns (`debugmsg.c:384-390`); the helper comment's
claim that `-q` cannot silence it is source-supported and NOT measured by this probe. Among the offsets the
default arm now declines are four DOCUMENTED registers this model has never had -- STAT0, STAT1, SFT_RST,
PAR_DIS -- two of which S6.4.14 requires SROM to write; they survive instead of ending the process, which is
an improvement and not the register, and are filed as `lcaiocstat0` (grok found them; the codex design
pre-read then REVISED the filing: STAT1 is RO, STAT0 is RO status plus W1C ERR/LOST, SFT_RST is a persistent
WO reset control -- member 7 for the status pair, member 3 now for the other two). The only executable
`exit(1)` left in the file is `lca_isa`'s lane check, assigned to `lcaisalane` by the 2026-09-09 adjudication
and witnessed at rung 3 today (13/16 on HEAD: a byte read of the console UART's LSR answers zero).

**THE DETECTOR, shipped with the fix in the same probe: 67 rows, 67/67 on the fix**
(`witness_20260909/FIX518_detector_run5.out`). The instrument grew through four pass-2 repair rounds --
40 rows at 40/40 (`FIX518_detector_run1.out`), 53 rows at 52/53 (`run2.out`: my own wrong test constant,
recorded below), 58 at 58/58 (`run3.out`), 64 at 64/64 (`run4.out`; the unsplit-session draft that read 63/64
was re-measured from its backed-up instrument as `FIX518_detector_run3_D9unsplit.out` because the first run's
log had been overwritten), 67 at 67/67 (`run5.out`). Twenty witness rows and forty-seven detector rows:
`<arm> stored` (accepted then legal, read back the NORMALIZED value -- `TB_ENA` 0x81 reads 0x80; writing the
accepted value first makes a skipped later store visible only where accepted and normalized differ, which
is why `tbena clear` exists), `wmask{0,1} declined` / `wmask0 once` / `kept2` / `wmask1 indep` / `wmask1 once`,
`conf reserved` / `conf once`, `wen once` / `wbase1 wen` / `wbase0 zero`, `def alive` / `def w once` /
`def read0` / `def r once` / `def width`, the mask cells (`conf widen`, `tbena clear`, `tbena b1`, `wbase0 sg`,
`wbase0 widen`, `wmask0 widen`, `wmask0 hif`, `wmask0 f2`), the six-announce cross-latch session with two
reasons repeated, the per-label WEN rows, the silence session (`wen silent`, `wbase0 nowen`, `conf silent`)
and the announcing session (`conf ann6`, `conf 6 stored`), and round four's `wmask0 zero`, `wbase1 sg` and
`def state`. The PRE-TABLE CHECK's sections 1-5 were written before the first table -- proven not by the
file's mtime (it has been appended nine times) but by their verbatim copy inside the pass-2 brief sent at
00:02 -- and sections 6-9 are dated appendices, never rewrites.
