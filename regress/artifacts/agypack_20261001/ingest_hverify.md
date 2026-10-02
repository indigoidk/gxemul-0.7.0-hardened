## hverify -- the harness review's findings, re-verified by agy beside the codex fallback

| job | agy VERDICT | agy rows parsed | codex rows parsed | status disagreements | draft-kind disagreements |
|---|---|---|---|---|---|
| hverify_07 | 45 right, 0 wrong, 0 unsettled of 45 findings -- 6 cannot-fai | 45 of 45 | 45 | 0 | 0 |
| hverify_09 | 44 right, 0 wrong, 0 unsettled of 44 findings -- 6 cannot-fai | 44 of 44 | 44 | 0 | 0 |
| hverify_11 | 69 right, 0 wrong, 0 unsettled of 69 findings -- 4 cannot-fai | 69 of 69 | 69 | 1 | 2 |
| hverify_12 | 27 right, 0 wrong, 0 unsettled of 27 findings -- 5 cannot-fai | 27 of 27 | 27 | 0 | 0 |
| hverify_13 | 47 right, 1 wrong, 0 unsettled of 48 findings -- 9 cannot-fai | 48 of 48 | 48 | 2 | 0 |
| hverify_14 | 48 right, 1 wrong, 0 unsettled of 49 findings -- 10 cannot-fa | 49 of 49 | 49 | 2 | 2 |
| hverify_15 | 23 right, 0 wrong, 0 unsettled of 23 findings -- 1 cannot-fai | 23 of 23 | 23 | 1 | 1 |
| hverify_16 | 51 right, 0 wrong, 0 unsettled of 51 findings -- 6 cannot-fai | 51 of 51 | 51 | 2 | 0 |
| hverify_17 | 24 right, 0 wrong, 0 unsettled of 24 findings -- 0 cannot-fai | 24 of 24 | 24 | 1 | 0 |
| hverify_18 | 7 right, 0 wrong, 0 unsettled of 7 findings -- 0 cannot-fail  | 7 of 7 | 7 | 0 | 0 |
| **total** | | 387 | 387 | 9 | 5 |

### Every disagreement, both lines

* **hverify_11 hcheckprobewiring:F12** (STATUS): agy RIGHT / draft RECORD ; codex UNSETTLED / draft RECORD 
  * agy: hcheckprobewiring:F12 | RECORD | RIGHT | RECORD "alphatbinegsel (#520) table 3: the CLOSING 15-row instrument, matching the oracle logic of shipped regress/alpha_tbi_probe.py" | tools/pipeline/check_probe_wiring.py:1382-1383, regress/artifacts/alphatbinegsel/killtable_20260910/t3/alpha_tbi_probe.frozen.py, regress/alpha_tbi_probe.py
  * codex: hcheckprobewiring:F12 | RECORD | UNSETTLED: the byte-identity assertion exists, but the required frozen artifact is outside the permitted artifact list. Its alleged 28,008/29,269-byte sizes, historical mismatch, and oracle equivalence were not checked. A permitted comparison of both HEAD blobs and the shipping-commit pair would settle it. | DROP "Defer the proposed record correction until the required frozen-blob com
* **hverify_11 hbundle_tools2:F2** (DRAFT): agy RIGHT / draft NEW MED; codex RIGHT / draft FILED-BY-PROSE 
  * agy: hbundle_tools2:F2 | STATUS-LAUNDERED | RIGHT | DRAFT: NEW MED adjudcontentcheck "adjudicate.sh size-only check counts long OLLAMA_SEAT_ERROR or recovered thinking as answered" | tools/adjudicate.sh:103-107, tools/panel_ollama.py:106-125
  * codex: hbundle_tools2:F2 | STATUS-LAUNDERED | RIGHT: nonempty-file and size ≥800 are the complete answer predicate. Preserved thinking or a sufficiently long OLLAMA_SEAT_ERROR therefore earns answer credit without an answer. | FILED-BY-PROSE OUTSTANDING_BUGS.md:10878-10888, describing the size-credit mechanism without naming this adjudicate instance | tools/adjudicate.sh:103-107; tools/panel_ollama.py:106-150
