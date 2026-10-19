# Commit A confirm -- #564's stranded gate-6 census pins, landed alone before #567

Open your answer with the token ASTRA_CENSUS_CF_20261019, then ONE line: VERDICT: COMMIT | COMMIT WITH CHANGES | DO NOT COMMIT -- <one line>.

READ-ONLY.  This is a records and gate-pin check: does the unit below say only what is true, change only what it should, and match what the F2 pass agreed (land #564's census repair ALONE, before #567: EXPECT_PTY_PROBES 74 -> 75 with #567's probe absent, the promptless probe grandfathered)?  Name any wrong number, any line that does not belong, and anything missing.

## 1. The commit message (verbatim)
```
records: #564 left gate 6's readiness census stranded -- its promptless probe is grandfathered and the pty pin re-derived, on their own; three rows filed

#564 (e7fc97e6) committed sgi_mte_decline_probe.py, a PROMPTLESS pty probe (fixed waits, no
readiness read), and moved neither of gate 6's censuses: EXPECT_PTY_PROBES stayed 74 and the
probe was in neither the grandfathered list nor the prompt-detecting set.  Gate 6 runs only in
the weekly battery, so this week's battery would have reddened it.  #567 found it re-deriving its
own pins: tools/derive_hygiene_pins.sh read 76 against 74 and 44 against 43, and --write refused.

* gate_hygiene.sh: the probe is grandfathered by derive_hygiene_pins.sh --grandfather (the
  2026-09-19 precedent: converting a probe's readiness is its own round), the list's comment names
  the fourth block and its provenance, and EXPECT_PTY_PROBES is 75 -- derived with #567's probe
  moved out of the tree, all eight censuses equal to their pins;
* FILED: ptyprobepins (MED), a precommit check so a commit cannot strand the pins again;
  sgimtereadiness (LOW), the probe's readiness conversion; batterystandby (MED), the 2026-10-18
  weekly battery that died in Modern Standby at ~18:13 (re-run by hand at 23:19: REGRESS_PASS 16/16).

Split from #567 at its pass 2's request (GPT-6 Astra, Grok 4.7, GLM 5.3), so this repair neither
rides in nor reverts with #567.  ledger.json, matrix.html, fable_queue.md, OUTSTANDING_BUGS.md,
CHANGELOG.md and gate_hygiene.sh only.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## 2. regress/gate_hygiene.sh, HEAD -> commit A (unified diff)
```diff
--- /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/cen/gate_hygiene_head.sh	2026-10-19 08:07:39.049675800 -0500
+++ /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/cen/gate_hygiene_commit.sh	2026-10-19 08:07:38.979928400 -0500
@@ -385,7 +385,7 @@
 #  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
 #  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
 #  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
-EXPECT_PTY_PROBES=74
+EXPECT_PTY_PROBES=75
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
 #
@@ -419,8 +419,9 @@
 sgi_de_width_probe.py sgi_re_unmapped_probe.py
 alpha_harness_probe.py alpha_pfnoffset_probe.py alpha_swpctx_v0_probe.py alpha_tbi_probe.py arm_bfx_width_probe.py landisk_aux_probe.py lca_badval_probe.py lca_confbus_probe.py lca_confwidth_probe.py lca_irqstub_probe.py lca_irqstub_uart_probe.py lca_isalane_probe.py lca_widewrite_probe.py maple_dmaaddr_probe.py pcc2_c040_probe.py sgi_mte_fill_probe.py sgi_re_colourdefault_probe.py sgi_re_randompixel_probe.py sgi_re_rgb_probe.py wdc_altdigin_probe.py
 arm_msrmode_probe.py lca_isaphys_probe.py
-crime_width_probe.py"
-#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended THREE blocks to the list above; they are
+crime_width_probe.py
+sgi_mte_decline_probe.py"
+#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended FOUR blocks to the list above; they are
 #  named here by their FIRST NAME, never by position, because the next --grandfather appends another.
 #  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 PROMPTLESS pty probes committed
 #  between 2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
@@ -433,9 +434,16 @@
 #  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
 #  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
 #  principle): crime_width_probe.py (#529), hidden from this census by a comment until pass 2 stopped the
-#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three are UNTRACKED and lying
+#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three were UNTRACKED and lying
 #  in the tree, named so the census passes on
-#  the tree the weekly battery runs.  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
+#  the tree the weekly battery runs.  (2026-10-18: crime_width_probe.py was committed by 7440e129 and
+#  arm_msrmode_probe.py by 4f908ad5; lca_isaphys_probe.py still lies untracked.)  The block beginning
+#  `sgi_mte_decline_probe.py` (2026-10-18, #567): #564 (e7fc97e6) committed that promptless probe -- fixed
+#  waits, no readiness read -- and moved neither census, so this gate would have reddened at the next battery;
+#  #567, adding its own pty probe, could not re-derive its pins while it stood, because --write refuses a
+#  promptless probe that is neither grandfathered nor prompt-detecting.  Grandfathered on the 2026-09-19
+#  precedent; converting its readiness is its own round.
+#  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
 #  `--grandfather NAME...` / `--release NAME...`, then `--write`.
 
 #  *** THIS WAS THE THIRD POPULATION AND THE F2 EDIT MISSED IT.  Found by the agy seat
```

## 3. The deriver's report on commit A's tree (#567's probe moved out of regress/ while it ran, then restored md5-verified)
```
census                                got pinned
EXPECT_BARE                             0      0
EXPECT_UNKNOWN                          0      0
EXPECT_PTY_PROBES                      75     75
promptless vs GRANDFATHERED            44     44
EXPECT_CONVERTED (anchor)              25     25
EXPECT_CONVERTED (echo)                25     25
EXPECT_CONVERTED (fresh mark)          25     25
EXPECT_WHOLE_FULL                       3      3
WHOLE_FULL_FILES                   got    [arm_bdt_probe.py:1 arm_flags_probe.py:2]
                                   pinned [arm_bdt_probe.py:1 arm_flags_probe.py:2]
UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):
  lca_isaphys_probe.py
