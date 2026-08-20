# GXemul 0.7.0 hardened fork — standing instructions (every session)

`GXEMUL-SEC/` is the git repo (push from Windows git-bash, never WSL). `est/` is its
non-git twin; `build/` (pmax) and WSL `/tmp/gxsec-build` (arc) are in-place build trees
with **NO VPATH** — propagate every edit into them or you measure a stale binary.

**First stop each session:** `git -C GXEMUL-SEC log --oneline -5` (memory summaries go
stale; the repo is the truth), then `_scratchpad/CHECKPOINT.md` (in-flight uncommitted
work + **build-tree dirtiness** — see below), then `GXEMUL-SEC/OUTSTANDING_BUGS.md` (the
"OPEN LIST" head plus the dated tail entries = the live queue) and the harness TaskList.

**Checkpoints (standing directive, 2026-08-11): survive power/Windows outages.**
1. `_scratchpad/CHECKPOINT.md` is OVERWRITTEN (never appended) at every round boundary
   and before/after any build-tree mutation. It records only what git cannot: uncommitted
   files, in-flight measurements, and which build trees are dirty and how to restore
   them. Its own staleness rule: if its HEAD line disagrees with `git log`, re-derive
   and rewrite it. (RESUME.md once went stale for 26 rounds — a checkpoint that grows or
   lingers is worse than none.)
2. **Any script that mutates a build tree MUST drop a sentinel first** —
   `build/.MUTANT: <file> <what>` — and remove it only after restore is VERIFIED by
   `cmp` against GXEMUL-SEC (the repo source, NEVER the script's own backup: a crashed
   run once left the tree mutant, so the next run's "orig" backup captured the mutant
   and its restore restored it). A fresh session finding a `.MUTANT` sentinel restores
   from SEC (`rm src/cpus/*.o`, rebuild) before trusting ANY measurement.
3. Commit+push at every green gate — an unpushed round is the largest single exposure.

