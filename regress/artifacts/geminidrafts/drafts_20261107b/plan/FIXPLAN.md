# Gemini fix drafts for the oldest open rows -- state and handoff, 2026-11-07 06:3x (proposals for the Fable/Mythos adjudication)

Everything here is a PROPOSAL from one model (Gemini 4 Argon, web) that both drafted and reviewed (badge `s`, same-model).  Nothing
is in GXEMUL-SEC, est/ or a build tree.  Each fix still owes its round: reproduce per the witness ladder (rung-3 attempt), panel
pass 1, implement, pass 2, gates, records.

## Pipeline and counts (fixcheck_results.tsv, the compile clone at HEAD 8d9df658)

| step | tool | result |
|---|---|---|
| candidates | `mk_fixpacket.py --list` (FIX-NOW, cites `src/...:<line>`) + `mk_fixpacket_located.py` (names a file; line located by a SPECIFIC identifier) | 137 + 20 + the 2 earliest strays = 159 rows |
| draft | `fixdraft_worker*.sh` (WIDE +-120 for later batches) | |
| compile | `fixcheck_all.sh` (apply exactly-once, incremental build; **NO_EDITS** for an empty list -- an empty draft once scored BUILD_OK) | **111 BUILD_OK**, 48 SKIP (UNSETTLED/NO), 0 APPLY_FAIL |
| vacuity | `scan_commentonly.py` (code tokens unchanged = COMMENT_ONLY) | 0 vacuous; 3 COMMENT_ONLY are RECORD rows whose defect IS a comment (heldrecedits, i8259pollcomment, wdcatadocstale) |
| review | `mk_fixreview.py` (row + APPLIED.diff + every edited function IN FULL, post-edit -- the sketch rule) | current draft of all 111: **72 SOUND, 34 DEFECT, 5 UNSETTLED** (`FIXREVIEWS.md`; the UNSETTLED ones re-sent once with the definitions they named) |
| revise | `mk_fixrevise.py` -- ONE round, capped; HEAD functions + previous edits + the review; the drafter ACCEPTs/REJECTs each finding | first batch: 117 accepted / 35 rejected over 41 rows; later batches 7 + 7 rows |

**The 34 DEFECT verdicts are on drafts that already had their one revision** (or, for a few, on the revision itself): they are NOT
revised again.  Their findings are pointers for the adjudication.  Same-model review finds something nearly every time; a finding
can be wrong (one proposed an `info()` macro that does not exist in this tree).

## Rows that need a decision before any round

* **PEER-HELD FILES** (the Alpha/LCA session's holds -- draftable here, not landable without it): `palputslen`
  (cpu_alpha_palcode.c); `shrfcrkey` (dev_sh4.c).  `wdcatadocstale`'s row also names a comment in regress/gate_offline.sh (peer)
  and regress/diff_wdc_identify.c -- its draft fixes only the two dev_wdc.c comments (partial by scope).
* **HELD BACK**: `vr41xxgiuwidth` (not drafted -- the vr41 classifier history); `alphaifetchkill` and every lca*/alpha* row (the
  peer's, owner ruling 2026-10-07).
* **APPLY_FAIL -- cleared on the second (last) retry**: `ctorabortclass` now BUILD_OK (reviewed); `ppcbranch32width` UNSETTLED.
* **`ofemulnodata` -- a DESIGN question, not a draft defect**: redrafted 07:1x at the SHARED site (`of_emul()`,
  src/promemul/of.c:1099, which both the ARM and PowerPC decoders call) as a once-latched decline + `return 0`; it compiles.
  Its review says the row's own state note records a decoder-site design, and that `return 0` lets the guest continue
  with an unwritten result instead of FAULTING -- the option-set question (decline vs fault) for the adjudication.
* **UNSETTLED with a named gap** (8 from the missing-definitions pass, 6 after revision, others): each reply names the definition,
  function or file it could not see -- e.g. a header bitmask, a macro pair, a function's opening lines (each reply names it).

## Combining (Gemini planning pass, `grouping/reply.txt`) -- CANDIDATES under the round-scope rule

The rule: a round takes ONE site; a second joins only if WITNESSED, same device, same semantic class, same detector, no new oracle.
None of these drafts is witnessed yet, so these are candidate groups only:

1. `ppccrnandundec`, `ppcdcbiundec`, `ppc4xxcacheundec`, `ppcmtmsrlbit` -- cpu_ppc_instr.c undecoded instruction (split: mtmsr's
   L bit is a modifier of a decoded instruction)
2. `armclrexundec`, `armexregstop`, `armldrexbhdspin` -- cpu_arm_instr.c undecoded (split: ldrexbhd decodes to X(invalid))
3. `m88kcarryundec`, `m88kzeroword`, `m88kaluignored` -- cpu_m88k_instr.c `goto bad` (split: the zero word)
4. `mipsdsbranch`, `mipsllzero`, `mipsmuldivrd` -- cpu_mips_instr.c unsupported operand variants (split: delay-slot state)
5. `scsimodeselhdr`, `scsimodesensepc` -- diskimage_scsicmd.c unlatched guest-drivable `fatal()` (split: hex dump vs one line)
6. `armdacr2kill`, `armdesc3kill` -- memory_arm.c `fatal()+exit(1)` on translation (split: different detectors)

**CONFLICTS -- same function, landing one invalidates the other's `old` strings:** `pit8253lsbnotimer` / `pit8253flood`
(DEVICE_ACCESS(8253)); `mipscountrate` / `mipscountread` (DYNTRANS_RUN_INSTR_DEF).  Land one, then redraft the other at the new HEAD.

## Where the material is

`_scratchpad/gweb/jobs_20261106_kits/`: `fix_<row>/` (packet, reply, APPLIED.diff, every earlier version kept with a time stamp),
`rev_<row>/` (reviews; earlier rounds `*.r1_*`), `fixcheck_results.tsv`, `commentonly.tsv`, `FIXREVIEWS.md`, this file.
The 8d9df658 bank carries the bank-time subset; its "74 compile" is an L4 (67 real) queued for the post-#587 bank update.
