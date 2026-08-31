# GXemul 0.7.0 hardened fork — standing instructions (every session)

`GXEMUL-SEC/` is the git repo. *** OWNER DIRECTIVE 2026-08-22: LOCAL GIT ONLY -- DO
NOT PUSH. *** Commit as normal; do not run `git push`, and do not treat an unpushed
commit as an exposure (the older "an unpushed round is the largest single exposure"
line below is superseded for as long as this holds). The remote is left configured and
untouched -- it is the owner's plumbing, and nothing here removes or rewrites it.
(Historic note, still true if pushing ever resumes: push from Windows git-bash, never
WSL.) `est/` is its
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
   > ### *** AND THE RESTORE IS NOT FINISHED UNTIL THE BINARY IS REBUILT. THE SENTINEL
   > ### PROTECTS THE SOURCE; THE THING MEASURED IS THE BINARY. Measured 2026-08-27. ***
   >
   > ### *** AND IT IS NOT ONLY A MUTATION HAZARD. MEASURED AGAIN 2026-08-27, WITH NO
   > ### MUTANT ANYWHERE IN THE STORY. ***
   >
   > `build/gxemul` was found at `05:52:15` sitting on a `dev_wdc.c` of `14:56:12` -- nine
   > hours older than the only file that had changed, so it predated three shipped rounds.
   > **No script mutated anything.** A round propagated its edit into `build/src/` (as the
   > no-VPATH rule requires) and nobody rebuilt.
   >
   > **So part 1 passed and part 2 failed on a tree that was never mutant**, and the
   > SENTINEL DISCIPLINE CANNOT CATCH THIS CLASS AT ALL -- sentinels are dropped around
   > mutations, and there was no mutation. `CHECKPOINT.md` asserted `build/ CLEAN`,
   > written that same afternoon by the same loop that had done the propagating.
   >
   > > **THE TWO-PART CLEARANCE IS A ROUND-BOUNDARY OBLIGATION, NOT A MUTATION-RESTORE
   > > ONE. RUN IT; DO NOT ASSERT IT.** The checkpoint's build-tree section records the
   > > OUTPUT of the check, never a remembered state:
   > >
   > >     cmp -s build/src/devices/<edited>.c GXEMUL-SEC/src/devices/<edited>.c
   > >     [ build/gxemul -nt build/src/devices/<edited>.c ]
   >
   > Found by a rung-3 witness seat that noticed the impossible timestamp pair and
   > measured against its own `/tmp` tree instead, saying so plainly. **Nothing in the
   > harness would have reported it** -- and a `build/` measurement taken in that window
   > would have tested pre-`#481` code against a tree that `cmp`s clean.
   >
   > *Note the checker to build here is NOT another sentinel. It is two lines in the
   > checkpoint step, because the failure is a habit -- propagate, forget to rebuild --
   > and the carrier's own finding is that a rule fires when it lives where the decision
   > happens.*
   >
   > A mutant script restored `dev_dreamcast_asic.c`, `cmp`'d it clean against SEC, and
   > cleared the sentinel — exactly as this rule says. **It left a MUTANT `gxemul` on
   > disk.** The tell was an impossible pair of timestamps: binary `05:47:23`, restored
   > source `05:51:44` — *the binary was OLDER than the source it was supposedly built
   > from.*
   >
   > A later probe would then have measured the mutant against a tree that `cmp`s clean
   > and carries no sentinel — **the stale-binary trap reached from the other side, and
   > with the sentinel discipline fully obeyed.**
   >
   > **THE CLEARANCE CONDITION IS TWO-PART: source `cmp`s clean against SEC AND
   > `[ binary -nt source ]`.** Rebuild inside the restore, and leave the sentinel in
   > place if the rebuild does not produce a fresh binary — a sentinel that outlives its
   > mutant costs one restore; one cleared over a mutant binary costs a wrong
   > measurement nobody suspects.
3. Commit+push at every green gate — an unpushed round is the largest single exposure.
4. *** KILL TABLES RUN IN A SCRATCH CLONE BY DEFAULT. Mutating `build/` is the EXCEPTION and
   carries its stated reason in the checkpoint. Owner decision 2026-08-28, on measured
   practice rather than on proposal. ***

   `#489`'s pass-2 seat ran a nine-log table in `/tmp/gxopus489` (a relocatable `cp -a` of
   `build/`) **CONCURRENTLY with the main loop's own table holding `build/.MUTANT`**, wrote
   into no project tree, and left its scratch `cmp`-clean. **Two tables at once, zero commits
   blocked, zero restores owed.** The relief is measured.

   > **The obvious objection is backwards, and it is worth stating because I raised it: a
   > mutant table NEVER measures the battery's binary.** Every measurement is of a MUTANT
   > binary built over baseline sources. The load-bearing identity is SOURCE identity with the
   > intended baseline, which `cmp` establishes in a clone exactly as in `build/` -- and
   > `build/`'s own binary has twice been caught STALE over clean sources. *A clone that
   > rebuilds its baseline before mutant 1 is more trustworthy than an in-place run inheriting
   > whatever binary sat there.*

   **The recipe that makes the default safe, each a checkpoint line:** (1) **NAME THE
   BASELINE** -- HEAD or the round's post-fix working set -- and `cmp` the files-to-be-mutated
   against it before mutant 1, since a clone inherits whatever `build/` held mid-round;
   (2) **rebuild the baseline binary IN THE CLONE** and check `[ binary -nt source ]` -- the
   base-table run doubles as the freshness proof; (3) clone-local sentinel plus the
   frozen-copy driver rule, unchanged; (4) the volatile-path rule **with extra force** -- /tmp
   evaporates, and copying any number a durable record will cite into `regress/artifacts/`
   comes BEFORE the record is written.

   **For the `build/`-mutating exception nothing is overturned: TOTAL blast radius, two-part
   clearance.** Narrowed in population, unchanged in scope. *No checker -- there is no
   mechanical observable for "should have cloned", and a check that cannot fail is worse than
   none.*

## *** WHERE A LESSON GOES: STRUCTURE FIRST, PROSE ONLY AS FALLBACK. ***
## Owner-adopted 2026-08-26. Read this before adding anything to this file.

> **Every incident must first propose a STRUCTURAL landing spot — a check, a gate section, a
> brief-template line, a script practice. A carrier paragraph is the FALLBACK, used only when
> no structure can hold the lesson. And a rule that earns its SECOND INSTANCE while sitting in
> this file has thereby proven it was mis-filed as prose.**

**The evidence is one day's own record, and it falls on both sides.** What changed outcomes was
structure: `check_seats_read.py` was taught ONE filename mapping and surfaced three unread
reviews the same day; `panel.sh` gained a fourth Ollama seat and it has answered in every panel
since; a kill table now runs from a frozen copy. What failed *while written down here* was prose:
the frozen-copy rule was violated by its own author hours after he wrote it, the
guest-drivable-`fatal()`-needs-a-latch rule went unconsulted by a round that debated exactly that
question, the unread-review class reached its third instance, and the frozen-number class its
fourth generation.

> **THIS FILE IS NOT FAILING AS MEMORY. IT IS FAILING AS A TRIGGER.** The frozen-copy rule was
> *cited by the person breaking it*, on a different object, in the same hour. Knowing a rule and
> having it fire on the right object are different problems, and only the second one is solved by
> writing more.

**The carve-out is real and must not be eroded:** judgment rules — option-set completeness,
adjacency, severity ranking — cannot be mechanised and belong here. But note *why* the
premise-audit paragraph is the one piece of prose that demonstrably works: it lives in the BRIEF
TEMPLATE, the artifact present at the moment of decision. **That is structure in the sense that
matters — text located where the decision happens, not text located where the reasoning was
recorded.**

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

*** DO NOT LOOK FOR SEAT STATUS IN THIS FILE. *** Live status is `panel.sh`'s seat check and
the ledger; both are generated and neither can go stale. **Two status snapshots used to live
here — an 08-19 table headed "CURRENT" and an 08-14 one below it — and by 2026-08-26 the first
was wrong about every seat it named while still calling itself current.** A status line in an
auto-loaded file is a wrong record waiting for a calendar. The 08-14 table is kept below for its
REASONING only; read no status out of it.

**THE ONE LESSON WORTH THE SPACE, and it cost a real panel to learn: VERIFY THE CONTENT, NEVER
THE SIZE.** Codex once returned the **LARGEST file in its panel — 26,992 bytes** — and it was the
echoed brief followed by "You've hit your usage limit", twice. *A size check scores that the best
answer of the nine.* The failure mode is a big file, which is why every seat check in this
project greps the content and the TAIL rather than measuring bytes.

### *** A WALL IS A MOMENT, NOT A STATE — MEASURED 2026-08-23, and it CONTRADICTS the
### "never by a date" line in the Fable row below. ***

*** AND THE SAME DAY, THE OTHER HALF OF THAT RULE WAS CONFIRMED FOR THE THIRD TIME:
AN ACCOUNT-STATE CHANGE REVIVED A SEAT THAT TWO FIRINGS HAD FOUND WALLED. ***

The Fable seat failed twice on 2026-08-23 with `You've reached your Fable 5 limit` — the
second firing deliberate, per the re-fire-a-walled-seat-once rule. **The owner then ran
`/login`, and the next firing returned BOTH liveness tokens** (the prompt nonce and a
verbatim quote from `CHECKPOINT.md`), so prompt delivery and file access were proven
rather than assumed. It then produced the round's adjudication: seven wrong records and
one undischarged obligation.

**So both halves now have measured instances:** Kimi revived across a date boundary with
no account change (cause NOT established), and Fable has now revived twice on a `/login`.
The operational rule is unchanged and is the cheap one: **TEST THE SEAT, do not reason
about why it might be back.** One Agent call with a liveness token settles it in seconds.

**AND THE HOLD WAS WORTH IT, WHICH IS THE PART WORTH RECORDING.** The round was held
uncommitted for this seat by owner decision across two failures. Waiting cost nothing —
the work was checkpointed and unrelated work was split into its own commit — and the
seat that eventually answered found the round's one L3 obligation, which no other seat
had named across two full panels.


Kimi walled mid-panel at 23:01 with a `403 usage limit for this billing cycle`. **One hour
later, across the date boundary, a liveness test returned its token on the first try.** No
account-state change was made. So the sentence below — *"Both 'dead' Anthropic-side states
this project has seen were revived by ACCOUNT-STATE CHANGES … never by a date"* — has a
counter-example. **Cause is NOT established** (a billing cycle rolling at midnight is a
guess, not a measurement); what is established is that the seat was walled and then was not.

**The ADVICE in that row was right even though its stated reason was wrong**, which is worth
keeping separate: *"DO NOT ASSUME A CALENDAR DATE RESTORES A SEAT — TEST IT"* is exactly what
settled this, in one invocation and about four seconds.

**Two harness consequences, both applied:**
* **A WALLED SEAT IS RE-FIRED ONCE before the round closes.** It costs a minute and recovers
  a seat the round would otherwise silently lose. The owner caught this one only because the
  seat showed as available in their own UI — which is a human noticing, i.e. the thing this
  harness exists to stop depending on.
  > *** THE RULE IS SOUND AND "BOTH APPLIED" WAS FALSE ABOUT THIS HALF. Measured 2026-08-26
  > by an audit of this file. *** `panel.sh` printed **"re-firing once (a wall can be minutes
  > long) ..."** and then `return 2` — and every caller is a bare `check "name" "$file"` whose
  > exit status is discarded, with no seat command re-invoked anywhere afterwards. **Nothing
  > was ever relaunched.**
  >
  > **That is worse than a stale citation.** A stale citation misleads a reader who follows
  > it; this printed a claim of ACTION to the operator at the moment a seat was lost, so the
  > one person who could re-fire it by hand was told it had already been done. It is the
  > failure `panel.sh` itself warns about sixty lines earlier — *"a documented check that
  > cannot fail, which is worse than no check because it reassures."*
  >
  > The message is now an INSTRUCTION, not a false report. **Automatic re-firing is FILED,
  > not done**, because it is a behaviour change to the script every panel runs and it owes
  > two negative controls: prove the retry fires on a walled seat, and prove a seat that
  > answered is NOT retried.
### *** THE CHECK-THAT-CANNOT-FAIL: TWO INSTANCES IN ONE DAY, AND THE HUNT FOR A THIRD
### CAME BACK EMPTY IN THE PLACE YOU WOULD EXPECT IT. Measured 2026-08-26. ***

Two shortcuts were found inert on the same day, and both had the same shape -- **a cheap
substitute for a real test, which returns the same answer whether or not the thing it checks
is true**:

* `panel.sh` printed **"re-firing once (a wall can be minutes long) ..."** and re-fired
  nothing; every caller discards the `return 2`.
* The seat table called `grok models` **"itself a cheap tier check"** for whether the paid
  subscription is live. Running it prints **`You are not authenticated.`** and lists both
  models anyway -- the list is served without auth, so it answers identically in both states.

**THE HUNT FOR A THIRD WENT TO THE GATES AND FOUND NOTHING, WHICH IS THE PART WORTH
RECORDING.** 251 `check` rows were scanned for a want that is literally the got expression.
Twenty matched -- and **all twenty are the GUARDED parse idiom**, where an `if` arm emits
`"no" "yes"` and the `else` arm emits `"yes" "yes"` for the same label, so the row fails
loudly when parsing fails. **Zero unguarded.** A row of mine that looked self-comparing
(`"${wfres%/*}" "${wfres#*/}"`) was checked too: the two halves are the numerator and
denominator of one probe string -- different quantities -- and it reds whenever the score is
below its own denominator, with a companion row pinning that denominator to a literal.

> **SO THE CLASS LIVES IN PROSE AND SHORTCUTS, NOT IN CHECK ROWS.** The gates are written by
> people thinking about failure; the shortcuts are written by people trying to AVOID running
> something. **A check that cannot fail is almost never a badly-written assertion here -- it
> is a claim that some cheap observable stands in for an expensive one.** Ask of any such
> shortcut: *what does it print when the thing is FALSE?* Both instances above answer "the
> same thing", and neither had ever been asked.

*Both were found by the exemplar audit, not by a gate, and neither could have been: one is a
`say` in a shell script and the other is a sentence in a table.*

* ***`panel.sh` COULD NOT SEE THIS WALL AT ALL.*** Its check only caught the ECHO-ONLY shape
  (brief echoed, tiny payload — the codex signature). Kimi's wall was **36 KB of real content,
  98% novel, ending mid-sentence with the notice**: payload huge, echo absent, invisible to
  every test it had, and printed as a healthy answer. It now also checks the TAIL, using the
  same POSITION discriminator `seat_verdicts.py` already used — which is why the extractor
  caught what the panel script missed.

### *** A FOURTH CLASS, MEASURED 2026-08-24: ONE SHARED SERVICE BEHIND TWO SEATS.
### THE ROSTER SAYS NINE; AVAILABILITY SAYS EIGHT. ***

Opus 5 failed three consecutive times on `API Error: 529 Overloaded`. Fable 5 was
then asked to do its job -- it is the only other seat with build and execute access
-- and failed on **the same error**. Meanwhile all seven CLI/cloud seats answered
normally inside the same window.

So the diagnosis is not *"the Opus seat is overloaded"*. **The Agent-tool path is
overloaded, and both Anthropic seats sit behind it.**

It is none of the three classes already recorded: no quota text, so the wall rule
passes it; substantive partial answers on two of the four attempts, so the stall rule
passes it; and the CLI seats share no transport with these, so the daemon rule does
not apply.

> **THE CONSEQUENCE, which matters more than the diagnosis: the two Anthropic seats
> are independent for REASONING and correlated for AVAILABILITY.**  They are the only
> two that compile and run. A panel that counts nine seats and loses both to one
> outage has lost **all** of its compile-and-measure capacity, and a round whose
> remaining obligation is a MEASURED KILL then has no fallback anywhere in the
> roster.

That happened on `#462`: everything was measured except the mutant table, and the
only seats that could produce one went down together. **A held round is the correct
response** — the owner chose it — but the roster should not be read as nine
independent chances at a measurement. It is seven readings and one measuring
capability with two front ends.

*** AND IT CAN. ESTABLISHED 2026-08-24, DURING THE OUTAGE THAT PROMPTED THE
QUESTION. ***

