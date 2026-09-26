# `#549` fbctrlportkill -- PASS 1, the FLAGSHIP seat (you fire LAST, after all eight other seats and the measuring seat)

Open with the line `FABLE549_ALIVE`, then the FIRST LINE of `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`
verbatim, then `VERDICT: <PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED>` and numbered findings.  Keep it under about
1500 words, verdict and any ruling you would change at the top.

The tree under review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).  READ-ONLY: do not edit
any file under GXEMUL-SEC.  **If you measure, do it ONLY in WSL `/tmp` (e.g. `/tmp/gxfable549`) -- NEVER anywhere under
`C:\DocumentNoSnc\cc\GXEMUL`**: this morning a scratch clone under `_scratchpad/` made fourteen old CHANGELOG citations
ambiguous for precommit's `check_cited_artifacts` (it walks the whole project root) and blocked a commit.  Please do not
simply ratify.  **The load-bearing question is at the end: WHICH OF MY DISPOSITIONS IS WRONG.**

## What the round is

`src/devices/dev_fbctrl.c` (the test machines' framebuffer controller, unchanged since the upstream import): the PORT
arm stores any selector value with only a warning, and the DATA arm then calls `exit(1)` when the stored `int` is out of
range -- two ordinary guest accesses end the emulator process.  Proposed: the PORT arm REFUSES a selector >= 8 (keeps the
previous, valid one) and announces that once per device with the house `(once)` marker; the DATA arm is not edited.  A
detector `regress/fbctrl_port_probe.py` grows from the witness.

Evidence, all under `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/`:
* `p1_brief.md` -- the brief (the eight transports answered it; it inlines the whole access function);
* `witness_HEAD/` -- the rung-3 witness on HEAD f4f601c4, test-first (`-E testmips`, stepped guest sw/lw):
  `sw 9` to PORT then `lw` from DATA ends the process, exit 1, with the DATA arm's diagnostic; controls OK;
* `panels/panel_20260924_102737/` -- agy, grok 4.7, glm, deepseek, minimax, the kimi seat via `kimi-k3:cloud` (the kimi
  CLI is on its weekly limit: `kimi.txt`), and codex.  **codex's panel seat was REFUSED TWICE by its provider's content
  filter** -- once on the brief inlined, once on a neutral-vocabulary copy (both kept as `codex*.flagged_refusal.*`) --
  and answered in POINTER form (a short prompt naming `p1_brief.md`); that answer is `codex.txt`;
* `panels/codex_p1dedicated.txt` -- the dedicated adversarial codex job (pointer form from the start; not refused);
* `opus5_p1.md` + `opus549_measured/` -- the measuring seat.  **CAUTION: `agent_models.py` shows that answer was written
  by `claude-opus-4-8` after two refusal events by `claude-opus-5-5` -- a FALLBACK, not the Opus 5 seat.**  The
  measurements are its logs (`runs/`, `BINARIES.md5`).  The seat was resumed for a verdict-first restatement from those
  logs, `opus5_p1b.md`, **written by `claude-opus-5-5`** (agent_models.py: final text 15:54:39 UTC) -- PROCEED WITH
  CHANGES; it marks which rows it measured as SOLE catchers (boundary, wide, announce) and which not.  Say whether that
  satisfies the seat of record.

## SETTLED PREMISES (measured or read this session; cite them, do not re-derive unless you doubt one)

* `current_port` is written only by `DEVINIT`'s memset and the PORT arm (every seat, read; Opus grep).
* With the proposed `uint64_t idata >= 8` refusal, no access reaches the DATA arm's `exit(1)` (codex x2, agy, grok, glm,
  kimi-sub, read; Opus MEASURED: widths 1/2/4/8 x every offset in the 0x20 window, zero DATA-arm deaths on the fix).
* `sd 0x0000000100000003` delivers all 8 bytes on `-E testmips` (5KE, BE), and on HEAD it lands as port 3 and is
  SERVICED -- the process survives (Opus MEASURED).  So "a store of 8 or more, then DATA, ends the process" was too broad.