DERIVE_DONE
```

## 4. The CHANGELOG block (verbatim)
```
# Records, 2026-10-19: `#564` left gate 6's readiness census stranded -- its promptless probe is grandfathered and the pty pin re-derived, in a commit of its own; three rows filed

**The defect.**  `#564` (`e7fc97e6`, 2026-10-18 03:57) committed `regress/sgi_mte_decline_probe.py`, a PROMPTLESS pty
probe -- fixed waits (a 1.5 s settle, 0.22 s between commands), no readiness read -- and moved neither of gate 6's
censuses: `EXPECT_PTY_PROBES` stayed 74 and the probe was in neither the grandfathered list nor the prompt-detecting set.
Gate 6 (`regress/gate_hygiene.sh`) runs only in the weekly battery, so nothing said so; this week's battery would have
reddened it.  `#567`, re-deriving its own pins with `tools/derive_hygiene_pins.sh`, found it: the pty census read 76
against 74 (its own probe and this one), the promptless census 44 against 43, and `--write` refused while the probe stood
neither grandfathered nor prompt-detecting.

**What this commit does.**  Only `#564`'s half, so that its attribution, and a revert of `#567`, stay separate -- the
order GPT-6 Astra, Grok 4.7 and GLM 5.3 each asked for in `#567`'s pass 2:
* `regress/gate_hygiene.sh` -- `sgi_mte_decline_probe.py` is appended to the grandfathered list by
  `derive_hygiene_pins.sh --grandfather` (the 2026-09-19 precedent: grandfathered, not converted -- converting a probe's
  readiness is its own round), the list's comment names the fourth block and its provenance, and `EXPECT_PTY_PROBES`
  moves 74 -> 75.  Derived with `#567`'s probe moved out of the tree: all eight censuses equal their pins.  The comment
  also corrects "All three are UNTRACKED" -- `crime_width_probe.py` was committed by `7440e129` and `arm_msrmode_probe.py`
  by `4f908ad5`; `lca_isaphys_probe.py` still lies untracked and is counted as it lies (the 2026-09-23 "count all" ruling).
