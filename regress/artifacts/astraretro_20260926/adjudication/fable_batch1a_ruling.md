VERDICT: 29 of 30 dispositions kept as written, 1 changed.

PROVENANCE (agent_models.py, 2026-09-26): the dispositions BELOW the line were written by claude-opus-4-8 after two
refusals by claude-fable-5-1 (a silent fallback -- NOT a seat answer on their own).  The Fable seat then reviewed them
FIRST-HAND on its resumed agent (claude-fable-5-1 wrote fable_batch1a_firsthand.md and the final text): 29 kept as
written, 1 changed (devsh4:F1 sh4tmupending LOW -> MED).  The combined ruling is the first-hand review plus the kept
dispositions.

===== fable_batch1a_firsthand.md (claude-fable-5-1) =====
VERDICT: 29 of 30 dispositions kept as written, 1 changed.

First-hand engineering re-review of fable_batch1a.md (HEAD 8ea26abb), read as a plain correctness review of the emulator source. Severity scale as instructed: HIGH = the emulator process terminates or memory use leaves a buffer's bounds; MED = guest-visible behaviour differs from the hardware manual; LOW = records, diagnostics, test coverage.

CHANGED
devsh4:F1 | was CONFIRMED-NEW LOW sh4tmupending | now CONFIRMED-NEW MED sh4tmupending | src/devices/dev_sh4.c:527 (`timer_interrupts_pending[i]++`, unsaturated), :604-607 (DEVICE_TICK re-asserts and re-sets TCR_UNF while pending > 0, with no test of tstr), :2148-2151 (one TCR ack decrements by one). Two underflows before one acknowledgment yield two delivered interrupts, and a stopped timer with residual pending keeps re-asserting; the manual (sh7750_hardware.txt:20741-20755, :21037) defines UNF as a single status bit cleared by writing 0. That is guest-visible behaviour differing from the manual, so MED on the scale regardless of the in-comment note at :518-525 that the queue-vs-coalesce choice was "recorded rather than decided." The signed-overflow half (~226 days) stays latent and does not change the grade.

KEPT (29)
devwdc: F1 wdcpktstatus, F2 wdcbeoddtail, F3 wdcresetirq, F4 wdcsrstnoedge, F5 wdcaltdecode, F6 CONFIRMED-NEW MED wdcnien, F7 wdccylwrap, F8 RECORD-L4, F9 RECORD-L4, F10 RECORD-L4, F11 UNSETTLED, F12 RECORD-L4.
devdreamcastgdrom: F1 CONFIRMED-NEW HIGH gdromdmareentr, F2 RECORD-L4 (minor), F3 RECORD-L4, F4 RECORD-L4 (minor), F5 RECORD-L4, F6 RECORD-L4, F7 RECORD-L4, F8 RECORD-L4, F9 CONFIRMED-FILED.
devsh4: F2 RECORD-L4, F3 RECORD-L4, F4 RECORD-L4, F5 RECORD-L4, F6 UNSETTLED, F7 TEST-GAP-FILE sh4chcrdualdiag, F8 CONFIRMED-FILED M1_sh4latchleak, F9 CONFIRMED-FILED pcicmergeA.

Severity spot-checks on the kept new rows, first-hand:
- gdrom:F1 HIGH holds. dev_dreamcast_gdrom.c:1502-1503 writes d->data to a guest-chosen dst via memory_rw(PHYSICAL); with dst inside the device's own DMA window at +0x18, memory_rw.c:480/587 dispatches back into the same handler, the arming words (+0x0c, +0x14) and d->data are unchanged, and the call repeats without bound. Unbounded recursion terminates the process. No in-flight guard exists.
- wdc:F6 MED holds. nIEN is never read; INTRQ is asserted with nIEN set, contrary to ATA-2 :1311-1314. Guest-visible, not a bounds or termination issue.
- gdrom:F2 and F4 are kept as L4 but are the two weakest rulings in the file (precision of comment wording, not behaviour); I would not object to either being dropped by the confirming seat.

THE TWO L2 OBLIGATIONS -- are their rows absent from the committed probes at HEAD?
- M2_gdromnodatawidth: YES, absent.
  grep: `git grep -n -E 'row\("(nodata byte|accept byte)"' HEAD -- 'regress/*.py' 'regress/*.sh'` -> no match (rc=1). The only hits in all of regress/ are
  `HEAD:regress/artifacts/stateaudit_20260923/diffs/regress_gdrom_default_probe.py.diff:210` and `:294` -- a diff artifact of uncommitted work, not the live probe. The committed gdrom_default_probe.py has only `arm bytetrig` (:1096), which drives the arming arm, not the no-data completion arm.