`agy` was given a bounded capability test -- build the tree unmodified, then build
ONE mutant and score it -- with an explicit instruction to say so plainly and stop
if it could not. It produced `/tmp/gxagy/gxemul` (6.1 MB), applied the mutant
correctly (2 `idata = 0;` against the repo's 3), and ran the 44-row probe against
its own binary. **It builds and it measures.**

> **So the roster has THREE compile-and-measure front ends, not two, and only two of
> them share the Agent-tool service.**  `agy` is on an entirely separate path, which
> is exactly the property the fourth failure class showed was missing.

Two cautions, both from how this test was set up rather than from anything agy did:
* **It has no sandbox.** `codex` is read-only and `grok` is plan-mode by
  construction; `agy` runs with `--dangerously-skip-permissions`, so the BRIEF is the
  only thing keeping it out of the repo. Spell out "copy the tree, build the copy,
  never write to GXEMUL-SEC" every time, and verify afterwards rather than trusting.
* **Give it the build traps explicitly.** `-d Gentoo` (the default distro has no
  `make`), `rm` the `.o` first, and check `[ binary -nt source ]` because `MAKE_RC`
  has been observed reporting 0 on a failed build. It followed all three when told;
  none of them are guessable.

*The capability question sat unasked for months and cost this round its fallback.
It took one bounded invocation to answer. Ask the cheap question early.*

### *** A THIRD SEAT-FAILURE CLASS, MEASURED 2026-08-22: THE TRANSPORT, NOT THE SEAT. ***

All THREE Ollama seats returned 155 bytes each in one firing —
`ConnectionRefusedError(10061)` on `localhost:11434`. **The daemon was not running at all.**
Not a wall, not a stall, not a brief defect: the models were available the whole time and one
`ollama serve` recovered every one of them into the same panel dir.

**It defeated every rule this file had.** It carries no quota keyword, so the wall rule passes
it. It is 100% novel against the brief, so the echo rule passes it. It is short — but so is a
stall, and this file already warns that short does not mean dead. `seat_verdicts.py` therefore
filed all three under *"answered, NO VERDICT LINE (format miss)"*: **three DOWN seats recorded
as live seats with bad formatting**, which is the seat-failure-counted-as-agreement shape in
its purest form.

Fixed in both places, and the two fixes are different on purpose: `seat_verdicts.py` reports
`SEAT DOWN` and **separates "daemon refused the connection" from "transport/model error"
because the remedies differ**, and `panel.sh` now PRE-FLIGHTS the daemon and starts it, since
starting it is cheaper than losing three seats. If it still will not come up the script says
so loudly rather than leaving it to be read out of three error files.

**The general rule: a WALL is the seat refusing and you wait it out; a REFUSED CONNECTION is
the transport being absent and one command fixes it. Reporting the second as the first
silently gives up seats that were available all along.** Check the daemon before blaming the
seat — `curl -s localhost:11434/api/tags` is the whole test.

### *** A SIXTH CLASS, MEASURED 2026-08-25: ONE TRANSPORT WALLED, ANOTHER LIVE — AND THIS IS
### THE ONLY CLASS WHERE THE SEAT IS AVAILABLE THE WHOLE TIME AND NOBODY ASKS. ***

*(Numbering, because a reader counting headings in this file finds third, fourth, then sixth:
**the FIFTH is `seatthinkburn` in the ledger — an empty response wrapped in 260 KB of thinking,
which every size check scores as the best answer in the panel — and it was never written up
here.** The hole is in this file, not in the count. Filed, not lost.)*

### *** THE FIFTH CLASS, WRITTEN UP AT LAST — AND THE 2026-08-26 INSTANCES SHOW IT IS DRIVEN BY
### THE BRIEF, NOT BY THE SEAT. ***

`deepseek-v4-pro:cloud` returns `"response": ""` inside a JSON object whose `thinking` field is
hundreds of KB, with `done_reason: "length"` and `eval_count: 65536`. **It spends its entire
output budget on hidden reasoning and never emits an answer.**

It is none of the other four classes: no quota text (not a WALL), nothing echoed (not the
echo-only shape), the daemon served it for minutes (not a REFUSED CONNECTION), and the other
cloud seats answer normally in the same firing (not the shared-transport outage).

*** AND IT DEFEATS EVERY SIZE-BASED CHECK: the burn is one of the LARGEST files in the panel. ***

**THE CORRELATION, measured across four firings in one day:**

    090604    4,032 b   normal      simple brief
    190055    2,845 b   normal      simple brief
    222557  142,525 b   BURNED      three-claim band-arithmetic audit
    230207  222,981 b   BURNED      five questions across two rounds

**Same seat, same transport, same day — the burns track BRIEF COMPLEXITY.** That is the
carrier's oldest packet-fed lesson recurring: their behaviour is governed by the brief, and this
project once spent DAYS misdiagnosing a brief defect as a seat outage.

**WHAT IS LOST IS NOT NOISE.** The second burn ends mid-sentence — *"So verdict likely NOT
RATIFY due to #467. But maybe the question is from a panel"* — **it had reached a verdict and was
second-guessing itself when the budget ran out.** On that same panel the other dissenting seat
found a live defect in code shipped an hour earlier, so a lost dissent is real cost.

> **DETECTION IS SOLVED — `seat_verdicts.py` keys on `done_reason`, not size, and named both
> burns correctly. THE MITIGATION IS THE BRIEF: keep a packet-fed brief to ONE question with its
> facts inlined.** Splitting a complex audit across two firings costs one extra invocation and
> preserves the answer.

The kimi CLI returned `provider.auth_error: 403 You've reached your usage limit for this billing
cycle`. That is a genuine wall, correctly detected, and it was recorded as a down seat.

**kimi was never down.** `curl -s localhost:11434/api/tags` lists **`kimi-k3:cloud`** alongside
the three named Ollama seats, and three earlier panel dirs each hold a healthy `ollama_kimi.txt`
(17,684 / 17,382 / 9,227 bytes) — so the substitute was being fired BY HAND and then quietly
stopped being. `panel.sh` launched exactly one kimi seat, the CLI, with its Ollama seats hardcoded
to glm / deepseek / minimax.

**FIXED IN THE SAME COMMIT THAT SHIPPED THIS PARAGRAPH (`faffad7`), AND THE PARAGRAPH DID NOT SAY
SO — which made it a wrong record from the moment it landed.** `panel.sh` now fires `OLLAMA4 =
kimi-k3:cloud` as a fourth Ollama seat, and its seat check reports a walled CLI with a live
substitute as ONE SEAT COVERED rather than one lost. It has answered in every panel since.
`check_seats_read.py` and `seat_verdicts.py` both learned the mapping in the same commit, so a
substitute answer is no longer invisible to section G. *A present-tense description of a tool,
written in the commit that changes the tool, is stale before anyone reads it.*

> **WHEN A SEAT WALLS, ASK WHETHER THE MODEL IS REACHABLE BY ANOTHER TRANSPORT BEFORE RECORDING
> IT DOWN.** The wall rule says wait it out; the daemon rule says one command fixes it. This
> class says **neither applies — the seat is answerable right now, on a different road.**

**Why it is worse than an undercount, which is how the ledger row first described it.** A
mis-tallied seat is a reporting defect a reader can correct. Here the roster records no failure
to investigate at all: every panel since the CLI wall ran one seat short while a working
transport sat idle. *That is the seat-failure-counted-as-agreement shape with an extra step,
because the missing seat never even appears as missing.*

**The cheap check is the same one the daemon rule already mandates**, read for a different fact:
`api/tags` answers "is the transport up?" AND "which models can I reach?" — it was being used for
only the first. A walled CLI seat costs one `grep` against that list to recover.

*Recovered the same minute by hand onto the live panel dir. The `panel.sh` fix was deliberately
NOT applied while a panel was running: bash reads a script incrementally, so editing a running
script is its own defect class.*


**A SHORT ANSWER AND A DEAD SEAT ARE NOT THE SAME THING.** Grok's file was 119 bytes when first
sampled — opening line only, "I'll read the full offloaded packet first" — and looked exactly
like the minimax stall this file spent days mis-attributing. It was MID-ANSWER. Sample twice
before calling a seat dead; the size check cannot distinguish slow from dead.

**SEAT RANK DOES NOT SETTLE FACT — measured twice today, in both directions.** The flagship seat
corrected a false "strict superset" claim about header closures and its correction was ALSO
false; `gcc -E -H` settled it (two exceptions, not the one either of us named). And a reading
seat's claim that production `fatal()` exits — which would have made a shipped correction into
guest-reachable process death — was refuted by opening `src/core/debugmsg.c:384`. **Both were
settled in under two minutes by looking.**

*** AND THE REFUTATION'S REASON WAS ITSELF FALSE, corrected 2026-08-21 after TWO seats
challenged it independently and a direct reading settled it. *** This paragraph said `fatal()`
is "byte-for-byte `debug()`". **It is not.** `debug()` (`:365-381`) computes
`ss = single_step || about_to_enter_single_step`, decrements `v` when `emul_executing`,
increments it when stepping, and then **`if ((quiet_mode && !ss) || v < 0) return;` at `:375`**.
`fatal()` (`:384-390`) has **no early-out at all** — it goes straight to `va_debug`. The
conclusion held (neither exits), but the reason given was wrong, and a wrong reason gets reused:
it was cited a second time before anyone opened the file.

**Two live consequences, both measured:** `fatal()` cannot be silenced by `-q`, which is why a
guest-drivable `fatal()` needs a latch and not a verbosity flag; and **a probe CAN distinguish
the two, contrary to the older rule 6** — free-running gives `v < 0` so `debug()` returns while
`fatal()` prints, whereas single-stepping raises `debug()` above the threshold and both print.
**That distinction is conditional on `verbose == 0`**: run with `-v` (or `-i`/`-r`, which imply
it) and free-running gives `v == 0`, `debug()` prints, and any row resting on the difference
goes quiet without saying so.

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

**Nine seats by design. `panel.sh` fires EIGHT scriptable transports as of 2026-08-25 (the
eighth is `kimi-k3:cloud`, the kimi SUBSTITUTE -- see the sixth seat-failure class). The
count below is the 2026-08-14 snapshot: SEVEN answering, `panel.sh` firing seven scriptable
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

*** BATCHING THE FLAGSHIP SEAT IS RIGHT FOR CLOSURES AND WRONG FOR RULE QUESTIONS —
measured 2026-08-22 on a 46-row batch, by the seat that was being batched. ***

Its finding, and the evidence is inside the batch: **the closures lost nothing by waiting.**
Every row was gate-green with its record written, and five days of delay produced exactly one
hold text overtaken by events (`sgiarcbiosoob` still said "not committed yet" after its oracle
landed) and one state-vs-substance mismatch (`es438` marked "dropped" on shipped, witnessed,
reviewed work — *a future reader who trusts states reads that as "not done", which is false*).

**But the RULE questions did not wait safely.** #451 had to answer its own accept-row question
locally, by building both mutant forms, because the seat that adjudicates that rule was
batched; and the failability rule was minted, corrected and re-corrected across #448/#449 with
the flagship signature arriving days later. Nothing broke — the measuring seats covered it —
but *that is the panel silently absorbing a missing seat's function*, which is the thing the
seat ledger exists to refuse to count as agreement.

> **SPLIT THE QUEUE BY QUESTION TYPE.** CLOSE / KEEP-OPEN sign-offs on shipped work batch
> freely; weekly is fine, and a 46-row batch proved it. Rows raising a **RULE QUESTION** get
> the seat at the next round boundary, cap about a day — they change how future rounds run, so
> every day they wait is rounds executed under an unadjudicated rule. The cost is small: rule
> questions were 6 of 46, and they are the short ones.

> **A STAGE HELD *FOR* A SEAT MUST CARRY THE QUESTION IT IS HELD FOR.** Three of the four
> meta-rows in that batch carried identical boilerplate with no question in them, and the
> question had to be reconstructed from the row's subject. The two rows that named their
> question explicitly were the easiest to answer *accurately*. One habit, and it makes the
> batch both faster and safer.
>
> ### *** THAT HABIT WAS AT **ZERO** ON 2026-08-26, WHICH IS WHY THE RULE IS NO LONGER PROSE.
> ### It is now `check_stage_panels.py` + a `hold_question` field. Owner-decided the same day. ***
>
> **THE NUMERATOR IS THE CLAIM AND IT IS ZERO. THE DENOMINATOR IS DELIBERATELY NOT A NUMBER
> HERE, because writing one is what went wrong.** This clause read "0 FOR 18" and named no
> UNIT -- and when the exemplar audit challenged it, FOUR counting methods gave FOUR answers:
> the audit seat 21 stages / 18 rows; a bare entry-grep of mine 30 / 26 (it counted ENTRIES,
> so two markers in one stage counted twice); the checker's phase rules 26 / 22; and its full
> rule set, excluding closed rows, 24 / 21. **I could not reproduce the seat's figure, so I
> am not writing any of them down** -- that is precisely how the original number got there.
>
> To re-derive it at any commit: `git show <rev>:tools/pipeline/ledger.json` and count held
> markers **one per (row, phase), recognised phases only, excluding closed rows** -- which is
> what `check_stage_panels.py` does. **STAGES AND ROWS ARE DIFFERENT UNITS and a count that
> names neither cannot be checked.**
>
> Every held stage then in the ledger carried a DISPOSITION note where a
> question belongs -- *"FILE - no measurable effect until a caller survives"*, *"a policy, not a
> round"*, *"FILE - offer as a rider in b120u's first panel"*. Each is a true statement about
> the row. **None is a question a seat can answer.**
>
> **This is the carrier diagnosing itself, exactly as the structure-first rule at the top of
> this file predicts.** The rule was written down, it was minted from a measured incident, it
> sat in an auto-loaded file -- and the very next population of held rows scored zero. *Knowing
> a rule and having it fire on the right object are different problems, and only the second is
> solved by writing more.*
>
> **Why it is worse than untidy:** a seat fired against a disposition note has to GUESS what it
> is being asked, and a guessed question yields an answer to the wrong question **that still
> looks like a discharged stage**. That is the seat-failure-counted-as-agreement shape moved
> one step earlier -- earlier, and therefore harder to see, because the stage shows a real
> answer from a real seat.
>
> **The check is dated-cutoff, the same shape `check_bugfile_sync.py` uses**: stages whose
> newest entry postdates `HOLDQ_CUTOFF` FAIL; the eighteen older ones are reported every run
> and not failed. That is deliberate and it is not timidity -- a rule that retro-fails
> eighteen rows blocks the next commit on reconstruction nobody scheduled, and **a rule that
> does that gets switched off**, which is worse than a rule that warns. Negative-controlled in
> both directions on the day it landed: injecting a post-cutoff hold with no question turns it
> red and names the row; adding the question turns it green again.

*** SUPERSEDED 2026-08-16 BY OWNER DIRECTIVE: FULL PANEL ON EVERY STAGE. ***

**THE RULE NOW: every stage — assess, research AND review — runs all nine seats before the round
moves on. If a seat cannot be run, STOP AND ASK THE OWNER.** Do not degrade quietly; that is
exactly what this replaces. `regress` remains FABLE-ONLY (separate standing directive), and stages
that ran before 2026-08-16 are grandfathered forward-only and carry an explicit annotation entry so
their blanks do not read as seat failures.

*** EVERY LEDGER ENTRY WRITTEN FROM A PANEL MUST NAME ITS PANEL DIR. One field, and it
is what makes section G work at all. Learned 2026-08-24 by breaking it for a whole day. ***

Seven panels ran that day, all answering. The ledger recorded two or three seats per stage;
about **forty seat-entries were missing**, and one seat's 7.6 KB answer had never been
opened at all -- only its verdict line read.

**The gates caught ONE of the seven, and the reason is structural.** Section G's scope
trigger is an entry that CITES A PANEL DIRECTORY. The ledger cited six `panel_20260823_*`
dirs and **zero** `panel_20260824_*` dirs -- so G never looked at any of that day's panels.
Section H compounds it: it counts the per-stage seat union ACROSS DATES, so a new panel on
a row that already had seats from an earlier one folds in invisibly.

> **The defect was the PRACTICE, not the gates.** The day before, every panel got cited and
> G enforced the rest mechanically. Nothing in the tooling changed.

Each time the citation was added, that panel came under G's scope in one step -- and on the
last one G immediately reported *"1 seat answers exist on disk and are recorded NOWHERE"*.
Its wording is the rule worth keeping: **a seat that answered and was not recorded is NOT a
seat failure and NOT agreement -- it is an UNREAD REVIEW**, and this project has twice found
real defects sitting in one.

**And a counting trap that costs exactly two seats every time:** the two Agent seats leave
NO FILE in the panel dir. Any check that counts files under-counts by two, and they are
precisely the two most likely to have found something.

Mechanically enforced by `GXEMUL-SEC/tools/pipeline/check_stage_panels.py`, wired into `precommit_check.sh` as a
hard section H. Note it complements rather than duplicates section G: **G verifies that a seat which
ANSWERED was recorded; H verifies the seat was FIRED at all.** Neither catches the other's failure.

> *** H's GUARANTEE IS NARROWER THAN "FIRED AT ALL", and the overclaim was measured
> 2026-08-26. *** H reads LEDGER ENTRIES, not process execution. It **skips stages that
> never started**, treats a one-seat stage as a filing rather than a short panel, and
> accepts a seat entry without any proof a process ran. The honest statement is: **a
> STARTED, non-filing stage must carry nine recorded seats.** A stage that was never begun,
> and a seat entry written without firing anything, both pass. The policy is unchanged and
> right; the mechanical guarantee is smaller than the sentence claimed.

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
| Codex 5.6-SOL (xhigh/ultra) | `codex exec --sandbox read-only --skip-git-repo-check -m gpt-5.6-sol -c model_reasoning_effort="xhigh" "$(cat brief)" < /dev/null` — the `< /dev/null` is required. Windows argv caps ~32 KB. *** `panel.sh` NOW HANDLES THIS ITSELF, as of 2026-08-30 -- do NOT hand-trim a brief for it. *** Above `ARGV_CAP` (30000) codex and kimi are fed a POINTER (`PTR_PROMPT`: read `$BRIEF_ABS` and review it as its own Questions section directs) instead of the contents; below it the inline form is byte-unchanged. Both are FILE-READING seats, so this costs nothing -- and grok (`--prompt-file`) and agy (`--add-dir`) were already immune, leaving these two as the only argv-fed seats. **The block previously WARNED and then launched anyway**, which cost both seats on a 38 KB brief and is the check-that-cannot-fail family's sibling: *a message reporting an ACTION the code does not take*, exactly like the re-firing message. `PANEL_ARGV_CAP` overrides the cap **only so the branch is testable in both directions** without keeping a 38 KB fixture; it is not a tuning knob. Controlled by extracting the real decision block out of `panel.sh` and `eval`ing it -- 6/6 rc=0 fixed, EXTRACT FAILED rc=9 pre-fix. **A HAND-WRITTEN BRIEF STILL NEEDS TO BE READABLE**: the pointer form only helps seats that can open the file, so it is not licence to grow briefs without limit -- the packet-fed Ollama seats still get the whole thing POSTed and still burn budget on it. Never the trailing-`-` stdin form (died silently once). |
| agy 3.7 (high) | `agy --dangerously-skip-permissions --add-dir <dir> --print-timeout 30m --model gemini-3.7-flash-high --effort high --print "<short prompt pointing at brief file>"` — reads files via `--add-dir`; no stdin prompt mode. **Model set by user directive 2026-08-13.** PASS BOTH `--model` and `--effort`: the effort tier is baked into the model name (`-high`/`-medium`/`-low`) AND there is a separate `--effort` flag, so naming only one leaves the other at its default. Before this, `panel.sh` passed NEITHER while printing "agy(high)" — the banner was an overclaim. **`agy models` is the authority on valid names** (it lists gemini-3.7/3.6/3.5-flash and 3.1-pro tiers, plus claude-sonnet-4-6 and claude-opus-4-6-thinking); a wrong name is a SEAT FAILURE, so re-check after any CLI upgrade.  *** AND IT HAS A QUOTA.  MEASURED 2026-08-30, THE FIRST agy WALL ON RECORD, AND IT ARRIVED WHILE THE SEAT WAS BEING DELIBERATELY PUSHED. ***  `Error: Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 1h56m37s.` -- **111 bytes, on stderr, with the process exiting immediately**, so the `.out` file is ZERO BYTES and nothing is written to the panel dir but that one line.  **THE ROSTER ASSUMPTION IT OVERTURNS:** the owner's own read was *"seems like there is limitless agy use"*, and this project had never seen it wall, so it was being farmed 3 jobs at a time.  Six substantial invocations inside about forty minutes reached the limit.  Treat it like Grok's paid cap: **not queryable, not unlimited, and a raised cap has the same failure mode further out.**  *** THE DETECTION IS EASY AND THE MISREADING IS NOT. ***  It states its own reset time, which no other seat here does -- so a walled agy tells you exactly when to re-fire, and the re-fire-a-walled-seat-once rule becomes a scheduled thing rather than a guess.  But **the zero-byte `.out` is the trap**: this file's own rule says a zero-byte agy log is the NORMAL mid-run state because agy does not stream.  Zero bytes plus a live process is mid-run; zero bytes plus 111 bytes on stderr is a WALL.  **Check the `.err`, not the size** -- `panel.sh` writes one per seat and this is what it is for.  *Recorded because a seat that walls with the machine otherwise healthy is the state this project most often misfiles: three jobs failed identically and instantly, which reads like a launcher bug and is not.* |
*** OWNER RULING 2026-08-30: **agy IS RESERVED FOR MEASUREMENT AND HELD OUT OF ROUTINE
PANELS.** ***  Asked after its first quota wall proved the cap is real (~6 substantial calls
per window), and the question was forced rather than tidy: it cannot be a measuring front end
AND a panel seat on one budget.

**THE WARRANT IS THE ROSTER'S ONE STRUCTURAL WEAKNESS, already measured.**  There are THREE
compile-and-measure front ends and TWO of them -- Opus 5 and Fable 5 -- sit behind the SAME
Agent-tool transport.  When that transport went down on `#462`, the panel lost **all** of its
measuring capacity at once while seven reading seats answered normally, and the round had to
be held with a measured kill outstanding.  **agy is the only measuring seat on an independent
road**, so spending its budget on reading is spending the roster's insurance on a job seven
other seats already do.

**WHAT THIS COSTS, stated rather than glossed: routine panels now fire EIGHT seats, and every
one of them records agy as DELIBERATELY NOT FIRED.**  That is a different thing from a seat
failure and from agreement, and conflating the two is exactly what the seat ledger exists to
refuse -- so it is written by name in the round record, every time.

*The cost is real and today shows why it is worth paying: agy's READ-ONLY audits settled the
alignment premise path-by-path and found the debugger's `put d` exception that a clean
invariant claim would have missed.  Losing that from panels is not free.  But a reading is
recoverable from another seat, and a MEASUREMENT with both Anthropic seats down is not.*

**IT IS STILL FIRED FOR READING WHEN NO MEASUREMENT IS IN FLIGHT** -- the reservation is about
not spending the budget where it is fungible, not about idling the seat.  And note the two
roles genuinely conflict in practice, not just on paper: for most of 2026-08-30 agy was given
reading precisely BECAUSE a concurrent build would have corrupted the measuring seat's
wall-clock oracles.

| Kimi 3 | *** THE CLI IS THE SEAT AGAIN AS OF 2026-08-29, BY OWNER DIRECTIVE, AND THE WALL CLEARED BY TESTING RATHER THAN BY WAITING. ***  Its 403 was a **WEEKLY (7-day)** limit, not a billing cycle; a real invocation returned the liveness token, so the seat is **FILE-READING** again.  *** THAT IS A CAPABILITY CHANGE, NOT A TIDY-UP *** -- the `kimi-k3:cloud` substitute is PACKET-FED, so for the whole time it stood in, "the kimi seat" could not read the repo, and any answer credited to it as a REPO FACT was the conflation the doctrine forbids.  `panel.sh`'s `OLLAMA4` is now blank, and the launch, banner, seat check, verdict roster AND coverage note are all conditional on it -- **blanking the variable alone would have left `panel_ollama.py` running with an empty model name, writing an error file, and producing a PHANTOM seat that answers the seat check.**  Restoring the substitute is ONE LINE: `OLLAMA4="kimi-k3:cloud"`.  The two-transport history is kept below because it IS the recovery path. |
| *(kimi, historical)* | **TWO TRANSPORTS, AND THE SEAT WAS LIVE ON THE SECOND.** CLI: `kimi -p "$(cat brief)" -m kimi-code/k3` (rejects `--auto`/`--yolo` with `-p`) — **403-walled on its billing cycle; its ~348-byte error file is NOT a seat answer.** SUBSTITUTE: `kimi-k3:cloud`, fired automatically by `panel.sh` as `OLLAMA4` since `faffad7`, answering in every panel since. **Record it by transport (`kimi-k3:cloud`), never as "the kimi CLI seat".** *This row said QUOTA-DEAD / "do not wire it into panels" for days after the substitute was working — a FALSE ROSTER in the table a fresh session fires from. Fixed 2026-08-26.* |
| Grok 4.6 (xhigh) | `grok --prompt-file <brief> -m grok-4.6 --effort xhigh --permission-mode plan --cwd <proj> < /dev/null` — **xhigh set 2026-08-13 by user directive and VERIFIED to be a real tier, not assumed: passing a bogus value makes the CLI name its own list, `use one of: xhigh, high, medium, low`, which proves the flag is validated AND that xhigh is the top of it.** That discriminator is the general technique — if a bad value were silently ignored, acceptance would prove nothing and the seat would quietly run at the default, which is precisely the trap the agy seat sat in. **A bad effort value EXITS 0 while printing its error**, so exit status cannot catch it; `panel.sh`'s seat check greps for "unknown effort level"/"unknown model" alongside the quota patterns. — binary at `~/.grok/bin/grok.exe`, **added 2026-08-13 by user directive.** *** `--prompt-file` TAKES THE BRIEF FROM A FILE, so the ~32 KB Windows argv cap DOES NOT APPLY — this is the only CLI seat immune to the failure that killed Codex on a 36 KB brief today, so it is the seat to trust with a large inlined diff. *** `--permission-mode plan` keeps it READ-ONLY (verified: it read a repo file and answered correctly, without prompting or hanging) and `--cwd` lets it consult source like Codex and agy do. `grok models` is the authority on IDs. **MEASURED 2026-08-26 by running it: it lists TWO** -- `grok-4.6` (default) and `grok-4.5`. *** THIS CELL CARRIED BOTH "today it lists exactly one" AND "now lists TWO" AT ONCE, two present-tense claims that cannot both be true, until the exemplar audit found them. Settled by running the command rather than by choosing between them. *** **AND THE SAME RUN REFUTED THE TIER-CHECK CLAIM, which mattered more than the count.** This said the model list is "itself a cheap tier check" for whether the subscription is active. It is not: `grok models` printed **`You are not authenticated.`** and STILL listed both models -- so the list is served without auth and proves nothing about tier. **The seat was verified live in the same minute by a real invocation** (`--prompt-file`, xhigh, plan mode: it answered, read `CHECKPOINT.md`, and exited 0). **So the ONLY trustworthy health test is firing the seat.** That is the rule this file already states for walled seats -- *do not reason about whether a seat is back, test it* -- and the tier-check shortcut was a way of dodging it. The paid cap is still not queryable (no `usage`/`quota` subcommand; `du` is disk usage), so DO NOT ASSUME IT IS UNLIMITED — a raised cap has the same failure mode further out. `panel.sh`'s seat check scans any non-answering seat for quota/rate/auth text generically, so a wall is reported as an OPERATIONAL failure rather than counted as agreement. **FREE-TIER HISTORY, kept because it calibrates expectations: the free tier died after ~4 substantial invocations, mid-way through its first real review — and even so it found a genuine defect in that partial output (three surviving "un-fakeable" overclaims that two other seats had missed).** |
| Ollama cloud ×3 | POST `http://localhost:11434/api/generate` from **git-bash** python (WSL cannot reach the host API); write responses to utf-8 files, never `print()` (cp1252 crash). Three seats, verified live 2026-08-10: **`glm-5.3:cloud`** — *** MIGRATED TWICE BY OWNER DIRECTIVE: glm-5.2 -> glm-5.3-flash on 2026-08-28, then glm-5.3-flash -> **glm-5.3** on 2026-08-29. BOTH VERIFIED BEFORE THE EDIT, which is the discipline that matters here: `ollama pull glm-5.3:cloud` succeeded and an `api/generate` call returned the liveness token EXACTLY (`done_reason=stop`, eval_count 52, no thinking-burn). *** Verified BEFORE the edit rather than after: `ollama pull glm-5.3-flash:cloud` succeeded while the near-miss `glm-5.3flash:cloud` FAILED with `file does not exist`, and an `api/generate` call returned its liveness nonce exactly (`done_reason=stop`, 25 bytes, no thinking-burn). **The tag lives in TWO files and both were changed together** — `panel.sh`'s `OLLAMA1` and `adjudicate.sh`'s two loops, where the second loop must carry the `${m%%:*}` short form or the seat check hunts a filename the run never writes and reports a LIVE seat as missing. **The seat itself is keyed by FILENAME (`ollama_glm.txt`) everywhere else**, so `check_seats_read.py` and `seat_verdicts.py` needed no edit — record a seat by its transport, not its tag —, **`deepseek-v4-pro:cloud`** (DeepSeek is back — v3.2 was retired 2026-07-15 but v4-pro is live; the exact tag needs `-pro`), **`minimax-m3:cloud`**. All three are THINKING models — send NO `num_predict` cap or hidden reasoning eats the budget and the response is empty. Recheck: `curl -s localhost:11434/api/tags`. |
| Claude (Opus 5) | the Agent tool with `model: "opus"` — it has repo Read/Grep/Glob, and is the seat most likely to COMPILE AND MEASURE (it has overturned readings twice). Use plain bounds-/correctness-engineering framing, never offensive-security wording (refusal/flag risk); keep the adversarial instruction aimed at the engineering claim. There is no opus/fable CLI. |
| Claude (Fable 5) | the Agent tool with `model: "fable"`. **LIVE and answering** — it holds two hats and both are in use: this review seat, and (in the main loop) the ADJUDICATOR of the panel's suggestions. Same benign-framing rules as the Opus seat. Open every invocation with a liveness token plus a verbatim quote from a named file, so prompt delivery AND file access are proven rather than assumed. *This row read QUOTA-DEAD with three dated re-test failures long after the seat came back; the standing lesson survives and is the useful part — **a wall is a moment, not a state, and one Agent call settles it in seconds.** Do not reason about whether a seat is back; test it. Fixed 2026-08-26.* |

*** THERE IS A FIFTH `src/` AT THE PROJECT ROOT AND IT IS PRISTINE UPSTREAM. A FILE-READING
SEAT POINTED AT THE PROJECT ROOT WILL READ IT AND BE CONFIDENTLY, DETAILEDLY WRONG.
Measured 2026-08-22. ***

`C:\DocumentNoSnc\CC\GXEMUL\src\` is dated **April 2021**, is untracked, and is NOT the
hardened fork. The four fork trees are `GXEMUL-SEC/`, `est/`, `build/`, `build-asan/` (plus
WSL `/tmp/gxsec-build`).

> #### *** AND ON 2026-08-31 IT CAUGHT THE MAIN LOOP, NOT A SEAT.  THIS WHOLE SECTION IS
> #### WRITTEN AS A WARNING ABOUT SEATS WITH `--add-dir`; THE PERSON IT ACTUALLY BIT WAS ME. ***
> 
> I "refuted" a flagship seat's claim that `memory_rw.c` pre-zeroes a device read buffer, by
> grepping `src/cpus/memory_rw.c` while the cwd had drifted to the PROJECT ROOT.  That resolved
> to the pristine 2021 copy -- **530 lines against the fork's 794** -- which genuinely does not
> have the `#95` pre-zero.  The fork does, at `if (writeflag == MEM_READ) memset(data, 0, len);`
> immediately above `paddr -= mem->devices[i].baseaddr;`.  The seat was right, I shipped the
> refutation in a commit, and reported it to the owner as a finding.
> 
> > **THE TELL WAS IN MY OWN OUTPUT AND I DID NOT READ IT.  Every line number I quoted -- 161,
> > 222, 425, 437, 486 -- is below 530.  The fork's are 215, 267, 492, 671, 683, 732.  The
> > section three paragraphs down already says a seat reading another copy "reports line numbers
> > off by hundreds"; that is exactly what I did, to myself.**
> 
> **The cheap defence is not vigilance, it is the PATH.**  `grep -n ... GXEMUL-SEC/src/...` from
> the project root, or an absolute path, cannot resolve to the wrong tree.  A bare `src/...`
> depends on a cwd that this file elsewhere records as DRIFTING for whole rounds.

> #### *** AND IT IS NOT THE ONLY ONE. `./src/` IS THE ONE THIS PARAGRAPH NAMES; THERE ARE
> #### **THREE** PRISTINE-UPSTREAM COPIES UNDER THE PROJECT ROOT. Derived 2026-08-27 by
> #### running the command below, not transcribed -- and two of them were undocumented. ***
>
> **THE DERIVER, because a hand-maintained inventory of files is a wrong record waiting for
> someone to add a directory** -- this is the same failure the `_scratchpad/*.pdf` list made
> twice:
>
> ```
> find . -name 'dev_wdc.c' | while read f; do echo "$(md5sum "$f" | cut -c1-8) $f"; done
> ```
>
> On that date it printed **four fork copies sharing one hash** and **three upstream copies
> sharing another**, the extra two living under `_archive/audit-results-*/builds/`
> (`est-asanonly/` and `orig-asan/`). A seat given `--add-dir` at the project root can reach
> all of them.
>
> **THE SAVING GRACE, and it is worth knowing rather than relying on: these are PRISTINE
> 2021 upstream, not partially-patched fork copies.** A seat reading one reports line
> numbers off by hundreds and arms whose existence differs -- loud, and detectable by the
> rule two paragraphs down. *A nearly-right stale FORK copy would be far worse and would
> shift lines by tens.* So the hazard is bounded by luck, not by design; do not assume the
> next stale copy will be as obvious.
>
> *Surfaced by the codex seat while answering an unrelated design brief, as a held queue
> item (`stalecopies`). Its count was right and its characterisation -- "pre-#337 copies" --
> was not; they predate the fork entirely. Re-derived here rather than transcribed.* A brief that says only *"project root: C:\DocumentNoSnc\CC\GXEMUL"*
lets a seat with `--cwd` there resolve `src/cpus/cpu_sh.c` to the 2021 file.

**What that cost:** on the `sh4tlbmulti` pass 1, Kimi returned **80 KB, internally consistent,
with a DO-NOT-SHIP verdict and a dramatic finding — that the defect family was far larger than
the brief said, with `EXPEVT_RES_INST` itself ending in `exit(1)` and the `SLOT_INST`,
`FPU_SLOT_DISABLE` and `ADDR_ERR_LD/ST` arms simply absent.** Every word of it is TRUE OF
UPSTREAM and FALSE OF THIS FORK: `RES_INST` was fixed in **#217** and carries a comment saying
so, and all four arms exist at `cpu_sh.c:780-796`. Its own line numbers were the tell — it
reported the raise site at `dev_sh4.c:700-702` where the fork has it at `:1159`, and it said
so out loud, attributing the difference to "maybe GXEMUL-SEC or est".

**Two rules follow, and the second is the cheap one:**
1. **NAME THE TREE IN THE BRIEF**, not just the project root: *"the tree under review is
   `GXEMUL-SEC/src/`; ignore any other `src/` you find."*
2. **A SEAT REPORTING LINE NUMBERS THAT DISAGREE WITH THE BRIEF HAS PROBABLY READ ANOTHER
   COPY** — check that before crediting or dismissing the finding. Drift from an intervening
   commit shifts lines by tens; reading a different tree shifts them by hundreds and changes
   which arms exist.

**Do not score this as a seat failure.** The seat did exactly what it was asked, found real
defects in the file it was given, and flagged its own uncertainty about which tree it had.
The defect is in the BRIEF, and it is the same shape as the "inline every fact" rule below:
what the cloud seats cannot read, the file-reading seats can read too much of.

### *** AND A WRONG FACT IN A BRIEF COMES BACK CONFIRMED. Measured 2026-08-24: six of
### seven seats ratified a census that was wrong by 4x, including one that verified every
### other claim against the source. ***

The `asicbadaddr` pass-1 brief stated that **sixteen** offsets reach a host kill at
`(relative_addr / 4) & 3 == 3`. The true number is **sixty-four**, because `relative_addr`
is not necessarily word-aligned -- a BYTE access at `+0x0d` gives `0x0d / 4 == 3` and dies
exactly like `+0x0c`. The sixteen cited were the word-aligned quarter.

*** THE TALLY WAS REPORTED THREE TIMES BEFORE THE PANEL HAD FINISHED ANSWERING, AND ALL
THREE WERE WRONG. ***  "One seat of seven", then "two of nine", then "three of eight" --
each stated as fact while seats were still returning. **That is the frozen-number class
wearing a different hat: a count written before the thing it counts has finished.** The
score-claims rule already says a number names the artifact that produced it; the same
applies to a tally of seats, and the artifact is *the completed panel*.

Final, measured by grepping all nine answers for any engagement with alignment:

| seats | what they did |
|---|---|
| **codex, grok, fable5, opus5** | **CORRECTED it** -- each derived that `relative_addr` need not be word-aligned and the killing set is 64 byte addresses, not 16 |
| **agy** | **silently NARROWED the claim** to "Exactly 16 *word-aligned* offsets", inserting a qualifier the brief did not have. It verified every other claim against source, in detail and correctly |
| **kimi, glm, deepseek, minimax** | did not engage with alignment at all |

*** THE agy CASE IS THE ONE WORTH KEEPING, because it is neither agreement nor
correction. ***  A locally-true restatement repairs the sentence and hides the defect: a
reader sees a verified claim, and the fact that the true set is four times larger appears
nowhere. **That is harder to catch than a plain wrong answer**, because it survives every
check except asking what the qualifier was doing there.

*** AND ONE OF THE FOUR CORRECTORS PUT THE WRONG NUMBER IN ITS VERDICT LINE. ***  Its
verdict ratified "the sixteen word-aligned killing offsets" as verified; eight paragraphs
down it derived 64 and called the brief's framing an understatement. **This project's
policy is VERDICT LINE FIRST so the answer survives truncation** -- and here the surviving
half would have been the wrong half. A verdict line is a summary written against the
brief's own framing, so it is the LEAST likely part of an answer to hold the correction.
Read the body of any seat whose verdict merely agrees.

**And the strongest corrector gave the reason the enumeration could not:** `r == 3` is
exactly `(relative_addr & 0x0c) == 0x0c` -- *the fourth word of every 16-byte group* --
while all twelve implemented cases are three CONSECUTIVE words at group bases
`0x00/0x10/0x20/0x30`. **A structural invariant tells a future edit what it must not do;
an enumeration only tells you today's answer.** It also checked the one thing the brief
asserted implicitly and nobody else tested -- the DOMAIN of `relative_addr` -- confirming
from `memory_rw.c` and `core/memory.c` that it is exactly `[0, 0x100)` with no page
rounding and no fast path.

> **A STATED PREMISE IS LOAD-BEARING FOR EVERY SEAT, AND AGREEMENT WITH IT IS NOT
> EVIDENCE.** The existing rule says packet-fed seats can only know what the brief inlines.
> The sharper form is that they cannot know what it inlines WRONGLY -- and neither, in
> practice, do the file-reading seats, because a brief that presents a derivation directs
> them to check the arithmetic instead of the premise.

**Two things follow, and the second is the cheap one:**
* **Unanimity on a brief-supplied fact is worth nothing.** Score agreement only where a seat
  says it re-derived the fact from something the brief did NOT give it. This is the same
  distinction the seat ledger already draws between a READING and a MEASUREMENT, applied one
  level up -- to the brief itself.
* **State premises as questions where they are cheap to check.** Writing *"I believe these
  are the only reachable offsets -- check whether `relative_addr` can be unaligned"* costs
  one clause and converts a ratification into a test. The seat that found this was the only
  one whose answer engaged with alignment at all.

*Consequence in this instance, and it is why the class matters rather than being a tidy-up:
a detector built from the wrong census walks sixteen addresses, covers a QUARTER of the
defect, and reports full coverage.*

### *** THE REMEDY MEASURED: PUT THE PREMISE-AUDIT INSTRUCTION IN THE BRIEF. Second
### trial, 2026-08-24, and it found FOUR wrong premises in one brief. ***

The next brief opened with: *"please do not simply ratify — a recent panel had seven of
nine seats confirm a premise this brief stated wrongly. **Check the premises, not just the
derivations.**"*  Four of its load-bearing premises were then refuted, each by a different
seat, and **not one of them was refuted by argument — every refutation was a file opened
or a command run:**

| my premise | how it died |
|---|---|
| *"Site A is already half-fixed, so someone decided the kill was wrong"* | `git log -L 676,700:<file>` returns ONE commit — the upstream import. The fork never touched those lines |
| *"quoted verbatim from"* over a condensed comment | the real comment is **thirteen lines**; the brief showed two, with no ellipsis |
| *"nobody noticed"* | `#461`'s census had already counted the three disabled exits, and another row named the live one by its diagnostic |
| *"removing the guard deletes a tripwire that announced itself loudly"* | the `fatal()` REMAINS — only process termination goes. The tripwire still fires, it just stops shooting |

**And the corrections were BETTER ARGUMENTS than the claims they replaced**, which is the
part worth internalising. The upstream-residue reading (*whichever exit the author happened
to HIT while developing against one driver*) is a stronger warrant for de-fatalising than
"someone decided", because it explains why the live kill survived: **that driver never
wrote the bad value — not that such writes are unthinkable.**

> **THE RULE: state a brief's load-bearing premises AS QUESTIONS, and say plainly that
> ratification is not wanted.** Seats that would otherwise verify a derivation will
> verify the assumption under it. Two trials, two catches, and the second found four.

*Cost: one paragraph. It also produced the session's only finding that would have hidden a
defect outright — a queue id covering TWO defects, where closing it on one would have
buried the other.*

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
  acting on, not as a law. *(From ledger row `m8invpred`. The lesson was moved here FIRST and the row's closure held
  behind a seat — an earlier draft of this line said "dropped", which ran ahead of the gate
  that had refused the closure. The adjudicator caught it. Record the move, not the outcome.)*
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
original, putting two copies of the carrier in one context -- **151 KiB** as of 2026-08-26, and
this line said 38 KB, which was true when it was written and has quadrupled since.

## Tooling that makes the panel automatic (the "always" layers)

1. **Carrier** — this `CLAUDE.md`, auto-loaded every session.
1a. **THE PIPELINE DOCTRINE** — `PIPELINE.md` (project root): the owner's portable multi-LLM
   fix-pipeline methodology, supplied 2026-08-15 and ADOPTED (pasted into the loop five times —
   that is a directive). Two seat CLASSES recorded on every dispatch: FILE-READING (Codex, agy,
   Grok, Opus, Fable — facts about the repo) vs PACKET-FED (the Ollama transports —
   attack reasoning only; their blindness is a feature; NEVER equivalent votes on repo fact).
   *** KIMI IS CLASSIFIED BY ITS TRANSPORT, NOT BY ITS NAME, and this line listed it as
   FILE-READING until 2026-08-26. *** The CLI is file-reading; the live substitute
   `kimi-k3:cloud` goes through `panel_ollama.py` and is a **FOURTH PACKET-FED
   transport**.
   *** THIS SENTENCE SAID THE SUBSTITUTE GOES THROUGH `panel_ollama.py` "with
   `PACKET_BRIEF`".  THERE WAS NO SUCH THING.  Measured 2026-08-27 by opening the
   file: it was 24 lines and POSTed the brief VERBATIM, with no preamble of any
   kind. ***
   The cost was a lost seat.  A brief written for the file-reading seats carries
   instructions a packet-fed seat cannot obey -- *"check the premises against the
   source"*, *"grep the fork"* -- and a seat that TRIES to comply stalls.  On the
   `wdcdataoutdrain` pass 1 the substitute returned **127 bytes** (*"I'll check the
   premises against the actual tree ... Starting by locating"*) and stopped; with the
   CLI 403-walled that lost the kimi seat entirely, and `seat_verdicts.py` filed it as
   *"answered, NO VERDICT LINE (format miss)"* rather than as the stall it was.
   **This is the carrier's own "it was never the seat, it was the BRIEF" recurring,
   for the documented reason: the remedy lived in PROSE (remember to inline every
   fact) instead of in the tool that fires every time.**  `panel_ollama.py` now
   prepends a `PACKET_PREAMBLE` telling the seat it cannot read files and asking it to
   name any premise it cannot settle from the packet -- so an uncheckable premise comes
   back as an honest "not checkable" instead of silence.  Controlled in four states,
   including the negative one (the pre-fix source must NOT carry the preamble).
   *A tool's own source is the primary authority about the tool; this row asserted a
   wrapper that a 24-line file plainly did not have.*
   Since the CLI is 403-walled, **the kimi answers actually
   arriving today are PACKET-FED** -- so crediting one as a repo-fact reading is exactly
   the conflation this doctrine forbids.
   Conflict-of-interest badges on every closure: `A` = author self-review disclosed, `s` =
   same-model replication (weaker than two-family, never passed off as it). Evidence ladder
   CONFIRMED > MANUAL > BELIEVED > UNKNOWN — an honest UNKNOWN outranks a confident guess.
   VERDICT LINE FIRST in every requested seat output (truncation survives). Echo-test = nonce in
   the prompt + nonce in a file, both required back. **The ledger**: `GXEMUL-SEC/tools/pipeline/ledger.json` is
   the single source of truth; `GXEMUL-SEC/tools/pipeline/gen_dashboard.py` renders **`matrix.html`** (published as
   a claude.ai artifact; this line said `dashboard.html` until 2026-08-26 -- the
   generator itself documents the stale name at its `OUT =`) — write the ledger, regenerate, republish, NEVER hand-edit the output.
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
2. **One-command convening** — `./panel.sh <brief_file>` fires **EIGHT transports**
   concurrently (seven logical scriptable seats, because the Kimi CLI and its
   `kimi-k3:cloud` substitute are two transports for ONE seat), verifies each produced a
   real answer, and reminds you to launch **Opus AND Fable** via the Agent tool. *This
   read "five scriptable seats ... the sixth (Opus)" until 2026-08-26.* `panel_ollama.py` is its cloud-seat helper. Low
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
   oracles. *`gate_ab`'s 300 s WALL budget was REPLACED by an accounting of GUEST WORK
   in #419 (`LUNA_BUDGET`, `LUNA_STALL`, `LUNA_BACKSTOP`); this line said "300 s against
   a ~100 s normal" until 2026-08-26. The contention hazard is unchanged -- only the
   oracle's shape, and it is still load-sensitive.* In
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

**Panel roster for the loop — NINE seats by design, and as of 2026-08-26 ALL NINE ANSWER.**
The kimi CLI is 403-walled and its seat is covered by the `kimi-k3:cloud` substitute, which
`panel.sh` fires automatically and reports as COVERED rather than lost. *A dead seat is a SEAT
FAILURE and is never counted as agreement — and never silently: say which seats answered in the
round's record. But do not read a stale status line as a dead seat either; this paragraph
claimed two dead seats for over a week after both were answering.*
`bash GXEMUL-SEC/tools/panel.sh` fires EIGHT scriptable transports: Codex 5.6-SOL (xhigh —
the CLI's "ultra" intent), agy 3.7 (`gemini-3.7-flash-high`, `--effort high`), Kimi 3 (max
effort), **Grok 4.6 (high, `--prompt-file` so no argv cap)**, Ollama glm-5.3:cloud
(migrated from glm-5.2 on 2026-08-28, pull- and liveness-verified),
deepseek-v4-pro:cloud, minimax-m3:cloud. Two more are launched in the same turn via the
Agent tool: **Opus 5** (`model: "opus"`) and **Fable 5** (`model: "fable"`). Fable also
ADJUDICATES the panel's task suggestions in its main-loop role — seat and adjudicator are
distinct hats; the adjudication happens in the main loop, not in the seat.

**ADJUDICATION IS A MAIN-LOOP ROLE THAT FABLE HOLDS BY PREFERENCE, and that distinction is
load-bearing: it DEGRADES rather than blocks.** Proved on 2026-08-13 when the Fable seat was
genuinely walled: the adjudication still ran, in the main loop, and worked — 9 of 13 candidates
dropped, folded or retired, two of which would have caused harm. The seat has since been live
for days and holds both hats. What made the degraded form work was NOT the model: every one of
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

  **VERIFY CONTENT, NEVER SIZE.** Codex's wall, when it had one, was five echoed-brief-plus-429
  files of 26,992 / 11,180 / 10,036 / 8,323 / 12,414 bytes — *a size check alone scores those the
  largest answers in their panels.* That lesson is permanent; the outage was not.

  *This block used to END with "So: ONE full panel per ROUND, not one per pass" — the SUPERSEDED
  conclusion, sitting after the rule that replaced it and holding the closing position of
  authority. Which is this file's own "a policy written around two dead seats outlived both of
  them" failure, happening a second time, inside the paragraph that records it. **When a rule is
  superseded, delete its conclusion; do not demote it to a footnote that still reads as the
  verdict.***

## THE VACUITY FLOOR AND THE DE-ESCALATION CLAUSE (flagship adjudication, 2026-08-21)

**"Weak earns its own round; vacuous does not get to ship" IS A RATIONALISATION UNTIL A FLOOR IS
ATTACHED** — the adjudicating seat said so about the main loop's own call, and it was right:
*weak* has no lower bound, so any detector that kills one mutant can claim it.

> **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
> pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
> site**, and (c) fails on a null medium (a stale copy, a comment-only file — i.e. it carries
> identity rows). Below the floor, the round's own claim to have "shipped a detector with the
> fix" is a WRONG RECORD, which the stopping rule already fixes in-round.
>
> ### *** CLAUSE (d) — NULL-REPAIR RED. Adopted 2026-08-23 by OWNER RULING, on the round
> that measured its case. ***
>
> **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
> the guard kept, its effect removed.**
>
> **(b) DOES NOT IMPLY (d), and #461 measured both in the same hour on the same detector:**
>
> | mutant | shape | score |
> |---|---|---|
> | `m_dmarevert` | (b): reinstate the `exit(1)` verbatim | **22/31 — killed** |
> | `m_align1` | (d): keep the guard, weaken `& 3` to `& 1` | **27/27 — ESCAPED** |
>
> The detector passed (a), (b) and (c) and was still blind to a ONE-CHARACTER edit that
> re-opened the very defect the round had just closed. (b) restores the DEFECT; (d) neuters
> the FIX. A detector can be sensitive to one and blind to the other, because they fail at
> different sites: (b) fails where the old code was, (d) fails where the new code is.
>
> **HOW TO BUILD THE (d) MUTANT — and it is the same discriminator the accept-row rule
> already uses.** Take each predicate the fix **DEPENDS ON** and weaken it to the
> least-restrictive form that still *reads* like the same check: a mask narrowed
> (`& 3` -> `& 1`), a condition qualified (`if (X)` -> `if (X && writeflag == MEM_WRITE)`),
> a bound relaxed. **Not deletion** — deletion is (b) wearing (d)'s clothes and is usually
> already covered. The test is whether a plausible future edit could produce it.
>
> **WHY THE ONE-CHARACTER FORM IS THE ONE THAT MATTERS.** `dma alias`, the row written
> specifically to pin that repair, was **STRUCTURALLY BLIND** to it: it used an ODD address,
> which both guard forms drop. *The row aimed at the defect could not see the defect return.*
> A row written from the FIX's intent tests the intent, not the boundary — so (d)'s mutant
> has to come from an adversary, which is exactly what the ask-again buys.
>
> **COST: one mutant per repair predicate**, the same order as the accept-row rule (#448 = 4,
> #449 = 1, #461 = 4 across two arms). It is bounded by the diff, so it cannot become #392:
> the predicates are the ones the fix ADDED, and that list is finite and visible.
>
> ### *** "THE PREDICATE THE FIX INTRODUCED" ENUMERATED THE EMPTY SET FOR MOST OF THIS
> ### QUEUE, AND NOBODY NOTICED FOR THREE ROUNDS. Corrected 2026-08-24 -- clause (d) now
> ### reads DEPENDS ON, not INTRODUCED. ***
>
> Clause (d) says *keep the guard, null its repair*. As written it enumerated only
> predicates the diff ADDS -- and **the two commonest fix shapes here add none**:
>
> * a **pure deletion** introduces no predicate at all;
> * a **DE-FATALISATION** introduces none either -- it changes what an EXISTING
>   predicate's branch does. That is most of this project's queue.
>
> So for those rounds clause (d) enumerated **nothing**, and a round could satisfy the
> floor while having built no (d) mutant whatever. `#461` measured (d) successfully only
> because its fix happened to ADD a predicate (an alignment mask) for the mutant to weaken.
>
> **Reading it as DEPENDS ON fixes both cases at once**, and it is why this now replaces a
> narrower deletion-only rule written earlier the same day: that rule was a special case of
> this gap, and two overlapping statements of one rule is the accumulation this carrier is
> supposed to refuse.
>
> **The two shapes, once the enumeration is right:**
> * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
> * **fix adds none** -> the (d) mutant reroutes an EXISTING guard's repair. For a
>   de-fatalisation: **swap the guard's operand for a field the guarded BODY reads.**
>   For a pure deletion: **re-introduce the removed behaviour under a DIFFERENT predicate**
>   -- not the same one widened, which is (b) wearing (d)'s clothes.
>
> *** THE MEASURED CASE, and it is why this matters rather than being tidy: ***
> `#462` de-fatalised two arms. Its guard reads `d->data`; the body it guards reads
> `d->data` AND `d->data_len`; the two are set together in one place and cleared in two
> places that touch only ONE of them. Swapping the guard's operand to `d->data_len == 0`
> **scored a CLEAN SWEEP on a 52-row detector that had just passed twelve mutants**, and
> restored a NULL-pointer read of 408 bytes. Under the old wording that was coverage debt;
> under DEPENDS ON it is a **floor breach, L2, fix in-round** -- which is what the round
> did, before the wording was corrected.
>
> #### *** THE BOUND, and it is not optional: "DEPENDS ON" INVITES TRANSITIVE DATA-FLOW
> #### CHASING, which is unbounded and is how this becomes `#392`. Named 2026-08-24 by the
> #### adjudicating seat, in the same breath as upholding the correction. ***
>
> > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
> > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
> > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
> > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
>
> That is finite, derivable from the diff by reading, and **it provably contains the
> measured case**: the `d->data == NULL` guard dominates the edited decline (clause 1), and
> `data_len` is a body-read field (clause 2), so `M11` falls out mechanically rather than
> by inspiration. It cannot become `#392` because the enumeration stays closed over the
> diff's own hunks -- the same closure the INTRODUCED wording had, without the empty-set
> defect that made INTRODUCED enumerate nothing for a de-fatalisation.

> ### *** THE PRE-TABLE CHECK -- three greps, ~30 min, and it protects the ASK-AGAIN'S
> ### CAP rather than the clock. Adopted 2026-08-24; two seats derived it independently. ***
>
> > ## *** MANDATORY as of 2026-08-28, by flagship adjudication. It was RECOMMENDED prose for
> > ## four days and TWO rounds skipped it -- which is this file's own structure-first trigger,
> > ## met exactly. ***
> >
> > **SCOPE, and this is what answers the cost objection: it binds EXACTLY the population the
> > vacuity floor already binds** -- any round shipping or EXTENDING a kill-table-backed
> > detector. **Not every round.** Records-only, documented-only and table-less harness rounds
> > are untouched.
> >
> > **FORM: recorded OUTPUT, never assertion** -- the two-part-clearance precedent, *run it, do
> > not assert it*. One `PRETABLE.out` in the round's kill-table artifacts dir (or a probe-header
> > section), **written BEFORE table 1 runs so its own mtime proves the order** -- the same
> > order discriminator the oracle-correction rule uses. It carries: the sibling arms compared
> > and any asymmetry; each enumerated claim sentence mapped to a row or an owed sentence; the
> > guard-field/body-field lists and any disagreeing-state row owed; and per row, the mutant it
> > kills and the observable that differs.
> >
> > **Any check may discharge `N/A` WITH ITS REASON RECORDED. An unrun check and an inapplicable
> > one must not render the same** -- this project's oldest rule about blanks.
> >
> > ### *** AND A THIRD FAILURE MODE, MEASURED 2026-08-28: THE BLOCK WAS RUN, ITS ROWS WERE
> > ### PRESCRIBED, AND THEY WERE LOST WHEN THE ROW LIST WAS REWRITTEN THREE HOURS LATER. ***
> >
> > `#490`'s `PRETABLE.out` named two mutants at **16:05** -- a latch-bit collision and a brace
> > slip -- and prescribed a row for each (`crossbit`, `latch cond`). At **18:45** a nine-seat
> > panel found a DIFFERENT defect (the row set was site-asymmetric), the addition list was
> > rewritten to carry the panel's findings, and **both earlier rows silently vanished.** The
> > measuring seat then BUILT both mutants and both escaped the committed 13-row detector --
> > two clause-(d) floor breaches that the round's own artifact had predicted and specified.
> >
> > **Nothing was forgotten in the sense of never known.** The knowledge sat in the file that
> > exists precisely to be consulted at row-writing time, and did not survive a rewrite in a
> > DIFFERENT artifact. The new list was not careless -- it correctly added everything the
> > panel had just found.
> >
> > > **A ROW LIST REWRITTEN FROM A PANEL'S FINDINGS IS DIFFED AGAINST THE PRE-TABLE BLOCK'S
> > > OWN PRESCRIBED ROWS, NOT MERELY EXTENDED WITH THE NEW ONES.** The block PRESCRIBES rows;
> > > a later list that does not contain them has dropped an obligation, and the diff is the
> > > only thing that says so.
> >
> > *This is the block's own lesson turned on the block: it exists because a recommended check
> > is memory and memory does not fire. Running it once does not make its OUTPUT durable --
> > the output has to be carried forward, and nothing was checking that it was.*
> >
> > **AND THE GUARD-FIELD CHECK COULD NOT HAVE CAUGHT EITHER**, which is worth knowing before
> > relying on it: it asks where the guard field and the body field DIFFER. For the latch
> > collision they are the SAME field (`d->warned`). **For a shared bitfield the question is
> > *"who else writes this field, and can they set my bit?"*** -- measured here as
> > `grep -c 'd->warned |='` = 8 sites, **6 of them inside `DEVICE_ACCESS`**, so most bits are
> > set by ordinary guest register reads and a collision would be silenced by benign traffic.
>
> > **THE TRIGGER WAS MET TWICE IN FOUR DAYS, and the value at each was specific rather than
> > general:** at `#485` the GUARD-FIELD grep enumerates `D1..D5` mechanically, because the
> > `default:` arm's `fatal()` arguments ARE the guarded body's field reads; at `#489` the
> > CHANNEL line names the one shape all four escapes shared -- **and the probe header carried
> > the governing sentence before three of the four were found.** Knowledge present, unconsulted
> > at row-writing time. *A recommended check is memory, and this file's finding is that memory
> > does not fire.*
> >
> > **ENFORCEMENT is existence-only and FILED, not built:** a commit adding a killtable artifacts
> > dir must add `PRETABLE.out` beside it, forward-only from a cutoff. That is a tooling change
> > owing two negative controls, so it ships as its own harness round rather than as a rider.
> > Until it lands the mandate lives HERE, in lifecycle steps 4-5, and in `/round`.
> >
> > *** AND THE FIRST MANDATED APPLICATION MUST **CHECK** THE CHANNEL LINE, NOT MERELY OBEY IT.
> > *** CHANNEL is one day old, and this file's freshly-minted-exemplar rule says a new rule's
> > example is a HYPOTHESIS. Its claim is that a row's channel-under-its-mutant is knowable at
> > WRITING time, before any table runs. One sentence in the first `PRETABLE.out` says whether
> > that held.
> >
> > *Provenance note, because the ruling corrected my own citation: the twice-skipped rounds are
> > `#485` (wdcnoirq) and `#489`, **not `#486`** -- `#486` is wdcfloodstale's non-discriminating
> > gate row. The substance was intact and the number was wrong, and a wrong number in a
> > mandate's provenance gets reused.*
>
> *** THE DIAGNOSIS THAT PROMPTED IT WAS WRONG, AND THE CORRECTION IS THE USEFUL PART. ***
> `#462` ran a 12-mutant table clean, then one capped ask-again found escapes needing five
> rows -- and adding rows changed other mutants' scores, forcing a **second four-hour
> table**. The adjudicator blamed obligations caught too late. **A seat then checked the
> preserved logs and refuted that: both "late" rows were in the FIRST table already.** They
> cost nothing. What cost four hours was that **the probe cannot score one row** -- 39
> `session()` calls, no row filter -- so re-measuring five rows meant re-running everything.
>
> **So the checklist does NOT save the table.** Its real value is narrower and it is worth
> having: **the ask-again is capped at ONE, and every hole it spends itself naming is a
> query not spent on coverage debt.** A detector arriving with visible holes wastes the cap.
>
> | check | how | catches |
> |---|---|---|
> | **SIBLING PARITY** | for each arm the diff de-fatalises, compare its observable channels against its nearest sibling arm. An asymmetry is a row you owe or a sentence you owe | a de-fatalised arm with NO completion-event row while its sibling had one |
> | **CLAIM -> ROW** | every ADDED comment sentence asserting an OBSERVABLE CONSEQUENCE owes a row or an explicit no-row sentence. Claim verbs (*observes, controls, pins, proves, the X control*) are EXAMPLES, not the test | a "device-signature control" claimed in prose and implemented by nothing |
>
> > *** THE VERB LIST WAS THE TEST UNTIL 2026-08-28, AND IT COULD NOT FIRE ON THE INCIDENT THAT
> > MADE THIS CHECK MANDATORY. Caught by the adjudicating seat while ruling on the mandate. ***
> >
> > `#489`'s load-bearing added comment reads *"An early return would skip that event and hang the
> > guest."* **It contains not one of the five verbs** -- it is a COUNTERFACTUAL-CONSEQUENCE claim
> > about a hypothetical edit, and the grep form walks straight past it. Mandating the block
> > unrepaired would have mandated a check that cannot fail on its own motivating case, which is
> > this file's check-that-cannot-fail shape arriving inside the repair for it.
> >
> > **So the trigger is SEMANTIC: does this sentence assert something a row could observe?** A
> > *"would &lt;consequence&gt;"* clause qualifies -- it names a channel (the event, the hang) and
> > predicts a difference -- and `#489` shipped exactly that channel's row only after a panel
> > found the escape three times.
> | **GUARD FIELD vs BODY FIELD** | list fields the PREDICATE reads and fields the guarded BODY reads; where they differ, grep whether they are written at the same sites. If not, the detector owes a state where they DISAGREE | the guard's operand swapped for a field whose third state no row built |
> | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
>
> ### *** THE CHANNEL LINE IS THE FOURTH CHECK, ADDED 2026-08-28 AFTER `#489` SHIPPED A
> ### DETECTOR THREE TIMES AND A PANEL MEASURED FOUR ESCAPES OF ONE SHAPE. ***
>
> `#489` de-fatalised a guard, and **four separate mutants left the host ALIVE while the guard
> was wrong** -- `> 408`, exempt-zero, `< 408`, and a latch-state collapse. Each was caught
> only by a row reading a DECLINE channel (COND_DATA_AVAIL, the zeroed count, the fired event).
> Each was predicted by a seat from the packet alone, and **each escaped a table that had
> already come back CLEAN.** The round's own probe header carried the governing sentence before
> three of the four were found.
>
> **THE COST WAS NOT MISSING KNOWLEDGE.  IT WAS KNOWLEDGE LIVING WHERE NOBODY CONSULTS IT AT
> ROW-WRITING TIME** -- this file's trigger-versus-memory finding, again.
>
> #### AND THE OBVIOUS GENERALISATION IS UNBOUNDED, SO IT IS NOT THE ONE ADOPTED
>
> The tempting sentence is *"every VALUE and every STATE in which a guard refuses needs a
> decline-channel row."*  **That licenses unbounded row growth -- the `#392` shape** -- and the
> adjudication that produced this line rejected it for exactly that reason. The distinction:
>
> * **ROW DEMAND** -- *which* refusals need pinning -- is ALREADY bounded and is not touched:
>   the floor clauses, the (d) DEPENDS-ON closure, one accept row per conditioned predicate,
>   one anchor row per position claim, one ask-again. **Rows are owed PER ENUMERATED MUTANT,
>   never per refusing state**; two states no enumerated mutant distinguishes collapse into one
>   row. That enumeration is diff-closed and finite.
> * **ROW VALIDITY** -- what `#489` actually measured -- is the CHANNEL line above, and it is a
>   WRITE-TIME check on rows that already exist.
>
> > **A FILTER CAN REJECT OR REPAIR A ROW; IT CAN NEVER DEMAND A NEW ONE -- SO IT CANNOT GROW
> > WITHOUT BOUND.**  That is the stop condition, and it is structural rather than a cap: the
> > generator side is untouched.
>
> *Mechanising it -- a `# kills: <mutant> via <channel>` comment per row -- is FILED, not
> adopted: it changes what every probe in the tree must carry, and that is an owner decision
> rather than a round's.*
>
> **The third is the one that looked impossible and is the cheapest.** It only seemed
> unreachable because it was approached from the mutant side -- *"what edit escapes?"*,
> which is unbounded -- instead of the field side -- *"what states can these two fields be
> in?"*, which is a grep. In `#462` that was three lines of output: `alloc_data` sets both
> fields; two `free` sites clear only one.
>
> **DO NOT move the ask-again earlier.** It works BECAUSE a clean table redirects seats away
> from shapes the author already covered; measured yield says so. And do not raise the cap
> -- the cap is what stands between this and `#392`.

> **(e) THE CONTRACT.** The probe header names which edits this detector is designed
> to catch. *A detector that says so is falsifiable; one claiming completeness is
> not* -- and a later escape becomes "outside the contract" or "a breach of it",
> which are different dispositions, rather than an argument about overclaiming.
> Two lines in a header.
>
> **IT IS A FLOOR CLAUSE, so a breach is L2 — replace IN-ROUND however late it is found.**
> That is deliberate and it is the whole point: an escaped (d) mutant means the round's
> claim to have "shipped a detector with the fix" is false about the fix's own repair.
>
> ### *** (f) THE ANCHOR RULE -- adopted 2026-08-25 after a CLEAN 12/12 detector was escaped
> ### by a ONE-TERM translation that three purpose-built rows could not see BY CONSTRUCTION. ***
>
> **Rows that assert only PAIRWISE DISTINCTNESS, or a same-path round-trip, test the decode
> against ITSELF.** They are therefore invariant under any edit that re-maps addresses
> INJECTIVELY over the probed set -- translations first among them -- and they catch a re-map
> only where it COLLIDES on that set.
>
> `#463` shipped three rows built specifically to pin an index bound: `alias`, `alias2` and
> `crossarr`. All three read back `+0x10` and together assert exactly
> `cell(+0x10) != cell(+0x14), cell(+0x18), cell(+0x24)`. **They never assert WHICH cell any
> offset names.** So `r = (relative_addr / 4) & 3` -> `((relative_addr / 4) + 1) & 3` slid the
> whole window one word, every pair stayed distinct, and the detector scored a CLEAN SWEEP --
> while every `+0x?8` register moved one past a `[3]` array and a documented register's store
> landed on `int asserted_13`, making the device drop a legitimately pending interrupt.
>
> > ### *** THE SAME RULE ON THE ACCEPT SIDE: AN ACCEPT ROW MUST USE THE WINDOW'S **LAST**
> ### SLOT. Measured 2026-08-31, where a one-hex-digit edit scored a TOTAL ESCAPE. ***
>
> A detector for `sgireunmapped` carried an accept row per window, each writing to the
> window's **BASE**. Shrinking a window bound -- `+ 0x80` -> `+ 0x40`, one hex digit --
> **swept that 9-row detector CLEAN**, because moving the FAR bound is invisible from the
> base by construction. The accept rows proved the window still *starts* where it did and
> said nothing about where it *ends*.
>
> > **AN ACCEPT ROW WRITTEN AT A WINDOW'S BASE TESTS THE NEAR BOUND TWICE AND THE FAR BOUND
> > NEVER.**
>
> > #### *** THE SECOND HALF OF THAT SENTENCE -- "put it at the LAST legal slot, WHERE BOTH
> > #### BOUNDS ARE LOAD-BEARING" -- IS MEASURED **FALSE**, and it was falsified the same day
> > #### it was written, by the measuring seat working on the very row it was minted from. ***
> >
> > **`M5`: move the NEAR bound instead.**  `>= CRIME_RE_LINEAR_A` -> `>= CRIME_RE_LINEAR_A +
> > 0x40`, **one token**, against the 14-row detector whose accept rows all sit at their
> > window's TOP slot: **14/14, a total escape** -- while a control row storing at the window
> > BASE reds on that mutant and is serviced normally on the fix.
> >
> > **SO MOVING THE ROWS FROM BASE TO TOP SWAPPED THE BLINDNESS RATHER THAN REMOVING IT.**  A
> > single accept row pins exactly ONE bound -- the one it is near.  There is no slot from
> > which both bounds are observable, because an accept row's oracle is *this access was
> > serviced*, and servicing is a single bit that one bound can explain on its own.
> >
> > **THE REPAIR THAT ACTUALLY WORKS, and it costs no extra sessions: ANCHOR THE ORACLE
> > INSTEAD OF MOVING THE ROW.**  The store's own `debug()` already prints the destination --
> > `[ d->re_linear_b[30] = 0x... ]`.  Assert **the array NAME and the INDEX**, not merely
> > that the catch-all was missed.  That converts each relative row into an ANCHORED one in
> > clause (f)'s sense, pins BOTH bounds from one access, and additionally catches
> > TRANSLATIONS, which no base-or-top accept row can see at all.
> >
> > *Two rows (base AND top) is the fallback where no such channel exists.  It is strictly
> > weaker: it pins the two bounds and still cannot see a re-map that keeps both.*
>
> It is clause (f) arriving from the other direction: (f) says a distinctness suite cannot
> tell you WHERE an access lands, and this says an accept suite cannot tell you HOW FAR a
> window reaches. Same blindness, opposite polarity -- and the same one-row repair.
>
> *Cheap reviewer check, beside the existing one:* ***"if this window got smaller, which row
> reds?"*** If the answer is none, the far bound is unpinned however many accept rows exist.
>
> **AND WATCH FOR MIXED IDIOMS IN ONE CASCADE:** the same file bounds TLB_A and TLB_B by *the
> next window's constant* and the other four by *base + size*.
>
> > #### *** THIS CLAUSE ONCE ADDED "a shrink edit to the first kind moves a boundary two
> > #### windows share; to the second it opens a gap -- two different blast radii".  ALSO
> > #### MEASURED FALSE, in the same table. ***
> >
> > **Editing the `<` EXPRESSION in the TLB_A arm opens a gap and does not touch TLB_B's arm
> > at all.**  `M1`, `M2` and `M3` each reddened EXACTLY their own accept row -- 13/14 apiece,
> > the same one-row signature as the three base+size siblings already discharged.  No shrink
> > perturbed a neighbour.
> >
> > The shared-boundary hazard is real only for editing **`CRIME_RE_TLB_B` in `crmfbreg.h`**,
> > which is a different edit on a different file.  *The idiom governs which EDITS are
> > available, not how a given edit propagates -- and the original wording conflated them,
> > which is what left three accept rows filed as needing "a different mutant shape" when they
> > needed the ordinary one.*

> **A DETECTOR CLAIMING TO PIN *WHERE* AN ACCESS LANDS MUST CARRY AT LEAST ONE ANCHORED ROW:
> > an oracle tied to a SPECIFIC CELL by a channel OUTSIDE the decode under test** -- a side
> > effect (a tick that zeroes the cell), an architectural reset value, or a second access path
> > to the same cell. **One anchored row converts a whole distinctness suite from relative to
> > absolute.**
>
> **THE REVIEWER CHECK, and it costs two seconds** -- it belongs beside *"does this diff delete
> `exit(` from a device? then look for accept rows"*:
>
> > ***"If every address in this device shifted one word, which row reds?"*** If the answer is
> > NONE, position is unpinned, whatever the row count.
>
> **This is not a new species.** It is the witness ladder's DEVICE-SIGNATURE control one level
> down: RAM-vs-device needed a signature because a value-only read cannot tell them apart;
> cell-vs-cell needs one for the same reason.
>
> Two cautions the same round measured, both worth carrying: a row that catches a re-map by
> COLLISION is **layout-dependent** -- `crossarr` catches `-1` only because the probed cells
> collide there, and a struct REORDER would silently unpin it.
>
> #### *** THE CLAUSE ABOVE ONCE ENDED "where an anchored row would not". THAT WAS MEASURED
> #### FALSE 2026-08-25, AND IT WAS FALSE IN THE CARRIER, THE PROBE AND THE QUEUE FILE AT ONCE. ***
>
> The exemplar anchored row, `mask9 rt`, was described as *"anchored to a cell by a side effect,
> **not to a neighbour by distance**"*. **It is anchored to a neighbour by distance.** The struct
> declares `pending_irq[3], mask_13[3], mask_11[3], mask_9[3], int asserted_13` consecutively, so
> `mask_9[3]` lands on `asserted_13` at byte 48 -- verified by `offsetof`, and the probe says so
> itself two hundred lines below the clause that denies it. A struct reorder moving
> `asserted_13` off that slot **can let** the `+1` store round-trip so that `mask9 rt` goes GREEN,
> which is the identical failure the clause attributes only to `crossarr`. *Existential, not
> universal, and the distinction matters because a wrong reason gets reused: a reorder that puts
> some OTHER tick-zeroed field at byte 48 keeps the kill. What is unsafe is relying on the
> arrangement, not any particular rearrangement of it.*
>
> > **THE CORRECT STATEMENT: anchoring makes an oracle absolute with respect to the DECODE --
> > which is real, and is exactly what clause (f) buys -- but it does NOT make it independent of
> > struct LAYOUT, because which cell an out-of-bounds index lands on is itself a layout fact.**
>
> *So the two cautions are not a contrast between a weak row and a strong one. Both rows are
> layout-dependent; the anchored one is additionally decode-absolute. Stating it as a contrast
> made the anchor rule sound like it bought more than it does -- in the carrier, where future
> rounds apply it.*
> And **translations beyond the measured ones are not covered by having measured +/-1**: a
> derivation says `+2` escapes both the distinctness rows and that round's anchored row. A
> contract must claim the translations it MEASURED and disclose the rest.

> ### *** THE LATE-DISSENT RULE -- adopted 2026-08-25, after a panel stage fired AFTER a round
> ### had committed returned 4-2 AGAINST the shipped fix. ***
>
> `#463` closed with its research stage at 3 of 9. An exemption was offered to the owner and
> **DECLINED in favour of firing the missing seats** -- and the filled stage dissented on code
> that had already shipped. There was no rule for that, so:
>
> > **A panel stage fired after a round closes adjudicates like any other finding. Closure
> > changes the LICENSE, never the truth-value.** Three dispositions, exhaustive:
> >
> > 1. **WRONG RECORD -> L4, correct in place.** Closure is no shield for false prose.
> > 2. **MEASURED FALSE PASS** against the shipped detector's floor, contract or obligations
> >    -> L2/L3 per the existing rules, in a follow-up commit.
> > 3. **EVERYTHING ELSE, design dissents included -> FILES AS A NEW QUEUE ITEM**, carrying the
> >    dissent VERBATIM as provenance and ranked by severity like any filed item. The closed
> >    round's record gains one line naming the dissent and where it went, **so a future reader
> >    never sees false unanimity.**
> >
> > **Never amend shipped code under a closed round's number**, and never let "the round is
> > closed" reduce a dissent to a footnote no queue item carries.
>
> **THE DISCRIMINATOR for whether a filed dissent earns a round is the universal one: CAN IT
> STATE A MEASURABLE CONSEQUENCE?** `#463b` could -- a `+2` translation predicted to sweep the
> shipped detector clean, and an added-`case` scenario that passes the de-escalation membership
> test. A design dissent that can name no measurement files as documented-only.
>
> *** AND COUNT THE ARGUMENTS, NOT THE SEATS. *** That stage read 3-2 and then 4-2, and the
> count was never the reason. One defending headline was **contradicted by the round's own L4
> correction**; another's objections aimed at options the dissent had not proposed. Meanwhile
> three DISSENTING seats proposed a one-line `return` that would have skipped the function's
> common tail and handed a guest an untouched read buffer -- **none of them read nine lines
> down**. What settled it was neither tally but asking *what the proposed line does to the
> already-built mutants and rows*, which had empirical content the moment it was phrased that
> way.
>
> **A corollary worth its own line, because it cost this round its best evidence:** a detector
> can be green under EVERY candidate fix and therefore settle nothing between them. `#463`'s
> thirteen rows leave the shipped fix, a bare decline, a decline-plus-latch and a latched
> diagnostic all at 13/13, because every row touching the disputed offsets is SURVIVE-ONLY.
> **"The gate is green" is not evidence for a disposition the gate cannot observe** -- which is
> why a research panel cannot be replaced by re-running the battery.

> ### *** THE SKETCH RULE -- adopted 2026-08-25, after FOUR independent readers wrote the same
> ### broken line into a function none of them knew had a tail. ***
>
> Three panel seats and the ADJUDICATOR each proposed `if (r == 3) return;` as a defensive
> decline. The function's last three lines are:
>
> ```c
> 	if (writeflag == MEM_READ)
> 		memory_writemax64(cpu, data, len, odata);
> 	return 1;
> ```
>
> An early `return` **skips that**, handing a guest read an untouched buffer -- a defect the
> shipped code does not have. Four readers, nine lines, nobody looked.
>
> > **A PROPOSED EDIT IS A SKETCH, NOT A FIX, UNTIL IT HAS BEEN RUN AGAINST THE ENCLOSING
> > FUNCTION'S REAL CONTROL FLOW -- and a brief that solicits or evaluates edits must INLINE THE
> > FULL ENCLOSING FUNCTION: every exit path, and the common tail included.**
>
> **This is the dual of the mutant-table rule.** That one says a brief must inline the exact
> EDIT, never just its label. This one says it must inline the exact CONTEXT the edit lands in.
> Both failures look like seat error and are brief defects: the packet showed the guard and the
> switch, the visible shape invited a per-case-return idiom, and four independent readers
> produced the same wrong line. **When every reader makes the same mistake, suspect the brief.**
>
> Corollary, measured the same day and worth its own sentence: **a handler's RETURN VALUE is
> itself a contract** (`return 1` = handled). What a `0` does to the caller was checked by
> nobody in that entire exchange -- not the three seats, not the adjudicator, not me. An edit
> that changes a return path owes that check.

> ### *** THE THREE-MEMBERED OPTION SET -- adopted 2026-08-25, after a round chose between two
> ### options while the third was already shipping ONE FILE UP ITS OWN CALL PATH. ***
>
> `#463` de-fatalised a device and framed the choice as *keep `fatal()` unlatched* versus
> *delete it*. It deleted, and recorded honestly that this cost the unconditional diagnostic.
> **But `src/cpus/memory_rw.c:495-523` -- in the file that DISPATCHES to that very device --
> already bounds a guest-drivable diagnostic to 8 emissions via `n_trunc_msgs`**, reasoning that
> *"probing at the end of a device's mapped range is common and benign."* Same phenomenon, and
> the fork's own answer was BOUND THE COUNT, KEEP THE MESSAGE.
>
> Worse: **this carrier already said so.** *"A guest-drivable `fatal()` needs a latch and not a
> verbosity flag"* was standing rule before that round, and the two-membered framing never
> consulted it.
>
> > *** THE SET HAS SIX MEMBERS, NOT THREE.  Grown twice, and BOTH TIMES BY A SEAT THAT WENT
> > LOOKING IN THE TREE RATHER THAN REASONING -- which is the instruction below working. ***
> >
> > **1 DELETE  ·  2 DECLINE (silent)  ·  3 DECLINE + BOUNDED (LATCHED) ANNOUNCE  ·
> > 4 ACCEPT  ·  5 FAULT  ·  6 BACKED ACCEPT**
> >
> > * **4 ACCEPT** -- the model ALREADY computes the right value and then discards it.  Delete
> >   the kill, keep the value, NO latch: there is no event to announce, and a bounded announce
> >   would ship a wrong record in product code (*"unimplemented; ignored"* about a read that
> >   is implemented and is not ignored).  Found 2026-08-27 when the DC21285 datasheet showed
> >   `+0x188` is IRQEnable, a documented read-only register the model answers correctly.
> > * **5 FAULT** -- deliver the architectural bus error, by MODELLING THE SPACE AS UNMAPPED.
> >   `src/devices/dev_unreadable.c` is a device whose entire access function is `return 0;`
> >   ("returns an error for all reads/writes"), and `machine_sgi.c` installs it TEN times so
> >   absent hardware faults, because the PROM and NetBSD probe those regions and RELY on the
> >   failure.  **This is why *`return 0` is not a decline* and *FAULT is a member* are both
> >   true: it is not a refusal, it is a positive statement that nothing is there.**
> > * **6 BACKED ACCEPT** -- invent storage and accept, the `mte_reg[]`/`de_reg[]` idiom.
> >   Distinct from 4: nothing computes a value, so this FABRICATES one.  Governed by the
> >   ADDITION LICENCE -- a measured delta or a transferred warrant, never "cannot hurt".
> >
> > *(A seventh, ALIAS/mirror -- partial address decode folding a high window onto a low one,
> > which real hardware often does -- was named and dismissed for want of evidence.  An
> > unmapped-space arm's option set generically contains it; name it before dismissing it.)*
> >
> > **Before choosing, GREP THE FORK FOR AN EXISTING IDIOM -- the tree's own precedents are
> > part of the design space.**  Members 4, 5 and 6 were ALL found that way and none of them
> > by argument.  **And grep for the SIBLING HANDLERS' disposition in the same file**: on
> > `sgireunmapped` that showed the three siblings already declined without `exit(1)` and
> > pristine upstream did too, making the arm under review the file's own outlier -- upstream
> > residue rather than a policy.  *That is a far stronger warrant than "it is a host kill",
> > and it is one `grep` away.*
>
> This is the premise-audit discipline aimed at **option-space completeness** instead of at
> factual premises. A brief that lists two options gets a panel arguing about two options;
> nobody proposes the member that was never named. *Five seats and an adjudicator debated the
> two-membered set; the seat that found the third had gone looking in the tree.*
> #### *** AND THE FOUNDING STORY WAS WRONG. THE THIRD MEMBER *WAS* NAMED -- ON PASS 1, IN A
> #### VERDICT LINE, BY A SEAT `panel.sh` HAD STOPPED FIRING. Discovered 2026-08-25, one day
> #### after this rule was minted, by teaching a checker about that seat. ***
>
> The sentence above says *nobody proposes the member that was never named*. In the round this
> rule was minted from, somebody did. `_scratchpad/panel_20260824_191634/ollama_kimi.txt`,
> written at **19:36 on the FIRST pass**, says in its verdict line:
>
> > *"the latent index protection should be carried as a **point-of-use decline**, not only a
> > comment."*
>
> **That is the SECOND member -- and an earlier version of this block called it the third,
> which overcorrected the very story it was correcting.** Checked across all 70 lines of that
> answer: what it proposes is `if (r > 2) break;`, described as *"decline-not-die, so if the
> forbidden `case 0x0c:` ever arrives it fails safe instead of killing the host"* -- a SILENT
> decline. It never proposes a bounded or latched announce; its only two mentions of `fatal()`
> are to escalate the flood problem and to request a measurement about rate limiting.
>
> **The 17.7 KB answer was recorded nowhere.** It surfaced only when `check_seats_read.py` was
> taught that `ollama_kimi.txt` maps to the kimi seat -- until then a substitute-transport
> answer was invisible to the very check that exists to catch unread reviews.
>
> > **SO THE DIAGNOSIS IS BOTH, ONE MEMBER EACH.** Member 2 WAS proposed on pass 1 and went
> > unread -- that half is an UNREAD REVIEW and the fix is to read what the seats already sent.
> > Member 3, the bounded announce, was genuinely never named by anyone until a seat went
> > looking in the tree -- that half is real OPTION-SPACE BLINDNESS and the founding story
> > survives for the member it was actually about.
>
> *An earlier draft replaced one wrong diagnosis with another wrong diagnosis, and it was
> caught by a seat that read all seventy lines instead of the verdict line. That is the
> read-the-body rule this file already states -- **a verdict line is written against the
> brief's framing and is the LEAST likely part of an answer to carry a correction** -- turned
> on a correction of my own.*
>
> The same answer also named `asicindexcase` on pass 1 -- *"post-switch `r`-use audit before
> the edit lands; absence admits converting a host kill into a silent OOB write on declined
> offsets"* -- which the round later filed as a discovery.
>
> *Two rounds of design argument, one filed row and one carrier rule, all of which existed in
> a file on disk the whole time. This is the third recorded instance of the unread-review
> class and by some distance the most expensive.*
>
> And it pays across a whole filed queue, not one device: every remaining `exit(` de-fatalisation
> faces the same choice, and `floodclass` already records guest-drivable log floods as a CLASS.
>
> #### *** THE RULE'S ADVICE WAS RIGHT AND ITS EXEMPLAR WAS THE TREE'S ONE OUTLIER.
> #### Corrected 2026-08-25 -- and it was corrected BY FOLLOWING THE RULE. ***
>
> The rule says *grep the fork for the existing idiom rather than reason from first
> principles*. The first round to obey it did exactly that, on `wdcflood`, and the census
> came back against the rule's own example.
>
> **`memory_rw.c:495-523` is a bounded diagnostic, but it is the ONLY counter-style bound in
> the tree, and every property that makes it a bad model was verified by reading it:**
>
> * it is **not a `fatal()`** -- `debugmsg_cpu(..., VERBOSITY_DEBUG, ...)`;
> * it is **DOUBLE-GATED**: `ENOUGH_VERBOSITY(SUBSYS_MEMORY, VERBOSITY_DEBUG) && n_trunc_msgs < 8`,
>   and because `&&` short-circuits, **the counter never increments at default verbosity**. The
>   bound almost never engages, because the message is already invisible;
> * `static int n_trunc_msgs` is function-local -- **GLOBAL, shared by every device and CPU**,
>   not per-instance;
> * it prints **no give-up notice**.
>
> > **THE HOUSE IDIOM IS NOT "FIRST N THEN QUIET". IT IS `N = 1`, PER DEVICE INSTANCE, PLUS AN
> > EXPLICIT SUPPRESSION MARKER IN THE MESSAGE TEXT** -- roughly 34 latch sites across 11 device
> > files. So member 3 should be read as **DECLINE + LATCHED ANNOUNCE**, and the counter form is
> > the exception that needs a warrant, not the template.
> >
> > *** THE MARKER'S SPELLING WAS NAMED WRONG HERE: this clause used to say the idiom is
> > `(further occurrences suppressed)`, which is the MINORITY form. Censused 2026-08-26 across
> > `src/devices/*.c`, by message text: ***
> >
> > *** ALL THREE NUMBERS WENT STALE AND WERE RE-DERIVED 2026-08-30, after the kimi seat
> > challenged the `(once)` figure in a brief that quoted this block.  It counted 24 where
> > this said 9, and it was right.  The fable5 seat independently confirmed 24 and supplied
> > the reason: *the count has grown past 9 because `#497` itself added six sites.* ***
> >
> > **THE DERIVER, so the next reader re-runs it instead of trusting a literal:**
> >
> >     for m in '(once)' 'further occurrences suppressed' 'reported once'; do
> >         printf '%-34s %3s occ %3s files' "$m" \
> >             "$(grep -o "$m" src/devices/*.c | wc -l)" \
> >             "$(grep -l "$m" src/devices/*.c | wc -l)"; echo; done
> >
> > On 2026-08-30 that printed:
> >
> >     (once)                            24 occ   4 files
> >     (further occurrences suppressed)   4 occ   2 files
> >     (reported once)                    5 occ   3 files
> >
> > **THE ADVICE IS UNCHANGED AND STRENGTHENED: `(once)` is the plurality by a WIDER margin
> > than this block claimed.**  Only the literals were wrong.  The growth is this project's
> > own doing, which is exactly why a transcribed count in an auto-loaded file decays: the
> > rounds that consult it are the rounds that change it.
> >
> > *(Superseded literals, kept only as the demoted record of what was measured on
> > 2026-08-26: 9 / 3 / 2 = 14.  Never a current claim.)*
> >
> > **A CAUTION FROM DERIVING IT: one of my four counting methods returned ZERO.**  A regex
> > requiring `fatal(` and `(once)` on the SAME line finds nothing, because the marker sits on
> > a continuation line of a wrapped string.  A single method would have produced a confident
> > wrong answer in either direction; four methods disagreeing is what made the right one
> > obvious.
> >
> > **`(once)` is the plurality and is what a new site should use.** The N=1 per-instance SHAPE
> > is unaffected and unchanged -- only the words. Note the two quantities are different and the
> > "roughly 34 sites" figure is probably a count of latch VARIABLES rather than of suppression
> > markers; it is left standing because nobody has re-counted it, which is exactly the kind of
> > unexamined number this file keeps having to correct.
> >
> > *Found while a seat was checking a DIFFERENT claim, which is how all four carrier
> > corrections today were found. Nothing systematically re-derives these.*
>
> **And the fork has a recorded warrant for KEEPING `fatal()` rather than downgrading it**, at
> `dev_asc.c:250-257`: under `-q` verbosity settles at `VERBOSITY_ERROR`, so a WARNING-level
> `debugmsg` would be **invisible to the boot-log hygiene grep**, and an ERROR-level one would
> trip `#261`'s break-on-ERROR. The chronology runs one way and is worth trusting: `#245` chose
> verbosity-gating; `#265`/`#269`, `#337`, `#460` and `#461` all chose **latch + `fatal()`**.
>
> *`dev_wdc.c` is the tree's REFERENCE implementation -- `dev_dreamcast_gdrom.c:147` says its own
> latch is "Modelled on `dev_wdc.c`'s `warned_badlen` (#337)". The file the rule was about to be
> applied to was already the exemplar it should have cited.*
>
> **The general lesson is not about this idiom.** A rule minted from ONE instance carries that
> instance's shape as if it were the class. The instruction survived contact and the example did
> not, which is the right way round -- but it means **a freshly minted rule's exemplar is a
> hypothesis, and the first round to apply the rule should be asked to CHECK it, not just obey
> it.** Here that cost one census and corrected the rule in the same pass that used it.
>
> ### THE ADDITION LICENCE -- the discriminator against "one more line cannot hurt"
>
> > **Additions to product code in a hardening fork are licensed by MEASURED DELTAS or by a
> > TRANSFERRED WARRANT -- never by "it cannot hurt."**
>
> The same round rejected three additions and each died on a measurement or a named defect:
> sizing the arrays `[4]` was **measured to COST a mutant kill** (it makes `+1` escape `mask9 rt`,
> because that row's kill works by a tick erasing the cell and `[4]` gives index 3 a real slot);
> the `r = 0` clamp would have **defeated `crossarr`**; a disjointness assert **guarded the wrong
> invariant**. The decline arrived with the opposite signature -- a measured delta (`+2`, which
> escapes even `mask9 rt` today, reddens `safe 4` once the decline pins the refusal column) and a
> transferred in-tree warrant. **"Cannot hurt" is not a licence; it is how dead guards accrete.**

> ### *** PROVISIONAL ADJUDICATION -- adopted 2026-08-25, MINTED BY THE ADJUDICATOR AGAINST
> ### ITSELF after it issued a final-sounding ruling on 8 of 9 mandated seats. ***
>
> A round's research stage stood at 8/9. The ninth entry was a **HELD MARKER counted as an
> answer** -- the gap-closes-itself shape -- so the adjudicator ruled as though the roster were
> complete. The ninth seat then landed and **killed the ruling outright**, on a fact that
> defeated its central warrant.
>
> > **AN ADJUDICATION NAMES ITS EVIDENCE BASIS -- "on N of M mandated seats" -- AND ANY RULING
> > ISSUED SHORT OF THE ROSTER IS PROVISIONAL ON ITS FACE. The commit holds until the roster
> > completes or the owner exempts.**
>
> This is section H's spirit applied to adjudication TIMING rather than to stages. And the
> measured case is instructive about what waiting buys: three successive reversals landed
> almost exactly where the position stood before the detour -- **but with the warrants
> transformed**. The churn cost adjudication text and zero code, because nothing was committed
> between reversals. *The hold discipline is what made the reversals free.*
>
> ### THE COMPANION, and it is the reason that ruling was defeatable at all
>
> The refuted warrant had three elements. The adjudicator checked the one it suspected
> (*"is the announced event common and benign?"*), found it non-load-bearing, and shipped. The
> vulnerable element was a different one (*"does the diagnostic announce something REAL?"*) --
> **and the fact that defeated it was already in that round's own record, filed under another
> heading four findings earlier.**
>
> > **BEFORE TRANSFERRING A PRECEDENT, GREP THE ROUND'S OWN FINDINGS AGAINST EACH WARRANT
> > ELEMENT.** A warrant checked only against the facts you have in hand can be defeated by a
> > fact you already hold under a different label.

> **Above floor, measured escapes are COVERAGE DEBT: FILE them**, with the escape list recorded,
> ranked by what they would admit — and ranked BELOW live defects in the same file.

The floor is not invented: it is what four earlier rounds already did. `sh4bcr`'s first detector
passed a mutant reinstating the very host kill its round removed; `sh4pcicexit`'s passed the
original kill verbatim; `pitflip`'s rewind had zero coverage; #446's passed a **217-byte
comment-only file**. All four strengthened or replaced IN-ROUND, and all four were below this
floor. #447's detector is above it, checked row by row — so filing its nine escapes was right.

**Reading "MEASURED FALSE PASS" as "any measured mutant escape" would reproduce #392**: the
measuring seat finds escapes essentially every round and the mutation space is unbounded. The
severity rule settles the ordering — #447's escapes are *hypothetical edits in uncovered product
cells*, while `sh4chcr` is a **measured live host death in the shipped tree**.

> ### *** THE DE-ESCALATION CLAUSE — the one genuinely new rule, and it names a hazard this
> project created for itself four times. ***
>
> **A fatal→survive fix DELETES THE ACCIDENTAL TRIPWIRE that made guard-mask growth
> self-announcing.** Before #447, adding `| TCR_UNIE` to a guard mask meant `exit(1)` on the
> first legal write — unmissable. After it, the same edit means a **silently refused write** and
> nothing anywhere notices.
>
> So: **when a fix removes a host-fatal guard, enumerate from the diff every predicate that used
> to gate death, and the detector shipping with that fix must pin the ACCEPT SIDE of each** — a
> row per adjacent modelled bit or value, proving legal writes still land. Those rows are part
> of the FIX'S COST, not future strengthening, because the fix itself destroyed the old
> (accidental) detector for that class.

It is bounded (the class is exactly "edits the old `exit(1)` would have announced"), and it is
checkable at review time by one question: **does this diff delete `exit(` from a device? then
look for accept rows.** Deliberately NOT mechanised — the enumeration needs judgement about
adjacency, and the existing "what is the smallest edit that breaks this and still passes?" seat
invocation already FINDS the instances. What was missing was never detection; it was
DISPOSITION.

> ### *** ACCEPT-ROW FAILABILITY — the companion rule, adopted 2026-08-21 after #449's accept
> row was MEASURED VACUOUS. ***
>
> An accept-side row is **not discharged by existing** — it is discharged by a **MEASURED
> KILL**. For each predicate the clause enumerates from the diff, build the smallest
> **realistic JOINT** guard-growth mutant — widen the predicate **and** its diagnostic/latch
> operand together, the way adjacent code actually evolves — and the accept row must REDDEN
> under it. A row green under its own growth mutant is vacuous whatever the chosen bit's
> legality.
>
> Choose the pinning value so a guest store can leave it **in the predicate's OPERAND**: read
> the store arm, and cite its line in the row's comment. **Write-1-to-keep, write-to-clear,
> read-only and never-set-by-device bits cannot carry an accept row.**

**"Reaches the predicate's operand" is the checkable notion, and "the guest can produce it" is
one level too shallow** — #449's guest *did* write CMF=1 at the interface; the store arm filtered
it before the predicate ever saw it. The measured kill subsumes reachability, and it catches
wrong-regex, wrong-register and wrong-width vacuities in the same row for free.

*** "JOINT" WAS THE FIRST MEASURED INSTANCE OF THE RULE, NOT THE RULE — restated 2026-08-22
by the flagship seat after #452 measured the opposite case. *** #449's guard-only widening was
measured **EQUIVALENT** (the latch argument still masked to the original bits, so nothing
observable happened) and A1's kill only appears when guard and latch widen together. But at
#451's SCI site the latch operand is a compile-time constant the guard cannot feed, so
guard-only and joint redden the accept rows byte for byte — and guard-only ADDITIONALLY
silences its own growth, printing one diagnostic where joint prints two. **There, guard-only is
the HARDER mutant, and building only the joint form is the WEAKER test.**

> **THE RULE, BY ITS DISCRIMINATOR:** the accept row must redden under the **least-observable
> growth form that is measured NON-EQUIVALENT at that site**. Find it by the reading the rule
> already mandates — read the latch/store arm and cite its line. Where the latch operand CAN
> mask the guard, guard-only is equivalent and JOINT is that form. Where the latch operand is a
> constant the guard cannot feed, guard-only is non-equivalent AND quieter, so it is that form.
> **"Build the form the latch operand does not mask"** is the generalisation, and it is not a
> new rule — it is this rule's own reason made explicit.

Cost stays one mutant per de-fatalised predicate, not per row (#448 = 4 builds, #449 = 1).
**Where the reading is uncertain, build BOTH** — #451 proved both directions measurable in
minutes, and a spare build is cheaper than a wrong reading.

> ### *** THE ASK-AGAIN, ADOPTED 2026-08-22, AND ITS CAP IS THE WHOLE SAFETY. ***
>
> **Once a detector's kill table is CLEAN, ask the panel once more for another mutant.**
> Measured yield: 2 of the 5 rows #451 added, and 6 of the 15 in #452, came only from that
> second ask — after the first table was already green. The mechanism is real: a clean table
> redirects seats away from the shapes the author already thought of.
>
> **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
> unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
> against a clean table with a measured stop: nothing found, done; something found, row added
> under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
> is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
>
> > ### *** THE CAP COUNTS **ASKS**, NEVER **FINDINGS**. Adjudicated 2026-08-28, because the
> > ### singular in the sentence above ("row added", "something found") invited the opposite
> > ### reading and that reading NEARLY FILED A FLOOR BREACH. ***
> >
> > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
> > floor breach among the findings is L2, repaired in-round however late it is found.** A
> > second ASK is where the #392 chain starts; the number of rows one ask yields is not.
> >
> > **The founding measurement already said so and the wording contradicted it:** this block's
> > own text records *"6 of the 15 in #452 came only from that second ask."* A reading under
> > which #452 should have taken one row and filed five is refuted by the paragraph that mints
> > the rule.
> >
> > **The live cost of the misreading, from `#488`:** three escapes were found by one ask; the
> > author took one and filed two, reasoning "the cap says I may take only one". `E1` was
> > `if (X)` -> `if (X && Y)` on the DOMINATING predicate — the canonical clause-(d) form, i.e.
> > a floor breach, which the floor says must be repaired in-round. **So one rule's cap was
> > about to silently override another rule's MUST.** A reading that produces that collision is
> > wrong on its face.
> >
> > The anti-runaway property is untouched: the bounded resource was always the adversarial
> > QUERY, and what it returns is bounded by being the findings of ONE query against ONE clean
> > table.

> ### *** THE ORACLE-CORRECTION RULE — adopted 2026-08-22, and it is TEST-FIRST restated
> for the case test-first did not cover. ***
>
> Sometimes the DETECTOR is the thing that is wrong: a shipped row pins the opposite of the
> architecture, so correcting the code turns the row red. Re-pinning it is then necessary —
> and it is also **observationally identical to fitting the test to the binary**, which is
> the classic way to fake a green detector.
>
> **THE DISCRIMINATOR IS ORDER, AND IT IS MECHANICAL:**
>
> > **Re-pin the oracle FIRST. Measure the COMMITTED build RED under the new expectations.
> > THEN change the code.** Same scripts, opposite colour. If you cannot show that red, you
> > do not have test-first, and the re-pin collapses into laundering.
>
> Three further obligations, each from a seat that reached it independently:
> * **PROVENANCE MUST SHOW.** The rewritten row comment quotes the source VERBATIM with
>   file/line, so a future seat can re-derive it without trusting this round. The old pin's
>   authority is the thing being overturned, so it cannot also be the warrant.
> * **CORRECT THE FALSE RECORD IN PLACE**, never silently supersede it. A re-pinned oracle
>   sitting next to an uncorrected claim of provenance is exactly what laundering looks like
>   from outside.
> * **A RE-PIN THAT REMOVES THE LAST FAILING ROW IS NOT FINISHED.** Ask what still faults
>   after the correction. If the answer is "one row, and it observes the same value either
>   way", the round owes a row on the OTHER observable channel before it may ship.
>
> *Provenance of the rule itself: the `sqreadtype` pass-1 panel. The brief proposed the
> re-pin in the WRONG ORDER and no seat let it pass; one named the order fix, a second
> supplied the provenance half, a third put it strongest — the re-pin **is** laundering
> unless the new-channel row ships with it.*

> ### *** A MUTANT THAT WILL NOT DIE IS A RESULT, NOT NOISE. Adopted 2026-08-23 by the
> regress seat, after one round produced three of them with three DIFFERENT causes. ***
>
> A mutant that cannot be made to fail has **exactly three explanations**, and silently
> re-aiming it picks one without measuring which:
>
> 1. **The mutant is mis-built.** A single edit meaning to restore a historical defect
>    measured GREEN because `re.I` supplied the case-insensitivity the edit targeted --
>    the defect needed two edits, and the one-edit form reported a row as defended when
>    nothing defended it.
> 2. **The target is dead.** A class the regex no longer needed; deleting it changed
>    nothing, which is a finding about the code, not the test.
> 3. **The row is mis-cut.** Four rows were rejected by a newly-added anchor BEFORE
>    their own guard was reached, so four live guards looked dead. Each row was re-cut
>    to start with the label so only the guard under test can reject it.
>
> This is not a generalisation from two cases: the carrier already treats non-dying
> mutants as results twice — #449's guard-only widening measured EQUIVALENT, #451's
> measured the opposite — and equivalence-disposition is this same question one level
> down.
>
> #### *** AN ABSENCE RECORD IS TIME-INDEXED, AND THIS ONE WENT FALSE WITHIN ONE
> COMMIT. ***
>
> Case 2 above was recorded honestly: the class was measured dead, deleted, and its
> absence written down **with its warrant** ("`re.search` is unanchored, so the match
> starts at the label and the TRAILING class consumes the closing `**`").
>
> The very next commit **anchored the label and introduced a new leading class** —
> broader than the one that died — and nothing re-ran the death measurement. A regress
> seat checked out the earlier revision to verify the original warrant, then measured
> HEAD: dropping the new class reddens a row. The class was alive, load-bearing, and
> covered by no mutant at all.
>
> > **THE RULE: an absence record must NAME ITS WARRANT, and any edit touching that
> > warrant RE-RUNS THE DEATH MEASUREMENT.**
>
> Naming the warrant is what made the record falsifiable — it is the only reason the
> claim could be re-tested at all. *"Deleted, absence recorded as the result" was the
> right disposition; the missing half was the expiry check.*
>
> #### MULTI-PART MUTANTS ARE LICENSED, NOT THE DEFAULT
>
> The main loop proposed making multi-part the default form. **The adjudicating seat
> said no**, and gave the boundary: the default stays the SMALLEST SINGLE EDIT, with
> multi-part licensed in exactly two shapes:
>
> * **(i) verbatim reinstatement of what shipped** — floor clause (b) applied to a
>   harness tool, taking however many edits the historical diff took;
> * **(ii) reach-the-guard composites where EVERY added edit is first measured GREEN
>   ALONE** — e.g. a guard unreachable under the shipped regex, where the other edits
>   are the only road to it.
>
> **That second condition is what answers the unfalsifiability objection**, which the
> main loop had raised against its own proposal: an unconstrained composite can be
> steered until it fails for an unrelated reason, while a composite whose parts are
> proven inert can only fail through the interaction being claimed.
>
> Bonus property worth knowing: a driver that treats MUTANT-TEXT-NOT-FOUND as a FAIL
> turns every find-text into a **presence pin**, so a multi-part mutant additionally
> pins the existence of each feature it edits.

> ### THE FOUR REASONS THAT LICENSE AN IN-ROUND FIX OF DETECTOR MATERIAL
>
> Everything else is FILED. Named so no round has to re-argue it:
>
> * **L1 — pre-ship construction.** The row is part of the deliverable still being built. A row
>   measured vacuous before commit is unfinished, not a reopening. **The stopping rule governs
>   findings against SHIPPED material only.**
> * **L2 — floor breach.** The shipped detector fails vacuity-floor clause (a), (b) or (c) —
>   replace in-round however late it is found.
> * **L3 — undischarged obligation.** The row is the sole carrier of something the round OWES
>   (a de-escalation accept row; the "shipped a detector" claim itself). A vacuous sole carrier
>   makes the round's record false.
> * **L4 — wrong record.** Prose or comments claiming coverage a measurement refutes.

This resolves an apparent inconsistency: #447's escapes were FILED while #448's and #449's were
fixed in-round. #447's were measured against a **shipped** detector sitting above the floor —
coverage debt. #448's and #449's were caught **inside their own construction** (L1), and #448's
`return`→`break` variant additionally re-reached the removed `exit(1)`, which is L2.

**A disjointness assertion over the latch classes was REJECTED, on three measured grounds** — the
class bit-domains overlap pervasively today, so the general form is unsatisfiable; separation
rests on the array INDICES rather than on the constants, so the assert would guard the wrong
invariant; and for the one disjoint pair the values are hardware register layouts that cannot
legitimately change, so it could never fire. **The real hazard is a duplicate class ID**, and its
zero-cost structural fix is converting the `SH4_VAL_*` defines to a C99 enum ending in
`_NCLASS`, where duplicates are impossible by construction.

*** DISCHARGED -- DO NOT REDO IT. Verified 2026-08-23 by opening the file. *** The trigger
was "when a tenth class arrives"; `SH4_VAL_SCICMD` was the tenth, the conversion happened,
and `dev_sh4.c:124` is now `enum {` ending in `SH4_VAL_NCLASS`, with the file's own comment
at `:119-122` recording that the pre-set trigger fired. An eleventh class is therefore free.
This paragraph is kept for its reasoning; its instruction is complete.

This applies to the whole #438 / #441 / #443 / #447 family, and #447's own probe already *stated*
the hazard in its constants block ("a mask pinned only from BELOW … cannot see a guard that
GREW") while shipping no row for it. **The file knew. The rows just did not exist.**

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
  off to weekly -- **SUNDAYS 18:00**, scheduled task `GXemul-weekly-battery`; it was
  moved there from Saturday 03:00 and this line said Saturday until 2026-08-26.
  *`nightly_check.sh:45-52` had ALREADY RECORDED that a doc "still said ... Saturdays
  03:00 afterwards" -- the tool noticed the drift and the carrier kept it, which is the
  structure-knew-and-prose-did-not shape again*), alone,
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
executed?" — with `armbdt` as the proof (no ARM rig exists, yet gate 14 runs **358** real-decode
checks across `testarm`, `barearm` and `cats` -- this said "261 ... on `testarm`" until
2026-08-26; commit `6014b7e`'s own message records "PASS 358 checks (was 261)", and
`gate_arm.sh:561` carried the same stale number in its own comment). But only executions that preserve the committed hardware selection and
routing count. The ladder, and what each rung licenses:

1. **`#include`/direct-call harness — NEVER a reproduction.** The discriminator is mechanical:
   *if it still compiles and still fails after the machine description and CPU/device dispatch
   are removed, leaving only a direct call, it was never a reproduction* — it is a restatement
   of the source. (It measurably distorts, too: m8820x's offline repro reported 1013/1015/11
   where the true numbers were 1007/1009/17, a NULL-callback stub artefact.) Such harnesses are
   DETECTORS and still ship as regression rows — graded by the vacuity taxonomy (must fail on a
   mutant), never by the witness clauses.
2. **Machine construction** (gate 9's mechanism, **41 types / 58 subtypes**; this said
   "23 types" until 2026-08-26, and `gate_asan_sweep.sh:11` keeps the 23 only as history
   while `:26` reasons about "15 of the 41") — a reproduction ONLY for defects in
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
per-probe; (ii) **for ACCESS witnesses (rungs 3–4)** it carries a LIVENESS control (a known value
returns through the same decode) AND a DEVICE-SIGNATURE control (the observed value could only
have come from the device — RAM would answer differently; **the footbridge probe's first draft
returned 0x0 everywhere WITH ITS RAM CONTROL GREEN**, so one control is not enough); (iii) the
machine description and dispatch are committed and unmodified — a machine or `device_add`
introduced IN ORDER TO reach the site is
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
has a rung-4 boot witness but a guest-visible symptom measured NIL **on the pair that was
compared**, while `armbdt` has only a rung-3 probe and CORRUPTS GUEST DATA. So:

> #### *** THE EXEMPLAR OVERSTATED ITS OWN EVIDENCE, corrected 2026-08-26 by the codex seat
> #### answering `b120r`'s held stage -- and the refutation was sitting in `b120r`'s own
> #### ledger row the whole time. ***
>
> This clause used to read *"a MEASURED guest-visible symptom of NIL (two transcripts
> byte-identical)"*. The row says something narrower: `told-98` vs `told-35/11` give ORDERED
> TRANSCRIPTS IDENTICAL, 0 diff lines across 97 lines each -- **but `told-0` FLIPS CONTROL
> FLOW, 32 MODE SENSE commands instead of 11, including MODE SENSE(10) fallbacks and page 5,
> because OpenBSD 7.7 branches on that byte.**
>
> **So NIL was measured for a PAIR, and restated as a property of the PARAMETER.** That is the
> dropped-qualifier class again, in the file that teaches it -- and note the qualifier was never
> missing from the evidence, only from the summary, which is exactly how `#464`'s "floods
> identically" went wrong on the same day.
>
> **THE RULE IS UNCHANGED AND THE EXEMPLAR IS WEAKER.** Rung still measures reachability-proof
> strength and not harm; `armbdt` still corrupts guest data and still outranks `b120r`. What
> changes is that the contrast is severity-versus-*small* severity rather than
> severity-versus-nothing -- so this pair no longer makes the point as sharply as it reads, and
> a future round wanting a clean illustration should find a better one rather than lean on this.
>
> *This is the anchor rule's lesson recurring: a rule minted from ONE instance carries that
> instance's shape as if it were the class, and **a freshly minted rule's exemplar is a
> hypothesis**. The instruction survived contact; the example did not.*
**a witness makes an item ELIGIBLE; SEVERITY and gate blind-spots order the queue.** Rung
is a floor on admissibility, never a priority. Strongest witness today — boot > probe >
construction **"No witness of either kind" is a CHECKABLE claim and must be checked, not
asserted.**

> #### *** THE EXEMPLAR THAT USED TO SIT HERE WAS WRONG, corrected 2026-08-26. The RULE is
> #### untouched -- it is one of the most useful lines in this file -- but `dfreq` is not an
> #### instance of it. ***
>
> This clause read *"dfreq's was measured false by building the witness in one session."*
> Checked against the row and the probe: **`dfreq`'s `witness` field is `None`.** Its closure
> names *"the MIPS compare write ... converts the distance to a deadline into a frequency"*,
> i.e. MIPS CP0 Compare -- while the row mentions ARM Footbridge four times and MIPS CP0 not
> once. **The probe that was actually built (`footbridge_sites_probe.py:111`) execs `-E cats`,
> an ARM/SA110 machine that executes no MIPS instruction and cannot reach CP0 Compare.** It
> returned entirely CORRECT values, and its own cited line has since gone stale
> (`dev_footbridge.c:548` is `console_putchar`; the timer mask is at `:640`).
>
> So a witness was built and it witnesses a DIFFERENT PATH from the one the row's closure
> defines. The row is internally conflated, which is the finding -- not the rule's failure.
> Found by the codex seat answering `dfreq`'s held stage; every element re-verified here
> before the edit.
>
> ### *** AND THIS IS THE THIRD EXEMPLAR IN THIS FILE TO FAIL IN A SINGLE DAY WHILE ITS RULE
> ### HELD. That ratio is itself a finding about this file. ***
>
> The anchor rule's `mask9 rt` ("anchored to a cell, not to a neighbour by distance" -- it is
> anchored by distance); `b120r`'s "MEASURED symptom of NIL" (NIL for the pair compared, and
> `told-0` flips control flow); and now `dfreq`. **Three rules, three intact instructions,
> three broken examples.**
>
> The reason is structural rather than careless. **A rule is a claim about a CLASS and ages
> well; an exemplar is a frozen claim about ONE INSTANCE, and instances move** -- code is
> edited, rows are re-scoped, line numbers drift, and a row can be silently conflated with a
> second defect. Nothing re-checks an example once it is written down, because it reads as
> illustration rather than as an assertion.
>
> **So: an exemplar in this file is a DATED MEASUREMENT wearing the clothes of an
> illustration.** When a round leans on one, re-derive it rather than cite it -- and if it has
> decayed, correct it in place and keep the rule. All three today were caught that way, and in
> all three the instruction survived contact while the example did not.

**Round scope (the reopening rule):** a witness makes a site ELIGIBLE, never mandatory. A round
takes ONE site; a second joins only if it is witnessed, in the SAME device and SAME semantic class
under the third doctrine arm (so one fix design covers both), and covered by the SAME detector
with no new oracle. **More witnesses create more candidate ROUNDS, never bigger rounds.**

### *** TWO CORRECTIONS TO THIS LADDER, 2026-08-26, from `reprowitness`'s held stage. The
### ladder failed its OWN exemplar, and its own checker had already written down the second gap. ***

**(a) CLAUSE (ii) IS SCOPED TO ACCESS WITNESSES, RUNGS 3–4 — it was written as rung-2–4 and is
UNSATISFIABLE AT RUNG 2.** Rung 2 admits machine construction for init-time defects and names the
macppc heap OOB (#23). A construction-time OOB **performs no address decode and returns no device
value**, so it cannot carry a control of the form "a known value returns through the same decode".
The ladder's own exemplar could not satisfy the ladder's own clause, and had not been able to
since the day both were written.

> **A RUNG-2 WITNESS OWES CONSTRUCTION-SPECIFIC CONTROLS INSTEAD, and they are the same idea
> aimed at a different channel:** a LIVENESS control that the construction under test actually
> ran (the gate's own object count, or the machine type appearing in its list), and an
> ATTRIBUTION control that the observed failure came from THIS construction rather than from the
> harness or a neighbour (rebuild it alone; show the symptom follows the machine type). Same
> two-control discipline; different observable, because there is no decode to route through.

**(b) THERE IS A FIFTH WITNESS KIND, `harness:`, AND THIS FILE NEVER SAID SO WHILE ITS OWN
CHECKER ENFORCED IT.** `check_witness.py:56` has accepted
`^(boot:|probe:|construction:|harness:|none)` since its first run, and its header at `:24-28`
states the finding outright: **none of the four rungs fits a defect in the TEST APPARATUS
ITSELF**. `precommit_check.sh:678` repeats it. Meanwhile the prose above still said "no witness
at rung 2–4 → document instead", with no exception.

> **`harness:<what proved it>` is a valid witness EXACTLY WHEN THE ROUND'S SUBJECT IS THE TEST
> APPARATUS** — a gate, a probe, a checker — and the proof is normally a MUTATION: the tool fails
> on a mutant it should catch. **It never licenses an `#include`/direct-call witness for emulator
> code**, which rung 1 rejects and which stays rejected; that boundary is what keeps this from
> becoming a hole.

*This is the structure-versus-prose failure INVERTED, and worth noticing in that form: the usual
shape is a rule living in prose that never fires. Here the STRUCTURE knew — the checker had the
category, enforced it, and documented why — and the PROSE never absorbed it. Auto-loaded text can
be stale in both directions, and a tool's own header is a primary source about the tool.*

**Ledger:** a row that closes with commits names its witness: `boot:<rig/gate>`, `probe:<path>`,
`construction:<gate>`, `harness:<what proved it>`, or `none` (documented-only).

### *** CLOSING A ROW AS **OVERTAKEN** -- THE THREE CONDITIONS. Adjudicated 2026-08-28. ***

A row closed because SOMEONE ELSE'S fix removed the defect adds **no row of its own**, and that
is correct rather than lazy: row demand is bounded PER ENUMERATED MUTANT, never per attribution
need, and a row added so that coverage "is attributable" is the **addition licence's "cannot
hurt" wearing detector clothes**. `#462` measured the real cost -- added rows perturb other
mutants' scores and force a full re-table.

> **But the disposition is only available on three conditions, and a copier must meet all
> three:**
> 1. **A DISCRIMINATING CONTROL, MEASURED AT HEAD** -- neutralise the overtaking fix and this
>    row's OWN symptom figures come back.
> 2. **THE CARRYING ROWS NAMED** by label and probe path, in the witness or closure field.
> 3. **THE CONTROL MEASUREMENT PRESERVED AT A DURABLE PATH** -- not `_scratchpad/`.
>
> **A candidate that cannot meet (1) or (2) is NOT overtaken** -- it is either still live, or it
> owes a carrier of its own. That sentence is the whole discriminator.

**Attribution is a RECORDS property and lives in the witness field**, which is why no row is
owed: `wdcoddstep`'s reads `detector:regress/diff_wdc_identify.c -- the two 'odd chunk:' rows
shipped by #475 pin both halves`, and its control sits in `regress/artifacts/wdcoddstep/`.

*Condition 3 is not decoration and the exemplar nearly failed it: that row's own `ev` field
cited `_scratchpad/odd/out` and `_scratchpad/oddm/out`, **both since deleted**, while the durable
copies had existed the whole time. The precedent-setting row was one `ls` away from being
unverifiable.*

### *** A SIXTH TERM, `detector:<path>` -- OWNER DECISION 2026-08-27, WITH A BOUND THAT IS
### PART OF THE ADOPTION AND NOT A FOOTNOTE TO IT. ***

**The gap, and it took three rounds to become visible.** `b115` (#472),
`wdcringambig`/`wdcrearmzero` (#473) and `fbclearread` (#474) each shipped a REAL FIX to
emulator code whose only evidence is an offline differential plus a measured kill table.
**None of the five terms fitted.** `boot:`/`construction:` are false. **`probe:` is actively
DANGEROUS** -- `check_witness.py`'s shape regex scores it rung-3, which that file's own header
calls laundering. `harness:` is admitted only when the round's SUBJECT is the test apparatus,
and all three fix emulator code. And `none` is defined as DOCUMENTED-ONLY, so on a round that
shipped a fix **it asserts that no code changed.**

So each round parked at `held` carrying a prose note -- **the note doing work a schema value
should do.** Survivable once; at three it is a pattern, and a fourth would have copied
whichever note it found.

> **THE BOUND: `detector:` IS NOT A RUNG.** It records that a fix shipped with a MEASURED
> DETECTOR and no guest-path witness. It ranks BELOW every access witness, and it does NOT
> satisfy the reproduce-before-you-edit step: **a round using it still owes the rung-3 ATTEMPT**
> the 2026-08-27 lifecycle ruling requires, and must record that the attempt was made and what
> it found. The one thing it may never mean is *we did not think to ask*.

It exists so the checker can tell FIXED-WITH-A-DETECTOR from DOCUMENTED-ONLY, which it could
not do before -- both had to be written `none`, and that conflation is what made three honest
rounds look like three rounds that shipped nothing.

*The alternative put to the owner was a per-round exemption. It was declined for a reason worth
keeping: an exemption is a NOTE, and a note is exactly what had already failed three times. The
cost the owner accepted is real and is written here rather than glossed -- **adding a term
changes what every future round may claim** -- which is why the bound above is part of the
adoption.*

Controlled in both directions on the day it landed: `detector:<path>` passes, a bare
`detector:` with no path is REFUSED, the near-miss `detectorish:` is REFUSED, and all five
pre-existing terms still pass unchanged.
 Forward-only from
2026-08-19.

## Round lifecycle, with the end-of-round parallel step

1. Claim the top TaskList item (or top of OUTSTANDING_BUGS "OPEN LIST").
2. Reproduce on the committed build per the WITNESS LADDER. No witness at rung
   2–4 → document instead, stop.
   > ### *** BEFORE RECORDING A ROUND AS RUNG-1, ASK ONE SEAT TO TRY A RUNG-3 PROBE.
   > ### Owner ruling 2026-08-27, and the evidence is that nobody had asked. ***
   >
   > Three rounds shipped on offline differential fixtures with `witness: none`, and
   > the ladder was blamed for having no term that fits. Then a seat was asked, once,
   > and **built a rung-3 witness for `wdcdataoutdrain` in a SINGLE invocation** — a
   > guest arming WRITE SECTORS and issuing one `sd` on unmodified `evbmips -e malta`,
   > with the sector clobbered pre-fix, clean post-fix, and an accept control.
   >
   > **So the gap was HABIT, not a hole in the ladder**, and the ruling is deliberately
   > NOT a new ladder term: admitting differentials as their own rung would legitimise
   > the shortcut the ladder exists to discourage. The ladder was always fine.
   >
   > **The ask costs one invocation and is the cheapest thing in this file.** A seat
   > that reports it cannot build one has given a real answer and the round proceeds
   > as documented-only — with the ATTEMPT recorded, so `none` means "tried and could
   > not" rather than "did not think to". Those are different states and must not
   > render the same, which is this project's oldest rule about blanks.
   >
   > *It sits HERE, in the lifecycle step, rather than in the ladder — the carrier's
   > own finding is that the one piece of prose which demonstrably fires is the
   > premise-audit line, because it lives in the artifact present at the moment of
   > decision. This is that moment.*
3. Design brief → **panel pass 1** → converge (empirically where split).
   > ### *** START FROM `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md`.  DO NOT WRITE A BRIEF FROM
   > ### MEMORY. *** Adopted 2026-08-28 by flagship adjudication.
   >
   > It carries the premise-audit opener, the tree-naming line, the **SETTLED PREMISES**
   > section, the full-enclosing-function rule, and the three-question set — each with the
   > measured incident that bought it.
   >
   > **THE RULING THAT CREATED IT, because the evidence is unusually clean:** the settled-
   > premises block was invented on 2026-08-27 from `#488`'s loss of three seat-answers,
   > **applied correctly that same evening at 22:21, and dropped at 11:55 the next morning by
   > its own author in the next brief of the same campaign.**  Fourteen hours from minting to
   > breaking, and nobody had forgotten it.  Two packet-fed seats then spent their entire
   > answers re-deriving `fatal()` returns.
   >
   > That is this file's own structure-first test met exactly — *"a rule that earns its SECOND
   > INSTANCE while sitting in this file has thereby proven it was mis-filed as prose"* — and
   > it earned the second instance **before it was even filed**, against the person who
   > proposed it.
   >
   > **The obligation is PER-PACKET and BROAD:** any packet-fed brief re-inlines every settled
   > premise its own questions depend on, whatever pass or round settled it.  The narrow
   > "pass 2 re-inlines pass 1" form was considered and **refuted by its own second instance**,
   > which ran pass-1-to-pass-1 across two rounds with no pass 2 in the story.
   >
   > Stop condition, so it cannot become "inline everything": settled means a RECORDED
   > resolution citable in a line or two with its warrant; a premise enters only if a question
   > in THIS brief depends on it (test: could a seat build an "if X then A, else B" answer on
   > it?); and scope is the CAMPAIGN, with cross-campaign premises escalating to the template
   > skeleton — **never into `panel_ollama.py`, whose preamble stays semantic-free.**
4. Implement (byte-identical in both trees for shared files); propagate to build trees.
5. **Panel pass 2** on the real diff.
5b. **THE ADJUDICATION PASS — the panel SHARES its findings.** *** STANDING OWNER DIRECTIVE,
   2026-08-30: "always adjudicate findings and make sure the full panel shares findings." ***
   Consolidate every seat's pass-2 findings into ONE numbered packet with YOUR DISPOSITION on
   each, list the DISAGREEMENTS separately with both sides in their own words, and re-fire all
   nine. **Template section `§F2` carries the shape; do not write it from memory.**

   **Why it is a pass and not a tidy-up:** until this directive every seat answered blind to
   the other eight and the main loop silently arbitrated — so a seat could not correct another
   seat's error, and *a disagreement was resolved by whoever wrote it up*. That is the
   seat-failure-counted-as-agreement shape moved into the arbitration step, where nothing in
   the harness looks for it.

   **Ask the parties to adjudicate their OWN disputes, and ask a seat reviewing its own
   finding to be HARDER on it** — including whether the FIX is right, not merely whether the
   finding was. Those are different claims and the second does not imply the first. Same for a
   ruling that ADOPTS a seat's position: that seat scrutinises it MORE, because a ruling in
   your favour is the one you are least likely to test.

   **The load-bearing question is "WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?"**, asked with
   the count named. A round that accepted everything has either had a very good panel or has
   stopped arguing, and only a seat can tell you which.
6. `GXEMUL-SEC/regress/run.sh` → `REGRESS_PASS`. **Never run two harness/gate invocations
   concurrently** — but *** THE REASON GIVEN HERE FOR FOUR MONTHS WAS WRONG, corrected by
   measurement 2026-08-14: `selftest_mutation.sh` does NOT `rm -rf` the shared workdir. It is
   `T=$LOGDIR/mutation` and `rm -rf "$T"` -- scoped to one subdirectory. *(Cited as
   `:27`/`:41` until 2026-08-26; they are `:40`/`:54` today. Re-keyed to the code itself:
   `grep -n 'LOGDIR/mutation' selftest_mutation.sh` resolves it at any commit.)* *** Nor do
   the rig images serialise: both consumers open them read-only with `R:` and the overlay is
   pid-unique. **The real serialisers are three producer/consumer orderings and a load-sensitive
   oracle**, and they are worse than the wrong reason was: `gate_build.sh:64-65` WITHDRAWS
   `/tmp/gxsec-gxemul` and `$RIG/gxsec-gxemul` at gate start and republishes only at `:302-305`,
   while `gate_mips.sh:30` `need_exec`s it — concurrent runs make gate 4 `gate_skip` on a missing
   binary, which is **silent coverage loss scored as SKIP**; `gate_hygiene.sh` grades pty
   logs that gates 4 and 5 produce (the block cited as `:198-258` has moved; its own header
   comment says it "READS THE RAW PTY LOGS ON PURPOSE", which is the durable key), so concurrency grades a partial log and yields **a wrong
   answer, not a crash**; `gate_ab.sh`'s `rm -rf "$dir"; mkdir -p "$dir"` (cited as `:42`, now `:43` --
   grep the statement, not the line) removes `/tmp/gx-pristine` and `/tmp/gx-prebatch`,
   which `gate_upstream.sh:46-47` reads. A per-gate `LOGDIR` would NOT isolate them, because
   the ORDERINGS above are what serialise the gates — the driver's own hardcode is gone (#422:
   `drive_guest.py` honours `$LOGDIR` -- `grep -n 'honour .LOGDIR' drive_guest.py`, at
   `:239` today and cited as `:207-211` until 2026-08-26 -- and `lib.sh` exports it), and it changed nothing
   about them. **47 wall-clock oracles by direct census 2026-08-26** -- `while time.time() - t < ...`
   loops across **27** python files in `regress/`, where this line said 33 loops in 18
   files. *(An auditing seat counting slightly differently got 45; the number moves with
   the regex, so what matters is that it GREW rather than the exact value -- the
   concurrency warning is more strongly supported now, not less.)* Plus
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

*** AND `dc21285.pdf` / `dc21285.txt` (Intel 278115-001, the DC21285 'Footbridge' core logic
controller) HAVE BEEN PRESENT SINCE 2026-08-15 AND THIS LIST DID NOT SAY SO UNTIL 2026-08-27. ***

It was found by a seat that went looking for it rather than by this list, and it immediately
settled a round that was about to transfer the wrong warrant: the `+0x188` read arm in
`dev_footbridge.c` was being treated as an unimplemented register needing a decline, and Table
7-10 (`dc21285.txt:6826`) plus the prose at `:6911-6915` say it is **IRQEnable, a documented
read-only register** -- *"The value of this register can only be changed by writing to the
EnableSet and EnableClear registers"*, reset value 0. The model already returns the right value
and then calls `exit(1)` on it.

**That produced a FOURTH member of the de-fatalisation option set, which the three-membered rule
above does not contain: ACCEPT.** delete / decline / decline+bounded-announce all presume the
access is unserviceable. Where the model already computes the correct answer and then discards
it, the disposition is to delete the kill and KEEP THE VALUE -- no latch, no message, because
there is no event to announce. *A bounded-announce here would ship a wrong record in product
code: printing "unimplemented; ignored" about a read that is implemented and is not ignored.*

**The general lesson is about this list, not about footbridge: an absent-source note is
load-bearing and this one was wrong for twelve days.** The same failure is already recorded
above for the SH manual, where 'there is no SH documentation' was load-bearing for four rounds.
**Before reasoning from first principles about a device, `ls _scratchpad/*.pdf` -- do not trust
this paragraph to be complete.**

*** THE COMPLETE LIST, DERIVED 2026-08-27 BY `ls _scratchpad/*.pdf` RATHER THAN TRANSCRIBED.
FIFTEEN PDFs ARE PRESENT AND THE PROSE ABOVE NAMED ABOUT SEVEN. ***

```
  dc21285.pdf
  ddi0100i.pdf
  i8254.pdf
  idt_r30xx.pdf
  mc88100.pdf
  mips-iv.pdf
  mips32_volII.pdf
  mips64_volII.pdf
  mips_r4000.pdf
  ppc_oea_book3_v201.pdf
  ppc_pem32_rev2_2001.pdf
  ppc_pem_32and64_2005.pdf
  ppc_vea_book2_v201.pdf
  sh4_programming.pdf
  sh7750_hardware.pdf
```

**SIX were undocumented**, and two of them are load-bearing for work in flight the day this was
derived: **`i8254.pdf`** (three PIT rows were worked this week arguing about counter behaviour
from the source alone) and **four PowerPC manuals** -- `ppc_oea_book3_v201`, `ppc_pem32_rev2_2001`,
`ppc_pem_32and64_2005`, `ppc_vea_book2_v201` -- while a PowerPC straddling-store defect
(`mrwstore2`) was being recorded with no reference to any of them.

Extracted text PAIRED with one of those manuals (grep these, not the PDFs):

```
  dc21285.txt
  ddi0100i.txt
  i8254.txt
  idt_r30xx.txt
  mc88100.txt
  mips-iv.txt
  mips32_volII.txt
  mips64_volII.txt
  mips_r4000.txt
  ppc_oea_book3_v201.txt
  ppc_pem32_rev2_2001.txt
  ppc_pem_32and64_2005.txt
  ppc_vea_book2_v201.txt
  sh4_programming.txt
  sh7750_hardware.txt
```

> **THE RULE THAT REPLACES MAINTAINING THIS LIST BY HAND: `ls _scratchpad/*.pdf` IS THE
> AUTHORITY, AND IT COSTS ONE COMMAND.** This paragraph has now been wrong twice in the same
> way -- 'there is no SH documentation' was load-bearing for four rounds, and the footbridge
> datasheet sat unlisted for twelve days while a round reasoned around it. A hand-maintained
> inventory of files is a wrong record waiting for someone to add a file.


*** SH DOCUMENTATION NOW EXISTS — OBTAINED 2026-08-22 BY OWNER DIRECTIVE, AND THE FIRST
THING IT DID WAS REFUTE A FINDING THIS PROJECT WAS ABOUT TO FILE. ***

`_scratchpad/sh7750_hardware.txt` (2.4 MB, 50,853 lines, from `sh7750_hardware.pdf`,
Renesas SH7750/SH7750S/SH7750R Hardware Manual Rev.7.00, REJ09B0366-0700, 1074 pages) and
`_scratchpad/sh4_programming.txt` (661 KB, from `sh4_programming.pdf`). Extracted with
git-bash `/mingw64/bin/pdftotext -layout` — the same tool that made `ddi0100i.txt`; note
WSL Gentoo has NO poppler, so run the extractor from git-bash.

**The old note said there was none, and that note was load-bearing for four SH rounds.**
It is kept below in substance because its CAUTION still holds even though its FACT does
not: cite only what you have READ in these files. `#357`/`#362`/`#365` shipped DDI 0100I
page numbers that came from panel LLM output rather than a local manual, and the same
temptation exists here — a web SEARCH RESULT summarising a manual is not the manual, and
on 2026-08-22 a search summary and the real page agreed only by luck.

**WHAT IT SETTLED IMMEDIATELY** (`#452`, and it went AGAINST the main loop's reasoning):
the loop had argued that `dev_sh4.c`'s `aa` handlers ignoring address bit 23 while the
`da1` handlers treat it as selecting a second array meant "one of those is wrong". The
manual says both are right — P4 gives `H'F200 0000`–`H'F2FF FFFF` to the instruction TLB
ADDRESS array as ONE undivided 16 MB region, while `H'F300 0000`–`H'F3FF FFFF` holds
instruction TLB data arrays **1 AND 2**, split at `H'F380 0000`. Same for `H'F600 0000`
(UTLB address, undivided) versus `H'F700 0000` (UTLB data 1 and 2, split). §3.7.3 also
confirms the entry is "selected by bits [9:8]", matching `SH4_ITLB_E_MASK`, and that array
2 holds SA and TC — **different fields from array 1**, which is why `#452` declines those
accesses rather than aliasing them onto array 1.

*** THE EXTRACTED TABLES STAGGER NAMES AGAINST VALUES, AND THE STAGGER READS AS A
CONTRADICTION. Decode it against a block the tree ALREADY PINS -- do not "correct" code
from a raw table row. (2026-08-23, #458.) ***

`pdftotext -layout` renders a vertically-centered table cell on a different line from its
row's value. Table 19.4 comes out as `RTC ATI H'480` / `H'4A0` / `PRI H'4C0` / `CUI`,
which reads as *PRI = H'4C0* and would have condemned three correct constants.

**The decoder is the SCI block four rows below it**, because `sh4_exception.h:93-96`
already pins SCI ERI/RXI/TXI/TEI at `0x4e0/0x500/0x520/0x540` in shipped, working code.
That extraction shows `SCI ERI H'4E0` / `H'500` / `RXI H'520` / `H'540` / `TXI` / `TEI` --
which reconciles with the header ONLY if names and values pair **strictly in order down
each column**, the printed adjacency being an artefact. Apply that to RTC and ATI/PRI/CUI
are `0x480/0x4a0/0x4c0`, which is what the code says.

**The general rule: before citing a value from an extracted table, find a row in the SAME
table whose answer this tree independently knows, and use it to calibrate the layout.** A
second, unstaggered table elsewhere in the manual (here `:32655`, DMTE0/DMAE) is the other
confirmation and is worth grepping for -- these manuals list most codes twice.

> ### *** ONE CALIBRATION POINT IS NOT ENOUGH, AND THE RULE ABOVE WOULD HAVE CERTIFIED A
> ### TABLE THAT WAS WRONG FROM ITS FOURTH ROW DOWN. Measured 2026-08-26 on `sh4tlbda2`. ***
>
> Table 19.4's stagger was UNIFORM -- every name one row off from its value -- and that is
> the only shape this rule was minted from. **Figure 3.4 at
> `_scratchpad/sh7750_hardware.txt:9014-9029` is NOT uniform: it has a MISSING NAME CELL,
> so the stagger BEGINS PARTWAY DOWN.**
>
> ```
> 9017| H'F000 0000    Instruction cache address array     <- correct
> 9018| H'F100 0000      Instruction cache data array      <- correct
> 9019| H'F200 0000     Instruction TLB address array      <- correct
> 9020| H'F300 0000                                        <- THE GAP: address, NO name
> 9021| H'F400 0000  Instruction TLB data arrays 1 and 2   <- really F300 0000
> 9025| H'F800 0000    Unified TLB data arrays 1 and 2     <- really F700 0000
> ```
>
> **The first three rows pair CORRECTLY.** So a calibration point taken from above the gap
> reports the table as sound, and everything below it is wrong by one. A reader trusting the
> figure puts ITLB data at `F4000000` and UTLB data at `F8000000` -- and **`F8000000` is
> RESERVED**; the prose jumps `F7000000` straight to `FF000000`. *The figure would have
> condemned both shipped constants, and the calibration rule as written would have blessed
> the figure.*
>
> > **THE REFINEMENT: calibrate on a row BELOW the value you are about to cite, or on TWO
> > rows STRADDLING it. A single calibration point is only valid for a UNIFORM stagger, and
> > you cannot tell which kind you have from one point.**
>
> **And prefer the PROSE.** The unstaggered section paragraphs at `:9052-9065` and the
> per-array section heads gave the right answer at every one of the four windows this round
> needed. Extracted FIGURES are the hazard; extracted PROSE is not.
>
> *This is the exemplar problem again, one level down: the rule was right about the class and
> its single instance carried a property -- uniformity -- that the class does not have.*

**AND THE TOOL YOU CHECK WITH DECIDES WHETHER YOU CATCH IT.** `sed -n 'A,Bp'` prints the
lines WITHOUT their numbers, so the number has to be counted by hand off the top of the
range -- and on 2026-08-23 that produced a citation two lines off in a comment that had
just been written to FIX a citation error. **Use `grep -n` or
`awk 'NR>=A && NR<=B {print NR": "$0}'`**, which carry the number with the line. Three of
that round's four wrong citations were found by a seat re-deriving them with `grep -n`.

*** AND A PATTERN THAT MATCHED NOTHING REPORTS ZERO FOR EVERYTHING. Twice in one
session, 2026-08-24, in OPPOSITE directions -- and both looked like results. ***

* An **unanchored** `grep FAIL` over probe output matched the word FAILED inside a row's
  own DESCRIPTION, on a GREEN run -- **a phantom failure**. The tell was that the row
  printed `survived` against a wanted `survived`.
* An **`awk` range whose start pattern did not match** returned 0 for every query, and the
  0 was read as "the summary never mentions this" -- **a phantom absence**, which then had
  a whole narrative built on it before one grep at the right anchor refuted it.
* *** A FIFTH, 2026-08-26, AND IT GETS WORSE AS THIS FILE GETS MORE HONEST. *** A grep
  built to find STALE CLAIMS reported a defect that was really **an honest correction
  quoting the text it refutes** -- the exact form this project mandates. It cannot tell an
  ASSERTION from a QUOTATION OF ONE.
  **The working form: search BACKWARD from the hit for a correction signal** (`said the
  opposite`, `WAS FALSE`, `Corrected 20..`, `used to read`) before scoring it stale. With
  that discriminator, seven audit items resolved to six gone, one quoted-by-its-correction,
  **zero genuinely stale**; without it, one honest correction read as a live defect.
  *The trend matters more than the instance: every correction added here quotes what it
  refutes, so a naive stale-text grep gets steadily MORE wrong as the file improves.*

  > *** AND THE SAME COLLISION HAS A SECOND, WORSE FORM: A QUOTED MARKER RE-ARMS THE TOOL
  > THAT READS IT. Measured 2026-08-28, on a defect I created while fixing another. ***
  >
  > `gen_codex_wall.py` keys on the literal text `[HELD AWAITING SEAT: <seat>]`. A stale held
  > marker was cleared -- and the clearing note **preserved the question verbatim**, exactly as
  > the quote-what-you-refute rule requires. **The quote contained the marker, so the generator
  > still counted the stage as held**, and the "cleared" edit changed nothing. The count sat at
  > 27 through two regenerations and I read it as a stable number rather than a stuck one.
  >
  > **The grep case makes a READER wrong; this one makes a TOOL wrong**, silently and durably,
  > because the record now *says* the thing was answered while the machinery keeps reporting it
  > owed. That is the gap-closes-itself shape with the two halves disagreeing.
  >
  > > **QUOTING A MACHINE-READ MARKER REQUIRES DEFANGING IT.** Keep it human-legible and break
  > > the pattern -- `(HELD-AWAITING-SEAT fable5 -- defanged)`. The rule generalises past this
  > > one generator: **before quoting any string a tool matches on, ask what that tool will do
  > > with your copy of it.**
  >
  > *Bounded, and the hunt is recorded: all 263 rows were scanned for answered entries still
  > carrying a live marker. **Exactly one, the one made here.** The class is real and its
  > population today is zero.*
  >
  > > ### *** THAT LAST SENTENCE WAS MEASURED **FALSE** ON 2026-08-29: THE POPULATION WAS
  > > ### **TWENTY**, ACROSS SEVENTEEN ROWS, THE OLDEST NINE DAYS STALE. ***
  > >
  > > **The hunt was right about the class and wrong about its size, and the reason is the
  > > CRITERION.**  Looking for *answered entries still carrying a live marker* asks whether
  > > the entry HOLDING the marker was answered.  That finds one.  The question that finds
  > > twenty is different and is the one that matters to the tools:
  > >
  > > > *** SUPERSEDED THE DAY AFTER IT WAS WRITTEN, AND THE CARRIER KEPT THE OLD WORDING
  > > > FOR ONE MORE DAY AND SIX MORE MIS-CLEARS.  Corrected 2026-08-30. ***
  > > >
  > > > **THE RULE: does the marker name a seat that has answered in THE SAME STAGE, at a
  > > > STRICTLY LATER date?**  Mechanically: marker names seat S in phase P at date D, and S
  > > > has an entry on the same row IN PHASE P, dated STRICTLY AFTER D, of real length, that
  > > > is not itself a marker.
  > > >
  > > > **BOTH QUALIFIERS WERE PAID FOR IN BLOOD, AND NEITHER WAS IN THE ORIGINAL WORDING:**
  > > >
  > > > * *ANYWHERE ON THIS ROW* let a RESEARCH answer discharge a REGRESS hold.  `regress` is
  > > >   FABLE-ONLY by standing directive, so cross-phase credit is wrong there by
  > > >   construction.  **This was diagnosed and corrected on 2026-08-29 IN THE LEDGER** --
  > > >   `wdccdbmidxfer` entry [28] says in its own words *"My second sweep used same-stage
  > > >   matching and did not repeat it"* -- and THIS FILE was never updated, so the next
  > > >   round read the superseded wording here and repeated the documented failure at SIX
  > > >   TIMES the scale.
  > > > * *a LATER entry* was implemented as `>=`.  All six 2026-08-30 mis-clears were
  > > >   discharged by SAME-DATE siblings written by the very batch that created the marker
  > > >   to record the stage as NOT done.  A strictly-later test keeps all six.
  > > >
  > > > **AND THE FAILURE IS WORSE THAN INVISIBILITY.**  `check_stage_panels.py` keys on the
  > > > live literal, so a wrongly-defanged `seat=fable5, phase=regress` entry stops being a
  > > > marker and falls through into the SEAT TALLY as a regress ANSWER.  Defanging does not
  > > > merely hide an obligation; it MANUFACTURES a seat answer that never happened -- the
  > > > seat-failure-counted-as-agreement shape, inverted.
  > > >
  > > > *This is this file's own structure-first thesis, demonstrated against itself: the
  > > > correction lived in the LEDGER, where it was written by the person who found it, and
  > > > the auto-loaded carrier kept the superseded verdict.  The file already says "when a
  > > > rule is superseded, delete its conclusion" -- and then did not.*
  > >
  > > **MEASURED COST, and it is not cosmetic: `gen_codex_wall.py` reported 27 HELD STAGES
  > > and 15 of them were PHANTOM.**  Defanging the twenty took it to 12.  `check_stage_panels`
  > > was telling the operator `wdccdbmidxfer` awaited *fable5, opus5* when fable5 had answered
  > > that morning.  THREE tools read this literal -- `gen_codex_wall.py`,
  > > `check_fable_queue.py`, `check_stage_panels.py` -- so a stale marker misleads all three.
  > >
  > > *And I read the stuck 27 as a STABLE number across two regenerations before asking why
  > > it never moved.  A count that does not change is not thereby correct.*
  > >
  > > **Five markers were deliberately KEPT** -- `ieeeupgrade`, `pitclobber`, `proberowsubset`,
  > > `probetimebased`, and `wdccdbmidxfer`/opus5 -- because those seats genuinely have not
  > > answered.  The `wdccdbmidxfer` row is the discriminator working: its fable5 marker went
  > > and its opus5 marker stayed, on the same row, in the same pass.
  >
  > *Two of the three greps in this same repair also silently matched nothing --
  > `"gdromwarnbits ("` (the list renders the id in BACKTICKS) and an `entries`-vs-`stages`
  > field-name error that reported a volatile-path defect as absent when the adjudicating seat
  > had correctly found it. **Both were caught only because a seat's answer disagreed with my
  > check and I opened the artifact instead of keeping the check that agreed with me.***

* *** A SIXTH, 2026-08-26, AND IT IS THE FIRST WHERE TWO APPARATUS ERRORS STACKED INTO A
  CONVINCING FALSE RESULT. *** A 30-minute gate was launched as
  `timeout 1800 bash gate_sh_rounding.sh | grep -E ...`. Both halves were wrong and they
  covered for each other:
  * `timeout` killed the gate at exactly 30 minutes -- the last section finished at
    `18:01:38` and the run died at `18:02`, **before reaching the section under test**;
  * the **`| grep` made the reported exit status GREP's `0`**, not `timeout`'s `124`, so a
    KILLED gate presented as a CLEAN COMPLETION.
  The conclusion drawn was "my new gate section never ran, something is wrong with it." The
  section was innocent and untouched by the failure.
  > **NEVER PIPE A LONG-RUNNING GATE THROUGH A FILTER WHEN YOU NEED ITS EXIT STATUS**, and
  > size the timeout from a measured run rather than a guess. `gate_sh_rounding.sh:615`
  > already warns about the buffering half of this, one layer down: *"-u IS LOAD-BEARING ...
  > with stdout redirected to a file it is block buffered, and a killed run then loses every
  > row and looks like a run that produced nothing."*
  **And the diagnosis itself produced two more phantoms before landing**, both caught only by
  asking for a denominator: a `grep` for `gate_skip` that "found" `:618` -- an artifact of a
  broken `awk` in the same pipeline, not a match -- and a log listing rendered with
  `%H:%M:%S`, which **drops the date**, so logs from different days interleaved and read as
  one chronological run. A story about an upstream skip was nearly built on each.

> **CHECK THAT THE APPARATUS SELECTED SOMETHING BEFORE READING WHAT IT SAYS.** A range, a
> regex or a filter that selects the empty set produces a clean, confident, wrong answer --
> and unlike a crash it looks exactly like a measurement.

> ### *** THREE MORE, ALL ONE SHAPE: A FAILURE LAUNDERED INTO A CLEAN COMPLETION.
> ### 2026-08-28, two from a measuring seat and one of mine. ***
>
> * **A BUILD-AND-MEASURE SCRIPT MUST NOT END IN A COMPARISON.** A runner ended in `diff`,
>   which exits 1 on differences; under `set -e` that killed the script **before its two
>   probe runs**, and the wrapper still reported `rc=0`. No measurement happened and nothing
>   said so.
> * **A WINDOWS PATH PASSED TO `wsl -- bash` FAILS WHILE `wsl` ITSELF EXITS 0.** The error is
>   `No such file or directory`; the exit status is success. (This is why the invocation rule
>   is `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...` -- the `/mnt/c` form, every time.)
> * **PRESERVING A LOG FROM A STILL-RUNNING JOB CAPTURES A TRUNCATION, AND THE COPY LOOKS
>   COMPLETE.** I copied a seat's `table2_targeted.txt` at 1402 bytes; the finished file is
>   1529 ending `TARGETED_DONE`. The copy stopped at `SELECTED 1 of 8: S1 unkcmd` -- **so the
>   last mutant read as a session that started and produced nothing, which is indistinguishable
>   from a hang.** It was already staged for commit when the seat that wrote it noticed.
>
> > **THE RULE, and it costs one line: A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL,
> > NOT BY ITS EXISTENCE.** Every probe in this tree emits one (`TPROBE2_DONE`, `TARGETED_DONE`,
> > `FREEZE_DONE`, `REGRESS_PASS`). `tail -1` before citing, and re-copy if it is absent.
>
> *The volatile-path rule says copy the log before the record cites it. This is its missing
> half: copy it AFTER the job finishes, or the durable artifact preserves a lie. The first rule
> pushes you to copy EARLY and the second says not too early -- which is why the sentinel, not
> the timing, is the test.*

**The cheap defence is a DENOMINATOR.** Print how many lines the range selected, or how
many rows the grep considered, next to the answer. `0 of 0` and `0 of 41` are different
claims and only one of them is evidence. This is the same discipline as *a score claim
names its log*, one level down: the log makes the number checkable, the denominator makes
the SEARCH checkable.

**ITS LIMIT, MEASURED 2026-08-25: A DENOMINATOR VALIDATES THE ARTIFACT, NOT THE PATTERN'S
FITNESS FOR ITS FORMAT.** `grep -cE '^[+-][^+-]' nullfix.diff` returned **0** on a file
holding exactly one added line -- in `diff` NORMAL format (`610a611` then `> ...`), not
unified. The count was `0 of 2`, a nonzero denominator that looks like a real measurement
of a real file. So `0 of 41` is NOT always evidence, and the sentence above overstates it:
**the denominator catches selecting nothing FROM NOTHING, never selecting nothing from
SOMETHING IN AN UNEXPECTED SHAPE.**

> **WHEN A COUNT IS SURPRISING, OPEN THE ARTIFACT BEFORE BELIEVING THE COUNT.** "Zero
> changed lines in a diff that exists" is a contradiction, not a result — and a
> contradiction is the cheapest signal there is.

*** AND A FOURTH, WITH THE OPPOSITE SHAPE: A CORRECT READING NEARLY DISCARDED BECAUSE A
SECOND, BROKEN CHECK DISAGREED WITH IT. ***  `tasklist | grep` reported three panel CLI
processes alive. `tasklist /v | grep` -- the follow-up meant to identify them -- reported
none, because `/v` changes the column layout. **The three were real; the SECOND check was
the broken one**, and I had already written "false positive" before looking at what
matched.

> **When two checks disagree, find out WHICH ONE IS BROKEN. Do not keep the one that
> agrees with what you expected.** The first three incidents invented a failure or an
> absence; this one nearly destroyed a true positive, and the disagreement itself was the
> signal.

*Both incidents were mine, in tooling I wrote that day, while applying rules about careful
measurement. Neither was caught by a gate -- one by an impossible-looking row, one by a
follow-up grep that happened to use a different anchor.*

*** THE GENERAL RULE, after THREE incidents in one session (2026-08-23): ONE BACKSLASH LEVEL IS CONSUMED on the Bash -> heredoc -> Python path, IN BOTH DIRECTIONS. ***

Measured, same session, opposite failures:
* `'...\\\n'` intended as backslash+newline produced the two characters `\n` in a
  shell word list -- a bogus `for` word, and a RED GATE.
* `'...\\n"'` intended as the two characters `\n` inside a C string literal produced a
  REAL NEWLINE, splitting the literal and breaking the build.

So do not reason about the level count -- **use `chr(92)` for any backslash that must
survive into the file, and build the line by concatenation.** `BS = chr(92)` at the top
of the script costs nothing and is immune in both directions. The same applies to shell
regex arguments: `grep -n '\\n'` silently degrades to matching the letter `n` (it did,
twice, once producing a false "the ledger is ascii-escaped" reading) -- use `grep -nF`.

*** DO NOT BUILD A BACKSLASH-CONTINUED SHELL LINE THROUGH A NESTED HEREDOC. It mangled
TWICE in one session (2026-08-23), and the second one shipped a RED GATE. ***

Writing `'... "ipra rtc" ' + '\
' + '  "scif eri" ...'` from inside
`python - <<'PYEOF'` produced the two characters `
` in the file instead of a backslash
followed by a newline. In a `for v in ...` word list that adds a **bogus word `n`**, so the
gate ran `check "  n"` against a row that does not exist and reported
`FAIL n got=0 want=1` -- **1 of 111**.

**Two lessons, and the second one is the reassuring half:**
* **Write the word list on ONE line**, or edit line-by-line with `chr(92)` for the
  backslash. Never assemble a continuation inside nested quoting.
* **THE GATE CAUGHT IT, LOUDLY AND CORRECTLY.** A name list that gains a bogus entry fails
  rather than silently skipping a real row -- the opposite of the padded-column trap, where
  a too-long name makes a check UNSATISFIABLE and the row quietly stops being tested. Both
  failure modes are real; this one is the safe direction, and it is safe by design.

*** AND A COUNT CHECK CANNOT SEE THE LIST LANDING IN THE WRONG SECTION. Measured
2026-08-23, and MY OWN VERIFICATION PASSED ON IT. ***

A 32-name row list was written into `gate_sh_rounding.sh` with
`re.search(r'^    for v in ("live".*?); do$', ...)` — and **every section's list
starts with `"live" "devsig"`**, so it matched the FIRST one, which was the #459
pclock section. The gdrom names were written over the pclock names, the real gdrom
list was left at its old 27, and the pclock gate would have looked for 32 gdrom rows
in `$PCLOG`. **A red gate, and a destroyed list.**

**The cross-check I ran to confirm the edit reported `VERDICT: MATCH`** — because it
used the same first-match regex, so it compared the list I had just written against
the probe I had written it from. *A verification that shares the defect of the thing
it verifies always passes.*

**THE DISCRIMINATOR IS THE LOG VARIABLE ON THE NEXT LINE, and it is the only thing
that identifies which section a row list belongs to:**

```
    for v in "live" "devsig" ... ; do
        n=$(count "$GDDLOG" "^$v  .*ok$")     <-- THIS names the section
```

So: **anchor on `count "$XXLOG"`, never on the list's own first names**, and after
editing, diff EVERY list in the file against `git show HEAD:` — expect exactly one to
change. That check found it in seconds; the count check never could.

*Related but distinct from the padded-column and bogus-word traps below: those make a
row silently stop being tested. This one tests the right rows against the wrong log.*

**Cheap check before running a 15-minute gate:** paste the `for v in ...` list into
`bash -c '... echo "[$v]"; done' | nl` and count. It takes two seconds and it is the whole
test.

*** AND THE SAME RULE GOVERNS COUNTS, NOT ONLY SCORES. Adjudicated 2026-08-26 after an
audit of this whole file found the transcribed count to be its single largest decayed class. ***

> **A COUNT WRITTEN INTO A DURABLE RECORD NAMES ITS DERIVER** -- the command, script, manifest
> or log that produces it -- **or carries its method and date inline. And a count being
> CORRECTED may never land as a fresh bare literal: it lands as deriver-plus-demoted-prose.**
>
> **STOP CONDITION, in the same sentence because that is what keeps it from becoming `#392`:**
> it fires only on NEW and CORRECTED counts, at writing time; it audits NOTHING retroactively;
> it builds NO checker; and the ~70 legacy counts stay governed by the existing read-side rule
> -- re-derive an exemplar before leaning on it, and FILE anything found decayed rather than
> sweeping it.

**THE HONEST SEVERITY, because the ruling turned on it: NO STALE COUNT HAS EVER CHANGED A
DECISION.** The adjudicator hunted for one and came back negative, checking every candidate
where a count sat near a decision -- `exitsweep`'s census (re-derived by a seven-seat panel
BEFORE the round acted, and its bound deliberately written *"as a condition rather than a
number"*), gate 9's 23-vs-41 (the gate already refuses the class in its own words), and the
house-idiom's wrong marker spelling (all three sites predate the clause that misnamed them).
**Transcribed counts have cost audit expense and reader distrust; they have cost zero
decisions.** That is written down so nobody re-argues this class as though it were urgent.

*And the near-misses are NOT in this class, which is the sharpest thing the hunt produced:* the
one measured case of a stale number changing a decision was an **absence claim** -- a five-seat
panel voting to drop a row on a sentence derived at 7 differentials and quoted at 13, resolved
by a targeted CHECK (`check_optpin.py`, whose header states the maxim: *"An audit is a claim
with a shelf life; a check is not"*). The other decision-costing stale facts on record are
EXPIRED MEASUREMENTS AND ROSTERS -- the ~20-minute Ollama spacing that rationed panels for a
week, the kimi substitute left unfired, "no SH manual" load-bearing for four rounds.

**WHY NO CHECKER, and it is a measurement rather than a preference.** This file carries **33**
digit+noun counts and **67 WORD-number forms** (`ONE LESSON`, `TWO INSTANCES`, `nine seats`) --
**the blind spot is twice the visible population**, and the word forms are overwhelmingly
rhetorical structure rather than facts. A checker policing the minority of a class while
alarming on prose is the switched-off-check shape this file already names, and section U's own
header states the principle: *guessing would produce false positives, which is how a check gets
ignored.*

> **PRE-SPECIFIED ESCALATION, so nobody re-argues it later: the FIRST measured decision that
> consumed a stale count converts this writing rule into the `check_cited_artifacts.py` idiom**
> -- existence-only, forward-only from a cutoff, carrier files only. **Until that trigger
> fires, no machinery.**

*The rule is prose and that is deliberate, against this file's own structure-first default: the
adjudicator rejected both mechanical options on measurements, and a prose rule with a named
stop condition and a pre-specified escalation trigger is what the evidence supports. Recorded
here rather than as a checker because the evidence says a checker would be switched off.*

*** A SCORE CLAIM MUST NAME THE LOG THAT PRODUCED IT. Adopted 2026-08-23 after the
FOURTH generation of the frozen-number defect appeared in one round -- inside the
sentence memorialising the third. ***

`#461` wrote `8/32 pre-fix ... both MEASURED at 32 rows` into a heading and a gate
comment. The heading was written at 17:33; **the 32-row run started at 17:50.** The
only pre-fix number on record was 8/31, and the 8 had been carried forward when the
row count grew. A seat caught it by comparing mtimes.

**Section U cannot catch this class and never will.** It checks DENOMINATORS against
the gate pin, mechanically and well. The defect here is the NUMERATOR and the word
*measured* -- and no comparison against a pin can tell a measured 8 from a carried 8.

> **THE RULE: a score claim names its artifact — `8/32 pre-fix (kill461e.out)`.**
>
> ### *** AND THE ARTIFACT MUST BE IMMUTABLE, OR THE CITATION DECAYS SILENTLY.
> ### Measured on my own harness, 2026-08-24. ***
>
> A driver that writes `probe_<mutant>.raw` and truncates its results file **reuses those
> names on every run**. So a record citing them is true only until the next run — and
> then it is worse than uncited, because the named log now says something ELSE.
>
> Concretely: `#462`'s round block cited `probe_base.raw` for **52/52**. A second table
> at 57 rows overwrote that file, and the citation now points at a 57-row log. **The
> claim did not become unverifiable; it became CONTRADICTED BY ITS OWN EVIDENCE** —
> exactly the shape that made the mislabelled "PRE-FIX" caption detectable, arrived at
> from the opposite direction.
>
> **Two rules, and the second is the one that costs nothing:**
> * **A measurement cited in a durable record must live at a durable path.** Stamp the
>   run (`table_<n>/`, or a timestamp) or copy the log beside the record. A pointer into
>   a buffer that gets reused is not a citation.
> * **Before any re-run that reuses log names, PRESERVE the prior run's logs first.**
>   Ten of twelve were saved here only because the question was asked while the re-run
>   was still early; `probe_base.raw` and `probe_Mb1.raw` were already gone.
>
> *The scores themselves survived — because they had been written into the records at the
> time. **The transcription outlived the evidence**, which is precisely the situation the
> names-its-log rule exists to prevent, reached by a route the rule did not cover.*
> That makes the claim checkable BY EXISTENCE, which is the same witness discipline
> the ledger already imposes on rows, and it is the only mechanical guard available
> for a number that was never run.

It is the oracle-correction rule's own order discriminator applied to prose: **a
number written before the run that produces it cannot be told from a number fitted
to the answer**, whatever it later turns out to be. Recording it as OWED costs
nothing; asserting it costs the round's credibility on every other number it states.

*** AND A CORRECTION IS NOT SAFER THAN THE THING IT CORRECTS. ***  In the same round
a recount of "26 of 31 rows carry a measured kill" was itself wrong twice: the seat's
recount gave 25 and six, and the draft correcting it listed `dma accept` among the
unkilled rows *while also saying it had been discharged*. A correction carries more
authority than the error, so it earns a second reading, not less of one -- which is
what the existing "budget a second review pass for any records-correction round"
note already says, now with a third instance.

> ### *** THE CITATION-FORM RULE -- STANDING as of 2026-08-26, after the same remedy was
> ### adopted FOUR SEPARATE TIMES round-locally and never carried, while the class bit EIGHT
> ### times. Adjudicated, and the mechanical check it was competing with was REJECTED ON
> ### MEASUREMENT. ***
>
> > **Line numbers only ACROSS files, with the qualifier ON the citation. SAME-FILE references
> > POSITIONAL or by CONSTRUCT NAME. Durable cross-file references as VERIFIED-UNIQUE GREP
> > ANCHORS.**
>
> **It removes the measured population: 7 of the 8 recorded instances were same-file or bare
> forms the rule eliminates outright.** And it is structure in the sense this file means --
> it lives where citations are WRITTEN and it fails at the point of USE, because a grep anchor
> that matches nothing is loud, while a wrong number is silent.
>
> *** THE CHECKER WAS REJECTED, AND ITS NUMBERS ARE THE REASON THIS RULE IS PROSE. *** The
> proposal was: warn when an added `file.ext:NNN` names a file the same diff also edits.
> Measured over 429 commits -- **it fires on 57 commits / 263 citations (~11 a week) and its
> recall on the eight recorded instances is ZERO**, because every recorded instance is a BARE
> `:NNN` that section D's `[a-z0-9_]+\.(c|h):[0-9]+` cannot see. On the motivating round
> it emits 15 warns, none of them the stale one. **A checker policing the visible minority of
> a class while blind to its dominant form is the check-that-cannot-fail shape** -- which is
> what the proposal had accused section D of being.
>
> **AND THE CLASS IS WEAKER THAN THE COUNTS CLASS THAT WAS ALREADY DECLINED, for a structural
> reason worth knowing: NO GATE, PROBE OR SCRIPT IN THIS TREE READS A LINE CITATION
> FUNCTIONALLY.** Gates key on grep anchors and content. A citation is consumed only by a
> READER -- and a reader using one opens the file, so **a drifted number self-refutes at the
> point of use.** A carried count does not. That is why all eight instances were caught by a
> seat or a re-read, and why the hunt for a consumed decision came back empty across 135
> "stale" mentions in the CHANGELOG.
>
> **PRE-SPECIFIED ESCALATION:** the first MEASURED decision consumed by a stale line citation
> -- a fix mis-aimed by one, a gate passing falsely, a seat verifying green against wrong
> content -- converts this into an anchor-verification check bounded to ADDED citations,
> forward-only from a cutoff. **Until that trigger fires, no machinery.**

**A LINE NUMBER IN A COMMENT IS INVALIDATED BY YOUR OWN EDITS TO THAT FILE.** The same
round cited `dev_sh4.c:2379-2381` correctly, then inserted a seven-line comment ABOVE it
in a later step, moving the target to `:2386-2388` and making its own fresh citation
wrong. **Re-grep every same-file citation AFTER the last edit to that file**, not when
first written.

This is the `#458` case of the same class as the hand-assembled-encoding trap: **a wrong
constant is invisible when the probe reads the same constant**, so the check has to come
from outside the code entirely.

A filed item (`sh4aaalias`) was withdrawn on that reading. **Obtaining the manual cost one
download and refuted a wrong finding in the same session it was raised.**

**The ARM manual was ABSENT until 2026-08-11.** Rounds #357/#362/#365 cite DDI 0100I page
numbers that came from **panel LLM output, not a local manual** — the load-bearing ones were
later checked against a genuine copy and held, but that is luck plus good seats, not process.
Cite only what you have read in these files. Two things a real reading corrected: **A2.8.3
does not exist** (A2.8 has only A2.8.1 and A2.8.2), and the endian-specific rotation statement
is not in A2.8 at all — it is in **LDR's own Alignment note, p. A4-44**.

## Build/measure quick facts

- Build inside `wsl -d Gentoo` (default Ubuntu lacks make); `rm src/cpus/*.o` first.
  *** THE STATED REASON FOR THAT `rm` WAS FALSE, and it has been repeated in every
  round and every seat brief. Measured 2026-08-26. *** This said the `#include`d `.c`
  files are "invisible to the dep rules". **They are not.** `src/cpus/Makefile:214`
  -- the GENERATED makefile make actually reads -- contains
  `cpu_sh.o: cpu_sh.c cpu_sh_instr.c cpu_dyntrans.c memory_rw.c tmp_sh_head.c
  tmp_sh_tail.c`, and `Makefile.skel:194` is where it comes from. Make tracks them.

  **The `rm` survives as a CONSERVATIVE CLEAN-BUILD precaution, not as a necessity**,
  and nobody has measured whether it is needed at all. **That is worth measuring,
  because it is not free:** a mutant table rebuilds per mutant (one round built NINE
  binaries), and if incremental builds are sound there, mutant-table time -- the
  dominant cost of a round -- drops substantially. Filed as `depsrm`.

  Until it is measured, KEEP the `rm`: an unnecessary rebuild costs minutes, while a
  stale object costs a wrong measurement, and this project has already paid that once.
- est/ and GXEMUL-SEC differ by the paths declared in `tools/est_divergence.txt` -- *** COUNT DELIBERATELY NOT RESTATED HERE, and the reason is that this line has now been wrong TWICE. ***  It said **SEVEN**; the file holds **six** non-comment entries (`grep -vcE '^\s*(#|$)'`).  The paragraph diagnoses the failure, prescribes the right remedy -- *derive the allowlist rather than quoting a count* -- and then commits the failure in its own headline number.  **Run the deriver.**  *(For the record, this line was ALREADY a correction of an even earlier one, which said not "5 named files +
  `dev_ne2000.c`" -- the omitted one is `src/devices/.index`. The list is
  `tools/est_divergence.txt` and `precommit_check.sh` reads it, so **derive the
  allowlist rather than quoting a count**.  So the instruction has been right all along and the number beside it has been wrong twice.)*
  Any other shared file must land byte-identical in both. Commit only GXEMUL-SEC files.
- Debugger `dump` reads device state through `memory_rw`, so **read SH4 device state with
  guest loads via `step`** -- but the REASON given here was a blanket claim and it is false.
  *** CORRECTED 2026-08-26. *** `debugger_cmds.c:716` calls `memory_rw`, and
  `memory_rw.c:585` DOES dispatch to handlers registered
  `DM_READS_HAVE_NO_SIDE_EFFECTS`. What makes the advice true for SH4 is narrower and
  better: **SH4 registers `DM_DEFAULT`** (`dev_sh4.c:2860`, `:2867`), so ITS handler is
  bypassed. A device registered the other way WOULD be reached by `dump`. (There is also no
  `examine` command in the tree today.)
- *** A SINGLE-STEPPING PROBE CANNOT OBSERVE INTERRUPT DELIVERY, EVER. *** `cpu_dyntrans.c:204-206`
  reads `/* Do not cause interrupts while single-stepping. It is so horribly annoying. */`
  followed by `if (!single_step) {`. **Every SH probe in this tree single-stepped** when this was written, so none of
  them could see an interrupt arrive -- *and that is no longer universally true, because the
  tree then ADDED the free-running shape this very paragraph describes:*
  `sh_intprio_probe.py` and `sh_iprbcd_probe.py` both breakpoint-and-`continue` today.
  **The suppression rule below is unchanged and still governs any probe that DOES step**;
  what expired is the claim that they all do — a step-based oracle reads "not delivered" on a correct
  build and on a mutant alike, which is the vacuous shape in its purest form. This is why
  `sh4dmacie` was mis-ranked for weeks as needing "a new capability": the EXPEVT/INTEVT
  registers were readable by an ordinary guest load all along (`0xff000024`/`0xff000028`, served
  by `dev_sh4.c`); what was missing was a probe SHAPE, not emulator support.
  **The shape that works, measured:** free-running with `sr=0x40000000`, `vbr` pointed into
  RAM, a `bra .` self-loop after the triggering store, a breakpoint at `VBR+0x600`, then
  `continue`. Interrupt levels are hardcoded (IRQ10 is level 5 at `cpu_sh.c:255-258`), so
  IMASK must be low enough to admit the one under test.
  *** BUT "DELIVERY" IS THE EXACT WORD, AND READING THIS RULE MORE BROADLY COSTS A PROBE.
  Refined 2026-08-22, verified by opening all three files. *** The guard suppresses the
  EXCEPTION DISPATCH only. **The ASSERT path runs perfectly well while stepping**, by two
  routes: a device handler asserts SYNCHRONOUSLY inside the guest's own store instruction.
  *** THE PARENTHESIS HERE SAID "nothing in `memory_rw` or device dispatch consults
  `single_step`", AND HALF OF IT IS FALSE. Corrected 2026-08-26. *** `memory_rw.c:284`
  reads `!single_step && !about_to_enter_single_step &&` -- for WATCHPOINTS. **The
  conclusion survives on the half that is true:** DEVICE DISPATCH carries no single-step
  guard, which is what makes a synchronous assert visible while stepping. The watchpoint
  path is a different mechanism and does not gate device access, and **tick functions
  run under stepping too** — `machine.c:726-728` is
  `ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT;`, so they still fire, just
  one tick at a time.
  *** AND THAT IS STILL NOT THE WHOLE RULE — corrected AGAIN the same day, by a panel seat,
  after the paragraph above had already been written into the carrier and a witness designed
  on it. VERIFY BEFORE REUSING EITHER HALF. *** A tick function RUNS under stepping but does
  no work if what it consumes is produced by a HOST TIMER: `debugger.c:800` calls
  `timer_stop()` "while interacting with the user", and the step command returns at
  `:835-836` **before** `timer_start()` at `:840`, so `timer_add`/SIGALRM callbacks are
  stopped for the entire `step N`. `sh4_timer_tick()` therefore never runs, `DEVICE_TICK`
  finds `timer_interrupts_pending == 0`, and nothing asserts.
  > **THE RULE, BY ITS DISCRIMINATOR:** a step-based probe sees an assert that is
  > **SYNCHRONOUS** — a device handler reached inside the guest's own load or store. It does
  > NOT see one that depends on a host-timer callback, however much the tick loop appears to
  > run. Ask *"what produces the thing the tick consumes?"* — if the answer is `timer_add`,
  > the probe must free-run.
  The case that forced the first correction was `cpu_sh.c:312-316`, whose `exit(1)` sits in
  the assert path; the case that forced the second was the WITNESS for that same defect,
  where the TMU route is a host-timer route and only the `testsh` IPI route is synchronous.
  **Three passes over one sentence, each narrower than the last — the general lesson is that
  "runs under stepping" and "does its work under stepping" are different claims, and this
  file conflated them twice.** Instruction-combination work needs FREE-RUNNING execution: the
  #340 two-pass loop driver, breakpoint AFTER the sequence, instruction tracing OFF
  (recipe in OUTSTANDING_BUGS.md, 2026-08-03 entry).
- Probe harness: `_scratchpad/gxprobe.py` (don't hand-roll pty plumbing). Reconstruct the
  arc screen (`r49_screen.py` pattern) for BOOT-PROOF tokens.
  *** "NEVER grep the raw arc pty log" IS TOO STRONG, and the two sources are
  COMPLEMENTARY rather than one-right-one-wrong. Corrected 2026-08-26. ***
  **Gate 4 obeys the rule and always did** -- `gate_mips.sh:62` rebuilds via
  `r49_screen.py` and `:64`/`:66` grep the REBUILD, because arc's VGA console
  repaints DIFFERENTIALLY and a raw grep misses tokens.
  **Gate 6 deliberately accepts EITHER** (`gate_hygiene.sh:402`), and its own comment
  at `:11` records the measured reason: `'{ asc: data in'` reads **0 from the screen
  rebuild and 5 from the raw log**. *The rebuild is required to avoid
  differential-repaint FALSE NEGATIVES; the raw log is required for content the
  rebuild DROPS.* Choose by what you are looking for, not by a blanket ban.
  *(An auditing seat reported that gate 4 greps the raw log. It does not -- it greps
  `arc.screen`. The seat was right that "never" is false and wrong about which gate,
  which is why this was re-derived rather than transcribed.)*
*** AND THE OPPOSITE FAILURE ALSO EXISTS: A PLAIN `&` IN A BASH CALL DOES *NOT*
SURVIVE, AND IT FAILS SILENTLY WITH A ZERO-BYTE LOG. Measured 2026-08-23. ***

Two measurements were launched as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash ... &`
inside a Bash tool call. Both produced **zero-byte output files**: the `wsl.exe`
child is killed when that invocation's shell exits, so the run never happened.

**It looks exactly like a run still in progress.** `ps aux` shows nothing, the log
is empty, and the natural reading is "not finished yet" — which is how ~25 minutes
went by twice before the zero byte count was noticed.

*** THE TELL IS THE PROCESS, NOT THE SIZE -- and this clause said the opposite until
2026-08-26. *** It read *"a live run's log grows, and a dead one is exactly 0"*.
**The ledger holds the counter-example in its own records:** `agy` writes NOTHING until
it finishes -- its file sat at **EXACTLY 0 bytes for minutes with a live `agy.exe`
(pid 23548)**, then landed 8,044 bytes in one shot. So for agy, a zero-byte file is the
NORMAL mid-run state, and the size rule would have declared a healthy seat dead.

> **Zero bytes alone proves neither live nor dead. Check the PROCESS** (`ps aux` for the
> child, or `tasklist` for a Windows CLI seat) **and the completion sentinel.** Size is
> evidence only where the tool is known to stream -- `grok` does, agy does not, and the
> two demand opposite readings of the same observation.

*The original rule was minted from a real incident and its ADVICE survives: a plain `&`
inside a Bash call dies silently. What failed is the DISCRIMINATOR it offered, which is
the exemplar problem again -- the incident's own shape taken for the class.*

**Use `run_in_background: true`** (the harness tracks it and notifies on exit).

> ### *** THE PROCESS CHECK THIS FILE PRESCRIBES IS **ARGUMENT-BLIND ON THIS MACHINE**, SO IT
> ### RETURNS "DEAD" FOR EVERY SCRIPT, ALWAYS.  Measured 2026-08-31 -- and I believed it, wrote
> ### a false correction into this file on the strength of it, and had to take the rule back. ***
>
> git-bash `ps -ef` prints the **executable path and no arguments**:
>
>     User00    7854       1 ?  03:32:47 /c/Users/.../Python312/python
>
> So `ps -ef | grep -c 'panel_ollama'` returns **0** and `grep -c 'python'` returns **2**, on the
> same processes, in the same second.  **Any pattern naming a SCRIPT -- `panel_ollama`,
> `gate_arm.sh`, `make -j4` -- can never match, so the check answers "not running" whether or
> not anything is running.**  That is this file's own check-that-cannot-fail shape, sitting
> inside the remedy it recommends for the previous one: the bracket trick
> (`ps -eo pid,args | grep -E "[m]ake"`) presumes an `args` column that MSYS `ps` does not have.
>
> **WHAT IT COST, because the damage was not the wasted check.**  Three cloud seats were
> launched `nohup ... &`; the blind check said 0 alive; I concluded nohup had failed, relaunched
> all three, and **ran two writers against the same three output files** -- `ollama_deepseek.txt`
> was measurably truncated and rewritten, 3475 -> 2928 bytes, between two reads.  Then I wrote a
> rule into this file saying *nohup is not a reliable fallback*.  **It is; the check was blind.**
>
> **THE DISCRIMINATOR THAT SETTLED IT, and it is available in the same command:** a python with
> **PPID 1** and a start time matching the FIRST launch is an orphaned `nohup` survivor -- which
> is exactly what `ps -ef` showed once I read the PPID column instead of grepping for a name.
>
> **SO, ON THIS MACHINE:**
>
>     ps -ef | grep <script-name>    -> ALWAYS 0.  Never use it.  It cannot fail.
>     ps -ef, read PPID + START      -> works; PPID 1 means orphaned/nohup'd
>     tasklist | grep -i '^python'   -> works (Windows-native; image name, still not args)
>     the redirect target's SIZE     -> works, and is the cheapest of the three
>
> **And the standing advice is unchanged and is what avoids all of this: long jobs go to
> `run_in_background`, which the harness tracks and which notifies on exit** -- no process check
> needed, and no chance of a second launch racing the first.
>
> *Recorded in this shape because the near-miss is the instructive part: I ran a check, got a
> confident answer, acted on it, and the action created a real defect (duplicate writers) that
> nothing would have reported.  The file changing size between two of my own `ls` calls is what
> gave it away -- a contradiction, which this file already names as the cheapest signal there is.*

*Note this is the MIRROR of the hazard below, and the two want opposite reflexes: a
TIMED-OUT foreground run keeps going invisibly, while a plain-`&` run dies
invisibly. Check `ps aux` for the first; check the log's byte count for the second.*

> ### *** AND ON 2026-08-27 THE RULE'S OWN TELL FAILED, WHILE THE FALLBACK CHECK LIED IN THE
> ### OTHER DIRECTION. TWO APPARATUS ERRORS, STACKED, PRODUCING A CONFIDENT WRONG READING
> ### THAT PERSISTED ACROSS THREE SEPARATE CHECKS. ***
>
> An ASAN rebuild was launched as `wsl -d Gentoo -- bash -c '... nohup make -j4 > /tmp/x.log
> 2>&1 & echo started'`.  It printed `started`.  **It never ran at all.**
>
> * **The size tell did not apply: THERE WAS NO LOG FILE.**  The rule above says a dead run
>   leaves a log of exactly 0 bytes.  That presumes the redirect happened.  Here the child was
>   torn down with the invocation's shell before the redirect took effect, so `/tmp/x.log`
>   **did not exist** -- and `tail` on a missing file prints nothing, which reads exactly like
>   a build that has produced no output yet.
>
> * **`pgrep -f "make -j4"` MATCHED ITS OWN WRAPPER.**  The pattern appeared in the
>   `bash -c` command line running the check, so it found itself and reported RUNNING.  Three
>   consecutive polls said RUNNING with zero make processes alive.  `ps -eo pid,args | grep`
>   showed the truth immediately: the only match was the checking shell.
>
> **Neither error is new as a class** -- the carrier already records the check-that-cannot-fail
> and the pattern-that-matches-nothing.  What is new is that the FIRST rule's remedy was
> defeated by the SECOND rule's failure mode, so every reading agreed with every other reading
> and nothing looked wrong.
>
> > **THE CHEAP DISCRIMINATOR IS THE REDIRECT TARGET, NOT THE PROCESS AND NOT ITS SIZE.**  A
> > shell creates the redirect file *before* it execs the command, so:
> >
> >     log MISSING   -> the command NEVER STARTED
> >     log 0 bytes   -> started; either mid-run on a non-streaming tool, or dead
> >     log growing   -> alive and streaming
> >
> > `ls -la <log>` separates "never started" from "started", which is the distinction both
> > older rules assume you have already made and neither one gives you.
>
> **And when a process check is genuinely needed, it must not be able to match itself:** use
> `ps -eo pid,args | grep -E "[m]ake"` (the bracket trick), or grep for something only the
> real process has -- never a literal that also appears in the command you are typing.
>
> *The operational rule is unchanged and is the one that was ignored here: long jobs go to
> `run_in_background`, which the harness tracks and which notifies on exit.  Both of these
> checks exist only because a plain `&` was used in the first place.*

*** A BASH-TOOL TIMEOUT DOES NOT KILL THE WSL-SIDE PROCESS, AND THE ORPHAN KEEPS
WRITING THE TREE. Measured 2026-08-23, and it produced TWO CONCURRENT RUNS IN ONE
MUTANT TREE. ***

A kill-table script was launched in the foreground with `timeout 2400000`. **The Bash
tool caps at 600000 ms**, so the wrapper died at ten minutes reporting exit 143 -- and
the WSL-side script carried on building mutants. Re-launching it in the background then
gave two scripts checking out different mutants into the SAME `/tmp/gx461`, each
measuring a binary the other was overwriting. `ps aux` showed both, four minutes apart,
and **neither measurement was worth anything**.

It defeats the usual signal: the tool REPORTS a failure, so it does not look like a
silent success -- but the failure it reports is *its own wrapper*, and nothing says the
work is still running. **After any timed-out or interrupted WSL invocation, `ps aux`
for the probe/emulator before starting anything else.** Never re-launch on the
assumption that a timeout stopped the work.

**Two consequences, both applied:**
* Long measurements go to `run_in_background` from the start. 600000 ms is the ceiling,
  and a six-probe kill table exceeds it by design, not by accident.
* **THE SENTINEL RULE IS NOT OPTIONAL AND THIS SESSION'S OWN SCRIPT BROKE IT.**
  `kill461b.sh` mutated `/tmp/gx461` with no `.MUTANT` file, so when it was killed
  mid-mutant the tree was left mutated with nothing saying so. The dirt was found only
  because a `cmp` against SEC was run by hand. A script that mutates a tree drops the
  sentinel FIRST and clears it only after `cmp` against GXEMUL-SEC succeeds -- which is
  what the carrier already said, and what the script did not do.

*** EDITING A RUNNING SHELL SCRIPT CORRUPTS IT MID-EXECUTION. Documented for `panel.sh`
at midday 2026-08-25, then committed by me against `killwdc.sh` the same evening. ***

**Bash reads a script INCREMENTALLY, by byte offset.** Inserting lines into a file a shell is
currently executing shifts every offset after the insertion point, and the shell resumes mid-
token. The failure looks like a syntax error in a file that is perfectly valid:

    killwdc.sh: line 90: syntax error near unexpected token `('
    ...and `bash -n killwdc.sh` afterwards reports NO ERROR AT ALL.

That disagreement is the diagnostic. **A script that fails to parse while running and parses
clean afterwards was edited underneath itself** -- nothing else produces that signature.

The cost here was an eight-mutant table killed on its first mutant, plus a tree left holding
a sentinel. Cheap this time only because the sentinel discipline worked: the tree said what
state it was in, and one restore-and-`cmp`-against-SEC settled it.

> **LAUNCH LONG JOBS FROM A FROZEN COPY.** `cp script.sh script.run-<stamp>.sh` and run the
> copy. Then the original is free to edit while the job runs, which is exactly when the urge
> to edit it arrives -- because that is when you are watching it and thinking about it.

> ### *** AND THE SAME HAZARD HAS A PYTHON FORM THAT THE BASH RULE DOES NOT COVER: A
> ### MULTI-RUN SCRIPT RE-READS ITS PROBE BETWEEN RUNS. Noticed 2026-08-28, before it bit. ***
>
> Bash reads a script INCREMENTALLY, so editing it mid-execution corrupts THAT run -- which is
> the rule above. **Python is the opposite and it is not safer: the interpreter reads the whole
> file at startup, so the RUNNING invocation is immune -- and the NEXT invocation loads
> whatever the file says then.**
>
> So a comparison driver shaped like
>
>     for tree in base mutant; do python3 -u probe.py $tree/gxemul "$IMG"; done
>
> **gives run 1 and run 2 DIFFERENT INSTRUMENTS if the probe is edited between them**, and the
> difference lands in the very output being diffed. An edit to a row's NOTE text is enough:
> the note is printed in the row line, so a records-only correction shows up as an apparent
> behavioural difference between base and mutant.
>
> > **A COMPARISON RUN OWES ONE INSTRUMENT. Freeze the probe (`cp`) for the duration, or make
> > every edit BEFORE the driver starts and say so.** The bash rule protects the run in flight;
> > this protects the COMPARISON, which is the thing the measurement actually rests on.
>
> *Recorded because it did not bite, not because it did: the edits happened to precede the
> launch. The near-miss is the useful part -- the failure would have presented as a real
> difference between two trees, which is exactly what the run exists to detect, and nothing
> in the output would have said the instrument changed.*

*I knew this rule, had written it down hours earlier for a different script, correctly held
off editing `wdc_flood_probe.py` for the same reason -- and then edited the driver. The
probe was protected because the hazard was FRONT OF MIND FOR THE PROBE. Knowing a rule and
having it fire on the right object are different things, which is the argument for making it
STRUCTURAL (a frozen copy) rather than remembered.*

*** AND `pkill -f <script>` KILLS THE SHELL RUNNING IT. ***  The cleanup command was
itself a WSL bash invocation whose command line matched the pattern, so it terminated
itself and reported exit 15 before printing its verification. Pattern-kill and then
verify in a SEPARATE invocation; a cleanup that cannot report its own result is a
cleanup you have to redo.

- Invoke WSL scripts as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...`; write
  scripts to the session scratchpad, not git-bash `/tmp`.