* FILES `ptyprobepins` (MED): a commit adding a pty probe can strand these pins with only the weekly battery to notice --
  the third instance (`#500`'s probe; the 24 of the 2026-09 drift); the landing spot is a precommit check, and its design
  question is that a precommit sees the STAGED tree while the pin counts the WORKING tree.
* FILES `sgimtereadiness` (LOW): convert `sgi_mte_decline_probe.py`'s fixed waits to a readiness read.
* FILES `batterystandby` (MED): the 2026-10-18 18:00 weekly battery died at ~18:13 when the laptop changed power source
  and entered Modern Standby (gate 3 of 16; no verdict; the task's last result 0x8007042B), and nothing re-ran it --
  `tools/nightly_battery.sh` holds no wake request.  Re-triggered by hand at 23:19, it passed: REGRESS_PASS, 16/16,
  `_scratchpad/nightly/verdict_20261018_231924.txt`.  The remedy is an owner decision about the machine's power policy.

`ledger.json`, `matrix.html`, `fable_queue.md`, `OUTSTANDING_BUGS.md`, `regress/gate_hygiene.sh` and this block only.
```

## 5. The OUTSTANDING_BUGS.md section (verbatim)
```
### 2026-10-19 -- `#564`'s stranded gate-6 census: the promptless probe grandfathered, the pty pin re-derived; three rows filed

* **Gate 6's readiness census, repaired in a commit of its own.**  `#564` (`e7fc97e6`) committed
  `regress/sgi_mte_decline_probe.py` -- promptless, fixed waits -- and moved neither `EXPECT_PTY_PROBES` nor the
  grandfathered list, so the next battery's gate 6 would have gone red.  `sgi_mte_decline_probe.py` is grandfathered by
  `tools/derive_hygiene_pins.sh --grandfather` (the 2026-09-19 precedent) and `EXPECT_PTY_PROBES` is 75, derived with
  `#567`'s probe moved out of the tree.  Found by `#567`'s pin re-derivation; split out at its pass 2's request (GPT-6
  Astra, Grok 4.7, GLM 5.3), so that `#564`'s repair does not ride in, or revert with, `#567`.
* **`ptyprobepins` (MED, open)** -- a commit adding a pty probe can strand gate 6's pins, and only the weekly battery
  sees it; the third instance.  Owed: a precommit section that runs the deriver in report mode and refuses a tree that
  leaves a census off its pin, forward-only and controlled both ways -- and a decision on which tree it judges (the
  STAGED tree, or the WORKING tree the pin counts under the 2026-09-23 "count all" ruling).
* **`sgimtereadiness` (LOW, open)** -- `sgi_mte_decline_probe.py`'s fixed waits want a readiness read (its own round).
* **`batterystandby` (MED, open)** -- the 2026-10-18 weekly battery died at ~18:13 in Modern Standby after a
  power-source change (gate 3 of 16, no verdict, task result 0x8007042B) and nothing re-ran it; the runner holds no wake
  request.  Re-triggered by hand at 23:19: REGRESS_PASS 16/16 (`_scratchpad/nightly/verdict_20261018_231924.txt`).  The
  remedy -- a wake request for the run's duration, or a DC power-policy change -- is the owner's to choose.
```

## 6. The three ledger rows it files
```json
{
 "id": "ptyprobepins",
 "sev": "MED",
 "opened": "2026-10-18",
 "state": "open",
 "witness": "none",
 "commits": "",
 "title": "A commit that adds a pty probe can leave gate 6's readiness-census pins stale, and only the weekly battery sees it: #564 (e7fc97e6) committed sgi_mte_decline_probe.py -- promptless -- and moved neither EXPECT_PTY_PROBES nor the grandfathered list, so the 2026-10-18 battery would have reddened gate 6 (instances before it: #500's probe, and the 24 probes of the 2026-09 hygienecensus drift)",
 "state_note": "filed 2026-10-18 by #567, which found it while re-deriving its own pins: tools/derive_hygiene_pins.sh reported the pty census 76 vs its pin 74 and the promptless census 44 vs 43, and refused --write while sgi_mte_decline_probe.py stood neither grandfathered nor prompt-detecting.  #567 grandfathered it on the 2026-09-19 precedent and wrote the pins.  The landing spot is STRUCTURAL: a precommit section that runs the deriver in report mode and refuses a commit whose tree leaves a census off its pin -- forward-only, controlled both ways (a pty probe added without its pin reds; with it, greens).  The design question it owes: the precommit sees the STAGED tree while the pin counts what lies in the WORKING tree (owner ruling 2026-09-23, 'count all'), so the check must be defined against one of them."
}
{
 "id": "sgimtereadiness",
 "sev": "LOW",
 "opened": "2026-10-18",
 "state": "open",
 "witness": "none",
 "commits": "",
 "title": "regress/sgi_mte_decline_probe.py (#564) is a PROMPTLESS pty probe -- fixed waits (settle 1.5 s, 0.22 s between commands), no readiness read -- grandfathered by #567 so gate 6 stays green; converting its readiness is its own round",
 "state_note": "filed 2026-10-18 by #567 (gate_hygiene.sh's fourth grandfather block names it, with its provenance).  Fixed waits are load-sensitive: on a slow host a command can be sent before the debugger prompt returns.  Same disposition as the 20 probes grandfathered on 2026-09-19 (their block begins `alpha_harness_probe.py')."
}
{
 "id": "batterystandby",
 "sev": "MED",
 "opened": "2026-10-18",
 "state": "open",
 "witness": "none",
 "commits": "",
 "title": "The weekly battery dies when the laptop enters Modern Standby: on 2026-10-18 a power-source change at 18:13 put the machine into Modern Standby during gate 3 of 16, the scheduled task's process was terminated (last result 0x8007042B), the verdict file holds START only, and nothing re-ran it -- tools/nightly_battery.sh holds no wake request",
 "state_note": "filed 2026-10-18 by the main loop (087a90) from the System log (Kernel-Power 105 and 506 at 18:13:18-26) and the dead run's log, _scratchpad/nightly/battery_20261018_180001.log, whose last write is 18:12:10.  The WSL VM survived (up since 2026-10-16); the Windows-side driver did not.  The active plan's AC standby is `never' and its DC standby 180 s, so this bites only off AC.  Re-triggered by hand the same night.  The remedy is an OWNER decision about the machine's power policy -- a wake request held for the run's duration, or a DC policy change -- not a round's."
}
```

## 7. Pretests on the unit (precommit sections H, O, I, L, R and C)
```
STAGE_PANELS_PASS / BOILERPLATE_PASS (0 new) / FABLE_QUEUE_PASS / ATTRIBUTION_PASS 0 hard 4 soft / PROBEWIRING_PASS 77/85 / section C path hits: none
```