- M1_sh4latchleak: YES, absent.
  Committed sh4_chcr_probe.py:572-574 drives X4a (channel 1) and X4b (channel 7) with `wr(addr, x, ...)` -- a single store each -- and `grep -n -E 'two_stores\(.*(SH4_CHCR1|SH4_CHCR7)'` returns nothing (rc=1). Only X3 (:550) repeats a request, on channel 0. The (1,set) and (7,set) cells named at CHANGELOG:2903 have no row.
Both were graded L2 in the CHANGELOG (#496 pass, :2896-2909), i.e. repair-in-round, and neither repair is in committed HEAD. That is an undischarged obligation, not a test-gap, and should be surfaced as such.

===== fable_batch1a.md (claude-opus-4-8 fallback; ratified above except devsh4:F1) =====
VERDICT: 3 confirmed-new, 9 confirmed-filed, 15 record-L4, 1 test-gap, 0 refuted, 2 unsettled, 0 duplicate, of 30 findings

FABLE_RETRO_1a_ALIVE_0926

CHECKPOINT.md first line, verbatim:
`# CHECKPOINT -- 2026-09-26 09:02 (087a90 sections rewritten; the peer's sections below are untouched)`

ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 1a. HEAD `8ea26abb`. Every disposition below was
checked against `git show HEAD:<path>` (extracted copies), the cited manuals, the cited probes, and
`OUTSTANDING_BUGS.md`/`CHANGELOG.md`/`ledger.json` at HEAD. Late-dissent rule applied: closure
changes the licence, never the truth-value.

================================================================================
JOB devwdc (src/devices/dev_wdc.c) -- 12 findings
================================================================================

devwdc:F1 | CONFIRMED-FILED wdcpktstatus
  dev_wdc.c never reads `atapi_st->status` (grep: zero `->status` in the file); backend returns 1 for
  CHECK CONDITION (diskimage_scsicmd.c:216/777/807 set status[0]=0x02 but the transfer still returns
  data_in). Filed OB:15582 (also :464, :19348), MEDIUM. Exists at HEAD.

devwdc:F2 | CONFIRMED-FILED wdcbeoddtail
  BE read arm dev_wdc.c:1209 `odata = (odata << 8) + wdc_get_inbuf(d)`; wdc_get_inbuf() returns
  (uint64_t)-1 on an empty ring (:303), so the last valid byte becomes v-1. Filed OB:15573 (also
  :459), MEDIUM. Exists at HEAD.

devwdc:F3 | CONFIRMED-FILED wdcresetirq
  wdc_new_command_reset() (dev_wdc.c:915-924) clears atapi/write/ring only; it does NOT clear
  int_assert, error, or deassert the IRQ. ATA-2 :1316-1318 (SRST clears pending interrupt) confirmed.
  Filed OB:12820. Exists at HEAD.

devwdc:F4 | CONFIRMED-FILED wdcsrstnoedge
  No held-reset state: dev_wdc.c:832-835 acts on the WDCTL_RST edge and never records "reset asserted";
  status never reports BSY (WDCS_BSY is set nowhere, per :1091-1094) and commands still execute. ATA-2
  :1589 and :3938-3945 confirmed. Filed OB:12556. Exists at HEAD.

devwdc:F5 | CONFIRMED-FILED wdcaltdecode
  DEVICE_ACCESS(wdc_altstatus) (dev_wdc.c:609+) has no `if (!d->io_enabled)` guard; only
  DEVICE_ACCESS(wdc):1176 does. OB:12848 finding 3 files exactly this ("io_enabled checked in
  DEVICE_ACCESS(wdc) only"). Filed OB:12835. Exists at HEAD.

devwdc:F6 | CONFIRMED-NEW MED wdcnien "wdc models no nIEN: completion IRQs are asserted even when the guest set nIEN"
  WDCTL_IDS (nIEN) is read nowhere in dev_wdc.c; every asserting arm (incl. #485's :1110-1111 and
  :1155-1156) sets int_assert unconditionally. ATA-2 :1311-1314 requires INTRQ high-Z when nIEN=1. The
  #485 comment (:1086-1089) is HONEST ("the model has no interrupt-disable state ... as nIEN-blind as
  the ten arms that already assert"), so it is not a record defect; but the gap is device-wide and has
  no queue row. #533 (OB:21797-21798) notes "does NOT implement nIEN" and files wdcrstbitonly, not
  nIEN. No `wdcnien` in OB/ledger. NEW; scope is the whole device, not just #485.
  Checked: dev_wdc.c:1086-1089,1110,1155; OB:21797; grep wdcnien -> 0.

devwdc:F7 | CONFIRMED-FILED wdccylwrap
  dev_wdc.c:338-339 writes cyls>>8 / cyls with no clamp; diskimage.c:290-297 gives H=S=1 on 32MiB ->
  65536 cylinders -> word 1 = 0. Filed OB:15589 (also :469, :19372), LOW->MED. Exists at HEAD.

devwdc:F8 | RECORD-L4 "The smallest size at which any byte diverges is 65,280 sectors. Since #414's `-d gH;S` override, H=S=1 on a 33,423,360-byte image gives EXACTLY 65,280 sectors, so that count IS reachable (it was unreachable only before #414, when diskimage_recalc_size()'s whole-cylinder round-up on the default 16/63 geometry could not produce it). The smallest divergence under the DEFAULT geometry remains 33,546,240 bytes (65 cylinders), where a 32 MB disk announces itself as 120 KB."
  dev_wdc.c:402-407 still says "that exact count is unreachable"; CHANGELOG:27979-27982 already records
  it as time-indexed/reachable since #414 (`-d g1;1` on a 33,423,360-byte image). Source comment stale.
  Checked: dev_wdc.c:402-407; CHANGELOG:27977-27982; diskimage.c:290-297,2022-2026.

devwdc:F9 | RECORD-L4 "atapi_len counts only what the DATAIN arms pushed. Before #495 a guest data-port WRITE mid-DATA-IN grew inbuf_head without touching atapi_len; #495 (:1576, `atapi_phase != PHASE_CMDOUT`) now REFUSES that push and #484 (:245) bounds every push, so the write-injection route is closed. The shared ring still feeds the CDB-dispatch and disk-drain paths; the residue described here can no longer be created by a mid-DATA-IN write. Tracked as `wdcaddtoinbufbound`, which OB:11591 records as FALSE/repaired since #484."
  dev_wdc.c:1373-1423 (#473 comment) still says the write arm "pushes guest bytes with no phase guard
  and no capacity check ... the live unbounded route." Both guards now exist (:1576 phase, :245
  capacity); OB:11591 marks wdcaddtoinbufbound FALSE since #484. Source comment stale.
  Checked: dev_wdc.c:245,1373-1423,1576; OB:11591.

devwdc:F10 | RECORD-L4 "`wdc_command(ATAPI_PKT_CMD)` sets PHASE_CMDOUT; a following command now calls wdc_new_command_reset() at the top of wdc_command() (:938), which zeroes atapi_phase -- so the phase is reset by every command since #479, and also by an SRST via the ALT-CTRL arm (:832-834 -> :917). Both conjuncts of the dispatch guard remain, but the stale-phase scenario this paragraph describes no longer arises; whether the flag conjunct is still load-bearing at HEAD should be re-measured. And `atapi_cmd_in_progress` is cleared by wdc_new_command_reset() (:917) on the NEXT command AND on an SRST, not only by the next command."
  dev_wdc.c:1660-1682 says "NOTHING RESETS THE PHASE" and "cleared only when the NEXT command does."
  Both false at HEAD: wdc_new_command_reset (:917-918) zeroes both, called from wdc_command:938 and
  from the SRST arm:834. Source comment stale.
  Checked: dev_wdc.c:832-834,915-924,938,1660-1682.

devwdc:F11 | UNSETTLED "Build the flag-only push-guard mutant at dev_wdc.c:1576 (`atapi_cmd_in_progress` in place of `atapi_cmd_in_progress && atapi_phase != PHASE_CMDOUT`) on HEAD and observe: does it produce a use-after-free (the #495 comment's claim, `re-arms #477's objection in full`) or merely block legitimate CDB collection (Astra's claim)? The dispatch/free at :1716-1734 requires phase==PHASE_CMDOUT, so occupancy 12 reached during DATA-IN does NOT dispatch, which is what makes this a measurement rather than a reading."
  Astra's static point (occupancy 12 also occurs during DATA-IN) does not itself show a false claim,
  because the dispatch guard already requires CMDOUT; but whether a flag-only push guard re-creates the
  #477 free at HEAD or only blocks CDB is not decidable by reading. #477 measured a flag-based guard
  creating a free historically; the current guard structure may differ. Needs the mutant.
  Checked: dev_wdc.c:1531-1544,1576-1578,1716-1734.

devwdc:F12 | RECORD-L4 "A guest MODE SELECT can set logical_block_size to any value in [256, 8192], but NOT through dev_wdc.c: the backend's `case SCSICMD_MODE_SELECT:` needs a completed 12-byte DATA OUT (diskimage_scsicmd.c:1287-1291 returns 2 requesting it), which the wdc model never supplies -- its DATA OUT phase is unimplemented (dev_wdc.c:1803-1818 latches warned_atapi_dataout and never resumes the command), and #495 declines DATA-OUT-phase pushes. The `(total_size+511)/512` dismissal therefore holds for every IDE/ATAPI image; only the word `always` was too strong in principle."
  CHANGELOG:27774-27777 (in the #408 block, header :27709) still says "dev_wdc.c reaches that path for
  ATAPI." The correcting parenthetical exists 76 lines away at CHANGELOG:27851-27855 (in the #407
  block) -- so the correction was ADDED elsewhere and the original left standing, and OB:15598's claim
  it was "corrected in place" is only half-true. Same "fixed the copy, left the original" pattern.
  Checked: CHANGELOG:27774-27777,27851-27855; dev_wdc.c:1803-1818; diskimage_scsicmd.c:1287-1327; OB:15598.

================================================================================
JOB devdreamcastgdrom (src/devices/dev_dreamcast_gdrom.c) -- 9 findings
================================================================================

devdreamcastgdrom:F1 | CONFIRMED-NEW HIGH gdromdmareentr "guest-aimed GD-ROM DMA into its own +0x18 trigger recurses unboundedly and exhausts the host stack"
  dev_dreamcast_gdrom_dma_access case 0x18 (:1502-1503) does `memory_rw(dst, d->data, data_len, MEM_WRITE,
  PHYSICAL)` with dst = dma_reg[0x04/4] & 0x0fffffff (guest-set). If dst = 0x005f7418 (the DMA window's
  own trigger), memory_rw dispatches back into this handler with relative_addr=0x18 and idata = first
  bytes of d->data (nonzero for a staged TOC/sector); count(0x0c) and enable(0x14) are still armed and
  d->data is still non-NULL, so case 0x18 re-runs and calls memory_rw again -> unbounded recursion ->
  stack exhaustion/SIGSEGV. No in-flight guard; PHYSICAL bypasses translation, not device dispatch.
  Setup is ordinary register writes plus one prior successful command. NOT filed (gdromdmaxferflood
  OB:20069 is the unlatched `Transfering` diagnostic, a different defect; no reentr/recurs id exists).
  Checked: dev_dreamcast_gdrom.c:1379-1507,1676; memory_rw.c:436-524,587; grep gdromdmareentr/dmareentr -> 0.

devdreamcastgdrom:F2 | RECORD-L4 (minor) "#462: prints d->data_len, the count STAGED for transfer (the memory_rw return is not checked, and a destination crossing a device-region boundary would move fewer). It printed `length` -- the guest's +0x08 register -- while the memory_rw below moves d->data_len, so the line lied in exactly the sessions where the two disagree."
  dev_dreamcast_gdrom.c:1493-1499 calls d->data_len "the count actually transferred," but the diagnostic
  prints BEFORE the memory_rw call (:1502) and the return is never checked; memory_rw truncates at a
  device boundary (memory_rw.c:495-524). The data_len-vs-length correction is right; "actually
  transferred" overstates. Minor.
  Checked: dev_dreamcast_gdrom.c:1493-1503; memory_rw.c:495-524.

devdreamcastgdrom:F3 | RECORD-L4 "Under `+`, `sum == all-ones` is NECESSARY but not SUFFICIENT for pairwise-disjoint-and-exhaustive one-bit masks: a sum-preserving non-one-hot redefinition escapes it (e.g. {1,2,4}->{1,1,5} keeps the sum while overlapping bit 0 and dropping bit 1). The one-bit-ness of each mask still rests on the `(1u << _B)` idiom, which the assert does not independently verify -- as the honest-limit note at :440-443 already states."
  dev_dreamcast_gdrom.c:422-424 claims a future edit that "abandons the idiom is caught," and :418-420
  claims "iff pairwise disjoint AND cover every bit." Astra's {1,1,5} counterexample refutes both, and
  the comment already half-admits it at :440-443, so the two passages contradict. Shipped masks are
  correct; the `+` form does catch enumerator-aliasing and multi-bit-superset edits it was built for.
  Checked: dev_dreamcast_gdrom.c:404-443,498-502 (arithmetic: 1+1+5=7=1+2+4, 1|1|5=5).

devdreamcastgdrom:F4 | RECORD-L4 (minor) "The same guard here would have NO EFFECT: an unaligned access CAN reach this arm (dispatch checks the registered range, not word alignment), but nothing here is indexed by relative_addr except the bounds-guarded latch bitmap, so the guard would fire without changing any outcome -- unlike `if (off >= 0x100)`, which can never fire at all."
  dev_dreamcast_gdrom.c:1329-1333 calls the hypothetical alignment guard "DEAD CODE ... for exactly
  that reason [`can never fire`]." An alignment guard CAN fire on an unaligned access; it is redundant,
  not unreachable. The primary reasoning at :1325-1327 (no relative_addr-indexed tail) is sound. Minor.
  Checked: dev_dreamcast_gdrom.c:1319-1341; memory_rw.c:480-481.

devdreamcastgdrom:F5 | RECORD-L4 "The clause's accept-row obligation applies to predicates a guest store can feed; this predicate tests the ACCESS WIDTH against a compile-time constant. All four de-fatalised predicates now carry rows: `accept d0`/`accept d1` and the 204 good reads in `overread` carry the two read predicates, the busy mask and data_len, and `accept w8` (gdrom_data_probe.py:420) carries the width predicate, proving six 8-bit stores still assemble and dispatch."
  dev_dreamcast_gdrom.c:1033-1040 says the width predicate is EXEMPT and "the other three DO carry
  rows." At HEAD gdrom_data_probe.py:396-421 has `accept w8` for exactly this predicate (header
  :324-326 "`accept w8` carries the width predicate"). Comment stale.
  Checked: dev_dreamcast_gdrom.c:1032-1041; gdrom_data_probe.py:324-326,396-421.

devdreamcastgdrom:F6 | RECORD-L4 "Releasing both fields in one place makes the disagreeing state unreachable through the release paths, rather than merely unreached -- but NOT unrepresentable: the two fields stay independent, and alloc_data() sets the length before the pointer, so a transient disagreement remains representable (see the free_data() comment at src/devices/dev_dreamcast_gdrom.c:650-658)."
  CHANGELOG:16753 still says "unrepresentable"; the source free_data() comment (:656-658) explicitly
  retracts that overclaim, and alloc_data():643-645 sets data_len then mallocs. gdrompionull records
  it but says the changelog was corrected -- it was not (the source was). Stale CHANGELOG sentence.
  Checked: CHANGELOG:16753; dev_dreamcast_gdrom.c:641-666.

devdreamcastgdrom:F7 | RECORD-L4 "`d->warned` now has ELEVEN writers (six were pre-#489, plus TOCLEN, FMT, CMD, 88VAL, CONDVAL). Of the pre-existing six, LEN, NODATA and OVERREAD can latch on an ordinary guest READ; NOTWAIT is set only on a write, and the two DMA warnings (in the DMA handler) require a nonzero write to +0x18. A bit collision is therefore silenced by ordinary read traffic for those three."
  dev_dreamcast_gdrom.c:258-260 says "NINE writers ... SIX ... set from inside DEVICE_ACCESS by
  ordinary guest register reads." Counted 11 writers at HEAD (:736,817,916,1044,1056,1095,1121,1169,
  1288,1466,1522). #496 added 88VAL/CONDVAL after the "nine" was written. Only LEN/NODATA/OVERREAD are
  read-settable; NOTWAIT is write-only; DMANODATA/DMAARM are write-triggered in the DMA handler.
  Checked: dev_dreamcast_gdrom.c:258-268 and all eleven writer sites.

