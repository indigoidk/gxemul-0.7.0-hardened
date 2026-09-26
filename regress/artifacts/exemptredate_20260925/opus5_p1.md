OPUS550P1_ALIVE

**VERDICT: SHIP WITH CHANGES.** The re-date removes the 09-28 cliff and should land before that date. Four of its reason lines are wrong or misleading, the ieee_store date lands on another cliff, and nothing enforces "no two alike".

**What I ran:** a scratch `git archive` of HEAD (`tools/`, `regress/*.py|*.sh`) with the three edit550 scripts applied, plus a WSL `/tmp/opus550` copy of `build/gxemul`. My regenerated checker diff matches `diff550_cpw.diff`. I wrote nothing under the project.

1. **Q2: a one-digit edit passes everything (measured).**
   - Change lca_widewrite `"2026-10-22"` to `"2026-10-21"`. The checker passes on 09-25, `--selftest` gives 22/22 (M5a/M5b still derive from 10-08), and gate 2 never reads this table. On 10-22 two entries then expire together (3 to 5 problems).
   - Changing ip30's `"2026-10-08"` to `"2026-19-08"` also passes 22/22, because DATE_RE only checks the shape. ip30 then expires on 2027-01-01, keyed on a string that is not a date.
   - Gate 2's helper has the same gap: `wdc_identify:2026-19-27` gives `none` on 09-28.
   - Fix: either add a check (parse each date with `fromisoformat`, fail on a repeated detector date, two mutants, pin 22 to 24), or state in the header that nothing enforces distinct dates.

2. **The ieee_store date joins an existing cliff (measured).**
   - All twelve AB_EXEMPT entries in `gate_asan_sweep.sh` (gate 9, same battery) are dated 2026-11-30. That file's own comment calls this an unconfirmed placeholder.
   - After #550, 13 of the tree's 25 dated exemptions fall on that day. Running both helpers for 12-01: gate 2 reports ieee_store, gate 9 reports 12 of 12 expired.
   - "Falls due as its own decision" is false. Pick another day.

3. **"Six inline counters" is an undercount (measured).**
   - ieee_store's DIFF_PASS requires nine counters to be zero: abs_bad, unexplained, missed, inrange_diff, rm_rn_bad, rm_rz_bad, rm_d_bad, rm_vec_bad, interp_bad. Eight nested counters feed into them.
   - The six carried over from the old comment leave out the three S-format sweep counters (unexplained, missed, inrange_diff), and gate 2 checks each of those as its own row.
   - The date's reasoning still holds, since the refactor is bigger than stated. The count should say how it was derived.

4. **ppc_rldicl: the parked repair is real but only touches dead code (measured).**
   - No row calls want_rldimi, want_rlwinm, want_rlwimi or mask32, or uses the RLDIMI/RLWINM/RLWIMI encoders, at HEAD or in the working tree.
   - I ran the HEAD probe and the parked probe on the same binary: 24/24 each, with identical rows.
   - So "the RESULT/CONTROL protocol follows that repair" only reflects that the same file is dirty; there is no real dependency. The 09-24 ruling's list of parked work does not name this file either.
   - The oracles that matter for rldimi/rlwimi are the sibling probes, and `gate_ppc.sh` already scores them with exactly this protocol.
   - The comment the diff leaves in place, "could only score its exit status", is also false. The probe exits 0 on every completed run, and it prints ok/FAIL rows, `SCORE n/m` and DONE, so a gate can score it by rows (the mk48 case).

5. **ip30 (read and measured).**
   - "Binary-only" is true: it runs `-V -x -E sgi -e ip30` on an 8-byte dummy. But it doesn't set ip30 apart: the four Alpha/LCA probes have the same shape and already print `*_RESULT`/`*_DONE`.
   - The comment the diff re-wraps keeps the command `grep -ln "E sgi|-e ip30" gate_*.sh`. As written it matches nothing (rc=1, because `|` is a literal character in basic regex). Even with `-E` it cannot see machines chosen inside probes.
   - HEAD's `gate_arm.sh` already runs seven `-V -x -E sgi -e ip32` probes. So "no gate … could host it today" is false, and it contradicts the new "cheapest" line.
   - The real reason ip30 can go first: `dev_sgi_ip30.c` has no parked change, while `dev_lca.c` carries #540's.
   - It is not cheap in gate time. On a copy of `build/gxemul` it took **568 s wall for 33/33** (CONTROL=OK). No session sends `quit`, so each surviving session waits out a 12 s poll. Its tick rows also need `step 65536` to finish inside a 2.85 s read window. By comparison, ppc_rldicl ran 24/24 in under a second.

6. **Alpha/LCA: one missing home is true, but the spacing doesn't help (read).**
   - No gated probe uses `-E alpha`; gate 5 drives only luna88k and landisk, and gate 9 only constructs machines.
   - All four depend on one prerequisite. If that slips, 10-21 to 10-24 bring four commit-blocking expiries in a row, all the same decision. That is a bulk push under another name.
   - The ruling says to stagger by each entry's owed work. Give alpha_tbi a lead of about a week, or state that the four are one decision.

7. **Q4 (measured).**
   - No path blocks a commit: precommit reads neither gate 2's lists nor battery verdicts, `check_optpin` passes, and `bash -n` is clean.
   - It can hide a red. Both entries share one gate row, so if #551 slips, ieee_store's 12-01 expiry lands in a row that is already red and changes nothing visible.
   - The 09-27 battery will be green, because the entry is valid on its own date. The first scheduled run that shows wdc_identify red is 10-04.

8. **How it gets committed (measured).**
   - The checker on disk still has ten `"2026-09-27"` dates plus the parked MANIFEST. Run read-only today, it fails with 79 GHOST errors.
   - Precommit section R runs that on-disk file, not the staged blob.
   - Apply `edit550.py` to the on-disk copy as well. Otherwise, staging that file wholesale (#549's line lives in it) brings the cliff back, silently if done before 09-28.

9. **Smaller points (read).**
   - "Shared with the 4bit sibling": the sig probe also imports `wdc_altoffset_probe`.
   - The four wdc entries name no queue row anywhere.
   - The #520 paragraph still sits above the ppc block rather than above alpha_tbi.
   - "Six exemptions remain" is still in the present tense.

---
*Recorded by the main loop: agent a8c6fd47a6c9c37ac, `agent_models.py` = clean, opus-5-5 throughout.  Its scratch was not
under the project and is not preserved; the measurements are restated here as the seat reported them.  Finding 2 was
confirmed by the main loop before this record was written: `grep -c 2026-11-30 regress/gate_asan_sweep.sh` = 13.*
