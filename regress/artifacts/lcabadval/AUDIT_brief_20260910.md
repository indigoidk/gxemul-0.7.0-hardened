# `#518` lcabadval -- RECORDS AUDIT of the CHANGELOG block BEFORE it is committed: find every claim the artifacts do not support

Please do not simply ratify. This is a RECORDS audit: read the draft below against the files on disk and
report every sentence that a file contradicts, that no file supports, or whose number does not match its
named log. The frozen-number class (a number written before or apart from the run that produced it) is
this project's most repeated records defect; the author wrote parts of this draft before some tables ran.
Prose only. VERDICT LINE FIRST, then a numbered list: claim (quoted), the file checked, what it says.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. The artifacts: `regress/artifacts/lcabadval/` -- `witness_20260909/`
(HEAD_74daefd.out, FIX518_detector_run1..4.out), `pass2_20260910/` (the seat answers), `killtable_20260910/`
(PRETABLE.out sections 1-8, SCORES.txt, SCORES_B.txt, README.txt, the .raw logs, `t2/` with PROGRESS.txt,
PREDICTIONS.txt and its .raw logs, `t3/SCORES3.txt` -- STILL BEING WRITTEN by a running table; audit what is
there and say which rows are not yet present), `propagate518.out`. The diff itself: `git diff -- src/devices/dev_lca.c`
(uncommitted) and `regress/lca_badval_probe.py` (untracked, 64 rows). The manual: `_scratchpad/21066_66a_hrm.txt`
at the project root, for the cited line numbers.

## WHAT TO CHECK, in order of value
1. Every SCORE (n/m) in the draft against the log it names or implies: 14/20, 20/20, 40/40, 52/53, 58/58,
   63/64, 64/64, every mutant score. Say which log carries each and whether the log's sentinel is present.
2. Every MANUAL citation (Table 6-6 :9586-9598, S6.4.14 :10791-10792, Table 6-13 :10443/:10453, legend
   :985-988, Table 6-10 :10246-10254, Figure 6-9 :10556-10560, S6.4 :10175) -- open the lines; does each say
   what the draft says it says?
3. Every claim about a SEAT ("codex NO-GO", "grok NOT RATIFY", "deepseek NOT RATIFY", the kimi substitute,
   "agy not fired", what each seat found) against `pass2_20260910/*.txt`.
4. Every claim about the CODE (which arms, which masks, `(f & (f + 1)) == 0`, "the only executable exit(1)
   left is lca_isa's", "six new d->warned bits", the default arm's behaviour) against the diff.
5. Every count: rows per stage (20, 40, 53, 58, 64), mutants per table, "three repair rounds", "four
   vacuous rows", "thirteen encodings".
6. Anything the draft asserts as done that the artifacts show as not done (propagation, clearance, tables).

## THE DRAFT (two files, verbatim)
# `#518` lcabadval: six chipset-register guards ended the emulator on values the LCA manual makes legal, one of which the manual REQUIRES the boot ROM to write

**THE DEFECT.** `DEVICE_ACCESS(lca_ioc)` in `src/devices/dev_lca.c` had six write arms of one shape --
store the value, then `fatal(); exit(1)` unless it equalled a tiny hard-coded set -- plus a `default:`
arm that ended the process on any unlisted offset in either direction. The accepted sets, enumerated
from the predicates: `IOC_CONF` {0, 1}; `IOC_TB_ENA` {0, 0x80}; `W_BASE0` {0, 0x300800000};
`W_MASK0` {0x700000}; `W_BASE1` {0x240000000}; `W_MASK1` {0x3ff00000}. **The guards were WRONG, not
merely harsh, and the manual is what says so** (Alpha 21066/21066A HRM, local since 2026-09-08 as
`_scratchpad/21066_66a_hrm.txt`, every line read rather than cited from a seat): Table 6-6 (`:9586-9598`)
lists THIRTEEN legal `W_MASK<31:20>` encodings, of which each register accepted one; S6.4.14 item 3
(`:10791-10792`) REQUIRES SROM to write ZERO to both `W_BASE` registers, and `W_BASE1` ended the process on
zero -- the value it also reads back before anyone touches it, so writing back what you just read was
fatal; Table 6-13 (`:10443`, `:10453`) makes every `TB_ENA` bit but TEN reserved type X, and the legend
(`:985-988`) says X bits are IGNORED ON WRITE -- `0x81` differs from the accepted `0x80` in one bit the
hardware is documented to ignore; Table 6-10 (`:10246-10254`) makes `IOC_CONF<1:0>` a two-bit FIELD, of
which the guard accepted half. Figure 6-9 (`:10556-10560`) gives `W_BASE` as base `<31:20>`, SG `<32>`,
WEN `<33>`, agreeing with `alpha_lcareg.h`. S6.4 (`:10175`) makes the accesses quadword.