Ethos (non-negotiable): terse portable C99, minimal surgical changes, `/* #NNN: */` tags,
a CHANGELOG.md round block per correction (REVIEW_FINDINGS.md is frozen at #290 — see its
scope banner, added by #385; rows #291+ live in the CHANGELOG round blocks), honest
"assessed, not changed" records. **Test-first:** reproduce on the committed build before
any edit — where *reproduce* is defined by the WITNESS LADDER below; a defect
with no witness gets documented instead. No session URLs
in commit messages (keep `Co-Authored-By`).

## SEAT LEDGER — which seats were USED, which were NOT, and why (keep this current)

**Record it every round.** A seat that did not answer is a SEAT FAILURE, never agreement, and a
seat that was deliberately not fired is a different thing again — conflating the two is how a
two-seat review gets reported as a panel. State both, by name, in the round record.

*** CURRENT AS OF 2026-08-19 ~23:0x — READ THIS BLOCK BEFORE THE TABLE BELOW IT, which is
the 08-14 snapshot and is kept for its reasoning, not its status. ***

**EIGHT OF NINE ANSWERING. The only seat down is CODEX — the one this table calls "USED, every
pass".** Two full panels ran today (rtcdet review, smharness assess) and every seat except codex
produced a substantive answer:

| seat | 2026-08-19 | what it did today |
|---|---|---|
| **Codex 5.6-SOL** | *** DOWN — quota, walled to Aug 22 12:12 *** | See below; this is the one that inverted. |
| **Opus 5** (Agent) | ALIVE, and again the highest-yield seat | Found the cheapest escape on record: `TIMER_MAX_FREQUENCY` -> `TIMER_MAX_CATCHUP`, ONE identifier, passing 12 of 12 rows. It COMPILED AND MEASURED, as usual. |
| **Fable 5** (Agent) | ALIVE — liveness token returned, twice in one session | Found SIX wrong records the round had shipped. One of its own calls was then overturned by the preprocessor; see the note on measurement below. |
| **Kimi 3** | ALIVE — 60 KB | Found the clamp escape INDEPENDENTLY and scoped it exactly. Gave no VERDICT line despite the brief asking for one — a FORMAT miss, recorded as such, not a seat failure. |
| **agy 3.7** | ALIVE — 15.7 KB | Named the clamp-value gap. |
| **Grok 4.6** | ALIVE — 2.5 KB | Short but substantive; named three gaps in one line, two of which measured true. |
| **glm-5.2** | ALIVE — 8.2 KB | Packet-fed, correct on the defect and honest about scope. |
| **deepseek-v4-pro** | ALIVE — 3.6 KB | The only dissenting verdict, and its headline was wrong for a reason worth keeping. |
| **minimax-m3** | ALIVE — 10.9 KB | The inlined-brief rule continues to hold. |

*** THE SEAT MOST RELIED ON IS THE ONE THAT FAILED, AND IT FAILED IN THE SHAPE THIS FILE WARNS
ABOUT. ***  Codex's panel file was **26,992 bytes — the LARGEST in the panel** — and it was the
ECHOED BRIEF followed by "You've hit your usage limit ... try again at Aug 22nd, 2026 12:12 PM",
twice. A size check alone scores that the best answer of the nine. `panel.sh`'s seat check caught
it as RATE-LIMITED. **Verify the CONTENT, never the size; the failure mode is a big file.**

**A SHORT ANSWER AND A DEAD SEAT ARE NOT THE SAME THING.** Grok's file was 119 bytes when first
sampled — opening line only, "I'll read the full offloaded packet first" — and looked exactly
like the minimax stall this file spent days mis-attributing. It was MID-ANSWER. Sample twice
before calling a seat dead; the size check cannot distinguish slow from dead.

**SEAT RANK DOES NOT SETTLE FACT — measured twice today, in both directions.** The flagship seat
corrected a false "strict superset" claim about header closures and its correction was ALSO
false; `gcc -E -H` settled it (two exceptions, not the one either of us named). And a reading
seat's claim that production `fatal()` exits — which would have made a shipped correction into
guest-reachable process death — was refuted by opening `debugmsg.c:384`, where `fatal()` is
byte-for-byte `debug()`. **Both were settled in under two minutes by looking.**

---

*The 2026-08-14 snapshot follows, kept because the reasoning outlived the statuses:*

| seat | status (2026-08-14) | evidence |
|---|---|---|
| **Codex 5.6-SOL** (xhigh) | **USED, every pass** | answered 400–600 KB each time. *But on the #416 pass 2 it stated plainly it COULD NOT EXECUTE (read-only session) — a READING, not a measurement. Its mutants were predictions; the measure seat settled them.* |
| **Opus 5** (Agent, `model: "opus"`) | **USED, every round — the highest-yield seat** | the only one that COMPILES AND RUNS. Overturned the main loop's conclusion four times in #414 and twice more in #416, including reversing its own answer on measurement. Resumable via SendMessage with its context intact. |
| **Grok 4.6** (xhigh) | **USED on pass 1 only** | rate-limited; deliberately not fired on pass 2. |
| **agy 3.7** (`gemini-3.7-flash-high`, `--effort high`) | **USED on pass 1 only** | same reason. Quantified the round-up gap across all five rig images. |
| **Ollama glm-5.2:cloud** | **USED on pass 1 only** | same reason. |
| **Ollama deepseek-v4-pro:cloud** | **USED on pass 1 only** | same reason. Named the discriminating mutant for the bound design. |
| **Ollama minimax-m3:cloud** | *** ALIVE — IT WAS NEVER THE SEAT, IT WAS THE BRIEF (proved 2026-08-15) *** | Stalled at ~108–149 bytes on every earlier attempt ("let me pull the key files") and was written off as broken for days. The #420 brief INLINED every fact and opened with *"do not plan to read files"* — **it answered with 12 KB, its first real answer on record, and deepseek answered in the same pass.** |

*** ALL SEVEN SCRIPTABLE SEATS ANSWERED THE #420 BRIEF — the first time that has happened.
The variable was the BRIEF, not the roster. *** A brief that inlines every fact and says
plainly "do not plan to read files" got 12 KB out of minimax and 5.6 KB out of deepseek, both
of which had been recorded as broken. **Two of the nine "dead" seats were alive the whole
time.** Before pruning any seat, re-run it against an inlined brief — a stall from a
file-reading instruction is indistinguishable from a quota wall in the output, and this
project mis-attributed it for days.

**THE CLOUD SEATS CANNOT READ FILES, AND THE BRIEF DECIDES WHETHER THEY ANSWER — this is a
PROMPTING defect, not a seat outage, and it was misdiagnosed as one for days.** On the #419 pass 1
**deepseek stalled at 136 bytes with minimax's exact signature**, having answered 7 KB the round
before. The difference was not the seat: #418's brief INLINED its measurements, #419's told the
seats to read the source. glm survived only by answering from the prompt alone and said so —
*"no files read; no boots executed; every line citation in this review is the prompt's, re-stated,
not independently verified."* That is the honest form and the right way to count it: a READING.
**RULE: inline every fact a cloud seat needs. A brief containing "read the source" guarantees a
stall from deepseek and minimax, and it will look exactly like a quota failure.**
| **Kimi 3** | *** BACK — USED AND ANSWERING, 2026-08-14 ~21:0x *** | Quota-dead since ~08-12 (403, 328-byte error file). On the #121 pass 1 it returned **128 KB** ending in a real verdict, and **it RAN ITS OWN PROBE** (`/tmp/t121`, `_scratchpad/t121_probe.c`) while re-checking `git status --porcelain` empty afterwards — so it is a MEASURING seat, not only a reading one. **It beat the main loop twice in that single pass:** it found the self-invalidating occurrence count at a SECOND site (`CHANGELOG.md:4580`) that a `src/`-only grep missed, and it caught that `prefix_d` is absent from the `prefix_i+prefix_f+prefix_s > 1` guard at `diskimage.c:1763`, so `ds:` is accepted and a naively-placed `d:` assignment would silently override an explicit `s:`. **A 128 KB substantive answer IS the health test.** Wire it back into panels AND into the #124 adjudication. |
| **Fable 5** (Agent, `model: "fable"`) | *** ALIVE — REVIVED BY THE 2026-08-15 /login, NOT BY THE CALENDAR *** | Six consecutive quota failures (the sixth deliberately after the date rollover, proving the reset is not at local midnight) — then the owner's `/login` at ~10:4x restored it. The post-login ECHO-TEST returned **both nonces** (prompt token + verbatim file quote from CHECKPOINT.md), so prompt delivery AND file access are proven, not assumed. **Both "dead" Anthropic-side states this project has seen were revived by ACCOUNT-STATE CHANGES (Kimi: billing cycle; Fable: login), never by a date.** The owner also set the session model to Fable 5 (max) — the flagship hat and the main loop are one model again. Its first act back: the FABLE half of the FABLE/KIMI adjudication, reviewing Kimi's docket verdict item by item. Health-tested **five times** across 2026-08-13/14, including on the day its reset was expected and again at ~22:2x on 08-14. DO NOT ASSUME A CALENDAR DATE RESTORES A SEAT — TEST IT; the test is one Agent call told to open with a liveness token (`FABLE_SEAT_ALIVE_<date>`), which costs one call and cleanly separates "dead" from "assumed dead". Kimi revived with no calendar signal after five failures, so keep testing this one too — but ONCE PER SESSION, not per round. |

**Nine seats by design; SEVEN answering as of 2026-08-14 ~21:0x. `panel.sh` fires seven scriptable
seats, only ONE of which (minimax) now produces nothing.** Kimi came back with no warning and no
calendar signal — which is the general lesson: **a dead seat is dead until a real invocation says
otherwise, and it may revive the same way. Fire the full roster and let the seat-check sort it;
do not prune a seat out of the script on the strength of a previous failure.** The only seat still
down is Fable, and the ADJUDICATION (see below) is no longer blocked, because Kimi can hold it alone.

### *** A FABLE/KIMI PASS IS THE ADJUDICATION FOR FIXES (standing user directive, 2026-08-14) ***

When Fable and Kimi come back, their pass is **not another review** — it is the **adjudication of
the fix list**. Give them the candidate fixes and residuals a round has produced and ask which are
worth making, in what order, and which should be filed or dropped. That is a different question
from "is this diff correct", which the reading and measuring seats already answer.

Until they return the adjudication degrades to the main loop, which is the documented fallback and
has worked — but the rule that made it work is unchanged and applies to whoever holds the hat:
**anything checkable in under about two minutes gets CHECKED, not judged.** Every useful drop on
2026-08-13 was settled by a grep, a run, or a five-rig spelling check.

*** SUPERSEDED 2026-08-16 BY OWNER DIRECTIVE: FULL PANEL ON EVERY STAGE. ***

**THE RULE NOW: every stage — assess, research AND review — runs all nine seats before the round
moves on. If a seat cannot be run, STOP AND ASK THE OWNER.** Do not degrade quietly; that is
exactly what this replaces. `regress` remains FABLE-ONLY (separate standing directive), and stages
that ran before 2026-08-16 are grandfathered forward-only and carry an explicit annotation entry so
their blanks do not read as seat failures.

Mechanically enforced by `GXEMUL-SEC/tools/pipeline/check_stage_panels.py`, wired into `precommit_check.sh` as a
hard section H. Note it complements rather than duplicates section G: **G verifies that a seat which
ANSWERED was recorded; H verifies the seat was FIRED at all.** Neither catches the other's failure.

*The superseded rule, kept because the reasoning is the part that expired, not the caution:* it said
ONE full panel per ROUND with pass 2 restricted to Codex + Opus, because the Ollama seats 429 if two
panels fire within ~20 minutes and Grok's free tier died after ~4 substantial invocations. **Grok is
paid now and Kimi is back**; all seven scriptable seats answered the last three panels, so the only
live constraint is the ~20-minute Ollama spacing — which real stages already exceed. A policy
written around two dead seats outlived both of them by a week.

## The multi-LLM panel — EVERY task, research and review (standing user directive)

Every code round runs the panel **twice**: pass 1 on the design brief BEFORE any edit,
pass 2 on the actual diff AFTER. Research/triage tasks get at least one pass. Launch all
seats **concurrently** (independent processes / one Agent batch), then collect.

| seat | invocation |
|---|---|
| Codex 5.6-SOL (xhigh/ultra) | `codex exec --sandbox read-only --skip-git-repo-check -m gpt-5.6-sol -c model_reasoning_effort="xhigh" "$(cat brief)" < /dev/null` — the `< /dev/null` is required. Windows argv caps ~32 KB: bigger briefs = short prompt pointing at the brief file. Never the trailing-`-` stdin form (died silently once). |
| agy 3.7 (high) | `agy --dangerously-skip-permissions --add-dir <dir> --print-timeout 30m --model gemini-3.7-flash-high --effort high --print "<short prompt pointing at brief file>"` — reads files via `--add-dir`; no stdin prompt mode. **Model set by user directive 2026-08-13.** PASS BOTH `--model` and `--effort`: the effort tier is baked into the model name (`-high`/`-medium`/`-low`) AND there is a separate `--effort` flag, so naming only one leaves the other at its default. Before this, `panel.sh` passed NEITHER while printing "agy(high)" — the banner was an overclaim. **`agy models` is the authority on valid names** (it lists gemini-3.7/3.6/3.5-flash and 3.1-pro tiers, plus claude-sonnet-4-6 and claude-opus-4-6-thinking); a wrong name is a SEAT FAILURE, so re-check after any CLI upgrade. |
| Kimi 3 | `kimi -p "$(cat brief)" -m kimi-code/k3` — rejects `--auto`/`--yolo` with `-p`. **QUOTA-DEAD since ~2026-08-12** (403 usage-limit-for-billing-cycle; five consecutive seat failures were this, not a wedge — the health test `kimi -p "say OK"` returns the 403). **RE-HEALTH-TESTED 2026-08-13: still the identical 403**, so it is out until the billing cycle refreshes — do not wire it into panels or adjudication meanwhile, and do not read its ~328-byte error file as a seat answer. Re-test before re-adding. |
| Grok 4.6 (xhigh) | `grok --prompt-file <brief> -m grok-4.6 --effort xhigh --permission-mode plan --cwd <proj> < /dev/null` — **xhigh set 2026-08-13 by user directive and VERIFIED to be a real tier, not assumed: passing a bogus value makes the CLI name its own list, `use one of: xhigh, high, medium, low`, which proves the flag is validated AND that xhigh is the top of it.** That discriminator is the general technique — if a bad value were silently ignored, acceptance would prove nothing and the seat would quietly run at the default, which is precisely the trap the agy seat sat in. **A bad effort value EXITS 0 while printing its error**, so exit status cannot catch it; `panel.sh`'s seat check greps for "unknown effort level"/"unknown model" alongside the quota patterns. — binary at `~/.grok/bin/grok.exe`, **added 2026-08-13 by user directive.** *** `--prompt-file` TAKES THE BRIEF FROM A FILE, so the ~32 KB Windows argv cap DOES NOT APPLY — this is the only CLI seat immune to the failure that killed Codex on a 36 KB brief today, so it is the seat to trust with a large inlined diff. *** `--permission-mode plan` keeps it READ-ONLY (verified: it read a repo file and answered correctly, without prompting or hanging) and `--cwd` lets it consult source like Codex and agy do. `grok models` is the authority on IDs; today it lists exactly one, `grok-4.6`, which is also the default. **PAID (SuperGrok) as of 2026-08-13 — verified live, health test passes at xhigh.** Two independent confirmations that the subscription is active: the health test answers, and `grok models` now lists TWO models (`grok-4.6` default plus `grok-4.5`) where the free tier listed only one — so the model list is itself a cheap tier check. The paid cap is still not queryable (no `usage`/`quota` subcommand; `du` is disk usage), so DO NOT ASSUME IT IS UNLIMITED — a raised cap has the same failure mode further out. `panel.sh`'s seat check scans any non-answering seat for quota/rate/auth text generically, so a wall is reported as an OPERATIONAL failure rather than counted as agreement. **FREE-TIER HISTORY, kept because it calibrates expectations: the free tier died after ~4 substantial invocations, mid-way through its first real review — and even so it found a genuine defect in that partial output (three surviving "un-fakeable" overclaims that two other seats had missed).** |
| Ollama cloud ×3 | POST `http://localhost:11434/api/generate` from **git-bash** python (WSL cannot reach the host API); write responses to utf-8 files, never `print()` (cp1252 crash). Three seats, verified live 2026-08-10: **`glm-5.2:cloud`**, **`deepseek-v4-pro:cloud`** (DeepSeek is back — v3.2 was retired 2026-07-15 but v4-pro is live; the exact tag needs `-pro`), **`minimax-m3:cloud`**. All three are THINKING models — send NO `num_predict` cap or hidden reasoning eats the budget and the response is empty. Recheck: `curl -s localhost:11434/api/tags`. |
| Claude (Opus 5) | the Agent tool with `model: "opus"` — it has repo Read/Grep/Glob, and is the seat most likely to COMPILE AND MEASURE (it has overturned readings twice). Use plain bounds-/correctness-engineering framing, never offensive-security wording (refusal/flag risk); keep the adversarial instruction aimed at the engineering claim. There is no opus/fable CLI. |
| Claude (Fable 5) | the Agent tool with `model: "fable"` — an independent Fable seat, separate from the main loop. Same framing rules. NOTE Fable wears two hats: this review seat, and (as the main loop) the ADJUDICATOR of the panel's task suggestions. **QUOTA-DEAD since 2026-08-13** ("You've reached your Fable 5 limit"; two consecutive relaunches failed identically — the Kimi pattern, a quota not a wedge, so a retry cannot clear it). **RE-HEALTH-TESTED 2026-08-14 ~09:4x, ON THE DAY THE TOKEN RESET WAS EXPECTED: STILL THE IDENTICAL LIMIT MESSAGE.** Third consecutive failure, so the reset either has not landed or the allowance is still exhausted — do NOT assume a calendar date restores a seat, TEST IT. The test is cheap (one Agent call told to open with a liveness token) and it is the only thing that distinguishes "dead" from "assumed dead". The ADJUDICATOR hat is unaffected while the main loop still runs. Substitute used meanwhile: an Agent seat with `model: "sonnet"` carrying the same static/records lens, **always recorded as a SUBSTITUTE, never as "the Fable seat"**. Health-test before re-adding. |

Panel rules, learned the hard way:
- *** A READING SEAT BUYS THE CLASS; A MEASURING SEAT BUYS THE INSTANCE — AND THE CLASS ARRIVES
  FIRST, FOR FREE. *** On #434's pass 1 a reading seat wrote that the planned detector was *"too
  clean and will green-light state-dependent mutants that still purge on the only path a guest
  takes."* **Nobody read it for a day.** Over the next two rounds measuring seats independently
  BUILT that exact class twice — value guards (`&& idata`, `odata != 0`, a UAPR-only equality
  guard) and selector guards (`&& d->cmmu_nr == 0`) — each discovery costing a full pass-2
  cycle. The measuring seats were necessary to PROVE the instances; the reading seat had already
  named the family. **So when a reading seat names a FAMILY of mutants, hand that sentence to
  the measuring seat as its next assignment rather than waiting to rediscover the members.**
  Honest limit, because one instance cannot settle it: whether that prediction was load-bearing
  or merely lucky is not decidable from a single case. It is recorded as a heuristic worth
  acting on, not as a law. *(Was ledger row `m8invpred`, dropped 2026-08-20 by unanimous panel
  verdict — a real lesson that was never a defect, and that nothing would ever have closed.)*
- **Verify every seat actually answered** — one 246 KB "answer" was the echoed prompt.
- **Disagreements are settled empirically** (instrument and boot), never by vote — the
  majority has been wrong on mechanism repeatedly (≥6 recorded cases; round 100's Opus
  seat overturned a confident measured reproduction by *compiling* variants).
- Seat health drifts. If a CLI wedges, re-test before dropping the seat.

## *** THE HARNESS MOVED INTO GIT ON 2026-08-17 — EVERY PATH BELOW CHANGED ***

It lived at the project root, **outside version control**, until the owner was asked and chose to
track it. It is now `GXEMUL-SEC/tools/` — `precommit_check.sh`, `nightly_battery.sh`,
`nightly_check.sh`, `panel.sh`, `adjudicate.sh`, `panel_ollama.py`, and `tools/pipeline/` with the
ledger, `gen_dashboard.py`, `check_seats_read.py`, `check_stage_panels.py` and `fable_queue.md`.
See `GXEMUL-SEC/tools/README.md`, which records which failure each gate was built after.

Scripts now DERIVE the project root from their own location (`$GXROOT` overrides). They used to
hardcode one machine's absolute path, which is only half-tracked. **The migration got that wrong
once and the dead-man switch caught itself** — a dangling `[ -d "$ROOT" ] ||` swallowed the new
assignment, `ROOT` resolved empty, and `nightly_check.sh` reported FAIL rather than passing.

The scheduled task `GXemul-weekly-battery` was repointed at `tools/nightly_battery.sh` and then
TRIGGERED to prove it fires. Its `LastRunTime` had read `11/30/1999` for its whole first week: it
had never run, and nothing said so.

**Two gates were added the same week and they are NOT redundant** — `precommit_check.sh` section
**G** verifies that a seat which ANSWERED was recorded; section **H** verifies the seat was FIRED
at all. Neither catches the other's failure. Two more followed, and the same warning applies:
**I** checks that flagship work which is OWED is written down (H reads a HELD marker as "waiting",
and waiting is indistinguishable from forgotten), and **J** checks the carrier copies below.

### THIS FILE IS TRACKED BY COPY, AND SECTION J IS WHY THAT IS SAFE

Owner decision 2026-08-17: `CLAUDE.md` and `PIPELINE.md` are tracked. They cannot be tracked
*where they sit* — **the git root is `GXEMUL-SEC/`, one level BELOW the project root**, and the
carrier has to sit at the project root to be auto-loaded. So the tracked form is a copy at
`GXEMUL-SEC/tools/CLAUDE.md` and `tools/PIPELINE.md`.

**A copy nothing checks is the antipattern the owner had just rejected** (a dated
`CLAUDE.md.snapshot_20260817` was deleted rather than committed, for the same reason RESUME.md
went stale for 26 rounds). So `precommit_check.sh` section **J** hard-fails on byte-divergence,
using check A's `cmp` idiom. **The root file is the live one; after editing it, re-copy.** An
absent root original is NOT a failure — on a fresh clone the repo copy is the only one there is.

`tools/` and not `GXEMUL-SEC/` deliberately: the cwd DRIFTS (it has sat in `GXEMUL-SEC/regress`
for whole rounds), and a copy at `GXEMUL-SEC/CLAUDE.md` would auto-load *alongside* the root
original, putting two copies of a 38 KB carrier in one context.

## Tooling that makes the panel automatic (the "always" layers)

1. **Carrier** — this `CLAUDE.md`, auto-loaded every session.
1a. **THE PIPELINE DOCTRINE** — `PIPELINE.md` (project root): the owner's portable multi-LLM
   fix-pipeline methodology, supplied 2026-08-15 and ADOPTED (pasted into the loop five times —
   that is a directive). Two seat CLASSES recorded on every dispatch: FILE-READING (Codex, agy,
   Grok, Kimi, Opus, Fable — facts about the repo) vs PACKET-FED (the three Ollama seats —
   attack reasoning only; their blindness is a feature; NEVER equivalent votes on repo fact).
   Conflict-of-interest badges on every closure: `A` = author self-review disclosed, `s` =
   same-model replication (weaker than two-family, never passed off as it). Evidence ladder
   CONFIRMED > MANUAL > BELIEVED > UNKNOWN — an honest UNKNOWN outranks a confident guess.
   VERDICT LINE FIRST in every requested seat output (truncation survives). Echo-test = nonce in
   the prompt + nonce in a file, both required back. **The ledger**: `GXEMUL-SEC/tools/pipeline/ledger.json` is
   the single source of truth; `GXEMUL-SEC/tools/pipeline/gen_dashboard.py` renders `dashboard.html` (published as
   a claude.ai artifact) — write the ledger, regenerate, republish, NEVER hand-edit the output.
   Two divergences held deliberately per newer owner directives, recorded in PIPELINE.md's
   adoption section: the loop does not halt at phase boundaries, and a dead seat degrades
   (recorded by name) rather than pausing the fix.
1b. **THE DEAD-MAN SWITCH** — `bash GXEMUL-SEC/tools/nightly_check.sh [max_age_h]`.
   *** THE NIGHTLY BATTERY IS UNCONDITIONAL, YET NOTHING MADE THE ABSENCE OF A TERMINAL
   RECORD A FAIL. *** Every threshold in this harness lives INSIDE the run, so none of them
   can observe the run not happening — gate 5 cannot report that gate 5 never started. A run
   that never fires (logged-out session, task unregistered, reboot) produced NO RED ROW
   ANYWHERE. Named by an adjudicating seat on 2026-08-15 as the sharpest gap three rounds of
   harness work had left. It separates NEVER RAN (no verdict file, or one older than the
   window — the scheduled task is "Interactive only", so a sleeping machine skips it
   SILENTLY) from RAN BADLY (a verdict whose four signals disagree), and it treats a STALE
   verdict as the same failure as a missing one, because reading yesterday's green as today's
   is the "a green row means nothing" class in its purest form. It also checks the HEAD stamp
   and TREE_DIRTY: a verdict that does not name what it tested cannot be attributed.
   Negative-controlled in both directions on the day it was written. **It generalises a check
   that was being tracked by hand — and a check a human has to remember is a check that
   eventually does not happen.**
2. **One-command convening** — `./panel.sh <brief_file>` fires the five scriptable seats
   concurrently, verifies each produced a real answer, and reminds you to launch the
   sixth (Opus) via the Agent tool. `panel_ollama.py` is its cloud-seat helper. Low
   friction is what makes "always" actually hold. **ALWAYS invoke it as
   `bash GXEMUL-SEC/tools/panel.sh <ABSOLUTE brief path>`, never `./panel.sh`:**
   the session cwd DRIFTS (it has sat in `GXEMUL-SEC/regress` for whole rounds), and from
   there `./panel.sh` dies with "No such file or directory" — a SILENT zero-seat failure
   that looks like a completed run, so you review the previous round's stale seat files by
   mistake. After firing, confirm a NEW `_scratchpad/panel_<timestamp>/` dir exists and each
   seat file is > a few hundred bytes before trusting any of it (a 152-byte file is a
   truncated-thinking-model non-answer, not a review).
2b. **One-command adjudication** — `bash GXEMUL-SEC/tools/adjudicate.sh
   <finding_file> [tail_bytes]` fires the three Ollama cloud seats at ONE seat's finding
   and asks them to REFUTE it, not summarise it. panel.sh convenes a panel on a *brief*;
   this is the other direction, for when a single seat has produced research that needs
   independent scrutiny before it is acted on. It INLINES the finding (the cloud seats
   cannot read files) and takes only the TAIL by default, because Codex streams its
   reasoning into the output file and the answer lives at the end — a Codex research run
   here has exceeded 1 MB. Standing user directive (2026-08-13): **farm Codex 5.6-SOL at
   xhigh out in parallel across independent read-only queue items — credits are plentiful
   and slow runs are fine — then adjudicate what comes back with the Ollama seats.** Read
   -only Codex jobs do not contend with the build trees or rigs, so many can run at once;
   gates and probes still may not run while they do.

3. **Deterministic reinforcement** (`.claude/settings.local.json` hooks →
   `.claude/hooks/round_reminder.sh`): a **SessionStart** hook re-injects the panel
   directive each session; a **TaskCompleted** hook fires the moment a task is marked
   done and injects the end-of-round parallel-work step (harvest residuals → start the
   next item's brief/panel while gates run). The hook triggers on the event, so it does
   not depend on remembering.
4. **One-keystroke round** — `/round` runs a whole correction round end-to-end
   (reproduce → panel pass 1 → implement → panel pass 2 → gates → commit → parallel triage).

The panel's *quality* — good adversarial review, honest empirical adjudication — is
judgment and cannot be enforced; the layers above guarantee it is always *convened* and
that the parallel-work step always *fires*, which is the enforceable part.

## The self-sustaining monitor loop

The queue is worked as a continuous loop, kept alive by three things together: the
background-completion notifications (each finished panel seat / gate / battery re-invokes
the main loop), the TaskCompleted hook (fires the end-of-task triage), and — for idle gaps
where nothing is running — a `/loop` driver (self-paced; it re-invokes the main loop to
start the next item). **The loop runs on THIS machine**, because the panel is local
(localhost Ollama + Windows CLI binaries); a cloud/cron run cannot reach the panel.

Each cycle of the loop, the main model (Fable) does:

1. **Advance the in-flight task.** If a panel / gate / battery is running, do NOT start
   contending work — wait for its notification. Never two gate/harness invocations at
   once; before re-running a battery, explicitly stop any prior run (a rebuild does NOT
   stop it). One gate run, one gate log. **"Contending" includes CPU-heavy work that
   touches no tree at all** — panel seats, subagents, big greps. Gates carry wall-clock
   oracles: `gate_ab` allows each luna88k boot 300 s against a ~100 s normal, and in
   round 108 two research subagents plus interactive commands pushed HEAD past that
   budget, producing a FAIL indistinguishable from a real capability regression (a bare
   `ls` under WSL took >120 s in that window; re-run alone it passed 1:1:1). Serialize:
   gate first, then panel. Docs, queue triage and brief-writing are the safe filler.
2. **On task completion → panel review + suggestions.** Convene the full panel
   (`./panel.sh` + Opus) to review the completed work AND to surface new tasks — residual
   defects, sibling bugs, instrument gaps, follow-ups. After-panel findings have become
   the next rounds repeatedly.
3. **Fable adjudicates each suggested task.** For every new candidate the panel raises,
   the main model decides: is it worth adding? (real defect / reachable / in-scope /
   test-first-able vs. noise or duplicate.) Record the verdict; add the worthwhile ones
   with TaskCreate, drop the rest with a one-line reason.
4. **Assign parallelism.** For each added task, decide whether a subagent can start it
   NOW in parallel: read-only work (source scoping, byte-order/idiom investigation,
   reachability analysis, brief-drafting) parallelizes freely and should be handed to a
   background subagent to de-risk the round before its panel convenes (as the round-101
   byte-order subagent did). Tree-contending work (builds, probes, gates) is serial —
   it waits its turn behind the single gate/rig/build-tree writer.
5. **Claim the next task** and run the round: reproduce (test-first) → panel pass 1 →
   implement → panel pass 2 → gate (single clean run) → docs → commit/push → back to 1.

The loop ends only when the queue is empty or a task needs a human decision (destructive
action, genuine scope change). It does not stop for a long session.

**Panel roster for the loop — NINE seats by design, SEVEN live as of 2026-08-13** (Kimi 3
and the Fable seat are both quota-dead; see their rows above. A dead seat is a SEAT
FAILURE and is never counted as agreement — and never silently: say which seats answered
in the round's record). `./panel.sh` fires seven, Grok 4.6 added 2026-08-13: Codex 5.6-SOL (xhigh —
the CLI's "ultra" intent), agy 3.7 (`gemini-3.7-flash-high`, `--effort high`), Kimi 3 (max
effort), **Grok 4.6 (high, `--prompt-file` so no argv cap)**, Ollama glm-5.2:cloud,
deepseek-v4-pro:cloud, minimax-m3:cloud. Two more are launched in the same turn via the
Agent tool: **Opus 5** (`model: "opus"`) and **Fable 5** (`model: "fable"`). Fable also
ADJUDICATES the panel's task suggestions in its main-loop role — seat and adjudicator are
distinct hats; the adjudication happens in the main loop, not in the seat.

**ADJUDICATION IS A MAIN-LOOP ROLE THAT FABLE HOLDS BY PREFERENCE, and that distinction is
load-bearing: it DEGRADES rather than blocks.** With the Fable seat quota-dead on
2026-08-13 the adjudication still ran, in the main loop, and worked — 9 of 13 candidates
were dropped, folded or retired, two of which would have caused harm. User expects Fable
back on the token reset (2026-08-14) and intends to adjudicate with it then; until then
whoever holds the main loop adjudicates. What made it work was NOT the model: every one of
the five drops was settled by MEASUREMENT — a grep, a run, a five-rig spelling check — not
by judgement. **So the rule that earns its keep is: any candidate checkable in under about
two minutes gets CHECKED, not judged.** Keep that whichever model holds the hat.

## FAN OUT WIDE, CONVERGE ON ONE PANEL (standing user directive, 2026-08-13)

**"Utilise tokens as much as we can, but circle back for a full panel review."** The two
halves land on different resources, and that is the whole point:

* **UNLIMITED — fan out hard.** Agent-tool subagents (`model: "opus"`) and farmed Codex runs
  have no quota that has ever bitten. Read-only work parallelises freely: source tracing,
  reachability analysis, round design, brief-drafting, records audits. Launch several in one
  turn. This is where "use as many tokens as needed" applies, and today it was the single
  highest-yield resource — the measure-seat overturned the main loop FOUR times.
* **RATE-LIMITED — spend once, at the convergence point.** Measured 2026-08-13: the three
  Ollama cloud seats return HTTP 429 if two panels fire within ~20+ minutes (21 was not
  enough); Grok 4.6's free tier died after ~4 substantial invocations; Kimi is 403-dead.

  *** ALL THREE OF THOSE ARE NOW STALE, AND THE FIRST WAS MEASURED FALSE ON 2026-08-20. ***
  FIVE full panels fired in one evening, with gaps of 66, 33, 13, **5** and **11** minutes --
  two of them far inside the "~20+ minutes" threshold -- and **all six non-codex seats
  answered every one**, substantively:

  | panel | agy | grok | kimi | glm | deepseek | minimax |
  |---|---|---|---|---|---|---|
  | 22:20 | 15k | 9k | 87k | 8k | 3k | 10k |
  | 23:26 | 12k | 9k | 45k | 13k | 4k | 16k |
  | 23:59 | 12k | 11k | 72k | 19k | 5k | 11k |
  | 00:12 | 11k | 7k | 37k | 6k | 3k | 8k |
  | 00:17 | 14k | 13k | 61k | 14k | 5k | 9k |

  No 429, no degradation, no shrinking answers. Grok is PAID now and Kimi is back, so those
  two clauses expired months ago; the Ollama one expired without anyone re-testing it. **The
  "ONE full panel per ROUND" policy rested on this constraint, and the constraint is gone** --
  which is the same failure this file already records one paragraph below: *"A policy written
  around two dead seats outlived both of them by a week."* It happened again, to the paragraph
  that says it.

  **The rule that replaces it: fire a panel whenever there is a brief worth panelling, and let
  the seat check report a wall if one comes.** Do not ration against a limit nobody has
  observed. The one real cost is CONTENTION -- panel seats are CPU-heavy and must not run
  during a gate, which is a scheduling constraint and not a quota.

  **The single genuinely walled seat is CODEX**, and its wall is loud and unmistakable: five
  identical echoed-brief-plus-429 files of 26,992 / 11,180 / 10,036 / 8,323 / 12,414 bytes.
  *A size check alone scores those the largest answers in their panels* -- verify CONTENT.
  **So: ONE full panel per ROUND, not one per pass.** Four panels in one afternoon exhausted
  every rate-limited seat and left two reviews resting on two seats each.

**THE STOPPING RULE, and it is the one that was missing.** #392 ran SIX follow-up passes,
each finding defects in the previous pass's fixes, and the chain did not converge.
> A review finding gets FIXED IN THIS ROUND only if it is a MEASURED FALSE PASS or a WRONG
> RECORD. Everything else gets FILED.
That rule alone would have ended #392 at pass-2c instead of 2f.

**TWO TIERS OF GATE — "green gate" was ambiguous and cost a day.** 24 commits shipped on
2026-08-13 with the full battery never run once; a red battery could not have been attributed
to any of them.
* every commit: its own TARGETED gate (~1 min), in the same commit as the fix;
* WEEKLY (owner directive 2026-08-15: small unit tests any time, the full battery holds
  off to weekly - Saturdays 03:00, scheduled task `GXemul-weekly-battery`), alone,
  nothing else running: the FULL battery (~45 min, and `gate_ab` carries a load-sensitive
  wall-clock oracle, so it genuinely needs the machine to itself).

**FIX-TO-TEST RATIO: ship the detector WITH the fix, then stop.** ~1:1 in commits, ~30-40% of
effort — not the 100% that 2026-08-13 spent. More verification is NOT what prevents mistakes;
today was ~100% harness work and produced more errors than a normal fixing round. What caught
them was EXECUTION and ADVERSARIAL attempts, not additional checks: three rounds of tightening
a regex left it evadable, and one seat asked to break it found two evasions in a single pass.
**For each fix, ask one quota-free measure-seat: "what is the smallest edit that breaks this
property and still passes?"** One extra invocation per round, higher yield than any ratio change.

**FIVE MECHANICAL RULES, all from real 2026-08-13 errors, all near-zero cost.** These would
have prevented roughly six mistakes outright:
1. Write commit messages **from the diff**, never from intent (a message claimed a citation
   fix that no hunk made).
2. When correcting a claim, **grep for its siblings** before calling it fixed (an "un-fakeable"
   claim was corrected in one place and survived in three).
3. **Regenerate before grepping a generated file** — build-tree residue is not evidence about
   the generator (four rounds of #88 read a stale `src/Makefile` as configure's output).
4. Every reproduction must answer **"did it fail for the reason under test?"** — a guard that
   says "FAILED FOR SOME OTHER REASON, do not claim it" stopped two false results.
5. **Read the line before citing it** (one echo got cited four different ways across three
   passes, each believing it was fixing the last).

**The goal is not "no mistakes" — that is unreachable and chasing it produced the six-pass
chain. The goal is NO MISTAKE SURVIVES UNCHALLENGED**, which is achievable and which the
panel already delivers: every error made on 2026-08-13 was caught, usually within one pass.
What failed was scope control, not correctness.

## THE WITNESS LADDER — what "reproduce" means (adopted by adjudication, 2026-08-19)

The old rule asked "can this MACHINE boot?"; the right question is "can this CODE PATH be
executed?" — with `armbdt` as the proof (no ARM rig exists, yet gate 14 runs 261 real-decode
checks on `testarm`). But only executions that preserve the committed hardware selection and
routing count. The ladder, and what each rung licenses:

1. **`#include`/direct-call harness — NEVER a reproduction.** The discriminator is mechanical:
   *if it still compiles and still fails after the machine description and CPU/device dispatch
   are removed, leaving only a direct call, it was never a reproduction* — it is a restatement
   of the source. (It measurably distorts, too: m8820x's offline repro reported 1013/1015/11
   where the true numbers were 1007/1009/17, a NULL-callback stub artefact.) Such harnesses are
   DETECTORS and still ship as regression rows — graded by the vacuity taxonomy (must fail on a
   mutant), never by the witness clauses.
2. **Machine construction** (gate 9's mechanism, 23 types) — a reproduction ONLY for defects in
   code construction itself executes (init-time, e.g. the macppc heap OOB #23). Never for
   access-path defects: registration proves presence, not reachability.
3. **Cold-debugger probe** — a real guest instruction through real address decode and real
   `memory_rw`, on an UNMODIFIED in-tree machine description. EQUAL to a boot in admissibility.
   Exemplar: `regress/footbridge_sites_probe.py`.
4. **Boot** — a real driver reaches the path unaided. SUPERIOR for ranking: a probe proves a
   path CAN be reached; a boot proves it IS travelled (#437's SYNCHRONIZE CACHE is boot-only
   knowledge).

**A rung-2–4 witness is INVALID unless all of:** (i) it shows the defect symptom on the pre-fix
committed HEAD and goes green post-fix with the same script — this is test-first itself, restated
per-probe; (ii) it carries a LIVENESS control (a known value returns through the same decode) AND
a DEVICE-SIGNATURE control (the observed value could only have come from the device — RAM would
answer differently; **the footbridge probe's first draft returned 0x0 everywhere WITH ITS RAM
CONTROL GREEN**, so one control is not enough); (iii) the machine description and dispatch are
committed and unmodified — a machine or `device_add` introduced IN ORDER TO reach the site is
laundering, not witnessing.

**Witness vs detector — the timing line:** a REPRODUCTION licenses a fix and exists BEFORE the
edit. A DETECTOR defends the fix and may ship with or after it (`m8820x_sites_probe.py` shipped
three commits post-fix; **its own commit title says "detector"**). Grading a detector by the
witness clauses is a category error in either direction. Round prose saying "reproduced" without
naming the artefact is a records defect; the ledger `witness` field is the fix.

**Ranking — and the first version of this clause was WRONG, corrected 2026-08-19 by the
same adjudication that wrote it.** It said *order items by the strongest witness that
exists today*. **RUNG MEASURES REACHABILITY-PROOF STRENGTH, NOT HARM**, and using it to
schedule promotes the benign item over the damaging one. The case that proved it: `b120r`
has a rung-4 boot witness but a MEASURED guest-visible symptom of NIL (two transcripts
byte-identical), while `armbdt` has only a rung-3 probe and CORRUPTS GUEST DATA. So:
**a witness makes an item ELIGIBLE; SEVERITY and gate blind-spots order the queue.** Rung
is a floor on admissibility, never a priority. Strongest witness today — boot > probe >
construction **"No witness of either kind" is a CHECKABLE claim and must be checked, not asserted:**
dfreq's was measured false by building the witness in one session.

**Round scope (the reopening rule):** a witness makes a site ELIGIBLE, never mandatory. A round
takes ONE site; a second joins only if it is witnessed, in the SAME device and SAME semantic class
under the third doctrine arm (so one fix design covers both), and covered by the SAME detector
with no new oracle. **More witnesses create more candidate ROUNDS, never bigger rounds.**

**Ledger:** a row that closes with commits names its witness: `boot:<rig/gate>`, `probe:<path>`,
`construction:<gate>`, or `none` (documented-only). Forward-only from 2026-08-19.

## Round lifecycle, with the end-of-round parallel step

1. Claim the top TaskList item (or top of OUTSTANDING_BUGS "OPEN LIST").
2. Reproduce on the committed build per the WITNESS LADDER. No witness at rung
   2–4 → document instead, stop.
3. Design brief → **panel pass 1** → converge (empirically where split).
4. Implement (byte-identical in both trees for shared files); propagate to build trees.
5. **Panel pass 2** on the real diff.
6. `GXEMUL-SEC/regress/run.sh` → `REGRESS_PASS`. **Never run two harness/gate invocations
   concurrently** — but *** THE REASON GIVEN HERE FOR FOUR MONTHS WAS WRONG, corrected by
   measurement 2026-08-14: `selftest_mutation.sh` does NOT `rm -rf` the shared workdir. It is
   `T=$LOGDIR/mutation` (`:27`) and `rm -rf "$T"` (`:41`) — scoped to one subdirectory. *** Nor do
   the rig images serialise: both consumers open them read-only with `R:` and the overlay is
   pid-unique. **The real serialisers are three producer/consumer orderings and a load-sensitive
   oracle**, and they are worse than the wrong reason was: `gate_build.sh:64-65` WITHDRAWS
   `/tmp/gxsec-gxemul` and `$RIG/gxsec-gxemul` at gate start and republishes only at `:302-305`,
   while `gate_mips.sh:30` `need_exec`s it — concurrent runs make gate 4 `gate_skip` on a missing
   binary, which is **silent coverage loss scored as SKIP**; `gate_hygiene.sh:198-258` grades pty
   logs that gates 4 and 5 produce, so concurrency grades a partial log and yields **a wrong
   answer, not a crash**; `gate_ab.sh:42` `rm -rf`s `/tmp/gx-pristine` and `/tmp/gx-prebatch`,
   which `gate_upstream.sh:46-47` reads. A per-gate `LOGDIR` would NOT isolate them, because
   the ORDERINGS above are what serialise the gates — the driver's own hardcode is gone (#422:
   `drive_guest.py:207-211` honours `$LOGDIR`, `lib.sh:31` exports it), and it changed nothing
   about them. **~37 wall-clock oracles exist
   across the battery** (33 `while time.time() - t < …` loops in 18 probe files, plus
   `gate_asan_sweep.sh:60,62`, `gate_upstream.sh:74`, and `run_emu`), so converting one gate does
   not license concurrency anywhere.
7. Docs (CHANGELOG round block, REVIEW_FINDINGS, OUTSTANDING_BUGS), commit, push.
8. **End-of-round triage — always, before calling the task done:**
   a. Harvest every seat's residuals/dissents into OUTSTANDING_BUGS.md — after-pass
      findings have repeatedly become the next rounds (#340's after-panel found three).
   b. Sync the harness TaskList: mark done, TaskCreate anything new, re-rank.
   c. **Start the parallel work:** while gates run (~45 min for the full battery), prep
      the NEXT item — reproduction probe, brief, panel pass 1. Reading, brief-writing and
      panel seats parallelize freely; the SERIAL resources are the build trees, the rigs
      and the gate workdir (single writer, one gate run at a time).
9. Convene the panel on the next item as soon as its brief exists — the panel is never
   idle while a build or gate runs.

## Primary sources actually present (checked 2026-08-11)

`_scratchpad/` holds `ddi0100i.pdf` (ARM ARM, **plus `ddi0100i.txt`** from
`pdftotext -layout` — grep that), `idt_r30xx.pdf`, `mc88100.pdf`, `mips-iv.pdf`,
`mips32_volII.pdf`, `mips64_volII.pdf`, `mips_r4000.pdf`.

**THERE IS NO USABLE SH DOCUMENTATION** (checked 2026-08-13): `sh4_manual.txt` is ONE
BYTE and `sh4_err.txt` records zero extracted characters. So an SH round must cite the
SOURCE and measurements only — never an SH manual, and never a reconstructed-from-memory
page number. This is the same trap the ARM manual's absence set before 2026-08-11, and it
is the reason #357/#362/#365 shipped citations that came from model output. If SH work
needs the architecture, obtain a real copy first.

**The ARM manual was ABSENT until 2026-08-11.** Rounds #357/#362/#365 cite DDI 0100I page
numbers that came from **panel LLM output, not a local manual** — the load-bearing ones were
later checked against a genuine copy and held, but that is luck plus good seats, not process.
Cite only what you have read in these files. Two things a real reading corrected: **A2.8.3
does not exist** (A2.8 has only A2.8.1 and A2.8.2), and the endian-specific rotation statement
is not in A2.8 at all — it is in **LDR's own Alignment note, p. A4-44**.

## Build/measure quick facts

- Build inside `wsl -d Gentoo` (default Ubuntu lacks make); `rm src/cpus/*.o` first (the
  `#include`d `.c` files are invisible to the dep rules).
- est/ and GXEMUL-SEC differ by exactly 5 named files + SEC-only `dev_ne2000.c`; any
  other file must land byte-identical in both. Commit only GXEMUL-SEC files.
- Debugger `dump`/`examine` do NOT route through device handlers — read device state with
  guest loads via `step`. Instruction-combination work needs FREE-RUNNING execution: the
  #340 two-pass loop driver, breakpoint AFTER the sequence, instruction tracing OFF
  (recipe in OUTSTANDING_BUGS.md, 2026-08-03 entry).
- Probe harness: `_scratchpad/gxprobe.py` (don't hand-roll pty plumbing). Reconstruct the
  arc screen (`r49_screen.py` pattern); never grep the raw arc pty log for tokens.
- Invoke WSL scripts as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...`; write
  scripts to the session scratchpad, not git-bash `/tmp`.
