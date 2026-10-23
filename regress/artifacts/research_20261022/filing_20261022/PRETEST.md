# PRETEST.md -- the external-fixes research filing, pretested on SCRATCH copies of HEAD de8c7547 (2026-10-22)

Every checker below is HEAD's own file, copied by `git show HEAD:tools/pipeline/<f>` into `work/pre/chk/` and md5-checked against the blob before use (all 15 equal).  Nothing under `GXEMUL-SEC/` was written; git was used for object reads (`show`, `ls-tree`, `archive`) and, inside the checkers, `log` and `ls-files` through `GIT_DIR`.  Scripts, all under `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\research_file\work\`:

* `build_rows.py` -> `ledger_rows.json`; `build_ob.py` -> `ob_section.md`; `build_corrections.py` -> `corrections.md` (each OLD copied from the HEAD blob and counted: exactly once);
* `pre/pretest_build.py` -- parses the three deliverables AS WRITTEN (their fences and `ledger_ops`), applies them to `head/` (HEAD's blobs) and stages the trees; `pre/run_pretest.sh` -- runs the checkers; `pre/make_pretest_md.py` -- writes this file from the outputs in `pre/out/`.

## 1. Assembly, and the byte-for-byte writer proof

Command: `python -I pre/pretest_build.py`

```text
writer reproduces HEAD's ledger byte for byte: True (HEAD 2a184268, rewritten 2a184268, 9635837 bytes, CRLF 65253, trailing newline False)
section bullets: 126; lead ids == new ids: True; each exactly once: True
bullet severity == row severity for every row: True
new ids as code spans in the assembled OB: 117 exactly once; more than once: {'m88kbuserrregs': 3, 'm88kscaledbyte': 2, 'mipsprimundec': 2, 'ppc64xlateexit': 3, 'ppccrandcorc': 2, 'ppcdsformxo': 2, 'vr41xx1kpage': 2, 'wdclbaaddr': 2, 'x11cursorclip': 2}
new ids in HEAD's OB (any code span): 0
rows 941 -> 1067; OB lines 25203 -> 25665 (min 25665); CHANGELOG lines 36102 -> 36118 (min 36118); script-only edits not applied here: ['gateab_r1b']
guard on ctl_dupnew: ["duplicate id 'lermd3fcs' (2 rows)"]
guard on ctl_dupold: ["duplicate id 'letxrestart' (2 rows)", "new id 'letxrestart' already exists at HEAD"]
  base      ledger 2a184268  OB a7da7bb7  CHANGELOG 2d618316
  root      ledger e404fb5b  OB 3971f32b  CHANGELOG d1cec103
  root_min  ledger e404fb5b  OB 1888134a  CHANGELOG 3fe335b8
PRETEST_BUILD_DONE
```

The ledger writer is `json.dumps(L, ensure_ascii=False, indent=1).replace('\n', CRLF)` with no trailing newline; reading HEAD's blob and writing it back gives the same bytes (md5 above), so every difference in the assembled ledger is the filing.  The nine ids named more than once are the nine new rows the batch head entry lists (`m88kbuserrregs` also appears in the R2 correction, `ppc64xlateexit` twice in the head entry); each still has exactly one bullet.

## 2. The checkers, base (HEAD) and root (the filing applied)

Command: `bash pre/run_pretest.sh` (per tree, each checker runs from the tree's own `tools/pipeline/` with `GXLEDGER`/`GXQUEUE` pointing at that tree, `GIT_DIR` at the real repository, `GX_ARTIFACT_DIR` at the real `regress/artifacts/`).  The runner's index, verbatim:

```text
base.P_bugsync         rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
base.W_rowstates       rc=0  ROW_STATES_PASS  no open row names a committed detector
base.O_boilerplate     rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
base.H_stagepanels     rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
base.K_witness         rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
base.Q2_entrydomain    rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
base.I2_codexwall      rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
base.I_fablequeue      rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
base.L_attribution     rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
base.X_cited           rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
root.P_bugsync         rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
root.W_rowstates       rc=0  ROW_STATES_PASS  no open row names a committed detector
root.O_boilerplate     rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
root.H_stagepanels     rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
root.K_witness         rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
root.Q2_entrydomain    rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
root.I2_codexwall      rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
root.I_fablequeue      rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
root.L_attribution     rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
root.X_cited           rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
base.Q_dashboard       rc=0  wrote C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\research_file\work\pre\out\base.matrix.html (8112320 bytes, 763 in work + 154 closed, 9 seats)
root.Q_dashboard       rc=0  wrote C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\research_file\work\pre\out\root.matrix.html (8555076 bytes, 888 in work + 154 closed, 9 seats)
base.matrix.html == HEAD tools/pipeline/matrix.html: IDENTICAL
root.matrix.html: 8555076 bytes; rows named in it: m88kscaledbyte ppc601xlateexit pristinesecondref 
root_min.P_bugsync     rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
root_min.W_rowstates   rc=0  ROW_STATES_PASS  no open row names a committed detector
root_min.X_cited       rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
ctl_dropbullet.P       rc=1  BUGFILE_SYNC_FAIL  1 open row(s) filed after 2026-08-20 with no entry
ctl_dropbatch.P        rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
ctl_dupnew.P_bugsync   rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
ctl_dupnew.W_rowstates rc=0  ROW_STATES_PASS  no open row names a committed detector
ctl_dupnew.O_boilerplate rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
ctl_dupnew.H_stagepanels rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
ctl_dupnew.K_witness   rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
ctl_dupnew.Q2_entrydomain rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
ctl_dupnew.I2_codexwall rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
ctl_dupnew.I_fablequeue rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
ctl_dupnew.L_attribution rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
ctl_dupnew.X_cited     rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
ctl_dupold.P_bugsync   rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
ctl_dupold.W_rowstates rc=0  ROW_STATES_PASS  no open row names a committed detector
ctl_dupold.O_boilerplate rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
ctl_dupold.H_stagepanels rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
ctl_dupold.K_witness   rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
ctl_dupold.Q2_entrydomain rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
ctl_dupold.I2_codexwall rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
ctl_dupold.I_fablequeue rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
ctl_dupold.L_attribution rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
ctl_dupold.X_cited     rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
  MISSING   lermd3fcs        open     newest entry (no entries -- treated as NEW)
RUN_PRETEST_DONE
```

Section letters are `precommit_check.sh`'s: P `check_bugfile_sync.py`, W `check_row_states.py`, O `check_boilerplate.py`, H `check_stage_panels.py --list`, K `check_witness.py`, Q2 `check_entry_domain.py`, I2 `gen_codex_wall.py --check`, I `check_fable_queue.py`, L `check_commit_attribution.py`, X `check_cited_artifacts.py`, Q `gen_dashboard.py --out`.

### Selected full outputs

`base.P_bugsync`:

```text
  human queue, and CLAUDE.md names it as a first-stop-each-session file.

BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
```

`root.P_bugsync`:

```text
  human queue, and CLAUDE.md names it as a first-stop-each-session file.

BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
```

`root.W_rowstates`:

```text
  check_row_states: 773 open row(s) checked, 7 exempt by state_note
ROW_STATES_PASS  no open row names a committed detector
```

`root.K_witness`:

```text
check_witness: 103 closed-with-commits rows named a witness, 22 grandfathered (pre-2026-08-19), 0 missing, 0 malformed
WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
```

`base.K_witness`:

```text
check_witness: 103 closed-with-commits rows named a witness, 22 grandfathered (pre-2026-08-19), 0 missing, 0 malformed
WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
```

`root.H_stagepanels`:

```text
  ..    fiqenableread  assess    1/9  filed, not yet panelled
STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
```

`root.Q2_entrydomain`:

```text
entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
```

`root.I2_codexwall`:

```text
CODEX_WALL_OK  46 held stages, section matches the ledger
```

`root.I_fablequeue`:

```text
check_fable_queue: 7 held-and-queued, 0 stages short without a hold, 0 holds not queued, 0 closed rows owing a regress review
FABLE_QUEUE_PASS  every owed flagship job is either done or written down
```

`base.L_attribution`:

```text
  scanned 60 commits deep; 41 subject/row matches already attributed
  NEVER NAMED in any scanned subject, yet carry commits: 141 -- a1a2 alphapfnoffset alphaswpctxptbr alphaswpctxreg alphatbinegsel arcbiosubsan armbdt armbfxwidth32 asicbadaddr b115 carrier census constblind deadman diskimagesign divsweeplines es438 exemptcliff exitsweep fablequeue fbdiv fbpending fbsmlane fbwitness gate3scope gdromcondlies gdromdefault gdromdmadefault gdromdmawidth gdromexitsix gdrompionull gdromwarnbits heldmasked holdmarkermulti hookctlgate hookdurability hpcabort landiskaux landiskdisk lcabadval lcaconfbus1kill lcaconfwidth lcairqstubkill lcaisalane lcashiftub ledgerwitness lethalonly lunaabsentcpu m437ord m8820x m88kexcrrtrapmode m8batc m8invread m8online m8sarpurge mk48nvramkill mrwstore2 nineseatreminder novpadfourth ns16550 nulheredoc optrow ovsync panelargvcap panelseatlabel pcc2c040assertrow pcc2c040ctlq pcc2c040kill pcc2c040mienannounce pcc2defaultkill pcc2genctlc040alias pcc2widthkills pitclobber pitflip pitlatch pkbrief ppcrldiclzero ppcwitnessmaskoracle probetimebased probewiring propagatecpsilent r418 r419 r420 r421 rtcgate scoreclaimhex scorehyphenfp seatthinkburn selfcheckman selfmutant6 sgiarcbiosoob sgideprimop sgidewidth sgimtedepth4dead sgimtelabelcells sgirandompixel sgirergbroundtrip sgireunmapped sh4bcr sh4chcr sh4dmacie sh4gdromexit sh4iprbcd sh4irq15 sh4pcicexit sh4pclock sh4prio0 sh4prioraise sh4rtcsr sh4sci sh4tlbda2 sh4tlbmulti sh4valguards shortread smdatefmt smhang sqreadtype stagetokens tfreq verdictbold wdcaddtoinbufbound wdcaltctrlbit wdcaltdigin wdcaltoffset wdcatapistswap wdccdbmidxfer wdcdataoutdrain wdcflood wdcfloodstale wdcnoirq wdcoddstep wdcrearmzero wdcringambig wdcringnoflush wdcstalephase wdcwidth4 wdcwipclear widthkillclass witnessinvisible xfamscope
ATTRIBUTION_PASS  0 hard, 6 soft
```

`root.L_attribution`:

```text
  scanned 60 commits deep; 41 subject/row matches already attributed
  NEVER NAMED in any scanned subject, yet carry commits: 141 -- a1a2 alphapfnoffset alphaswpctxptbr alphaswpctxreg alphatbinegsel arcbiosubsan armbdt armbfxwidth32 asicbadaddr b115 carrier census constblind deadman diskimagesign divsweeplines es438 exemptcliff exitsweep fablequeue fbdiv fbpending fbsmlane fbwitness gate3scope gdromcondlies gdromdefault gdromdmadefault gdromdmawidth gdromexitsix gdrompionull gdromwarnbits heldmasked holdmarkermulti hookctlgate hookdurability hpcabort landiskaux landiskdisk lcabadval lcaconfbus1kill lcaconfwidth lcairqstubkill lcaisalane lcashiftub ledgerwitness lethalonly lunaabsentcpu m437ord m8820x m88kexcrrtrapmode m8batc m8invread m8online m8sarpurge mk48nvramkill mrwstore2 nineseatreminder novpadfourth ns16550 nulheredoc optrow ovsync panelargvcap panelseatlabel pcc2c040assertrow pcc2c040ctlq pcc2c040kill pcc2c040mienannounce pcc2defaultkill pcc2genctlc040alias pcc2widthkills pitclobber pitflip pitlatch pkbrief ppcrldiclzero ppcwitnessmaskoracle probetimebased probewiring propagatecpsilent r418 r419 r420 r421 rtcgate scoreclaimhex scorehyphenfp seatthinkburn selfcheckman selfmutant6 sgiarcbiosoob sgideprimop sgidewidth sgimtedepth4dead sgimtelabelcells sgirandompixel sgirergbroundtrip sgireunmapped sh4bcr sh4chcr sh4dmacie sh4gdromexit sh4iprbcd sh4irq15 sh4pcicexit sh4pclock sh4prio0 sh4prioraise sh4rtcsr sh4sci sh4tlbda2 sh4tlbmulti sh4valguards shortread smdatefmt smhang sqreadtype stagetokens tfreq verdictbold wdcaddtoinbufbound wdcaltctrlbit wdcaltdigin wdcaltoffset wdcatapistswap wdccdbmidxfer wdcdataoutdrain wdcflood wdcfloodstale wdcnoirq wdcoddstep wdcrearmzero wdcringambig wdcringnoflush wdcstalephase wdcwidth4 wdcwipclear widthkillclass witnessinvisible xfamscope
ATTRIBUTION_PASS  0 hard, 6 soft
```

`base.X_cited`:

```text
check_cited_artifacts: 59 citations checked at/after round 462, 14 grandfathered, 0 missing, 4 artifact-like mentions NOT in enforced citation form
CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
```

`root.X_cited`:

```text
check_cited_artifacts: 59 citations checked at/after round 462, 15 grandfathered, 0 missing, 4 artifact-like mentions NOT in enforced citation form
CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
```

## 3. Negative controls

* **ctl_dropbullet** -- the filing with ONE bullet removed from the 2026-10-22 section (`lermd3fcs`, a row named nowhere else in the bug file).  MUST red P, naming the row.

```text

  An OPEN row nobody can find by reading OUTSTANDING_BUGS.md is work a fresh
  session will not see. The ledger is the pipeline's truth; the bug file is the
  human queue, and CLAUDE.md names it as a first-stop-each-session file.

BUGFILE_SYNC_FAIL  1 open row(s) filed after 2026-08-20 with no entry
```

* **ctl_dropbatch** -- the same with a BATCH row's bullet removed (`m88kscaledbyte`).  Expected to stay GREEN, and that is the disclosed limitation: the head entry names the row as a code span, which P accepts as findable.  Recorded so nobody reads P as a per-bullet check for the nine batch rows.

```text
  human queue, and CLAUDE.md names it as a first-stop-each-session file.

BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
```

* **ctl_dupnew** -- the filing with one new row duplicated (`lermd3fcs` twice).  **ctl_dupold** -- one new row renamed to an EXISTING id (`letxrestart`).  The drafter's own guard refuses both (section 1: `guard on ctl_dup*`).  Every precommit checker's verdict on them is in the index above (`ctl_dup*.`), and section 4 says what that means.

`ctl_dupnew.P_bugsync`:

```text

BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
```

`ctl_dupnew.W_rowstates`:

```text
  check_row_states: 774 open row(s) checked, 7 exempt by state_note
ROW_STATES_PASS  no open row names a committed detector
```

`ctl_dupnew.K_witness`:

```text
check_witness: 103 closed-with-commits rows named a witness, 22 grandfathered (pre-2026-08-19), 0 missing, 0 malformed
WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
```

`ctl_dupnew.L_attribution`:

```text
  Those rows shipped work this check cannot see. It reads SUBJECTS, not diffs.
ATTRIBUTION_PASS  0 hard, 6 soft
```

`ctl_dupold.P_bugsync`:

```text

BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
```

`ctl_dupold.L_attribution`:

```text
  Those rows shipped work this check cannot see. It reads SUBJECTS, not diffs.
ATTRIBUTION_PASS  0 hard, 6 soft
```

## 4. What the duplicate-id controls show: NO precommit check catches a duplicate ledger id

Both duplicate controls pass EVERY checker run here (the `ctl_dupnew.*` and `ctl_dupold.*` lines of the index: P, W, O,
H, K, Q2, I2, I, L and X all rc=0).  `check_bugfile_sync.py` builds `{r["id"]: r}`, so a second row with the same id
silently replaces the first; the others iterate the rows and never compare ids.  **So the requested negative control
"duplicate one id (must red)" does NOT red in the precommit.**  The only thing that refuses it is this drafter's own
guard (`pretest_build.py`'s `guard_ids`, section 1: both controls REFUSED, naming the id), which the coordinator's
commit tooling does not run.  No checker was changed here; see GAPS.md.

## 5. Sections emulated outside the scratch checkers

* **D (added citations, `precommit_check.sh` D1/D2)** -- `python -I pre/d_emulate.py` replays D on exactly the lines
  this filing adds to OUTSTANDING_BUGS.md, CHANGELOG.md and ledger.json (a changed JSON line re-adds its whole old
  text, so old citations are re-checked too), resolving each `name.c:N` the way D does (`git ls-files "*/name" |
  head -1`, then `wc -l` of the working-tree file):

```text
D1 over HEAD tracked files: 1763 added lines, 201 distinct citations -> 201 resolve within their file, 0 BAD, 0 not found (SOFT)
D1 over HEAD + the research dir: 1763 added lines, 201 distinct citations -> 200 resolve within their file, 1 BAD, 0 not found (SOFT)
   BAD  ('wdcreg.h:138', 'regress/artifacts/research_20261022/distro_patches/netbsd_pkgsrc/netbsd_src_refs/wdcreg.h', 74)
D2 over the added lines: 0 count mentions -> 0 HARD, 0 quoted (SOFT)
```

  **The BAD line is a hazard of the research directory, not of the filing**: the commit adds
  `regress/artifacts/research_20261022/distro_patches/netbsd_pkgsrc/netbsd_src_refs/wdcreg.h` (NetBSD's, 74 lines),
  which sorts ahead of `src/include/thirdparty/wdcreg.h`, so `closeassessrows`' existing `wdcreg.h:138` (re-added
  because the T95 widening edits that JSON line) resolves to the wrong file.  GAPS.md item 1 gives the options.
* **C (message vs diff)** -- `commit_msg.txt` cites no `src/`, `regress/` or `man/` path with a `.c/.h/.sh/.1`
  extension (0 matches of C's own regex), so C has nothing to cross-check.
* **L (subject)** -- the subject's 18 tokens match none of the 1,067 ids (941 at HEAD + 126 new), checked with a
  word-boundary match; the subject is 117 characters.
* **Y (NUL bytes)** -- 0 NUL bytes in the assembled OUTSTANDING_BUGS.md, CHANGELOG.md and ledger.json, in
  `R1_tree_diff_20261022.txt`, and in the 94 text-extension files of the research directory.

## 6. Not run here, with the reason

A, B, F (no `src/` change: no twin-tree propagation, no build, no pass-2 receipt owed by a records commit); E (no
`regress/diff_*.c`); G (no new panel is cited -- the new rows have no `entries`); H2 (no change to `tools/pipeline/`
code); J (no carrier change); M (the checkpoint is the coordinator's); N, R, T, U, V, Z (no detector, probe, gate pin,
extractor or WSL script changes; the research directory carries no `.py`).  The `gate_ab.sh` header comment
(`corrections.md` tag `gateab_r1b`) is a separate script commit and was not applied to any tree here.

**What a green run here means**: the decidable checks pass on HEAD `de8c7547` with these exact deliverables applied.
If HEAD moves before the commit (another session's records commit touches the same three files), the OLD anchors are
content-based and `pre/pretest_build.py` re-applies them; re-run it and `pre/run_pretest.sh` on the new HEAD.

## 7. The exact staged files (`staged/`, 2026-10-22, after the coordinator's decisions)

Built by `python -I work/stage_final.py` from the same deliverables and the same imported machinery (`pre/pretest_build.py`'s fence parser, writer, op semantics and edit application); the matrices by HEAD's `gen_dashboard.py` and `stage_tokens.py`, copied to `work/gen/` (md5 equal to the blobs).  The checkers then ran on trees holding byte-for-byte copies of the staged files (`pre/stage_trees_final.py` md5-checks each copy), via `bash pre/run_staged.sh`.

### Staging, with the byte-identity proofs

```text
WT input: 73de19cb80e870370522968712b14a5d C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\tools\pipeline\ledger.json (9632807 bytes, the bytes parsed for ledger.WT.json)
writer reproduces the HEAD ledger (2a184268) and the working-tree ledger (73de19cb) byte for byte
working tree: 9 rows differ from HEAD (peer, untouched by this filing): ['lcabadval', 'alphavmkill', 'cxseatcheck', 'lcaconfbus1kill', 'lcairqstubkill', 'lcaisaphys', 'untrackeddetectors', 'boilerplateprefix', 'alphaifetchkill']; top-level keys differing: none; wdc473floor/heldrecedits and the 14 touched rows equal HEAD
staged/ledger.json (HEAD-based): 941 -> 1067 rows; md5 2a184268 -> e404fb5b
  proof 1 (revert the appended and touched rows -> the base's bytes): True
  proof 2 (text blocks: the lines before and after the rows are equal, the old rows keep their order and the new rows follow them; 14 old row blocks differ, outside the touched set: none): True
  proof 3 (each of the 927 untouched rows serialises identically): True
staged/ledger.WT.json (working-tree-based): 941 -> 1067 rows; md5 73de19cb -> 55a22e87
  proof 1 (revert the appended and touched rows -> the base's bytes): True
  proof 2 (text blocks: the lines before and after the rows are equal, the old rows keep their order and the new rows follow them; 14 old row blocks differ, outside the touched set: none): True
  proof 3 (each of the 927 untouched rows serialises identically): True
  the 9 peer rows keep their working-tree content: True
  the 14 touched and 126 new rows are identical in both staged ledgers: True
staged/OUTSTANDING_BUGS.md: 25203 -> 25665 lines (9 in-place notes, the head entry, the section)
staged/CHANGELOG.md: 36102 -> 36149 lines (records block 31 lines + 2 in-place notes); script edit NOT applied: ['gateab_r1b']
STAGE_FINAL_DONE
```

### staged/MD5.txt

```text
# staged/MD5.txt -- md5 of each staged file (external-fixes research filing, against HEAD de8c7547)

e404fb5b31bbe91e9de3cae085fa5dc0  ledger.json
55a22e87da2c698ea27ae3715b92d657  ledger.WT.json
3971f32b3e19f34432f201d61a40ff16  OUTSTANDING_BUGS.md
4ef01caabbe595f1363c1cbd907dc10a  CHANGELOG.md
d30682d34285711fc2af320af6abbdd7  matrix.html
449e4d124a58b08736c927fb14c84e02  matrix.WT.html
251056582b2ce3910957f7c1baad0d09  WT_INPUT_MD5.txt

# the working-tree ledger exactly as parsed for ledger.WT.json (= WT_INPUT_MD5.txt):
73de19cb80e870370522968712b14a5d C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\tools\pipeline\ledger.json

# roles: ledger.json, OUTSTANDING_BUGS.md, CHANGELOG.md and matrix.html are the commit's files (HEAD-based);
# ledger.WT.json is the same filing applied to the working-tree ledger (peer edits kept), and matrix.WT.html
# is gen_dashboard.py's render of it -- the companion for a working tree that takes ledger.WT.json.
```

### The checkers and the emulated sections, on the exact staged files

```text
  staged   ledger e404fb5b  OB 3971f32b  CHANGELOG 4ef01caa  matrix d30682d3  (copied from staged/, md5-equal)
  stagedWT ledger 55a22e87  OB 3971f32b  CHANGELOG 4ef01caa  matrix 449e4d12  (copied from staged/, md5-equal)
wrote staged/MD5.txt
staged.P_bugsync         rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
staged.W_rowstates       rc=0  ROW_STATES_PASS  no open row names a committed detector
staged.O_boilerplate     rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
staged.H_stagepanels     rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
staged.K_witness         rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
staged.Q2_entrydomain    rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
staged.I2_codexwall      rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
staged.I_fablequeue      rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
staged.L_attribution     rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
staged.X_cited           rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
staged.Q_matrix          rc=0  matrix.html matches a fresh render of ledger.json
stagedWT.P_bugsync       rc=0  BUGFILE_SYNC_PASS  7 archived (on/before 2026-08-20), 0 new
stagedWT.W_rowstates     rc=0  ROW_STATES_PASS  no open row names a committed detector
stagedWT.O_boilerplate   rc=0  BOILERPLATE_PASS  54 archived (on/before 2026-08-20), 0 new
stagedWT.H_stagepanels   rc=0  STAGE_PANELS_PASS  every post-cutoff stage ran the full panel
stagedWT.K_witness       rc=0  WITNESS_PASS  every row that closed with commits since the rule names its witness, and every cited artifact exists
stagedWT.Q2_entrydomain  rc=0  entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
stagedWT.I2_codexwall    rc=0  CODEX_WALL_OK  46 held stages, section matches the ledger
stagedWT.I_fablequeue    rc=0  FABLE_QUEUE_PASS  every owed flagship job is either done or written down
stagedWT.L_attribution   rc=0  ATTRIBUTION_PASS  0 hard, 6 soft
stagedWT.X_cited         rc=0  CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round 462 resolves (parenthesised or backticked paths with a known extension; 4 artifact-like mentions are outside that form and are COUNTED, not enforced)
stagedWT.Q_matrix        rc=0  matrix.html matches a fresh render of ledger.json
research directory now: 281 files; its .c/.h basenames: ['patch-src_cpus_cpu__arm.c', 'patch-src_cpus_cpu__arm__instr.c', 'patch-src_cpus_cpu__arm__instr__dpi.c', 'patch-src_cpus_cpu__sh.c', 'patch-src_cpus_cpu__sh__instr.c', 'patch-src_devices_dev__wdc.c', 'patch-src_include_components_CPUDyntransComponent.h', 'patch-src_include_components_M88K__CPUComponent.h', 'patch-src_include_components_MIPS__CPUComponent.h', 'patch-src_include_mips_cpu_types.h', 'patch-src_include_refcount__ptr.h', 'patch-src_include_thirdparty_bootblock.h', 'patch-src_include_thirdparty_dp83932reg.h', 'patch-src_include_thirdparty_pcireg.h', 'patch-src_include_thirdparty_sgi__arcbios.h']
D over the commit (staged/ledger.json): 1794 added lines; D1 201 citations -> 201 resolve, 0 BAD, 0 not found (SOFT); D2 0 HARD, 0 quoted
D over the working tree (staged/ledger.WT.json, index = HEAD): 1809 added lines; D1 235 citations -> 235 resolve, 0 BAD, 0 not found (SOFT); D2 0 HARD, 1 quoted
C: the message cites 0 src/regress/man source paths (nothing to cross-check)
L: the subject (117 chars) names 0 of the 1067 ledger ids 
   message: 0 URLs, ends with 'Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>'
Y: ledger.json          NUL bytes 0
Y: ledger.WT.json       NUL bytes 0
Y: OUTSTANDING_BUGS.md  NUL bytes 0
Y: CHANGELOG.md         NUL bytes 0
Y: matrix.html          NUL bytes 0
Y: matrix.WT.html       NUL bytes 0
EMULATE_STAGED_DONE
RUN_STAGED_DONE
```

Q is run exactly as `precommit_check.sh` runs it: a fresh render of the tree's own `ledger.json` with `GXLEDGER` unset, compared with `cmp` against the staged `matrix.html` (and against `matrix.WT.html` in the working-tree tree).  D runs over the research directory as it stands now, with the `.txt` renames.  The working-tree variant's one quoted D2 mention is in the peer row `lcabadval` (its own text: `exactly FOUR occurrences`), not in this filing; D grades a quoted count SOFT.

**Result: every line green -- no rc other than 0, no BAD citation, no stale matrix.**

PRETEST_DONE
