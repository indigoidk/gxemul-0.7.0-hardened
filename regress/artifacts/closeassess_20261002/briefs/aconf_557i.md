#557 -- the repairs of your aconf_557h: right?

Open with the token `ASTRA557I_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA:** `draft\REPAIRS_since_aconf557h.diff` (5 hunks over the section, changelog and message drafts) and the new
pre-step `draft\queue557_pre.py.txt` (wired into the spec as `"pre"`; `commit_unit.py` runs pre-steps before the backup in
both `--precheck` and `--go`).

1. Your item 2: the hook's `gen_codex_wall.py --check` (`tools\precommit_check.sh:122`) reads the WORKING
   `fable_queue.md` against the ledger the hook sees (the staged one).  The pre-step keeps a byte copy of the working file,
   regenerates its GENERATED block from the STAGED ledger in place (`GXLEDGER`/`GXQUEUE`), and refuses (restoring the
   copy) unless `--check` then prints `CODEX_WALL_OK`.  Measured: after the pre-step, `gen_codex_wall.py --check` and
   `check_fable_queue.py` both PASS against the staged ledger, and `--restore` puts the working file back byte-identical
   (md5 `8ee2ed9a` before and after).  Is this the right repair, and does anything the pre-step does (touching an
   uncommitted file outside the unit) break a rule you can find in the scripts?  `post557.py` regenerates the block from
   the rebuilt working ledger after `--go`.
2. Your item 3: "committed" -> "staged" wherever the failed attempt is described.  Any copy left?
3. The chain paragraph and message now carry `aconf_557h` (2 things wrong, both named) and `aconf_557i` as the
   placeholder.  Accurate?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of 5 hunks read; pre-step read: yes/no`.