* **hverify_11 hdiffdiskimageio:F2** (DRAFT): agy RIGHT / draft NEW LOW; codex RIGHT / draft RECORD 
  * agy: hdiffdiskimageio:F2 | CANNOT-FAIL | RIGHT | DRAFT: NEW LOW diskionegwriteproof "Negative-offset WRITE proof returns zero via fseek failure without negative-offset guard" | regress/diff_diskimage_io.c:1522-1532, src/disk/diskimage.c:1256,1595,1653-1658
  * codex: hdiffdiskimageio:F2 | CANNOT-FAIL | RIGHT on the normal fseeko path: with the negative guard removed, length 512≤10,240 and offset −4,096≤9,728 pass the remaining bound; failed seeking returns lendone=0, and 0<512 makes the short-write check return 0. The guarded version also returns 0. The adjacent READ distinguishes guard removal. | RECORD "[CONTROL] WRITE at a NEGATIVE offset is refused" | regress/diff_diskimage_i
* **hverify_13 hgatehygiene:F3** (STATUS): agy WRONG / draft DROP ; codex RIGHT / draft NEW MED
  * agy: hgatehygiene:F3 | SELECTS-NOTHING | WRONG: no nested readiness_predicate_test.py exists in repo, and find exclusion correctly filters root test | DROP "overstated hypothetical; no nested readiness_predicate_test.py exists in repo, and find exclusion correctly filters root test" | regress/gate_hygiene.sh:151-153
  * codex: hgatehygiene:F3 | SELECTS-NOTHING | RIGHT: recursive exclusion by basename removes both the root truth-table file and a nested file with the same basename. The companion check reads only the root path; a nested helper without a PTY literal also contributes nothing to the PTY census. | DRAFT: NEW MED hygienenestedtest "Truth-table basename exclusion also exempts nested helpers" | regress/gate_hygiene.sh:151-153,454-46
* **hverify_13 hgatehygiene:F5** (STATUS): agy RIGHT / draft NEW MED; codex UNSETTLED / draft NEW MED
  * agy: hgatehygiene:F5 | SELECTS-NOTHING | RIGHT | DRAFT: NEW MED hygieneartifactlive "blanket ! -path artifacts/* hides live promptless PTY probe gdrom_pio_null_probe.py from census" | regress/gate_hygiene.sh:454-470, regress/gate_sh_rounding.sh:1019-1024
  * codex: hgatehygiene:F5 | SELECTS-NOTHING | UNSETTLED: invocation and artifact exclusion are confirmed. The claimed PTY creation and promptless implementation are not checked because that artifact source is outside the permitted list. Permitted committed evidence of those properties would settle the full claim; this draft remains conditional. | DRAFT: NEW MED hygieneartifacts "Live artifact probe omitted from the readiness c
