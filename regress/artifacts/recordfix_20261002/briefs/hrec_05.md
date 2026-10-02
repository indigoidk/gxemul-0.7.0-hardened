HARNESS RECORD CORRECTIONS, part 05 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_05_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing.  The tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`), and ignore any other `src/` under the project root.

**Context.**  A review of this project's regression harness (its gate scripts, probes and checkers under `regress/`
and `tools/`) found comments and records that say something false or out of date.  Each such finding was ruled
RECORD: nothing is wrong with the code, the SENTENCE is wrong, and a replacement sentence was written.  The
corrections will be made in place, file by file, in later rounds.  Before a sentence can be replaced, somebody has to
find the text it replaces in the committed file and say whether it is still there.  That is this job.  The line
numbers in the dispositions are an older commit's (`db8b1a33`); the files have moved since, so find the text by what
it SAYS.

**For each disposition below, ONE line:**
`<key> | <path>:<first line>-<last line> at 7440e129 | STILL SAYS IT / ALREADY CORRECTED / NOT FOUND | CURRENT: "<the sentence or comment as it stands now, verbatim, at most 300 characters>" | FITS / DOES NOT FIT: <why>`
* `STILL SAYS IT`: the false or stale statement the disposition describes is present.  Quote it exactly as it stands
  (comment markers and all), so that a script can find it.
* `ALREADY CORRECTED`: the place now says what the replacement says, or the statement is gone.  Quote what stands there.
* `NOT FOUND`: you could not find the statement in the file the disposition names.  Say where you looked.
* `DOES NOT FIT`: the replacement sentence would itself be false at `7440e129`, or it describes another place.  Say
  which, with `path:line`.  Your agreement is not what is wanted: a replacement you cannot check against the source is
  `FITS: NOT CHECKED`, never a plain `FITS`.

End with `DENOMINATOR: <a> of 18 dispositions looked up in the committed file`.

**The dispositions** (key | the governing line, cut at 640 characters; where a replacement sentence is quoted in it,
that is the sentence that should stand):
1. hcheckprobewiring:F15 | hcheckprobewiring:F15 | draft said RECORD “…30 rows…every row from a measured mutant kill” | should be RECORD “#498 sgidewidth — 30 rows, including controls, run by gate_arm.sh.” | `regress/sgi_de_width_probe.py:247-256` includes liveness/device-signature controls; `regress/gate_arm.sh:1387-1389` pins 30. Both controls remain green across every committed `gxdew_t2_*` leg under `regress/artifacts/sgidewidth/opus_witness_20260831/`, lines `2-3`. | high
2. hcheckprobewiring:F16 | hcheckprobewiring:F16 | RECORD | RIGHT | RECORD "FOUR False results, so the DENOMINATOR STAYS 22 and the run FAILS." | tools/pipeline/check_probe_wiring.py:103,3228-3233,3433-3440
3. hcheckprobewiring:F17 | hcheckprobewiring:F17 | RECORD | RIGHT | RECORD "case(\"M9  dropping gate_arm from GATES unwires its detectors\", 1," | tools/pipeline/check_probe_wiring.py:3367-3371, regress/gate_arm.sh:1-1400
4. hcheckprobewiring:F18 | hcheckprobewiring:F18 | RECORD | RIGHT | RECORD "It reddens because the nested probe is keyed under its bare basename rather than its manifest relative path." | tools/pipeline/check_probe_wiring.py:2885-2899,3418-3431
5. hdiffdiskimageio:F2 | 3 | CONCEDE: RECORD | HOLD: NEW LOW diskionegwriteproof -- Concede. `regress/diff_diskimage_io.c:1530-1531` wants write result 0. `src/disk/diskimage.c:1595-1599` returns 0 for `offset < 0`. With that conjunct removed, `:1256-1260` returns 0 on `my_fseek` failure and `:1653-1658` returns 0, so `:1531` stays green on the fseeko path (`:97`). `:1526-1527` goes red for the same removal, because a short read returns 1 at `:1660`. On the `HACK_FSEEKO` path `:76-95` a negative `SEEK_SET` returns success, and the write check can fail. The fseeko write line's `[PROOF]` claim is the sentence.
6. hdiffdiskimageio:F5 | hdiffdiskimageio:F5 | RECORD | RIGHT | RECORD "Early sections assert return values; later sections assert buffer contents. [PROOF] rows pass on the corrected tree." | regress/diff_diskimage_io.c:11-14,24-27,370-385,840-845,980-990
7. hdiffdiskimageio:F6 | hdiffdiskimageio:F6 | RECORD | RIGHT | RECORD "ROW P, ROW U and ROW Z do NOT: they are green pre-fix by design, while ROW S fails pre-fix." | regress/diff_diskimage_io.c:260-266,710-769, src/disk/diskimage.c:1416-1445,1627-1628
8. hdiffdiskimageio:F7 | hdiffdiskimageio:F7 | RECORD | RIGHT | RECORD "a fix that only stops the loop early greens the first and leaves the second at 0 (the continuing defect left 712)." | regress/diff_diskimage_io.c:380-386
9. hdiffdiskimageio:F8 | hdiffdiskimageio:F8 | RECORD | RIGHT | RECORD "ROW Z -- AN EMPTY OVERLAY, REACHING lenread == 0 AT ITERATION 1 (ROW S ALSO REACHES lenread == 0 AT ITERATION 3)." | regress/diff_diskimage_io.c:480-492,710-769
10. hdiffdiskimageio:F9 | hdiffdiskimageio:F9 | draft said RECORD “…frees heap memory to prevent resource leakage across tests” | should be RECORD “Closes the base and overlay streams and frees the overlay array between fixtures.” | `regress/diff_diskimage_io.c:237-248` performs that partial cleanup; it does not free the individual names allocated at `src/disk/diskimage.c:139`. The replacement should avoid implying complete cleanup. | medium-high
11. hdiffdiskimageio:F10 | hdiffdiskimageio:F10 | RECORD | RIGHT | RECORD "Overlay DATA: 4096 bytes of 'V' for this fixture; real production R: overlays start at 0 bytes and grow on demand." | regress/diff_diskimage_io.c:796-798, src/disk/diskimage.c:2180-2216
12. hdiffdiskimageio:F11 | hdiffdiskimageio:F11 | draft said RECORD “Earlier past-capacity rows…aim well past the boundary…” | should be RECORD “Some earlier past-capacity rows use far-out offsets, such as LBA 2048 and LBA 1,000,000; those examples cannot distinguish the boundary defects addressed here.” | `regress/diff_diskimage_io.c:1052,1171,1185` supports those examples, but `:1230,1245` places the earlier full-store write exactly at the first unbacked block. The categorical generalization remains false. | high
13. hdiffdiskimageio:F12 | hdiffdiskimageio:F12 | RECORD | RIGHT | RECORD "2^32 and 0 are EQUAL in their low 32 bits, so a comparator narrowed to int treats them as equal; the wide probe catches this narrowing, while the small probe catches unconditional true." | regress/diff_diskimage_io.c:1733-1766
14. hdifffootbridge:F2 | hdifffootbridge:F2 | RECORD | RIGHT | RECORD "Offline differential for dev_footbridge; footbridge_sites_probe.py provides complementary CATS probe detector without OS boot." | regress/diff_footbridge.c:7-11; regress/footbridge_sites_probe.py:293-303; regress/gate_arm.sh:1072-1085
15. hdifffootbridge:F4 | hdifffootbridge:F4 | RECORD | RIGHT | RECORD "Forked to contain narrower conditional zero-load mutants; unconditional zero-load divide terminates unforked at D2 earlier." | regress/diff_footbridge.c:310-319, 381-387; regress/gate_offline.sh:566-575
16. hdiffieeestore:F6 | hdiffieeestore:F6 | RECORD | RIGHT | RECORD "Change-set includes S gradual underflow (both signs) and D subnormals (dD > 0); update header and lines 476/490." | regress/diff_ieee_store.c:20-28, 286-295, 476, 490, 1289-1295
17. hdiffieeestore:F7 | hdiffieeestore:F7 | RECORD | RIGHT | RECORD "These rows PIN the documented accepted-nearest band (the operand guard at 2^-969 / IEEE_DIR_OPTINY);" | regress/diff_ieee_store.c:835-843; src/core/float_emul.c:824
18. hdiffm8820x:F3 | hdiffm8820x:F3 | RECORD | RIGHT | RECORD "Masking low 6 bits clears BATC_V, failing translation rows such as F1." | regress/diff_m8820x.c:800-808, 910-915; src/include/thirdparty/m8820x_pte.h:93-98; src/cpus/memory_m88k.c:156-158