**WITNESSED AT RUNG 3 BEFORE ANY EDIT** (`regress/lca_badval_probe.py`, unmodified `-E alpha -e
alphabook1`, built by the Opus measuring seat on the one-invocation ask the lifecycle mandates): on HEAD
`74daefd` the six `<arm> legal` rows are RED, **14/20**, each death carrying its own arm's diagnostic and
none landing in `default:`; the no-guard sibling `W_T_BASE0` survives the value that kills at `W_MASK0`
(`regress/artifacts/lcabadval/witness_20260909/HEAD_74daefd.out`, two runs byte-identical but for the
recorded HEAD). Values: `CONF` 2, `TB_ENA` 0x81, `W_BASE0` 0x280000000 (WEN + an aligned base), `W_MASK0`
0x100000, `W_BASE1` 0, `W_MASK1` 0xfff00000. The witness also **measured a prior panel claim false**:
`FIXDESIGN_brief.md` had recorded `TB_ENA` as "NOT a functional defect -- 0/2"; the `0x81` row is red, and
the count was right about the TEN field and wrong about the register. `#516` (74daefd) had removed the
confound the design phase worried about -- until then the ISA interrupt stubs ended the process with the
same status as these guards.

**THE FIX: widen the whitelists to the manual's fields** (flagship ruling 2026-09-09, on the codex fix
design of 2026-09-08 and a pass-1 panel). `IOC_CONF` stores `& 0x3` and announces once when bit 1
(type-1 cycles, not modelled) is set; `TB_ENA` stores `& TEN`; `W_BASE0/1` store `base | SG | WEN` with no
whitelist and announce once, on one shared bit, when any window is ENABLED (translation is not modelled);
`W_MASK0/1` validate the field -- `f = (idata & 0xfff00000) >> 20; (f & (f + 1)) == 0` is exactly Table
6-6's thirteen contiguous low-ones encodings -- and **store only when valid**, declining once per register
otherwise with the previous value kept (the old arms stored BEFORE they checked); the default arm declines
a write with no state change and answers a read with zero, once per direction. One helper,
`lca_ioc_announce()`, and six new `d->warned` bits beside `#516`'s two. Option-set member 3 throughout;
`fatal()` prints and returns. The only executable `exit(1)` left in the file is `lca_isa`'s `ofs > len`
lane check, assigned to `lcaisalane` by the 2026-09-09 adjudication. `W_T_BASE0/1` are untouched.