* **hverify_14 hgateshrounding:F4** (STATUS): agy RIGHT / draft FILED ; codex UNSETTLED / draft FILED 
  * agy: hgateshrounding:F4 | CANNOT-FAIL | RIGHT: [regress/gate_sh_rounding.sh:470](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_sh_rounding.sh#L470), :1063, :1125, :1195 check `gdrom map` rows converting any `0x...` readback to `"mapped"`; unmapped memory returns `0x0`, converted to `"mapped"`, so unmapped device passes; already filed | FILED gdrommappedvacuous | [regress/gate_sh_rounding.sh:470](file:///C:/Do
  * codex: hgateshrounding:F4 | CANNOT-FAIL | UNSETTLED: three checked producers convert `0x0` to `mapped`, accepting both registered-device zero and unmapped-read zero. All four gate locations exist, but the fourth producer lies under a forbidden artifact path and was not checked. Inspecting its committed predicate would settle the exact four-control assertion. | FILED gdrommappedvacuous | regress/gdrom_data_probe.py:167–169,1
* **hverify_14 hgdromdefaultprobe:F3** (STATUS): agy WRONG / draft DROP ; codex RIGHT / draft NEW MED
  * agy: hgdromdefaultprobe:F3 | CANNOT-FAIL | WRONG: on the committed test kernel at HEAD, destination address `DMA_DST_P1` contains `0xea` (`0xffffffea`), not `0x10` ([regress/gdrom_default_probe.py:1360-1372](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L1360-L1372)); omitting the DMA copy returns `0xffffffea`, failing the check against `0x10`; the finding's premise assumes an external hypot
  * codex: hgdromdefaultprobe:F3 | CANNOT-FAIL | RIGHT under the stated KERNEL precondition: destination memory is not initialized by this session; only `r4` is poisoned with `0x5a`. Initial destination `0x10` becomes `0x10` with a copy and remains `0x10` without it. Preserving announcement, event, and idle updates preserves the other acceptance results. | DRAFT: NEW MED gdromacceptseed "DMA movement check depends on an uniniti
* **hverify_14 hgateoffline:F5** (DRAFT): agy RIGHT / draft FILED ; codex RIGHT / draft NEW LOW
  * agy: hgateoffline:F5 | OTHER | RIGHT: `exempt_expired` at [regress/gate_offline.sh:1225-1234](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_offline.sh#L1225-L1234) matches dates via `[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]` and compares `d < today`, so calendar-invalid `2026-09-99` passes and sorts into future; `${e##*:}` also extracts after last colon; calendar validation is already filed | FILED exemptca
  * codex: hgateoffline:F5 | OTHER | RIGHT: `2026-09-99` matches the digit-only shape and sorts after `2026-09-28`, so the result is `none`. For `ieee_store:garbage:2099-01-01`, membership extracts `ieee_store`, expiration extracts `2099-01-01`, and the intervening component is unchecked. | DRAFT: NEW LOW offexemptparse "Offline exemptions accept impossible dates and extra components" | regress/gate_offline.sh:1215–1235,2335–23
* **hverify_14 hgdromcondprobe:F3** (DRAFT): agy RIGHT / draft NEW HIGH; codex RIGHT / draft FILED 
  * agy: hgdromcondprobe:F3 | STATUS-LAUNDERED | RIGHT: [regress/gdrom_cond_probe.py:421-423](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L421-L423) (`R1b`) and [:499-502](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L499-L502) (`R2b`) test only `m.group(1)` matching `"aa"` and `"01"` without inspecting `how` or `alive`; an abnormal exit following diagnostic output pa
  * codex: hgdromcondprobe:F3 | STATUS-LAUNDERED | RIGHT: `session()` captures termination as `how`, but R2b grades only capture `01`; diagnostic `01` followed by `exit1` passes. R1b likewise ignores status; R3/R4 count a diagnostic without proving completion of their repeated stores. Final success uses the resulting row booleans. | FILED ptywaitstatus | regress/gdrom_cond_probe.py:173–178,224–233,413–428,496–508,1017–1021; src
* **hverify_15 hm88kroundingprobe:F6** (STATUS): agy RIGHT / draft RECORD ; codex UNSETTLED / draft RECORD 
  * agy: hm88kroundingprobe:F6 | RECORD | RIGHT | RECORD "This tree implemented four to six of each (fdiv 4, fadd 5, fmul 5, fsub 6), with #306 adding the twelve missing forms." | regress/m88k_rounding_probe.py:184-190; src/cpus/cpu_m88k_instr.c:2634-2830 (commit 0fc81c5e)
  * codex: hm88kroundingprobe:F6 | RECORD | UNSETTLED: Current `#306` annotations corroborate the finding: untagged fdiv={00,01,05,15}, four cases; tagged additions={04,10,11,14}, four cases. Untagged fadd={00,01,05,11,15}, five; fsub={00,01,05,10,11,15}, six; fmul={00,01,05,11,15}, five. The exact pre-correction snapshot was not checked. Reading the parent and diff of `0fc81c5e` would settle historical provenance. | DRAFT: REC
* **hverify_15 hlcaisalaneprobe:F4** (DRAFT): agy RIGHT / draft FILED ; codex RIGHT / draft FILED-BY-PROSE 
  * agy: hlcaisalaneprobe:F4 | OTHER | RIGHT | FILED wiringcliff | regress/lca_isalane_probe.py:611; tools/pipeline/check_probe_wiring.py:2665; OUTSTANDING_BUGS.md:13702,20476-20478
  * codex: hlcaisalaneprobe:F4 | OTHER | RIGHT: The battery’s gate list supplies no invocation; the regression-shell reference is a hygiene census entry. The wiring checker explicitly exempts this detector through 2026-10-27 and names its future gate. Its ungated state is already recorded in prose. | DRAFT: FILED-BY-PROSE OUTSTANDING_BUGS.md:20476-20480 | regress/run.sh:10,82-95; regress/gate_hygiene.sh:407-429; tools/pipeline/
* **hverify_16 hpcc2widthprobe:F1** (STATUS): agy RIGHT / draft NEW LOW; codex UNSETTLED / draft NEW LOW
  * agy: hpcc2widthprobe:F1 | CANNOT-FAIL | RIGHT | DRAFT: NEW LOW pcc2iplrdvacuity "IPL wide-read check cannot fail against pre-fix code" | regress/pcc2_width_probe.py:1340-1343, src/devices/dev_pcc2.c:681-710
  * codex: hpcc2widthprobe:F1 | CANNOT-FAIL | UNSETTLED: the current rows check `exit0`, RAM sentinel `0x5a5a5a5a`, and zero `DECL` matches; they do not require the IPL read-body diagnostic. The historical executable guard and exact warning are not checked. An authorized pre-fix source read would settle the claimed verbatim reinstatement. | DRAFT: NEW LOW pcc2iplreadoracle "IPL read rows do not distinguish the legacy width warn
* **hverify_16 hprecommitcheck:F11** (STATUS): agy RIGHT / draft NEW LOW; codex UNSETTLED / draft NEW LOW
  * agy: hprecommitcheck:F11 | CANNOT-FAIL | RIGHT | DRAFT: NEW LOW hookctlzeropass "precommit check B hook controls accept 0 of 0 controls as pass" | tools/precommit_check.sh:1155-1161
  * codex: hprecommitcheck:F11 | CANNOT-FAIL | UNSETTLED: the consumer demonstrably accepts `0 of 0 controls pass`, `0 wrong`, and `HOOKCTL_DONE`, because the parsed count is display-only. Whether emptying CASES makes the actual producer emit those values and exit zero is not checked: its artifact file is outside the permitted list. Authorized inspection of that producer would settle the full claim. | DRAFT: NEW LOW pchookcount
* **hverify_17 hsgirecolourdefaultprobe:F4** (STATUS): agy RIGHT / draft RECORD ; codex UNSETTLED / draft RECORD 
  * agy: hsgirecolourdefaultprobe:F4 | RECORD | RIGHT | RECORD "and M39 measures it at 74/77 territory rather than a sweep." | [regress/sgi_re_colourdefault_probe.py](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/sgi_re_colourdefault_probe.py#L668-L688)
  * codex: hsgirecolourdefaultprobe:F4 | RECORD | UNSETTLED: Source says both THREE failing rows and “76/77 territory”: `77−3=74`, whereas `77−76=1`. The claimed historical `74/77` measurement is not checked because its raw report and score file are outside the permitted artifact list. Source cannot establish the observed readbacks where the altered path permits an uninitialized-buffer store. Authorized inspection of those meas

### Agreed-NEW rows where the two seats grade differently: 30

involving a HIGH on either side: 7
* hverify_07 hbundle_regress28:F1: agy HIGH, codex MED
* hverify_09 hbundle_regress32:F4: agy HIGH, codex LOW
* hverify_11 hcheckprobewiring:F3: agy LOW, codex HIGH
* hverify_13 hdiffwdcidentify:F1: agy LOW, codex HIGH
* hverify_13 hdiffwdcidentify:F3: agy HIGH, codex MED
* hverify_13 hgatehygiene:F6: agy HIGH, codex LOW
* hverify_13 hgatehygiene:F7: agy MED, codex HIGH

### NEW HIGH drafts (either seat)

* hverify_07 hbundle_regress28:F1: agy NEW HIGH; codex NEW MED
* hverify_09 hbundle_regress32:F4: agy NEW HIGH; codex NEW LOW
* hverify_09 hbundle_regress33:F10: agy NEW HIGH; codex NEW HIGH
* hverify_09 hbundle_regress33:F5: agy NEW HIGH; codex NEW HIGH
* hverify_09 hbundle_regress33:F8: agy NEW HIGH; codex NEW HIGH
* hverify_09 hbundle_regress33:F9: agy NEW HIGH; codex NEW HIGH
* hverify_11 hcheckprobewiring:F3: agy NEW LOW; codex NEW HIGH
* hverify_12 hdifffootbridge:F1: agy NEW HIGH; codex NEW HIGH
* hverify_12 hdiffm8820x:F2: agy NEW HIGH; codex NEW HIGH
* hverify_13 hdiffwdcidentify:F1: agy NEW LOW; codex NEW HIGH
* hverify_13 hdiffwdcidentify:F3: agy NEW HIGH; codex NEW MED
* hverify_13 hgatehygiene:F6: agy NEW HIGH; codex NEW LOW
* hverify_13 hgatehygiene:F7: agy NEW MED; codex NEW HIGH
* hverify_14 hgdromcondprobe:F3: agy NEW HIGH; codex FILED 
* hverify_15 hhpcmipsctorprobe:F2: agy NEW HIGH; codex NEW HIGH
* hverify_17 hsgideprimopprobe:F2: agy NEW HIGH; codex NEW HIGH
