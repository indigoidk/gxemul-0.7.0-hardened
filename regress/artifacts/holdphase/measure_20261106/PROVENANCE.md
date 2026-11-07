# PROVENANCE -- `regress/artifacts/holdphase/measure_20261106/`

Banked 2026-11-06 by a records commit (kit: `_scratchpad/wrec1106/landing/`, scratch) from the scratch original `_scratchpad/wholdphase/` -- scratch, outside git, NOT durable.  The measurement read GXEMUL-SEC at HEAD `2632277f` only (`git show`).  No gate, build, probe, panel seat or codex ran for it.

Scripts and data files here are BYTE-IDENTICAL to the scratch original (md5 below), except as stated next.  `EVIDENCE.md` carries a banner and the marked rewrites its banner lists, and nothing else.

**Inputs, re-derivable read-only:** `analyze.py` reads `ledger_HEAD.json` and `HEAD_stage_tokens.py` from beside itself; both are `git show 2632277f:` blobs (see the table).  To re-run it, in a SCRATCH copy of this directory: `git show 2632277f:tools/pipeline/ledger.json > ledger_HEAD.json`, `git show 2632277f:tools/pipeline/stage_tokens.py > HEAD_stage_tokens.py`, then `python analyze.py` (it rewrites `analysis.out`, `markers.tsv`, `differing.tsv` and the `frag_*.md` tables).

**Completion sentinels, checked when this kit was built:** `analysis.out` ends with `HOLDPHASE_ANALYSIS_DONE`.

## Inventory of the scratch original at banking time (16 files; `__pycache__/` and `.git/` internals omitted)

| file (relative to the scratch original) | bytes | md5 | here? |
|---|---|---|---|
| `EVIDENCE.md` | 35948 | `7aced8e50292347049c38e3c23039847` | **copied here** (banner + marked rewrites; here md5 a9818462d78b, 36772 bytes) |
| `EVIDENCE.template.md` | 15969 | `261ea53de3d3f1c4cd57e6f98495fd3b` | scratch only |
| `HEAD_check_fable_queue.py` | 9782 | `b316318da6eb33293b9b4be4e82e8213` | scratch only; == `git show 2632277f:tools/pipeline/check_fable_queue.py` |
| `HEAD_check_stage_panels.py` | 18575 | `ef1c2d37056ec47d91c773fac0337333` | scratch only; == `git show 2632277f:tools/pipeline/check_stage_panels.py` |
| `HEAD_gen_codex_wall.py` | 12815 | `20d4be605c1e8e5da0b93434a0684c93` | scratch only; == `git show 2632277f:tools/pipeline/gen_codex_wall.py` |
| `HEAD_stage_tokens.py` | 12618 | `03cef57f828106b151f6c88a984b5f8e` | scratch only; == `git show 2632277f:tools/pipeline/stage_tokens.py` |
| `analysis.out` | 16770 | `a35a48549dbef6191d51239287ec7684` | **copied here** |
| `analyze.py` | 21417 | `bb6a92ea17be3c85308666c8394d6eff` | **copied here** |
| `assemble.py` | 9830 | `f2795327d281d2cc14105ef217dece6b` | scratch only |
| `differing.tsv` | 2287 | `1204ccd7f9cb4fcfca1a6e9f17b98b3f` | **copied here** |
| `frag_appendix.md` | 15418 | `7e8a3964cc3d87772fe0f96ea668e364` | scratch only |
| `frag_consequence.md` | 1258 | `970e5411b5abc86e4d627c5d4b135fcb` | scratch only |
| `frag_differ.md` | 3095 | `80a72471c3e3455e6f304fbba8fd02c1` | scratch only |
| `frag_scope.md` | 278 | `9118a51fc2b2ac26a28354fe164dad13` | scratch only |
| `ledger_HEAD.json` | 10683076 | `c2886383d2467ace87db77d4c7ce53b0` | scratch only; == `git show 2632277f:tools/pipeline/ledger.json` |
| `markers.tsv` | 11128 | `225ba009bbad453c283a2acbda0f78ee` | **copied here** |