devdreamcastgdrom:F8 | RECORD-L4 "It changes the disposition of 65,127 of the 65,536 possible values, silently."
  dev_dreamcast_gdrom.c:714 says "65,527." Correct count of newly-honoured values under `< 408` is the
  set [409, 65535] = 65535-409+1 = 65,127 (cnt==408 was already accepted; [0,407] stay declined). The
  comment's number is wrong by 400. Frozen/wrong-number class.
  Checked: dev_dreamcast_gdrom.c:707-717; cnt domain [0,65535] via GDROM_CNTLO/CNTHI (:1190-1204).

devdreamcastgdrom:F9 | CONFIRMED-FILED gdromacceptdmanum (accept side) + M2_gdromnodatawidth (no-data side)
  `nodata byte` / `accept byte` rows exist at HEAD ONLY in the untracked-work diff
  artifacts/stateaudit_20260923/diffs/regress_gdrom_default_probe.py.diff and in old gate533.log; the
  committed gdrom_default_probe.py and gate_sh_rounding.sh do NOT contain them (`arm bytetrig` at
  :1096 is the DMA arming arm, not the no-data completion arm). The accept-byte half is filed
  gdromacceptdmanum (OB:20390, HIGH, clause-(b), in-work); the no-data-byte half is M2_gdromnodatawidth
  (CHANGELOG:2896-2909, graded L2). NOTE the M2 L2 obligation appears UNDISCHARGED at HEAD -- the row
  is not in the committed probe -- which is worth surfacing beyond a plain test-gap.
  Checked: gdrom_default_probe.py:1093-1097; git grep row("nodata byte"/"accept byte") HEAD -> only the
  diff artifact; OB:20390-20432; CHANGELOG:2896-2909; OB:20549-20553 (gdromcontractresidual).

