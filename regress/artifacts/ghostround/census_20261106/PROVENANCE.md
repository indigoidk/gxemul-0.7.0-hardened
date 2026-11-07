# PROVENANCE -- `regress/artifacts/ghostround/census_20261106/`

Banked 2026-11-06 by a records commit (kit: `_scratchpad/wrec1106/landing/`, scratch) from the scratch original `_scratchpad/wghost/` -- scratch, outside git, NOT durable.  The measurement read GXEMUL-SEC read-only: HEAD `2632277f` (`git show`, `git blame`) and, for the replay, older commits (`git show`).  No gate, build, probe, panel seat or codex ran for it.

Scripts and data files here are BYTE-IDENTICAL to the scratch original (md5 below), except as stated next.  `DECISION.md` carries a banner and the marked rewrites its banner lists, and nothing else.

**One edit after the outputs, verified docstring-only.**  `check_ghost_rounds.py` was last written at 22:47:33 CST, after `controls/run_controls.out` (22:47:22) and `census.out` (22:47:23).  The scratch `__pycache__` holds the bytecode compiled from the source those two runs imported (pyc header: source mtime 22:47:02, size 22428; the banked file is 22449 bytes).  Compiling the banked file and comparing every code object, constant, name and local with that bytecode: identical except the MODULE DOCSTRING, whose one usage line was rewrapped -- `--no-git` dates blocks by their headers only became `--no-git` (without --at) dates blocks by their headers only.  So the outputs here were produced by the code banked here.

**The banked script's own citations name the scratch original.**  Its docstring says it lives "in scratch (`_scratchpad/wghost/`)" and cites `controls/out/*.out`, `replay.out` and `replay_class.out`: of those only `replay.out` and `replay_class.out` are copied here.  The script is kept byte-identical, unedited, so that its md5 stays the one that produced the outputs beside it.

**Inputs, all re-derivable read-only:** the HEAD snapshots are `git show 2632277f:` of `CHANGELOG.md` and `tools/pipeline/ledger.json` (see the table) plus `git blame --porcelain 2632277f -- CHANGELOG.md` and a `git log` listing; the replay reads older commits with `git show`.  To run the banked checker against this repository, set `GXSEC` to it (its default resolves a sibling `GXEMUL-SEC/` of its own directory).

**Completion sentinels, checked when this kit was built:** `census.out` ends with `CENSUS_DONE`; `controls/run_controls.out` ends with `CONTROLS_DONE`; `replay.out` ends with `REPLAY_DONE`; `replay_class.out` ends with `REPLAY_CLASS_DONE`.

## Inventory of the scratch original at banking time (77 files; `__pycache__/` and `.git/` internals omitted; also omitted: `landing/` -- another session's landing-kit workspace, created inside this directory after the measurement and not part of it)