**THE DETECTOR, shipped with the fix in the same probe: 40 rows, 40/40 on the fix**
(`witness_20260909/FIX518_detector_run1.out`). Twenty witness rows (live + legal + attribution per arm,
two controls) and twenty detector rows: `<arm> stored` (accepted then legal, read back the NORMALIZED
value -- `TB_ENA` 0x81 reads 0x80, which is the reserved-bit rule in one row), `wmask{0,1} declined` /
`once` / `kept2` / `indep` (an unsupported encoding keeps the previous value, announces once, and MASK1's
latch is independent of MASK0's in the same session), `conf reserved` / `conf once` (0x100000002 reads
0x2), `wen once` / `wbase1 wen` / `wbase0 zero`, and `def alive` / `def w once` / `def read0` / `def r once`.
Every `stored` session writes the accepted value FIRST so a skipped store reads the accepted value, not
zero -- the one row whose channel would otherwise be fixed. The PRE-TABLE CHECK was written before table
1 (`killtable_20260910/PRETABLE.out`, mtime is the proof): sibling parity (three asymmetries, each a row
or a sentence), claim-to-row for every added comment, the guard/body field census (`d->warned` now eight
bits, the disagreeing state built in-session), and the CHANNEL line per row.

**KILL TABLE** -- `killtable_20260910/TABLE1.out`: *** OWED: base, M1..M23 from PRETABLE §5, the
measuring seat's own smallest-edit mutants, every clean sweep disposed. WRITE THE SCORES FROM THE LOGS
BEFORE THIS BLOCK IS COMMITTED; a number here that predates its log is the frozen-number class. ***

**PASS 2 ON THE REAL DIFF** -- `regress/artifacts/lcabadval/PASS2_brief_20260910.md`, eight transports +
the Opus seat + the main loop as Fable: *** OWED: seat-by-seat dispositions, the disagreements in both
sides' words, and the repair chain's closing zero with its denominator. ***

Propagated: *** OWED: est/, build-asan/, /tmp/gxsec-build; two-part clearance RUN, output recorded. ***
Witness: `probe:regress/lca_badval_probe.py` (rung 3, 14/20 -> 20/20 -> 40/40 with the detector).

---- (pass-2 section) ----
**PASS 2 ON THE REAL DIFF** (`regress/artifacts/lcabadval/pass2_20260910/`, brief 32.8 KB with the diff,
the detector block and the pre-table check inlined; codex and kimi pointer-fed above the argv cap): codex
GPT-6 Astra **NO-GO**, grok **NOT RATIFY**, deepseek NOT RATIFY, glm / minimax / kimi-substitute conditional;
the kimi CLI on its weekly 403 wall and COVERED by `kimi-k3:cloud`; agy DELIBERATELY NOT FIRED
(measurement reserve); the Opus seat holding the tables; the main loop as Fable adjudicating. **Every
finding was pre-ship (L1) or a wrong record (L4), and all were repaired in round, in two rounds:**

* **A live detector defect** (kimi substitute, from the packet alone): `def read0` scored the STALE `t3`
  printed after a store-only phase -- index 0 where the load was in phase 1 -- so `M20_def_echo`, a
  mutant in my own table, would have passed all 40. Index 1 now.
* **The enumeration was wrong, not merely incomplete.** My DEPENDS-ON grid had {kept, narrowed, dropped}
  per mask; four packet-fed seats named the missing **widened** cell (minimax: `& 0x3` -> `& 0x7` stores
  reserved bit 2; W_MASK `& 0xfff00000` -> `& 0xfffff000`; glm: `f = idata >> 20` declines a legal value
  carrying bit 32) and the missing **latch-removed** cells at MASK1 (one unsupported write) and at the
  default read (one read). Codex added the **assignment-vs-accumulation** latch cell (no session repeated
  an earlier reason after later ones), a field-rule weakening that admits encoding 2 (`== 0` -> `<= 2`;
  rejecting 5 and 9 does not exclude it), and that my full-width diagnostic check used `0x5a5a5a5a`, which
  fits in 32 bits. Grok added the **per-label WEN announce** (the shared latch bit is the 7g-1 join reached
  by another door: `wen once` pinned only "at least one of two in a BASE0-first session") and the CONF
  announce operand. Thirteen rows in round one, five in round two: 40 -> 58, **58/58 on the fix**
  (`FIX518_detector_run3.out`). Round one scored 52/53 because **my own test constant** `0x100f0000` was
  bit 28 (declined) rather than `0x100000` plus low bits; the row refused the wrong constant, and it is
  recorded rather than silently fixed.