================================================================================
JOB devsh4 (src/devices/dev_sh4.c) -- 9 findings
================================================================================

devsh4:F1 | CONFIRMED-NEW LOW sh4tmupending "unacknowledged SH4 timer underflows accumulate without bound in signed timer_interrupts_pending[]"
  sh4_timer_tick():527 does `timer_interrupts_pending[i]++` per underflow (up to 110/s) with no
  saturation; DEVICE_TICK():604-607 re-asserts and re-sets TCR_UNF while pending>0 regardless of the
  timer being stopped (tstr). Signed overflow at ~226 days is genuinely un-noted (practically
  unreachable). The queue-vs-flag divergence from the manual (:20741-20755: UNF is a status bit,
  cleared by writing 0) is ALREADY acknowledged in-comment at :518-525 ("recorded rather than
  decided"). LOW/latent; the fresh part is the unbounded signed accumulation. No sh4tmupending in OB.
  Checked: dev_sh4.c:474-529,603-607,2148-2153; sh7750_hardware.txt:20741-20755,21037.

devsh4:F2 | RECORD-L4 "CMF is never set: it is write-1-to-keep at :2377-2379, so a guest write cannot set it and the device never raises a compare-match. OVF has NO such handling -- a guest write stores it at :2381 and reads it back at :2383 -- so `OVF is never set on any path` is false for the guest-write path; what the device never does is GENERATE a compare-match/overflow to raise CMF or OVF, so RTCNT (which has no case) never produces one and a guest polling for a hardware-set flag waits forever."
  dev_sh4.c:454-457 says "CMF and OVF are never set on any path." RTCSR write (:2375-2383) special-cases
  only CMF (write-1-to-keep); OVF is stored unmasked and read back. CHANGELOG:24680 and OB:8534/8536
  repeat the false premise (note them too). (Deeper code angle, mine: letting a guest SET the OVF
  status bit via a plain write is itself arguably wrong vs write-0-to-clear hardware semantics.)
  Checked: dev_sh4.c:448-471,2361-2384; CHANGELOG:24680; OB:8534-8538.

devsh4:F3 | RECORD-L4 "PCR/RTCSR/RTCOR/RFCR (all `16bit` in sh4_bscreg.h) already accept any width and service it."
  dev_sh4.c:1600-1605 lists "PCR/RTCSR/RTCNT/RTCOR/RFCR." RTCNT has NO `case` in the device (verified:
  only RTCSR:2361, RTCOR:2386, RFCR:2394, PCR:2354 exist), so an RTCNT access falls to the default arm
  (:2824) and does not "accept any width and service it." Drop RTCNT from the list. The underlying
  RTCNT-unimplemented gap is filed sh4rtcflags (OB:8534/8536).
  Checked: dev_sh4.c:1600-1605,2354-2400,2824-2835; OB:8536.

devsh4:F4 | RECORD-L4 "`bits` is the OFFENDING bits, not the whole written value -- passing the value would report once per newly-set bit and give a per-(class,instance) ceiling of 32 lines instead of the tight per-feature bound the offending-bits form gives. The OR-and-mask makes even the whole-value form bounded (fresh = bits & ~reported), so this is about tightness, not about preventing an unbounded burn."
  dev_sh4.c:1691-1696 says passing the value "would make every distinct write look like a fresh
  complaint and hand a looping guest an unbounded host-CPU burn." sh4_val_first():1711-1712 ORs bits
  and returns fresh!=0, so at most 32 reports per (cls,inst) whatever the guest writes -- bounded, not
  unbounded. Comment overstates.
  Checked: dev_sh4.c:1689-1715.

devsh4:F5 | RECORD-L4 "SH4_VAL_RTCSRINT did not exist (NCLASS was 8, slots 0-7 used); reusing SH4_VAL_RCR1INT is measurably EQUIVALENT, not a collision -- RCR1's operand `idata & (CIE|AIE)` and RTCSR's `bsc_rtcsr & (CMIE|OVIE)` have disjoint bit supports (0x18 & 0x42 == 0) and sh4_val_first keys on bits. The class is kept separate for FRAGILITY (nothing enforces the disjointness), not because reuse would collide. See sh4latchcollide and dev_sh4.c:159-177."
  CHANGELOG:24626-24627 says "reusing SH4_VAL_RCR1INT would have collided." The round's own source
  comment (:159-177) and OB:8548-8557 record the correct conclusion (mutant EQUIVALENT, 10/10, bits
  disjoint). Stale CHANGELOG sentence stating the refuted premise as fact.
  Checked: CHANGELOG:24626-24627; dev_sh4.c:159-177; OB:8548-8557.

devsh4:F6 | UNSETTLED "Two questions. (1) Re-run the #459 repro writing 0x20 to TCR0 on a no-pclock machine and read back: if it reads 0x0, the CHANGELOG:18824 `0x0 versus 0x20` is a valid measurement of a 0x20 write (not a mis-transcription of the probe's 0x0001 readback rows) and that half is refuted. (2) Confirm no committed probe row polls TCNT (verified: sh_pclock_probe.py has zero TCNT accesses) -- the detector plants TCR stores plus a spin/step, so `plants exactly such a program [that polls TCNT]` is at most a loose wording nit, not a false behaviour claim."
  Part A (probe never accesses TCNT) is literally true but CHANGELOG:18813-18814 describes the generic
  baresh/testsh hang mechanism, and the detector does plant a TCR-program-then-wait program; "polls
  TCNT" is imprecise, not clearly false. Part B ("0x20") is not established as wrong -- a refused 0x20
  write reads back 0x0, a valid statement that need not match the probe's 0x0001 rows. Neither half is
  a clean confirmable false-behaviour claim from HEAD alone.
  Checked: CHANGELOG:18808-18825; sh_pclock_probe.py:80-93,240-379 (grep TCNT -> 0).

devsh4:F7 | TEST-GAP-FILE sh4chcrdualdiag "sh4_chcr_probe.py R7/L0 count only VAL_RE, so a mutant turning an RS-switch `return` into `break` (illegal RS + IE set -> decline PLUS a spurious IE_RE) would escape them; assert against both diagnostic families as X3/X4 do"
  sh4_chcr_probe.py:90-124 defines VAL_RE and IE_RE; `says()` returns VAL_RE only, `says_all()` both.
  R7 (:258-260) and L0 (:365-367) use the VAL_RE path; the RS default (dev_sh4.c:729-736) `return`s, so
  a `return`->`break` there would fall to the IE block (:785) and emit an extra IE_RE that R7/L0 do not
  count. Real coverage debt, above the vacuity floor. Not filed. LOW.
  Checked: sh4_chcr_probe.py:90-124,258-260,365-367,550-575; dev_sh4.c:648-657,729-737,785-793.

devsh4:F8 | CONFIRMED-FILED M1_sh4latchleak (CHANGELOG:2896-2903)
  X4a/X4b (sh4_chcr_probe.py:572-575) each issue ONE store; only X3 repeats a request, on channel 0.
  The per-channel ceiling for channels 1 and 7 (set state) is unobserved. Filed as M1_sh4latchleak,
  graded L2 (clause-(d) joint cell) at CHANGELOG:2896-2903. NOTE it has no distinct OB id and the L2
  repair looks UNDISCHARGED at HEAD (X4a/X4b still single-store), which is more than a test-gap and
  should be surfaced.
  Checked: sh4_chcr_probe.py:572-575; CHANGELOG:2896-2903; grep sh4latchleak OB -> 0.

devsh4:F9 | CONFIRMED-FILED pcicmergeA
  The third PCIC fault class (SH4_PCIC_NOCPU) diagnostic-independence has no assertion; P19
  (sh4_pcic_probe.py:734-751) checks readback in the PCICONF0 arm, P20 (:759-778) checks the
  (offset,class) latch. Filed pcicmergeA (OB:6989-6995), held pending a probe run after the third class
  landed. Exists at HEAD.
  Checked: sh4_pcic_probe.py:734-778; dev_sh4.c:1337-1359,1386-1417; OB:6989-6995.

================================================================================
(a) Astra CODE findings I could NOT confirm, and why
================================================================================
- devwdc:F11 (UNSETTLED). Astra's static observation (occupancy 12 also occurs during DATA-IN) does not
  demonstrate a false claim, because the dispatch/free at :1716-1734 already requires phase==CMDOUT.
  Whether a flag-only push guard re-creates the #477 free at HEAD or merely blocks CDB collection is a
  measurement (build the mutant), not a reading.
- devsh4:F6 (UNSETTLED). "polls TCNT" is a loose description of the generic hang, not a false behaviour
  claim (the detector spins/steps rather than polling TCNT); "0x0 versus 0x20" is plausibly a valid
  measurement of a 0x20 write and is not shown wrong from HEAD.
Everything else was confirmable from the source; the one HIGH CODE finding I could confirm as a real,
unfiled defect is devdreamcastgdrom:F1 (DMA self-target re-entrancy -> stack exhaustion).

================================================================================
(b) Findings Astra missed, that I noticed while checking (MINE)
================================================================================
- MINE, LOW/floodclass: DEVICE_ACCESS(sh4)'s default arm (dev_sh4.c:2824-2835) emits an UNLATCHED
  `fatal()` on any unhandled register in the 0xff000000+0x01000000 window (e.g. RTCNT at 0xff800020,
  which F3 shows has no case). fatal() has no -q early-out (debugmsg.c:384-390), so a guest kernel
  looping reads/writes there floods the host log unbounded -- the exact floodclass the file latches
  everywhere else (#443/#447/#459). It is `#ifdef SH4_DEBUG exit(1)` only, so not a crash in the
  shipped build. Proposed: file LOW under floodclass (verify it is not already implied by a floodclass
  row).
- MINE, code angle on devsh4:F2: OVF is guest-writable-and-readable through RTCSR (:2381) while CMF is
  write-1-to-keep protected (:2377-2379). Letting a guest SET a status bit that hardware sets only on
  overflow is a small behaviour divergence in its own right, beyond the record wording.
- MINE, on devsh4:F8 and devdreamcastgdrom:F9: both point at L2 obligations (M1_sh4latchleak;
  M2_gdromnodatawidth) recorded in CHANGELOG whose rows are absent from the committed probes at HEAD.
  If those were graded L2 (repair in-round), the repairs appear undischarged in committed HEAD -- worth
  an explicit status check rather than leaving them as test-gaps.

================================================================================
(c) DENOMINATOR
================================================================================
Checked against the source at HEAD: 30 of 30 findings. Every disposition rests on a file read
(`git show HEAD:` extracts of dev_wdc.c, dev_dreamcast_gdrom.c, dev_sh4.c, memory_rw.c, diskimage.c,
diskimage_scsicmd.c), the cited probes (gdrom_data_probe.py, gdrom_default_probe.py,
sh_pclock_probe.py, sh4_chcr_probe.py, sh4_pcic_probe.py), the cited manuals
(ata2_x3t10_948d.txt, sh7750_hardware.txt), and OUTSTANDING_BUGS.md / CHANGELOG.md / ledger.json at
HEAD. Zero ruled from Astra's text alone. Arithmetic re-derived by hand where a number was in dispute
(devdreamcastgdrom:F8 65,127; devdreamcastgdrom:F3 {1,1,5} sum/OR; devwdc:F7/F8 65,280 vs 65,536).