| file (relative to the scratch original) | bytes | md5 | here? |
|---|---|---|---|
| `CHANGELOG_HEAD.md` | 3048723 | `239ce85cb5e4b68b6271d42cee77bea5` | scratch only; == `git show 2632277f:CHANGELOG.md` |
| `DECISION.md` | 16717 | `55f16f74f938b2fc1defc940727263d5` | **copied here** (banner + marked rewrites; here md5 0277ae72cc95, 17560 bytes) |
| `HEAD_SHA.txt` | 41 | `222ed88cac94c2ca2089f5c0e8cd40b3` | scratch only |
| `at/ledger_2343036.json` | 2540937 | `351adb8d1a3b249731a178a06d5a1042` | scratch only |
| `at/ledger_7457c04b.json` | 6228971 | `64f7edcbdfe3da95831e632efa2ebcd0` | scratch only |
| `at/ledger_9c91999a.json` | 6256560 | `738671cdd4c628e9839b9445c888230b` | scratch only |
| `at/ledger_ccd1c502.json` | 10683054 | `df17b8b1ffcb623b1f053be42de9f6ef` | scratch only |
| `at/ledger_e1a091e4.json` | 10653411 | `1c7a215c4811f7d0f62663540d59b984` | scratch only |
| `blame_HEAD.porcelain` | 5212628 | `01c27ffc3fff080fcb41bcc7a55ad3d7` | scratch only |
| `census.out` | 3171 | `678030f2f8d03ed9cdf362763647bbfb` | **copied here** |
| `census.py` | 11352 | `5a04555b245bfa3c3a4667fee3d0c254` | scratch only |
| `census_hits.tsv` | 136430 | `8f95b3812941b3a9f4ff3f59eaf57af4` | scratch only |
| `check_ghost_rounds.py` | 22449 | `1914528f885b38cac521489c225d672e` | **copied here** |
| `controls/gitrepo/CHANGELOG.md` | 181 | `cdbd487d9106d5c1695b93225a6dec19` | scratch only |
| `controls/gitrepo/ledger_wb.json` | 1411 | `c8d128a96e03297e907e4a3335d177fe` | scratch only |
| `controls/out/c1a_open_date.out` | 772 | `c7cb8de468e669936392c40adc6d0d3c` | scratch only |
| `controls/out/c1a_open_mention.out` | 765 | `882dc9cd77d1b4bb388184bbee8ccee0` | scratch only |
| `controls/out/c1b_sameday_date_BLIND.out` | 432 | `94049520196577ee778122ce89f54e59` | scratch only |
| `controls/out/c1b_sameday_mention.out` | 768 | `d89ab7b2c67cb3265570961684a41749` | scratch only |
| `controls/out/c1c_claimed_date_BLIND.out` | 433 | `38f4382ef201c2285dbb2ac5409cdce5` | scratch only |
| `controls/out/c1c_claimed_mention.out` | 767 | `136c0530f35e6fc0238c44393658a0e3` | scratch only |
| `controls/out/c2a_closed_date.out` | 431 | `7964d1cd4b7ddfec288dce78d8d2ca54` | scratch only |
| `controls/out/c2a_closed_mention.out` | 434 | `7524605db4326cab168896ae2e196938` | scratch only |
| `controls/out/c2b_recorded_date_FP.out` | 776 | `1047b98e8e780e70284cc81779d86d1f` | scratch only |
| `controls/out/c2b_recorded_mention.out` | 436 | `6ad1a52049f9a8c94c38709b601becda` | scratch only |
| `controls/out/c2c_reference_all.out` | 764 | `3eb1b4228440610d4e394df402fc7674` | scratch only |
| `controls/out/c2c_reference_subject.out` | 437 | `d6981177f42ba8bd06bf572109d5cd51` | scratch only |
| `controls/out/c3a_empty_changelog.out` | 556 | `595c1bb32319c869483c9580d837670c` | scratch only |
| `controls/out/c3b_empty_ledger.out` | 562 | `a6562a0be6a46b0c5818614fa80b9ab8` | scratch only |
| `controls/out/c3c_records_only.out` | 563 | `8ba063162602777d86cc291c2d748a62` | scratch only |
| `controls/out/c4a_d9efd339_mention.out` | 1534 | `77ffdfe19eea1781a92dfb5c9d789963` | scratch only |
| `controls/out/c4b_d9efd339_date_BLIND.out` | 846 | `fb195db29d37a05aa91956309d014b00` | scratch only |
| `controls/out/c4c_4cc3952a_mention.out` | 969 | `d6e9478eabbf80d550cd14469664aa9e` | scratch only |
| `controls/out/c5_HEAD_all.out` | 29030 | `156d0abb91f6ffcb5d5749fa1030b795` | scratch only |
| `controls/out/c5_HEAD_date_all.out` | 41532 | `c1836c0da2b78a47cb5380e46c93d8d5` | scratch only |
| `controls/out/c5_HEAD_subject.out` | 2207 | `705934f972e43b88efcf232cceb048a7` | scratch only |
| `controls/out/c6a_uncommitted_FAIL.out` | 777 | `c0f21fdd97b50a1df08657e923bbc15e` | scratch only |
| `controls/out/c6b_uncommitted_writeback_PASS.out` | 449 | `b92cb044c5b839cc39365f40cd26ae36` | scratch only |
| `controls/out/c7a_2951694f_default.out` | 2962 | `297a05a08ff06ebd15b6d78677e5456f` | scratch only |
| `controls/out/c7b_2951694f_accept_commits.out` | 2249 | `95e2fa995ceff6712f461718353a5e84` | scratch only |
| `controls/run_controls.out` | 3293 | `ef7024aa372e3e08cba5c9859ea08622` | **copied here** |
| `controls/run_controls.sh` | 7685 | `70985358d4a5724aa39b3a70050be66f` | scratch only |
| `controls/synth/c1a_open.md` | 142 | `080283b10dad089fe0fcfed6070c9cdf` | scratch only |
| `controls/synth/c1b_sameday.md` | 139 | `ceff00b05b6393d3e84e1ef13c408150` | scratch only |
| `controls/synth/c1c_claimed.md` | 185 | `7f695325a2127585a9d5b2f1520dfec1` | scratch only |
| `controls/synth/c2a_closed.md` | 143 | `4f92ec891c3ea70f5d385e1c7c701eca` | scratch only |
| `controls/synth/c2b_recorded.md` | 150 | `5d76e7615212fd784cd71b861f49aa8c` | scratch only |
| `controls/synth/c2c_reference.md` | 187 | `bd08379fa25992a3cb23b32850fbc6a4` | scratch only |
| `controls/synth/c3a_empty.md` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | scratch only |
| `controls/synth/c3c_records_only.md` | 65 | `53d718cda21c42696eb62b332ed7559e` | scratch only |
| `controls/synth/ledger.json` | 1317 | `c5f7fdcea3237d4e47cf4452df24f5e4` | scratch only |
| `controls/synth/ledger_norows.json` | 12 | `7f5b28f957010af4d3cdfaebd7eb09b4` | scratch only |
| `gitlog_HEAD.tsv` | 109115 | `a67a0d4cd73a815bd3941443347e7963` | scratch only |
| `ledger_HEAD.json` | 10683076 | `c2886383d2467ace87db77d4c7ce53b0` | scratch only; == `git show 2632277f:tools/pipeline/ledger.json` |
| `parse_blame.py` | 1746 | `6514811166d20a0a799cf45802b25846` | scratch only |
| `ref_check_bugfile_sync.py` | 6405 | `0b8829786ff835049a55a1c3d34d96c7` | scratch only; == `git show 2632277f:tools/pipeline/check_bugfile_sync.py` |
| `ref_check_stage_panels.py` | 18575 | `ef1c2d37056ec47d91c773fac0337333` | scratch only; == `git show 2632277f:tools/pipeline/check_stage_panels.py` |
| `ref_precommit_check.sh` | 82600 | `7c878c20dc21195efdccf4b39eebdbb2` | scratch only; == `git show 2632277f:tools/precommit_check.sh` |
| `replay.out` | 638 | `0ceef6ba175150167f0e071b8576f4d3` | **copied here** |
| `replay.py` | 5786 | `66148ff60c050f906e2a34f66c8cf07a` | scratch only |
| `replay_class.out` | 817 | `c48b6493e65088e0fc168c30c55d255c` | **copied here** |
| `replay_class.py` | 5995 | `62ab3becdb5788efe55ce7416db87cc7` | scratch only |
| `replay_class.tsv` | 3137 | `0db9c6943a87209d2e59bd090d9c8ef7` | **copied here** |
| `replay_d9efd339/CHANGELOG.md` | 1422211 | `417e6841f7573086ced20d21aceb4055` | scratch only |
| `replay_d9efd339/ledger.json` | 2847930 | `38e3e28e0afda461a3b486d468629778` | scratch only |
| `replay_hits.tsv` | 133621 | `d2c506898070eff7c1c92fdba8065f07` | scratch only |
| `survey_blocks.out` | 68637 | `db384b7bc133b6051f2a959a59893f06` | scratch only |
| `survey_blocks.py` | 977 | `4f353fb2ceb02010646a9815cb967b87` | scratch only |
| `survey_h1.py` | 1378 | `1b94e8ac307bdbec5a2f79e3408381dc` | scratch only |
| `survey_h2.py` | 432 | `3458e67c1b0febe23792427d1da4e6d8` | scratch only |
| `triage.py` | 1077 | `27272fb140118e6ce9c6e49af5221bea` | scratch only |
| `triage_filed.txt` | 27911 | `55942399fd92a5b1ff0f05eea96a8f94` | scratch only |
| `triage_read.txt` | 39499 | `40fe32f38cbb4c46120f16f4ce6c15ab` | scratch only |
| `triage_recorded.txt` | 14534 | `3f6c3d524b53e2329f63130e5437a91e` | scratch only |
| `writeback_delay.out` | 68 | `44d5ca60717b7854ad8e092777cc7e24` | scratch only |
| `writeback_delay.py` | 3054 | `65bcb70c964f78de34d99555cd360a04` | scratch only |
| `writeback_delay.tsv` | 4501 | `8359ba66f896370907364677aad322cc` | scratch only |