* **Two corrections of the loop by codex, both accepted:** the SG-drop cell three packet-fed seats named
  was never a hole (`wbase0 live`'s accepted `0x300800000` carries SG); and my accept-row growth
  candidate (the old whitelist re-added) was inconsistent -- that whitelist accepts `0x300800000` and
  zero, so it reddens neither `wbase0 live` nor `wbase0 zero`. `conf live` and `tbena live` get real
  growth mutants (`& 0x2`, `& 0`) instead.
* **L4 in the diff** (grok, from `lca_pci_conf`): my CONF comment and announce called bit 1 the type-1
  select; `type1 = d->ioc_conf & 1` (`#515`) says bit 0 -- bit 1 is CFG AD<1> (encodings 10/11, not a
  configuration-cycle type). Reworded. And the default-arm comment called every non-switch offset
  "unlisted": **STAT0, STAT1, SFT_RST and PAR_DIS are documented registers this model has never had**,
  two of which S6.4.14 requires SROM to write; they now survive as declined writes instead of ending the
  process, which is an improvement and not the register -- filed as `lcaiocstat0` (member 7), and the
  comment says so.
* **Recorded, not rowed:** the registers are WO on hardware with UNPREDICTABLE readback (HRM `:980-988`),
  so every read-back row tests the model's echo POLICY, written into the probe's contract (grok); "once per
  device instance" is untestable with one LCA (codex); the `-q` clause is the carrier's measured fact about
  `fatal()`, not this diff's claim (kimi, codex); the HEAD log's banner stamps `54a2eb4` because HEAD moved
  during the witness run, `dev_lca.c` unchanged across it (Opus, grok). PRETABLE gained §6 and §7 as
  dated appendices, never a rewrite: §4 had named four mutants that §5's list dropped -- the
  prescribed-rows-lost-in-a-rewrite shape, caught by grok and restored.

**Round three came from the tables themselves.** Both Opus seats were walled mid-table by the Agent
tool's session limit (resets 03:00 America/Chicago; the shared-transport class, both Anthropic measuring
seats lost at once), and what they had measured stood, every log carrying its sentinel. Table 2 (58 rows,
`killtable_20260910/t2/`) had BASE 58/58 and M1..M24 all killed but `M20_def_echo` -- which is
**equivalent by construction** (`odata = idata` on a default-arm READ, where `idata` is zero: the fixed
code under another name; the table-1 seat had already built the working form, `M29_def_allones`, killed
57/58 by `def read0`). Table 1's own additions swept the 58-row instrument four ways and each was a
vacuous row of mine: `wmask0 hif`'s prior value equalled its wanted value, so a decline read like a store
(blind to the wide-mask forms); the TB_ENA rows drove only reserved bit 0 (blind to `& ~1`); and no
session had written W_BASE without WEN, or CONF without bit 1, and asserted SILENCE (blind to `&` -> `|`
on either announce test, and to `== 0x2`). Round three: `tbena b1`, a distinct prior at `wmask0 hif`,
and two silence sessions -- the first draft put the announcing value in the same session and `conf silent`
read 1 on the correct build (63/64), the row refusing its own construction. **64 rows, 64/64 on the fix**
(`FIX518_detector_run4.out`). The main loop then ran TABLE 3 itself in the seats' scratch clones, against
their frozen baselines (both `cmp`-identical to SEC at start): BASE, M20, the twenty-three table-2 mutants
not yet run, and table 1's six sweepers. Kills measured on the 58-row instrument stand for their mutants,
because added rows can only add reds.

*** OWED: the table-3 scores from `killtable_20260910/t3/SCORES3.txt`, every clean sweep disposed; then the
closing pass with its denominator. ***

State what you read versus what you took from this packet. A claim you could not check is reported as
UNCHECKED with the reason, never as fine.
