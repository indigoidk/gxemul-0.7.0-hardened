# PROVENANCE -- `regress/artifacts/codeqlscope/plan_20261106/`

Banked 2026-11-06 by a records commit (kit: `_scratchpad/wrec1106/landing/`, scratch) from the scratch original `_scratchpad/codescan/dismiss/` -- scratch, outside git, NOT durable.  The plan read GitHub's code-scanning API with GET requests only, and GXEMUL-SEC read-only: HEAD `2632277f`, the scanned commit `f58105b7`, `git blame`.  No gate, build, probe, panel seat or codex ran for it.

Scripts and data files here are BYTE-IDENTICAL to the scratch original (md5 below), except as stated next.  `SUMMARY.md` carries a banner and the marked rewrites its banner lists, and nothing else.

**`plan.tsv` is NOT byte-identical: three comment cells were edited, 2026-11-06, to carry the two wording notes of Fable 5.1's final ruling** (`../ruling_20261106/RULING.md`, section 4: *"I would add 'on guest-reachable paths; the host-set initial stride is #124's'"* for #126/#127, and #130's comment *"is loose about the (dpl+1)*4/bpp derivation"*).  Scratch original md5 `c26391171a7c33f947997b126bab415f`; here md5 `f89bd0416f089deefdc6a0df8dad8089`.  Each edit, as old -> new text (the count is how many cells carried the old text):

* (2 cells)
  * old: False positive: dev_fb_resize() caps both sizes at 10..16384 with SIZE_MAX checks, so rows * line stays below 2^30 (code-scanning triage 2026-11-05).
  * new: False positive: dev_fb_resize() caps both sizes at 10..16384 with SIZE_MAX checks, so rows * line stays below 2^30 on guest-reachable paths; the host-set initial stride is #124's (code-scanning triage 2026-11-05; final ruling 2026-11-06).
* (1 cell)
  * old: False positive: xsize and ysize come from the masked DIWSIZE fields and bytes_per_pixel is at most 4, so the product cannot overflow an int (code-scanning triage 2026-11-05).
  * new: False positive: xsize = ((DIWSIZE_DPL & 0x3ff) + 1) * 4 / bytes_per_pixel and ysize = (DIWSIZE_LPF & 0x3ff) + 1, each halved in some modes, so bytes_per_line * ysize is at most 4096 * 1024 and cannot overflow an int (code-scanning triage 2026-11-05; final ruling 2026-11-06).

**STILL OWED IN SCRATCH, before any `dismiss.sh --apply`:** the scratch originals in `_scratchpad/codescan/dismiss/` still carry the old text -- `plan.tsv` and its generator `tools/mkplan.py`, where the comment text lives (the ruling: "a one-line edit there before the re-derivation carries them").  Make the same two edits in `tools/mkplan.py`; the post-push re-derivation then regenerates `plan.tsv` with them.  This kit did not edit the scratch originals.

**Durable twins the rewrites point at** (byte-identical, checked when this kit was built):

* `_scratchpad/codescan/fmt_warnings.tsv` (cited as `../fmt_warnings.tsv`) == `regress/artifacts/fmtattr/scan_20261105/fmt_warnings.tsv` at HEAD, md5 `34e8d8fb9e94347bfd181832c183573b`.
* `_scratchpad/codescan/fmtfix/fmtverify2.out` (cited as `../fmtfix/fmtverify2.out`) == `regress/artifacts/fmtattr/stage_20261105/fmtverify2.out` at HEAD, md5 `4c117982be4565adae116d74df60b6ae`.

**Inputs:** a read-only fetch, `gh api --paginate "repos/indigoidk/gxemul-0.7.0-hardened/code-scanning/alerts?state=open&per_page=100"` (2026-11-06T04:07:53Z) and the same endpoint without `state=open`; `ALERTS_JSON.txt` records each file by size and md5.  `plan.tsv` and `SUMMARY.md` are written by `tools/mkplan.py` and `evidence_expected.txt` by `tools/verify_expected.py` (scratch originals, md5s below).  `dismiss.sh` reads `plan.tsv` from beside itself; its default mode is a dry run with no network access, and `--apply` was never run.

**Completion sentinels, checked when this kit was built:** `checks/run_checks.out` ends with `RUN_CHECKS_DONE`.