* `fatal()` prints and returns (debugmsg.c; the witness survives the PORT warning).
* `dev_fb_resize()` already rejects SET_RESOLUTION sizes < 10 or > 16384 and guards overflow (#184, #156) -- kimi-sub's
  side-finding about unvalidated X1/Y1 is already covered (read).

## THE CONVERGED FINDINGS AND MY DISPOSITIONS

F1 -- **the DATA arm keeps its `exit(1)`** (agy, grok, glm, minimax, deepseek, kimi-sub, Opus MEASURED: with `>`
replacing `>=` the kept check fires loudly; declining instead would index `port[8]`).  Warrant: `#521` left an
unreachable `default:` exit "deliberately ... as a tripwire for a later edit" (CHANGELOG, `#521` block).
**DISSENT (codex panel, verbatim in `codex.txt` item 3):** make it a quiet refusal -- "a future upstream-check regression
would restore process termination"; it cites `dev_sh4.c`'s `sh4_val_first()` as a documented unreachable bounds check that
returns safely.  DISPOSITION: keep the `exit(1)`, disclose it in the contract as unobservable on a correct build.

F2 -- **the detector's row set grows** (codex x2, agy, grok, glm, kimi-sub; Opus measured each row load-bearing):
`sd -1` refused (a signed `(int64_t)` compare, or `int64_t idata`, escapes every proposed row); `sb 0xff` and an `sh`
refusal (`len >= 4 &&` escapes); all EIGHT legal selectors accepted at least once (`else if (idata != 2)` escapes); a
refusal with the PREVIOUS selector 7, not only 5 (`current_port &= 5` escapes); selectors 16 and 0x200000000 refused
(a bit test, or `idata % 0x200000000`, escapes); accepted writes at widths 1, 2 and 8 (`else if (len == 4)` escapes);
the announce count checked AFTER EACH refusal (1, 1, 1 -- `warned_port++ == 2` gives 0, 0, 1) with three DIFFERENT
refused values; a DATA write after a refusal lands in the retained selector's cell.  **And one announce row runs
FREE, not stepped:** stepping raises `debug()`'s verbosity, so a `fatal` -> `debug` swap passes every stepped row
(codex dedicated).  DISPOSITION: all adopted; rows per enumerated edit, not per state.

F3 -- **five sentences of my brief were false** (codex x2, grok, glm): the "8 or more then DATA ends the process"
overclaim; "on HEAD the refusal rows end the process" (the wide and PORT-only rows fail a PRESERVATION assertion, they do
not die); the RAM counterfactual (RAM at `+0x10` would read back 2, the last value written there -- a banked register
WITHOUT command execution would read 123; the control still discriminates); "+0x03 is the low byte of PORT on a
big-endian guest" (a layout convention, not an alias -- the access lands on the `default:` arm); "no gate drives a test
machine's devices" (gate 16's `mlw2_dev_tm64` reads the testmips console; gate 14 reads testarm's MP device).
DISPOSITION: none reaches code; the probe header and the round record carry the corrected forms.

F4 -- **wiring** (agy, grok, codex): gate 16 (`gate_mips_folds.sh`) is the home, but the probe runs BEFORE its pmax-kernel
preflight (a missing kernel `gate_skip`s the whole script today), degrading the fold half when the kernel is absent;
`check_probe_wiring.py` MANIFEST entry as a `detector`, `git add`ed in the same commit; gate 6's census pins re-derived with
`tools/derive_hygiene_pins.sh`, never hand-edited; the probe's own N/N pinned in the gate; the `gatedevicesplit` note.

F5 -- **two things no rung-3 row can observe, DISCLOSED under clause (e)** (all seats): a process-global latch instead of
the per-instance field (every machine installs ONE fbctrl; adding a device to reach it would be laundering), and the
deletion of the DATA-arm check (unreachable on a correct build).

F6 -- **the fix RELOCATES one path's exit rather than removing it** (Opus MEASURED): from reset the selector is 0
(COMMAND), so "refused selector, then a DATA WRITE of a value other than 0/1/2" now ends the process in
`fbctrl_command()`'s `default:` (4 cells of the walk).  That arm was already reachable directly (PORT=0, DATA=5) and is
section 4's filed site; FILL (3) and COPY (4) are documented and marked TODO.  DISPOSITION: THIS round takes the selector
only, and says in its contract, its CHANGELOG and the probe header that the device still ends the process through its
command default and its unmapped-offset default; the command default becomes the NEXT round, filed today.
**DISSENT (kimi-sub, verbatim item 11):** "the command-default meets the reopening rule as written ... same device; the
probe's signature row already drives COMMAND ... same detector, no new oracle ... Either take it in this round or amend the
rule's wording."  codex (panel) and grok hold the opposite: a new decision (execute, decline, or implement a documented
TODO command) is a new fix shape.

F7 -- **keep-previous, not reset or clamp** (every seat): reset-to-0 routes a refused selector into COMMAND immediately
(glm: it re-manufactures the exit one step later); clamp silently selects COLOR_B.  Keep-previous matches `dev_fb.c`'s own
"reject and keep the old framebuffer" behaviour (codex panel).  The residual in F6 is keep-previous FROM RESET.

## THE RULINGS I NEED FROM YOU

1. **F1: keep the unreachable `exit(1)`, or turn it into a quiet refusal?**  Rule on the arguments (a loud tripwire for a
   future PORT regression vs "no process-ending call should remain anywhere a regression could re-open"), not the count.
2. **F6: take the command default in this round, or disclose and file?**  Rule on the reopening rule's text: does a
   different decision about WHAT the arm does (decline an unknown command; decline or implement the documented FILL/COPY)
   make it a different class, when the detector and oracles would be shared?
3. **Which of my dispositions is wrong?**  Name the count.  In particular: is any row in F2 not owed (rows are owed per
   enumerated edit), and is anything owed that F2 does not list?
4. **Test-first**: is the witness in `witness_HEAD/` a valid rung-3 reproduction (liveness, device signature, an
   unmodified machine, stepped real instructions)?
5. If, while verifying a claim, you found something ELSE -- say so.