## Inventory of the scratch original at banking time (32 files; `__pycache__/` and `.git/` internals omitted)

| file (relative to the scratch original) | bytes | md5 | here? |
|---|---|---|---|
| `SUMMARY.md` | 11527 | `fcf110445ec373c1af16fc5d010e7003` | **copied here** (banner + marked rewrites; here md5 eab2bed3ae3f, 13163 bytes) |
| `alerts_all_now.json` | 731247 | `2bb6e6b4f8874f1db1a614709b23831a` | recorded in ALERTS_JSON.txt |
| `alerts_all_raw.err` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | recorded in ALERTS_JSON.txt |
| `alerts_all_raw.json` | 677717 | `5f6b199961be199bd11ccb3c9e406041` | recorded in ALERTS_JSON.txt |
| `alerts_open.json` | 692632 | `20469c2cdfa16eaa05229f7f95814b89` | recorded in ALERTS_JSON.txt |
| `alerts_open_raw.err` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | recorded in ALERTS_JSON.txt |
| `alerts_open_raw.json` | 641934 | `62948787311d1cbd063d8476be257997` | recorded in ALERTS_JSON.txt |
| `checks/badhdr.out` | 67 | `8caa15087547d2e96b45f1291130ee6a` | scratch only |
| `checks/check.out` | 8660 | `7ff5260e54574bf10313fac23146da14` | scratch only |
| `checks/check_neg.out` | 1391 | `11a13e008976d433012382887a28b04e` | scratch only |
| `checks/dryrun.out` | 6758 | `2f5542fcf1480891ab7b826b23dacb8f` | scratch only |
| `checks/dryrun_commands.txt` | 6118 | `778bf864896a5147c4f6f4b289674a4b` | scratch only |
| `checks/gh_check.log` | 4816 | `e9d544a704b4edf7d6763acf7c616634` | scratch only |
| `checks/gh_guard.log` | 623 | `683a38c09b3e904441bf586c5ce32820` | scratch only |
| `checks/gh_neg.log` | 1507 | `6202c47b732955dffc1a369abfd5fcb4` | scratch only |
| `checks/guard.out` | 316 | `a5dcea9f680649c42aacc48b3a8feff2` | scratch only |
| `checks/mkplan.out` | 245 | `815d83fd2f0c2f7771d9936300547614` | **copied here** |
| `checks/plan_badhdr.tsv` | 16 | `c355164580c40466d1da5818ea92c027` | scratch only |
| `checks/plan_neg.tsv` | 1871 | `e48da0a688dd6ba3ef1377abdd6b19c9` | scratch only |
| `checks/run_checks.out` | 869 | `84cdd83c6e9e5bf032fe1ff4b596b9b4` | **copied here** |
| `dismiss.sh` | 5798 | `ed965f9dc840479bbb0bf3e1a67fcfc4` | **copied here** |
| `evidence_expected.tsv` | 10740 | `6a5adc46b64e77645a435c6468793176` | scratch only |
| `evidence_expected.txt` | 93702 | `e578958a5c1ca1ebe3b6d18490b2f8e7` | **copied here** |
| `evidence_tree.txt` | 1176 | `45d5d8969ddfdcb3022bf724541447b7` | scratch only |
| `plan.tsv` | 65591 | `c26391171a7c33f947997b126bab415f` | **copied here** (three comment cells edited per the 2026-11-06 ruling, below; here md5 f89bd0416f08, 65870 bytes) |
| `tools/gh_readonly.sh` | 1257 | `9e8836df976c51e3f4b652eb885478af` | scratch only |
| `tools/mk_plan_neg.py` | 2434 | `498fb32ccb3bcc8b1e1aca1b42a6294f` | scratch only |
| `tools/mkplan.py` | 26475 | `ba9bb7d788fc6dad1f581e907a2ba928` | scratch only |
| `tools/run_checks.sh` | 2722 | `a21e02287b9593505cd39366c9778dc6` | scratch only |
| `tools/tree_identity.py` | 3989 | `855cd6dce5a2275295657d7fc0c2c3b5` | scratch only |
| `tools/verify_expected.py` | 7316 | `5e6ef3aa76c351cd7efef0519ba921ae` | scratch only |
| `work_open.tsv` | 41645 | `6bd8e629183f188d5df222910c4fd424` | scratch only |
