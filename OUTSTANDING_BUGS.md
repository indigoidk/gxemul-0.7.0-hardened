# GXemul est/ — Outstanding bug candidates (not yet fixed)

> ## 2026-08-01 — OPEN LIST, at a glance
> **[#385 status, 2026-08-12]** This head is a snapshot dated 2026-08-01 that has drifted
> from the charter in the next paragraph: most entries below now carry ✅/strikethrough
> resolution marks (the charter says resolved items are REMOVED), and residuals found from
> 2026-08-02 onward lived only in the dated tail, invisible from here. What is true today:
> **the live queue is the harness TaskList, plus the "post-2026-08-01 open residuals" block
> just below, plus the un-ticked entries in this head.** Ticked/struck entries are kept in
> place — mass removal was judged too deletion-risky for a records round (an over-deleted
> open item is forgotten work; a kept-but-ticked one is only clutter) — and their full
> stories live in the dated tail and the CHANGELOG round blocks.
>
> **Only genuinely OPEN items live here.** Resolved ones are removed, not annotated: an
> index that accumulates its own history stops being an index, and a section headed
> "everything genuinely open" that is mostly ticks is the dishonest-listing class #270
> exists to prevent. The dated blocks below and the CHANGELOG carry what was fixed and
> why. Rounds 60–65 (#295–#300) cleared the entire floating-point feasibility queue;
> what follows is what they left, plus what they found on the way.
>
> ### OPEN — surfaced 2026-08-25 by fixing `check_bugfile_sync.py`, which had been blind to them
>
> **These thirteen rows were OPEN in the ledger and invisible here, and the check that exists
> to prevent exactly that was reporting PASS.** Two independent defects in it: its
> `OPEN_STATES` tuple omitted `open` — 49 rows, the second-largest state, and two of the four
> states it *did* list do not occur in the data at all — and `newest_date()` returned `""` for a
> row with no entries, which sorts *before* every date, so freshly filed rows were classified
> ARCHIVED and forgiven. A row with no entries is the newest kind of row, not the oldest.
>
> *The `open` omission is the same one the ledger's own `state_semantics` block made, found
> independently the same day in a different tool. When one enumeration is found short, grep the
> others — the omission is a habit, not an accident.*
>
> - *** THIS ROW READ ✅ FIXED IN #473 UNTIL 2026-08-27, DIRECTLY ABOVE AN ENTRY
>   SAYING THE AMBIGUITY IS STILL PRESENT.  TWO CONSECUTIVE LINES ASSERTING OPPOSITE
>   STATES. ***
>
>   **STATE: OPEN.**  `#473` fixed the ATAPI DATA-IN CHUNKING -- it moved an existing 32768
>   clamp before the push loop.  **It did not touch the ambiguity**, and the entry below says
>   so in its own words: *`head == tail` for BOTH empty and full with no disambiguator*.
>   Re-verified 2026-08-27 by reading `wdc_addtoinbuf()` and by MEASURING it -- a four-leg
>   reproduction on this exact HEAD reports a full ring as occupancy 0 with DRQ CLEAR
>   (`regress/artifacts/wdcringambig/repro_20260827/PREFIX_committed_ce75b1d.out`).
>
>   **THE CAUSE IS THE HAZARD THIS PROJECT HAS ALREADY NAMED: ONE QUEUE ID COVERING TWO
>   DEFECTS, CLOSED ON ONE.**  The chunking overrun and the ring's full/empty ambiguity were
>   filed under a single id; `#473` closed the id on the first.  The second was refiled as
>   `wdcaddtoinbufbound`, so it was not LOST -- but the ✅ on the original was false,
>   and a reader who trusts states read a live guest-reachable defect as done.
>
>   *The tick is the part that misleads.  A future reader scanning for open work skips a
>   ticked row without reading the body that contradicts it -- which is why the correction
>   goes HERE, in the state line, and not as a note further down.*
>   **`wdcringambig`** — *** ESCALATED 2026-08-26: GUEST-REACHABLE, NOT LATENT, AND ONE LEGAL
>   COMMAND DOES IT. *** The wdc inbuf ring uses `head == tail` for BOTH empty and full with
>   no disambiguator; the overrun check is post-hoc, so **the store that actually corrupts is
>   the NEXT one and is SILENT**; and the two BULK paths never compare the pointers at all,
>   only against the array end. Four seats located it independently on the `wdcflood` pass-1
>   panel.
>   **THE ESCALATION, found by a farmed codex job and re-verified by reading:** `dev_wdc.c`
>   sets `atapi_len = data_in_len` and then loops `wdc_addtoinbuf()` over ALL of it **with no
>   bound against ring capacity**, capping `atapi_len` only afterwards — and `READ(10)` takes
>   a **guest-controlled** transfer length. `WDC_INBUF_SIZE = 512*(512+1) = 262,656` = exactly
>   513 blocks, so **block 514 of a single READ(10) begins overwriting unread data.**
>   DETECTOR DESIGNED, with the seat naming why the obvious oracle fails: fill the ring
>   exactly, require DRQ still set, write marker `0x5a` to DATA, read one byte and require
>   `0x40`. *"The marker is the crucial oracle: it proves the next producer did not overwrite
>   the oldest queued byte. Merely counting the diagnostics does not."* The committed probe
>   already reaches the exact-full path and does **not** measure the overwritten value, so the
>   round costs one row on an existing probe rather than a new witness.
>   Ranked above dormant debt, below a demonstrated boot-path corruption (stock-OS incidence
>   is unmeasured). **Needs a build** — queued behind the machine embargo.
> - **`wdcexpecteddata`** — the unexpected-DATA-write site is guarded by
>   `!d->write_in_progress && !d->atapi_cmd_in_progress`. **Drop the first conjunct and it
>   warns-and-latches on a perfectly LEGAL write during an active transfer** — and every row
>   of the shipped detector stays green, because none of them stages a WRITE command. This is
>   the accept-side hole the three quiet accept rows cannot cover: they pin a legal COMMAND, a
>   legal narrow WRITE and a legal narrow READ, none of them a legal DATA write mid-transfer.
>   Raised by the grok seat on the `wdcflood` pass-2 panel.
> - **`wdcflagindep`** — `#464`'s contract lists reset-on-normal-operation and
>   guest-resettable-operand under DESIGNED TO CATCH; each is measured at exactly ONE site of
>   six. Unpinned and known-reachable: reset-on-normal at `:160`, `:704` and `:145`;
>   operand-swap at `:583`, where the guard reads `warned_unimpl_cmd` while the body reads
>   `d->seccnt` — a field the guest writes — so `if (!d->seccnt)` scores a clean sweep. Site
>   numbers are PRE-FIX, the naming convention `wdcringambig` above already uses.
> - **`wdcperopcode`** — `:583` latches one line per DEVICE, not per opcode; the deepseek seat
>   argued for a per-opcode set. Explicitly OUTSIDE `#464`'s contract, not a floor breach.
>   Filed because the probe header asserted this was filed while no row existed: **a contract
>   line asserting a disposition is a WRONG RECORD until the disposition is a row.**
> - **`wdchpcmipsaddr`** — `DEVINIT(wdc)`'s `MACHINE_HPCMIPS` branch assigns `0x14000386`,
>   exactly what the default `devinit->addr + 0x206` already computes for `0x14000180`. It
>   carries a `TODO: Fix` and does nothing. Not guest-reachable; it earns a line only because
>   it sits on the two-instance route `wdcflagindep`'s probe would have to use.
> - **`wdcsectorreset`** — a ONE-LINE latch reset on a NORMAL register write restores the
>   `#464` width flood while leaving **all 26 detector rows green**. The edit, verbatim from the
>   pass-2 codex seat: add `d->warned_nonbyte_write = 0;` to the `wd_sector` write arm after the
>   existing `d->sector = ...`. A guest alternating a wide write to `wd_seccnt` with an ordinary
>   8-bit write to `wd_sector` then floods at one host line per pair, forever.
>   **Why every row misses it:** `interleave` pins reset-on-normal-operation at `:583` only,
>   using a valid COMMAND opcode; no row writes `wd_sector` between two wide accesses, so none
>   can see a reset keyed there. **It is SMALLER than the escape the capped ask-again found** —
>   that was two lines at the guard, this is one line at a different register — which is a
>   recorded limit of the ask-again rather than a failure of it: the ask-again asked about the
>   GUARD, and this edit never touches a guard.
>   SOURCE-PROVEN, **not measured** — the seat said so itself, so it is coverage debt under the
>   stopping rule and not a floor breach (`#464`'s detector satisfies clauses (a)–(f)). First
>   job is to build the mutant and score it. **Do not fold this into `wdcflagindep`**: that row
>   is about which SITES share a flag, this is about which REGISTER can clear one.
> 
> ### Six rows whose HELD stage was answered 2026-08-26 by a codex farm, one job per row
> 
> *Each was fired against the row's own `hold_question` rather than a disposition note. Every
> load-bearing claim below was re-verified against the source, the local DDI 0100I extraction,
> or the row itself before being written down.*
> 
> - **`b118L`** — a disk that fails to be added stays on the list. **DOCUMENTED-ONLY**: no
>   surviving caller exists. `emul_parse.c:558` exits at `:561`; `main.c:707` returns 1 at
>   `:709`, never reaching `emul_simple_init()`. **And `exitsweep` cannot activate it** —
>   `census_exits.py:59` scopes the census to `src/devices/` while both callers live in
>   `src/core/`, so the two rows must not be ranked together. Keep the reopen trigger: any new
>   caller, or any change to `:561`/`:709` that continues after failure.
> - **`b120r`** — SCSI reports a length exceeding what the guest asked for. **NOT covered by
>   `b120u`**: MODE SENSE is a known-command arm that already installs GOOD status, so a
>   default-arm repair leaves it untouched. Allocation 156 → internal `retlen` 256 → reported
>   length byte **0**. Ride it with `b120u` for economy but require its own hunk and an
>   allocation-length-invariance test. Priority stays LOW: no recorded rig naturally requests
>   156, and the full chain was not measured end to end.
> - **`dfreq`** — a one-shot deadline modelled as a repeating rate. **The row is internally
>   CONFLATED**: its closure names the MIPS CP0 Compare path while its assessment and the probe
>   that was built concern the ARM Footbridge. `footbridge_sites_probe.py` execs `-E cats` and
>   cannot reach CP0 Compare, and it returned correct values. The MIPS defect is real and
>   source-demonstrable — an accumulated periodic callback count means a Compare write clears
>   IP7 only momentarily, giving a wrong guest-readable Cause and an extra interrupt — but it
>   is **not end-to-end measured**. Documented-only under the stopping rule.
> - **`armbdt`** — ARM block transfer disagrees about an unaligned base. **REAL.** With
>   `U=0`, the masked fast path is right and the raw slow path is wrong. Controlling text is
>   **LDM(1) p. A4-37 and STM(1) p. A4-190**, read from `_scratchpad/ddi0100i.txt:7954`
>   and `:14115` — *not* LDR p. A4-44, which governs LDR's rotation rule and does not apply to
>   block transfers. **Fix shape:** mask ONLY the addresses passed to the two slow `memory_rw`
>   calls; masking at function entry corrupts writeback, which Addressing Mode 4 computes from
>   the raw `Rn`. Caveat for the record: `ARM_CONTROL_ALIGN` is initialised enabled but never
>   enforced, so at the advertised `A=1` state **both** paths are wrong — an alignment
>   exception is owed.
> - **`reprowitness`** — **NOT DISCHARGED**, two gaps in the shipped witness ladder. (1) Rung 2
>   admits construction witnesses, but the universal clause (ii) demands a device-signature
>   control that a construction-time OOB cannot produce — the ladder's own named exemplar fails
>   its own clause; scope (ii) to rungs 3–4. (2) `check_witness.py:56` already accepts
>   `harness:` and its header says *"IS A GAP IN THE LADDER, FOUND BY THIS CHECK ON ITS FIRST
>   RUN"*, which CLAUDE.md never absorbed. **The structure knew and the prose did not.**
> - **`ovsync`** — **NO-GO for closure as worded.** `4d0981d` fully fixes SYNCHRONIZE
>   CACHE(10) `0x35` — and did more than its filing claimed, since the base file was also
>   unflushed (`fsync()` with no `fflush()`). But **SYNCHRONIZE CACHE(16) `0x91` is undefined**,
>   falls to the unimplemented default, and `dev_asc.c:1287` converts absent status to `0x00`
>   GOOD — so a guest gets GOOD with overlay and bitmap still unflushed. Either route `0x91`
>   through the same helper, or narrow `ovsync` to SC(10) and transfer the `0x91` instance to
>   `b120`; then it may close.
> 
> ### Six more held stages answered 2026-08-26 by opus5, one job per question
> 
> - **`gateflr`** — if a whole gate BLOCK is deleted, nothing outside it notices. **Premise
>   refuted for part of the battery**: section R hard-fails for any block that is the sole
>   invoker of a python detector (every detector has exactly one invoker, verified). It stays
>   TRUE for log-grading blocks, source-grep blocks, per-row name lists, and all of
>   `gate_ab`/`gate_build`/`gate_upstream` — 38 check sites with zero python detectors.
>   **Its measured finding is already fixed**: section U's ratchet floor was 16 against a real
>   18, so two gate blocks could have been deleted with the check printing `good`. Now an
>   equality pin. Remaining proposal: a per-gate runtime check-count floor in `gate_end()`,
>   placed AFTER the fails/degraded tests so a degraded run reports SKIP and is never falsely
>   reddened. Honest limit recorded — a count floor cannot see a block hollowed while keeping
>   its call count, and this tree has a measured instance of exactly that.
> - **`seam`** — nothing goes red if the driver and the log grader disagree about the path.
>   **The cause is gone (#422) and the detector is still missing, asymmetrically.**
>   `drive_<rig>.log` is spelled twice: `drive_guest.py:250` is pinned by `selftest_logdir.py`,
>   `gate_hygiene.sh:444` is pinned by nothing — and a missing log there is answered with
>   `note` + `continue`, which increments nothing, **so two rigs' distress grading can silently
>   not happen while gate 6 reports PASS.** Sibling parity fails against the pmax/arc half
>   twelve lines up, where a missing log is `gate_skip`. Fix is one row in gate 5 (the
>   producer, because `$LOGDIR` persists between runs and a gate-6 discriminator would read a
>   stale log).
> - **`pcheck`** — the pre-commit check's blind spots. Python half PARTLY closed by a separate
>   tool (section R sees all 56 python artefacts; check E still cannot). Directory half
>   UNCHANGED and now broader: check C's `(src|regress|man)` alternation predates the harness
>   migration into git, **so the entire `tools/` tree is invisible** — `precommit_check.sh`
>   cannot cross-check a message naming itself. **And a FOURTH blind spot the row never named:
>   check D uses bare `git diff -U0` (unstaged only) while every other section uses both, so on
>   the ordinary add-then-commit workflow both its sub-checks print green about a diff they
>   never read.**
> - **`census`** — the proposed "a round that touches a gate runs that gate's mutant census"
>   rule is **REJECTED on three measured grounds**, and explicitly NOT as a clause-(b)
>   duplicate (different denominators). Its warrant is a stale 13-of-18 when the census defines
>   22 today; its trigger scales cost with the GATE rather than the diff, which is the `#392`
>   shape; and the function already ships continuously as `gate_offline.sh`'s selfmutant
>   manifest, with dated exemptions and an anti-paper check. **Adopt instead, bounded:** extend
>   `SM_COVERED`/`SM_EXEMPT` to `*_probe.py` — 40 probes exist and only 4 carry a failability
>   control. Section R checks a probe is RUN; nothing checks it CAN FAIL.
> - **`mrwstore2`** — a straddling store whose tail faults makes an MMIO head see the write
>   twice. **Keep filed/latent, but the blocking reason is REFUTED and was an L4.** Four
>   PowerPC manuals are now in `_scratchpad/` (OEA Book III, VEA Book II, MPCFPE32B Rev 2, the
>   2005 PEM): every one makes partial execution **PERMITTED, never REQUIRED**, so a fix that
>   never partially executes cannot diverge — it is the intersection of both readings. The
>   manuals **disagree** on the caching-inhibited+guarded head case (Book III says it must not
>   be accessed; the PEM has no such rule), recorded as an honest UNKNOWN. Also found: a second
>   straddling producer the row never named (`X(stvx)` does a raw 16-byte access with no
>   `EA & ~0xF` mask), and that "memory_rw is the choke point" is FALSE for the class —
>   `stmw`/`stswi`/`bdt_store` have the same property outside it, **so a memory_rw fix would be
>   a partial fix that reads as a complete one.**
> - **`m8probe`** — m8820x PROBE_USER/PROBE_SUPER are dropped. **LATENT — re-filed on the
>   `gdrompiooddlen` precedent, reachability MEASURED NEGATIVE with controls both ways.** A full
>   OpenBSD 7.7/luna88k boot to `login:` issues seven distinct CMMU commands and **zero**
>   probes; a planted supervisor store fires the detector on 0x24/0x20 and not on 0x35, so the
>   negative is real. OpenBSD's CMMU driver issues probes only from DDB display routines — a
>   debugger feature, not an operating path. **The cost note was wrong**: the translation walk
>   EXISTS and is already side-effect-free under `FLAG_NOEXCEPTIONS`, and the driving probe
>   shape is already committed. What is missing is an ORACLE (no 88200/88204 manual), so the
>   hold is now conditional on obtaining one. Current behaviour is the better one: a dropped
>   probe leaves SSR zero — a defined miss — where an invented answer could steer guest paging.
> - **`panelrefire`** — `panel.sh` printed **"re-firing once (a wall can be minutes long) ..."**
>   and then `return 2`. Every caller is a bare `check "name" "$file"` whose exit status is
>   discarded, and no seat command is re-invoked anywhere afterwards. **Nothing was ever
>   relaunched.** Worse than a stale citation: it printed a claim of ACTION to the operator at
>   the moment a seat was lost, so the one person who could re-fire by hand was told it had
>   already been done — the failure `panel.sh` itself warns about sixty lines up. **The message
>   is FIXED** (it instructs rather than reports) and the carrier's "both applied" claim is
>   corrected. **What is filed is the automatic retry**, which owes two negative controls: prove
>   it fires on a walled seat, and prove a seat that ANSWERED is not retried.
> - **`depsrm`** — the standing `rm src/cpus/*.o` before every build rests on a **false
>   reason**. The carrier said the `#include`d `.c` files are "invisible to the dep rules";
>   `src/cpus/Makefile:214` — the *generated* makefile make actually reads — names
>   `cpu_sh_instr.c`, `cpu_dyntrans.c`, `memory_rw.c` and the `tmp_*.c` files as explicit
>   prerequisites of `cpu_sh.o`. **Make tracks them.**
>   **This is a throughput question, not a tidy-up:** the `rm` runs before every mutant build,
>   and mutant tables are the dominant cost of a round — one round built nine binaries. **KEEP
>   THE `rm` until measured**: an unnecessary rebuild costs minutes, a stale object costs a
>   wrong measurement. Owed measurement is small — edit an `#include`d `.c`, rebuild without
>   the rm, assert the binary changed; then repeat for a generated `tmp_*.c`, the case most
>   likely to still need it.
> - **`gdromallocpair`** — `alloc_data()` does not release before it allocates, so #465's
>   `free_data()` pairing is **conventional, not structural**. Found by the grok seat on
>   #465's pass 2, verified by reading: `free_data(d)` runs once at the function entry
>   (`:343`) and both `alloc_data(d)` sites (`:359`, `:435`) are downstream, so the buffer is
>   always released before replacement *today* — but `alloc_data()` overwrites `d->data`
>   unconditionally, and **a future third call site not preceded by that entry release leaks
>   the previous buffer silently.** NOT fixed: a release inside `alloc_data()` is an ADDITION,
>   and with no third caller there is no mutant that can measure the delta the licence
>   requires. Recorded so a round that ADDS a third call site inherits the obligation.
> - **`preserveinstrument`** — the durable-path rule preserves **measurements** but not
>   **instruments**. #465 saved a seat's 22 artifacts (8 score logs, 8 build logs, source
>   snapshot) and *not* the 26-row probe that produced them. When the pass-2 adjudication then
>   recommended porting six of its rows — explicitly because "the construction and measurement
>   cost is already paid" — the instrument was gone and the cost had to be paid again.
>   **A score log makes a claim CHECKABLE; only the instrument makes it REPRODUCIBLE.**
>   Proposed, not adopted: preserve the instrument alongside the output. One more `cp`.
>   *Same shape as #465's own defect, one level up: that round fixed two fields SET together
>   and RELEASED apart; here an output and its instrument are PRODUCED together and PRESERVED
>   apart.*
> - **`probewiringscope`** — `check_probe_wiring.py` **cannot see any detector below
>   `regress/`'s top level**, while its own docstring (`:2`) claims *"every committed
>   DETECTOR under regress/"*. `:475` filters `f.endswith(".py") and "/" not in f`; `:481`
>   uses `os.listdir` rather than `os.walk`.
>   **This is the structural home #465's headline lesson should have had.** That round
>   found its detector wired into no gate, discharged it by a HUMAN GREP, and wrote the
>   lesson as prose — while the mechanical check for exactly that class sat one directory
>   away, blind by scope. A check that cannot fail for a whole subtree; third instance of
>   that class in one day, after `panel.sh`'s phantom re-fire and `grok models` as a tier
>   check.
>   **Exposure is ZERO today** — 1 of 57 tracked `regress/**.py` sat below top level and it
>   is now gated by hand — so the defect is LATENT, which is why it is filed rather than
>   fixed in-round. The fix re-keys `MANIFEST`/`EXEMPT` from basename to relative path and
>   swaps `listdir` for `walk`; it **owes negative controls in both directions** (a
>   subdirectory detector with no gate must go RED; a gated one must stay GREEN), and the
>   file already carries an 18-mutant `--selftest` harness to hang them on. A basename→path
>   re-key can silently collide when two directories hold the same basename, so that needs
>   its own row. Found by the opus5 seat on #465's pass 2.
> - **`panelcite0824`** — four uncited panel dirs from 2026-08-24 hold **~23 substantial
>   seat answers** that section G has never scoped. `check_seats_read` verifies every seat
>   in a **cited** dir is recorded; **an uncited dir is invisible to it by construction** —
>   the second check-that-cannot-fail found on 2026-08-26, after `check_probe_wiring` being
>   blind below `regress/`'s top level.
>   MEASURED: 166 `panel_<date>_<time>` directories exist, 76 cited, 94 not. **Scoped
>   deliberately to the last three days**, only five were uncited and one was that day's own
>   panel (since cited). The older dirs belong to closed rounds whose findings *were* acted
>   on, so counting all 94 would overstate the class ~4×.
>   DISPOSITION: harvest the four dirs — read each answer, record what it found, cite the
>   dir — after which G covers them mechanically forever. Bounded, with a definite end.
>   **CORRECTED after adjudication: the set is EIGHT dirs, not four** — four more on
>   08-25 that an exact-match filter could not see, one of them a **pass 2 on a shipped
>   source-touching commit**. Census, suffix-aware: **174 dirs / 78 cited / 96 uncited**
>   (deriver on the ledger row), so the gap is ~12×, not the ~4× first filed.
>   *Filed first as 166/76/94 — the third wrong census in a row and by the OPPOSITE error
>   to the second: a loose glob matched `.out` files, then an exact filter dropped eight
>   suffixed dirs. `check_seats_read.py` already handles suffixes; I wrote a filter
>   instead of reading the one that works.*
>   **The cutoff is 2026-08-24 — the citation rule's own adoption date, forward-only** —
>   re-warranted after an adjudicator checked three older dirs and found every finding
>   absorbed. n=3 is not a proof: **if the harvest finds one live unacted finding, sample
>   the 08-22/23 band before closing.**
>   *Two defect shapes worth keeping. (1) The first draft named a dir in full, so a grep
>   scored it CITED on the strength of the sentence saying it was uncited — and the first
>   fix was defeated by its own explanation. A record naming an artifact it asserts is
>   unrecorded must not write that name in the form the checker matches, prose included.
>   (2) The claim that every unread-review instance that day was "a finding nobody had
>   opened" is refuted by my own commit body: the largest was a review read thoroughly
>   and left unrecorded. Today's were RECORDING gaps; the round-costing ones are
>   historical.*
> - **`loadfragile`** — every pty probe waited on an **absolute** deadline, so a merely SLOW
>   run failed identically to a STUCK one and the battery could only be trusted on an idle
>   machine. **Zero files used an inactivity deadline.** `#467` resets the clock when the
>   buffer grows, so `timeout` means SILENCE — strictly more permissive for a run that
>   produces output, identical for one that does not.
>   *The first framing was wrong and was corrected before acting: work-accounting (`#419`'s
>   `LUNA_BUDGET`) cannot fix a TRANSPORT timeout, because while waiting for bytes there are
>   no guest instructions to count. Classification of 249 references: **245 transport
>   timeouts, 3 guest-side budgets, 1 true measurement oracle** — converting literally as
>   first proposed would have changed one thing.*
>   Detector `selftest_inactivity.py` ships with it, two legs OPPOSITE IN SIGN (the
>   genuinely-stuck leg is the one that matters — a conversion making the timeout
>   unreachable would sail through the other and defend nothing). **`free_run()` is
>   deliberately NOT converted:** it is an exposure window, not a timeout, and a naive sweep
>   over `time.time()` sites would have eaten it.
> - **`gdrompiooddlen`** — the GDROM PIO read guards ONE byte and then reads TWO, and
>   `alloc_data` mallocs exactly `data_len` with no padding. **LATENT, NOT LIVE:** the owed
>   reachability check came back NEGATIVE the same day. `data_len` has exactly one writer, and
>   both routes to it force an even value (`cnt != 408 -> exit(1)`, and
>   `sector_count * 2048 != cnt -> break`). A guest CAN express an odd count at the CNTLO/CNTHI
>   registers; it cannot get that value past either guard. The asymmetry is real and any future
>   edit admitting an odd length makes it live immediately — but it is not a defect a guest can
>   reach today, and this row must not be ranked as one.
> - **`asicannounce`** — `#463` deleted the ASIC's only diagnostic on a warrant measured too
>   broad; a bounded latched announce IS constructible, on a predicate that is not empty. Filed
>   under the late-dissent rule with three seats' dissent carried verbatim.
> - **`asicarraygeom`** — shrinking a modelled array to `[2]` scores a CLEAN SWEEP; no row
>   verifies the struct declaration the whole invariant rests on.
> - **`gdromkeyindex`** — five mutants score a full 32/32 against `#461`'s detector.
> - **`probeabsentraise`** — three rows guard a THREE-state value with a TWO-state test and
>   raise `ValueError` on `absent`.
> - **`proberowsubset`** — the probes cannot score ONE row, so adding a row to a measured
>   detector costs a full re-run. *This one bit the `wdcflood` round directly.*
> - **`killdriverunTracked`** — the kill-table driver lives in a session temp dir, so the
>   apparatus producing this project's most-cited numbers is untracked.
> - **`citestale`** — a same-file line citation is invalidated by the round's OWN later edits.
> - **`scoreclaimhex`** — `check_score_claims` reads a slash-separated HEX LIST as a score claim.
> - **`sectionEnarrow`** — precommit section E sees only `regress/diff_*.c`, 14 of 52 detectors,
>   and prints an unqualified verdict over that subset.
> - **`ledgerstatelies`** — the ledger's `state` field had no written semantics; the block is now
>   RATIFIED with the `open` definition added.
> - **`ledgerclosureby`** — `closure.by` holds the wrong KIND of value on two rows.
>
> ### OPEN — post-2026-08-01 residuals (surfaced by the #385 re-audit; full detail in the dated tail)
> - **#364 residuals** — the general-path writeback sites remain unmeasured beyond the
>   shipped telemetry; four load/store translation units have no row (`p0_u0_w1`,
>   `p0_u1_w1`, `p1_u0_w0`, `p1_u0_w1`); the general STORE-arm row is owed
>   (harness tasks #42, #22).
> - **#378 latent** — `generate_arm_multi.c`'s emitted fast path is order-blind by
>   construction and 23/256 emitted handlers load PC; #378's install gate closes the
>   BE *install*, not the emitter. Latent, not live (harness tasks #59, #60 carry the
>   measurable edges).
> - **#380/#381 residuals** — crosspage idle-fold loss (pre-existing), the tb1
>   privilege-by-construction note, the once-per-BREAK semantic limit
>   (harness task #61).
> - **#376 harness residuals** — the mutation selftest counts a crashing mutant as
>   detection (task #55); the rounding-probe parser lacks address binding (task #56);
>   arc-only `.l` rows owed (task #57).
>
> **Ready to work — reproduced, and an instrument already exists**
> - ✅ **MIPS `cvt.d.l` (and `cvt.s.l`) ignore the rounding mode → RESOLVED as #301**
>   (round 66). L→D is exact integer rounding in the requested mode (the discarded low
>   bits ARE the remainder — no fma); L→S goes via round-to-odd so the single store
>   rounds correctly in every mode. The L→S half was deferred in the first draft and the
>   panel refused, each seat with its own witness class (tie-down-twice, and
>   one-below-a-midpoint rounded onto it). Covered by the new gate 12 on the arc rig —
>   including an FR=0 row, because every other row ran with Status.FR set and the
>   pair-assembly path deserved a measurement, not a reading — plus 34 offline vectors
>   with both helpers' negative controls failing exactly their five predicted rows.
>   pmax raises Reserved Instruction on the `ldc1` (cvt.d.l is MIPS-III+), so the blast
>   radius is R4000+ and the R3000 rig is untouched by construction.
>   Indexed, not modelled: some real silicon (the VR4300 famously) raises Unimplemented
>   Operation for L operands beyond 2^53 and lets the kernel softfloat complete —
>   architecturally the same FCSR-rounded value; GXemul's no-trap depth here matches its
>   pre-existing modelling (#246 covers denormals only).
> - ✅ **m88k float→int conversions → RESOLVED as #302** (round 67), and the scope GREW
>   in review: `trnc.ss`/`trnc.sd` were raw C casts (host-UB on specials — x86 answered
>   0x80000000 for everything), and `int`/`nint` — the other two thirds of the MC88100
>   triad — were **absent from the decoder entirely**, so a legal guest instruction
>   halted the emulator ("All machines stopped", reproduced for both). The contract is
>   OpenBSD's kernel completion (the MC88100 traps on every special and writes nothing;
>   the manual's trap window even catches in-range [2^30, 2^31), which the handler
>   completes): SoftFloat saturation with **all NaN forced positive** — a third table,
>   distinct from SH's (#297) and MIPS's (#273). One shared mode-parametric ladder
>   serves the triad: trnc→toward-zero, int→fcr63 via the #298 decode, nint→nearest.
>   Thirteen new gate-11 rows (38 total); the trnc mutant failed exactly its four
>   discriminators.
> - ~~**`ieee_interpret_float_value` mis-decodes subnormals with an implicit 1**~~ —
>   **RESOLVED as #303 (round 68)**: biased exponent 0 now decodes without the implicit
>   1 at exponent 1−bias; exhaustive both-signs S + 400k D offline rows, all bit-exact.
>   The "invisible through stores that flush" theory was HALF-wrong: the pass-1 claim
>   that MIPS was fully masked by #246 was refuted by two panel seats and the rig —
>   `fpu_unimpl_trap()` returns 0 on EXC3K (R3010 interrupt pin unwired), so
>   **pmax/R3000 consumed the garble** (measured `0x32000001` for S-min×2^100, now
>   `0x27000000`), as did m88k, SH, Alpha and PPC (`lfs` alone: `0x3800000020000000` →
>   `0x36a0000000000000`). arc/R4000 keeps the trap — the no-change control. Sixteen
>   new gate rows across gates 2/10/11/12 + mutant `revert303`; two pinned KNOWN-CHANGE
>   flip rows (garbled S-normal products → true subnormal results → deliberate
>   #287/#292 store flush → +0) are the before/after evidence the store-side round
>   below inherits.
> - ~~**Store-side subnormal ENCODE**~~ — **RESOLVED as #331–#334 (round 72)**, and the
>   entry as filed named the wrong line for half of it. Measured on the committed build
>   first, against oracles that are not the code under test — for D the identity (every
>   finite double is exactly representable, so nothing is rounded and the owed answer is
>   the input's own bit pattern), for S the host's correctly-rounded cast under the
>   matching mode: **D 220/220 wrong** (no gradual underflow in double precision *at
>   all* — the arm was an empty `// TODO`) and **S 65737/65740 wrong, of which 65736 came
>   through the `FP_NORMAL` arm and one through the `FP_SUBNORMAL` arm this entry
>   blamed.** A single-subnormal value like `1e-40` is a NORMAL host double; it was lost
>   to the exponent clamp and the flush, not to the TODO.
>   **Both of #292's stated rationales were false.** "MIPS routes non-flush denormal
>   results away (#246)" holds only for EXC4K+ with FS clear — `fpu_unimpl_trap()` returns
>   0 on EXC3K so R3000 fell through, and the FS=1 arm *deliberately skips* the routing,
>   so **R4000 was getting its flush from the bug**. "SH DN=1 silicon" was true of the
>   silicon and not of this tree: `SH_FPSCR_DN_ZERO` was read by nothing, and FPSCR resets
>   with DN set, so the encoder fix alone would have changed the DEFAULT SH configuration.
>   Both now state their policy at their own store sites (#332, #334), as does Alpha
>   (#333). pmax is deliberately **left flushing**: a panel seat established from the IDT
>   manual that the R3010 leaves the destination unchanged on UnImp and that software
>   completion is a later action, so recording `0x80000002` as the hardware answer would
>   have been a false row — and GXemul wires no R3010 interrupt pin, so declining to write
>   would leave a stale register instead. Nine new named vectors, two new mutants.
>
> - ~~**PowerPC `fmadd`/`fmsub` modelled unfused**~~ — **RESOLVED as #335 (round 92)**.
>   Book I rounds the product-sum once; `fra.f * frc.f + frb.f` rounds twice unless the
>   compiler contracts it, so correctness was a property of the BUILD HOST. Measured
>   `0000000000000000` where the ISA owes `b970000000000000`, with a `2.0*3.0+1.0 → 7.0`
>   control passing on both sides to rule out a wrong register field. Now `fma()`.
>
> - ~~**`fmadd`/`fmsub` raise none of their exception causes**~~ — **RESOLVED as #343
>   (round 95)**. Measured at `00001000` (FPCC alone, no cause bits) on every row before
>   the fix. `ppc_invalid_cause_fma()` treats the three conditions as independent, which
>   `ppc_invalid_cause()` cannot: it returns a single cause and abandons its op test at the
>   first NaN. The `Inf × 0` with sNaN addend case now correctly owes **both** `VXIMZ` and
>   `VXNAN` (`a1101000`), and the four VXISI rows are a 2×2 on identical operands pinning
>   `fmsub`'s addend-sign inversion. Eight new gate-13 rows.
> - **`fnmadd`/`fnmsub` are not decoded and halt** (`ppc_halt_probe.py:260` has them
>   pending). When implemented they must negate the **already-rounded** result —
>   `-fma(a,c,b)` and `-fma(a,c,-b)` — because the ISA rounds before the final negation,
>   so moving those signs inside the FMA is NOT equivalent under directed rounding. The
>   single-precision `fmadds`/`fmsubs` family must stay fused as well and cannot alias
>   the double handlers, whose final rounding is to D.
> - ~~**PowerPC `FPSCR[RN]` is not wired to arithmetic**~~ — **RESOLVED as #336 (round 91)
>   for `fadd`/`fsub`/`fmul`/`fdiv`**, which now use #300's `_rm` helpers. Measured
>   `1.0 + 3*2^-54` under RZ answering `3ff0000000000001` (the nearest result) where
>   toward-zero owes `3ff0000000000000`, with an RN control row pinned unmoved.
>   **`fmadd`/`fmsub` remain unwired**: #335 made them correctly fused, but `fma()` rounds
>   per the HOST mode, so a directed-mode fused rounding needs an exact product-sum rather
>   than a two-operand helper. That is the residue of this item.
>
> - **(historical) PowerPC `FPSCR[RN]` was not wired to arithmetic at all.** `fadd`, `fsub`, `fmul`,
>   `fdiv`, `fmadd` and `fmsub` all compute in host double under the HOST rounding mode
>   and store through the legacy entry point (`cpu_ppc_instr.c:1746/1800/1849/1907/1961/
>   2024`); only the conversions `frsp` (`:1546`) and `fctiw` (`:1687`) read the mode.
>   #300's `ieee_add_round_rm`/`ieee_mul_round_rm`/`ieee_div_round_rm` already exist and
>   are wired on MIPS, SH and m88k. The fused `fmadd` case is harder than the other four:
>   `fma()` rounds once but per the host mode, so a directed-mode fused rounding needs an
>   exact product-sum rather than a helper call. Gate 13 exists with 121 rows to build on.
>
> - ~~**The ARM instruction COMBINER changes observable flags — and NO probe can
>   see it.**~~ — **RESOLVED as a campaign, not an entry.** #340 built the
>   two-pass free-running witness and fixed the `teqs`/`tsts` `*_samepage`
>   handlers; #342 the `xchg` fold; #345/#346/#347 the cache-clean matchers and
>   registers; #348/#349/#350 the cache-clean exit flags, the fold-fired marker
>   channel, and the non-multiple runtime guard (see the 2026-08-09 entry at the
>   end of this file). [#385 update, 2026-08-12: the two family members this
>   entry still named as diverging have since been resolved as well —
>   `netbsd_idle`'s skipped TEQs and unwritten destination by #351/#352/#353,
>   `netbsd_memcpy`'s stale r3/r4/ip/lr by #354; the dated entries below carry
>   both resolutions.]
>
> - **Still open, from round 72's own findings** (recorded, not guessed at):
>   - **PPC-D, Alpha, and SH PR=1 D arithmetic have no gate rows at all**, so #331 changed
>     them without a witness. Alpha has no rig, which is why #333 is deliberately
>     bit-identical to previous behaviour rather than a refinement; whether the
>     architecture wants `+0` for a negative tiny cannot be measured here.
>   - **The #246 trap predicate is pre-rounding.** `fabs(nf) < FLT_MIN` at
>     `cpu_mips_coproc.c` traps values in `(2^-126 - 2^-150, 2^-126)` that round *up* to
>     `FLT_MIN` and are therefore normal results; MIPS specifies tininess after rounding.
>     #332's substitution classifies on the encoded word and is correct; the trap check
>     above it was left alone because moving it changes WHEN the trap fires for a band the
>     committed arc trap rows sit near, and that measurement was not made this round.
>   - **PowerPC `NI`** is defined and never consumed — another architecture-level FTZ
>     policy that must not contaminate the generic encoder.
>
> - ~~**PowerPC, four measured defects**~~ — **RESOLVED as #304/#305 (round 69)**, with
>   **gate 13** built first on the probe path: 50 rows, every committed byte recorded
>   before a line of the fix existed. `frsp` now narrows by exact bit surgery under
>   `FPSCR[1:0]` (three of four modes had been unreachable behind a host cast) and keeps
>   a NaN instead of delivering +0.0; `stfs`/`stfsx` implement Book I's denormalization
>   band; and #305 stopped all four conversion instructions destroying a NaN's sign and
>   payload (`lfs(0xffc00001)` used to arrive as `0x7fffffffffffffff`). All 25
>   discriminators flipped to pre-registered bytes on the first run; all 25 pins held.
>   The fourth "defect" was REFUTED by measurement — finite values ≥2^128 already give
>   ±Inf (#287) — and closes as a pin.
>   **Still true, still enforced:** do NOT wire `stfs` to FPSCR.RN; it does not round.
>
> **PowerPC, filed by round 69's panel and each owed its own round**
> - **The single-precision arithmetic family does not narrow**: `fmuls` is an alias of
>   `fmul` (and the rest follow), so `float` arithmetic keeps double precision. #304's
>   helper now exists, so this is wiring — but it needs the store-side subnormal contract
>   settled first, or it bakes in a policy that round may change.
> - ~~**The update-form conversions are not decoded at all**~~ — **RESOLVED as #310
>   (round 70B)**, and the family was twice the size this entry named: the four primary
>   opcodes (`lfsu`/`lfdu`/`stfsu`/`stfdu`, whose defines were missing outright) *and*
>   the four indexed forms (extended opcodes 567/631/695/759). All eight were measured
>   halting the emulator; eighteen gate-13 rows now assert both the value transferred and
>   the base-register update, with non-update controls proving the base stays put.
>   A prevalence claim made for this fix was **withdrawn**: restricted to the executable
>   section, the NetBSD/macppc kernel contains none of these forms — the hundreds first
>   reported were data in the read-write-execute segment.
> - **The exception-enable bits (OE/UE/VE) and the FPRF class bits are unmodelled.** Not
>   forced piecemeal, for the reason the SH exception model is not: a lone enabled bit
>   implies the others work. Round 73's after-pass added two specifics and a warning:
>   `fctiwz` owes **VXCVI** (and **VXSNAN** for a signalling operand). ~~and `mtfsf`
>   must not copy FEX and VX~~ — **RESOLVED as #327 (round 88)**, together with the
>   recompute it had to land beside: VX and FEX are now DERIVED from the causes and
>   enables rather than stored, in both directions, so the phantom "VX set with no
>   cause" state #326 made reachable is gone. `frsp`'s unconditional FX set and an
>   order-dependence in FEX went with it. The warning, and it is load-bearing: `fctiwz`'s existing
>   `>= 2147483647.0` / `<= -2147483648.0` branches give the right *result* but are not a
>   correct *classification* of "out of range" — the model range-checks after rounding,
>   so under round-toward-zero an operand stays convertible while `x < 2147483648.0`.
>   Reusing those branches to raise VXCVI would flag endpoints that are not invalid.
> - ~~**Seven FP control/convert encodings are absent from the tree entirely**~~ —
>   **largely RESOLVED as #326 (round 87)**, and the entry understated it badly: a 28-row
>   sweep measured **twenty-four** legal encodings halting the emulator, not seven. The
>   biggest was not an instruction at all but `if (rc) goto bad;` at both floating-point
>   entries, so **every record form** halted — `fadd.`, `frsp.`, `fmr.` — including those
>   of instructions that worked with Rc=0. Twelve are decoded now (the Rc forms, `mcrfs`,
>   `mtfsb0`, `mtfsb1`, `mtfsfi`, `fctiw`, `fnabs`, `fsel`); gate 15 holds the line.
> - **Twelve encodings still halt, deliberately, and gate 15 asserts that they do.** Split
>   by reason, because the reasons are not the same:
>   - `fctid`, `fctidz`, `fcfid`, `fsqrt`, `fsqrts` — **64-bit-only, or outside the G4's
>     instruction groups.** On a 32-bit G4 real silicon raises a program interrupt, so
>     implementing them unconditionally would make the model *less* faithful. These ride
>     on the missing exception model, not on decode work.
>   - `fres`, `frsqrte` — estimate instructions, accuracy implementation-defined.
>   - `fcmpo`, `fnmadd`, `fnmsub`, `fmadds`, `fmsubs` — **no technical blocker.** A few
>     dozen lines each at the fidelity bar already shipped (`fadds` and `fmuls` are
>     aliases of their double forms today). Out of #326 for round size alone. Do
>     `fmadds` first: gcc emits it for ordinary `float` arithmetic, so it is likely the
>     most frequently executed instruction still in this set.
> - **The splice letter is deliberately not followed** for finite values around 2^129:
>   Book I's `SINGLE()` would WRAP the exponent (2^129 → a 2.0f-class pattern, 1.5·2^128
>   → the NaN pattern `0x7FC00000`), and this fork keeps #287's ±Inf instead. Panel
>   3–1 with the dissent recorded; reopen only on silicon evidence or a guest victim.
>
> **Instruction-coverage gaps (the decoder rejects legal encodings)**
> - ~~**m88k `fdiv.dds`** and **mixed-format S-destination arithmetic**~~ — **RESOLVED as
>   #306 (round 70A)**, and the census found the entry understated it: the size field is a
>   format *triple*, so each of `fadd`/`fsub`/`fmul`/`fdiv` has eight legal forms and
>   **twelve** were missing, not two. Six were measured halting the emulator on the
>   luna88k rig. Eighteen gate-11 rows cover them — including the `fmul.ssd` mode rows
>   that caught a double rounding in the fix itself, registered by a panel seat before the
>   code was tested.
> - ~~**m88k `tcnd` absent from the decoder**~~ — **RESOLVED as #307**: modelled from the
>   manual's four-class condition mask (the zero test is the NOR of the low *31* bits, so
>   `0x80000000` is its own class), with `tb0`/`tb1`'s privilege-then-condition order,
>   plus disassembly. Upstream's own narrow patch was refused: it leaves `tcnd eq0,r0`
>   halting, and `0 == 0` is the case that must trap.
> - ~~**`fdiv_sss` double-rounds**~~ — **WITHDRAWN as a phantom** in the same review that
>   filed it. Inexact is not the same as double-rounds-wrong: with two single sources the
>   quotient's error can never reach a single-precision midpoint (the exclusion-zone
>   argument), and 400,000 random single÷single quotients found no disagreement with a
>   single correct rounding. The arms that genuinely had the hazard were the six #306
>   introduced, and they were fixed in the same round by **#308**'s round-to-odd helpers —
>   which also revealed that #300's `_rm` helpers return the host result unchanged under
>   nearest, correct for a double destination and a double rounding for a narrower one.
>   **The "still open elsewhere" clause that used to close this entry is WITHDRAWN too**,
>   as the same phantom wearing a different architecture's name. It read: the narrowing
>   question "applies to MIPS `div.s`, SH `fdiv`, and both architectures' single-precision
>   `sqrt`" — but that is the *same arithmetic* the paragraph above refutes, single sources
>   into a single destination, and the sentence sat ten lines under its own refutation for
>   five rounds. Neither instruction has a mixed-format form: `cpu_mips_coproc.c:1301`
>   and `cpu_sh_instr.c:3425` divide S by S, `:1313` and `:3212` take the root of an S.
>   The bound is explicit — for singles `a`, `b` and any single-format value or midpoint
>   `s`, `q* - s = (a - s*b)/b` where `a - s*b` is an integer multiple of
>   `2^min(ea, es+eb)` with a significand product under 2^48, so a nonzero difference is at
>   least `2^-48*|q*|` (`2^-49` against midpoints), while harmful double rounding needs the
>   exact value inside the intermediate double's half-ulp at `~2^-53*|q*|`. That is a
>   32-fold gap, 16-fold against midpoints; the same argument through `s^2` gives
>   `>= 2^-49*sqrt(a)`. Measured as well as argued, against exact-rational oracles using no
>   host FP, in all four modes: 157,920 random quotients and 120,006 random radicands, plus
>   219,888 **constructed** division cases and 95,628 constructed root cases built to land
>   *on* grid points and midpoints — 0 mismatches, closest approach `2^-41.29`, twelve
>   binades short of where a double rounding could bite. Two review seats reached this
>   independently, one analytically and one by sweep. The hazardous class is
>   wide-source/narrow-destination, which is exactly where #308's helpers were applied
>   (`cpu_m88k_instr.c:1668`); MIPS and SH have no such instruction to apply them to.
>   **The deliverable for this item was the search, and this paragraph is it** — recorded
>   at length so the next triage does not re-file it a third time.
> - ~~**m88k `bcnd`'s condition table is NULL for legal unnamed masks**~~ — **RESOLVED as
>   #323 (round 76)**. Reproduced first: all nine named masks ran, and all eight unnamed
>   ones tested (0, 4, 6, 9, 0xa, 0xb, 0xf, 0x11) halted the emulator. Fixed the way #307
>   fixed `tcnd` — the manual's four-class mask written once, replacing the enumeration of
>   nine named comparisons rather than sitting beside it, so `print_operator()` is gone.
>   Seven gate-11 rows assert the branch DECISION, including the pair `m5=4` vs `m5=0xc`
>   that differs only on the most negative value and would catch an implementation that
>   collapsed those two classes.
> - **MIPS paired-single arithmetic is unmodelled.** Deferred on purpose: the FIR
>   advertisement sits inside `#if 0`, so the emulator makes no false claim a test could
>   reproduce. This is feature work, not defect work. Reopen when a rig boots a
>   PS-capable CPU or a guest binary executes PS.
> - **SH `ftrc` with an odd m under PR=1** decodes as an odd `fr[]` pair (reserved
>   encoding, pre-existing dispatch behaviour).
> - ~~**ARM's subtract carry, ADCS's overflow flag, and the undefined space**~~ —
>   **RESOLVED as #311/#313/#312 (round 71)**, the first ARM work in this fork, opened
>   with a new instrument (gate 14, 58 rows on a `testarm` cold debugger; the pre-fix
>   build scored 39 of the 56 rows then present, failing exactly the 17 predicted rows
>   and nothing else). #311: the carry-out was `a >= b` for the whole
>   subtract family, which is right for SUB/CMP/RSB but ignores the borrow SBC/RSC just
>   subtracted — wrong exactly when `a == b` with carry-in clear, i.e. the ordinary way
>   multi-word arithmetic makes a zero limb. #313, found by a panel seat reading the `#if`
>   nesting: ADC was named in the outer guard that CLEARS V but matched neither inner
>   formula, so `ADCS` could only ever clear the overflow flag. #312: unmatched encodings
>   in the `main_opcode >= 6, bit 4` space halted the emulator, and the halt fired at
>   DECODE — so a *conditional* undefined word whose condition was false stopped the
>   machine too. The tree's own correct routing sat a few lines below, unreachable behind
>   an identical predicate; three seats verified the identity and it was deleted.
> - **The `A__PC` operand at the very top of the address space** (`cpu_arm_instr_dpi.c`,
>   raised by three seats reviewing #311, one of them calling it a regression the round would
>   introduce rather than a pre-existing corner). With Rn = PC the operand is recomputed as
>   page base + slot + 8 in 64-bit arithmetic, which passes 2^32 for the last two instruction
>   slots of the 4GB space, and #311's `c32 == c64` would then differ from the old truncating
>   test. **FIXED as part of #311** by truncating that operand to 32 bits — correct
>   independently of the carry change, since ARM's PC is 32 bits and reading it must wrap, and
>   it also removes a spurious carry the ADD family has reported at those two addresses since
>   long before this round. **Still open is the measurement:** the fix is a provable no-op for
>   every operand below 2^32, which is everything these rigs can reach, so its effect at the
>   top of the address space is reasoned rather than measured. Reaching it needs RAM mapped at
>   `0xfffff000` — a `dev_ram` config statement is the only route found so far.
> - ~~**Three more guest-reachable halts in the ARM decoder**~~ — **RESOLVED as #319/#320
>   (round 78)**, and the round found a fourth defect that never halted: the immediate
>   guard exempted an imm8 of zero, so `movs r0,#0 ROR 4` shipped with the wrong carry
>   instead of stopping loudly. Also **#321**: `mvns` with an immediate took its shifter
>   carry from the COMPLEMENTED operand (the decoder rewrites `mvn #imm` to `mov #~imm`),
>   which is wrong in every band — measured setting the carry where the architecture
>   leaves it alone, setting it where the architecture clears it, and clearing it where
>   the architecture sets it.
> - **The combined TST/TEQ handlers never update the carry** — established by reading,
>   **NOT reproduced**, and deliberately not fixed. `tsts_lo_beq_samepage`,
>   `teqs_beq_samepage` and their `bne` twins all do
>   `flags &= ~(ARM_F_Z | ARM_F_N)` and never write C, while the uncombined path does
>   write C whenever the immediate was rotated. The combiner installs them from
>   `COMBINE(beq_etc)` on `ic[-1].f == instr(tsts)` with only a bit-31 guard on the
>   immediate — which prevents the case where C would need to be SET and not the case
>   where it must be CLEARED.
>
>   **What defeated the reproduction, recorded so the next attempt starts further on:**
>   instruction combination is gated on `!single_step && !single_step_breakpoint`, so a
>   `step`-driven probe can never reach it — and on `testarm` a free-running `continue`
>   never returns to the prompt (the machine's halt stub leaves the guest spinning), so
>   there is no way back to read the result. Driving it with a breakpoint DOES return,
>   but a differential run with and without `-J` (which forces combining off) produced
>   **identical** flags, so either the breakpoint suppressed the combination or it fired
>   without changing the answer. The two cannot be told apart without a positive control
>   that the combination actually occurred — the instruction counter is the obvious one,
>   since a combined handler counts one instruction where two executed.
>
>   Until that control exists this stays open and unfixed: the reading is suggestive,
>   but a fix with no reproduction is exactly what this project does not ship.
>   **[#385 re-audit update, 2026-08-12]** The missing positive control has since been
>   BUILT, so the blocker above is obsolete: #340's two-pass free-running driver
>   (breakpoint AFTER the sequence, tracing off) and #358's fold-fired marker channel
>   both post-date this paragraph — and #358 measured that the bare instruction-counter
>   route this paragraph proposed is by itself NOT a sufficient witness. Re-filed as:
>   REPRODUCIBLE NOW with the #340 driver + #358 markers; whether the C-flag divergence
>   is live remains UNMEASURED (nothing here claims the defect is fixed).
> - **`sxtab` and `sxtah` are not decoded at all** — the encodings `0x06a00070` and
>   `0x06b00070` appear nowhere in `cpu_arm_instr.c` (confirmed by a round-78 diff seat and
>   verified). #319 gave the UNSIGNED extend-and-add pair its rotation; the signed pair has
>   no handler in any form and has raised Undefined since #312. A missing instruction, not
>   a halt — the "half a family" shape again, and it belongs with the rest of the
>   unimplemented ARMv6 media set.
> - ~~**#320's PC carve-out survives for `rn == PC`**~~ — **RESOLVED as #322**, after four
>   of the five diff-review seats independently named it and one supplied the witness
>   (`tst pc, #4 ROR 2`, measured leaving the carry set where the architecture clears it).
>   The stated reason for leaving it — that a cold handler could not reach the PC+8
>   reconstruction — was false; it needs only `ic`, `cur_ic_page` and `cpu->pc`.
>   `rd == PC` remains excluded and correctly so: writing the PC with S set is an
>   exception return whose flags come from SPSR, so the carry there is overwritten
>   rather than lost.
> - ~~**ARM Thumb `add`/`sub` take Z from the untruncated 64-bit result**~~ — **RESOLVED as
>   #328 (round 77)**, and the entry was wrong in three ways worth recording. There were
>   **four** near-identical blocks, not three. Carry was **not** "correctly read from bit
>   32": subtracting zero produced no carry-out at all, so `cmp r0,#0` reported a borrow
>   that never happened. And a **third** flag was wrong that the entry never mentioned —
>   V came from the sign of the *negated* subtrahend, which fails at `0x80000000`, the one
>   value that is its own negation; it was inverted in both directions, and `x - x` at that
>   value claimed overflow. Only N was right, because it truncated first.
>
>   Reproduced first, as owed: Thumb is reached by an ARM `bx` to an odd address, and all
>   thirteen defect rows were measured failing on the committed build before any edit.
>   V is reachable only in the two REGISTER forms — imm3 and imm8 cannot encode
>   `0x80000000` — so that one defect was in two copies while Z and C were in four.
> - **The ARMv6 media encodings decode on every ARM model**, including the ARMv4 SA1110
>   this rig runs, where silicon would raise Undefined. Pre-existing fidelity gap rather
>   than a halt; deliberately not entangled with #312.
>
> **Round 71B — the non-ARM upstream candidates, triaged. Two refuted, one promoted.**
> - ~~**MIPS "early-store hazard"** (`cpu_mips.c`, the `store_32bit_word` to
>   `0xffffffff9fc00000` in `mips_cpu_new`)~~ — **REFUTED by measurement, no change.** The
>   worry was that a store issued at CPU-creation time lands before the machine has
>   installed RAM. Read back on the pmax rig, that address holds `0x00c0de0c` repeated
>   every 8 bytes — the DEC PROM emulation's own vectors — not the `0x00c0de0d` the CPU-init
>   store writes. So the store is not lost into a void; it is *overridden by
>   machine-specific initialisation*, which is precisely what the comment above it says
>   should happen. The mechanism is working as designed. Left open, and much weaker than the
>   original claim: whether the default ever survives on a machine that does NOT override it
>   (`testmips` did not construct in the configuration tried), which would make it a dead
>   default rather than a hazard.
> - ~~**m88k `PFAR`**~~ — **REFUTED as a defect: the register is not modelled at all.**
>   `PFAR` appears nowhere in `src/`. That is a missing feature, not a wrong behaviour, and
>   there is no reproducer to write for it.
> - ~~**SH `synco` (0x00ab) is undecoded and HALTS the emulator**~~ — **RESOLVED, much
>   wider than filed, as #314 (round 79).** The premise recorded here was wrong twice over:
>   `synco` is an SH-4A instruction and this tree models no SH-4A core (landisk is an
>   SH7751R), so a nop would have made an SH-4 execute an SH-4A instruction; and the claim
>   that `PREF` was "already a nop" was false — `pref_rn` is a store-queue writeback engine.
>   A sweep then found **eight** legal encodings halting, three of them BASE ISA (`MAC.L`,
>   `MAC.W`, `TST.B`, present since SH-1/SH-2 and legal on the modelled part). Fixed the way
>   #309 and #312 fixed their architectures: the ten unimplemented-opcode `goto bad` sites
>   now decode to `instr(reserved)` and raise the illegal-instruction exception at EXECUTE
>   time. Eight of eight halted before, none after.
> - **Legal SH encodings that no longer halt but are still UNIMPLEMENTED** (they now raise
>   the exception, which is honest, but the instructions are absent): `ICBI`, `MOVLI.L`,
>   `MOVCO.L`, the `SGR` and `DBR` load/store forms, and `FPCHG`. `MOVLI.L`/`MOVCO.L` are
>   the guest's atomics and must be implemented rather than nopped if anything ever needs
>   them.
> - ~~**Four legal SH-4 sequences reach `ABORT_EXECUTION`**~~ — **three RESOLVED as #315/#316
>   (round 80)**, and they were worse than filed: two of them did not stop the emulator at
>   all, they called `exit()` and killed the gxemul process. `fmov drM,@rN` with SZ=1 exited
>   the host for HALF of all rN, because the odd-register check read its parity from the
>   address register instead of the floating-point one. `fneg`/`fabs` with an odd field under
>   PR=1 exited too. Also fixed in passing: the register-pair alignment class (8 bytes, asked
>   for 4), a second word that was never byte-swapped, and — a prerequisite the panel found —
>   `sh_exception` had no case for EITHER delay-slot event, so `trapa` in a delay slot and an
>   FP instruction in a delay slot with FD=1 both killed the process. Lazy-FPU kernels run
>   user code with FD=1, so that one is plausibly reachable by a real guest.
> - **[2026-08-22, #454: the load/store conclusion in the next bullet is REVERSED. It
>   credits "the manual's own evidence" for a WRITE classification; no SH manual existed
>   in this tree until 2026-08-22, and the real 4.7.4 says the PREF transfer is READ
>   type. The `EXPEVT_ADDR_ERR_ST` in the "Adjacent store-queue model gaps" bullet below
>   inherits the same presumption and owes the `_LD` form. The composition witness and
>   the [25:6] withdrawal both STAND. See the Round 454 CHANGELOG block, `sh4sqwrite`
>   and `sh4sqexpevt`.]**
> - ~~**The store-queue prefetch with the MMU on STILL HALTS**~~ — **RESOLVED as #318
>   (round 81)** via a dedicated entry point, `sh_translate_sq_v2p`, since the general one
>   deliberately maps the range identically and must keep doing so for ordinary queue-filling
>   stores. The load/store question two rounds could not settle was decided on the manual's
>   own evidence rather than by count: an SQ page's UTLB entry keeps the `D` bit meaningful
>   while `C` and `WT` are explicitly meaningless, and `D` is consulted only on a write. The
>   dissenting reading came from the manual's *plain* `PREF` description — the sentence quoted
>   in the comment above that very handler — which is true of every other address range.
>   Measured with a composition witness, not just survival: operand `0xE00000E7` lands at
>   page + `0xE0`, proving `[9:5]` carried and `[4:0]` zeroed.
> - **The `SQMD` user-access check is still wrong in three ways** (round 81 deferred it,
>   deliberately): it raises reserved-instruction where hardware raises a data address error,
>   it is gated on `AT=1` though the rule is not, and ordinary queue-filling stores skip UTLB
>   validation altogether. Two seats wanted it folded into #318 and two did not — and they
>   disagreed on the correct event code, which is the argument for a round that can measure
>   it. Needs a user-mode witness, which does not exist yet.
> - ~~**SH `MOVCA.L` is decoded as a nop but architecturally STORES R0 to `@Rn`**~~ —
>   **RESOLVED as #317**: it decodes to the existing longword store, which has the same
>   alignment class and exception behaviour.
> - **Adjacent store-queue model gaps** (same function, same audit, not fixed): the SQMD
>   user-access check raises reserved-instruction where hardware raises an address error
>   (`EXPEVT_ADDR_ERR_ST`, which `sh_exception` already implements) and is only consulted
>   when AT=1, though the manual's SQMD rule is not AT-conditioned — so with AT=0, SQMD=1
>   and a user-mode guest, the flush proceeds where hardware would fault; queue-filling
>   stores under AT=1 take the identity map and skip UTLB judgment entirely, where real
>   hardware exception-judges SQ-area writes too; and UTLB multiple-hit detection is
>   unimplemented.
>
>   **Correction, 2026-08-01 (retrospective review of round 81).** This entry used to add
>   that "the identity mapping ignores address bits [25:6], so a guest filling a queue
>   through a non-zero offset stores where the flush will not read it." That is **not
>   true**, and it was a bug report against correct behaviour. `memory_sh.c:301` passes the
>   **full** vaddr through, and the SQ device wraps with `% sizeof(d->sq)` (`dev_sh4.c:952`),
>   so bits [5:0] — the queue select and the offset within it — survive intact. An aliased
>   fill lands exactly where the flush reads, which is hardware's own don't-care treatment
>   of [25:6]. Removed rather than annotated in place, per this file's rule, but the
>   correction is recorded because a false entry in a bug list costs a future round the time
>   to re-derive it.
>
> **Known and deliberately not forced — each with the reason it stays**
> - **The SH FPU exception model does not exist**: no instruction sets any FPSCR cause
>   bit and no arithmetic trap is delivered. #297 made it observable (`STS FPSCR` after
>   `ftrc(+Inf)` reads V=0 where hardware reads 1). Not patched piecemeal, because a lone
>   V bit would imply the other flags work. OpenBSD leaves the enables clear at exec.
> - **MIPS FCSR exception flags** — deferral re-confirmed 4–0. The blockers are
>   structural: `ieee_float_value` carries a single `nan` flag (no qNaN/sNaN
>   discrimination, so V is uncomputable) and the stores return a bare value with no flag
>   channel. **New reopen condition:** #299/#300's residual machinery computes exact
>   inexactness as a byproduct, which makes the I flag nearly free and inverts the
>   original "I last" sketch.
> - **#300's accepted-nearest bands** — div/sqrt below a 2^-969 operand, mul below a
>   2^-969 product — are real divergences from IEEE, pinned as named gate vectors rather
>   than hidden. Closing them needs scaled residuals, not a threshold.
> - **SH `fsca` and `fsrra` stay on the truncating store**: transcendental
>   approximations where silicon deviates by roughly 2^-21, so no witness exists whose
>   correct answer is decided by `FPSCR.RM`. Untestable by this project's rule.
> - **#291 was a symptom fix**: 32 ARM CPU table entries still have an unpopulated
>   `dcache_shift`, `iway`/`dway` are ignored, and ARMv6 parts use a different cache-type
>   register format than the v4/v5 layout hardcoded for every CPU.
> - The console overrun's remaining two sites are **X11-only** and this project runs
>   headless; the SuperH `RDF` status bit is never set (patched and measured — it was not
>   the input-loss cause), and the SSR verbatim-write and FDR-width warts stand.
> - Items 4, 6, 7 and 9 of the rounds 41–46 block: LANCE `STP` on chained frames
>   (unreachable on both rigs), the Class-A diagnostic remainder, `dev_wdc.c`'s
>   guest-reachable `exit()` (out of scope), and the #182-shaped stale length on the
>   VGA's accepted mode paths.
> - **OB-22** (`dev_jazz.c:613` jazzio vector-read blanket deassert) — self-healing, and
>   a change there would touch the verified arc boot.

> ## ✅ 2026-07-30 — RESOLVED as #294: cvt.w honours the rounding mode (item 2 of the rounds 41–46 block)
> `cvt.w` of 3.5 under the default mode now yields 4 (nearest-even); `trunc.w` still
> truncates regardless of the mode, as the architecture requires — and the live probe
> proves both, on both rigs, under all four FCSR modes (32 rows, PROBE294_PASS). The
> panel-refuted proof (a computed remainder can equal 0.5 for a non-tie) and the repaired
> midpoint comparison, the mode-by-mode boundary table, and the non-discriminating
> +2147483647.5 case are all recorded in CHANGELOG "Fifty-ninth round". The related trap
> is now enforced by a mutation self-test: the W arm rounding under LEGACY is a mutant the
> gate must detect.

> ## 2026-07-30 — ✅ round.w / ceil.w / floor.w / cvt.l are not decoded → RESOLVED as #295
> **RESOLVED, and this entry is why the queue nearly funded the work twice.** All six of
> `round.w`/`round.l`, `ceil.w`/`ceil.l`, `floor.w`/`floor.l` are decoded with the correct
> forced modes, and `cvt.l` is decoded rounding per FCSR, which is right for that
> instruction. Shipped as **#295** in commit `e61badd` (round 60) — see
> `CHANGELOG.md`'s "#295" block. Verified three ways on 2026-08-11: the commit exists with
> that subject; the forced modes are live in the tree (`IEEE_RM_RN` for round, `IEEE_RM_RP`
> for ceil, `IEEE_RM_RM` for floor, and the constants at `src/core/float_emul.c` are
> 0/1/2/3 = nearest-even/zero/+Inf/−Inf, matching MIPS IV per-instruction pages B-85, B-44,
> B-57 and B-48); and `grep -rn "295\|round\.w" regress/` returns **nothing**, which is the
> separate real defect — see the 2026-08-11 entry below.
>
> **This entry read as OPEN for 47 rounds because it never got its resolution marker**,
> unlike its immediate neighbours which carry `✅ … RESOLVED as #294 / #292`. `CLAUDE.md`
> defines the live queue as the OPEN LIST head *plus the dated tail entries*, so an unmarked
> tail entry **is** the queue saying open. A stale `/* TODO: … ROUND.W … */` sitting 600
> lines above the implementation in the same source file made it believable. The lesson is
> not "read more carefully" — it is that a resolved entry must be marked at the moment it is
> resolved, and that `git log` plus a `grep` of `regress/` costs seconds before funding any
> round. Noted for the irony: #295's own CHANGELOG block records that it "came out of a
> backlog audit that found five of nine items in an older block had silently been fixed".
>
> Original text follows, kept because its reproduction recipe is still the right one for the
> detector that is now owed.
>
> Found by the #294 panel and verified by two seats independently. The COP1 dispatcher
> admits these by format, `fpu_function()` matches no function code (upstream's own TODO
> at ~:1056 lists exactly these opcodes), and the tail raises a Coprocessor-Unusable
> exception for CP1 **with CU1 already enabled** (`cpu_mips_coproc.c` ~:2373-2381). A BSD
> kernel answers CpU(1) by granting the FPU and retrying the same instruction — a retry
> livelock plus a host-log flood. Latent on both rigs: zero `UNIMPLEMENTED coproc1
> function` markers across green boots, and OpenBSD 2.2's base system does not emit these
> opcodes. With #294's forced-mode parameter the fix is three copies of the trunc.w decode
> block — `round.w` forces nearest, `ceil.w` toward-+Inf, `floor.w` toward--Inf — plus a
> decision about `cvt.l` (MIPS III; the ISA-gating question recorded under #290/#273
> applies). Directly testable with the #294 probe pattern: `round.w.d(2.5)=2`,
> `ceil.w.d(2.25)=3`, `floor.w.d(-2.25)=-3` under FCSR mode 1, proving the override.

> ## 2026-07-30 — #26 re-review (four seats, unanimous): the FCSR exception-flag defer STANDS after #292
> #292 thinned exactly one blocker — target-format rounding now exists, so the
> Overflow/Underflow/Inexact flags are computable in principle. Everything load-bearing is
> untouched, verified in-tree: the store has no channel to return flag events (an API
> change across five CPU families); `struct ieee_float_value` still carries a single `nan`
> flag, so signalling-NaN Invalid is undetectable; trap delivery does not exist (only
> `MIPS_FPU_EXCEPTION_UNIMPL` is ever raised, and the CTC1 enable-bit TODO stands);
> R3000 FCSR bit-identity (#246) still constrains; and the guest enables no FP traps and
> reads no sticky flags (the kernel zeroes FCSR on exec and after every FP trap), so the
> in-scope consumer count is zero. If a consumer ever appears, the panel's first slice is
> STICKY FLAGS ONLY — Z and O first (both cleanly detectable post-#292), V only after
> qNaN/sNaN discrimination exists, I last — R4000-gated, with no cause/trap semantics.

> ## ✅ 2026-07-30 — RESOLVED as #292: S-format round-to-nearest (was item 8 / "round 55 unblocked")
> Fixed via a mode-aware sibling `ieee_store_float_value_rm()`; the historical entry point
> is a bit-identical wrapper and only the MIPS store passes `FCSR & 3`. Measured before:
> 50.12% of in-range single-precision stores 1 ulp low. Measured after: 0 mismatches
> against the host's correctly-rounded oracle over ~10M finite inputs, and a live-rig probe
> shows `ctc1` RM=0 → `cvt.s.d(1/3)` = `0x3eaaaaab`, RM=1 → `0x3eaaaaaa` on both pmax and
> arc. See CHANGELOG "Fifty-seventh round". **Kept open under this entry, deliberately:**
> - ~~**SH FPSCR.RM is stored but decoded nowhere**~~ — **RESOLVED as #296** (round 61).
>   The blocker recorded here was "no live test until the landisk rig can run FP (its
>   ramdisk has no FP-capable tool)". That premise was wrong: no FP-capable *tool* is
>   needed, because the guest does not have to be booted at all. A cold debugger seeds the
>   registers, the guest executes one instruction and stores the result with its own
>   `fmov.s`, and the value is read back from memory. That is now gate 10, and it is how
>   the defect was reproduced before the fix.
> - ~~PPC `stfs` rounding is DISPUTED between panel seats~~ — **SETTLED 2026-07-30** from
>   Power ISA v3.0B Book I §4.6.3, quoted verbatim by a panel seat: `stfs` is a defined
>   bit-EXTRACTION (fraction truncated at bit 23; a denormalization band; no rounding, no
>   FPSCR.RN, "Special Registers Altered: None"); `frsp` is the rounding instruction. Do
>   NOT wire `stfs` to FPSCR.RN — that would move away from the architecture. The real
>   PPC defects found instead are listed in the at-a-glance section above.
> - ~~m88k models no rounding register at all~~ — **WRONG as recorded; see the
>   at-a-glance section above** (fcr file modeled and retained; live 1-ulp defect on
>   luna88k userland; queued as its own round).

> ## ✅ 2026-07-30 — RESOLVED as #293: the SuperH console input loss (2026-07-27 entry below)
> The mechanism was none of the recorded suspects: on landisk nothing claimed
> `machine->main_console_handle`, so handle 0 (polled each tick for CTRL-C) raced the
> SCIF's console handle for the same host stdin and stole whole lines —
> `console_charavail()` imports up to 100 bytes into whichever handle polls first. Fixed
> by the one-line claim `dev_dreamcast_maple.c` / `dev_luna88k.c` / `dev_vr41xx.c` already
> make; Dreamcast is unaffected (maple still overrides, it initialises later). Measured:
> 10/12 commands stolen before, 12/12 delivered after; a side-effect probe proved the
> stolen commands never executed. **Instrument warning kept for the next console mystery:**
> a global chars-in/chars-out counter pair balanced at 77/77 *while lines were being
> stolen*, because the debugger's exit-time drain of handle 0 evened the books — count
> per-handle or not at all. The never-set RDF status bit remains a modelling gap (patching
> it changed nothing here); the SSR verbatim-write and FDR-width warts are recorded in the
> round-58 panel record.

> ## ✅ 2026-07-29 — RESOLVED as #291 (see CHANGELOG "Fifty-sixth round")
> Fixed: an unspecified cache size now encodes as 0 and each field is masked to its own
> width. `rpi` goes from 1 sanitizer report to 0; `cats`, `netwinder`, `iq80321`, `iyonix`
> and `testarm` stay at 0; both trees rebuild 0/0. Worth keeping from the investigation:
> it affected **32** CPU table entries, not just `rpi`, and casting to unsigned would have
> silenced the sanitizer while leaving the register byte-identically corrupt.
>
> **2026-07-30 retroactive review (one seat) — the fix stands, and it is a SYMPTOM fix.**
> Per the ARM ARM, a size field of 0 means a **512-byte cache**, not "unspecified" — the
> real defect is that those 32 table entries in `arm_cpu_types.h` simply never had their
> `dcache_shift` populated. So the register is no longer undefined or corrupt, but it
> under-reports the D-cache on those CPUs. The only reader is the guest's
> `MRC p15,0,Rd,c0,c0,1`, and GXemul executes cache flushes as no-ops, so nothing a guest
> does changes — the visible effect is a wrong size in a guest kernel's boot messages.
> Follow-on candidates recorded, none taken up (all latent, none testable on the rigs):
> populate the 32 missing `dcache_shift` values from CPU datasheets; honour the table's
> `iway`/`dway` fields instead of the hardcoded 32-way/8-word constants; shifts above 16
> would silently wrap in the 3-bit field (no current entry exceeds 16); and ARMv6 parts
> (ARM1136) architecturally use a different cache-type register format than the v4/v5
> layout GXemul hardcodes for every CPU.

> ## 2026-07-29 — NARROWED: the console/keyboard overrun is X11-only, and mostly guarded
> The earlier entry (item 5 of the rounds 41–46 block) says three ring buffers share the
> "overrun discards the whole queue" shape, one fixed and two still broken. The *code
> pattern* is identical in all three, but two of them have **feeder-level guards the entry
> does not mention**, so the exposure is far narrower than it reads:
>
> * `console/console.c:311` — the site is unguarded, but `console_charavail()` refuses to
>   read when the FIFO has less than 101 bytes of room, and **that guard is upstream's**
>   (`git log -S roomLeftInFIFO` shows only the import commit). The stdin path therefore
>   cannot overrun. Bypassing callers: `x11.c` (42 sites), `debugger.c` (11),
>   `dev_ns16550.c`, `dev_vr41xx.c` (24).
> * `devices/dev_dc7085.c:109` — the site is unguarded, but `lk201.c:253` loops on
>   `space_available_in_queue()`, which reserves 20 slots, before feeding console input.
>   The bypasses are the X11 keyboard/mouse expansions (`lk201.c:135-148`, `199-203`,
>   `290-291`), each adding up to ~4 bytes per event unchecked — so an overrun needs more
>   than five X11 events between drains.
> * `devices/dev_pckbc.c:159` — already fixed by #288.
>
> **Net: the residual exposure on both remaining sites is X11-only.** This project runs its
> rigs headless, so the bug cannot be reproduced in our own configuration — which under
> "only change what we can test for" means it is not fixed here. Recorded so the next
> reader does not act on the older entry's wider framing.

> ## 2026-07-29 — (superseded, kept for the trail) undefined behaviour in the ARM cache-type register, on `rpi`
> **What's wrong.** `cpus/cpu_arm.c:144` builds the ARM cache-type register like this:
>
> ```c
> | ((cpu->cd.arm.cpu_type.dcache_shift - 9) << ARM_CACHETYPE_DSIZE_SHIFT)
> ```
>
> On the Raspberry Pi machine (`-E rpi`) `dcache_shift` is 0, so this shifts **−9** left,
> which is undefined behaviour in C. The same site is used for `icache_shift` two lines
> below.
>
> **How it was found.** Gate 9 (the AddressSanitizer machine sweep) reports it on *both*
> upstream 0.7.0 and this fork:
>
> ```
> cpu_arm.c:144:49: runtime error: left shift of negative value -9
> ```
>
> So it is **inherited from upstream, not introduced here** — one of only two machines in
> the whole sweep still dirty on both sides, against 13 where this fork already fixed the
> memory errors.
>
> **Why it wasn't fixed in this round.** The fork has touched `cpu_arm.c` (two lines), but
> not this site, and it is outside the pmax/arc priority scope. It is also *latent*: the
> register is documented in-source as "aren't used yet". The fix is the same pattern as
> corrections #24/#25 — compute in an unsigned type, or guard the subtraction so it cannot
> go negative — but per the project rule, it needs a test that reproduces the wrong
> behaviour first. Gate 9 already is that test, which makes this a well-scoped next round.


> ## 2026-07-27 — (superseded, kept for the trail) the SuperH console loses guest input non-deterministically
> **→ RESOLVED as #293 — see the ✅ entry at the top of this file. The mechanism was none
> of the suspects recorded below** (it was an unclaimed main console stealing lines before
> the serial port saw them), but the refuted-hypothesis measurements below are what made
> the real diagnosis fast, so they stay.
> Found while building the landisk rig for round 55's harness, and **not yet diagnosed** —
> recorded here with its measurement so a future round starts from evidence rather than
> from the symptom.
>
> **Symptom.** Driving OpenBSD 7.6 / landisk (`-E landisk -M 64 openbsd76-landisk-bsd.rd`)
> to the installer's `(S)hell` and then typing commands, individual commands vanish
> **whole**: no terminal echo, no output, no error. The shell is alive — a command sent
> moments later runs correctly and prints the right answer.
>
> **What it is not.** Three hypotheses were tested and refuted:
> - *Timing.* Adding a settle delay before each write, and raising the post-write wait from
>   8 s to 25 s, changed nothing.
> - *Line terminator.* Switching from `\r` to `\n` (what the long-standing pmax and arc
>   rigs use) improved matters but did not fix them.
> - *Input length.* One boot, ten `echo` commands of increasing length: the **15, 23 and
>   33** byte lines ran; the **9, 17, 27 and 41** byte lines were lost. Neither a length
>   ceiling nor a strict alternation. Roughly one write in three survives.
>
> Retrying a command up to six times still failed to land `$((6*7))` or `uname -m`
> reliably, and even a bare `echo` succeeded only sometimes.
>
> **Where to look.** `dev_scif.c` (the SH SCIF serial console) and the console host-glue in
> `core/console.c`. Rounds 26/27 (#251/#252) already found two real bugs in that glue — an
> output-flush bookkeeping error and a stdin-EOF freeze — so an input-side defect in the
> same area is plausible. The alternative is a receiver-ready/interrupt-timing issue in the
> SCIF model itself, where a byte written while the guest has not armed its receiver is
> dropped instead of held.
>
> **Why it was not chased in round 55.** The rig only needed a dependable boot gate, and
> `BOOT_REACHED` is 1 on every run, so the harness asserts the boot and the chip identity
> the guest's own PCI probe prints (`shpcic0 at mainbus0: HITACHI SH7751R`) and sends no
> input at all. That is honest coverage; this is a separate bug and deserves its own round.
> **Reproduce with** `regress/drive_guest.py` by giving the `landisk` rig a `steps` list.

> ## 2026-07-27 — (superseded, kept for the trail) Round 55: the harness UNBLOCKED an item that was dropped as un-testable
> **→ RESOLVED as #292 — see the ✅ entry at the top of this file.** This entry records the
> moment the obstacle turned out to be the instrument rather than the bug.
> **S-format round-to-nearest** (`core/float_emul.c` ~277: `ieee_store_float_value()` truncates to 23
> fraction bits, so single-precision inexact results are 1 ulp low — pre-existing, all ops, all five
> calling CPU families) was previously set aside as **un-testable**: exercising it live was thought to
> need hand-written single-precision assembly, because the OpenBSD 2.2 rig image has no working `cc`
> and gcc never emits the relevant instruction forms.
>
> **That reasoning was wrong, and round 55's `regress/diff_ieee_store.c` is the counter-example.**
> `ieee_store_float_value()` is a **pure function**, so it needs no guest at all: it can be
> differentialled offline over tens of millions of inputs in seconds, and — unlike the #287 overflow
> case, where the differential compared old against new — round-to-nearest has an **independent
> oracle** available. The host's own `(float)x` conversion *is* correctly-rounded IEEE-754, so the
> test is not "did the answer change" but "is the answer right", which is a strictly stronger claim
> than anything the project has been able to make about this function.
>
> The measurement to run first, per the standing "only change what we can test for" rule: sweep random
> doubles, compare `store(x, IEEE_FMT_S)` against the host `(float)` result, and count how many differ
> and by how much. If the 1-ulp-low characterization is right, the differential will show it directly
> and bound the blast radius before a line is edited. **Still un-fixed — this entry records that the
> obstacle was the instrument, not the bug.**
>
> Note the one thing the offline route does *not* cover, so it is not oversold: SH-4 resets to
> round-to-zero (established in round 51), so any rounding change must be FCSR/FPSCR-aware rather than
> unconditionally round-to-nearest. The differential can prove the arithmetic; it cannot by itself
> decide the per-architecture rounding-mode policy.

> ## 2026-07-26 — Rounds 41–46 (#271–#279): the backlog this batch DOCUMENTED rather than fixed
> Six rounds shipped **nine corrections** (#271–#279) across `devices/dev_vga.c`, `core/float_emul.c`,
> `devices/dev_le.c`, `devices/dev_asc.c` and `cpus/cpu_mips.c` — see CHANGELOG / REVIEW_FINDINGS
> "Forty-first" … "Forty-sixth round". Each round was gated on its own; the batch was then closed with a
> **holistic regression at HEAD `b38cc4f` built from committed source** (clean rebuild **0 warnings / 0 errors**
> both trees, 223 pmax / 224 arc objects; **pmax 15/15 + arc 13/13 → `uid=0(root)`**; log hygiene **0** for
> every string the batch touched; live pmax ping **3/3, 0 % loss**; in-guest `sprintf("%d", ±1e30)` →
> `+2147483647` both signs; all twelve per-correction probe rigs re-run on the final binaries, plus the
> `trunc.l` addendum; the #274 would-fire counter still **0** on both a healthy boot and a flood, byte-identical
> to the pre-change reading; 20/20 machines byte-identical to a pre-batch binary rebuilt from `be95418` on both
> trees; divergence set still exactly the five known files).
>
> **The items below were found and characterized during this batch and deliberately NOT fixed.** Each is
> recorded with the evidence a next round needs, so the backlog is a record rather than folklore. Line numbers
> are at HEAD `b38cc4f`; items 8 and 9 were added later and re-verified at HEAD `895af34`, which touches only
> `README.md` and this file, so every number in the block refers to the same source.
>
> **STATUS AS OF 2026-07-30 — five of the nine have since been dealt with; the items keep their original
> text as the historical record, each with a pointer:**
> - item 1 → partly resolved as **#290** (round 54: the ISA gate); the PS-arithmetic half is still open
> - item 2 → resolved as **#294** (round 59), and its round-to-nearest tail as **#292** (round 57)
> - item 3 → defer **re-confirmed 4–0** on 2026-07-30 (entry at the top of this file)
> - item 5 → the pckbc third fixed as **#288** (round 52); the rest narrowed to X11-only (2026-07-29 entry)
> - item 8 → resolved as **#287** (round 51)
> - items 4, 6, 7, 9 → still open, unchanged
>
> 1. **[→ partly resolved as #290, round 54: the ISA gate shipped; the PS-arithmetic half for
>    5Kc/5KE/SB1/SR7100 remains open]** **COP1 ISA-level routing — the best-scoped next-round candidate (fidelity, not hygiene).** An R4000 is
>    MIPS III, but `cpus/cpu_mips_instr.c:4991-4995` admits `COP1_FMT_PS` (along with S/D/W/L) to `cop1_slow`,
>    so `add.ps` **executes** on an R4000/R3000 and silently writes `fd = 0x00000000` instead of raising
>    **Reserved Instruction**. Measured in round 46: one `add.ps` produced 8.0 host lines and a zeroed `fd`,
>    identically on arc/R4000 and pmax/R3000A; only PS reaches `float_emul.c` at all — every *other* reserved
>    fmt hits the decoder's own `fatal()` + `goto bad` at `:5006-5008` (fmt 18 and fmt 23 controls: **0**
>    `float_emul` lines). **The constraint already established, and the reason this is not a one-line deletion:
>    `include/mips_cpu_types.h` DOES contain `isa_level == 64` CPUs that have FPUs — `5Kc` (:103), `5KE` (:104),
>    `SB1` (:111), `SR7100` (:112) — for which PS is architecturally plausible (MIPS64r1 defines it; r6 removes
>    it). So the routing cannot simply be deleted.** The fix has **two halves**: an ISA gate that raises RI below
>    MIPS-V, *and* the fact that `float_emul.c` models no PS arithmetic whatsoever, so gating alone would leave
>    those CPUs without a format they are entitled to. Whoever picks this up must decide both. Same family:
>    **`trunc.l` executes on an R3000A** although it is MIPS III and an R3010 would raise RI — measured in
>    round 42 and re-measured in this regression. That measurement has a trap worth keeping: the obvious
>    `sdc1` read-back of the result is itself a MIPS-II 64-bit store an R3000 does not have, so the RI it
>    raises is easily mistaken for the instruction under test faulting; reading `$f2`/`$f3` back with two
>    MIPS-I `swc1`s (`probe_273_pmax_l.py`) shows `trunc.l.d` really did run and returned the pinned values.
>    So the COP1 decoder does not enforce ISA level **anywhere**.
> 2. **[→ resolved as #294, round 59; the round-to-nearest tail as #292, round 57]**
>    **FP rounding mode — `cvt.w` truncates, and `FCSR.RM` is read nowhere.** `cvt.w` of `3.5` yields **3**
>    where the MIPS default rounding mode (RN, round-to-nearest-even) gives **4**; measured as a deliberate
>    control in the #273 probe, which carries both a rounding-*sensitive* case (`3.5`) and a rounding-*insensitive*
>    one (`3.25`) so this defect can never be confused with the conversion defect #273 fixed. A tree-wide grep
>    finds `MIPS_FPU_FCSR` touched **only** for the condition-code bits and the flush-to-zero bit
>    (`MIPS_FPU_FLUSH_BIT`, #246): the **rounding-mode field is never decoded anywhere**. **Record the trap:
>    `cvt.w` should honour `FCSR.RM`, but `trunc.w` is architecturally round-toward-zero *regardless* of RM, so
>    a future fix must NOT "fix" `trunc.w`.** That is not academic here — `cpu_mips_coproc.c` routes
>    `cvt.w.fmt` (`:1574`), `trunc.w.fmt` (`:1498`) and `trunc.l.fmt` (`:1485`) through the **same**
>    `FPU_OP_CVT` call with the same target format, so `cvt.w` and `trunc.w` are currently indistinguishable
>    downstream: honouring RM requires separating them first. Related and also unfixed: **S-format round-to-nearest** in `ieee_store_float_value()` (truncates the
>    fraction instead of rounding → single-precision results 1 ulp low), already recorded under round 28 and
>    still blocked on the same thing — gcc never emits the single-precision compares, so only hand-assembled
>    tests reach it.
> 3. **[→ defer re-confirmed 4–0 on 2026-07-30 after #292 — see the entry at the top of this file]**
>    **FCSR Invalid-flag signalling — still the documented deferred TODO.** #273 corrected only the *result* of
>    an invalid FP→integer conversion (the pinned `0x7fffffff` / `0x7fff…ffff`); the Invalid flag is still not
>    raised on these conversions, and the wider FCSR V/Z/O/U/I cause/flag maintenance + enabled-exception
>    trapping remains deferred for the reasons recorded under round 28 (needs qNaN/sNaN discrimination,
>    target-format rounding, R4000-gating so R3000 FCSR stays bit-identical per #246). Noted here because #273's
>    W bound was deliberately given slack that *would* matter only if Invalid signalling were added later.
> 4. **LANCE `STP` stamped on the last descriptor of a chained frame** (`devices/dev_le.c`): the end-of-packet
>    block clears `d->rx_middle_bit` at **`:604`** (and frees the frame), and the `STP` block at **`:610-611`**
>    then sets `LE_STP` *because* `rx_middle_bit` is clear — so the **last** descriptor of a chained frame is
>    stamped `STP` as well as `ENP`, and it carries the **whole frame length** in rmd3. A BSD driver reads that
>    as a complete single-buffer packet (`am7990_rint()` accepts only `STP|ENP` and otherwise prints "dropping
>    chained buffer"). **Pre-existing** (not introduced by #262 or #274) and **unreachable on both rigs** —
>    neither guest chains RX, which the #274 would-fire instrumentation measured directly (`rx_calls=14
>    frames=14` on a healthy boot + ping, `321/321` under flood, `la_extra_reject = 0` in both). Recorded so
>    that anyone who makes chaining reachable fixes this first.
> 5. **[→ the pckbc third fixed as #288, round 52; the remaining two narrowed to X11-only exposure on
>    2026-07-29 — see that entry — and left, since this project runs headless]**
>    **Console/keyboard FIFO overrun discards the WHOLE queue, not one byte.** Three ring buffers share one
>    shape — the producer advances/stores and *then* warns, leaving `head == tail`, which every consumer reads
>    as **EMPTY**: `console/console.c:306-315` (`console_makeavail`, `"console fifo overrun"`),
>    `devices/dev_dc7085.c:103-110` (`add_to_rx_queue`, `"rx_queue overrun!"`) and
>    `devices/dev_pckbc.c:129-137` (`pckbc_add_code`, `"queue overrun"` — this one advances the head, warns,
>    then stores at the new head). So an overrun does not drop the newest byte, it **silently discards every
>    byte already queued**. **Host-input-driven, not guest-driven** (it needs input arriving faster than the
>    guest drains it), which is why it is out of the guest→host charter and was not fixed in this batch; it is
>    also why the boot rigs never hit it (**0** occurrences of all three strings on the pmax and arc boot logs).
>    A fix would drop the incoming byte and keep the queue, not the other way round.
> 6. **The Class-A "ungated diagnostic a guest can repeat" remainder in the pmax/arc set.** Rounds 41/44/45/46
>    fixed the sites that were measured at 1.00+ host lines per guest access; these were **swept and left**:
>    - **MEASURED on the final binaries** (fresh boot logs, this regression — so these fire during an ordinary
>      healthy boot): `devices/dev_asc.c:406` `{ asc: data in, lenIn=%i lenIn2=%i }` — **1** hit on pmax, **5**
>      on arc; `devices/dev_fdc.c:75-78` `[ fdc: write to reg %i: … ]` (a **2+len-call** site: one `fatal()`
>      for the prefix, one per data byte, one for the closer; the read arm at `:71` is one call) — **2** hits on
>      arc, 0 on pmax; `devices/dev_pckbc.c:718`
>      `[ pckbc: TODO: hack for non-8242 … ]` — **1** hit on arc (this is the long-known pre-existing arc-log
>      line the hygiene greps whitelist). All other swept strings measured **0** on both logs:
>      `dev_pckbc.c:944` (`write to DATA`), `dev_jazz.c:199` (`dma not enabled?`) and `:207`
>      (`wrong direction?`), the `promemul/arcbios.c` escape-sequence loop (`:255-266`, one `fatal()` per byte
>      of an unimplemented sequence), the remaining `dev_le.c` register/SRAM write dumps (`:899-902`,
>      `:948-951`, `:964-968`), and `cpus/cpu_mips_coproc.c:1327` (`fpu_op(): unimplemented op`) / `:2365`
>      (`UNIMPLEMENTED coproc%i function`).
>    - **READ ONLY (static sweep — reachability reasoned from source, amplification not measured):** the
>      `dev_asc.c` tail — `:357`, `:369`, `:373`, `:396`, `:455` (a bare `printf("WARNING!!!!!!!!! BUG!!!!…")`),
>      `:487`, `:505`, `:579`, `:611`, `:648`, `:655`, `:760`, `:766`, `:780`. Two neighbours that a naive grep
>      would add are **compiled out** and are deliberately excluded: `:641` (`#ifdef MACH`) and `:943`
>      (`#if 0`).
>    None of these was reproduced test-first, so under the project rule ("only change what we can test for")
>    none was touched. The two that fire on a healthy boot (`asc: data in`, `fdc: write to reg`) are the
>    cheapest next targets **because they are already reproducible without a rig**; the rest need a trigger
>    designed first. Note the sweep's original line numbers were taken at `be95418` and rounds 43–44 have since
>    shifted them; the numbers above are re-located at HEAD `b38cc4f`.
> 7. **`devices/dev_wdc.c` guest-reachable `exit()` — out of scope, and stated precisely.** Four
>    guest-reachable `exit(1)` calls remain at **`:654`, `:669`, `:708`, `:730`**, and **`:708` fires on any
>    failed ATAPI command** (`WDC: ATAPI scsi error?`). **`machines/machine_pmax.c` does not instantiate the
>    device at all, and `machines/machine_arc.c`'s `device_add(machine, "wdc addr=0x900001f0, irq=38")` at
>    `:235` sits inside a `#if 0` (`:232`) whose body begins `Not yet.` (`:233`).** That precision matters: an
>    earlier, looser phrasing of this item said only "not instantiated", which was corrected during round 41 —
>    the `device_add` line *does* exist in `machine_arc.c`, it is simply compiled out. So the site is real and
>    the `exit()` is a genuine defect of the same class as #167/#240/#264/#271, but it is unreachable on either
>    rig and belongs to a tree-wide `fatal()`/`exit()` hygiene round rather than to the pmax/arc mandate.
> 8. **[→ resolved as #287, round 51 — CHANGELOG "Fifty-first round"]**
>    **S-format store: an overflow produces a NaN encoding where hardware gives ±Inf.** In
>    `core/float_emul.c`, `ieee_store_float_value()` (`:245`) reaches the shared S/D arm at `:309-310`, whose
>    `FP_NORMAL` case (`:330`) writes the fraction bits into `r` at `:354-360` and *then* **clamps** the biased
>    exponent at `:367-368` (`if (exponent >= ((int64_t)1 << n_exp)) exponent = ((int64_t)1 << n_exp) - 1;`)
>    and ORs it in at `:369` — **without clearing the fraction it has already written**. Exponent 255 with a
>    non-zero fraction is a **NaN** encoding. The `FP_INFINITE` arm two cases up (`:318-323`) holds the right
>    answer (`0x7f800000`) and is simply never reached, because the *double* being stored is finite; it is the
>    single-precision destination that overflows. Measured in this batch's class-B sweep: `1e40` →
>    **`0x7feb194f`**; a second seat independently measured `1e39` → **`0x7fbc143f`**, `1e300` →
>    **`0x7fbf21e4`** and `-1e300` → **`0xffbf21e4`**, where hardware gives `0x7f800000` / `0xff800000`. **All
>    four reproduce bit-for-bit** when the function's own arithmetic is replayed on host doubles, which also
>    pins the threshold: the clamp first fires at |x| ≥ 2^128 ≈ `3.4028e38`, just above `FLT_MAX` — `3.4e38`
>    still stores exactly (`0x7f7fc99e`, identical to a host `(float)` cast) while `3.5e38` already yields
>    `0x7f83a7c6`. (That is a re-derivation, not a live reading; an in-emulator measurement still wants a
>    hand-assembled `-V step` probe of the round-46 shape.) **The interaction that lets this survive #255 is
>    the part worth keeping:** the NaN canonicalizer #255 added (`cpus/cpu_mips_coproc.c:1123-1133`) gates on
>    `fpclassify(nf) == FP_NAN` at `:1128`, and `nf` is the *host double* result — `fpclassify(1e300)` is
>    `FP_NORMAL`, so the canonicalizer never fires and the bogus NaN reaches `fd` untouched.
>    **Reachable from ordinary guest FP code**, not only from hand-assembly: `cvt.s.d` of any double past the
>    threshold (`cpu_mips_coproc.c:1552`, `output_fmt = COP1_FMT_S`) and any `add.s` / `mul.s` / `div.s` whose
>    result overflows single precision (`:1392`, `:1416`, `:1428`, each passing `output_fmt = fmt`); all of them
>    reach `fpu_store_float_value()` (`:1105`) → `ieee_store_float_value()` (`:1121`). **Distinct from the
>    S-format round-to-nearest item in 2 above** — that one is a 1-ulp truncation of the fraction (the same
>    `:354-360` loop), this one produces the wrong *class* of value.
>    **The blast radius is wider than #273's, which is the reason it is recorded rather than fixed.** #273 was
>    confined to the MIPS-only W/L arm and said so; the S/D arm is shared. On the **store** side mips, m88k
>    (`cpu_m88k_instr.c`), ppc (`cpu_ppc_instr.c:2421`, `:2444`) and sh (`cpu_sh_instr.c`) all store S, and
>    alpha stores D (`cpu_alpha_instr.c` has zero `IEEE_FMT_S` references); `dev_pvr.c` touches the S arm on the
>    **interpret** side only (13 `ieee_interpret_float_value(…, IEEE_FMT_S)` calls, no stores). So this needs
>    the non-MIPS blast-radius gate #279 used, not a MIPS-only one.
>    **Fix shape one seat proposed, recorded because it is a better shape than three separate S-format
>    patches:** follow the **#254** precedent and route the S store to the host FPU — a single `(float)` cast
>    plus a `memcpy` into a `uint32_t` — which collapses **three** defects into one change: this one, the
>    round-to-nearest truncation (item 2), and the **underflow sign loss** at `:365-366` + `:372-373`, where a
>    value too small for single precision is clamped to exponent 0 and then `r = 0` discards the sign bit set at
>    `:312-313` (`-1e-40` stores as `0x00000000`, not `0x80000000`; same replay). On MIPS that third half is
>    partly masked — #246's guard at `cpu_mips_coproc.c:1115-1119` traps an S-format result below `FLT_MIN`
>    rather than storing it — but only on EXC4K parts and only while `FCSR.FS` is clear (`fpu_unimpl_trap()`
>    returns 0 for EXC3K at `:1091-1092`), and the other four families have no such guard at all.
> 9. **The #182-shaped stale length is still live on the VGA's *accepted* mode paths — latent, and deliberately
>    left.** In `devices/dev_vga.c` the geometry block that follows a mode change assigns `d->fb_size`
>    **unconditionally** in both arms — `:924-925` (charcell) and `:929-930` (graphics) — immediately after
>    calling `dev_fb_resize()` at `:921-923` / `:927-928`, which returns `void` and whose effect is never
>    checked. `dev_fb_resize()` (`devices/dev_fb.c:123`) has **five** early returns that leave the old buffer
>    and the old `d->framebuffer_size` in place: `:129-132` (`d == NULL`), `:134-142` (#184, a dimension < 10),
>    `:147-151` (#156, a dimension > 16384), `:153-157` (`bytes_per_line` overflow) and `:161-165` (total-size
>    overflow); the buffer and its length are updated only at `:189-190`, past all five. `fb_size` is then used
>    as a **write bound** at `dev_vga.c:381` (graphics redraw) and `:488` (text redraw), each gating a
>    `dev_fb_access(…, MEM_WRITE, d->fb)`. That is the same shape as **#182** — a length outliving the resize
>    that was supposed to change it — which was rated CRITICAL. **Two independent review seats found it.**
>    **It is NOT guest-reachable on pmax/arc, so it is latent, and the panel's explicit call was to document it
>    rather than expand round 41 into it:** #271 now `return`s at `:917`, before the block, on a rejected mode,
>    and all eleven accepted mode bytes are self-consistent — at the default `scaleup == 1`
>    (`machines/machine.c:91`) every accepted arm resizes to 640×400, 640×350 or 640×480, far inside
>    `dev_fb_resize()`'s [10, 16384] window, so no accepted mode can take an early return. The only route found
>    is host configuration rather than guest input: `-Y -26` or lower (`core/main.c:490-501`, and the same shape
>    in `core/emul_parse.c:545-547`) makes `scaleup > 25` and pushes a charcell width past 16384 — reasoned
>    from source, **not** exercised.
>    **Two qualifications, so the item is neither over- nor under-stated.** (a) A stale-too-large `fb_size`
>    would **not** overrun the host through these two sites: `dev_fb_access()` re-bounds every access against
>    `d->framebuffer_size` at `dev_fb.c:719-721` (the OB-1 end-span guard), so the observable consequence is
>    dropped or mis-shaped paint, not a write past the allocation. The *shape* is #182's; the severity is not,
>    and #182's own severity came from feeding the dyntrans fast-map (`core/memory.c:339`,
>    `memory_device_update_length()`), which this does not. (b) Noticed while verifying, and belonging to the
>    same fix: `d->fb_max_x` / `d->fb_max_y`, which supply the **stride** in both bounded expressions
>    (`:379-380`, `:486-487`), are assigned **only** in `dev_vga_init()` (`:1307-1311`) and are never
>    recomputed on a mode change — so after even a *successful* resize the address arithmetic still uses the
>    initial geometry while `fb_size` describes the new one. Whoever fixes the `fb_size` assignment should fix
>    that in the same pass.
>
> **Resolved by this batch — do not carry these forward:**
> - **"In-guest FP microtest blocked" (recorded under round 28) — RESOLVED for the paths that matter.** That
>   note assumed a future round would have to install a toolchain or inject a static MIPS binary, because the
>   OpenBSD 2.2 rig image has no working `cc`. Round 42 found the route with no compiler at all: `awk`'s
>   `printf`/`sprintf` **`%d`** casts a double to a C `long`, which on 32-bit MIPS is exactly the double→int
>   conversion, so `sprintf("%d", 1e30)` → **2147483647** and `sprintf("%d", -1e30)` → **+2147483647** proves
>   #273 end-to-end in ordinary compiled guest code (round 28's regression had already reached `div.d`/`sqrt.d`/
>   `c.lt.d` through plain `awk` arithmetic). Recorded with its trap: **`awk`'s `int()` does NOT exercise this
>   path** — it stays in floating point (`int(1e30)` prints `1.0000…e+30`, `int(3.9)` yields `4`), so a test
>   built on `int()` proves nothing. What remains genuinely blocked is only the **single-precision** S-format
>   work in item 2, which needs hand-assembled instructions gcc never emits.
> - The open question under #279 — whether the COP1 PS routing could simply be removed — is **answered** (item
>   1: no, `mips_cpu_types.h` has MIPS64 CPUs with FPUs), so it is no longer an open question, only an
>   unimplemented fix.
> - Older, and noticed while auditing this file for stale entries: the seventeenth/eighteenth-round blocks below
>   still list **"#185 `dev_asc.c` DATA_OUT `data_out_len==0` `exit(1)`"** as deferred. It was **resolved as
>   #264** (round 35) — the branch now `fatal()`s and returns 0, which the `NCRCMD_TRANS`/`NCRCMD_TRPAD` caller
>   converts into a guest-visible SCSI disconnect. Recorded here rather than by editing the historical blocks,
>   which are kept as the audit record.

> ## 2026-07-19 — Post-batch pmax/arc fidelity cluster: CONCLUDED (2 refuted, 2 un-testable, 2 left untriaged)
> After rounds 28-39 (#254-#268) a final pmax/arc fidelity cluster of 6 candidates was scoped under the rule
> **"only change what we can test for"** + a full 4-model panel per change. Outcome — **no further corrections
> made; the pmax/arc hardening is considered complete for this pass:**
> - **REFUTED by test-first** (details in the entry below): unaligned-ifetch TLBL-vs-AdEL (already correct via
>   #228) and arc VGA text-console char-drop (faithful differential repaint, mis-measured).
> - **Un-testable on the rigs → not changed** (per the rule): **S-format FP round-to-nearest**
>   (`core/float_emul.c:~277`, `ieee_store_float_value` truncates the fraction instead of round-to-nearest →
>   single-precision 1 ulp low) — reaching it needs hand-assembled single-precision ops (gcc never emits
>   c.olt.s/etc.; the rig image has no in-guest `cc`), AND the function is SHARED across alpha/m88k/mips/ppc/sh so
>   the blast radius exceeds pmax/arc; **arc partition LBA signed `int*512`** (`arcbios.c`, defeats the #168 bound
>   on a hostile partition table) — needs a crafted large-LBA partition image to exercise. Both remain genuine
>   pre-existing candidates; deferred until a test fixture exists.
> - **LEFT UNTRIAGED this pass** (low value, deferred): **OB-22** (`dev_jazz.c:613` jazzio vector-read blanket
>   `mips_irq_3` deassert without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQ) — latent
>   (the arc boot reaches 13/13 without hitting it, so a repro needs a crafted multi-IRQ sequence and the fix
>   would touch the verified arc boot); **NE2000 invalid-TX log-flood** (`dev_ne2000.c`, SEC-only) — cosmetic log
>   hygiene, gate the diagnostic if pursued. Neither triaged; recorded here so they aren't lost.

> ## 2026-07-19 — GXEMUL trueness candidates TEST-FIRST TRIAGED → both REFUTED (no change; "only change what we can test for")
> Two gxemul candidates were raised from the cross-arch trueness campaign, then reproduced test-first on the
> committed builds before any change. **Both NOT-REPRODUCED — neither is a real reachable bug; no fix made:**
> - **unaligned instruction-fetch exception class (TLBL vs AdEL) — ALREADY CORRECT.** Correction **#228** guards
>   all six register-indirect PC-setting sites (`cpu_mips_instr.c` 1343/1373/1396/1424/1462/1495: `if (pc & 3)
>   → EXCEPTION_ADEL`). Live test: pmax `jr ra`/`jalr` with ra=0x42424242 → `cause: ADEL (exccode 4)` on BOTH
>   R3000 and R4000. `jr`/`jalr` are the only genuine MIPS instructions that can produce an unaligned PC (j/branch
>   targets are word-aligned by encoding), so the reachable path is fully covered. The residual TLBL appears ONLY
>   when `pc` is *forced* unaligned in the debugger (non-instruction) — present identically on R3000 AND R4000, so
>   not R3000-specific and not guest-reachable. The trueness note's "R3000 TLBL" was that debugger artifact.
> - **arc VGA text-console character-drop — FAITHFUL differential repaint, not a drop.** `vga_update_textmode`
>   (`dev_vga.c:276`) emits `ESC[y;xH`+char only for cells that CHANGED vs `charcells_outputed`, and never emits
>   `\n` — correct for a persistent 2D ANSI terminal / the real VGA screen. Live test: a 25-line rapid burst
>   renders all visible lines + `FINALMARKER…DONE` byte-perfect on a faithful 2D render. The campaign's
>   `BOUND`→`BOUN` was a LINEARIZATION artifact (ANSI-stripping the paint stream without a terminal model makes
>   skipped-because-unchanged cells look dropped) plus an INVALID test (arc root shell is `csh`; the burst used
>   `sh` `while`/`$((…))` → "Illegal variable name"). `console_putchar` writes every byte with the #251 flush
>   guarantee — nothing is lost at the console layer.
> Test scripts (scratchpad): `itemA_pmax.py`/`itemA_pmax_jalr.py`/`itemA_arc.py`, `itemB3_arc.sh`/`itemB3_parse.py`.
> (Latent/optional, NOT live bugs: the generic-fetch-path TLBL divergence is arch-neutral + debugger-only-reachable.)
> Already-resolved trueness items (NOT open): **L12** serial-drop → #251; **L5** pty/forkpty hang → #252; **L13**
> UDP-inetd handoff → dispositioned (userspace-NAT topology, reachable via tap **#253**). Inherent GAPs (not
> fixable without a rewrite): **L1** not-cycle-accurate; **L7** FP/uninitialized-memory lowest-confidence (FP
> largely #254/#255; uninit zero-fill #244). **[FAITHFUL]** L2 strict-alignment + LE endianness are correct
> reproductions — do NOT touch. All the trueness doc's #5–#23 items are [FAITHFUL] gxemul reproductions
> (they *confirm* fidelity), not emulator defects.

> ## 2026-07-18 — Twenty-eighth round (#254, #255): MIPS FPU result-correctness (4-model panel)
> Item #1 of the 8-item TODO-triage batch. Applied **#254** (div/sqrt/compare result bugs in `fpu_op`) + **#255**
> (NaN → legacy-MIPS quiet-NaN canonicalization), 4-model-panel designed+reviewed (Codex xhigh + agy + Fable +
> Ollama), build 0/0 both, pmax 15/15 + arc 13/13 boot, host-side FP-logic microtest 11/11 (rig image lacks an
> in-guest compiler).
> **DEFERRED (own future corrections, documented):**
> - **FCSR V/Z/O/U/I cause/flag maintenance + enabled-exception trapping** — needs qNaN/sNaN discrimination (`struct
>   ieee_float_value` keeps only one `nan` flag), target-format rounding for O/U/I, R4000-gating (R3000 FCSR must
>   stay bit-identical per #246), and the CTC1-writes-enabled-cause TODO (`cpu_mips_coproc.c` ~2216). ~0 benefit for
>   OpenBSD 2.2 (no FP traps enabled); medium-high risk. Panel unanimous DEFER.
> - **S-format round-to-nearest** in `ieee_store_float_value` (`float_emul.c` ~277 truncates to 23 fraction bits →
>   single-precision inexact results 1 ulp low). Pre-existing, all ops; own correction.
>   **[→ resolved as #292, round 57; and the FCSR item above was re-confirmed deferred 4–0 on 2026-07-30]**
> - **In-guest FP microtest blocked** — the OpenBSD 2.2 rig image has no comp set / working `cc`; a future round
>   could install a toolchain or inject a static MIPS test binary to exercise c.olt/c.ole live (gcc never emits them,
>   so only hand-asm reaches those paths).

> ## 2026-07-18 — Twenty-seventh round (#253): Linux tun/tap enablement — L13 inbound now DELIVERABLE (Codex + Fable)
> Round 26 dispositioned L13 (inetd UDP `dgram/wait`) as "not an emulator bug — the userspace NAT has no
> unsolicited-inbound path; resolve via tap or an outbound hole-punch." A Codex `gpt-5.6-sol` + Fable panel enabled
> the tap path on Linux. **Applied + verified live:** **#253** `net/net_tap.c` `net_tap_init()` gains a
> `#if defined(__linux__)` branch opening `/dev/net/tun` + `ioctl(TUNSETIFF, IFF_TAP|IFF_NO_PI, ifr_name=tapdev)`
> (Linux tapdev = tap interface **name**; BSD `open(tapdev)` device-path unchanged in `#else`; shared FIONBIO/tail →
> non-Linux compiles byte-identical). Build 0/0 both trees; both NAT boot regressions still pass (pmax 15/15 + arc
> 13/13 → `uid=0(root)`, zero NAT-path impact since `net_tap_init` is only reached when `tapdev != NULL`). **Live
> proof (pmax rig):** `gxemul -e 3max -L tap0 -d 1:disk bsd.pmax` attaches (host `tap0` → `UP,LOWER_UP`); guest
> `ifconfig le0 10.0.0.10`; then host→guest **unsolicited** `ping` = 4/4 replies and a UDP datagram reached the guest
> kernel (ICMP port-unreachable) — the delivery the NAT structurally can't do.
> **=> The L13 class (unsolicited-inbound UDP services: inetd dgram/wait, portmap, photurisd) is now reachable via
> `-L tap0`.** Host setup: `ip tuntap add dev tap0 mode tap user $USER; ip addr add 10.0.0.1/8 dev tap0; ip link set
> tap0 up`. **Use the pmax rig** (arc/pica SONIC `dev_sn.c` is an RX/TX-less register stub; 3max LANCE `dev_le.c` is
> complete). Under WSL2 the tap is host↔guest only (VM net not bridged to the LAN) — sufficient for the proof. Header
> choice (`<net/if.h>`+`<linux/if_tun.h>`, not `<linux/if.h>`) resolved by test-compiling all three variants.

> ## 2026-07-18 — Twenty-sixth round (#251, #252): console host-glue fidelity (3-view panel)
> An OpenBSD 2.2 pmax/arc audit reported three "emulation-layer" bugs. A source-verified panel (Codex `gpt-5.6-sol`
> high + Fable + reviewer holistic pass, each `diff`-checked vs pristine `src/`) **converged** that the audit
> mis-attributed the subsystem in all three; the two real defects are in the shared host-console glue
> (`console/console.c`, byte-identical to stock 0.7.0). **Applied (both trees, build 0/0, pmax 15/15 + arc 13/13
> boot PASS, reproduced+fixed on the pmax rig):**
> - **#251** `console_putchar` cleared the stdout flush-pending flag on `'\n'` assuming libc line-flush — false
>   when stdout is a pipe/file (fully buffered), so newline-terminated bursts sit unflushed and are lost on
>   kill/wedge (the audit's "L12 serial drops output"). Always mark pending → `console_flush()` drains it. Not the
>   UART (DZ/ns16550 TX is lossless).
> - **#252** `console_charavail` drain loop spins forever on stdin EOF (`select`→readable, `read`→0), *inside a
>   device tick*, wedging the whole emulator (the audit's "L5 pty/forkpty hang"). `if (len < 1) break;`. Repro:
>   `gxemul -e 3max -d 1:disk bsd.pmax < /dev/null` froze at 0 bytes; post-fix boots to `root device?` like an
>   open-stdin control.
>
> **Triaged / DEFERRED / DO-NOT (documented — not applied):**
> - **L13 inetd UDP `dgram/wait` — NOT an emulator/device bug.** The userspace NAT (`net/net_ip.c` `net_ip_udp` /
>   `net_udp_rx_avail`) creates mappings only from guest-*outbound* traffic and has **no unsolicited-inbound path**;
>   an `inetd dgram wait` service waits on purely unsolicited inbound → never delivered (once `inetd`'s `select()`
>   is readable, the datagram is already in the guest socket buffer — nothing is lost in the fork+exec window). The
>   real axis is *solicited vs unsolicited*, not inetd-vs-standalone. Resolutions: tap networking
>   (`net/net_tap.c`, already implemented) or a one-datagram outbound "hole-punch" in the test — NOT a
>   `dev_le`/`dev_sn`/`net.c` change. True inbound port-forwarding = a new feature with new state/options, out of
>   the minimal-surgical ethos.
> - **L12 UART model — not a bug** (lossless; the ready-always TX status is a fidelity simplification, not a
>   data-loss source).
> - **`dev_jazz.c` R4030 `EXT_IMASK` IP3/4/6 namespace gating** — real interrupt-model issue in the *est/* copy
>   (ANDs CPU-IP funnel enables directly against Jazz device-line bits, arc-only). **SEC's `dev_jazz.c` already
>   carries the corrected split** (the SEC-only jazz boot-enablement layer the arc rig runs), and pmax has no
>   jazzio — so it affects neither rig and is not the L5 hang. Companion **OB-22** (`dev_jazz.c` vector-read
>   blanket deassert) stays deferred (self-healing; would touch the verified arc boot).
> - Minor `console/console.c` residual (not applied, low value): `d_avail()` retries *all* `select()` errors as if
>   `EINTR` (incl. `EBADF`); could tighten to `errno==EINTR` only. #252's `break` already resolves the reachable
>   (EOF) freeze.

> ## 2026-07-17 — Twenty-fifth round (#248, #250): debugger QoL for the audit (4-model panel)
> Scoped the author's `doc/TODO.html` for **debuggability** wins for the OpenBSD 2.2 pmax/arc audit. A **4-model
> panel** (Codex `gpt-5.6-sol` + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`; Fable seat down on
> credits) reviewed the verified-undone candidates. **Applied (both trees, build 0/0, pmax+arc boot + live feature
> verification):** **#248** breakpoint hit-counts + "run N then break" (`breakpoint add addr[, N]`, counts on
> `show`/CTRL-T); **#250** data write-watchpoints (`watchpoint add addr[, len]` → break on guest store, report
> writer pc/value; physical-address match via `host_store` suppression + early `memory_rw` check). Both opt-in and
> guest-invisible (single `n!=0` early-out when unset). See CHANGELOG / REVIEW_FINDINGS "Twenty-fifth round".
> **Already implemented — candidate withdrawn (recon before coding):**
> - **C3 disk fsync-on-write toggle → the shipped `-f` option** (`main.c` `case 'f'`, opts string, `usage()`).
>   Its tentative number **#249 is VOID / unconsumed.**
> - The rest of the panel's "already-done" set: `find`, `put s/z`, `step call`, `verbosity`, subsystem/`debugmsg`
>   breakpoints, prefix-abbrev subcmds, `tlbdump`, CTRL-T-while-single-stepping (all the #120–#128 author-TODO round).
> **Assessed, DEFERRED / DO-NOT (documented — not applied):**
> - **CTRL-T in the main emul (run) loop — DEFER (unanimous):** async stdin polling under `-x` is historically
>   fiddly and risks console regression, for mostly-observational value; subsystem breakpoints + halt cover the need.
> - **PC / execution statistics (profil-style coverage) — DO-NOT (unanimous):** hot-path per-instruction counters
>   are a fuzzer feature, out of the accuracy-or-debuggability charter and against the minimal-changes ethos.
> - **Watchpoint limitations (documented, by design):** matches on physical addresses (so it needs the typed vaddr
>   to be translatable at add-time — trivial for kseg0/kseg1, needs a mapped TLB entry for kseg2/kuseg); write-only
>   (no read watchpoints); the shared expression parser doesn't accept bare register names (`r29`) — use literals.

> ## 2026-07-17 — Twenty-fourth round (#245–#246): debuggability logging + FPU denormal fidelity (5-model panel)
> A **5-model panel** (Codex `gpt-5.6-sol` + Fable + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`)
> reviewed the round-23 Part-B suggestions. **Applied:** #245 (C5) route the rounds-18–23 guest-reachable
> fault-conversion diagnostics (`dev_asc`/`dec_prom`/`arcbios`, 8 sites) through the verbosity-gated
> `debugmsg`/`ENOUGH_VERBOSITY` channel (`VERBOSITY_DEBUG`) so a guest/fuzzer can't flood the host log; #246 (C3)
> FPU denormals → real Unimplemented-Operation trap (FCSR cause E + `EXCEPTION_FPE`, no result written), **gated to
> EXC4K+ (arc)** — EXC3K/pmax bit-identical. Build 0/0, pmax+arc boot (trap active on arc, no misfire). See
> CHANGELOG "Twenty-fourth round". **Assessed, intentionally left (not bugs to force):**
> - **C1 (R3000 IsC cache) — already correct:** GXemul allocates real per-cache buffers (`cpu_mips.c`
>   `cache[i] = malloc(...)`) + `memory_cache_R3000()` routes isolated data accesses to them. Faithful already.
> - **C2 (R4000 TLB-Shutdown on overlap) — DO-NOT:** no machine-check delivery (`EXCEPTION_MCHECK` never raised, no
>   `STATUS_TS`/DS state); R4000 multiple-match is architecturally undefined (reset-latched wedge, not an
>   exception); MIPS32 ExcCode 24 would be anachronistic + panic-prone on OpenBSD 2.2; upstream's own duplicate
>   detector is `#if 0`'d as unreliable; first-match is a valid concretization of UNDEFINED. **#247 unconsumed.**
> - **C4 (R3000 delayed-IE / IRQ-in-delay-slot) — already correct where it matters:** the delay-slot
>   `Cause.BD`+`EPC=branch` signature is textbook; only the 1–2-instruction IE cycle-timing hazard is unmodeled and
>   nothing depends on it (functional emulator, no cycle timing).
> - Residual (deferred, low value): FCSR *flag* bits still never set; CTC1-written cause bits don't trap
>   (pre-existing TODO); the optional C2 write-time overlap **debug warning** (resurrect the `#if 0` block at
>   `cpu_mips_coproc.c` as a `debugmsg` — tooling, not fidelity) was left unimplemented.

> ## 2026-07-16 — Twenty-third round (#234–#244): guest-reachable host-halt tail → hardware-plausible faults
> A **Fable (source-verified) + agy** panel took the remaining guest-reachable **host-halt** tail of the Codex
> round-19 backlog (~13 candidates). **10 DO-NOW** (all MIPS/pmax/arc audit path) converted to the correct fault
> or graceful return: #234 failed ifetch `goto bad`→`return` (cf. #210); #235 `break 0x30378` reboot sentinel gated
> to the reset stub (phys `0x1fc00000`), else real BP; #236 reserved COP0 fn→RI; #237 COP0 STANDBY/SUSPEND/HIBERNATE
> → R4100 idle / else RI (was HIBERNATE `goto bad`, SUSPEND reboot-at-any-PC); #238 `memory_mips_v2p` supervisor/
> reserved KSU→TLB walk not `exit(1)`; #239 R3000 `tlbw*` under IsC→`return`; #240 `dev_asc` unimplemented cmd→
> deliver the ILL IRQ, no exit; #241 `dec_prom` unsupported services→`V0=-1`+return; #242 `arcbios` non-SGI private
> call / `0x888` / unimplemented vector→`V0=ARCBIOS_EINVAL`+return; #243 `diskimage_scsicmd` `malloc(0)`→`malloc(1)`;
> #244 `memory_rw` zero-fill the read buffer on a failed/`NO_EXCEPTIONS` translation (whole class; DEC-PROM uninit
> buf). Build 0/0, pmax+arc boot. See CHANGELOG "Twenty-third round". **Clears ~10 of the ~15 remaining Codex
> round-19 items; ~5 remain for #245+** (all off the MIPS audit path or verified unreachable there):
> **DEFERRED / NOT reachable on pmax/arc (documented — not bugs to force):**
> - **#10 PPC/ARM slow-path ifetch `exit`** (`cpu_ppc_instr.c` ifetch fail; `cpu_arm.c` `running=0`) — direct analog
>   of #234 but off the MIPS audit path; the PPC data side is already fixed (#216). Fix = `return`/RI when promoted.
> - **#11 PPC `MSR.IP` reboot hack** (`cpu_ppc.c`) and **#12 m88k CMMU / `dev_mb89352`** fatal errors — off-path.
> - **SPECIAL3 `RDHWR` selector halt + `HWREna` gate** (`cpu_mips_instr.c`): Fable verified SPECIAL3 is ISA-gated to
>   RI on R3000/R4000, so the halt is **unreachable** on pmax/arc (MIPS32r2-only). Cheap hardening for a future
>   round; no audit-path exposure.

> ## 2026-07-16 — Twenty-second round (#230–#233): MIPS fault-signature fidelity (FULL 4-model panel)
> A **full 4-model panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Ollama (`gpt-oss:20b`; the `480b-cloud` model
> returned HTTP 410) + Fable — fixed 4 fidelity items and DEFERRED 2. **FIXED:** #230 R3000 RFE KUo/IEo preserve
> (`~0x0f`); #231 ERET-on-R3000 → RI (decode-gate); #232 J/JAL region from the delay-slot PC `(branch+4)[31:28]`;
> #233 `mtc0`/`dmtc0` `cop0_availability_check` (writes only). Build 0/0, pmax+arc boot. See CHANGELOG
> "Twenty-second round". Clears 4 of the ~19 remaining Codex round-19 items; ~15 remain for #234+.
> **DEFERRED by the panel (documented — NOT bugs to force):**
> - **Privilege-transition fast-map bleed (Codex #17):** the dyntrans fast host-page map is not privilege-tagged,
>   so a kseg mapping cached in kernel mode can be hit by a later user access, bypassing AdEL/AdES (the slow
>   `memory_mips_v2p` path raises it correctly). The proposed invalidate-all-on-RFE/Status-write fix is a
>   non-starter — R3000 RFE fires on every syscall/interrupt/TLB-miss return, so a full invalidate there causes
>   continuous re-translation and would **hang the boot**; a Status-write-only hook misses R3000 RFE entirely
>   (RFE rotates Status directly in `X(rfe)`); the only correct+cheap fix is privilege-tagging the fast map = a
>   structural refactor the ethos forbids. agy+Fable ruled DEFER; Codex+Ollama conceded HIGH risk. Documented as
>   a known fast-map-vs-slow-path privilege-boundary fidelity limitation for the audit.
> - **#233 remainder:** the mfc0/dmfc0 READ-side availability check (side-effect-free fast paths), the
>   `rt==$zero`→nop fold, and the EXC3K user-mode-from-PC heuristic (in-code comment: forcing KUc "crashes
>   Linux") — invasive/risky for marginal reachability value; deferred.

> ## 2026-07-16 — Twenty-first round (#227–#229): fault-signature fidelity trio (multi-model panel, unanimous 3-0)
> A **multi-model advisory panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Fable (Ollama not installed on host) —
> unanimously (3-0) FIXED the three fault-signature-fidelity items promoted from the Codex round-19 backlog:
> **#227** `SWL/SWR` store pre-read mislabeled every fault as TLBS → map only load→store codes (TLBL→TLBS,
> AdEL→AdES; DBE/Mod correctly left alone); **#228** misaligned `jr`/`jalr` silently rounded down → raise AdEL
> (BadVAddr=EPC=rs, BD=0) in all 6 register-jump handlers; **#229** `mtc0 $8` `BadVAddr` → read-only. Build 0/0,
> pmax+arc boot. The panel resolved the earlier BadVAddr disagreement (Codex "fix" vs a prior Fable
> "Irix-compat/document-only") **3-0 to fix**, after Codex extracted the OpenBSD 2.2 kernel source and confirmed
> pmax/arc only `mfc0`-read CP0 $8 → no boot regression. See CHANGELOG "Twenty-first round".
> This clears **3 of the ~22 Codex round-19 backlog items**; ~19 remain for #230+ — the rest of the
> fault-signature fidelity set (`J/JAL` region from page-base not PC+4; R3000 `RFE` Status bits; `ERET`-on-R3000
> → RI; CP0 availability check; privilege-transition fast-map bleed) plus the guest-reachable host-halt tail
> (`goto bad`, `malloc(0)`, PPC/Thumb/m88k slow-path, dec_prom/arcbios unsupported-service, DEC-PROM uninit buf).

> ## 2026-07-16 — Twentieth round (#224–#226) + Codex round-19 backlog recorded
> Applied **3 HIGH MIPS-FPU memory-safety fixes** to both trees (build 0/0, pmax boots): #224 `ldc1`/`sdc1`
> `ft=31` → `reg[32]` OOB into `tlbs`; #225 `ldc1` uninitialised-`fpr` leak on a faulting load; #226 coproc
> paired-store `fd+1` sign-extension OOB. See CHANGELOG "Twentieth round".
> **Codex round-19 backlog — 22 items NOT yet applied (future rounds; full text saved in the session scratchpad
> `codex_round19.txt`, 2026-07-16):**
> - **HIGH (done this round):** Codex #23→#225, #24→#224, #25→#226.
> - **Fault-signature fidelity (recommended next — directly affects controlled-PC / BADVADDR trust):** misaligned
>   `JR/JALR` silently rounded down (should raise instruction-fetch AdEL with BadVAddr); `SWL/SWR` pre-read
>   rewrites every fault as TLBS (should preserve AdES/DBE); `mtc0`-writable `BadVAddr` (Codex: fix for
>   fault-signature auditing — Fable-B had called it Irix-compat/document-only, so reconcile); `J/JAL` region from
>   translated page base not `PC+4`; R3000 BEV=1 vector base `0xbfc00200` vs `0xbfc00100`; R3000 `RFE` Status bits;
>   `ERET` accepted on R3000 (should RI); CP0 availability check omitted; privilege-transition fast-map bleed
>   (stale kseg mapping bypasses AdEL/AdES after kernel→user).
> - **More guest-reachable host-halts:** `cpu_mips_instr` `goto bad`/BREAK-reboot-sentinel/RDHWR/SUSPEND;
>   `memory_mips_v2p` KSU=supervisor `exit(1)`; TLBWI/TLBWR under Status.IsC; `dev_asc` unsupported-command exit;
>   `dec_prom`/`arcbios` unsupported-firmware-service halts; `diskimage_scsicmd` `malloc(0)`→NULL→exit; PPC/Thumb
>   slow-path; PPC `MSR.IP` reboot hack; m88k CMMU / `dev_mb89352` protocol errors.
> - **Category 3:** `dec_prom` uninitialised `ch`/`buf` on a failed `NO_EXCEPTIONS` translation (silent
>   nondeterminism / unbounded string scan).

> ## 2026-07-16 — Nineteenth round (#210–#223): MIPS exception fidelity/debuggability + host-halt sweep
> Codex `gpt-5.6-sol`/ultra + a 2-agent Fable panel + per-site verification applied **14 corrections #210–#223**
> to both trees (build **0/0**, all tags matched, **pmax boot regression PASS**) — see CHANGELOG /
> REVIEW_FINDINGS "Nineteenth round". Highlights: #210 wire MIPS exceptions to the trappable `SUBSYS_EXCEPTION`
> breakpoint (catches controlled-PC-into-unmapped that `-p` can't reach); #211 AdEL/AdES no longer clobber
> Context/EntryHi (BadVAddr only, like silicon); #212 unaligned LL/SC → AdEL/AdES; #213/#214 CONFIG/ENTRYLO1;
> #215–#217 Alpha/PPC/SH host-crashes → guest faults; #218–#223 OF + footbridge/mp/kn02ba/8253 guest-reachable
> `exit(1)`s → graceful.
> **New deferred (broad device-exit tail):** the same untagged `fatal("…TODO/unimplemented…"); exit(1)` inside
> many other guest-writable `DEVICE_ACCESS` handlers persists (Fable-A's list: `dev_adb.c`, `dev_clmpcc.c`,
> `dev_igsfb.c`, `dev_lca.c`, `dev_m8820x.c`, the `dev_pcc2.c` remainder, `dev_mb8696x.c`, `dev_mvme187.c`,
> dreamcast gdrom/maple/g2, and `cpu_arm_coproc.c` CP15 writes 165/252/407/518). Each is guest-reachable when its
> machine is selected; extending the #118/#119 warn-once-and-continue pattern would close them — a future round.
> **Document-only (assessed, not bugs):** R3000 BEV=1 bootstrap-vector base (`0xbfc00200` vs `0xbfc00100`; off the
> fault window — OpenBSD clears BEV early); `mtc0`-writable `BADVADDR` (Irix compat); the SH `sh_exception()`
> default and the dyntrans `bad:` halt (both already emit a trappable SUBSYS message — an intentional
> "unimplemented" signal the maintainers want surfaced).

> ## 2026-07-16 — Eighteenth round (#188–#208): accuracy/debuggability pass (Codex 5.6-Sol-Ultra + Fable panel)
> A fresh full-tree Codex `gpt-5.6-sol`/ultra review (17 findings) + a 4-reviewer Fable panel + per-site
> verification, narrowed to **hardware-accuracy + debuggability + ethos** (not new hardening for its own sake),
> applied **21 corrections #188–#208** to both `est/` and `GXEMUL-SEC/` (build **0/0**, all 21 tags matched) —
> see CHANGELOG / REVIEW_FINDINGS "Eighteenth round". This **clears one deferred item below: the `dev_ram.c`
> MAP_FAILED-vs-NULL #175 straggler → now fixed as #208.** Highlights: R4000 invalid-PageMask host-`exit()`
> (#188 write-canonicalize / #189 translate-refill), `TLBWR` divide-by-zero (#190), DEC/ARC PROM `malloc` DoS
> (#191/#192), ARM/Alpha/m88k page-walk & signed-div host-crashes → guest faults (#193–#195), and Codex HIGH
> guest→host OOBs (#202 SII, #203 MEC, #204 flat-CD, #205 MODE SELECT, #207 PX copyspans).
> **Still deferred (unchanged):** #185 ASC DATA_OUT `exit(1)`; the four PVR render/texture-loop `exit(1)`s
> (868/1084/1245/1419); CUE symlink-follow; cross-memblock invalidation gap (#165); overlay write
> silent-success; Jazz `LB_IE` / dual-pending IRQ; ARC partition signed-`*512`; TCP-debug over-read; NE2000 TX
> log-flood.
> **New "not changed" (documented):** the MIPS `add/addi/sub` Integer-Overflow *trap* (`cpu_mips_instr.c`) —
> defined 2's-complement wrap in practice; a real trap is the hottest instruction path + boot-regression risk,
> so left per OB-24.

> ## 2026-07-10 — Cross-model re-review (Codex 5.6-Sol-Ultra + Fable panel): #182–#187 applied; deferred candidates
> A full-tree adversarial re-review (Codex `gpt-5.6-sol`/ultra, 17 findings, + a 4-reviewer Fable panel, each
> source-verified) fixed a **CRITICAL fb-resize stale-length OOB (#182)**, a HIGH X11 alloc overflow (#183), and the
> clean part of the guest-`exit(1)` cluster (#184 dev_fb, #186 mb89352, #187 eight dev_pvr MMIO sites) — see
> CHANGELOG / REVIEW_FINDINGS "Seventeenth round". Build 0/0 (gcc 15.2.1); applied to both `est/` and `GXEMUL-SEC/`.
> **Deferred candidates (recorded for a follow-up fix pass; not yet applied):**
> - **#185 `devices/dev_asc.c` DATA_OUT `data_out_len==0` `exit(1)` (med DoS):** reachable via `NCRCMD_TRPAD|DMA`
>   before a SELECT (TRPAD allocates `xferp`, so the #167 null-guard passes, then the DATA_OUT phase has len 0).
>   The fix needs a structural transfer-skip (wrap the ~40-line copy in `if (len != 0)`), so it is held for its own pass.
> - **`devices/dev_pvr.c` render/texture-loop `exit(1)`s (med DoS): lines 868 (texture pixelformat), 1084 (non-RGB565
>   render cfg), 1245, 1419 (unimplemented TA list-cmd).** Reachable via STARTRENDER; converting these safely needs
>   flood-free per-iteration recovery, unlike the simple MMIO-write fall-through used for #187.
> - **CUE symlink/junction bypass of #158 (`disk/diskimage.c`, med, host-side threat):** the #158 guard rejects only
>   *lexical* `..`/absolute paths; `fopen()` still follows a symlink/junction inside a caller-supplied CUE bundle.
>   Needs a caller-supplied disk image (host-side), not an untrusted guest — lower priority under the guest→host charter.
> - **Cross-memblock dyntrans invalidation gap in #165 (`cpus/memory_rw.c`, med):** a bulk RAM write spanning a
>   memblock boundary invalidates only the endpoint pages, so translated code in interior pages can go stale.
> - **Lower-severity Codex findings:** overlay write rejected-but-reported-GOOD (`diskimage.c`, silent data loss);
>   Jazz `LB_IE` not implemented + dual-pending-IRQ loss (`dev_jazz.c`); ARC partition LBA signed-`int *512` overflow
>   (`arcbios.c`, defeats the #168 bound); TCP-debug options over-read (`net_ip.c`, debug-verbosity only); NE2000
>   invalid-TX log-flood (`dev_ne2000.c`, SEC-only); one `dev_ram.c` `MAP_FAILED`-vs-NULL check (#175 straggler).

> ## ✅ 2026-06-28 — OB-35 RESOLVED (correction #117; build 0/0, Codex+agy APPROVE FOR COMMIT, regression-clean)
> Added a **7445/7455 CPU model** as a NEW, purely-additive macppc subtype **`-e g4plus`** (→ MPC7455, PVR
> 0x80010000) so the existing `-e g4` (MPC7400) and g3/g5 are unchanged and OpenBSD 3.4/macppc stays
> regression-safe. **Verified:** on `-e g4plus`, NetBSD 8.2/macppc sets HID0[HIGH_BAT_EN] → #116's extended
> BATs **engage** (gate-opened=1, confirmed via a temporary ppc_bat debug) → it advances past the BAT/MMU
> layer; on `-e g4` the gate stays closed. Files: `cpu_ppc.h` (cpu_type row), `machine.h`
> (MACHINE_MACPPC_G4PLUS=4), `machine_macppc.c` (CPU map + subtype). See CHANGELOG/REVIEW_FINDINGS
> "Eleventh round".
> - **Known residual (NOT a safety bug, pre-existing): macppc OpenFirmware is skeletal.** Past the MMU,
>   NetBSD 8.2/macppc stalls in GXemul's incomplete OpenFirmware (`machine_macppc.c` skeletal model + `of.c`
>   device-tree `getprop` gaps). Reaching a full NetBSD-8.2/macppc multiuser boot is open-ended OF/device
>   work beyond OB-35's CPU-model scope — left as a future enhancement, not tracked as an OOB/safety OB.


> ## ✅ 2026-06-28 — OB-27..34 RESOLVED (corrections #106–#113; build 0/0, pmax+arc regression-clean)
> All 8 deferred Phase-B/C candidates were Claude-verified (**all confirmed real**) and fixed — see
> CHANGELOG / REVIEW_FINDINGS "Eighth round". Map: OB-27→#106 (dev_fb from_x), OB-28→#108 (ps2_gif),
> OB-29→#107 (pvr span), OB-30→#109 + OB-31→#110 (iso9660), OB-32→#111 (bootblock n_blocks), OB-33→#112
> (diskimage %s), OB-34→#113 (SCSI CDB-length).
> ~~Still open: OB-25 / OB-26~~ → **now also RESOLVED: OB-25→#115 (mymkstemp unpredictable overlay temp
> names), OB-26→#114 (osiop skip data phase instead of exit(1)) — see "Ninth round". ALL OB-1..34 are now
> resolved.**

> ## 2026-06-28 — Phase-C deeper audit (3-agent fan-out): #101–#105 applied; 1 new candidate
> Agents swept network/NAT, SCSI/ATA storage, and the remaining devices + dyntrans. Claude verified +
> fixed 5 bugs (#101–#105, incl. 2 CRITICAL: dev_scc OOB heap write + net_arp heap overflow — see
> CHANGELOG / REVIEW_FINDINGS "Seventh round"). One candidate deferred:
> - **OB-34 `disk/diskimage_scsicmd.c` short-CDB over-read (med):** `diskimage_scsicommand()` only checks
>   `cmd_len >= 1`, then every opcode reads fixed CDB offsets (up to `cmd[8]`) — so a guest that submits a
>   short CDB (the SCSI/ATA controllers allocate `cmd[]` to the guest's byte count) causes an OOB read of
>   the host `cmd` buffer, influencing the computed LBA/transfer length. Fix with a per-opcode CDB-length
>   table (6/10/12/16) validated before the reads, under its own regression (touches every controller).

> ## 2026-06-28 — Phase-B new-surface audit (3-agent fan-out): #96–#100 applied; 7 new candidates
> Agents swept the PROMs (all CLEAN), the framebuffer renderers, and the disk parsers; Claude verified +
> fixed 5 bugs (#96–#100, incl. a CRITICAL ps2_gs OOB heap write and a HIGH Apple-partition stack
> over-read — see CHANGELOG / REVIEW_FINDINGS "Sixth round"). These further agent-found candidates are
> **not yet exact-fix-verified by Claude** (record for a follow-up fix pass):
> - **OB-27 `devices/dev_fb.c` `framebuffer_blockcopyfill` (high):** in copy mode the source column
>   `from_x` is not clipped (dst `x1/x2` and `from_y` are), so the `memmove` source over-reads the host
>   framebuffer; reachable from dev_ps2_gif blockcopy and dev_igsfb scroll → host-heap info leak.
> - **OB-28 `devices/dev_ps2_gif.c` TA-putchar (high):** pixel source offset `(24 + y*xsize)*4` uses
>   guest `xsize`/`ysize` (≤65535) with no check against the input `len` → large OOB read of the host DMA
>   buffer (also an `int addr` overflow).
> - **OB-29 `devices/dev_pvr.c:2438` (med):** the 24-bit `pvr_fb_tick` copy wraps only the start
>   `vram_ofs % VRAM_SIZE`, not the span → reads past the 8 MB VRAM; also signed `vram_ofs` can go
>   negative. Other pixelmodes wrap each access.
> - **OB-30 `disk/bootblock_iso9660.c:188` (med):** the root-directory walk reads the 8-byte record
>   header + up to 64 name bytes past `dirbuf` (guard only checks `dp < dirbuf+dirlen` at the top).
> - **OB-31 `disk/bootblock_iso9660.c:308` (med):** `if (i < len - strlen(filename))` underflows
>   `size_t` when `strlen(filename) > len`, defeating the bound → over-read.
> - **OB-32 `disk/bootblock.c` (low):** the bootblock/OSLoader size "WARNING" checks call `fatal()`,
>   which does NOT exit (debugmsg.c:334), so a disk-controlled `n_blocks*512` proceeds with int-overflow
>   UB → `malloc` abort (DoS). Make the checks `return`; use size_t math + an upper bound.
> - **OB-33 `disk/diskimage.c:321` (low):** `fatal("… type %i …", id, diskimage_types[type])` passes a
>   `char *` to `%i` (UB on the not-found path); use `%s`.

> ## 2026-06-28 — multi-model review (Codex + agy + Claude): #89–#94 applied; 2 new candidates
> A three-engine review (Codex `gpt-5.5`/xhigh, agy `Gemini 3.1 Pro`/High, Claude verification + a
> consensus rebuttal loop) of the full hardening diff fixed **6 confirmed bugs (#89–#94** — see
> `CHANGELOG.md` / `REVIEW_FINDINGS.md` "Fifth round") and **rejected 3 false positives** (both models
> conceded). **2 lower-severity items remain open:**
> - **OB-25 `disk/diskimage.c` temp-file TOCTOU (low, local-only).** #7/#20 create the overlay temp
>   files with `fopen "wx"` but then close and **reopen them by name** in `diskimage_add_overlay()`,
>   leaving a swap/symlink race window. Fix: `mkstemp()` + pass the fd; never reopen by name.
> - **OB-26 `devices/dev_osiop.c` guest-reachable `exit(1)` (low DoS).** The #10 NULL-`xferp` guard
>   calls `exit(1)` on a state a guest can drive (SCSI data phase, no active transfer) → a guest can
>   halt the emulator. Prefer aborting the phase (`break`) over killing the process. (Replaced a worse
>   null-deref, so not a regression — a hardening-quality improvement.)

> ## ✅ RESOLVED 2026-06-27 — see CHANGELOG.md "#70–#88"
> All 24 candidates below were triaged (Codex `gpt-5.5` *xhigh* proposals + independent source audit):
> - **19 fixed → corrections #70–#88** (builds 0/0; pmax + arc rigs re-verified):
>   OB-1 #70 · OB-2 #71 · OB-3 #72 · OB-6 #73 · OB-7 #74 · OB-8 #75 · OB-9 #76 · OB-11 #77 ·
>   OB-12 #78 · OB-13 #79 · OB-14 #80 · OB-15 #81 · OB-16 #82 · OB-17 #83 · OB-18 #84 · OB-19 #85 ·
>   OB-20 #86 · OB-21 #87 · OB-23 #88.
> - **3 false positives (not real)** — OB-4, OB-5, OB-10: `cpus/memory_rw.c:288` clamps `len` to the
>   device length before the handler runs, and these three are registered with length == backing size
>   and have no direct callers, so the "end-span" is unreachable.
> - **1 deferred** — OB-22 (jazz jazzio vector-ack): emulation correctness, not host-OOB;
>   medium-confidence; in the #69 arc interrupt path — deferred to avoid regressing the verified arc boot.
> - **1 skipped** — OB-24 (signed `byte<<24` in CPU instruction cores): UBSan-only, hottest path, no
>   reachability path; consistent with the pre-existing "intentionally left" decision (shared decoder fixed in #27).
>
> The per-finding analysis below is retained as the audit record.

---

Consolidated from two **read-only** Codex reviews (model `gpt-5.5`, effort `high` + `xhigh`)
on 2026-06-27, plus the manual audit. These are **static-analysis findings** — bounds/overflow
reasoning from reading the source; most are **not yet runtime-confirmed** (several need a specific
guest/board, e.g. Dreamcast, SGI, TURBOchannel framebuffers). They are candidates for the next
correction set (#70+). The 69 already-applied corrections are in `REVIEW_FINDINGS.md` / `CHANGELOG.md`
and are **not** repeated here. `src/` (pristine baseline) is untouched.

**Threat model:** the emulator runs untrusted guest OS images (device MMIO/DMA) and loads untrusted
executable files (loaders). HIGH = an untrusted guest or input file can cause a guest→**host**
memory-safety violation (OOB read/write of host memory). MED/LOW = host DoS / UB / device-state
corruption without a clear host-OOB path.

**Two dominant root patterns** (almost every HIGH below is one of these):
1. **End-span not checked.** An MMIO handler validates the *start* (`addr < size`) but then
   `memcpy`/indexes `len` bytes, so a 2/4/8-byte access at the last valid offset crosses the host
   buffer. Fix shape: require `addr + len <= size` (or clamp `len`).
2. **MMIO window larger than its backing array.** The registered device length exceeds the
   allocation, so high offsets index past it. Fix shape: bound the offset to the real backing size.

---

> ## STATUS OF THIS SECTION, re-verified against the source 2026-08-01
>
> **The tables below are the ORIGINAL audit listing and are largely historical.** Nineteen
> of the twenty-four entries have since been corrected and carry an `OB-N` marker comment
> at the fixed site: OB-1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 and
> 23. Treat a row below as closed unless it is named here.
>
> **OB-4, OB-5 and OB-10 are NOT DEFECTS — closed by round 84 after a full review, no
> source changed.** All three copy `len` bytes at `buffer + relative_addr` with no end
> check *in the handler*, which is why the original audit flagged them; but
> `memory_rw.c` clamps `len` to the device length before dispatching to any handler, so
> `relative_addr + len <= length` is guaranteed on entry. Adding the checks would have
> been three tests that can never fire — and worse than inert, since a handler returning
> 0 raises a guest bus error rather than doing nothing.
>
> **The rule, now stated so this does not get re-filed:** a handler reachable only
> through the memory layer relies on that central clamp. A handler that another handler
> calls DIRECTLY bypasses it and needs its own bound — which is exactly why OB-1
> (`dev_fb_access`, called straight from `dev_dec21030.c` and `dev_sgi_mardigras.c`) was
> a real defect and carries its own overflow-safe check. The three above are registered
> and never called directly; that was checked, not assumed.
>
> **A different shape the clamp does NOT cover:** "window larger than backing" (OB-2,
> OB-12, OB-15). The clamp bounds against the REGISTERED LENGTH, not the allocation, so
> a device registering a window bigger than its buffer satisfies the clamp and overruns
> anyway. Those three carry fix markers and are believed done — but that is the shape
> that genuinely needs a per-device check.
> - **OB-22** — left as recorded: self-healing, correctness-only.
> - **OB-24** — the residual signed `byte<<24` UB; real C UB that never reaches a host
>   pointer, size or index. Deliberately not chased (see the "Not changed" note).
>
> Two rows were checked by hand during that pass and are worth recording because the first
> reading of each was wrong: **OB-6** is fixed, and **OB-7** is fixed at the index-WRITE
> site (`idata & 0xff`), not at the data-write site where the indexing itself looks
> unguarded. Reading only the second site suggests a defect that is not there.

## High — guest → host OOB read/write

| ID | Site | Pattern | Trigger / impact |
|----|------|---------|------------------|
| OB-1 | `devices/dev_fb.c:646` (+ callers `dev_dec21030.c:135`, `dev_sgi_mardigras.c:200`) | end-span | `dev_fb_access()` checks `relative_addr >= framebuffer_size` only, then `memcpy(framebuffer+addr,…,len)` — wide access at last pixel → host fb heap OOB R/W |
| OB-2 | `devices/dev_px.c:608` | window>backing | PX SRAM MMIO window is 512 KB (`0x200000..0x27ffff`) but `sram[]` is 128 KB; offsets >`0x21ffff` corrupt host heap — any PX/PXG TURBOchannel guest |
| OB-3 | `devices/dev_px.c:315` (+`:414`,`:531`) | unchecked rows | PX STAMP DMA copyspans/fill/putchar use guest `span_src/span_dst` rows in fb pointer math with only `span_len` capped → fb heap OOB R/W |
| OB-4 | `devices/dev_pvr.c:2551` / `:2567` | end-span | `dev_pvr_vram_access()` copies to/from `vram+relative_addr` without `addr+len <= VRAM_SIZE` (distinct from the fixed #65/#68 render/texture paths) |
| OB-5 | `devices/dev_asc.c:778` / `:794` | end-span | ASC 128 KB DMA window: raw `memcpy(dma+addr,…,len)` with no end check |
| OB-6 | `devices/dev_adb.c:300` / `:305` | unbounded append | `output_buf[MAX_BUF=100]` appended via `output_buf[cur_output_offset++]=c` with no cap; guest toggles ACK in output mode → heap OOB write past `struct adb_data` |
| OB-7 | `devices/dev_igsfb.c:183` | unbounded index | DAC `palette_write_index` unclamped; `rgb_palette[index*3+sub]` past the 256-entry palette (start at 255) |
| OB-8 | `devices/dev_kn01.c:171` | unbounded index | KN01 VDAC overlay palette has 16 entries but `cur_write_addr_overlay` is raw guest data → `rgb_palette_overlay+3*addr` OOB |
| OB-9 | `devices/dev_sgi_mardigras.c:220` / `:224` | end-span | microcode-RAM MMIO validates `< MICROCODE_END` only, copies `len` → OOB past `microcode_ram` |
| OB-10 | `devices/dev_ether.c:82` / `:89` | end-span | test-ethernet `buf` MMIO copies to/from `buf+addr` with no end check |
| OB-11 | `devices/dev_pcc2.c:327` (+`:372`) | end-span | `relative_addr %= PCC2_SIZE` folds the *start* only; wide access near end of the 0x40-byte `pcctwo_reg[]` spans past it |
| OB-12 | `devices/dev_pmagja.c:111` | window>backing | PMAG-JA treats all `>=0x200000` as 8-bit pixels up to `0x3c0000`, but `pixeldata` is only 1280×1024 → OOB (and drives `dev_fb_access` out of range) |
| OB-13 | `devices/dev_sgi_gbe.c:706` | unmasked index | GBE palette store `selected_palette[color_index]` instead of `[color_index & 0xff]`; cmap 1..31 writes far past the 256-entry cache |
| OB-14 | `devices/dev_sgi_gbe.c:274` | stack over-read | tile convert: `fb_buf` sized for 512 px but guest partial-tile fields make `fb_len` up to 992 px → `dev_fb_access` copies past `fb_buf` (stack-byte leak into emulated fb) |
| OB-15 | `devices/dev_vga.c:607` | window>backing | VGA gfx window is fixed `0x18000` but `gfx_mem_size` is realloc'd per mode (e.g. 64,000 for mode 0x13) → access in-window but past `gfx_mem` → heap OOB |
| OB-16 | `devices/dev_vga.c:412` | unchecked index | VGA CRTC guest-programmed `base` (start hi/lo) added to every visible charcell index without `base+end` check → charcell heap OOB read on redraw |

## Medium — host DoS / overflow / device-state corruption

| ID | Site | Issue |
|----|------|-------|
| OB-17 | `devices/dev_dec21143.c:763` | TX descriptor chain: many non-`LS` descriptors → repeated `realloc(cur_tx_buf_len+bufsize)` (unbounded host alloc); `int cur_tx_buf_len` can wrap → alloc/copy size bug |
| OB-18 | `file/file_android.c:103` / `:146` / `:186` | file-controlled `page_size`: `==0` → divide-by-zero; very large → 32-bit page/seek overflow → crash/misload |
| OB-19 | `file/file_elf.c:94` (loop `:450`–`:482`) | PT_LOAD copy cursor `ofs` is `int` vs file-controlled `p_filesz` → signed overflow/UB on huge segments (chunk buffer itself is bounded) |
| OB-20 | `devices/dev_dreamcast_gdrom.c:183` (`:90`) | `READ_SECTORS` with `cnt==0` derives `cnt = 2048*sector_count` from guest bytes, then allocates it → guest-triggered host OOM/hard-exit |
| OB-21 | `devices/dev_dreamcast_g2.c:94` | EXTDMA maps `0x100` but `extdma_reg[]` is 0x80; offsets `0x90..0xbc` index `extdma_reg[>=36]` → C subobject OOB into adjacent `misc_reg` (device-state corruption) |
| OB-22 | `devices/dev_jazz.c:613` (`jazz_jazzio`) | **pre-existing, correctness only** (NOT a #69 regression): after reporting a vector it deasserts `mips_irq_3` without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQs until next edge/mask write |

## Low / reviewed

| ID | Site | Note |
|----|------|------|
| OB-23 | `devices/dev_sgi_re.c:1127` | MTE fill subtracts `sizeof(zerobuf)` from `dstlen` while writing only `fill_len` → mis-accounting → guest hang / wrong emulated writes (no host OOB observed) |
| OB-24 | `cpus/*` (e.g. `cpu_arm_instr_loadstore.c:297`; ARM/MIPS/PPC/m88k/PROM) | residual signed `byte<<24` UB; real C UB but does not feed host pointers/sizes/indices — sanitizer/portability cleanup, no reachability path found |

## Confirmed clean
- **#69 (arc Jazz interrupt-enable mask)** — both review passes independently found **no regression**:
  assert/deassert gate on `int_asserted & int_enable_mask`, `EXT_IMASK` recomputes IRQ3/6 on mask
  change, and masked pendings stay in `int_asserted` (delivered when later enabled).

## Suggested remediation order
1. **Window>backing (OB-2, OB-12, OB-15):** straight out-of-bounds host write from any access in-window;
   bound the offset to the real allocation size. Highest priority.
2. **End-span family (OB-1, OB-4, OB-5, OB-9, OB-10, OB-11):** add `addr+len <= size`; many share the
   `dev_fb_access` helper (fix once in OB-1 covers OB-1's direct callers).
3. **Unbounded index/append (OB-6, OB-7, OB-8, OB-13, OB-14, OB-16, OB-3):** clamp/mask the
   guest-controlled index; size the temp buffer to the max (OB-14).
4. **Loader/alloc (OB-17..OB-21):** reject `page_size==0`, cap aggregate/realloc sizes, widen `int`
   cursors to `off_t`/`size_t`, validate `cnt`.

> Generated read-only; no source was modified. Raw review transcripts:
> session scratchpad `codex_review.txt` (high) and `codex_review_xhigh.txt` (xhigh).
>
> **That last sentence is true only of the ORIGINAL audit pass.** Nineteen of these have
> been corrected in the source since, and the remediation order above is therefore stale as
> a work list — see the status block at the head of this section for what is actually left
> (OB-4, OB-10, and OB-5 pending re-location). Round 84 carries them.

> ## 2026-08-02 — round 85 (#57) partial: `fsrra`'s store settled, the rest still open
> **#339** records why `X(fsrra_frn)` uses the LEGACY store while its neighbours use the
> mode-aware one: FSRRA is an approximation instruction, specified only to a relative error
> bound, so there is no rounding mode for it to honour. That is now a comment in the source
> instead of a recurring re-file. **Everything else in round 85 remains open** — the
> unimplemented legal encodings, the missing SH FPU exception model (which #334 also
> depends on: DN=0 should raise an FPU error rather than deliver a value), and `fsca`'s
> store. None of those is a comment-sized change.

> ## 2026-08-03 — the free-running witness IS buildable; recipe recorded
> Round 83 was blocked because `cpu_dyntrans.c:1888` disables instruction combining under
> single-step and every probe in `regress/` drives the guest with `step`. Checked whether a
> breakpoint-and-continue harness can work instead. **It can**, and the one thing that
> looked fatal is not:
> - `single_step_breakpoint` appears in the SAME guard, but it is **transient, not a mode**:
>   set only when the PC equals a breakpoint address (`:1802-1823`) and cleared at `:1930`
>   after that one instruction executes and is marked for re-translation. It suppresses
>   combining for the instruction **at** the breakpoint, not globally.
> - `allow_instruction_combinations` already defaults to 1 (`machine.c:86`) and is a
>   registered runtime setting (`machine.c:109`). Nothing to turn on.
> - `breakpoint` and `continue` both exist (`debugger_cmds.c:2022`, `:2028`).
>
> **Recipe.** Put the breakpoint on an instruction AFTER the sequence under test, never on
> the sequence. Keep the pair in straight-line code within one page so the combiner sees
> `ic[-1]` at translation time. Drive with `continue`. **Do not enable instruction tracing**
> — `!cpu->machine->instruction_trace` is in the same guard, so a probe that switches on
> tracing to observe what happened disables the thing it is measuring. That is the identical
> failure mode as the five `step`-driven rows that passed green while measuring the
> standalone path; it is written down here rather than rediscovered.
>
> This unblocks round 83 (#55) and is the likely route for round 82's user-mode SH witness
> (#54) as well, since that one also needs real execution rather than stepped instructions.
> It also closes the wider hole: the whole combined-handler family (`cmps_*`, `teqs_*`,
> `tsts_*`, `netbsd_*`, `strlen`, `xchg`) is ungated today for exactly this reason.

> ### RESOLVED as #340 (round 83): the witness was built and the defect measured
> The two corrections below were both right, and together they made the witness buildable.
> See the round-83 block in CHANGELOG.md. Original notes kept:
>
> ### Correction: breakpoint-and-continue is NECESSARY but NOT SUFFICIENT
> Built the free-running driver described above and measured with it. The combined rows
> **still** read the standalone answer. The recipe was incomplete, and the missing piece is
> not about how execution is driven at all:
>
> `arm_combine_instructions` rewrites **`ic[-1].f`** — the PREVIOUS instruction — while the
> BRANCH is being translated. In straight-line code the `teq` has already executed by then.
> So the combined handler is reached only on a **second pass** over the same code; a single
> forward run cannot reach it no matter whether it is stepped, continued, or breakpointed.
>
> A working witness therefore needs the sequence inside a **loop** executed at least twice,
> publishing flags on the second iteration — with the breakpoint after the loop, still not
> on the pair, and tracing still off. The two facts recorded above (that
> `single_step_breakpoint` is transient and that `allow_instruction_combinations` defaults
> on) remain correct and are still prerequisites; they were just not the whole story.
>
> The rows were withdrawn rather than committed, for the second time in this file's
> history, and for the same reason: they passed green while measuring the wrong code path.
> That is now the strongest argument for building this witness properly — the defect has
> twice looked absent under instrumentation that could not see it.

> ## 2026-08-03 — three MORE combined handlers diverge in flags (found by #340's after-panel)
> #340 fixed the four `teqs`/`tsts` `*_samepage` handlers. A review seat then swept the rest
> of the family and found three that are **still** wrong, all pre-existing:
> - **`netbsd_cacheclean`** never writes flags at all, though the loop it replaces contains
>   a `subs` (`cpu_arm_instr.c:2067`, `:2072`). It also skips the loads, leaving r2 stale.
> - **`netbsd_cacheclean2`** skips its `subs` entirely (`:2087`, `:2093`) and leaves r0/r1
>   unchanged despite the ADD/SUB loop it stands in for.
> - **`netbsd_idle`** skips both TEQs on its fast paths without updating N/Z (`:2141`,
>   `:2172`); C/V happen to be right only because both immediates are zero. It also reads
>   rX into a local without writing the guest destination register.
>
> Two non-flag divergences in the same sweep: **`xchg`** has no `a != b` guard
> (`:2889`), so where standalone `eor r,r,r` would zero the register the folded form leaves
> it unchanged; and **`netbsd_memcpy`** bypasses its LDMs without publishing the final
> r3/r4/ip/lr.
>
> These are now MEASURABLE: #340 built the two-pass free-running probe driver that reaches
> folded handlers, which is what made the sweep worth doing. Verified equivalent and needing
> no work: all `cmps_*`, `tsts_lo_*` (after #340), `netbsd_memset`, `netbsd_scanc`,
> `netbsd_copyin/out`, `strlen`.

> ## 2026-08-03 — round 86 (#58) scoped accurately; the queue text was wrong
> The item said "32 table entries have no feature data". Measured against the tree, that is
> not the shape of the problem:
> - `ARM_CPU_TYPE_DEFS` has **51** entries (`src/include/arm_cpu_types.h:50`), not 32.
> - The `flags` field is not partly-filled — it holds exactly **three** bits, and they are
>   all it has ever held: `ARM_NO_MMU`, `ARM_DUAL_ENDIAN`, `ARM_XSCALE` (`:38-42`). There is
>   **no architecture-level field at all**. The file says so itself, twice:
>   `/* TODO: Include "ARM level", i.e. ARMv5 */` and `/* NOTE: Most of these are bogus! */`.
> - `cpu_type.flags` is read in exactly **three** places tree-wide — `cpu_arm.c:178`,
>   `cpu_arm.c:498`, `memory_arm.c:198` — and every one is XScale coprocessor/cache/memory
>   behaviour. **No instruction-decode path consults the CPU model at all**, which is why a
>   v6 media encoding decodes happily on an ARMv4: nothing is gating it, rather than a table
>   row being blank.
>
> So the real round is: add an architecture-level to the struct, populate it correctly for
> all 51 models from ARM's own documentation, and then gate the decoder on it. Populating it
> WRONG would be worse than leaving it — a model marked too high silently permits encodings
> that should trap, and too low breaks working guests — so this needs per-model primary
> sources, not inference from the names. Scoped, not started.

> ## 2026-08-03 — round 82 (#54): the "no user-mode witness" blocker is FALSE
> This item was parked on "needs a user-mode witness, which does not exist yet", and round
> 81's note recorded that debugger writes do not reach SR's mode fields. That is true of
> `sr` and it is the wrong register to write.
>
> **`rte` performs the transition architecturally**: `cpu_sh_instr.c:2767` calls
> `sh_update_sr(cpu, cpu->cd.sh.ssr)`, which applies MD and performs the r0-r7 bank swap —
> precisely what a kernel returning to user code does. So the witness is: debugger-write
> **`ssr`** with MD clear and **`spc`** to the user code address, plant `rte` plus its delay
> slot, and run. No SR write is involved and none is needed.
>
> Combined with #340's free-running two-pass driver, the remaining pieces are ordinary:
> set MMUCR.SQMD through the MMIO window (round 81's probe already writes MMUCR), plant a
> handler at the exception vector to publish EXPEVT and TEA, breakpoint after it, tracing
> off. The event-code dispute recorded above (ADDR_ERR_LD vs ADDR_ERR_ST) is exactly what
> such a probe settles by measurement instead of by argument — which is why it was left
> open rather than guessed.
>
> Scoped and unblocked; not built. The three code defects are unchanged: the check raises
> reserved-instruction where hardware raises a data address error, it is nested inside the
> `AT=1` branch though the rule is not conditioned on address translation, and the
> queue-FILL path (`memory_sh.c:298-303`) has no privilege check at all.

> ## 2026-08-03 — #341: dev_wdc's ATAPI read accounted for bytes it never delivered
> Found by #337's review sweep, and it is the READ-side twin of #338. The data-register
> read consumes one byte, two if `len >= 2`, four only if `len == 4` — so a 3- or 8-byte
> access consumes 1 or 2 — but the accounting used the REQUESTED `len`:
> `d->atapi_len -= len; d->atapi_received += len;`. For `len == 8` that subtracts 8 for 2
> bytes delivered, which lets `atapi_len` step PAST zero; its `== 0` test then never
> matches, `PHASE_COMPLETED` never fires, and the guest is told a transfer is further along
> than the data it actually got. Fixed to account for what was consumed.
>
> Same class as #283 (ASC) and #338 (mb89352): **the count reported has to be the count
> that happened.** Reachability-argued rather than rig-measured, like #337 — the landisk
> ATAPI witness is still its own round, and no gate row asserts this yet.
>
> **Still open from the same sweep**, none of them mine and all now measurable with #340's
> free-running driver: `netbsd_cacheclean` and `netbsd_cacheclean2` skip their `subs` flag
> updates entirely; `netbsd_idle` skips both TEQs without updating N/Z and never writes its
> guest destination register; `xchg` has no `a != b` guard, so where standalone
> `eor r,r,r` zeroes a register the folded form leaves it unchanged; `netbsd_memcpy`
> bypasses its LDMs without publishing the final r3/r4/ip/lr. On the PowerPC side:
> `fmadd`/`fmsub` raise none of their exception causes, `fnmadd`/`fnmsub` are undecoded and
> halt, and `NI` is defined but never consumed.


> ## 2026-08-05 — #342 resolves the `xchg` entry above
> The XOR-swap fold had no `a != b` guard. With one register the three encodings are
> `eor rX,rX,rX` three times over, each of which ZEROES rX, while `X(xchg)` exchanges rX
> with itself and leaves it unchanged. Measured on the committed build with #340's two-pass
> free-running driver: **0x5a where the architecture owes 0**. That byte is the row's own
> proof that the fold occurred — three standalone EORs cannot leave a nonzero value — which
> matters because this project has twice shipped combiner rows that were silently measuring
> the standalone path instead.
>
> **The other combined-handler entries above still stand**, and all four remain measurable
> with the same driver: `netbsd_cacheclean` and `netbsd_cacheclean2` skip their `subs` flag
> updates entirely, `netbsd_idle` skips both TEQs without updating N/Z and never writes its
> guest destination register, and `netbsd_memcpy` bypasses its LDMs without publishing the
> final r3/r4/ip/lr. Those four are harder than `xchg` was: each needs the exact NetBSD
> instruction sequence its combiner matches, reconstructed from the match conditions, before
> a row can be written at all.

> ## 2026-08-05 — netbsd_cacheclean2 is worse than its sibling, and #345 did not touch it
> **RESOLVED as #347** (see the entry at the end of this file). Both halves are fixed: the
> matcher now pins the add's base to r0 and the subs's counter to r1, and the handler
> performs the register update. One detail below is **wrong** and was corrected by
> measurement — the closed form is not variant 1's `r[0] += r[1]; r[1] = 0`.
>
> #345 fixed variant 1's missing register check. Variant 2 has the same hole **and a second,
> larger one**. Its matcher (`cpu_arm_instr.c:2833-2839`) pins the two MCRs exactly by their
> instruction words, then accepts `add rX,rX,#32` and `subs rY,rY,#32` **without checking
> either register** — the same shape-not-registers defect #345 measured. But
> `X(netbsd_cacheclean2)` (`:2085-2089`) only advances `n_translated_instrs` and sets
> `next_ic = &ic[5]`. **It updates no registers whatsoever.**
>
> So it skips the two MCRs, the `add`, the `subs` and the branch, and leaves every register
> exactly as it found them. The loop it replaces would end with the add's register advanced
> by 32 per iteration and the subs's register at zero. This is wrong *even for the NetBSD
> sequence it was written for* — unlike variant 1, which at least performs
> `r[0] += r[1]; r[1] = 0`. It also reads `r[1]` for its instruction count without ever
> having checked that `r1` is the loop's counter.
>
> The fix is therefore two-part, and larger than #345's one-line guard: pin the registers as
> #345 did, **and** perform the update the fold is standing in for
> (`r[0] += r[1]; r[1] = 0`, the same closed form variant 1 uses). A witness needs the two
> exact MCRs plus add/subs/branch, run twice, with both registers seeded and published —
> the `run_cacheclean` driver in `arm_flags_probe.py` is the right starting shape.
>
> **The flag divergence originally filed against both variants still stands and is separate**:
> neither writes flags though the loops they replace end on a `subs` reaching zero, which
> owes Z=1 N=0 C=1 V=0.

> ## 2026-08-05 — the shape-not-registers defect is a FAMILY, not two instances
> After #345 and the cacheclean2 note above, swept every ARM combiner for the same
> mismatch: does the matcher verify the registers its handler hardcodes? Counting register
> references in each matcher against each handler:
>
> | combiner | matcher reg-checks | handler reg-uses | verdict |
> |---|---:|---:|---|
> | `netbsd_cacheclean` | (now 2) | 2 | **fixed as #345** |
> | `netbsd_cacheclean2` | 0 | 1 read | **broken** — and updates nothing at all |
> | `netbsd_memset` | 0 | 3 (`r[ARM_IP]`, `r[2]`, `r[3]`) | **broken** |
> | `netbsd_memcpy` | 0 | 4 | **broken** |
> | `netbsd_scanc` | 4 | 5 | guarded; the fifth wants checking |
> | `netbsd_copyin` / `copyout` | 6 | 3 | guarded |
> | `strlen` | 2 | 0 | fine |
> | `netbsd_idle` | 0 | 0 | no hardcoded registers; its defect is the skipped TEQs |
>
> So **three more handlers write hardcoded registers their matchers never verified**, the
> same defect #345 measured on `netbsd_cacheclean` — where a loop using r5/r6 had r0 handed
> r1's value and r1 zeroed. `netbsd_memset` is the sharpest of the three: it hardcodes
> `r12`, `r2` and `r3`, so a matching loop built on other registers has three clobbered at
> once.
>
> This reframes the round. It is not "four handlers have flag bugs" but **one systematic
> defect in how these combiners were written** — the matchers were built to recognise a
> code SHAPE and the handlers to shortcut a specific NetBSD register allocation, and nobody
> connected the two. Each needs the same one-line-per-register guard #345 added, and each
> needs its own witness because the sequences differ.
>
> `netbsd_scanc`'s fifth register use is the one open question in the table: it may be a
> read of an already-checked register, or a fourth unguarded write.

> ## 2026-08-05 — RETRACTION: the "shape-not-registers FAMILY" entry above is WRONG
> The table in the entry dated earlier today generalised #345's defect to `netbsd_memset`,
> `netbsd_memcpy` and possibly `netbsd_scanc`. **That generalisation is refuted**, by a
> review seat and then independently by measurement. The counting method was the error: it
> counted literal `r[...]` tokens in each matcher and missed that these combiners match on
> **exact 28-bit instruction words**, so the register encoding is carried by the matched
> function's IDENTITY rather than by an explicit comparison.
>
> `COMBINE(netbsd_memset)` requires all sixteen slots to be `instr(multi_0x08ac000c__ge)`,
> installed only under `(iword & 0x0fffffff) == 0x08ac000c` — `stmia r12!,{r2,r3}`, i.e.
> Rn = `ARM_IP` and reglist r2/r3, exactly the three registers the handler hardcodes. There
> is nothing to guard. Measured: a foreign-register loop left `ip` intact at its seeded
> `0x11` **even with the fold forced live**, which is the empirical half of the proof rather
> than merely "nothing folded". `netbsd_memcpy`'s registers are pinned the same way
> (`0x08b15018` / `0x08a05018`). #345 itself stands — `netbsd_cacheclean` matches on
> function CLASS, not exact iword, which is why its registers really were free.
>
> ## The same investigation found something larger: X(netbsd_memset) is DEAD CODE
> It has never executed. `cpu_arm_instr.c:3979-3981` arms
> `combination_check = COMBINE(netbsd_memset)` for `iword == 0xcaffffed`, and
> `:4040-4043` then **unconditionally overwrites it** with `COMBINE(beq_etc)` for
> `main_opcode == 0xa` with condition code 12 — and `0xcaffffed` is condition GT = 12.
> Ordering decides it: `strlen` (cond 1) and `netbsd_cacheclean2` (cond 8) are in that same
> list but armed *after* the catch-all, so they survive; `netbsd_memcpy` (cond GE = 10) is
> not in the list at all. `netbsd_memset` is the only loser. Proven twice: an instrumented
> build logged zero entries to the combiner, and re-arming it after `:4043` made it fold
> immediately.
>
> **Latent, not live:** with the fold reachable, the matcher tests its `subs` only as
> `arg[0]==arg[2] && arg[1]==128` — any register — which collides with the hardcoded
> `r[ARM_IP]` when the subs targets ip: the handler reads the address *before* the subs and
> then overwrites ip with `addr+128`, discarding the subtraction (measured `0x100` where the
> architecture owes `0x80`, with the 128 bytes landing at `0x80..0xff`). That is #342-class
> and dormant. Whether to revive this fold at all is a scope decision, not a bug fix, and it
> has no value-discriminating PIN available: for a well-formed loop the fold is
> observationally equivalent to the STMs apart from a missing `&= 0xffc` base alignment.
>
> **`netbsd_memcpy` has a real but DIFFERENT defect, and it IS live** (cond GE escapes the
> overwrite): it replaces four block transfers with one `memcpy` and publishes only r0 and
> r1, leaving **r3, r4, ip and lr** stale where the LDMs would have left the last sixteen
> bytes copied. A missing side effect, not a register-guard hole.

> ## 2026-08-05 — #346 closes the cache-clean STRIDE hole; two defects there stay open
> Two review seats found #345 incomplete on the same point, and both were right. #345
> checked the two registers `X(netbsd_cacheclean)` **writes** and stopped; the load's own
> other two operands were still unchecked, and the first of them is a stride. The closed
> form `r[0] += r[1]` is arithmetic that is only true when each iteration advances the base
> by 32, so `ic[-3].arg[1]` is part of the contract. Measured on the committed build,
> `ldr r2,[r0],#4 / subs r1,r1,#0x20 / bne / mcr` folded and returned r0 = `0x9120` where
> the architecture returns `0x9104` — eight times the real advance, from a loop a compiler
> can emit. **#346 requires `arg[1] == 0x20` and `arg[2] == &r[2]`.**
>
> The same round found the **control row committed with #345 was asserting the wrong thing**
> and would have locked the defect in: `run_cacheclean(use_r01=True)` built its "must still
> fold" loop with `ldr r4,[r0],#4` and asserted the FOLDED answer `0x9120` for a program
> whose architectural answer is `0x9104`. It has been rebuilt on the genuine sequence. Note
> for anyone rebuilding it again: for a real 32-stride loop **r0 cannot discriminate**,
> because the closed form is exactly right there and both answers are `0x9120`. The only
> value that proves the fold fired is the stale destination.
>
> **Still open on this handler, both pre-existing and both recorded above:**
> - **the load's destination is never written.** `X(netbsd_cacheclean)` skips the loads, so
>   r2 keeps whatever it held (measured: seed `0x77` retained where the architecture leaves
>   the fetched `0xa5a5a5a5`). #346 does not fix this — it only confines it to r2, since a
>   fold on any other Rd would strand that register too. Fixing it means performing the
>   final iteration's load, which is a scope decision about a fold whose whole purpose is to
>   skip loads.
> - **flags are never written**, though the loop it replaces ends on a `subs` reaching zero,
>   which owes Z=1 N=0 C=1 V=0.
>
> `gate_arm.sh` now carries seven rows here, each loop one field off the genuine sequence.
> The two control rows pass on both builds by design; the pre-fix build scores 162/165.

> ## 2026-08-05 — #347 closes BOTH cacheclean2 defects; the flags stay open
> The entry above dated today ("netbsd_cacheclean2 is worse than its sibling") is
> **resolved**. `X(netbsd_cacheclean2)` really did update no guest register at all, and its
> matcher really did take any register pair; both are measured and both are fixed.
>
> Premise checked first, because the previous round of this family turned on exactly that
> point: `netbsd_memset`'s operands are pinned by the exact iwords its matcher demands, so
> there was nothing to guard. Here `instr(add)` and `instr(subs)` are the **generic** dpi
> table entries (`arm_dpi_instr[]`, `cpu_arm_instr_dpi.c:72-74`), selected by
> condition/opcode/S-bit alone, so the registers really are free. That the right ones to
> demand are r0 and r1 is not a convention either: the two MCRs are pinned by exact iword
> and both name Rd = r0, so the address the cache ops walk **is** r0.
>
> Measured on the committed build, two-pass free-running driver, r0 = `0x9100`, counter
> `0x40`: the genuine sequence folded and returned r0 = `0x9100`, r1 = `0x40` where the loop
> owes `0x9140` and 0; `add r5,r5,#32` folded anyway and stranded r5 at `0x9100`; and
> `subs r6,r6,#32` folded anyway and left r6 at `0x40`.
>
> **The closed form recorded in the entry above was WRONG.** `r[0] += r[1]; r[1] = 0` is
> variant 1's, and variant 1 ends on `bne`. This loop ends on `bhi` (`C && !Z`), so it exits
> on a BORROW as well as on zero, and its branch is at the bottom, so one iteration always
> runs. The measured trip count is
> `n = (r1 == 0 || (r1 & 31) != 0) ? (r1 >> 5) + 1 : (r1 >> 5)`, then `r[0] += n << 5` and
> `r[1] = r1 - (n << 5)`. Swept against the un-combined loop for r1 = 0, 1, 0x1f, 0x20,
> 0x21, 0x30, 0x40, 0x60, 0x7f: agrees on all nine, where the proposed form agrees on
> **three** of them — `0x20`, `0x40`, `0x60`, the only nonzero multiples of 32 in the set.
> `r1 = 0x30` really advances r0 by `0x40` and leaves r1 at `0xfffffff0`, where the proposed
> form gives `0x30` and 0; `r1 = 0` really advances r0 by `0x20` and leaves r1 at
> `0xffffffe0`, where the proposed form leaves r0 alone.
>
> ## STILL OPEN HERE: the flags — and READ THIS BEFORE FIXING THEM
> The `subs` that ends this loop owes N/Z/C/V and the fold writes none of them — the same
> divergence still filed against variant 1. With the registers now correct it is the **only**
> guest-visible difference left between the fold and the loop.
>
> That has a consequence for whoever closes it. Gate 14's control row **`A cclean2 still
> fold`** is built on this defect: it seeds N=1 with `cmp r9,#2` and asserts the folded run
> still reads N=1 where the real loop leaves Z=1 C=1. It is the *only* evidence that the
> optimisation still fires at all, because once the closed form is right r0 and r1 read the
> same folded or unfolded, so no register can discriminate. Writing the flags will therefore
> make that row **fail**, and it will not be a regression — it will be the row doing its job
> in a world where its premise is gone.
>
> **So the flag fix and the control row have to be re-authored in the SAME change.** Do not
> "fix" the failure by relaxing the row. There is no register left to move it to; it needs a
> genuinely different instrument — an execution-count/timing observable, or a sibling loop
> deliberately one field off the matcher so that folded and unfolded diverge somewhere the
> handler is not required to be right. Budget for building that instrument as part of the
> flag round, not as a surprise at the end of it.
>
> `gate_arm.sh` carries eight `A cclean2 ...` rows: five discriminators, one cpsr control,
> and two anti-clobber pins that pass on both builds and exist to catch the opposite error —
> a handler writing r[0]/r[1] by name behind a matcher that still accepts any register. The
> pre-fix build (`be6ea08`) scores 168/173.

> ## 2026-08-09 — #348/#349/#350 close the cache-clean flag entries; the fold detector was re-authored in the same change
> The flag divergence filed against both cache-clean folds is **resolved**: each
> handler now leaves r1 at the final iteration's operand and delegates the last
> subtraction to the real dpi `subs` (the netbsd_memcpy fold's own pattern), so
> the exit flags are computed by the same instruction the loop would have
> executed — Z|C on a zero exit, N on a borrow exit, V structurally 0 (the
> final operand lies in [0, 0x20] for every uint32 counter). Gate 14 grew
> 173 -> 189 rows; the pre-fix HEAD binary scored 181/189 failing exactly the
> eight new discriminators; the fixed build 189/189.
>
> `A cclean2 still fold` — the control row built ON the missing flags — was
> retired and replaced by #349's marker channel in the same change, as the
> entry above demanded: a DEBUG-gated `debugmsg_cpu` at the top of each
> handler, silent at default verbosity (pinned by the quiet rows), visible
> under `verbosity cpu 3` (the fires rows, each carrying its own echoed
> "3: DEBUG" as proof the level took), and deliberately not pre-gated with
> ENOUGH_VERBOSITY() per the #278 convention, so `breakpoint subsystem cpu`
> can catch a fold in flight.
>
> **#350** closed a hole this file had not yet named: variant 1's closed form
> terminated loops the architecture never exits. A counter that is not a
> multiple of 32 has an invariant residue, so its subs never reaches zero —
> the fold returned r1 = 0 anyway. The matcher cannot see r1 (translation
> time), so the HANDLER bails out to the pinned genuine load handler whenever
> `r1 & 0x1f` is nonzero; the residue is invariant, so every re-entry bails
> too and the guest keeps the infinite loop, the real loads, the faults and
> the interruptibility. r1 == 0 stays folded (it terminates, in 2^27
> iterations) and its marker/instruction accounting now uses the honest
> n = 2^27 rather than the 0 that `r1 >> 5` reported.
>
> **Still open on these handlers, deliberately:**
> - **Variant 1's skipped load** — stale r2 stays, and stays USEFUL: it is the
>   fold detector independent of the marker, and `A cacheclean still folds`
>   pins it. Two consequences sharpened in review and recorded here: a folded
>   run can never take the **data abort** the real loads could take, and never
>   performs their **MMIO/read side effects**. Fixing any of that means
>   performing real loads, i.e. deleting the fold's reason to exist.
> - **Both folds elide their MCRs.** Harmless while cr7 operations are no-ops
>   (`cpu_arm_coproc.c:209-216`); the day cache operations or coprocessor
>   traps are modelled, both folds silently skip them.
> - **`netbsd_idle` and `netbsd_memcpy`** (2026-08-03 entry above) remain the
>   open combiner divergences, next in the queue.
>
> **New follow-up candidate, found by the #350 witness:** a read of
> non-existent physical memory emits one host log line per access —
> `memory READ: from non-existant paddr=...` — and execution continues. That
> is a guest-reachable, per-access host-log flood of exactly the class this
> fork has repeatedly gated (#278 et al.), reachable on any ARM machine by a
> loop walking past the top of RAM, and presumably on other architectures
> through the same memory layer. Measured live: ~one line per loop iteration,
> tens of thousands per second. Needs its own round: locate the emitting
> site(s), classify latch-vs-gate per the recorded axis, and check which
> architectures share the path.
>
> The witness's own first draft is part of the record (see run_cc_nonmult's
> docstring): it expected a data abort at the top of RAM — measured false,
> the read logs and continues — and it compared a dump string against
> "deadbeef" unswapped, reading its own sentinel's parity as a measurement.
> Both are the file's recorded trap classes, re-encountered and re-recorded.

> ## 2026-08-10 — #351/#352/#353 resolve netbsd_idle; a fourth defect and an instrument blind spot found on the way
> The `netbsd_idle` entries in the 2026-08-03 combiner sweep are **resolved**. The fold
> wrote neither the load destination (#351) nor the flags (#351, by delegating the second
> `teqs` and branching on its `ARM_F_Z`); a loop whose second `teqs` aliased the load
> destination exited where the architecture idles (subsumed by #351's write-dest-before-read
> ordering, NOT a matcher guard); and a **FORWARD `beq` matched the loop and HUNG the guest**
> (#353 pins `ic[0].arg[0] == &ic[-4]`). Gate 14 grew 9 rows via a new `arm_idle_probe.py`;
> pre-fix HEAD scores 2/9, fixed 9/9; seven-seat panel, both passes, unanimous GO.
>
> **The alias defect was nearly filed as "harmless."** A first reproduction concluded it
> could not diverge — an artifact of its own debugger breakpoint, which turns translation
> read-ahead OFF (`cpu_dyntrans.c:1939` gates read-ahead on `breakpoints.n == 0`) and so
> forced a two-pass install whose real `ldr` pre-wrote the aliased register. A review seat
> that COMPILED variants found it live under read-ahead, and found the forward-`beq` hang no
> reading had surfaced. See task #12 below.
>
> **Still open / recorded, deliberately:**
> - **The read-ahead install-path audit (task #12).** Every gate-14 combiner row before this
>   round used a breakpoint, so none exercised the read-ahead path real guests take. The new
>   idle probe runs read-ahead-ON; the flag probe's false "a single forward run cannot work,
>   however driven" law is corrected. But #340/#342/#345/#346/#347/#348/#350's rows were all
>   breakpoint-driven — their FIXES are install-path-independent and stand, but their COVERAGE
>   of the read-ahead path is absent, and a register-aliasing defect in any of them would have
>   been masked exactly as netbsd_idle's was. Worth a sweep.
> - **`A idle alias exits`'s want is the dest prefill** (0xdeadbeef = "the exit store never
>   ran"), so its anti-vacuity rests on the IDLE_CONTROL bail and the `alias -J ref` PIN, not
>   on a self-evidently-non-seed value. Kept together on the record.
> - **`netbsd_memcpy`** (publishes only r0/r1, leaves r3/r4/ip/lr stale) remains the open
>   combiner divergence, next in the queue.

> ## 2026-08-10 — #354 resolves netbsd_memcpy's unpublished r3/r4/ip/lr
> The `netbsd_memcpy` entries above ("bypasses its LDMs without publishing the final
> r3/r4/ip/lr", filed by #340's after-panel and repeated in the #342 and #347 blocks) are
> **resolved**. The fold now publishes those four registers from
> `page_1 + (addr_r1 & 0xffc) + 16` on every iteration, so the final iteration's second
> `ldmia` block persists exactly as the architecture leaves it. Direct host read, NO
> byteswap, word-aligned base — matching the handler it emulates
> (`multi_0x08b15018`, `tmp_arm_multi.c:595-599`) and, decisively, the fold's own
> page-cross / NULL-page bail-outs which delegate to that handler; a byteswap would have
> made an on-page copy leave different registers than an identical copy that straddles a
> page. Published BEFORE the memcpy, matching ldmia-before-stmia order. Measured: pre-fix
> the four registers held their seeds on both a 1-iteration and a 2-iteration loop; the new
> `arm_memcpy_probe.py` scores 4/12 pre-fix (failing exactly the eight DISC rows) and 12/12
> after, with gate 14 at 210 checks.
>
> **Recorded, NOT fixed — pre-existing, deliberately out of #354's scope:**
> - **Unaligned base divergence.** The fold's `memcpy` copies from the unmasked
>   `& 0xfff` offsets, while both the real LDM and STM mask `& 0xffc`. The matcher matches
>   code SHAPE, not register values, so a guest entering with `r1 & 3 != 0` does fold and
>   the data path diverges from the genuine instructions. #354 deliberately sides with the
>   handler for the register publish (proven bit-identical to what the real second `ldmia`
>   reads, since `(r1 & 0xfff) + 16 <= 0xff0` rules out a carry past bit 11), but the copy
>   itself is unchanged. The honest fix is a runtime unaligned bail-out, not masking only
>   the new read.
> - **Forward-overlap divergence, same root.** For `dst` in `[src+1, src+31]` the real
>   sequence's second `ldmia` sees the first `stmia`'s bytes; a single
>   `memcpy(dst, src, 32)` cannot reproduce that (and is UB on overlap) regardless of where
>   the publish sits. Publishing before the copy is correct for non-overlap and backward
>   overlap; forward overlap matches nothing, because the copy is already wrong there.
> - **`host_store` as the source page.** The fold reads its source through
>   `host_store[addr_r1 >> 12]` where the genuine handler uses `host_load`. Harmless: a
>   read-only source page is NULL in `host_store` and takes the bail-out to the handler.
>   But it means "the fold's source read is identical to the handler's" is true only
>   because of that bail-out, not by construction.
> - **No fold-fired marker, so the new rows could go vacuously green.** Post-#354 the fold
>   and the genuine path agree by construction, so if a future change broke the combiner
>   registration (`iword == 0xaafffff9`) or the matcher, all 12 rows would keep passing via
>   the genuine instructions and the coverage would silently disappear. Closing that needs a
>   #349/#352-style DEBUG-gated marker; out of #354's minimal scope, recorded here.
> - **Audit sweep worth doing:** several ARM folds publish fewer registers than the
>   sequence they replace — `netbsd_cacheclean`'s known-stale r2 is the same species as this
>   defect. A systematic pass over every combiner ("which registers does the replaced
>   sequence write that the handler does not?") is the generalisation of #354.
>
> **Added by round 101's pass-2 seats (measured, recorded not fixed):**
> - **The complete fix for all three divergences is one shape**, and it is worth writing
>   down: replace the fold's single `memcpy(...,32)` with the handler pair run twice —
>   load four words at `(addr_r1 & 0xffc)`, store four at `(addr_r0 & 0xffc)`, repeat at
>   `+16`, with the register publish falling out of the second load. That is
>   architecturally exact for unaligned bases AND for every overlap direction, and it
>   subsumes the unaligned-base, forward-overlap and publish-placement questions at once.
>   It costs the fold its single-`memcpy` advantage, which is why #354 did not take it.
> - **Big-endian ARM guests get unswapped word reads from the multi fast path itself.**
>   The handler install at `cpu_arm_instr.c:4198` is guarded only on `HOST_LITTLE_ENDIAN`,
>   never on `cpu->byte_order`. So "#354 == handler == bail-out for every guest byte order"
>   is literally true and adds no divergence, but the SHARED answer is wrong for a BE
>   guest. One-place fix in `generate_arm_multi.c`, not here.
> - **Citation hygiene:** `tmp_arm_multi.c` is a BUILD ARTIFACT (generated by
>   `src/cpus/Makefile.skel` from `generate_arm_multi.c` + `cpu_arm_multi.txt`); it does
>   not exist in a fresh checkout and its line numbers move whenever an opcode is added.
>   Cite `generate_arm_multi.c` instead — #354's comment was corrected to do so.

> ## 2026-08-10 — ARM combiner publication audit: every fold, what it fails to publish
> The generalisation of #351 (netbsd_idle's unwritten load destination and flags) and #354
> (netbsd_memcpy's unwritten r3/r4/ip/lr): a read-only audit of EVERY ARM combiner, asking
> per fold which guest-visible effects the replaced sequence produces that the handler does
> not. Method notes that matter, because a previous attempt at this generalisation was
> retracted: an exact-iword pin implicitly pins its registers (the encoding rides on the
> matched function's identity — do NOT count literal `r[...]` tokens in a matcher), and
> `instr(X)` names are the UNCONDITIONAL table entries, so no matcher can catch a
> conditional compare, and `rd == PC || rn == PC` selects a different table entirely.
> Structural non-finding worth recording: every matcher rewrites only the ENTRY slot's `f`,
> so a guest branch into the middle of a folded window executes the original handlers — no
> fold diverges that way.
>
> **CLEAN, needing no work** (so a future round need not re-derive it): `netbsd_scanc`,
> `netbsd_idle` (post-#351/#353), `xchg` (post-#342), `netbsd_memcpy`'s registers and flags
> (post-#354), `netbsd_cacheclean2`'s registers and flags (post-#347/#348), and all
> thirteen `cmps_*` plus four `teqs_*`/`tsts_*` folds (post-#340) — each verified against
> the dpi templates for N/Z/C/V, including the `b == 0` and sign-restricted V
> specialisations and the shifter-carry restoration.
>
> **RESOLVED: `netbsd_scanc`'s fifth register use** (the open question above) is a READ of
> an already-pinned register, not an unguarded write. It is `r[ARM_IP]` at
> `cpu_arm_instr.c:2301`, standing in for `tst r3,ip`, and the arming condition
> `iword == 0xe113000c` (`:4014`) fixes BOTH operands by encoding. Its flags are exact for
> a non-obvious reason worth keeping: N is cleared and never set, correct only because r3
> holds a freshly loaded BYTE so `r3 & ip <= 255`; and C is left alone, correct because the
> register form of TST takes no shifter-carry path (`cpu_arm_instr_dpi.c:123` excludes the
> register variants).
>
> **FOUR live divergences found, none previously recorded, each now a queued task:**
> - **`netbsd_cacheclean` publishes an unmasked r0.** `:2166` does `r[0] += r1` where the
>   genuine post-index writeback stores the MASKED address (`cpu_arm_instr_loadstore.c:292`
>   masks, `:342` writes back the masked value). r0 = 0x9101, r1 = 0x40: the loop leaves
>   0x9140, the fold 0x9141. The matcher cannot see r0's value, so any shape-matching loop
>   with an unaligned base folds. Note the tension: the handler's masking is itself a GXemul
>   simplification (real ARM writes back Rn+offset unmasked), so which side to correct needs
>   a primary source. Distinct from this handler's already-recorded stale r2 / elided loads.
> - **`netbsd_copyin` / `netbsd_copyout` diverge twice**, and unlike the memcpy byte-order
>   case these disagree with the very instructions they replace: `:2495` writes `r0 + 24`
>   and `:2530` writes `r1 + 24` where the six genuine `ldrt`/`strt` write back the masked
>   address; and `:2489-2494` / `:2524-2529` move words by direct `uint32_t` access where
>   the single-register template swaps per `cpu->byte_order`
>   (`cpu_arm_instr_loadstore.c:293-302`), so a BE guest on an LE host moves byte-reversed
>   words. The folds' own data offsets ARE masked (`:2478`/`:2513`), which is what confines
>   the first defect to the base's two low bits.
> - **`strlen` has an unbounded, non-interruptible loop.** `:2425-2442` exits only on a NUL
>   byte or a NULL host page — no iteration cap, no `N_SAFE_DYNTRANS_LIMIT` check — so a
>   guest pointing it at a long non-NUL run stays inside one C call for millions of
>   iterations with no device ticks and no interrupt delivery, then adds an unclamped
>   `n_loops * 3` (`:2444`). That is the #169 class #350 already clamped for both
>   cache-clean folds. Latent alongside it: the matcher (`:3161-3166`) never requires
>   `arg[0] != arg[2]`, so `ldrb r3,[r3,#1]!` makes the genuine `cmps` compare an ADDRESS
>   while the fold compares the byte (#342 class, on an encoding ARM calls UNPREDICTABLE).
> - **`netbsd_memset` is DEAD and its divergences are latent** — re-verified: `0xcaffffed`
>   is condition 12, so the arming at `:4266-4268` is overwritten by the `beq_etc` catch-all
>   at `:4327-4330` before the check ever runs. Were it revived, its generic `subs` pin
>   collides with the hardcoded `r[ARM_IP]` read taken before the subtraction, and its
>   `memset` uses the unmasked offset where the sixteen real stores mask. Correctness-neutral
>   side effect of the same arming order, worth knowing: for the exact iwords `0x1afffffc`
>   and `0x8afffffa`, `strlen`/`cacheclean2` STEAL `beq_etc`, so a compare immediately before
>   one of those two branch words is never folded into it — a lost optimisation, not a
>   divergence.
>
> Ranked by live x guest-visible severity: cacheclean-r0 (wrong register value on every
> folded call), memcpy's data path (wrong BYTES for unaligned/overlapping copies — higher
> per-occurrence, lower reachability, complete fix already specified above),
> copyin/copyout (two one-line fixes), strlen (host liveness), cacheclean2's elided MCRs
> (unobservable until cache ops are modelled), memset (dead).

> ## 2026-08-11 — #355/#356 resolve the strlen fold's two defects
> The audit block's `strlen` entry is **resolved**. **#355**: the matcher now requires the
> load's base and destination to differ, rejecting exactly `0xe5f33001`. Recorded honestly:
> this is a **self-consistency / oracle** fix, not a wrong-answer fix — ARM calls the
> encoding UNPREDICTABLE, so the fold's answer was not wrong; what was wrong is that this
> emulator returned two different answers for one program depending on whether the
> combination happened, and `-J` is gate 14's own architectural oracle. #342 is precedent
> for the guard's SHAPE only (its case is well-defined ARM and produced a wrong value).
> The rejected alternative is in the source: a handler-side "fix" would put the guest's
> genuine infinite loop inside one C call — an unkillable host hang.
> **#356**: the walk is bounded by the batch budget, tested at the BOTTOM of the do-while
> so at least one iteration always completes (a top-of-loop return would skip the load and
> let a guest with r3 == 0 exit its loop having never loaded a byte — a new divergence of
> the class being fixed), yielding to `&ic[0]` with the same `3n-1` billing as the normal
> exit. Gate 14 grew 7 rows (now 220 checks): pre-fix 3/7, fixed 7/7.
>
> **Corrections to what this file previously said about this defect:**
> - Reachability was understated ~30x. `n_translated_instrs` resets once per `run_instr`,
>   not per fold entry, and the walk is REPLAYABLE — twenty back-to-back walks measured
>   983,080 instructions accumulating into one int. The signed overflow needs ~18-24 MB of
>   non-NUL memory at the DEFAULT `-M 64`, not ~700 MB.
> - "No device ticks" was wrong: `machine_run` decrements by a constant and discards
>   `run_instr`'s return, so no tick is skipped. The real faults are a ~6000x
>   instructions-per-tick ratio distortion and a host stall in which ^C, the console and
>   the debugger are dead.
>
> **Recorded, not fixed:** the signed-overflow EVENT stays **reasoned-not-witnessed** —
> ~716 MB of contiguous non-NUL memory is not honestly gateable — with #350 as the family
> argument. Also recorded, from the same review: the probe cannot verify the `3n-1` billing
> constant to better than ~8K instructions, because `ninstrs` is committed only when
> `run_instr` returns; the constant rests on the source derivation plus a 1 MB differential
> (folded 3,144,852 vs an architectural 3,145,728, `-J` 3,138,120), not on any gate row.
> And once a walk exhausts the budget, the rest of that dispatch group advances one byte
> per dispatch, so ~4% of a long walk's dispatches are near-empty — progress is guaranteed,
> but the derivation is written down so the next reader need not redo it.

> ## 2026-08-11 — CORRECTION to the combiner audit: two of its four "live defects" may be non-defects
> Scoping the copyin/copyout item turned up a root cause that INVERTS part of the audit
> recorded above, and it is written down here before anyone acts on that ranking.
>
> The audit measured each fold against the handler it stands in for. For the two
> "unmasked base writeback" findings — `netbsd_cacheclean`'s `r[0] += r1` and
> `netbsd_copyin`/`netbsd_copyout`'s `r0 + 24` — the handler is the wrong yardstick:
> `cpu_arm_instr_loadstore.c` masks the address (`addr &= ~3`) and then post-index writes
> back `addr + offset`, i.e. the MASKED base plus the offset. **Real ARM writes back
> `Rn + offset` UNMASKED** — the alignment masking governs only which bytes are read and
> how a loaded word is rotated. If that reading holds, GXemul's TEMPLATE is the
> simplification and those two folds are CLOSER to the architecture than the code they
> were compared against, so "mask the base on entry" would move them away from real
> hardware to agree with a local shortcut.
>
> **Required first step, now queued as its own item:** settle the post-index writeback from
> a primary source (ARM ARM DDI 0100, LDR/STR post-indexed, plus what silicon does with an
> unaligned base and W=1). This project has needed the manual twice for exactly this class
> of question (m88k #307 and #323). Then either fix the template ONCE — writeback
> unmasked, data path still masked and rotated — which closes both fold items by agreement
> and touches no fold; or record the simplification deliberately and close them as
> non-defects. A template change's blast radius is every ARM load/store with writeback, so
> it needs its own round with aligned and unaligned rows and a full battery.
>
> **Unaffected by this correction, still live:** the byteswap half of the copyin/copyout
> item (those folds move words with a direct `uint32_t` access where the single-register
> template assembles per `cpu->byte_order`, so a big-endian guest gets byte-reversed words
> — and unlike the memcpy case the template really does swap, so the fold genuinely
> disagrees with the instructions it replaces); `netbsd_cacheclean`'s stale r2 and elided
> load side effects; and the `strlen` items, resolved this round as #355/#356.
>
> **The general lesson, recorded because it cost a near-miss:** "measured against the
> handler" is not "measured against the architecture". A fold that diverges from its
> handler is a divergence to explain, not automatically a defect to fix — the handler may
> be the one that is wrong.

> ## 2026-08-11 — #362: unaligned word loads returned the aligned word, unrotated
> The second divergence #357's research found, now closed. An unaligned word LOAD must return
> the aligned word ROTATED RIGHT by `8 * addr[1:0]` (DDI 0100I A2.8 p. A2-38, and A4.1.23's
> pseudocode `data = Memory[address,4] Rotate_Right (8 * address[1:0])` when the CP15 U bit is
> 0). The template masked and never rotated. Fixed in both paths plus `netbsd_copyin`.
>
> **The measurement identifies the model**, which is a better instrument than a pass/fail
> expectation and worth reusing: mask-only, rotate, and the ARMv6 `U == 1` true unaligned
> access are pairwise distinct at every nonzero offset, so a wrong answer says WHICH model is
> implemented. Pre-fix read the unrotated word at all four offsets; post-fix reads
> `0x11223344 / 0x44112233 / 0x33441122 / 0x22334411`.
>
> **TWO OF THIS FILE'S OWN CLAIMS WERE WRONG AND ARE CORRECTED.** (i) The #357 entry recorded
> that the rotation "must land in BOTH paths in one change or the fast path silently undoes it"
> and that the fast path was materially more work — that is why this sat queued as a large
> round. It is the same three lines: the fast path already masks and then assembles the bytes
> of the ALIGNED word, so rotating the assembled value is exactly equivalent to re-indexing
> them. Eleven lines, four sites. The "both paths in one change" part stands; the "materially
> more work" part was an overestimate that cost several rounds of deferral. (ii) #357's
> `wb_addr` cannot be carried over: it exists only under `!defined(A__P) || defined(A__W)`, and
> the plain offset-addressing word load has neither, so the rotation needs its own capture.
>
> **Version gating was rejected on a dominance argument, not a preference**, and the reasoning
> should survive: rotation is correct for ARMv3/v4/v5 and for v6+ with `U == 0`, and where v6+
> with `U == 1` wants a true unaligned access, masking and rotating are wrong EQUALLY — so
> unconditional rotation is never worse than what it replaced, in any combination. Gating would
> also be unsound: there is no architecture level in the CPU type table (its own header says
> "TODO: Include ARM level" and "Most of these are bogus"), deriving one from the ID register
> misclassifies one part as ARMv6 — wrong in the direction that changes behaviour — and no
> `ARM_CONTROL_U` is defined anywhere. **Recorded divergence: ARMv6+ with `U == 1`**, where the
> architecture wants a true unaligned access and this emulator now rotates. Unmeasured: whether
> `U` is 0 at reset on the specific v6 parts the table names; the decision does not depend on
> it, but a divergence note quoting a reset value would need a source.
>
> **Still open in this family, all recorded with measurements:** `swp` implements a THIRD model
> (a true unaligned access whose store crossed the word boundary — measured) **[RESOLVED as
> #386, 2026-08-12: byte-order + rotate + mask in one round, RED 42/58 → GREEN 58/58, three
> mutants each caught at their predicted counts — see the 2026-08-12 entry]**, `ldrex` HALTS the
> emulator on an unaligned address, and the LDM/STM class was left alone because this project
> has not checked the manual's wording for it — treat "UNPREDICTABLE" there as unverified
> rather than established. Also open and adjacent: the #357 path-coverage claim in
> `arm_writeback_probe.py`'s docstring is false, because `put w` warms the mapping and the rows
> it attributes to the general path take the fast one; the general load path may currently be
> exercised by nothing, and the cheap fix is one `put b`-seeded row.

> ## 2026-08-11 — #360: the `quiet` row asserted an absence, and an absence is what a dead fold produces
> #358's `quiet` rows assert that no marker appears at default verbosity. That tests the
> verbosity gate, not the fold. #360 replaces them with `warm`/`cold` pairs that make a
> positive statement, and adds the two markers that let them: a **decline** marker computed in
> the guard's own short-circuit (so the diagnosis cannot drift from the condition it
> describes) and an **install** marker in each matcher.
>
> **The install marker is load-bearing, not decoration.** A decline marker alone is a two-way
> split, because "the matcher declined" and "the slot was never dispatched" both read fire 0 /
> decline 0. All three terms give a one-read diagnosis: install 1 / fire 1 / decline 0 healthy;
> install 1 / fire 0 / decline 1 reached and declined, with the text naming the clause;
> install 1 / fire 0 / decline 0 never dispatched (a misplaced breakpoint); install 0 the
> matcher declined. One line per translation, so it is free even in a hot guest. The decline
> text avoids the word "combined" because the probes count fires by matching
> `<name>: combined` and would otherwise tally declines as fires.
>
> **The whole point, in one measurement.** On a build with ONLY `netbsd_copyin`'s arming
> disabled, `A fold copyin quiet` still reads **ok** while `A fold copyin cold` goes **red** —
> the vacuous row and its live replacement side by side on the same run. 5 of 8, red at exactly
> the three copyin rows, copyout's four green, and `install 0` naming the cause.
>
> **"Reads zero" is unsound as a control, and this is measured, not argued.** With verbosity
> off the guest ran *perfectly* — full six-transfer advance — and reported zero fires AND zero
> installs, so an install marker does not rescue that case; a program whose pc never reaches
> the block also reads zero. So each arm asserts the verbosity echo, an execution witness
> (`r0`/`r1` advanced by the full six transfers, which holds folded or not and so proves the
> program ran without presuming the fold), and the exact decline count. Counts are numbers
> derived from the mechanism — a straight-line single-pass block dispatches the entry slot
> once, so warm is 1/0 and cold is 0/1 with 1 install either way — never thresholds.
>
> **A prediction that would otherwise have cost a false failure:** `copyout`'s warm-up must be
> a **store**. A load sets the user-page bit but leaves the store mapping empty, so the fold
> declines `no-page` instead of firing and the *healthy* build fails its own row. Derived from
> source by a review seat, confirmed by measurement, and now stated in the handler comment.
>
> **Still owed:** rows for `xchg` and `scanc`, which have markers but none. Their constants are
> measured and recorded on the queue item — notably that `xchg`'s negative control is a
> **matcher** decline (install 0), a different signature that must not share an expected shape
> with these pairs, and that `scanc` needs a trailing sentinel because its result register
> reads zero in every arm, plus that its "omit the warm-up" control is wrong when the row
> seeds data with `put w`, which already warms the load mapping.

> ## 2026-08-11 — #359: a fold copying HALF THE BYTES passed all 243 gate-14 checks
> The severest coverage finding of this whole sequence, and it was measured rather than
> suspected. A build whose `netbsd_memcpy` fold called `memcpy` with **16 instead of 32** —
> same iteration count, same register advance, half the data moved — passed the committed
> `arm_memcpy_probe.py` at **12/12** and gate 14 at **243 checks**. The blindness is
> structural, not an oversight: `r3/r4/ip/lr` are published by a direct page read that
> **bypasses the fold's `memcpy` call** (that is #354's own design and it is correct), and
> `r0`/`r1` advance unconditionally. Every register this gate asserted was right on a build
> moving the wrong bytes. **A count-based row would not have closed it either** — reported
> iterations × 32 still equals the register advance when the copy size shrinks, and a count
> row was the plan for this round until a seat built the mutant and measured the count blind
> to it. Closed by five rows that read the destination bytes against a pre-filled sentinel:
> **17/17** healthy, **15/17** on the mutant, red at exactly `1it dst w6` and `2it dst w14`.
> Gate 14 is now 248 checks. The rows are **PIN not DISC** — the genuine `ldmia`/`stmia`
> moves the same bytes, so they discriminate a broken COPY rather than fold-versus-no-fold,
> a different axis from everything else in the gate.
>
> **Measured mechanics of this fold, kept because they were expensive to establish.** A
> page-aligned multi-page copy **never bails**: `(addr & 0xfff) + 32 > 0x1000` is false at
> the last in-page offset (`0xfe0 + 32 == 0x1000` exactly), so an 8160-byte two-page copy is
> one dispatch and one marker with an exact sum. A 32-byte-misaligned copy bails once per
> crossing and the deficit is exactly 32 bytes per bail, because **each bail delegates one
> genuine UNCOUNTED iteration** — so the general identity is
> `32 × (reported + bail delegations) == advance`, not the simpler form, and the `n_iter == 0`
> bails print nothing today so that term is currently unobservable. The fold reads
> `host_store` for its **source** page as well as its destination, so a copy whose source has
> never been stored into never folds at all (measured: 255 of 255 iterations genuine, source
> page flag clear every time). [#385 precision: "never stored into" overstates — the operative
> condition is never **warmed by any data access**, since MMU-off a load alone sets host_store
> (`ok-1 == 1`, the #382 mechanism). The "255/255 genuine, flag clear every time" record is
> UNRECONCILED under that mechanism — a fully-cold source should self-warm on the first
> delegated iteration (bail → bdt_load → memory_rw insert), predicting ~1 genuine + 254
> folded; re-measurement queued, treat as unexplained meanwhile.]
> And the debugger's `put w` **does** populate that array —
> previously recorded here as not established — which is why the committed probe folds with
> no explicit warm-up. **A cold program is a double trap:** without warming, the healthy
> build FAILS its own count row (the first dispatch takes a silent no-page bail, so healthy
> reports one fewer than owed) while the `n_iter += 2` mutant PASSES at one seed by
> coincidence — both failure modes in a single row.
>
> **Still owed, with every constant already measured so the next round need not re-derive
> them.** (i) `copyin`/`copyout` **bail and install markers**: a bail marker alone gives a
> two-way split, since "arming or matcher broke" and "breakpoint misplaced" both read fires 0
> bails 0; adding an install marker in the matcher completes the table — install 1 / fires 1 /
> bails 0 is healthy, install 1 / fires 0 / bails ≥ 1 means the guard rejected and its fields
> name which clause, install 1 / fires 0 / bails 0 means the slot never dispatched, install 0
> means the matcher rejected **or the session broke**. Volume measured at 1:204 against the
> fire marker; the install marker is one line per translation. A shipped memcpy bail marker
> must keep printing `n_iter` — a prototype that dropped the field destroyed the summing
> identity. (ii) The **warm-up A/B rows**, whose exact counts are measured: copyin and
> copyout give install 1 / fires 1 / bails 0 warm and install 1 / fires 0 / bails 1 cold;
> `xchg` needs no warm-up and its negative control is the **matcher** (install 0), a
> different signature that must not share an expected shape with the others; `scanc` warm
> gives fires 1 and an unmapped base gives fires 0 / bails 1. (iii) A **"reads zero" negative
> control is unsound on its own** — measured twice: with verbosity off the program ran
> perfectly (full six-transfer advance) and reported zero markers AND zero installs, so an
> install marker does not rescue it; and a program whose pc never reaches the block also
> reads zero. Every negative arm needs the verbosity echo, a positive execution witness, and
> ideally `bails == 1`. **`scanc` has no natural witness** (its result register is zero in
> every arm) and needs a trailing sentinel, measured not to perturb the fold. (iv) `scanc`'s
> "omit the warm-up" control is **wrong** if the row seeds data with `put w`, because that
> seeding already warms the load array — use the unmapped base. (v) Do **not** replace the
> two-pass rows: they are the only shape exercising the guard transitioning from reject to
> accept inside one session, which is the mechanism a real guest depends on.
>
> **Unmeasured and honestly open:** whether `is_userpage` survives TLB eviction; the
> per-megabyte bail rate under a real guest (the 256/MB figure is extrapolated from a
> six-page synthetic walk and assumes one crossing per page, which unaligned guest bases
> would exceed); and whether the `-J` control arm and the marker arms agree on instruction
> billing, which no row reads.
>
> **Pass-2 residuals on #359 itself — gaps in the new rows, not defects in them, so queued
> rather than held.** (i) There is **no two-iteration tail row**: nothing asserts that the
> sentinel survives at word 16 after the 64-byte copy, so a fold that over-copied to 80 or 96
> bytes would pass all five. The one-iteration tail row covers the over-copy *class*, so a
> mutation that over-copies only on the second iteration is contrived — but the row is one
> line and the dump would need to reach 18 words. (ii) **A dump-format mismatch is
> indistinguishable from a byte defect.** If the emulator's `dump` output ever stops matching
> the probe's regex, the destination list comes back short and the rows read red for a reason
> that has nothing to do with the fold — the same misleading-symptom class as the teardown
> defect this round already hit. A distinguishable failure line (rather than letting the rows
> simply go red) would make a future red row triageable in one look. (iii) Eleven destination
> words are never read back, and word-level reads cannot see a byte permutation *inside* a
> word that preserves the 32-bit value. A seat named the specific mutation that survives,
> which is more useful than the word count: **a fold writing 7 words instead of 8** — an
> off-by-one on a *count* rather than a stride — because every sampled word is still a correct
> source word and the tail is still sentinel. Same hole at 15-of-16 in the two-iteration case.
> Both the pre-fill and the dump are already 16 words wide, so closing it is "add more `dst`
> rows", not "widen the pre-fill". Three seats independently agreed this is a future-work item
> rather than a defect in the shipped rows, at 5-of-16 sampling density.
>
> **One pass-2 claim was checked and is wrong**, recorded so it is not acted on later: a seat
> reported the probe's existing `0xdeadbeef` pre-fill as vestigial, on the reasoning that the
> publish area and the copy destination must be the same region. They are distinct — the
> publish area sits at one address and the copy destination 0x300 bytes above it, the program
> stores its registers to the former via r7 and copies into the latter — so both pre-fills are
> live and neither should be removed.

> ## 2026-08-11 — #358 fold-fired markers: what shipped, what is measured, and what is still owed
> Five ARM combiners produce results identical to the sequences they replace, so a row
> asserting their result passes whether or not the fold fires. #358 adds DEBUG-gated markers
> to `netbsd_copyin`, `netbsd_copyout`, `netbsd_scanc`, `xchg` and `netbsd_memcpy`, plus the
> first rows for the two that had none. Gate 14: 237 → 243 checks.
>
> **What is measured.** The folds fire on `testarm` — established on the pre-#357 snapshot
> where the old writeback detector still works (`0x10019` folded against `0x10018` under
> `-J`), deterministic across 5 consecutive runs. The marker discriminates: 1 line with
> combining on, 0 under `-J`, verbosity echo confirmed in both. Rows 4/4 on the shipping
> build; on a scratch tree with **only** `netbsd_copyin`'s arming disabled, 3/4 with exactly
> `A fold copyin fires` red and `copyout`'s rows green — so each row tracks its own fold's
> arming, which `-J` alone could not show.
>
> **CORRECTION, from the compile-and-measure seat: a marker-free instrument DOES exist.**
> This round's design claimed the `mp` device's instruction counter cannot detect firing for
> any of these folds because each bills exactly. The billing is exact; the conclusion does not
> follow. The run loop advances the counter by a fixed amount per **batch of 120 dispatches**
> and tests the batch limit only at those boundaries, so a fold — which changes
> instructions-per-dispatch — shifts the quantum and `ninstrs` lands elsewhere. Measured on the
> committed binary, no source change and no marker: **0xabef combining-on against 0xa1b8 under
> `-J`**, reproducible, discriminating across block counts 10 through 60, with the
> broken-arming build reading `0xa1b8` as the control. The unfolded value is `120 × 345`
> exactly, so this is quantisation, not a billing error. **Deliberately not made a gate row:**
> it pins emulator internals (the batch limit, the 120-dispatch unroll) rather than an
> architectural value, so a future dyntrans change rewrites it silently, and it must be
> re-checked per row — one shape collided, reading the same value folded and not. Recorded as
> the round's pre-fix reproduction instead, which also means the round was **not** forced into
> an inverted order. Related fidelity issue in its own right, worth its own look: the counter
> the guest reads leaks the dyntrans batch quantum, so an identical architectural instruction
> stream reads differently depending only on whether a combination fired.
>
> **CORRECTION: the `step` hazard is refuted as stated, and replaced by a sharper one.** The
> warning was that an already-installed fold would still execute under `step` and print its
> marker at default verbosity through the gate bypass. Measured: it does not — **stepping onto
> a fold slot re-translates it uncombined**, so no marker appears at any step. That also
> explains this round's own step-pc measurement: the mechanism is not "a breakpoint suppresses
> the fold" but "stepping un-folds the slot". The correct warning is stronger: never drive a
> row with `step`, because it measures the genuine sequence while appearing to measure the
> fold. Unmeasured: a `step` onto a fold slot reached as a branch target.
>
> **The breakpoint matrix, measured, because it is a trap for whoever writes the queued rows.**
> Breakpoint *after* the sequence: 1 install, 7 folds over 8 passes. Breakpoint *inside* the
> loop: **8 installs, 0 folds** — the matcher re-installs every pass and the fold never runs, so
> the row reads exactly like a dead fold on a healthy binary, and the signature is invisible
> without instrumenting the matcher. With read-ahead off (any breakpoint present) the fold
> count is always `passes − 1`. Every queued row's expected count must be a number derived
> from that rule, never "greater than zero".
>
> **A better row shape than the one shipped, measured and recommended for the queued work.**
> A single warm-up `ldrt` to the same page makes the fold fire on the FIRST execution of a
> straight-line block: with the warm-up, fires 1 and bails 0; without it, fires 0 and bails 1.
> That is a perfect A/B pair differing by one instruction — no loop, no branch, no
> free-running subtleties — and the no-warm-up arm is a negative control that must read zero,
> which makes the row unable to pass vacuously. It tests the FOLD, where the shipped `quiet`
> row only tests the verbosity gate. It needs read-ahead, so no breakpoint: a grace-then-
> interrupt row.
>
> **A gap in the markers themselves, worth closing next round.** There is no BAIL marker, so a
> red row is ambiguous between three causes needing three different fixes: arming or matcher
> broke (no install, no fire), the guard rejected the operands (install, no fire, bail), and
> the breakpoint was misplaced (install, no fire, no bail). A distinctly-named bail marker on
> copyin/copyout would name the cause in one read, and costs about 256 lines per MB against
> the fire marker's 42,900.
>
> **Flood measured rather than estimated:** 1010 KB of copyin produced 42,926 marker lines and
> 1.90 MB of console text, an 11 ms run becoming 538 ms — a 49x slowdown, and console output
> twice the size of the data copied. The design's ~44,700/MB estimate was right to within 4%.
> A 63 KB copy costs 40 ms, so block-sized rows are free, which is what the accept-the-volume
> decision rests on.
>
> **`is_userpage` is STABLE, contrary to two seats' concern:** 10 of 10 runs identical, and an
> intervening non-user access to the same page does NOT turn the fold off, because the clear
> lives inside `update_translation_table` which the plain load's fast path never calls once the
> page is mapped. Unmeasured, and the one thing that could still make a future row flaky: TLB
> eviction, which needs enough distinct pages to cycle the entries.
>
> **A pass-1 seat's marker-free instrument, and the honest limit of its refutation.** The
> seat proposed that one `step` across a warm folded slot would advance pc by the whole
> 24-byte window. Measured under the protocol `breakpoint` on the instruction before the
> window → `continue` (arrive pass 1, window untranslated) → `continue` (window translates
> during the free run, so the fold should install; arrive pass 2) → `step` over the `mov` →
> `step` across the entry slot: the result was **pc + 4 with one register loaded**, i.e. a
> single genuine instruction, on both the default and the `-J` build, with the fold's
> destinations zeroed first so pass-1 leftovers could not masquerade as loads. In pass 2 the
> seat proposed that exact first-hit/resume ordering as an *untested* variant; it is the
> protocol that was tested, so the refutation covers it.
> **The mechanism, initially recorded as unestablished, is now SETTLED by the
> compile-and-measure seat and it is neither of the two candidates guessed at first.** It is
> not that the fold failed to install, nor that a breakpoint suppresses it: **stepping onto a
> fold slot re-translates that slot uncombined**, so the step executes a plain instruction.
> That fully explains the observed `pc + 4`, and it is why the correct warning is "never drive
> a row with `step`" rather than anything about breakpoints per se. Note the pc-stride witness
> is dead for a sharper reason than brittleness, then — the act of stepping destroys the thing
> it would measure. Either way it would not remove the need for the marker:
> the `quiet` rows need the marker's ABSENCE at default verbosity, and single-step **bypasses**
> the verbosity gate, so a stepped session actively falsifies that direction.
>
> **Whether to ship markers without rows was the pass-2 panel's only real split**, and it was
> settled on the argument rather than the count: one seat wanted the round HELD, three wanted
> it shipped with the gap recorded. The decisive distinction is that an unexercised marker and
> an unfailable row are different classes. A row that cannot fail actively asserts coverage
> that does not exist — it lies to the reader of the harness. An unexercised marker asserts
> nothing to the harness at all; its failure mode is silent drift, not false assurance, and it
> is strictly better than the previous state, in which those folds had neither a marker nor
> firing coverage. Holding the round would also have pressured three rushed row-pairs, and a
> rushed unfailable row is the worse defect. **But the dissent lands on one item, and it is
> conceded here rather than argued away:** `netbsd_memcpy`'s iteration counter is not merely
> unexercised instrumentation, it is **untested LOGIC** — new state with arithmetic that no
> row checks — so if the count is wrong nothing notices. Two seats reached that independently.
> It is the first item below for that reason.
>
> **Owed work, each with its non-vacuity break named, so this is queued and not implied:**
> - **`memcpy`'s row FIRST, and it must check the count arithmetic** — the summed reported
>   iterations times 32 equalling the r0 advance — because reporting a count is the whole point
>   of counting it, and that arithmetic is the one piece of genuinely untested logic this round
>   ships.
> - **Rows for `xchg` and `scanc`** as well, which also received markers but no rows. Their
>   programs already exist in committed probes, so the additions are mechanical.
> - **`scanc`'s pair must include a "bail silent" row** — second-load page miss, marker count
>   0. This is the only arrangement that can detect a marker placed before or between the two
>   bail-outs, because a `fires` row alone prints in either placement. Without it the
>   placement argument rests on review, not on a row.
> - **`memcpy`'s row should check the count arithmetic** — the summed reported iterations
>   times 32 equalling the r0 advance — since reporting a count is the stated point of
>   counting it.
> - **Tighten the `fires` rows from `>= 1` to `== 1`** where the program's construction
>   warrants exactly one line, per this project's expect-an-exact-small-nonzero-value lesson;
>   it would surface a double-fire anomaly that `>= 1` accepts.
>
> **Recorded, not fixed:** `netbsd_memset` gets no marker because it is dead (its arming is
> overwritten by the compare-and-branch catch-all), and this round will not ship an
> instrument that cannot be exercised. The 17 micro-folds are excluded because a marker per
> compare-and-branch would make raised verbosity unusable for everything else, including
> these new rows. And the markers add a varargs call plus a few branches per fold dispatch at
> default verbosity — the accepted price of the no-pre-gate convention, unmeasured here, and
> the first suspect to eliminate if the known gate-14 timing flake's rate shifts.

> ## 2026-08-11 — #19 SETTLED from the ARM ARM: the TEMPLATE is the defect, and the folds were right
> The question the correction block above left open ("settle the post-index writeback from
> a primary source") is answered, and the answer confirms the inversion: GXemul's
> load/store template is the simplification, and the two folds that write an unmasked base
> were closer to the architecture than the code they were measured against. The two queued
> "mask the base on entry" fixes are **cancelled**; shipping them would have
> institutionalised the bug.
>
> **ARM Architecture Reference Manual, ARM DDI 0100I (July 2005):**
> - **A5.2.8, immediate post-indexed** (p. A5-28): `address = Rn`, then
>   `if ConditionPassed(cond) then Rn = Rn + offset_12`. Both the memory address and the
>   writeback read the **raw** `Rn`. A5.2.9 (`Rn = Rn + Rm`), A5.2.10 (scaled) and A5.3.6
>   (halfword, `Rn = Rn ± offset_8`) are identical in shape.
> - **A5.2.5, immediate pre-indexed** (p. A5-24): `address = Rn + offset_12`, then
>   `Rn = address` — the **unmasked** calculated address. So the pre-index arm is wrong for
>   the same reason as the post-index arm, which the original finding had not noticed.
> - **A2-43** puts the truncation in the memory interface, not the register: "When an
>   instruction ignores the low-order address bits that make an access unaligned, the
>   pseudo-code in the instruction description does not mask them out explicitly. Instead,
>   the `Memory[<address>,<size>]` function used in the pseudo-code masks them out
>   implicitly." Where the manual *does* force a value it says so plainly — LDC "ignores the
>   least significant two bits of the address" — and it never says anything comparable about
>   a base register.
> - **A4.1.31 LDRT**: only post-indexed forms exist, using W == 1 instead of 0, but "the
>   addressing mode is the same in all other respects", so `ldrt`/`strt` inherit A5.2.8
>   unchanged. Only privilege differs.
> - **Version-independent.** LDR/LDRT/STR/STRT are all "Architecture version: All"; the
>   v4-to-v5 delta in LDR is only for `Rd == PC`; ARMv6's CP15 U bit changes the **data**
>   path, never the writeback. So no per-CPU-model split is needed, which matters because
>   `arm_cpu_types.h` spans ARMv3 through ARMv7 on one code path.
> - Supporting, from two review seats: the ARMv7 **Base Updated Abort** model writes back
>   `Rn + offset` even when the access aborts, which is hard to reconcile with a masked
>   writeback; and had masking been intended, A5.2.8 would read
>   `Rn = (Rn AND NOT 3) + offset_12`.
>
> **Honest limit, recorded rather than glossed:** no silicon document states the writeback
> value for an unaligned post-indexed access. The SA-1110 Developer's Manual (§7 MMU) and
> the ARM920T TRM (§3.7.1) both defer to the ARM ARM on alignment behaviour and add nothing
> about the base register. This conclusion therefore rests on the ARM ARM pseudocode being
> normative plus the absence of any contradicting silicon text — strong, but not
> independently silicon-confirmed.
>
> **Four sites, all wrong the same way, in `cpus/cpu_arm_instr_loadstore.c`,** and four is
> the whole set by enumeration, not by argument: `reg(ic->arg[0]) =` appears at :213 and
> :216 (general path) and :338 and :342 (fast path), and `A__NAME_PC` plus every conditional
> variant (`__eq`, `__ne`, …) merely *call* `A__NAME`. Two review seats suspected the PC
> special case held a third copy; it does not. The general path computes `addr` at :118-122,
> masks it at :124 (`addr &= ~(datalen - 1)`), and writes the base back from the masked
> value; the fast path repeats both, masking at :283/:292 (halfword/word load) and
> :310/:319 (store). One variable is serving two purposes — the memory index and the
> writeback source.
>
> **The reachable symptom is not a wrong value, it is a loop that stops advancing.** The
> masked writeback latches the base's low bits after one iteration: `b → (b & ~(d-1)) +
> offset` drives the residue to `offset & (d-1)` and holds it there, so from the second
> iteration the loop advances by exactly `offset & ~(d-1)` — the offset truncated down to a
> multiple of the access size. When the offset is SMALLER than the access size that advance
> is zero and the base is a **fixed point**: `ldr r1,[r0],#1` with `r0 = 0x10001` masks to
> `0x10000`, adds 1, and writes back `0x10001` — the value it started from. (A review seat
> caught an earlier, overbroad claim that *any* non-multiple offset gives a fixed point:
> offset 5 on a word access advances by 4 per iteration, not 0. The law above was checked
> against the iteration map, and it also explains the aligned case — first step 1, every
> later step 0.) Measured on the committed build
> (`_scratchpad/r104b_writeback_probe.py`, 11 rows, **5 pass**): ten iterations left `r0` at
> `0x00010001` where the architecture gives `0x1000b`, and entering the same loop **aligned**
> still wedges — one step reaches the fixed point and then never moves. Post-index `#4` from
> an unaligned base gave `0x10004` (architectural `0x10005`), pre-index `#4` with W == 1 the
> same, and a **negative** offset gave `0x0000fffc` (architectural `0x0000fffd`). The
> **halfword** form is a fixed point too (`0x10001` for `ldrh r1,[r0],#1`), so the `~1`
> sites are not a lesser variant. Four controls held: aligned post-index, aligned loaded
> data, the byte path (where `datalen == 1` makes the mask a no-op), and pre-index with
> W == 0 (no writeback at all). A fifth control refuted a suspected second defect a seat
> asked to measure: there is **no 32-bit/64-bit width bug** in the offset arithmetic —
> a negative offset wrapping from base 0 already reads `0xfffffffc` on the buggy build.
>
> **Reachability from real guest code, stated honestly:** NetBSD's `copyin`/`copyout`
> (`sys/arch/arm/arm/bcopyinout.S`) test the source alignment and branch away before the
> six-`ldrt` block the folds match — `ands r3, r0, #0x03 / bne .Licleanup` — so the base is
> provably word-aligned whenever those folds run, and the divergence they exhibit is
> reachable only from hand-built programs. The template defect itself is not so confined:
> any guest using a word or halfword post-index with a non-multiple-of-size offset hits the
> fixed point, and nothing about that is NetBSD-specific.
>
> **No committed regression row pins a value this change moves**, checked before proposing
> it: every ARM probe seeds an aligned base (`mov r0,#0x9100`) and every committed
> post-index immediate is `0x20` or `0x04`, while the `strlen` walker uses `ldrb …,#1`.
> On the code side the folds (`netbsd_cacheclean`'s `r[0] += r1`, `cacheclean2`'s
> `r[0] += n << 5`, `memcpy`'s `r[0] = addr_r0 + 32`, `copyin`/`copyout`'s `+ 24`) and the
> LDM/STM `bdt_load`/`bdt_store` path all already write back **unmasked**, so the fix moves
> the template *toward* them. The cleanest statement of why the inversion is structural came
> from a review seat: `netbsd_copyin` masks the offset for the data access
> (`ofs = r0 & 0xffc`) and writes the base back unmasked (`r0 + 24`) — precisely "mask for
> the access, never for the register." **The fold was already the architecturally correct
> reference implementation.** Its single mask also equals per-access masking, because each
> of the six offsets is a multiple of 4, so `(r0 + 4k) & ~3 == (r0 & ~3) + 4k`.
>
> **Two residual risks named by the panel, neither a blocker.** Any guest code or future row
> built around the buggy masked `Rn` changes behaviour — that is the intent, not a
> regression, but it should be said out loud. And a loop that currently *terminates* only
> because the base sticks at the fixed point will now run further and could reach a
> different defect; nothing in the tree is known to do this, so it is a thing to watch
> rather than to pre-empt.
>
> **Deliberately not gated on the UNALIGNED axis, overruling three review seats:
> LDRD/STRD.** A2.8 makes a doubleword access UNPREDICTABLE prior to ARMv6 whenever the
> address is not doubleword-aligned, so *every* base that would exercise the `~7` mask
> makes the instruction unspecified. The fix does cover LDRD/STRD — the fast path chickens
> out to the general function unconditionally (the `#if defined(A__LDRD) ||
> defined(A__STRD)` at the top of `A__NAME`), which masks with `datalen - 1 == 7` — but
> that coverage cannot honestly be asserted, and #355 already taught this project not to
> build assertions on encodings the architecture declines to define. Covered on the
> unaligned axis, ungateable, recorded.
> [NARROWED by #389's pass-2, and the narrowing matters: **ALIGNED LDRD/STRD byte-order
> rows now exist** in arm_endian_probe.py, so do not read this as a blanket denial that
> LDRD/STRD can be gated at all — it is scoped to the UNALIGNED axis only. #389 narrowed
> the two OTHER copies of this rationale (gate_arm.sh, arm_writeback_probe.py) and MISSED
> this third one, which is the copy the #389 CHANGELOG block happened to cite; an Opus
> diff-review seat found it. The stale `:226-228` line cite it carried is replaced above
> with the construct's NAME rather than a new number: this file's own #357 comment already
> records that a numeric cite here has gone stale twice, and #389 made it three and four.]
>
> **Not moved by this, and deliberately kept separate:** unaligned word **loads** should
> also ROTATE the aligned word right by `8 * addr[1:0]` (A2.8 p. A2-38, A4.1.23), which this
> template does not do — measured as `0x11223344` where a rotating implementation returns
> `0x44112233`. Stores are correct as they stand (A4.1.99: "Prior to ARMv6, STR ignores the
> least significant two bits of the address. This is different from the LDR behavior") and
> unaligned halfword loads are UNPREDICTABLE (A4.1.28), so the rotation is a LOADS-ONLY item
> queued on its own. A review seat made the strongest case for folding it into this round and
> it is worth recording: leaving it out creates a window in which a future *slow-path-only*
> rotation fix would make the two paths disagree on data for unaligned loads, and since the
> combiners fall back from fast to slow, that window is exactly where a fold's fallback would
> change the visible value. The same seat supplied the tie-breaker — the rotation must be
> fixed in **both** paths in one change, and the fast path assembles bytes individually from
> `page[addr & 0xfff]`, so it is materially more work than the writeback; shipping a
> slow-path-only rotation that the fast path silently undoes would be worse than shipping
> neither. Hence a separate round, for a recorded reason rather than by reflex.
>
> **A row that would have been a trap, caught by a review seat.** The row set first carried
> a PIN asserting the loaded value `0x11223344` for an *unaligned* load — a value this file
> already documents as non-architectural. The round that fixes the rotation would invert
> that row's meaning, so the row would have to be rewritten by the very change it exists to
> guard. It now asserts the loaded data at an **aligned** base, where no rotation applies in
> any architecture version: the data path is still guarded against this round's edit, and
> nothing is pinned that the rotation round will move.
>
> **Pass-2 residuals, harvested from all eight seats.** Five were defects in this round's
> own *record* rather than its code, and were fixed rather than argued — an overclaiming
> comment counts as a defect here. (i) The fixed-point claim was too broad; the corrected
> law is above. (ii) `0xffc` is the *word* constant stated template-wide; the general form is
> `masked offset + datalen - 1 <= 0xfff`, and "this path masks later" is vacuous for the byte
> instantiations, which mask nothing. (iii) Four **stale numeric line cites** in a new
> comment — the diff shifted the mask sites by 42 lines, so `:283` came to point *into the
> comment making the claim*; this tree already carries a warning that numeric cites have gone
> stale twice in two rounds, so the cites are now symbolic. (iv) The cross-file
> "every other writeback is unmasked" claim was asserted without support; a seat then
> enumerated **every** base-writeback path in the ARM code — `arm_pop`/`arm_push`, the
> generated LDM/STM, `bdt_load`/`bdt_store` (which delegate to pop/push), and all of
> `netbsd_cacheclean`/`cacheclean2`/`copyin`/`copyout`/`memcpy`/`memset`/`strlen` — finding
> every one raw, with `ldrex`/`strex`/`swp`/`scanc` having no base writeback at all and
> LDC/STC unimplemented. The universal claim is TRUE over the full set, so it was kept and
> sourced rather than trimmed. (v) That enumeration was missing `X(strlen)`'s own base
> writeback, which is also unmasked (trivially — byte accesses mask nothing).
>
> **Two mechanism verifications worth keeping, because they underwrite the row set.** The
> row-to-site attribution ("iteration 1 takes the general path, iterations 2+ the fast path")
> is sound *by mechanism*: the generated dispatch arrays contain only the fast handler and
> its `_pc`/conditional wrappers, so the general function is reachable only through the fast
> function's own fallbacks; pass 1's access populates `host_load` via
> `update_translation_table` (`memory_rw.c:585`, which requires a full page and
> `!no_exceptions`); and — the part that could have invalidated everything — the debugger's
> `put w` seeding uses `CACHE_NONE | NO_EXCEPTIONS`, which that condition **excludes**, so
> probe seeding cannot pre-populate the arrays and make iteration 1 take the fast path.
>
> > **✗ THAT LAST CLAUSE IS BACKWARDS, and `#364` measured it.** It describes **`put b`**,
> > not `put w`. `put w` routes through `store_32bit_word` → `memory_rw` with **`CACHE_DATA`**,
> > and insertion is gated on `!no_exceptions`, so `put w` seeding **does** pre-populate the
> > translation array. `put b` is the one that uses `CACHE_NONE | NO_EXCEPTIONS` and does not.
> > This sentence is struck rather than deleted because it was recorded here as a *verified
> > mechanism* "underwriting the row set", and two shipped rounds then leaned on it: the
> > writeback probe's whole row-to-site attribution was inverted, so **`#357`'s general-path
> > writeback sites and `#362`'s general-path rotation were both unmeasured** — each
> > independently confirmed deletable with the whole of gate 14 green at 261 checks. Pinned on
> > one binary by changing only the seeding width: `put b` gave `ls_general=1` and the
> > mask-only answer, `put w` gave `ls_general=0` and the rotated answer. `#364` fixed **the
> > rotation half**: three `put b`-seeded rows, the first in that probe's history to enter
> > `A__NAME__general`. It did **not** fix the writeback half — those rows use a P=1/W=0 offset
> > form, which compiles no writeback statement at all, so `#357`'s general-path correction is
> > still unmeasured. See the `#364` residuals entry at the end of this file for what is owed.
> > A guest STORE does not substitute — `update_translation_table` sets `host_load`
> > unconditionally and gates only `host_store` on the write flag, so storing warms it for
> > loading too (measured, and it refuted the proposal that suggested it).
> Separately, the register-offset row's double `reg_func` call on the fast-to-general
> fallback is provably benign: both load and store decodes index the **s == 0** half of
> `arm_r[]`, and only the `s == 1` half writes the carry flag, so the offset function is pure
> and calling it twice is idempotent.
>
> **Still-open instrument gaps, recorded rather than implied away** (queued, with each row
> named): four of the eight generated translation units are entered by no row at all
> (`p0_u0_w1`, `p0_u1_w1`, `p1_u0_w0`, `p1_u0_w1`); every row that reaches the fast path is a
> *word* access, so the fast path's two halfword mask sites are executed by nothing; the
> negative-offset rows are single-shot, so the fast path's `!A__U` negation is untested; and
> no row asserts fast-path *data* at all — the loaded-data control is single-execution, so
> even the aligned fast-path data is unasserted, which means a future edit that fed the
> **unmasked** address to memory would still pass all fourteen rows. Also: the store
> *pre-index* sites have no row (textually shared with the load sites, and a guard-level
> divergence would be a compile error, so this is a list-only residual). The honest way to
> touch the `~7` doubleword mask is an **aligned** LDRD/STRD PIN, where masked and unmasked
> coincide, so it survives any future masking work — subject to confirming the test CPU model
> decodes LDRD at all. And `ldrt`/`strt`'s *general* site is honestly assertable while its
> *fast* site needs `is_userpage` set up first, so only the general one should be gated.
>
> **A sharpening on the DISC-M label**, which matters for how much work it is doing: under a
> CP15 A == 1 model *every* one of these rows changes expectation, since all use unaligned
> bases and real silicon would abort and restore the base. So the halfword row is not
> uniquely fragile — its uniqueness is only that its *data* is UNPREDICTABLE while its
> writeback stays defined. The word rows' mandate claim holds under the A == 0 behaviour this
> emulator actually models, which is also real silicon's reset state.
>
> **Process note, recorded so it is a decision and not an oversight.** The standing
> instruction for this project asks for a `REVIEW_FINDINGS.md` row per correction, and a seat
> flagged its absence for #357. `REVIEW_FINDINGS.md` is a one-time examination report with a
> declared scope ("framework + loaders + a `-fanalyzer` sweep of all TUs") whose last
> correction entry is **#290**; every correction from #291 to #356 is recorded in the
> CHANGELOG round blocks and here instead. Adding a lone #357 row to a document that stops
> 66 corrections earlier would misrepresent both. #357 therefore follows the established
> recent practice, and the discrepancy between the instruction and the repository is recorded
> here for whoever reconciles them.
>
> **Related, recorded from the same reading:** CP15's A (alignment fault) bit is decorative
> in this tree — `ARM_CONTROL_ALIGN` is read only to be printed (`cpu_arm_coproc.c:144-147`,
> `cpu_arm.c:474`), so no alignment exception can ever be raised — while `cpu_arm.c:129` ORs
> `ARM_CONTROL_ALIGN` into the initial control value, which contradicts SA-1110 reset state
> ("At the end of the reset sequence … Alignment faults are also disabled"). Because A == 0
> on real silicon, hardware rotates silently rather than faulting, which is what makes the
> rotation the reachable behaviour rather than an exception. And a sibling question worth not
> losing: PowerPC's update forms (`lbzu` and friends) do `ra = ea`, so if `ea` is masked
> before that assignment it is the same mistake in a sibling template — queued, with the
> caveat that PPC's alignment rules are not ARM's and the template may not mask at all.

> ## 2026-08-11 — the rest of the ARM alignment family, SETTLED from DDI 0100I: one real fix, one new defect, four non-defects
>
> `#362` fixed the unaligned word **load**. The research that produced it left four sibling
> questions marked "unverified", and reading the primary source rather than reasoning outward
> from `#362`'s answer settles all four — in three different directions, which is the point.
> One expectation of mine was **wrong**, and the correction changes what the fix is allowed
> to claim.
>
> **`swp` is a real defect with a MANDATED answer — a fix, not a `#355`-style record-and-leave.**
> I had guessed this might land as UNPREDICTABLE. It does not. A4.1.108 (pp. A4-212/213) gives
> the pseudocode as `temp = Memory[address,4] Rotate_Right (8 * address[1:0])` followed by
> `Memory[address,4] = Rm` when the CP15 U bit is 0, and its Alignment note says outright that
> "the alignment rules are the same as for an LDR on the read and an STR on the write". So the
> two halves obey **different** rules, which is exactly why this instruction looked like a third
> model: the load half rotates like LDR (A4.1.23), the store half ignores `addr[1:0]` like STR
> (A4.1.99, which says "This is different from the LDR behavior"). Table A2-9 (p. A2-39) files
> SWP in **both** the WLoad and WStore rows, and Table A2-10 (p. A2-40) gives WLoad "Loaded data
> rotated right by 8 * Addr[1:0] bits" against WStore "Operation unaffected by Addr[1:0]" at
> U=0/A=0. The measured before-state already satisfies test-first: `swp r1,r2,[0x10001]` with
> `r2 = 0xff` returned `r1 = 0x88112233` where the rotate answer is `0x44112233`, and the store
> crossed the word boundary, leaving `[0x10000] = 0x0000ff44` and `[0x10004] = 0x55667700`
> where `[0x10004]` must be **untouched**. The fix cannot regress aligned guests: rotate and
> mask are both the identity when `addr[1:0] == 0`. **[Done as #386, 2026-08-12 — plus the
> byte-order half the queue item led with (X(swp) was LE-only on BOTH assemble and emit):
> all three shipped together, and the committed P+4 sentinel row formalizes exactly this
> entry's crossed-the-boundary measurement. See the 2026-08-12 entry.]**
>
> **`swpb` is a NON-DEFECT.** A4.1.109 (pp. A4-214/215) carries no Alignment note at all, and
> Tables A2-9/A2-10 file SWPB in the Byte row, Normal for every combination. Closed with a
> citation, which is worth as much as a fix and costs a paragraph.
>
> **`ldrex`/`strex`: MY EXPECTATION WAS WRONG, and the honest framing changes with it.** I had
> assumed the alignment fault was mandatory regardless of the A bit. A4.1.27 (p. A4-53) and
> A4.1.103 (p. A4-203) both say: "If CP15 register 1(A,U) != (0,0) and Rd<1:0> != 0b00, an
> alignment exception will be taken. There is no support for unaligned Load Exclusive. If
> Rd<1:0> != 0b00 and (A,U) = (0,0), the result is UNPREDICTABLE." Table A2-10's WSync rows
> agree — only U=1 or A=1 give an Alignment Fault. This tree sits permanently at (A,U) = (0,0),
> so unaligned LDREX/STREX is **UNPREDICTABLE here**. Two caveats. `Rd<1:0>` is a manual typo
> for `Rn` — the pseudocode reads `Memory[Rn,4]`, and SWP's own note on p. A4-213 says `Rn[1:0]`
> correctly. And the **halt is still wrong**, because UNPREDICTABLE licenses any architectural
> outcome and stopping the machine is not one; that is precisely `#312`'s finding. But raising a
> data abort is a **choice under latitude**, not a mandated fault, and the record must say so —
> "chose the A=1/U=1 behaviour under UNPREDICTABLE latitude", never "implemented the mandated
> fault". It remains the better choice: it is what a checking part does, and the only outcome a
> guest handler can observe. Machinery exists and nothing needs building. `arm_exception()` is
> directly callable from a handler; copy the `X(swi)`/`X(bkpt)`/`X(und)` idiom. **Two mechanical
> requirements**: it ends with `quick_pc_to_pointers()`, so the handler must **not** also set
> `next_ic`; and for `ARM_EXCEPTION_DATA_ABT` it adds 4 on top of the usual 4, giving
> `r14_abt = pc + 8`, the architectural data-abort return address. Set `far` to the faulting
> address and `fsr` to `FAULT_ALIGN_0` (0x01, already in `thirdparty/armreg.h`; Table B4-1
> p. B4-20 gives Alignment as FS 0b00001 with Domain Invalid, so the domain term is 0). Whatever
> replaces the halt must not merely **delete** the guard: the raw addresses at the
> `ldrex`/`strex` `memory_rw` calls are unreachable only while the guard stands.
>
> **NEW DEFECT — `ldm`/`stm` answer the alignment question two ways depending on whether the
> page is mapped.** This **supersedes** the note above that recorded the LDM/STM wording as
> unverified. `arm_pop` and `arm_push` take an unmasked address from the base register and then
> the two paths disagree: the **fast** path indexes `p32[(addr & 0xfff) >> 2]`, and that `>> 2`
> truncates `addr[1:0]`, which **is** the architectural answer; the **slow** path hands the raw
> `addr` straight to `memory_rw`, which aligns nothing, producing a true unaligned access. One
> instruction, two answers, selected by page residency — the same fast/slow asymmetry class as
> the `#362` family, and a self-disagreement rather than a uniform wrong answer. Now citable:
> LDM (1) A4.1.20 p. A4-37 — "For CP15_reg1_Ubit == 0, the Load Multiple instructions ignore
> the least significant two bits of the address"; STM (1) A4.1.97 p. A4-190 — "the STM[1]
> instruction ignores the least significant two bits of address"; and Table A2-10 p. A2-40
> gives Multi-word at U=0/A=0 as "Operation unaffected by Addr[1:0]". So the correct behaviour
> is what the fast path already does, and it is **not** UNPREDICTABLE as previously recorded
> here. **The fix is a mask at the access only**, and the trap is one this project has already
> paid for twice: masking `addr` at **entry** would corrupt the base writeback, because that
> writeback assigns the running `addr` back to the base register and `#357` established the
> writeback must use the **unmasked** value. **Measurement caveat that will otherwise produce a
> false pass:** proving this requires reaching the slow path, i.e. a page absent from
> `host_load`/`host_store` — the same trap that made `arm_writeback_probe.py`'s path-coverage
> docstring false, since `put w` warms the mapping and `put b` does not. A cold-page or
> `put b`-seeded row is mandatory, or the probe measures the already-correct fast path and
> reports green.
>
> **The three masked Thumb paths are NON-DEFECTS, and `#362`'s rotate must NOT be propagated
> into them.** This is the sibling-transfer trap in the flesh: the natural move after `#362` is
> to sweep for other masks and rotate them all, and here that would inject a defect. Thumb
> LDR (1) A7.1.28 (p. A7-47) makes an unaligned load's data UNPREDICTABLE, and Thumb PUSH/STMIA
> "ignore the least significant two bits", so masking is legal in all three. Honest tension to
> record rather than resolve: Table A2-9 files Thumb LDR under WLoad, whose U=0/A=0 row says
> rotate, while the instruction page says UNPREDICTABLE — masking is within latitude under
> either reading, so the code is safe either way.
>
> **One memory-layer observation, worth the round even though it is not the defect.**
> `memory_rw` masks only the page base for the host-block lookup and keeps the byte offset
> verbatim, so an unaligned access straddling a 4 KB page boundary is **translated once**: the
> tail bytes come from the physical continuation of the first page's host block, and the second
> page's translation and permission check never happen. There is no host out-of-bounds —
> `#165`'s guard splits any access crossing a 1 MB memblock — so this is a correctness defect
> and not a memory-safety one. It is an additional argument for masking at the access rather
> than teaching the memory layer to perform unaligned transfers.
>
> **Sequencing: two rounds, `swp` first.** [#387 note: the swp round is DONE (#386);
> the `ldrex`-halt half is what remains of this pairing.] They look like one family but are findings with
> incompatible justifications — mandated answer versus UNPREDICTABLE latitude — so one
> CHANGELOG block cannot honestly state both. `swp` also needs no new machinery and cannot
> regress aligned guests, while `ldrex` needs a real exception path.

> ## 2026-08-11 — `gate_ab` fails under host load, and its failure is indistinguishable from a real regression
>
> Found while gating round 108, and recorded here rather than in that round's block because it
> is a **harness** defect the round merely tripped over. `#362`'s battery came back
> `REGRESS_FAIL` at 14/15. The failure was **not** gate 14, the round's own gate, which passed;
> it was gate 7, `gate_ab`, on "HEAD boots luna88k to a login prompt". HEAD returned `1:1:0`,
> stopping at "Automatic boot in progress: starting file system checks", while the pre-batch
> baseline reached `login:`.
>
> **Settled by measurement, not by argument.** Re-running `gate_ab` alone on a quiet machine
> returned HEAD `1:1:1`, matching prebatch `1:1:1` — gate PASS, 5 checks. The round under test
> could not have caused it in any case: `#362` touches only `cpu_arm_instr.c` and
> `cpu_arm_instr_loadstore.c`, and **m88k compiles no ARM code**. Corroborating the load claim
> unusually directly: during the battery a bare `ls` under WSL took **over 120 seconds**, with
> two research subagents and interactive commands running concurrently.
>
> **The defect is not the budget, it is that the failure is unfalsifiable.** `gate_ab` gives
> each luna88k boot `run_emu 300`, and the gate's own header records the normal boot as "about
> 100 s against a 300 s budget, so this was never a marginal timeout". That measurement is true
> on a **quiet** machine and false in general — a 3× margin does not survive a loaded host. But
> raising the budget alone would be the wrong correction, because the real problem is the
> **shape** of the failure: a timeout and a genuine capability regression both produce `1:1:0`,
> so the gate cannot distinguish "the guest never reached login" from "the guest was still
> booting when we killed it". That is the same class as the `A strlen alias moved` row in the
> gate-14 flake work — a check that fails to a value indistinguishable from the defect it
> guards manufactures a phantom regression, which is worse than missing a real one. And it does
> the specific damage this project keeps fighting: an unexplained red row in the battery that
> underwrites the shipped corrections teaches the reader to dismiss red rows.
>
> **Correction, two parts, the second being the load-bearing one:** raise the luna88k budget,
> but justify the number by measuring the boot under deliberate load rather than picking a round
> figure; and make the timeout **distinguishable** — `timeout(1)` exits 124, so `luna_markers`
> can report whether the emulator exited on its own or was killed, and assert a distinct
> "boot TIMED OUT at N s — inconclusive, not a regression" rather than falling through to the
> same `1:1:0` a real regression produces. An **inconclusive** verdict is the honest outcome for
> a wall-clock oracle that ran out of time, and `gate_ab` already has a `degrade` helper for the
> adjacent "did not run" case (image absent).
>
> **Sweep the siblings in the same round** rather than fixing one gate: any row whose oracle is
> a wall-clock budget shares this defect. To check — `gate_ppc_halt` and `gate_sh_halt` (both
> assert a guest does *not* halt within a window), the ARM probes' grace constants, and every
> `run_emu <n>` whose `n` was chosen against a quiet-machine measurement. General rule worth
> stating once: **a wall-clock budget is a load-sensitive oracle**, so either it reports timeout
> separately from failure, or its margin is justified against a loaded host and not a quiet one.
>
> **Operational rule this establishes, now in `CLAUDE.md`:** do not run panel seats, subagents,
> or other CPU-heavy work while a wall-clock-budgeted gate or battery is running. This is
> strictly stronger than the existing "never two gate/harness invocations at once" — the
> contending work here was not another gate, it was ordinary read-only research, and it still
> produced a false FAIL in a 45-minute battery.

> ## 2026-08-11 — `#363` residuals: what the gate-14 flake round deliberately left, and two seat claims that were refuted
>
> `#363` closed the flake mechanism — the prompt predicate now matches the full `GXemul>`
> rather than a bare `>` at all thirteen sites. What follows is what it did **not** do, and why
> each is separate rather than forgotten.
>
> **The stale-prompt false positive is still live in `arm_flags_probe.py`, and it is
> DETERMINISTIC, not a race.** Two whole-buffer waits remain (the one inside `session()` and the
> one inside `run_cc_nonmult`; `wait_past_mark` anchors only the post-`continue` wait). After any
> completed command `buf` **ends** with the prompt — so the next `send()` writes its bytes, calls
> `wait()`, immediately sees the *previous* command's prompt at the end of the buffer, and returns
> without waiting for the new command's output at all. Every `send()` after the first therefore
> returns instantly, and roughly 1500 commands stream into the 4 KB console FIFO instead of being
> round-tripped. **The probe's correctness currently relies on FIFO depth**, an implementation
> detail of `console.c`. Round 100 anchored the other five probes and never back-ported it here.
> Held out of `#363` for a reason that matters: the claim above is deterministic and therefore
> cheap to measure (count `send()` calls returning with zero new bytes in their own slice —
> prediction: nearly all of them), and it has **not been measured yet**. This project ships fixes
> whose effect was measured and documents the rest. Expect the fix to make gate 14 **slower** by
> tens of seconds, and record that, or the next reader will misread it as a regression.
>
> **`send()`'s return value is discarded at essentially every call site**, and in
> `arm_flags_probe.py`'s `session()` it is not even returned. A prompt that never arrived is
> indistinguishable from one that did. `if not send(cmd): return None` is smaller and more
> general than the retry loops below, and is the root defect underneath them.
>
> **Six reads still have no retry** while every other `dump` read retries three times: the three
> `reg` reads (`run_cc_nonmult`'s r0/r1, idle's r2/cpsr, strlen's r3), the two `print` loops
> (writeback's per-row register, fold-marker's ten registers), and the one the first scoping
> missed — fold-marker's **single-shot `dump`** of the copyout destination, whose truncation fails
> `A fold copyout fires` through `mem_ok=False`. The retry predicate must be **consumer-keyed**
> ("r2 present in this slice", "r0 AND r1 present"), mirroring the dump loops' `len(flat) >=
> nwords`; a retry keyed on "prompt seen" re-fires on the same truncation and changes nothing.
> Safe because re-sending a read to a stopped guest is idempotent, and because the absence rows
> are **verbosity**-gated rather than timing-gated — `A idle quiet` counts a `VERBOSITY_DEBUG`
> marker in a session run at default verbosity, where it cannot be emitted at all, so no amount
> of extra waiting can make it appear. Rule for the code: **never put `continue` or `step` inside
> a retry loop.** One wart in the *existing* loops while there: if attempt 1's output straggles
> into attempt 2's window, `buf[mark:]` holds tail-of-1 plus all-of-2 and `flat[0]` is the wrong
> word — parse from the **last** dump block in the segment.
>
> **The durable instrument, and the highest-value item left.** Have each probe count reads that
> had to be retried or came back unparseable, print `<probe>_READS_RETRIED=n`, and add
> `check "<probe> reads not retried" "$n" 0`. That makes the *next* flake self-identifying rather
> than costing a panel and a 45-minute battery, and converts the whole class from "intermittent
> red row of unknown origin" into a named, counted quantity.
>
> **Two small hardening items.** `gate_arm.sh` should `unset CLICOLOR`: `use_colorized_output()`
> requires `isatty(0) && isatty(1) && enable_colorized_output`, and **both** isatty checks DO pass
> under `pty.fork()` — so the probes' `-A` flag is load-bearing rather than decorative, and is
> currently the only thing keeping colour escapes out of the parsed output. And the enumeration
> "no site legitimately depends on a non-prompt `>`" is the load-bearing safety argument for
> `#363` and should live in a probe comment, not only in a review.
>
> **Two seat claims checked and REFUTED, recorded so nobody re-derives them.** One seat held that
> `#362`'s fast-path rotation has no `#if defined(A__L)` guard and would therefore rotate byte and
> halfword loads. It does not: the rotation sits in the `#else` of **both** `#ifdef A__B` and
> `#ifdef A__H`, so the guard is structural through the nested `#ifdef` chain rather than a fresh
> `#if` on the hunk — the seat read the diff without its enclosing context. Another held that
> `#362`'s guard might have caught `SWP`. It cannot: `SWP` is not instantiated through that
> template at all but is a standalone `X(swp)` handler, and the template's own header says so
> ("ldrex/strex/swp/scanc have no base writeback"). Both were confident and specific, which is
> exactly why the standing rule is to check rather than count votes.
>
> **One premise of `#363`'s own brief was false**, and the correction is the more useful half:
> the brief claimed `< no symbol >` is the ONLY `>`-terminated line in these sessions, eliminating
> the disassembly because its `<%s>` sites are symbol-guarded. They are not — the `else` branch
> prints `<0x%08x` with no guard and `debug(">")` closes it unconditionally, and both
> `DISASSEMBLE` call sites pass `running = 1`. So any breakpoint landing on an `ldr`/`str` emits a
> second `>`-terminated line; it is unarmed only because every breakpoint in these probes happens
> to target a `NOP`, which is a property of the probes and enforced by nothing. `dump`'s ASCII
> column is a third source, unarmed only by today's seed constants. This collapsed the brief's
> "only `reg` can do this" narrowing — and is simultaneously the strongest argument for the fix,
> which the brief had failed to make.

> ## 2026-08-11 — ✅ `#295` has NO committed detector, and the mutant that reverts it passes the whole battery → RESOLVED as #376
>
> **(2026-08-12, round 117.)** `regress/mips_fixedmode_probe.py` (14 rows × both rigs, every
> discriminating row under non-zero FCSR.RM), gate 12 section 3 (21 → 53 checks, single clean
> run green), and `regress/selftest_mutation_295.sh` (full-build /tmp mutation test — measured
> M295MUT_PASS with the exact per-op flip matrix, three mutants). Two of the one-off probe's
> rows were born vacuous against the primary mutant and were re-moded before promotion; the
> ctc1-witness is the `cvt.w.d`+`cfc1` pair (trunc cannot witness it — mode-immune). See the
> #376 CHANGELOG block for the panel adjudication and the two measurement incidents.
>
> Found while scoping what turned out to be an already-fixed queue item (the 2026-07-30 entry
> above, now marked resolved). The correction is real and shipped; the **instrument is absent**.
> Measured: `grep -rn "295\|round\.w\|ceil\.w\|floor\.w" regress/` returns **nothing**. Gate 12
> (`gate_mips_rounding.sh`) covers `#301`'s `cvt.d.l`/`cvt.s.l` and `#303`/`#309`'s
> subnormal-decode plus REGIMM, and nothing of `#295`. The round's own 20/20 verification was a
> one-off `_scratchpad/probe_295_fixedmode.py` with `mutant_295*.sh` alongside — none committed,
> none wired into `run.sh`.
>
> **This is worse than an ordinary coverage gap, and it is the sharpest instance of the class
> this project keeps finding.** `#295`'s own design note records that the likeliest wrong
> implementation — a copy-paste passing `FPU_RM_FROM_FCSR` instead of the forced mode — **agrees
> with correct code on every input under the default `FCSR.RM = 0`**. So the mutant is not merely
> undetected, it is **undetectable** by any row that does not first set a non-zero rounding mode.
> Every new row must do so or it is *born vacuous*. That is a fifth entry in the vacuity
> taxonomy: not an absent row, and not a row asserting a dead absence, but a row whose **oracle
> cannot separate the mutant from the fix**. General rule: **when a correction FORCES a
> parameter, the detector must vary that parameter away from its default.**
>
> Gate 12's own header already warned about exactly this hole — "the offline vectors pin the pure
> helper, but the CVT-case WIRING in `cpu_mips_coproc.c` could revert silently while the helper
> stayed perfect" — and nobody closed it. A gate that documents its own gap is not covered.
>
> **Test-first is honest here even though the defect is an absence:** the reproduction is "build
> the `FPU_RM_FROM_FCSR` mutant, run the committed battery, watch it pass 15/15", which is
> measurable on the committed build.
>
> Discriminators the round should use, all under a **non-zero** `FCSR.RM`: `round.w(2.5) → 2` and
> `round.w(3.5) → 4` (nearest-EVEN, which also separates nearest-away); `ceil.w(−2.25) → −2`
> against `floor.w(−2.25) → −3` (the pair separates RP from RM, which a single row cannot);
> `trunc.w` invariant across all four modes; and the pinned mutation witness `round.w(2.7)` under
> toward−Inf = **3** shipped versus **2** mutant. Add a NaN row expecting `0x7fffffff`, now
> citable verbatim to R4000 B-49 ("If Invalid operation is not enabled, then no exception is
> taken and 2^31−1 is returned") and MIPS IV B-85 rather than inferred from `#273`'s measurements
> on sibling instructions — but assert the **result** and not the flag, since FCSR exception
> flags are the four-to-nil re-confirmed defer recorded above, so `round.w(NaN)` returns
> `0x7fffffff` with V clear.
>
> No booting guest can witness this: MIPS IV opcodes cannot appear in a MIPS I/III guest, `#295`
> recorded zero `UNIMPLEMENTED coproc1 function` markers across green boots, and — the reason a
> guest can never substitute — **OpenBSD 2.2's GAS *expands* `trunc.w.d`** into save-FCSR /
> `ctc1` / `cvt.w.d` / restore, so pmax binaries exercise `cvt.w` heavily and never emit the
> fixed-rounding opcodes at all. Use gate 12's cold-debugger pattern (kernel loaded so the
> machine constructs but never executed; the guest sets FCSR itself with `ctc1`) and read results
> back with two MIPS I `swc1`s, **not** `sdc1` — per `#273`'s trap, `sdc1` is itself a MIPS II
> instruction and the RI it raises is easily mistaken for the instruction under test.
>
> **One primary-source tension, assessed and NOT changed.** The R4000 manual contradicts itself
> on out-of-range converts: its instruction pages give the IEEE default (2^31−1 written to `fd`
> when Invalid Operation is not enabled), but Table 7-2 p. 191 has the row "Overflow on convert
> V E E Source out of integer range" — i.e. the R4010 raises **Unimplemented Operation in both
> the trap-enabled and trap-disabled columns**, and §7.1 says a taken trap writes no result. So
> real silicon appears to punt out-of-range converts to software completion rather than deliver
> 2^31−1 in hardware. This does **not** undermine `#273`'s five-case table, which is
> independently corroborated by Linux `arch/mips/math-emu` and pre-2014 QEMU, and it is
> unreachable while FP trap delivery is unmodelled. But it qualifies `float_emul.c`'s comment
> that "R3010/R4010 return the largest positive integer", which states an architectural default
> as though it were an implementation fact. Fix the comment's claim, not the code.

> ## 2026-08-11 — `#364` residuals: the general path is entered at last, but its WRITEBACK sites are still unmeasured
>
> This is the entry that `arm_writeback_probe.py`, `gate_arm.sh` and `#364`'s CHANGELOG block
> all point at. Written because a review pass caught all three pointing at a record that did
> not exist — the same dangling-forward-reference defect `#364` removes from the gate, created
> by the round that removed it. Recorded here rather than in CHANGELOG prose because the live
> queue is the OPEN LIST head **plus the dated tail entries**: an item that exists only in a
> CHANGELOG paragraph is off-queue.
>
> **What `#364` actually closed.** Three `put b`-seeded rows now enter `A__NAME__general` — the
> first rows in that probe's history to do so — and they exercise its **load-and-rotate** arm
> plus the `memory_rw` slow path. Before them, `#362`'s general-path rotation was deletable with
> the whole of gate 14 green at 261 checks. That half is fixed and measured.
>
> **What it did NOT close, and a draft of its own table claimed it had.** The three rows use a
> P=1/W=0 offset form, and the template emits a writeback only under `(A__P ∧ A__W)` or `(¬A__P)`
> — so an offset form compiles **no writeback statement at all**, and `wb_addr` is not even
> declared for it (`#if !defined(A__P) || defined(A__W)`). Therefore **both** general-path
> writeback sites, pre- and post-index, remain uncovered, and **`#357`'s general-path correction
> still has no row that reaches it**. Two review seats caught this independently, in the same
> direction as the original inverted note — which is the argument for keeping the two axes
> (which function a row enters, versus which writeback statement it reaches) permanently apart.
>
> > **✗ "REMAIN UNCOVERED" IS WRONG — `#365` measured it.** Both sites were already being
> > **reached**, just not from this probe: deleting their two statements turns **8 of 264**
> > checks red, in the strlen probe (`ldrb r3,[r4,#1]!` is P=1/W=1, taking the general
> > pre-index arm on each new page) and in the fold-marker probe's `copyin cold`/`copyout
> > cold` arms (six `ldrt`/`strt` with the `is_userpage` bit deliberately clear, whose
> > "advanced by 24" witness is a writeback assertion). A post-index-only mutant separates
> > them: strlen 7/7 green, exactly the two fold arms red.
> >
> > What was actually missing is **DISCRIMINATION**, and that half stands: rebuilt with the
> > *faithful* pre-`#357` bug — general writeback **re-masked**, not deleted — the whole gate
> > **passed at 264 with zero failures**, because `ldrb` has `datalen 1` so
> > `addr &= ~(datalen - 1)` is the identity, and the fold arms use aligned bases where
> > masked and unmasked agree. **Reaching a statement without discriminating its correction
> > measures nothing about it** — a fifth way a green row can mean nothing, and the subtlest:
> > the row runs the code and still cannot tell the fix from the bug. `#365` adds the two
> > rows that do discriminate, verified against that exact mutant.
>
> **Owed rows, in value order.** ✅ **Items 1 and 2 were delivered by `#365`** — marked here
> rather than left standing, because an owed-list that still names delivered work is what sent
> this project to re-derive an already-fixed MIPS item 47 rounds late. Item 4's `reg_func`
> half is **closed by construction** (see the note at the end). Items 3, 5 and 6 remain.
>
> 1. ✅ **DONE in `#365`** — **General post-index writeback — and use an `ldrt` form, not a cold page.** The project had
>    already recorded the reason and never used it: the template's
>    `#if !defined(A__P) && defined(A__W)` block tests `is_userpage[addr >> 17]` and falls into
>    `A__NAME__general` when the bit is clear, **regardless of warming**. So an `ldrt` row cannot
>    be silently voided by a future `put w`, needs no cold page, and enters `p0_u1_w1` — one of
>    the four translation units this file's own residual list says nothing enters. Assert the
>    UNMASKED base: an unaligned base of `0x10001` with offset 4 owes `0x10005`, not the masked
>    `0x10004`. Confirm the encoding through `unassemble` first.
> 2. ✅ **DONE in `#365`** — **General pre-index writeback.** No T form exists, so this one does need the cold page: a
>    cold `ldr r1,[r0,#4]!` asserting `r0`. Note the buggy value is the *base itself*, which
>    makes the row weaker than the post-index one — state that when writing it.
>    *(As shipped, the discriminating value is the masked `0x20004` against the architectural
>    `0x20005`, which is stronger than this note anticipated.)*
> 3. **The general STORE arm is owed and was named nowhere.** Loads and stores are separate
>    instantiations by this probe's own axiom, and the existing store row covers the **fast**
>    arm only. `put b` leaves `host_store` NULL too, so a cold `str` row would reach the store
>    family's `A__NAME__general` and cover its post-index writeback. Non-obvious asymmetry worth
>    recording: instruction fetch inserts with `writeflag 0`, and
>    `invalidate_translation_caches(..., JUST_MARK_AS_NON_WRITABLE)` clears `host_store` for
>    translated pages — so code pages are load-warm and store-cold.
> 4. **Other general arms** — byte, the halfword `addr &= ~1` mask, and register-offset. A
>    register-offset row is constructible (`0xE6B01002 = ldrt r1,[r0],r2`, warming-immune, or
>    `0xE6901002` from a cold base). But the `reg_func` half of this item is **✅ CLOSED BY
>    CONSTRUCTION rather than owed a row**: the recorded "the double `reg_func` call on the
>    fast-to-general fallback is provably benign" claim is **unobservable**, not unmeasured.
>    Load/store decode always indexes the low half of `arm_r[8192]`, which the generator emits
>    as the `s == 0` family, and a scan finds **4096 `s == 0` functions of which none write CPU
>    state**, against 4080 of 4096 `s == 1` that do — even the RRX case reads `ARM_F_C` and
>    writes it only under `if (s)`. No row can observe a doubled call through a pure function.
>    A closure by construction is worth as much as a row, and cheaper to keep true.
> 5. ✅ **DONE in `#368`** — **The `netbsd_copyin` rotation's body never executes.** Every fold-marker arm bases on
>    `mov r0,#0x10000`, so `r0 & 3 == 0` always. Needs a two-pass `ldrt` arm with `r0` re-seeded
>    to `0x10001`, which is a self-contradiction test on ONE binary: pass 1 declines and runs the
>    template (rotated), pass 2 folds (unrotated) unless the fold rotates too.
>    *(As shipped: THREE arms, offsets +1/+2/+3, because one offset cannot separate the
>    `& 1`-for-`& 3` and skip-at-+2 mutants; and the comparison is carried in an XOR
>    accumulator in `r1`, because pass 2 overwrites r6–r11 so a final register dump cannot
>    see pass 1 — the original one-arm read-at-end design was refuted in review. Note also
>    the sentence above describes the BROKEN build; on the shipped build both passes rotate,
>    so the healthy expectation is agreement, `r1 == 0`.)*
> 6. ✅ **DONE in `#367`** — **Permanent path telemetry, the item that stops this recurring.** Delivered as a
>    `uint64_t` counter incremented at the top of `A__NAME__general`, read out through the
>    previously-EMPTY `arm_cpu_tlbdump` stub (pull-only, so nothing prints unless asked and no
>    absence-asserting row is disturbed), with a derived expected count asserted for all 22 rows —
>    **measured 22/22 on the first run**, seventeen zeros and five ones. The seventeen zeros are
>    exactly the claim `#364` found inverted, now asserted rather than believed. `#364`'s finding needed a
>    temporary `debugmsg_cpu` marker, a scratch build and a subagent — none of which survives the
>    round, so the next false attribution costs the same again. Emit a per-row general-path entry
>    count and assert in the gate that every WARM row takes **zero** general fallbacks and every
>    COLD row takes **exactly one**. That turns "which site does this row reach" from a comment
>    into a checked quantity, and would have caught the inverted table the day it was written.
>
> **Why the cold rows still need that telemetry, i.e. why item 6 is not optional.** They pass iff
> the loaded value is rotated — which is also what the fast path yields. Warm `COLD` by any route
> the new assert does not cover and they become silent duplicates of the `rot word unal` triple
> and stay green: the exact failure shape this round exists to correct, pushed one step away.
>
> **Mechanism notes that belong with the inventory, both counter-intuitive.** The device arm of
> `memory_rw` inserts into the translation array **even under `NO_EXCEPTIONS`** — its gate is
> `update_translation_table != NULL && !(ok & MEMORY_NOT_FULL_PAGE) && (devices[i].flags &
> DM_DYNTRANS_OK)`, with no `!no_exceptions` term — so a `put b` to a fully-backed
> `DM_DYNTRANS_OK` device page warms it while the write itself is dropped. And instruction fetch
> inserts with `writeflag 0`. So "`put b` leaves a page cold" is a claim about **seeding**, not
> about a page's whole life. Two further contingencies: the array is a **384-entry round-robin
> TLB**, so any attribution is a property of a probe's working set rather than a theorem; and
> with the MMU **on**, `arm_translate_v2p_mmu` failure returns before the insertion gate, so
> `put w` would not warm an unmapped page at all — `testarm` never enables it.
>
> **Three items in the instrument-gap inventory above are now FALSE**, from the same inverted
> premise, and are struck rather than silently edited: "every row that reaches the fast path is a
> word access" (the halfword and byte rows are fast-path; only the fast **store** halfword site
> is still uncovered); "the negative-offset rows are single-shot, so `!A__U` is untested"
> (single-shot rows are fast-path, so those rows do exercise it); and "no row asserts fast-path
> DATA at all" (the aligned data control is fast-path, and `#362`'s three rot rows assert
> unaligned fast-path data). The fourth item survives and is the real residual: **four of the
> eight translation units are entered by no row** — `p0_u0_w1`, `p0_u1_w1`, `p1_u0_w0`,
> `p1_u0_w1`. A full re-audit of the inventory against the corrected premise is owed, and must be
> done by **measurement** rather than re-reading, because reasoning confidently from a plausible
> premise is precisely what produced the original note.

> ## 2026-08-11 — ✅ LDM/STM fast path ignores byte order (#372's sibling, inverted) → RESOLVED as #378
>
> **(2026-08-12, round 119.)** One line: the fast-path install gate in `cpu_arm_instr.c`
> now requires `cpu->byte_order == EMUL_LITTLE_ENDIAN` (adjudicated S3 by all seven
> answering pass-1 seats; translate-time resolution proven sound — byte_order cannot
> change post-translation). Probe 12→34 rows with explicit per-row kinds (the polarity
> here is INVERTED vs #372: warm rows discriminate), gate 14 284→295 checks, single
> clean run green. Test-first 24/34 at the exact reversed values; fixed 34/34; mutation
> proof M378MUT_PASS with the exact flip matrix. See the #378 CHANGELOG block.
>
> **LATENT-DEFECT RECORD (do not lose):** the emitted multi fast path itself remains
> ORDER-BLIND — `generate_arm_multi.c` still has no byte-order term, and 23 of its 256
> handlers load PC. On BE guests it is unreachable via the install gate's new
> `byte_order` conjunct — the load-bearing term in the normal optimized LE-host
> configuration (the enclosing `HOST_LITTLE_ENDIAN` guard, `GATHER_BDT_STATISTICS`
> and `show_trace_tree` also suppress it in other configurations, per a #379 seat;
> and note the one-armed conjunct is correct ONLY under that enclosing host guard —
> the codebase's two-armed idiom is the hardening if the guard is ever relaxed). Any
> future round that wants a live BE fast path must use the S4 shape (emit `_le`/`_be`
> variant bodies and pick at translate time, the in-tree MIPS multi precedent), and
> must in the SAME change swap the `netbsd_memcpy` fold's four raw `pw[]` publishes —
> the amended `#354` comment marks both trip-wires in the source. The
> `netbsd_copyin`/`copyout` folds keyed on GENERIC handlers, so the install gate did
> NOT close them — they were RESOLVED separately as #382 (their own byte-order swap).
> [#382 correction: an earlier version of this line called them "latent only behind
> `is_userpage` (MMU-on)". Wrong — `is_userpage` is set by the LDRT/STRT T-bit alone,
> so the folds are reachable with the MMU OFF, and #382 measured them firing on the
> barearm rig. The "MMU-on" premise was the queue item's stated blocker and it did
> not exist.]
> [Historical note, #379: the pre-resolution text below this entry retains its
> discovery-time present tense — "largest remaining", an active "Fix:" — read it
> as written 2026-08-11, before #378 shipped.]
> Found by #372's pass-2 panel and verified from source. `generate_arm_multi.c` emits the
> LDM/STM fast path as raw `r[i] = p[x]` / `p[x] = r[i]` uint32 copies with NO byte-order
> handling (grep for byte_order/swap in that generator = 0), while the general fallback
> `bdt_load`/`bdt_store` (`cpu_arm_instr.c` ~1528/~1705) explicitly swap under
> `HOST_LITTLE_ENDIAN` for a big-endian guest. Same warm/cold self-contradiction as #372,
> INVERTED: here the FAST path is wrong and the GENERAL path is right, so a BE guest's
> LDM/STM to a WARM page is byte-reversed and to a COLD page is correct (the discriminating
> rows are the warm ones, opposite of #372's cold rows). LDM/STM is emitted on every function
> prologue/epilogue, so this is the largest remaining ARM-BE defect — reachable via `-E
> barearm`, measurable with the `arm_endian_probe.py` pattern. Fix: teach the generator the
> same `bdt_load` swap idiom (reuse it verbatim so the two paths cannot drift), or fall the
> fast path through to `bdt_load` for BE guests. Guest-value impact is nil today (no BE ARM
> guest boots), so like #372 the value is self-consistency + correctness, not a repaired boot.

> ## 2026-08-12 — round 117 (#376) residuals: three committed-harness defects found by the pass-1 panel
>
> Surfaced while reviewing the #295-detector design; each is its own small round, none blocks
> anything. Harness task numbers in parentheses.
>
> - **(#55) `selftest_mutation.sh` counts a crashing mutant as detection.** Its must-fail check
>   — `check "mutant $m is DETECTED" "$out" "0"` at `:167`, fed by the `grep -c DIFF_PASS`
>   at `:154` (a pass-2 seat corrected the first draft's ":153 area" cite) — never checks
>   the mutant executable's exit status, so a mutant that crashes, times out, or emits
>   nothing yields count 0 and passes as "DETECTED" vacuously (BUILDFAIL is separately
>   caught; the crash-after-build case is not). `selftest_mutation_295.sh` already refuses this (`grep M295_RESULT= ||
>   SETUP_FAIL`); port the same discipline back. Test-first: swap a mutant binary for
>   `/bin/false` and watch the old check "detect" it.
> - **(#56) `mips_rounding_probe.py`'s readback accepts any dump-shaped line** (`:151` regex) —
>   no binding between the parsed line's address and the requested one, so a stale or
>   interleaved dump line can satisfy a row. The #376 probe binds its parse to the aligned
>   line address. Facts for any new dump parser (`debugger_cmd_dump`): the line address is
>   aligned DOWN to 16 bytes; its width follows the CPU — 8 hex digits only when
>   `c->is_32bit` (pmax/R3000), 16 digits on 64-bit CPUs (arc/R4000) — and only in-range
>   words print, in memory order. The first draft of this entry said "truncates to 32 bits"
>   unconditionally; that is pmax-only, and the probe passed on arc only because its regex
>   prefix tolerates both widths (pass-2 seat finding — a parser built from the draft's
>   guidance would break on every 64-bit CPU). Same family as the #37 prompt-predicate sweep.
> - **(#57) arc-only `.l` rows for `round.l`/`ceil.l`/`floor.l`.** The W rows prove the forced
>   constants (same source line, `to_w ? W : L`), but the L branch and the L range guard
>   (`float_emul.c` strict lower bound) have no row. Needs a 64-bit readback design that avoids
>   `sdc1`'s #273 ambiguity on nothing — arc is MIPS-III so `sdc1` is legal there, but two
>   `swc1`-visible words of an FR=1 register need the pair trick or `dmfc1`; design first.
>   Candidate discriminators (from a pass-1 seat, unverified): `round.l.d(2147483648.5)@RP`,
>   `ceil.l.d(2147483648.25)@RM`, `floor.l.d(-2147483648.25)@RP`.
>
> Also recorded: the pass-1 kimi seat produced 328 bytes (a thinking-model non-answer) and was
> counted as a SEAT FAILURE, not agreement — 7 of 8 seats answered. The `cpu_mips_coproc.c:1185`
> stale comment (claims W/L ignore the store mode and cvt.w/trunc.w are indistinguishable —
> false since #294) is folded into the existing comment-only docs task rather than forcing a
> shared-C propagation into a regress-only round.

> ## 2026-08-12 — ✅ the m88k idle fold vs bcnd.n's delay slot → RESOLVED as #380 (round 121), with two residuals
>
> The queue item (harness task #53, from #375's audit): COMBINE(idle)'s .n arm installed the
> plain-bcnd handler, so the delay slot ran zero times per taken branch — witnessed live
> (`taken got=deadbeef` on the committed build, the slot's store never landing) and fixed by a
> dedicated protocol-faithful handler; probe + gate 11 section 2 (+6 checks, 74 total) +
> two-counter mutation proof. Full mechanics in the #380 CHANGELOG block. Residuals:
>
> - **Crosspage re-entry can silently LOSE an installed idle fold until page flush**
>   (pre-existing, performance-only, found by a #380 pass-1 seat): a crosspage-delay-slot
>   entry into the loop head re-translates the tb1's ic via `end_of_page`, the dyntrans
>   special case then resets it `TO_BE_TRANSLATED`, and a later plain re-translation of the
>   tb1 never re-fires the matcher — only bcnd words arm `combination_check`. The loop then
>   spins un-folded (correct results, no idle sleep) until the page is flushed. Affects all
>   three arms; worth a one-line fix only if a real guest measurably hits it.
> - **The elided tb1 privilege check is now closed by construction, unmeasured** (#380 added
>   `vector >= M88K_EXCEPTION_USER_TRAPS_START` to both tb1 arms): a user-mode guest whose
>   idle-shaped loop used a vector below 128 would have had its PRIVILEGE_VIOLATION silently
>   dropped by the fast path. No such guest exists on the rigs (the matched sequences use
>   0xff), so the conjunct has no live install to measure against — recorded as
>   by-construction, the honest label for a fix whose defect cannot be reproduced on any rig.
>
> **#381 additions to the residual list** (pass-2 findings; the two above stand):
> - **The once-per-BREAK approximation is itself a recorded semantic limitation, not just a
>   comment**: for a matcher-accepted slot that is accumulating, MMIO, order-sensitive, or
>   one that WRITES THE POLLED WORD (arm 3 is the first arm whose elided instruction can —
>   `tb1`/`ld` cannot), the collapsed spin diverges from per-iteration execution; a
>   polled-word-writing slot still arms one idle sleep decided from the PRE-slot value.
>   Exact for the live guests' loop-invariant `or`; listed so the next matcher widening
>   re-derives nothing.
> - **The crosspage fold-loss residual above is narrower than it reads**: the reset path
>   requires `low_pc == 0`, so the fold is lost only when the loop-head `tb1` sits at page
>   index 0 AND a `.n` branch ends the previous page with it as its slot — strengthening the
>   performance-only triage.

> ## 2026-08-12 — ✅ netbsd_copyin/copyout folds ignore guest byte order (task #17) → RESOLVED as #382, #383
>
> The live half: both folds moved six raw host words with no byte-order term while the
> template they delegate to is order-aware since #372 — the #342/#355 class, and (unlike
> memset/memcpy) NOT closed by #378's install gate because their matchers key on the
> GENERIC load/store_w1_word handler. Fixed by the same open-coded swap arm_push/arm_pop
> use (copyin in place before #362's rotation; copyout capture-then-swap since q32 aliases
> live r6..r11). Probe: 4 barearm rows (copyin two-pass XOR at +0/+1/+3 — the unaligned
> ones are the swap-before-rotation discriminators — and a raw-byte copyout row) +
> FOLDMARK_CONTROL_BE; gate 14 17 → 21 fold-marker rows; three-mutant proof (M383MUT_PASS).
> Full mechanics + the three record corrections in the #382/#383 CHANGELOG block (#383 = the swap, #382 = the record corrections; see the block header).
>
> **Two premises this round retired, both were wrong records:**
> - Reachability: the folds are reachable with the MMU OFF (is_userpage is set by the
>   LDRT/STRT T-bit, not by MMU state) — MEASURED firing on barearm. The queue item's
>   "(MMU-on)" blocker did not exist.
> - The "unmasked base writeback" half of task #17 is VOID: post-#357 the template also
>   writes the unmasked base, so the folds' r0+24/r1+24 agree exactly. Nothing witnesses a
>   divergence because there is none. Resolved-by-#357, not measured.
> Plus the load-vs-host_store comment fix (a load-only warm-up leaving host_store NULL
> holds only MMU-on + read-only; MMU-off a load sets it too) at cpu_arm_instr.c and the
> fold-marker probe. A sweep of #360/#367 records for the same wrong claim is a follow-up
> for task #43's OUTSTANDING re-audit. **[Done as #385, 2026-08-12 — the sweep found the
> #367 CHANGELOG block and `arm_writeback_probe.py` still carrying the claim (both corrected
> in place), the #379 "(MMU-on)" premise un-annotated (marked), #360's records CLEAN (no
> instance of the wrong claim — verified by grep in the pass-2 review), and NO load-bearing
> instance anywhere: every committed `LSGEN` expectation was already `1`. See the 2026-08-12
> entry.]**

> ## 2026-08-12 — #385 (round 125): the records re-audit (queue task #43) — no committed expectation was wrong, six records were
>
> Docs and comments only — no emulator code, no probe assertion, no gate expectation
> changed. A read-only audit swept this file, the CHANGELOG, REVIEW_FINDINGS.md and the
> probe comments against source ground truth, with the mechanism re-verified once at
> `cpu_dyntrans.c:1595-1596` (host_store = writeflag ? page : NULL), `memory_rw.c:585-589`
> (data-access writeflag = ok-1), `memory_arm.c:54-60` (MMU-off translate returns 2, so
> ok-1 == 1 for ANY data access — a load warms host_store too).
>
> **Headline: no load-bearing records error.** Every committed `LSGEN` expectation is `1`
> and none rests on the audited claims. (The six wrong records: the probe derivation
> comment, the #367 block's claim, the #379 premise, the head index, the TST/TEQ blocker,
> the memcpy wording. The REVIEW_FINDINGS freeze was deliberate and recorded — under-
> surfaced, not wrong, so not counted.) Corrected, in rank order:
> - the host_store family's last two live sites — `arm_writeback_probe.py`'s derivation
>   comment ("iff the access was a write" → any-data-access-MMU-off; "load then store on
>   one page is 2" → 1, it is 2 only MMU-on on a read-only page) and the #367 CHANGELOG
>   block (annotated `[#382 correction]` in place, not rewritten); plus the #379 block's
>   retracted "(MMU-on)" premise (forward-marker to #382);
> - the OPEN-LIST head brought current — honest status paragraph, the post-2026-08-01
>   open-residuals block (four open residual families previously visible only down here;
>   the fifth tail family, the #382 records sweep, is this round itself — it closes rather
>   than opens), the stale "still diverging" sentence updated (idle/memcpy both since
>   resolved);
> - the TST/TEQ-carry entry re-filed (its "no positive control exists" blocker predates
>   #340/#358; now: reproducible, defect-status UNMEASURED — no claim it is fixed);
> - the memcpy-fold wording made precise ("never stored into" → never warmed by any data
>   access; read-only-page remark tagged MMU-on-only; the recorded 255/255-genuine
>   measurement re-filed UNRECONCILED with the corrected mechanism — a cold source should
>   self-warm on the first delegated iteration — re-measurement queued);
> - REVIEW_FINDINGS.md's freeze banner (frozen at #290 per the recorded 2026-08-11
>   decision); the carrier's "row per correction" line now points at it (local-only file).
>
> **Assessed, not changed:** the ~30 ticked/struck head entries stay in place (clutter,
> not a trap — a ticked entry cannot be re-worked by mistake; mass removal was judged too
> deletion-risky for a records round); #366 keeps its inline-annotation record inside the
> #365 block (real commit `0aceec2`, citations resolve, nothing dangles).
>
> **Pass 2 (seven seats), fixes landed pre-commit:** the five-vs-four family count (four
> seats convergent), the "iff write … only MMU-on" restatement in the round's own block
> (the flag tracks page writability in every mode), the memcpy 255/255 re-endorsement
> (re-filed UNRECONCILED, re-measurement queued), the REVIEW_FINDINGS date line, the
> #360-records-clean clause. Refuted seat claims: a fabricated "word[*]" quote; a
> "wrong filename" (`arm_endian_probe.py`) that exists and carries the corrected fact.
> [#386 correction: the "word[*]" refutation belongs to the CONCURRENT #29 pass-1 panel,
> not to this round's pass-2 — only the wrong-filename claim was refuted here.] [#387:
> and "fabricated" is softened to "misattributed" — the `word[*]` tokens are
> ldrex/strex's real variable, lifted and presented as the brief's text.]
> Fifth consecutive records round whose pass 2 caught its own restatement of the claim
> under correction — the second pass stays mandatory.

> ## 2026-08-12 — #386 (round 126): swp — byte-order on both sides, rotate on the load, aligned word for both accesses
>
> `X(swp)` was LE-only on assemble AND emit (no `cpu->byte_order` term) and used the raw
> address with no rotate: on a BE guest every swp byte-reversed both the value into Rd and
> the value into memory, and any unaligned swp read/wrote 4 raw bytes at `Rn` (the "third
> model" this file's 2026-08-11 alignment-family entry measured). Fixed with the sibling
> idiom exactly: runtime byte_order (ldrex/strex token-identical), `rot_sh` captured from
> the RAW addr BEFORE `addr &= ~3`, rotate LOAD-only guarded on rot_sh, Rd written last,
> swpb untouched (order-free, no Alignment note). RED 42/58 on the committed build — all
> 16 DISC rows at their EXACT predicted buggy values (mechanism + register-field proof in
> one measurement) — then GREEN 58/58; mutants x3 each at its predicted count (LE-revert
> 48, no-rotate 56, no-mask 46, of 58 — the parenthetical values in the CHANGELOG block
> are the BE rows'; the LE rows differ [#387 precision]), three distinct signatures.
> Gate 14 PASS 317
> checks (34 -> 58 endian rows, +16 named DISC rows), zero FAIL/SKIP, single clean run.
>
> **Probe facts:** the LE-unaligned rows are ARCH rows, not controls — the manual's
> rotation is endian-independent, so the fix MOVES them; a must-not-move LE control would
> false-red the FIXED build. "swp be unal b2" is arch==buggy BY CONSTRUCTION (bits[15:8]
> lands at P+2 under both the buggy +1-shifted LE write and the fixed BE write, for any
> store value) — typed CTRL, excluded from the gate's named-DISC list. The P+4 sentinel is
> seeded 0x99, never 0x55: the buggy write's last byte IS 0x55, so a 0x55 seed cannot
> distinguish survival from corruption.
>
> **Panel:** pass 1 seven seats unanimous [#387 correction: "eight" was transcribed from
> the roster line, not counted — kimi's 403 quota error is not an answering seat] (fold
> the alignment half in; gate on the RED unaligned row — satisfied). One "critical
> compile blocker" was a quote MISATTRIBUTED from the sibling handlers' `word[*]`
> variable and presented as the sketch's text [#387 precision: "fabricated" overstated
> the mechanism] (refuted from another seat's verbatim brief echo); one ladder-base
> catch was real and adopted (the unaligned witness re-bases at the aligned P). Pass 2
> follows the commit.
>
> **Residuals:** swp's fatal()-on-abort console noise + missing next_ic reset vs the
> template idiom (task filed); cpu_arm_instr_loadstore.c:248-249 missing `(uint32_t)` cast
> on `<<24` (formal UB, benign, unmeasurable by construction — recorded, not tasked).

> ## 2026-08-12 — #387 (round 127): #386's pass-2 — the +2-offset detector, the kind pin, and eight record precisions
>
> No emulator code — all seven answering pass-2 seats verified the shipped X(swp) clean
> (five re-derived every constant; the Opus seat re-derived all four measured counts by
> hand and hand-decoded every encoding). Two DETECTOR findings closed:
> - **The +1-only hole** (the fold-marker probe's own three-offsets rule): a rotate
>   amount of `8*(addr&1)`, a raw-odd rotate guard, and a `~1` alignment mask all AGREE
>   with the shipped code at +1 and aligned — all three passed the 58-row set. Closed
>   with +2 groups both orders (12 rows, all DISC; P+5 seeded 0xAA so the buggy constant
>   is assumption-free). GREEN 70/70 on the committed build first; then each hole-mutant
>   EXECUTED and caught at its predicted count with the +1 rows still green: 68/70,
>   68/70, 58/70. Gate rows 58 -> 70, named DISC 31 -> 43, gate 14 PASS 329.
> - **The kind pin**: the gate's named pattern now requires `DISC ... ok`, so re-typing
>   a red discriminator as CTRL with arch==buggy can no longer keep its name green.
> Records corrected in place (tags at each site): pass-1 seat count "eight" -> SEVEN
> (kimi's 403 is not a seat — the recheck seat's catch; commit message immutable, block
> carries the note); "sentinel stuck at" -> overwritten to (2 seats convergent);
> "FABRICATED QUOTE" -> misattributed from ldrex/strex's real `word[*]` variable (the
> #385 copy softened identically, its "Two" count marked); mutant parentheticals scoped
> to the BE group; ladders parenthetical scoped to the aligned group; the no-writeback
> citation now names the #357 block comment (:157), not the file "header"; the stale
> "two rounds, swp first" sequencing pointer annotated (#386 done, ldrex-halt remains).
> Panel mechanics recorded: the I-bit refutation (0xE5D0xxxx IS immediate-form ldrb —
> the load/store I-bit is inverted vs data-processing; proven by field decode + months
> of committed ladder rows + the sentinel's exact 0x99/0x55 measured hits) and one cloud
> seat's length-death (65,536 eval tokens all thinking, empty response — a seat-health
> mode distinct from quota death).

> ## 2026-08-13 — #391 pass-2, SECOND correction: the records were wrong in BOTH directions
>
> *** THE SHIFT IS REAL AND PRODUCES WRONG VALUES. MEASURED. *** The brief said
> misattribution; the first correction "fixed" that to fail-safe truncation; a
> pass-2 seat then replayed the probe's OWN reader byte-for-byte against a
> scripted debugger with a virtual clock and showed THE BRIEF WAS RIGHT. A stall
> on `step` (or `pc=`, or any `print`) gives one DEAD row followed by FOUR
> registers each holding the PREVIOUS register's answer — an off-by-one-command
> shift. buf is shared and every mark is taken BEFORE the write, so output
> arriving after a timeout lands in the NEXT command's slice and re.search
> returns the FIRST bare-hex line there.
> *** WHAT SAVES THE GROUP IS THE VALUE TABLE, NOT THE PARSER. *** No two
> adjacent rows in any of the 34 groups share an expected value, so every
> shifted value mismatches and the group fails. That is a property of the DATA.
> ANY NEW ROW MUST BE CHECKED AGAINST ITS NEIGHBOURS — a future pair with equal
> adjacent expectations would pass silently.
> ALSO RETRACTED: "the echo flushes atomically at the newline" is FALSE. The
> debugger fflushes on EVERY iteration of its character loop, so the echo is
> emitted ONE CHARACTER AT A TIME, up to N writes. The conclusion survives, but
> it rests on the echo's CONTENT (it never contains the prompt), not on its
> atomicity — and a round whose thesis is "do not state a mechanism you did not
> measure" must not assert the wrong one.
>
> CODE FIX, one line, measured: puts_ok was FAIL-OPEN. `got is not None and not
> got.get("__put_ok")` meant a run() returning None never falsified it, so a
> session that NEVER STARTED printed PUT_STATUS=OK and gate 14's "endian puts
> all landed" asserted OK. Against a nonexistent binary it read OK before and
> reads FAIL now, while every OTHER control in the file already defaulted to
> FAIL. Same defect as #391's headline, three lines below #391's own fix — the
> round fixed one instance of a pattern and left its sibling adjacent to it.
> Gate 14 after: PASS 352, 0 FAIL, 0 SKIP; probe 102/102.
>
> THE MUTANT WAS HALF-BLIND: `_forced or not wait_from(mark)` SHORT-CIRCUITS, so
> wait_from was never called and the shipped conditional was never exercised by
> the mutant meant to prove it. It also modelled "the reader skipped the wait"
> rather than "the response never arrived" — the forced command still executes
> and its output lands in the next slice, silently constructing the very desync
> the records claimed impossible. Real detection needs PTY-LEVEL FAULT
> INJECTION; filed as task #81 with the structured-completion-result work.
>
> SIBLING SITES, none previously listed: arm_fold_marker_probe.py:161-168 has
> the byte-identical discarded-verdict defect feeding :182-185 -> :218 -> :652
> -> :667-668, in #379's own idiom (smaller blast radius, since a missing seed
> still reddens the value comparison, but the flag is a false False by the same
> mechanism); mips_fold_probe.py:311-318 and m88k_idle_probe.py:107-114 discard
> the verdict; arm_writeback_probe.py:547-553 and arm_idle_probe.py:198-204
> RETURN it correctly and every caller drops it one frame out, and
> arm_writeback has NO FAILED check on any put at all. Also: `pc=` emits a bare
> hex line into a discarded slice — a floating value of exactly the shape the
> register regex accepts.
> PROMOTE THIS RESIDUAL: "require the COMMAND ECHO in the slice before accepting
> a prompt" was filed only as the fix for the late-^C-prompt hole. It ALSO fully
> closes the measured shift — a `print r2` slice carrying `step`'s trailing
> prompt would be rejected for lacking `print r2`, the reader keeps waiting, and
> the stream resynchronises. Single change, both holes. Pair it with
> abort-and-resynchronise, since it is NOT a transaction id for IDENTICAL
> retries (a late prior identical echo+prompt still satisfies it).
>
> METHOD, four instances in one session: LDRD, the brief, the first correction,
> and a mutant that skipped its own conditional. EACH TIME ONE STEP WAS PROVED
> AND THE NEXT ASSERTED. Write only the claim you measured; mark the rest
> UNVERIFIED.
>
> ## 2026-08-13 — #391 (round 131): a control passed on evidence it never received
>
> arm_endian_probe.py's send() computed wait_from()'s verdict and DISCARDED it,
> returning the slice regardless. On a TIMEOUT that slice is EMPTY, so
> `"FAILED" in send(...)` was False, put_ok stayed True, PUT_STATUS printed OK,
> and gate 14's "endian puts all landed (379)" asserted OK. The probe's own
> comment eight lines below says why that is fatal: a silently failing `put w`
> leaves the page cold, routes through bdt_*, and turns every DISC row
> architecturally green ON A BUGGY BUILD — "a false pass, the one direction a
> control must never allow." The code contradicted its own stated intent.
> FIX: timed-out commands are recorded out-of-band in a `timeouts` list, so
> send()'s return contract is unchanged and every caller keeps working; the put
> loop fails put_ok if the list grew. A put is landed only if the debugger did
> not echo FAILED AND the command completed.
> MEASURED BOTH SIDES: with one put's response forced never to arrive, the
> fixed probe reports PUT_STATUS=FAIL and the PRE-#391 probe reports
> PUT_STATUS=OK. The second half is the one that proves the defect was real and
> silent. Unmutated 102/102, all controls OK; gate 14 PASS 352, 0 FAIL 0 SKIP.
>
> *** THE ROUND'S OWN BRIEF WAS WRONG ON ALL THREE HEADLINE CLAIMS. *** It
> asserted a deterministic wrong-value defect across six probes; a
> compile-and-measure seat confirmed none of it. SCOPE: one probe, not six —
> the other six already use the anchored model and arm_idle's comment records
> it fixed in round 100. MECHANISM: a load-dependent race, not determinism —
> GXemul always echoes the command and the echo flushes atomically BEFORE any
> reply, so the stale prompt is only at the tail after a >400 ms stall, the
> same load class that false-FAILs gate_ab; the brief's reproduction modelled a
> stream GXemul cannot emit. CONSEQUENCE: truncation, not misattribution — no
> consumer spans two sends, so the slice is SHORT not SHIFTED and the failure
> is None -> DEAD row -> FAIL, i.e. FAIL-SAFE. The item had been ranked #1 on a
> silent-wrong-value claim that is not reachable in the committed code.
> METHOD LESSON, second instance in one session: THE TRIGGER WAS REPRODUCED AND
> THE CONSEQUENCE WAS ASSUMED. Proving a predicate misbehaves says nothing
> about what the consumer does with it. The first instance was #390's LDRD
> reversal ("the mutant did not redden the row" -> "the defect is not there").
> Same shape: one inference past the evidence.
>
> *** PASS-2 CORRECTION: THE CONSEQUENCE CORRECTION ABOVE OVER-CORRECTED, and
> the over-correction is the SAME ERROR ONE MORE TIME. *** "Truncation, not
> misattribution / FAIL-SAFE" was extrapolated from the READ parsers to EVERY
> consumer. It does not hold. A timeout does not imply an EMPTY slice (echo or
> partial output may be present); a mark stops bytes present BEFORE it but not a
> delayed earlier response arriving AFTER it; and decisively, THIS ROUND EXISTS
> BECAUSE A SETUP-COMMAND CONSUMER WAS NOT FAIL-SAFE — the put control turned a
> timeout into a silent OK. Claiming the failure mode is fail-safe in the same
> entry that fixes a non-fail-safe consumer is a contradiction. HONEST VERSION:
> the checked READ parsers degrade to None; the SETUP-command consumers did not,
> which is what this round repaired; `pc=`, `step` and `print` remain UNVERIFIED.
> Also narrowed: "turns EVERY DISC row green" is too broad (one invocation
> affects only its own emulator group, and a code put lacks a warm-page seed's
> warmth consequence). Also corrected: the tlbdump rationale was WRONG —
> ls_general increments during GUEST EXECUTION while debugger commands run with
> emulation STOPPED, so two synchronised reads SHOULD agree; taking only the last
> is still unsafe, but a disagreement is a PROTOCOL FAILURE, not a legitimate
> monotonic increase. Also corrected: FOUR non-ARM families (MIPS, PPC, SH,
> m88k), not five — ARM emits such a line too but its sites no longer use the
> bare predicate.
> RESIDUALS THE ROUND MISSED, added in pass 2: unacted pc=/step/print failures;
> PUT_STATUS=OK when run() returns None; NO committed durable detector for the
> #391 timeout itself; continuing a session after synchronisation is lost;
> EOF/read errors mislabelled as timeouts; time.time() where a MONOTONIC
> deadline is required. Their disposition is bigger than this round: propagate a
> structured completion result instead of a side list, abort on a failed
> state-changing command, and add PTY-LEVEL FAULT INJECTION so the detector is
> real rather than simulated by string-matching a command.
> Also corrected: requiring the COMMAND ECHO is NOT a general transaction
> identifier for identical retries — a late prior identical echo+prompt can still
> satisfy it. Abort and resynchronise after a wait failure rather than retrying.
>
> RESIDUALS, all specified, none touched: anchoring has NO detector (reverting
> it passes on a healthy host — needs a stall-injection mutant); a bare
> wait(15) survives outside send(); two wait_from results are discarded after
> ^C where three sibling probes check and kill; byte-offset anchoring does NOT
> close the late-^C-prompt hole — requiring the COMMAND ECHO in the slice
> before accepting a prompt does, is free, and is strictly stronger;
> READS_RETRIED must NOT be asserted zero (retries are triggered by host
> slowness, so that makes the oracle a proxy for load — the gate_ab mistake in
> a new place) — fail on reads that NEVER answered instead; and "parse the last
> complete response" is wrong for tlbdump, whose counter is MONOTONIC, so two
> attempts can legitimately differ and "last" silently takes the larger.
> The 14 non-ARM readiness sites matching a bare '>' are recorded as HIGHER
> severity than this round: five CPU families print a '>'-terminated
> " no symbol " line FIRST in the register dump, line-buffered on a pty, so a
> reader waking between lines returns with the registers UNREAD — and that
> needs no unusual host conditions at all.
>
> ## 2026-08-13 — #390 (round 130): one scratch word, two roles — a PC-relative store's base was four bytes high
>
> A__NAME_PC splits on #ifdef A__L (instruction CLASS) while tmp_pc's two uses are
> distinguished by ROLE — BASE when Rn==PC, DATA when Rd==PC. The store arm set
> tmp + 12 UNCONDITIONALLY, and the decoder points arg[0] at that same word
> whenever rn==ARM_PC regardless of the L bit, so the base took the data value.
> `str rX,[pc,#imm]` addressed FOUR BYTES HIGH. DEFINED behaviour, not latitude:
> A5.2.2 :18700, A5.2.3 :18740, A5.2.4 :18840, A5.3.2 :19425, A5.3.3 :19473 all
> give Rn==R15 as instruction+8 for the non-writeback offset forms; only the
> writeback forms are UNPREDICTABLE. The emulator's own pc-relative LOAD fold
> already used +8 — it requires the L bit, so stores were never rescued.
> FIX: TWO scratch words. A one-word role-aware guard is MEASURABLY WRONG for
> `str pc,[pc,#imm]`, where arg[0] and arg[2] are the same pointer and setting
> the base to +8 silently moves the STORED word to +8 — which A2-9 :1637-1641
> forbids, since an implementation may pick +8 or +12 for R15 stores but must
> use ONE everywhere. cpu_arm.h gains tmp_pc_data[2]; both decoder sites point
> arg[2] at it; the store arm computes both values unconditionally. Separating
> the roles at DECODE time removes any run-time pointer-identity test, and the
> [2] sizing keeps a doubleword's second word off tmp_branch (THUMB state).
> MEASURED: RED on parent 495a07a both rigs, GREEN after; probe 102/102; gate 14
> PASS 352 checks 0 FAIL 0 SKIP; blast radius with the expected set DECLARED
> FIRST = 80 changed bodies across all EIGHT flavor files, all _pc, ZERO
> load-named. FOUR MUTANTS all caught, and the PAIRING is the evidence: blanket
> +8 / deleted data assignment / reverted decoder redirect each redden bothpc +
> data with base GREEN (98/102); reverting the base reddens base + bothpc with
> data GREEN (96/102 — exactly the pre-fix parent's own score). Opposite
> signatures prove the rows separate the roles rather than noticing change.
>
> *** [CORRECTED IN PASS 2. The paragraph that stood here claimed "LDRD's base
> was NEVER four bytes high" and called the LDRD rows "a row whose defect does
> not exist". BOTH ARE FALSE. The compile-and-measure seat settled it by
> measuring. LDRD's base WAS four bytes high and #390 FIXED IT — the round did
> more good than it credited itself with.] ***
> THE MECHANISM, and it is a defect-hiding surface that will do this again: the
> general path masks with `addr &= ~(datalen - 1)` and datalen is 8 for
> LDRD/STRD. The base error is exactly +4, so (I+8+off) and (I+12+off) fall in
> the SAME eight-byte block precisely when the correct address is
> doubleword-aligned — and A2.8 (ddi0100i.txt:3031) makes a non-doubleword-
> aligned LDRD/STRD UNPREDICTABLE before ARMv6. THEREFORE on every
> architecturally DEFINED mode-3 Rn==PC access the mask ALWAYS heals the error,
> and it is observable only where correct behaviour is already UNPREDICTABLE.
> That is a THEOREM, not a probe accident: the row used offset 0x40 at the code
> base, the aligned case. Rows at offset 0x44, or with the instruction one word
> later, show it plainly — measured 0xcccc0003 pre-fix against 0xaaaa0001 fixed,
> both rigs. STRD is covered identically, and its PC-relative form is DEFINED
> per A5.3.2.
> So the dispatch chain was exactly as the three original sources said, and
> nothing upstream supplies the base. The four LDRD rows are the ORDINARY
> vacuity class — a row that CANNOT DETECT ITS DEFECT. They stay CTRL because no
> DISC row is available: every mask-defeating layout is UNPREDICTABLE, which
> #355 forbids asserting on. But the reason recorded against them was wrong, and
> the promise that they "will redden if a later round drags LDRD into that path"
> is PROVABLY FALSE — reverting the base does not move them. WITHDRAWN.
> THE PRE-PARENT METHODOLOGY WAS SOUND; THE INFERENCE WAS THE ERROR. Restoring
> the three touched files into a build-tree copy does yield a faithful parent,
> and the stale-.o hazard is excluded by the round's own data (the STR rows went
> RED there, which a stale build could not do).
> LESSON, corrected and sharper: A MUTANT THAT FAILS TO REDDEN A ROW IS EVIDENCE
> ABOUT THE ROW — that part held, and it is what exposed the blindness. But the
> follow-up must be "therefore this row cannot see its defect", NOT "therefore
> the defect is not there". The first is a statement about the INSTRUMENT; the
> second is a claim about the WORLD and needs its own measurement. This round
> made that leap inside the very block congratulating itself for not leaping.
> And still true: a claim several seats agree on is still a claim.
> #68 does NOT fold in — its Rn==PC base half is refuted for LDRD; its Rd==PC
> half remains open and must be re-verified independently, not inherited.
> PER-INSTRUCTION, why the +12 DATA value is left alone: only STR (word) is the
> IMPLEMENTATION DEFINED +8-or-+12 case; STRB/STRBT (:14342, :14415) and STRH
> (:14690) make Rd==PC flatly UNPREDICTABLE, and STRD makes an odd Rd UNDEFINED
> (:14503). One blanket sentence across all four would overclaim.
>
> ## 2026-08-12 — #389 (round 129): big-endian LDRD/STRD — two 32-bit words, not one 64-bit swap
>
> Three defects in the template's BE LDRD arm (word-pair inversion BOTH sides — Rd
> pairs with the LOWER address per A4.1.26; a carry-corrupting data[1]<<6 term —
> buggy Rd = 0x55660908, not a byte permutation; a verbatim-LE R(d+1) branch) and
> E1's mirror in STRD. LE was correct on both sides. Fixed with two explicit
> per-word assemblies each side, casts on both branches of the new statements
> (shift UB; detector-free by construction, declared), the STRD arm lifted out of
> the shared descending walk (`int i` scoped inside #ifndef A__STRD; the :293
> guard reduced to #ifndef A__H — a dead disjunct is the #372 shape).
> MEASURED: RED on the committed build = r4 0x55660908 / r5 0x44332211 exactly
> (mechanism + encoding proof in one run — a seat's misencoding claim was refuted
> by mechanism then killed by these values); gcc -E blast radius = exactly the 4
> LDRD/STRD instantiation bodies of 620 changed; zero build warnings; GREEN 90/90
> with the BE ldrd pair equal to the gated LDM rows on identical memory (the
> internal-consistency oracle) and ENDIAN_CONTROL_D liveness pins OK.
> MUTANTS: eight executed (each in its own /tmp copy of the build tree, so no
> .MUTANT window; each anchored on the NEW code), ALL EIGHT CAUGHT with their
> sibling arms green — M1 the restored data[1]<<6 line (89/90; E3 not restored
> with it, so only the BE r4 row reddens), M2 the plausible HALF-fix = E2+E3
> corrected with E1's pair inversion LEFT STANDING (88/90), M6 the BE expression
> on both ternary branches (89/90, LE side red), M7 the dropped +1 on the pair
> write (86/90 — r5 keeps its sentinel in both orders AND both r4 rows take the
> upper word), M8/M9/M11 the three STRD-BE corruptions — pair
> inversion, per-word reversal, full 8-byte reversal (82/90 each), M12 an
> adjacent-index slip in the NEW LE store arm (88/90, b1/b2 red). M10 (~7 -> ~3)
> stays the DECLARED survivor per :2508-2514 — aligned bases make the masks
> coincide, so no legal row separates them.
> GATE 14: one clean serial run, PASS 340 checks, zero FAIL / zero SKIP (329
> committed + 10 named DISC + the ldrd/strd liveness check; "endian rows run"
> reads 90). Each new name matched EXACTLY ONE row, so neither half of the
> padded-column trap applies.
> Residuals: the A__NAME_PC family consolidated into task #68 (Rn==PC pc+12;
> Rd==PC pair-writes tmp_branch); the two "NO LDRD/STRD ROW" comments narrowed
> to their unaligned/writeback scope.
> [CORRECTED same day from the manual this repo actually holds — the withdrawn
> clause was "all UNPREDICTABLE inputs, #312 latitude rule attached", which was
> wrong on BOTH halves. Rn==R15 in the two OFFSET forms of BOTH addressing modes
> is DEFINED as instruction+8: A5.2.2 ddi0100i.txt:18700, A5.2.4 :18840,
> A5.3.2 :19425, A5.3.3 :19473. Only the pre-/post-indexed forms (which write
> back to R15) are UNPREDICTABLE: A5.3.4 :19526, A5.3.5 :19570. And Rd==R15 for
> LDRD/STRD is UNDEFINED, not UNPREDICTABLE — R15 is odd-numbered, and both
> A4.1.26 and A4.1.102 state an odd-numbered <Rd> makes the instruction
> UNDEFINED, which requires an exception rather than granting latitude. #68 is
> therefore a DEFINED-behaviour divergence and #312 does not apply to it.]
>
> PASS-2 PANEL (6 seats answered; kimi 328b quota, and the FABLE SEAT IS NOW
> QUOTA-DEAD too — two identical usage-limit failures, so a sonnet substitute
> carried that lens and is recorded AS a substitute). No seat found a code
> defect: every seat that derived the byte assembly independently agreed, and
> the restructuring was confirmed behaviour-preserving. The Opus seat compiled
> and measured, and STRENGTHENED the central proof — where this round
> preprocessed ONE flavor file (4 of 620 bodies), it preprocessed all twenty
> macro sets across all EIGHT p/u/w files: 160 instantiations, 128 identical,
> 32 differing, all 32 being LDRD/STRD imm+reg. 620 = 20x31 confirmed exact;
> true global blast radius 32 of 4960. It also caught its own vacuous green on
> the way (a broken -I path made both sides fail to preprocess, and a
> comparison of two FAILED builds is always "identical") — a new entry for the
> vacuity taxonomy.
> TWO MUTANT GAPS, both verified here before acceptance:
> (1) OPUS, MEASURED: a single WRONG cast — (int8_t)data[1]<<16 for
>     (uint32_t)data[1]<<16 — is wrong on 100000 of 200000 random doublewords
>     (50%) yet passes ALL 90 rows and ALL 8 mutants. The seed
>     11 22 33 44 55 66 77 88 has exactly one byte >= 0x80 and it only lands
>     where sign extension is harmless, so no sign-extension defect in
>     data[0..6] can move a row. Four rows on a high-bit seed close it. This
>     also corrects this round's "detector-free by construction" framing: that
>     holds for cast DELETION (benign UB here, sanitizer-only) but NOT for a
>     wrong cast. -> task #72.
> (2) AGY: NO LDRD/STRD row is warm — seed_bytes uses `put b` (does not warm)
>     and the STRD rows seed nothing — so the fast-path chicken-out disjunct
>     has NO detector. Deleting `|| defined(A__STRD)` makes a warm-page STRD
>     write 2 bytes of 8 (A__STRD implies A__H; the fast path's A__H arm writes
>     exactly 2), with all 90 rows still green. -> task #71.
> REFUTED BY MECHANISM: one cloud seat called M6's measured 89/90 "factually
> inconsistent" and demanded 88/90, assuming the mutant changed both register
> statements. The mutant's own anchor (assert s.count(a)==1) matches only the
> Rd ternary, so exactly one row can redden; a second seat derived the same
> reading unprompted. The measurement stood and the ambiguous SENTENCE was what
> changed — the sixth recorded case of the panel majority-or-confidence being
> wrong on mechanism.
> TWO HONESTY POINTS ACCEPTED: this round's headline is a MENTAL MODEL, not a
> measured property (for an aligned access the shipped code and the "one 64-bit
> value then split" formulation are the same function — 0 disagreements over
> 400k cases — since they diverge only at unaligned addresses, the region #355
> forbids gating); and "LDRD does not rotate" is asserted in prose and tested by
> nothing, so it is DECLARED as a second by-construction survivor beside M10.
> NEW TASKS: #71 warm rows, #72 high-bit seed + sanitizer, #73 register-offset
> and writeback rows (+ an STRD write-extent sentinel per #386/#387 practice),
> #74 the ARMv6 U=1 ~7 mask, #75 the device len=8 path, #76 odd-Rd UNDEFINED
> (the ONLY gateable divergence the pass surfaced), #77 Rd==R14 (in bounds —
> checked — but the PC desyncs).

> ## 2026-08-12 — #388 phase A (round 128): the MIPS folds get their witness — 34 variants, counters, tlbdump schema
>
> Design converged from a seven-seat pass-1 that changed the brief materially: install
> counters moved from the decoder arming lines to the per-variant REPLACEMENT SITES
> (arming is unconditional, variant-blind, retranslation-inflated — the lying-instrument
> variant; three seats convergent); fold_arm[9] added (site-entered vs no-arm-matched —
> two zeros a census must not conflate); fire by the CFG rule with pinned exceptions
> (idles bump before instr(idle) + idle_entered[] counts dispatches; jr_ra_addiu's AdEL
> path stays counted; memset counts handler COMPLETIONS); the 16 multi-width installs are
> single ternary lines AFTER their brace-less if/else pairs; install-without-fire is
> NORMAL for multi_*_2..4 (escalation supersedes pre-dispatch) — recorded so the census
> cannot read it as a defect. Refuted during review, by mechanism: "a breakpoint disables
> combining" (the :1888 gate has no breakpoints term — only read-ahead :1938 does; with a
> breakpoint fire==passes-1, without one folds install DURING read-ahead so fire==passes),
> "pmax/arc are BE" (both LE), enum counts 30/31 (mechanical manifest: 35 sites = 34
> variants). `-s` found to be a second fold kill switch besides -J (census argv must
> carry neither).
> Shipped: cpu_mips.h enums+counters (struct END, cache-line isolation), 9 arm + 27
> install + 18 hand fire + 2 idle_entered bumps (no file-scope objects — the TU is
> doubly included), generator-emitted bumps for the 32 generated bodies (each build
> asserts the regenerated tmp carries exactly 32), tlbdump MFOLD_START/rows/ARM/IDLE/
> MFOLD_END schema (absent END = DEAD; END with nonzero=0 = live all-zero; counts catch
> truncation) + flush. Measured: both trees build; testmips debugger smoke prints
> START n=34 / END n=0 nonzero=0 over piped stdin (no pty needed without a guest
> console — phase B reuses this). No-perturbation oracle: one clean serial gate 4
> [#388 pass-2: was "gate 3" — run.sh is 1-based, gate 3 is selftest_mutation] run
> on the instrumented build = mips-rigs PASS 6 checks zero FAIL (pmax uid=0, arc 13/13
> steps to root — unchanged boots; the counters are invisible until pulled).
>
> **Phase B MEASURED (same day):** mips_fold_probe.py 9/9 at derived equalities —
> bne_samepage_nop/lui_ori/multi_lw_2/memset across 3max(32LE) + testmips(64BE) +
> testmips -C R3000(32BE); the RUN contains the first BE MIPS guest executions in
> [#388 pass-2: bne_nop_tm64 precedes the multi rows — attribution corrected; the
> first-ever claim itself verified by both re-derivation seats] —
> the harness, with two value rows witnessing the _be body's BE32 assembly + sign
> extension; memset (1,1) = completions. One measured probe fix en route: `print`
> answers a BARE 0x%x line (no name echo — that form is the assignment echo).
> Mutant M388MUT_PASS: the deleted bne_samepage_nop sub-arm (incl. its install++)
> reads (0,0) with its two rows red and every OTHER ROW green [#388 pass-2: the
> "sibling" wording was false — the isolation shown is cross-SITE; and the deletion
> also un-installs linux_pmax_idle via its ic[-5] requirement, a coupling recorded
> for #69] — per-variant attribution -J cannot give. Gate 16 (gate_mips_folds.sh,
> wired into run.sh): PASS 11 checks [pass-2: grown to 17 — the (1,0) device-page
> bail-detector row (a fire bump hoisted above the generated bail measured RED at
> (1,4)), in-loop poisons making all six value rows load-bearing (the stripped-
> writes mutant measured all six red at the surviving poison), the MODE32 32-bit
> print expectations measured, and the did-not-complete path now FAILs instead of
> skipping]. **Phase C (census) re-scoped to its own follow-up task** per the
> design's pre-declared fallback (ctrl-C-ing the out-of-repo pty boot harnesses is
> a new flake surface that does not belong on this commit's green path); its zeros
> will be filed "unreached under the committed rigs" + expected_zero_reason, NEVER
> "dead"; install-without-fire stays the normal state for multi_*_2..4.

## 2026-08-14 — #418 residuals (the `d:` prefix round)

**THE HALF THIS ROUND DID NOT FIX, stated first because a reader of the diff could
believe otherwise.** #418 made the documented `d:` escape hatch work. It did NOT touch
the size heuristic that creates the unreachable type, so **a BARE floppy-sized image
with no prefix is still typed `DISKIMAGE_FLOPPY` and still invisible to every
controller** — no device references that type, and both selectors match on
`d->type == type`. That is the default path, the one a user hits without reading the
manual. Four `[RECORD] no prefix <size> unreachable by dev_asc` rows in
`regress/diff_diskimage_parse.c` pin it, and `gate_offline` checks them by name, so the
round that does fix it cannot land silently — but it is open.

**Two sub-defects found while measuring, FILED not folded in** (the stopping rule admits
only a measured false pass or a wrong record in-round, and neither of these is either;
harness task #126 carries them as one round because they share the same code):

1. **A small ISO becomes a `FLOPPY CD-ROM`, doubly unreachable.** Measured on the
   shipping binary: `-e 3max -d cd.iso` on a 1.44 MB ISO prints
   `FLOPPY CD-ROM id 0, read-only, 1440 KB (CHS=80,2,18)`. The heuristic tests only
   `type == DISKIMAGE_UNKNOWN` and ignores `d->is_a_cdrom`. **1.2 MB and 1.44 MB are
   standard El Torito floppy-emulation sizes**, so this is an ordinary shape of file.
   The candidate one-liner (`&& !d->is_a_cdrom`) touches the size heuristic, which is
   the collision surface with #414 and #418 — design it, do not patch it in passing.
   *** The `[RECORD] bare 1.44M *.iso is FLOPPY-typed (filed defect)` row asserts
   TODAY'S WRONG BEHAVIOUR on purpose and MUST be updated by the round that fixes it. ***

2. **`d:` is consulted for `.iso`/`.cdr` but not `.cue`.** The pass-1 panel split 2–2 on
   fix-vs-record. A seat corrected the brief on the substance, and the correction is the
   useful part: a `d:`-prefixed cue is **not** "additionally" unwritable — the unprefixed
   one is equally read-only, because `is_a_cdrom` forces `writable = 0` for both.
   Measured: `-d d:disc.cue`, `-d disc.cue` and `-d c:disc.cue` are byte-identical. So
   the asymmetry is real but costs nothing measurable today. Second argument for
   recording: a cue sheet is a multi-track *text descriptor* whose data lives in a
   separate `.bin`, so forcing it to "disk" would present the descriptor as a disk.

**Assessed, not changed — an offline parser detector cannot cover the controller side.**
Every row in `diff_diskimage_parse.c` asserts the PARSER's output. If a later round
taught `dev_asc.c` to also accept `DISKIMAGE_FLOPPY`, all 35 rows would stay green while
the reachability story flipped completely. That needs a call-site row or a booting rig.
Stated in the detector's own header rather than left to be discovered.

**Records rule earned this round:** `diskimage_scsicmd.c` claimed `DISKIMAGE_FLOPPY`
*"occurs in exactly seven places"* — and spelling the identifier in a sentence that
counts occurrences of that identifier **made the count eight the moment it was written**;
its "all inside `diskimage.c`/`diskimage.h`" clause was falsified by the file the sentence
lives in. The duplicate in `CHANGELOG.md` was found by a seat, not by the main loop, whose
grep had silently scoped itself to `src/` — the same omitted-scope failure it was
correcting. A tree-wide sweep found no other instance, so this is a one-off, not a class.
**A record may not state a count of an identifier it also spells.** State the structural
property instead; it survives edits.

## 2026-08-14 — #419 residuals (the gate_ab progress-oracle round)

**#419 converted GATE 7 ONLY. Everything below is what it did not touch, and the first item is
worse than the defect that was fixed.**

1. *** GATE 5 HAS THE SAME DEFECT AND BREAKS UNDER LOAD BEFORE GATE 7 DOES. ***
   `gate_crossfamily.sh:54,62` drives `drive_guest.py`, which allows luna88k a `boot_wait` of
   **600 s** and landisk **420 s**, plus ten per-step timeouts of 5–15 s
   (`drive_guest.py:41-52, 86-99`). The saturated luna88k boot measured in #419 took **742 s** and
   still reached `login:` correctly. So gate 5 false-FAILs at a load level gate 7 now survives.
   Converting it is the obvious next round; the machinery (`run_emu_progress()`) already exists.

2. **ROUGHLY 37 WALL-CLOCK ORACLES REMAIN ACROSS THE BATTERY.** 33 `while time.time() - t < …`
   wait loops spread over 18 probe `.py` files, plus `gate_asan_sweep.sh:60,62` (`timeout 25`),
   `gate_upstream.sh:74` (`timeout 20`), and `run_emu()` itself. #419 replaced one. **No
   battery-wide parallelism claim is earned until these are dispositioned**, and most of them are
   probe-internal step waits rather than boot budgets, so they need a different remedy.

3. **THREE PRODUCER/CONSUMER ORDERINGS SERIALISE THE BATTERY INDEPENDENTLY OF ANY CLOCK**, and
   these are the real reason gates cannot run concurrently:
   * `gate_build.sh:64-65` **withdraws** `/tmp/gxsec-gxemul` and `$RIG/gxsec-gxemul` at gate start
     and republishes only at `:302-305`, while `gate_mips.sh:30` `need_exec`s it. A concurrent run
     makes gate 4 `gate_skip` on a missing binary — **silent coverage loss scored as a SKIP**.
   * `gate_hygiene.sh:198-199,220,258` grades `pmax.ptylog`, `arc.ptylog`, `arc.screen` and
     `drive_*.log`, which gates 4 and 5 produce. Concurrency grades a **partial** log: a wrong
     answer, not a crash.
   * `gate_ab.sh:42` `rm -rf`s `/tmp/gx-pristine` and `/tmp/gx-prebatch`, which
     `gate_upstream.sh:46-47` reads.
   **A per-gate `LOGDIR` still would not isolate them**, and the reason is now the ORDERINGS
   ALONE: the driver's own hardcode was removed (`drive_guest.py:207-210` honours `$LOGDIR`,
   `lib.sh:31` exports it), but the producer/consumer edges above are untouched.

4. **CORRECTION TO A STANDING NOTE, kept here because it was load-bearing for four months:**
   `selftest_mutation.sh` does **NOT** `rm -rf` the shared gate workdir — it is `T=$LOGDIR/mutation`
   (`:27`) and `rm -rf "$T"` (`:41`), scoped to one subdirectory. The rig images do not serialise
   either: both consumers open them read-only with `R:` and the overlay is pid-unique. The reason
   given for "never run two gates concurrently" was wrong; the *conclusion* was right for the three
   different reasons in item 3.

5. **THE m88k IDLE-PATTERN DETECTION IS A SILENT CROSS-VERSION DEPENDENCY.**
   `cpu_m88k_instr.c:2584-2757` recognises the guest's idle loop **by pattern** and credits 8191
   instructions per fold. If the guest OS ever changes that loop the detection fails **silently**
   and instructions-to-login balloons — which would move #419's budget without any error anywhere.
   This is safe today only because the image is pinned (`liveimage-luna88k-raw-20250518.img`).
   Assessed, not changed; the budget's +54 % headroom absorbs ordinary drift but not this.

6. **UPSTREAM 0.7.0 SPINS ON luna88k RATHER THAN EXITING — mechanism unexplained.** It burns 100 %
   of one core (measured from `/proc/<pid>/stat` utime+stime over a 20 s window) while emitting
   fewer than 33,554,432 instructions in 300 s (< 111,848 instr/s). Whatever it is doing, it is not
   the dyntrans loop. Not investigated; recorded because it means **"the process is still alive"
   carries no information** for that row.

7. **THERE IS NO CLEAN WAY TO MAKE gxemul REPORT A FINAL INSTRUCTION COUNT.** SIGINT enters the
   debugger and then blocks on absent stdin; the process survived SIGINT plus 6 s and needed
   SIGTERM. `cpu.c:418`'s forced `cpu_show_cycles()` never runs. So the count must be scraped from
   the periodic `-N` records, which is why the oracle is quantised to 2^25 instructions (0.44 % of
   a luna88k boot — far below the 3.57 % run-to-run spread, so it costs nothing).

## 2026-08-15 — #420 residuals (the gate 5 progress-oracle round)

1. *** THE TEN PER-STEP WALL-CLOCK WAITS IN `drive_guest.py` ARE NOT CONVERTED, AND CANNOT BE
   WITH THE PRESENT ORACLE. *** Measured across five healthy runs, 25 step windows: **16 saw
   ZERO instruction records and none saw more than two**, because at a prompt the guest's rate
   collapses from 63.5 M to 1.53 M instr/s. So "require zero records" false-FAILs a healthy run
   16 times in 25, and scaling a step budget by the boot-phase rate applies a figure **40× wrong
   for the phase it gates**. They are also not verdict-bearing individually — the driver retries
   and the verdict comes from the log scan — and under the same 6× load that broke `boot_wait`,
   every step confirmed on attempt 0. **Residual stated honestly: if the retries are ever
   exhausted, the original defect returns with a much smaller trigger.** Any future scheme needs
   its own measurement first; do not port the boot-phase reasoning down to a 5 s window.

2. **LANDISK'S INSTRUCTION RATE IS UNCALIBRATED, AND ITS COUNT IS A POOR ORACLE.** Six idle boots
   span 2,046,965,550–2,852,740,381 — a **39.4 %** spread, against luna88k's 3.57 % over eight
   runs. #420 therefore gives landisk **no instruction budget at all**, relying on the stall
   detector and the backstop. Deriving a ceiling from six samples that scattered would be the same
   "mean quoted as a worst case" error #419 pass 4 corrected. To close this properly, measure the
   landisk rate across enough boots to bound the high side, then set a budget.

3. **`gate_crossfamily.sh`'s `v()` TAKES `head -1`**, so a rig declaring two `expect_values` has
   only the FIRST compared literally. Landisk's `GX_ANS 42` currently rides on `VERDICT` alone.
   *** THIS ENTRY ORIGINALLY SAID "not a live false pass today — landisk declares one value".
   THAT WAS FALSE, and the false half was the exculpatory one. Landisk declares TWO
   (`drive_guest.py`, `expect_values`) and the driver prints both — measured from the gate's own
   `rig_landisk.out`: `VALUES=SH7751R` and `VALUES=42`, each with its matching `VALUES_WANT`.
   So the literal comparison covers the first and `GX_ANS 42` is protected by the aggregate
   VERDICT only. IT IS LIVE. *** Fix `v()` to compare every reported value, not `head -1`.

4. **gxemul's OTHER bracketed messages already splice guest lines, with no `-N` involved.**
   Measured in the last pre-#420 gate logs: landisk 7 of 20 bracketed messages were not at line
   start, two splitting a guest word (`RS5C313 real t`+msg+`ime clock`), one landing immediately
   after `HITACHI SH7751R` — the exact string this gate asserts. #420's strip removes only
   `instrs` records. The general mechanism — `cpu_show_cycles()` and friends printf-ing into the
   same stdout as the console with no leading newline — remains, and a future message could land
   mid-token in an asserted string. Assessed, not changed.

5. **A backstop expiry in gate 5 is now a hard FAIL with no way to say "the host was slow".** That
   is deliberate — one guest per rig means no A/B witness, so the excuse is unfalsifiable — but it
   is a real behavioural difference from gate 7, and a genuinely overloaded host will produce a red
   gate 5 rather than a skip. The backstop is 2400 s against a measured worst boot of 742 s, so it
   takes a host ~3× worse than full saturation to reach it.

## 2026-08-15 — #420 pass 2 residuals (the measure seat's second sweep)

*** THE ROUND STATED A GENERAL PROPERTY THAT IS ONLY TRUE FOR ONE RIG. ***
"A budget of GUEST WORK is load-insensitive" is established for luna88k — two independent
measurements 3,498 instructions apart across load levels — and is **FALSE for landisk**.
Measured under 8 busy loops on 8 cores: landisk reaches its milestone at **1,040,286,129
instructions under load against 2,046,960,827 idle — a 49% drop.** The SH4 boot waits on
host-clock-driven emulated timers, so its instruction count tracks the host almost as badly as
wall clock does. Three consequences, all now recorded rather than assumed:
  * giving landisk NO instruction budget is right, for a far stronger reason than the round gave;
  * the quoted 39.4% landisk spread is IDLE-HOST VARIATION ONLY — across host conditions the
    real spread is at least 2.74x;
  * any future landisk budget MUST be derived from LOADED runs or it will be nonsense.

**The largest POST-milestone inter-record gap under load was 56.97 s against a 60 s stall.** The
step phase is not progress-checked today, so this is latent — but it is a 5% margin, and anyone
extending progress checking into the interactive phase will false-FAIL immediately. This is the
concrete number residual item 1 above was missing.

**Log size is not a stable oracle.** The claim that free-stripping reproduces the previous
no-`-N` log sizes "exactly (6234 B, 3838 B)" holds for luna88k (6234 exact) but landisk gave
**3837**, because the guest prints a variable CPU speed (`916.685 MHz` vs `550.11 MHz`). The
content-level comparison is the real evidence; the byte count was a coincidence that nearly
became a fixture.

**The anchored-vs-unanchored evidence does not describe the shipped code.** That table was
produced by injecting a record into WHOLE LOGS. Through `absorb()`, `(?m)^` also matches at
position 0 of every `tail`, i.e. at every chunk boundary, so the anchored variant behaves
differently in the streaming path than the table shows — and it passes every gate row on both
real streams. The conclusion (use unanchored) is unchanged; the cited measurement is not
evidence for the code as written.

**Landisk's stated minimum was breached by the next boot.** 2,046,965,550 was quoted as a range
floor; the following idle run measured 2,046,960,827. It is a sample, not a bound, and the
records should stop presenting sampled extremes as limits.

**A rig-generic budget bound will false-FAIL a legitimate landisk budget.** The pass-2b row
checks `[8174849291, 15571141508]`, which are luna88k's numbers. Closing the landisk calibration
residual will trip that row unless the bound is scoped per rig first.

**`STALL=500` survives the range row** (`30 <= st <= backstop/4`), which would make the stall
detector nearly useless while staying green. Accepted looseness, recorded so it is a decision.

**Housekeeping, and a real hazard:** the `-N`-removed mutant run left `/tmp/gxregress/drive_*.log`
containing no instruction records for roughly a minute. A `gate_hygiene` run in that window would
have graded the MUTANT's console log. Mutant runs must write to a scratch LOGDIR, never the
shared one.

## 2026-08-15 — #420 final-panel residuals (all seven scriptable seats, second full roster)

**Filed rather than fixed, because a seat labelled them PREDICTED AND NOT EXECUTED and said so
plainly.** That distinction is the reason they are here instead of in the diff: a predicted false
pass is a hypothesis until somebody mutates the committed code and watches the rows stay green.

1. **`boot_progress()` is free to ignore a constant the gate scores.** The gate range-checks
   `BUDGET`, `STALL` and `BACKSTOP` as *printed by the driver*, not as *used by the driver*. A
   mutant that keeps printing the right numbers while using different ones would pass every row.
   Closing it needs the values to be read from a single place the driver actually consumes, or a
   fake-rig row that drives the constant to a value whose effect is observable.

2. **A luna88k `BUDGET=0` would still print green.** The "deliberately absent (uncalibrated rig)"
   branch does not care WHICH rig it is describing, so zeroing luna88k's budget — disarming its
   only work-based ceiling — is reported as a deliberate design decision. The rig-scoped range row
   added this pass covers a *wrong* budget but not a *removed* one.

3. **`expect()` does not see `tail`.** `stop()` was taught to search `buf + tail` so a milestone
   held as a possible record prefix still wins, but the ordinary `expect()` used for the
   interactive steps still searches `buf` alone. A step confirmation whose text begins with `[`
   would be withheld until a newline released it. Latent: no step pattern currently starts that way.

4. **Landisk's runaway bound is 900 s of wall clock, and the "it cannot have a ceiling" reason is
   overclaimed.** The 49% load swing makes a *fixed* instruction ceiling unsafe; it does not make
   the wall-clock fallback load-independent. A sufficiently overloaded but healthy landisk boot can
   still exceed 900 s and fail. Closing this needs a different observable — emulated timer
   progress, phase markers, or a comparative witness — not a bigger number.

5. **"BACKSTOP is unfalsifiable" is an overclaim.** A seat pointed out that `NINSTRS` at the
   backstop does partially falsify host starvation, and that the gate runs two rigs whose relative
   slowdowns cross-witness each other. The design decision (hard FAIL) stands — a partial witness
   is not an A/B baseline — but the justification should say "no *comparable* witness", not "no
   witness at all".

6. **The 7.517 G / 7.316 G figures read as inconsistent.** The floor comment cites luna88k's lowest
   observed instructions-to-milestone as 7.517 G *idle*, while the design header quotes
   7.316–7.786 G over eleven boots without splitting idle from loaded. Both are probably true of
   different populations, which is exactly why quoting them side by side without saying so is a
   record defect. Populations must be labelled wherever an extreme is cited.

## 2026-08-15 — ADJUDICATION of the #418/#419/#420 residuals (Kimi holding the hat)

Fable has failed five consecutive liveness tests, and the standing directive names a **Fable/Kimi**
pass, so Kimi held it alone. This was an adjudication, not a review: the question was which
candidates are worth doing and in what order, not whether the diffs are correct.

### *** THE ORDERING VERDICT, WHICH OVERRIDES THE OBVIOUS ONE ***
**Do the pure-function `absorb()` selftest (B1) BEFORE #27**, even though #27 halts the emulator on
legal PPC guest code and sounds like it must dominate. The argument, which is accepted:

> #27's evidence will be produced by the very driver whose mutants currently survive **13 of 18
> gate rows**. Fixing the detector first makes #27's evidence worth something; fixing #27 first
> spends the gate's weakest credit. And the two exposures move in opposite directions — #27's halt
> is deterministic and known, so waiting costs nothing, while **the gate hole widens with every
> round that trusts it.**

It also matches the standing directive: accuracy first, bigger structural changes last, and #27 is
the most structural item on the list.

### FACTS THE ADJUDICATION CHECKED RATHER THAN JUDGED
* ***#27 is a deliberate `fatal()`*** at `cpu_ppc_instr_loadstore.c:66` — **loud by construction,
  not a silent hang.** The records had been carrying it as "halts the emulator", which is true but
  implies mystery. Its severity is unchanged; its diagnosis is not.
* ***#27 DEPENDS ON #47.*** #27's straddle fallback needs the translate-once fix
  (`memory_rw.c:84-87`) to be right first. They are ONE round, and **#47 goes first** — a
  dependency that was not previously recorded.
* **D1 is worse than filed:** `drive_guest.py` hardcodes `/tmp/gxregress` and IGNORES `$LOGDIR`
  entirely, so mutant runs cannot currently be isolated even if someone remembers to try.
  **[FIXED, round R1 (#422) + its follow-up: the driver reads `$LOGDIR` (`drive_guest.py:207`,
  made absolute before the `os.chdir` at `:211`) and `lib.sh:31` exports it. The panel measured
  that the obvious `os.environ.get(K, dflt)` form writes to the filesystem ROOT when `LOGDIR`
  is set but empty. Precise on the halves: the export is REQUIRED for a caller who writes
  `LOGDIR=x; ./run.sh` — the census shape — while a caller who already exported would have
  been served by the driver half alone, so the defect was CONDITIONALLY, not uniformly,
  silent. Detector: `selftest_logdir.py` in gate 2 — it runs the driver through a child shell
  that makes a BARE ASSIGNMENT and sources `lib.sh`, so removing either half turns both rows
  red (measured, two mutants). A gate-5 row would have been vacuous: in the default battery
  `$LOGDIR` IS the old hardcoded string.]**
* A2 confirmed: the branch is rig-blind — the comment knows about landisk, the code does not.
* A3 confirmed idle: no step pattern begins with `[`, so nothing can currently be withheld.
* A5 confirmed: "unfalsifiable" was verbatim in the shipped docstring (now corrected in both
  `gate_crossfamily.sh` and `drive_guest.py`).

### WHICH PREDICTED FINDINGS EARN A MUTATION RUN
* **A1 and A2: yes** — non-equivalent by construction, same surface, ONE batch, one fix commit.
* **A3: no** — an equivalent mutant, folded into B1's selftest as a unit test rather than a boot.
* **A4: no** — no code mutant exists; it is a claim about wall clock under load, to be answered
  with per-run telemetry rather than a synthetic overload against a bound with 50× headroom.
* **A5, A6: no** — *"prose has no mutants."* Settled by edit, in one record-hygiene commit.

### *** WHAT THREE ROUNDS OF HARNESS WORK SHOULD HAVE SURFACED AND DID NOT ***
These are new, and the first is the sharpest thing said all night:

1. **THERE IS NO DEAD-MAN SWITCH.** The nightly battery is UNCONDITIONAL, yet **nothing makes the
   ABSENCE of a terminal record a FAIL.** Every threshold shipped assumes the gate ran.
   *"No VERDICT line by deadline → red"* is a false pass that no current row can see — and it is
   exactly the shape of the open #125 check, generalised from one task into a missing mechanism.
2. **NO STANDING CANARY.** The directive mandates one mutation pass per *new* detector, but nothing
   carries a known-detectable mutant as a positive control in *every* run. The C probes already do
   this (`diff_wdc_identify.c:100-102`); gates 5, 7 and crossfamily do not.
   **Detector-alive must be proven per run, not per birth.**
3. **THE MUTANT CENSUS IS UNGENERALISED.** The 13-of-18 figure exists for ONE driver. Gates 5, 7
   and crossfamily have never had a survival census, and A1/A2 were found by panel reasoning rather
   than measurement. **If 13/18 is typical, every "verified" claim in this harness is
   over-credited.**
4. **NO AUDIT COVERAGE LEDGER.** #82's "never audited" was discovered by accident, and m88k has
   ZERO queue entries despite being booted nightly. A subsystem × family × last-audited ledger
   would make the queue's shape deliberate instead of a product of what happened to be noticed.
5. **HERMETIC RUN NAMESPACE AS POLICY.** D1 is one instance of a general gap: a run-id stamped into
   every log header, with each gate asserting the id it grades, plus a host fingerprint
   (load1/nproc/model) — which is also the permanent cure for the unlabelled-population confusion
   behind the 7.517 G / 7.316 G inconsistency.

### RESULTING ORDER
B1 (absorb selftest, folding A3) → A1+A2 as one mutation batch → A4/A5/A6 as one record-hygiene
commit → the disk batch → **#47 then #27 as one round, in that order** → #82 → #101 → #75.
The five gaps above are filed as their own candidates; the dead-man switch is the one to raise
first, because it is the only item whose absence hides every other row's failure.

---

## 2026-08-16 — residuals from R4's review (eight seats; the Fable seat deliberately not fired)

The R4 review found nothing wrong with the three shipped fixes — every seat that could trace
the code confirmed the domain clamp, the catch-up bound, the RTC narrowing and the
above-the-early-out placement. What it found was in the *instrument* and the *records*, all
fixed in the R4 follow-up. These are the items that were FILED rather than fixed, under the
standing stopping rule (only a measured false pass or a wrong record is fixed in-round).
Ranked, because the first is a live host crash.

1. **`dev_footbridge.c:141` — `random() % d->timer_load[i]` divides by a guest-written zero.
   MEASURED as SIGFPE, core dumped (exit 136).** `TIMER_1_LOAD` (`:417`) accepts
   `idata & TIMER_MAX_VAL` including 0 and calls `reload_timer_value()` directly. The guards
   are `TIMER_ENABLE` and `pending_timer_interrupts[i] > 0`.
   *** CORRECTION, 2026-08-15, AND IT LETS THIS ROUND OFF A HOOK IT PUT ITSELF ON. *** This
   filing originally said "#427/#428 convert a hang into a SIGFPE on this path". **HALF
   WRONG**, found by the measuring seat re-deriving the reproduction instead of citing its own
   earlier run. There are TWO routes to the division:

   * **Route 1**, as filed: `cycles == 0` → `freq = +INF` → before #427 that meant
     `interval = 0.0` and a catch-up loop that never advanced, so the machine froze before
     `DEVICE_TICK` ran. #427 clamps, #428 bounds, `pending` reaches `TIMER_MAX_CATCHUP` in one
     signal and the guard opens. This route IS opened by our hardening.
   * **Route 2 PREDATES BOTH.** `TIMER_1_LOAD` (`:413-424`) does NOT clear
     `pending_timer_interrupts[]` — contrast `TIMER_1_CONTROL` (`:447`), which does. So an
     ORDINARY LEGAL timer accrues a backlog (measured: 384 at 50 kHz), the guest then writes
     load = 0, and the next tick divides. No `+INF`, no clamp involved. **Measured against
     `git show 863d238^`, the pre-#427/#428 core: it crashes there too, exit 136.**

   The mechanism is that `DEVICE_TICK(footbridge)` is dispatched from `machine_run()`
   (`machines/machine.c:726-738`) — the MAIN EXECUTION LOOP, not the SIGALRM handler — so the
   CPU reaches the divide between signals, before any handler hang. Third route:
   `cpu_run_deinit()` (`cpus/cpu.c:411-415`) ticks every device twice at shutdown, so quitting
   with a zero load and a live backlog crashes on the way out.

   **So the honest statement is: the crash is PRE-EXISTING and guest-reachable on its own;
   #427/#428 added a second, faster route.** The original wording took blame this round had
   not earned — and a record that overstates a self-inflicted harm is no more true than one
   that hides it. The trap is
   CONFIRMED (a seat reproduced the core dump directly); the reachability is MANUAL —
   settling it needs a booted netwinder rig writing 0 to `TIMER_1_LOAD` and then enabling the
   timer. **Test-first is available here without a rig: the division is the subject, and an
   offline driver in the shape of `diff_timer.c` can reach it.**

2. **The domain ceiling and the catch-up cap do not meet, by a factor of 32.** The domain
   admits 2,147,483,647 Hz; the cap can deliver at most
   `TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY` = 68,157,440 ticks/s. Between them a guest can
   permanently request a rate the core can never serve, and the debt then grows without bound
   — MEASURED at 0.9683 s behind after one simulated second, delivered ratio 0.0317. Reached
   through an untouched caller: `cpu_mips_coproc.c` requests `emulated_hz / compare_diff`,
   which at `compare_diff == 1` is 166.56 MHz on Algor and 360 MHz on VoCore. **So the R4
   claim "every legitimate case is bit-identical" is false for those two machines** — two
   seats found this independently. Not made worse by R4 (the old code spun 33 million
   iterations per signal at the same rate), but unstated until now. The design question is
   whether an unserviceable rate should be rejected, dropped, or left to lag.

3. **The catch-up budget is per timer, and its derivation assumed one timer.** `timer.h`
   rejects 2^22 because it "would fill 59-77% of a 15.38 ms period" — but MEASURED, four
   timers at the ceiling take 10.65-10.74 ms of that period (69.2-69.8%), landing inside the
   very band that reasoning rejected. `dev_footbridge` has exactly four guest-controllable
   timers. The `#define`'s label ("ticks per timer per signal") is accurate; the derivation
   beside it is single-timer. Candidate fix: make the budget global across one signal.

4. **`timer_update_frequency`'s complaint is once per CHANGE, not once per timer**, so a guest
   alternating two out-of-domain rates drives an unbounded stderr write — MEASURED at 1000
   complaints for 1000 alternating updates. Same class as #265's flood. `dev_rtc` is immune
   (it pre-clamps); `dev_footbridge` is not. Candidate fix: a per-timer latch.

5. **`dev_sh4.c:193` `sh4_timer_tick()` calls `fatal()` then `exit(1)` from inside SIGALRM.**
   *(Line corrected 2026-08-17: this said `:191`, which is the `fatal()`; the `exit(1)` is
   `:193`. Cited three times before anyone read the line — the "read the line before citing
   it" rule, applied to a citation this file made about itself.)*
   Pre-existing, not introduced here, and `_exit()` is the async-signal-safe one.
   **`exitsweep` MUST NOT TOUCH THIS SITE, and the dependency runs the opposite way to the
   obvious guess.** It is tick-only — reached from the SIGALRM handler via `timer.c:284`
   (`timer->timer_tick(timer, timer->extra)`, inside the catch-up loop opened at `:283`), not
   from any `DEVICE_ACCESS` — so it is not in `exitsweep`'s class at all. Landing the generic
   complain-and-continue shape here first would make things *worse*: it keeps the
   async-signal-unsafe `fatal()` and **adds** a plain-`int` latch written from both the handler
   and the main loop, a data race this item would then have to undo. The right idiom is already
   in-tree at `timer.c:65` — `volatile sig_atomic_t timer_catchup_hit`, set in the handler and
   reported outside it.
   `pcc_timer_tick()` (`dev_pcc2.c:106` is its opening line, not the assert itself) likewise
   reaches interrupt work from the handler. Also pre-existing and
   worth recording together: `timer_stop()` does not block SIGALRM while disarming and
   replacing the disposition, so a pending signal can race that transition (harmless today —
   it delays one message by one stop), and `timer_init()` never clears `timer_catchup_hit`.

6. **#429 has no detector at all, and this is the fifth vacuity class in the taxonomy.**
   MEASURED: reverting `dev_rtc.c`'s range check entirely — or flipping its `>` to `<` —
   leaves gate 2 fully green, because nothing under `regress/` compiles or mentions
   `dev_rtc.c`. The differential cannot simply `#include` it: `dev_rtc.c` pulls in `cpu.h`,
   `machine.h`, `emul.h` and `device.h`. **The clean fix is to move the guest-rate narrowing
   into the timer core** — where the driver already reaches it, and where it belongs anyway,
   because `dev_footbridge`, `dev_vr41xx` and `dev_jazz` all derive a rate from a guest value
   and none of them range-check in the wide domain. That is a shipped-code change touching
   four devices, so it is a round of its own with a full panel, not a follow-up.

7. **A note on method, worth keeping because it generalises past the timer.** #425 established
   "read the constant from the header, never transcribe it". R4 followed it, and three seats
   independently MEASURED the consequence: a row that reads the constant is green for **any**
   value of it, so all three timer constants could be changed to values that break the round's
   claims with every row still passing. **Reading the constant defeats transcription drift and
   creates blindness to the constant itself. Both are needed: read it, and also assert an
   absolute consequence derived from outside the header.** Every differential in `regress/`
   that reads a `#define` for its expected value has this blind spot.
   **AUDITED the same evening, and the audit BOUNDS it:** all seven `regress/diff_*.c` were
   checked for macros on the expected side of a row. Four use none (`diskimage_geom`,
   `ieee_store`, `sh4_tmu`, `wdc_identify`). The two disk differentials use only TYPE TAGS and
   OPCODES — `DISKIMAGE_SCSI/FLOPPY/IDE`, `SCSICMD_READ_10`, `SCSICMD_REQUEST_SENSE`,
   `MACHINE_PMAX/EVBMIPS` — which do NOT carry the risk, because changing such a value is a
   rename that code and test follow together and no behaviour breaks. The risk is specific to a
   constant encoding a THRESHOLD or POLICY, where a different value IS different behaviour.
   **`diff_timer.c` was the only differential exposed and it is fixed.** What remains is the
   RULE, for any future differential that reads a tunable.

---

## 2026-08-15 — residuals from R5 (#430/#431), the page-crossing memory split

Eight seats reviewed the design; codex hit a CONTENT-POLICY FLAG after ~35 K tokens
("flagged for possible cybersecurity risk") and produced no verdict — a SEAT FAILURE of a
kind this project has not recorded before, and NOT a quota wall. Recorded by name so it is
not read as agreement. Six seats answered with a verdict; the Fable seat was deliberately
not fired (reserved for the batched regression review).

The design fork was settled by MEASUREMENT rather than by the 5-to-1 majority: one seat
argued for the late (memblock-generalising) split, and the row that decided it was a
straddling access beginning inside a device, which the late split leaves returning
`d0 d0 00 00` against a correct `d0 d0 bb bb`.

1. **`lvx`/`stvx` apply NO alignment mask at all** (`cpu_ppc_instr.c:3769`, `:3801`) — 16-byte
   accesses straight to `cpu->memory_rw`. Since 16 divides 4096, a properly masked effective
   address could never straddle; these straddle only because the mask is missing. That makes
   it arguably its own defect rather than evidence for #430. Whether real silicon masks the
   EA to 16 bytes is **BELIEVED, uncitable** — there is no PowerPC manual here.
2. **A partial `stwcx.` can leave a reservation held.** `lwarx`/`stwcx.` call
   `cpu->memory_rw` DIRECTLY (`:2309`, `:2357`), never through `LS_GENERIC_N`, so #431's halt
   never covered them; and the reservation is set in the instruction handler after
   `memory_rw` returns, so the split inside `memory_rw` is reservation-NEUTRAL (grep: zero
   references to `ll_bit`/`ll_addr` in `memory_rw.c`). It can only arise from an
   architecturally illegal unaligned `lwarx`. Filed as the missing alignment-exception model,
   not as a #430 question.
3. **The ARM 1 KB / mixed-AP subpage sibling.** `memory_arm.c:235` is the tree's only producer
   of `MEMORY_NOT_FULL_PAGE`. Under the split each half now gets its OWN `ok`, which is
   strictly better than one `ok` from the start page governing a two-page span — but the
   subpage case deserves its own rows.
4. **Every surviving straddle producer needs an UNALIGNED base**, in a tree that models no
   alignment exception. The scalar ARM slow path is NOT a producer (`cpu_arm_instr_loadstore.c:229`
   masks `addr &= ~(datalen - 1)` before the call); `lmw`/`stmw` issue one 4-byte access per
   register, not one large one; `arm_pop` (`cpu_arm_instr.c:1512`) IS a producer. **This is
   the honest way to state #430's severity: latent-but-real rather than routinely hit** — and
   it is the argument for fixing it once at the choke point instead of per caller.
5. **Device handlers now see two calls for a >1-page access into a multi-page device.** No
   handler was found that rejects an unexpected length except register-width devices
   (`dev_sgi_gbe.c:726`, `dev_sgi_ip32.c:698`, `dev_kn01.c:89`, ~15 in `dev_pcc2.c`), and a
   naturally aligned ≤4-byte register access cannot cross a page. MANUAL for the reading,
   **UNKNOWN for reachability** — the committed differential's D1/D2 rows are the standing
   check.
6. **Partial completion is RECORDED, not fixed.** A straddling write whose tail faults leaves
   the head written. The pre-change code had this property too (its memblock split still
   does), so the split does not introduce it; on a failing READ the new behaviour is strictly
   better — head kept, tail deterministically zeroed, and FAILED returned, where the old code
   returned OK with the wrong bytes. Atomicity is a separate question.

### R5 pass 2 added two more, both from the measuring seat's fuzz run

7. **An absurd length now GRINDS instead of mis-copying.** The overflow-safe loop test
   (`len > granule - offset`) is correct, but a length near `SIZE_MAX` iterates about 2^54
   times rather than being rejected — measured, a fuzz watchdog fired at two million chunks.
   Before the rewrite the same input silently under-split. No caller passes anything close
   (the largest transfers are `PHYSICAL` and exempt), so the code comment now says plainly
   that the case is declined rather than serviced. A length ceiling would close it.
8. **A straddling STORE whose second chunk faults leaves the first chunk written**, and the
   instruction then restarts — so an MMIO device at the head of the access sees the write
   TWICE. The read side of partial completion is recorded honestly in the differential's E4
   comment; this is the store side and it is the one with a visible consequence. Not
   introduced by #430 (the memblock split has had the property all along), but newly easier
   to reach now that the split fires 256x more often.

### And one method note, because it cost a vacuous row

**A row that measures an OPTIMISATION-DEPENDENT property must pin the optimisation.** "The
split is a loop, not recursion" was asserted by measuring stack growth — and gcc 15.2.1
eliminates the tail call at -O2, so the recursion mutant measured 96 bytes and the row passed
under the exact defect it existed to catch. One compile flag
(`-fno-optimize-sibling-calls`, on that differential only) turns it into a real detector:
loop 0 bytes, recursion 1,572,768. **Every row in `regress/` that measures a resource —
stack, allocation count, iteration count — has this shape and none of the others has been
checked for it.** Sibling of the `constblind` finding: there the row followed the constant,
here it follows the compiler.

---

## 2026-08-15 — the fbdiv round's residuals, and a bigger fish the audit found

#432 shipped the footbridge zero-load crash. Two read-only sub-agents ran in parallel with the
implementation; between them they obtained a datasheet this project has lacked since the
footbridge was written, and they found a guest-reachable host kill on a rig that **boots today**.

### *** THE HIGHEST-PRIORITY ITEM IS NO LONGER FOOTBRIDGE ***

**`dev_m8820x.c:220` — `DEVICE_ACCESS(m8820x)` has a `default:` arm that calls `exit(1)` on ANY
unhandled offset, on READS as well as writes, in a 4 KB window — and `dev_m8820x` is
memory-mapped on LUNA88K, which is one of the three rigs that actually boots in this tree.**
`M8820X_LENGTH` is 0x1000 (`cpu_m88k.h:229`) — 1024 word offsets — and the switch handles **18** of
them (a pass-2 seat counted the labels; the first filing said 21, which UNDERSTATED the gap, so the
finding is stronger than it was written). Everything else terminates the host. That includes registers the CMMU header itself
defines: `CMMU_CDP0-3` (0x800-0x80c), `CMMU_CTP0-3` (0x840-0x84c), and pointedly
**`CMMU_CSSP1/2/3` (0x890/0x8a0/0x8b0)** — `m8820x.h:86-91` defines `CMMU_CSSP(n)` for sets 0..3
and GXemul implements only set 0, so a cache-flush loop over the four sets walks straight off the
handled set. **Tempering that one honestly, from reading the header rather than the report:** the
line above CSSP1 says *"the following only exist on 88204"*, so a guest driving an 88200 would not
touch them and this particular example is weaker than it first looks. It does not rescue the
site — the gap is 18 handled offsets in a 1024-word window, and CDP0-3/CTP0-3 carry no such
caveat — but the CSSP example should not be quoted without the qualifier. Whether OpenBSD 7.7 actually does that is BELIEVED, not confirmed (no driver source
in tree, nothing booted for the audit) — but the register-map gap is CONFIRMED from the two files.
Ruled out while checking: `regs[]` is sized `M8820X_LENGTH/sizeof(uint32_t)`, so the unconditional
`odata = regs[relative_addr/4]` is in bounds — there is no OOB read hiding behind the exit.

Four more on the same booting rig, all CONFIRMED: `dev_luna88k.c:816` (write to `INT_ST_MASK0..3`
with any of bits 25..0 set), and `dev_m8820x.c:159` (**read** of `CMMU_SCR`), `:152` (write to the
read-only `CMMU_IDR`), `:169` (write to the read-only `CMMU_SSR`), plus `:125` transitively via
`m8820x_command()`.

**Tree-wide inventory, for the first time:** 220 `exit(`/`abort(` hits across `src/devices/`, of
which **114 are directly inside a `DEVICE_ACCESS` handler**, 17 are init-time, and 89 are in
helpers mostly called from `DEVICE_ACCESS`. **These counts are PATTERN-DEPENDENT and are marked
UNKNOWN until the round that acts on them re-derives them with its pattern stated**: the audit
stripped comments and strings before attributing each hit to its enclosing function, while a naive
`grep -c` over the same files gives 304. Both numbers can be right about different questions, which
is exactly why the pattern has to travel with the count. No `abort()` is guest-reachable. Two deliberate
exclusions, both checked: `dev_cons.c:80` is the testmachine's documented halt port (`exit(0)`,
intended), and `dev_ram.c:132`'s `default:` is not guest-reachable (`d->mode` is set at init).
**The rig question dominates the ranking**: arc and pmax have ZERO `DEVICE_ACCESS` exit sites
between them, so luna88k's five are the only ones reproducible today.

### `lunafuse` (2026-08-19) — filed properly, having existed only in a commit message

`dev_luna88k.c:573`'s byte-write arm is an unlatched `fatal("TODO: luna88k byte write to
fuse")` that **drops the write**, while the *word*-write arm directly above it stores. So the
model both lies and is width-inconsistent, and it is guest-reachable by a byte store to
`FUSE_ROM_ADDR`.

**It is NOT part of #438 and could not have been**, under the reopening rule the witness ladder
adopted: different semantic class (doctrine arm 3, where complain-and-continue may be exactly
the wrong shape, since dropping a write that changes state makes the model *lie* rather than
*lag*), and it needs a new oracle.

*Filed here because the flagship review found the filing existed **only in `cf4b083`'s commit
message** — no `OUTSTANDING_BUGS` line, no ledger row, no queue item. This project's own history
is that a commit-message-only filing is how work is forgotten.*

### `#437` residuals (2026-08-18) — filed by the pass-2 panel, not fixed in that round

The stopping rule admits a MEASURED FALSE PASS or a WRONG RECORD into the round that finds it.
These are neither, so they are filed rather than chased — the rule exists because an earlier
item ran six follow-up passes without converging.

#### `exitsweep` scope: "reproducible — ONE" is NOT what the table says (2026-08-19)

The inventory row reads **"reproducible by BOOTING a rig we have — ONE"**, and that is correct
as written. It has since been read as the broader claim *"reproducible — ONE"*, and used as the
justification for keeping the round at one site. **A measure seat has now witnessed a SECOND
site with a probe rather than a boot**: `dev_footbridge.c:495-497`, `case IRQ_ENABLE_SET:` on a
READ, reached from a `cats` cold-debugger probe — two arms of one script differing by a single
instruction, the isolation arm surviving with both controls green and the kill arm exiting 1.

**The round should still implement one site, but NOT for that reason.** The real bound is the
third doctrine arm, which is already written down above and is far stronger: complain-and-continue
is safe only when the dropped write's sole observable consequence is the register's own value.
That bounds the round on SEMANTICS, and semantics do not evaporate when someone writes a probe.

Proposed reopening rule, naming a condition rather than a number: add a second site only when it
is (a) witnessed by boot or probe, (b) in the **same device and same semantic class** so one fix
design covers both, and (c) covered by the **same detector** without a new oracle. Under it the
eight footbridge sites are **one candidate round, not eight**.

- **`m437ord` — the ordering rule is reasoned and reviewed, but NOT gated.** `diskimage_sync()`
  declines to sync an overlay's bitmap after its data fsync fails. Deleting that `continue` is
  the one mutant the shipped detector does not catch: the measure seat verified a row CAN catch
  it by injecting an fsync failure and asserting the bitmap fd is ABSENT from the trace
  (shipped syncs fds `[4 5 6]`; the mutant syncs `[4 5 6 7]`). **BUILT AND SHIPPED in `e051fc5`, and it took TWO overlays** — with one, `continue` deleted / `break` / `return 0` all trace identically. It ran green in the battery at `6014b7e`. *(This line read "One row, not yet built" for a day after the row existed — the dated-tail-carries-no-resolution-markers class, caught by the regress adjudication.)*
- **`m437multi` — a spurious CHECK CONDITION on a multi-overlay disk.** `fwrite_helper` writes
  only to the LAST overlay, so earlier ones hold no guest data — yet a failed fsync on overlay 0
  fails the whole command with sense 3-0c-00 while every guest byte is durable. Conservative,
  but wrong, and it costs two extra fsyncs per additional overlay.
- **`m437rtmp` — under `R:` the durability claim does not mean what it sounds like.**
  `diskimage_add_overlay(d, tmpname, true)` unlinks BOTH overlay files immediately after
  opening (`diskimage.c:177-184`; measured: `fstat(f_data).st_nlink == 0`). Syncing them makes
  bytes durable in files no post-crash reader can open. `R:` is meant to be ephemeral so this is
  not a defect, but `#437`'s framing presents `R:` as the motivating case and should not.
- **`idesync` — IDE has no durability path at all.** The `#437` fix is SCSI-only;
  `grep -i flush src/devices/dev_wdc.c` returns nothing, so a guest's ATA `FLUSH CACHE` is not
  merely unflushed, it is unimplemented. Reachability unknown — landisk is the ATA rig.

#### CORRECTED 2026-08-17 by the `exitsweep` assess panel (7 seats) — read this, not the above

The paragraph above is left standing rather than rewritten, because what it got right matters as
much as what it got wrong. **Its hedge was correct and load-bearing**: it marked the counts
PATTERN-DEPENDENT and UNKNOWN "until the round that acts on them re-derives them with its pattern
stated". That round has now happened, and the hedge is what made the correction cheap.

- **220 was not wrong. It was STALE BY ONE ROUND.** It reproduces *exactly* at `84f442d`, the HEAD
  it was recorded on, and is **215** today because `#433` removed the five `dev_m8820x.c` sites.
  Six of seven panel seats concluded "denominator unsound"; the measure seat compiled the scan and
  showed they were too strong. **Nothing could tell stale from wrong, because the METHOD was gone**
  — which is why the census now ships as `tools/pipeline/census_exits.py` instead of as a number.
  Re-run it; its output is authoritative and this text is not.
- **The in-handler count is 115 today** (119 at the record's own HEAD), not 114.
- **"17 init-time" undercounts by 8**: it counted only the `DEVINIT()` macro form and missed the
  longhand `dev_*_init` functions. The instrument reports **25**.
- **"89 helpers, *mostly* called from `DEVICE_ACCESS`" — `mostly` was doing a lot of work, and it
  has now been resolved**: **50 of 82** are genuinely reachable from a handler, 31 are not, and 1
  is tick-only. Corrected guest-reachable total: **170**, not 114.
- **A whole class was missing.** `CHECK_ALLOCATION` → `FAILURE` → `exit(1)` (`src/include/misc.h`)
  is invisible to every `exit(`/`abort(` pattern, and there are **183** such sites — the majority
  of all terminators here — **5 of them inside a `DEVICE_ACCESS` handler**, including
  `dev_wdc.c:873` `malloc(512 * count)` where the count is guest-set. Full total: **398**.
- ***"No `abort()` is guest-reachable" is FALSE.*** `dev_sgi_ip30.c:127` sits inside
  `case 0x10020: /* Set ISR */ d->isr = idata;` — an ordinary guest register write — and
  `dev_sgi_ip22.c:315` is the same shape in a mask-register write path. `abort()` is *worse* than
  `exit(1)`: SIGABRT and a core dump. (`bus_pci.c:222` genuinely is host-side and was classified
  correctly.)
- ***"luna88k's five" is a misreading of this file's own sentence.*** `dev_luna88k.c` has **ONE**
  `DEVICE_ACCESS` and two exit sites: `:816` guest-reachable and `:998` init-time. The five were
  `dev_m8820x.c`'s, and **`#433` already fixed them** — not `#435`, which is the translation-cache
  purge round.
- ***"arc and pmax have zero, so luna88k is the only reproducible one" omits a rig.***
  **`landisk` boots here** (`regress/gate_crossfamily.sh:199` runs `openbsd76-landisk-bsd.rd`), and
  `dev_sh4.c` carries 21 in-handler plus 7 reachable-helper sites. Honest negative result: no kill
  was demonstrated there — all eight one-value guards in `sh4_pcic_access` are written by the
  healthy guest with exactly the hardcoded constant on every boot, and `-M` is ignored because
  `machine_landisk.c:84` hardcodes 64 MB.

**And the doctrine gained a third arm, which BOUNDS this item rather than enabling it** — see the
`exitsweep` ledger row. Complain-and-continue is safe only when the dropped write's only observable
consequence is the register's own value. Where the write's PURPOSE is to change how the emulator
decodes, translates, transfers or invalidates, dropping it makes the model **lie** rather than
**lag**: at `sh4_dmac_transfer` the only implemented `CHCR_RS` mode transfers nothing, so a latched
drop means no bytes moved, `CHCR_TE` never set, and the guest polls forever — strictly harder to
diagnose than the `exit(1)` it replaced, **and the latch actively suppresses the evidence**.
`#433`'s own adjudication hit this once (`FLUSH_SUPER_LINE`) and fixed it locally without writing
the rule down. **A mechanical sweep over the 170 would ship it again.**

Useful for whoever writes the fixes: `memory_rw.c:572-578` already snapshots `cpu->running` around
the handler call and returns `MEMORY_ACCESS_FAILED` if the handler cleared it — so the `#220`
`cpu->running = 0` pattern is fully plumbed and needs nothing new.

### The eight footbridge sites (`#432` removed the ninth)

Addressability settled: the window is `[0x42000000, 0x42000400)` on BOTH machines
(`machine_cats.c:63-64`, `machine_netwinder.c:58-59`), `DEV_FOOTBRIDGE_LENGTH` is 0x400, and all
eight offsets fall inside it. Ranked by how likely a booting guest is to hit them, the top two are
**reads**: `IRQ_ENABLE_SET` (0x188) — which `dc21285reg.h:334-335` also names plain `IRQ_ENABLE`,
the register a spl save/restore reads — and `IRQ_ENABLE_CLEAR` (0x18c). In both cases GXemul
computes `odata = d->irq_enable` and then exits anyway. Then `IRQ_STATUS` (write-to-ack),
`SDRAM_BA_MASK` (read), `SDRAM_BA_OFFSET` (read), `FIQ_STATUS`, `IRQ_RAW_STATUS`, `FIQ_RAW_STATUS`.
The recommendation is to fix all eight rather than the plausible subset: the property being
restored is "no guest register access terminates the host", and the implausible ones are exactly
what a *wrong* guest reaches, which is the population the fix exists for. Note a real NetBSD/cats
guest has run this driver here without hitting any of them (`REVIEW_FINDINGS.md:171`, `:186`) —
a genuine negative-reachability datum that caps every plausibility claim above.

### Datasheet-backed defects, newly specifiable

The 21285 datasheet (`_scratchpad/dc21285.pdf`, Intel 278115-001) closes three questions that were
blocked on it:

*A caveat that travels with every §7.3.41 citation here:* the register table is COLUMN-MANGLED in
the `pdftotext -layout` extraction — it prints "5:4" beside the prescaler decode list. The "bits
3:2" reading is right, but it is right by RECONSTRUCTION: `dc21285reg.h`'s 0x04/0x08/0x40/0x80 pin
the prescaler at bits 3:2, Mode at 6 and Enable at 7. Said here because a future reader of the
`.txt` will hit "5:4" and reasonably doubt the record.

1. **FREERUN vs PERIODIC is ignored.** §7.3.41 bit 6: free-running wraps to `FFFFFFh` and keeps
   decrementing; periodic reloads `TimerNLoad`. The clock source is bits 3:2 alone, identical in
   both modes. `reload_timer_value()` computes one rate and hands it to a repeating timer, i.e.
   the PERIODIC cadence unconditionally — so a FREERUN timer's interrupt rate is too fast by up to
   `2^24 / load`.
2. **`TimerNValue` is READ-ONLY** (§7.3.38/7.3.40) but `dev_footbridge.c` accepts a guest write to
   it; and `case TIMER_1_CLEAR:` has **no `writeflag` test at all**, so a guest READ of a
   write-only register reloads the counter and deasserts the IRQ. Both one-line, safe under any
   semantics.
3. **Reset values diverge.** Hardware resets `TimerNControl` to 0x00 (free-running, fclk, disabled)
   and `TimerNLoad` to 0; the model sets `TIMER_MODE_PERIODIC` and `TIMER_MAX_VAL`. A guest reading
   `TimerNControl` before writing it sees 0x40 where hardware gives 0x00. **This is the model bug
   that #432's first draft mistakenly cited as evidence for its own zero mapping** — see that
   round's block.
4. **The `random()` counter model is now fully specified** and can be replaced: §7.3.40 plus
   §7.3.41 bit 7 give a 24-bit down-counter, readable at any time, RETAINED across disable and
   resuming from its current value on re-enable. The author's TODO is discharged; only a rig is
   missing.

### And the 8253 question is settled from a real document

`i8253reg.h` says nothing about a zero count (read in full, 102 lines). The Intel **8254**
datasheet (`_scratchpad/i8254.pdf`, 231164-005) does, twice on p. 17: *"The largest possible
initial count is 0; this is equivalent to 2^16 for binary counting and 10^4 for BCD counting."*
So `dev_8253.c:125`'s `else hz = 0` — which the timer core then floor-clamps to 1e-8 Hz, i.e.
never fires — is wrong against the hardware convention: count 0 means 65536. Cite it as the 8254,
not the 8253; the count-0 convention was verified in the 8254 document only.

### m8820x: REPRODUCED test-first, and it is worse than the audit filed

Before any edit, an offline driver (`_scratchpad`, not committed) drove **every word offset in the
mapped window** through the shipped `dev_m8820x_access`, each probe in a forked child so one host
kill did not end the run. Measured on the committed build:

| | |
|---|---|
| word offsets in the 4 KB window | **1024** |
| offsets whose **READ** kills the host | **1007** |
| offsets whose **WRITE** kills the host | **1009** |
| offsets whose READ survives | **17** |

So **98.3% of the window terminates the host process on a plain read.**

*** THE FIRST VERSION OF THIS TABLE WAS WRONG, AND IT WAS WRONG IN MY OWN HARNESS. *** It said
1013 / 1015 / 11. A review seat derived 1007 / 1009 / 17 from the source alone and named the exact
mechanism: the `PFSR PFAR SAR SCTR SAPR UAPR` arm calls
`c->invalidate_translation_caches(c, 0, INVALIDATE_ALL)` **before** the `writeflag` check, so it
fires on READS too — and my offline driver left that callback NULL. Six offsets SIGSEGV'd in the
DRIVER and I counted them as device kills, in both directions, which is the symmetric +6 signature
the seat spotted. Re-measured with a no-op callback installed and with the child's exit status
DISCRIMINATED (status 1 = the real `exit(1)` path, a signal = a harness fault): **1007 / 1009 / 17,
matching the source-derived prediction exactly.**

This is mechanical rule 4 — *"did it fail for the reason under test?"* — violated inside the
reproduction that was supposed to establish the defect. The defect is unaffected and still
overwhelming; the number was not. The committed detector must discriminate exit status the same
way, or it will enshrine the artifact.

The in-arm exits do add to the default arm, but by ONE on the read side, not seven: the only
in-arm READ exit is `CMMU_SCR` (`:157-159`), so 18 handled offsets minus that one gives the 17
survivors. On the write side `CMMU_IDR` and `CMMU_SSR` add two more, plus `CMMU_SCR` with an
unimplemented command value.

There are **five** `exit(1)` calls in the file, not "four inside the handler": four lexically inside
`DEVICE_ACCESS` (`:152` IDR-write, `:159` SCR-read, `:169` SSR-write, `:220` the default arm) and
one in the static helper `m8820x_command()` (`:125`), reachable from the SCR-write arm.

The count of handled offsets is **18**, confirmed by listing the case labels
(`CMMU_IDR SCR SSR SAR SCTR PFSR PFAR SAPR UAPR BWP0-7 CSSP0`). The first filing said 21; a
pass-2 seat caught it and the correction makes the finding stronger, not weaker.

**This is the first item in this sequence whose detector can be ONLINE** — luna88k boots in this
tree — but the offline driver above already reproduces it, so the fix is test-first-able today
either way. `memory_rw.c:572-578` already plumbs the `#220` `cpu->running = 0` return path.

### Seat health: minimax-m3 is an UPSTREAM OUTAGE, and the three failure modes are now separable

`minimax-m3:cloud` returned `HTTPError 500` on the R6 pass-2 brief and again on a single-seat
resend. Diagnosed rather than assumed, because this seat has three historically distinct failure
modes that look identical in the output file:

* **the endpoint is alive** — `glm-5.2:cloud` answered a one-line ping immediately;
* **the model is still served** — `minimax-m3:cloud` is present in `/api/tags`;
* **so it is neither a quota wall nor the file-reading stall** that used to characterise this seat
  (it had answered four consecutive packet briefs before this).

That leaves a server-side fault in the model backend. Recorded by name, never counted as
agreement, and **re-test before pruning** — this project has now been wrong three times about a
seat being permanently dead. Note `minimax-m2.7:cloud` is also served and could stand in; if it
is ever used it must be recorded as a SUBSTITUTE, never as "the minimax seat".

### m8820x: the rig was BOOTED with instrumentation, and it reframed the round

The measuring seat did what neither footbridge round could: it instrumented a scratch copy of the
device, drove a **full boot to a root shell** with the repo's own `drive_guest.py`
(`VERDICT=PASS`, login at 132.3 s, both FP values correct), and logged every offset and command a
real OpenBSD/luna88k guest actually touches. It also proved the logger CAN fire before trusting a
zero — the same binary emits an `EXITSITE` line the moment a probe reaches the default arm.

**A real guest touches 17 of 1024 words and 7 of 256 command bytes. Every one is already handled.
Zero of the five `exit(1)` sites is reached on a boot.**

*** BUT THE MOST REACHABLE EXIT IS NOT THE DEFAULT ARM, AND THAT IS THE FINDING. ***
Commands `0x34` and `0x24` reach `exit(1)` through **`CMMU_SCR` — an offset the model FULLY
HANDLES, and which this guest writes 640,016 times per boot.** `0x34` (FLUSH_SUPER_LINE) is ONE
BIT away from `0x35` (FLUSH_SUPER_PAGE), which the guest issues 158,664 times. Nine of the 22
commands defined in `m8820x.h` fall to `exit(1)`. So the exposure is not obscure reserved
offsets; it is a one-bit-different command on the hottest path in the device.

**Reachability is one instruction**, measured by a cold-debugger probe with every word
disassembled before stepping and every death attributed to its own diagnostic:

| probe | result |
|---|---|
| `ld r4,r5,0x0` (IDR read, control) | **SURVIVED, r4 = 0x00a90000** — the real IDR value |
| `st r4,r5,0x4` command 0x35 (control) | SURVIVED |
| `ld r4,r5,0x4` (SCR read) | HOST DIED — `read from CMMU_SCR: TODO` |
| `st r4,r5,0x0` (IDR write) | HOST DIED — `write to CMMU_IDR: TODO` |
| `st r4,r5,0x8` (SSR write) | HOST DIED — `write to CMMU_SSR: TODO` |
| `st r4,r5,0x4` command 0x34 / 0x24 | HOST DIED — `unimplemented command` |
| `st r4,r5,0x840` (CTP0) | HOST DIED — `unimplemented write to offset 0x840` |

The control returning `0x00a90000` is what makes it airtight: that value can only have come
through `dev_m8820x_access`. **`/dev/mem` from the guest userland is refused** (`Operation not
permitted`, securelevel 1), so OpenBSD userland is not a route — an honest negative that removed
the most convenient online-gate design.

**THE FIX IS BOOT-NEUTRAL, which means the rig CANNOT be the detector.** All three candidate
behaviours boot identically, because the arm is never reached on a boot. The choice has to be
argued on other grounds, and the detector has to be something sharper than "it still boots".

**The `#220` precedent reads AGAINST halting**, on a closer look than the brief gave it:
`dev_footbridge.c:348-349` uses `cpu->running = 0` because the GUEST ASKED THE MACHINE TO HALT
(GP16 reset) — that is the correct model, not a failure mode — while `:379-380` uses
complain-and-continue for an out-of-range PCI bus. The tree assigns the two shapes to two
MEANINGS. Neither m8820x site is a halt request.

**Detector shape, and it overturns this brief's own premise:** measured on this host, a full rig
drive costs 182-233 s while the cold-debugger probe costs **3.1 s for 8 rows** — 60-75x cheaper,
because reaching this device needs a constructed machine and one `step`, not an operating system.
The online probe is also structurally immune to the artifact that fooled the offline driver above:
a harness fault produces no `m8820x:` diagnostic at all, so the two are distinguishable BY
CONSTRUCTION rather than by remembering to check an exit status. Keep an offline differential for
breadth (1024 offsets x 2 directions x 256 commands is not a pty job). Build NO booting-rig row —
it could only assert "luna88k still boots", which `gate_ab` and `gate_crossfamily` already assert,
at ~200 s of load-sensitive wall clock added to a battery already carrying ~37 such oracles.

**And the rows must assert VALUES, not survival.** Rounds 79/80 taught this project that a
survival-only row cannot tell a repaired instruction from one that merely stopped faulting. The
smallest edit that breaks the property while passing a survival-only row: replace `exit(1)` with
`return 1` but drop the `memory_writemax64` — the guest gets garbage and the row goes green. Pin
the control at `r4 == 0x00a90000`, and carry a row for ALL FIVE sites, since a fix that repairs
the default arm and leaves the four in-arm exits passes any detector that only probes `0x800`.

### R7 pass 2: the fold is CONFIRMED correct, and the detector defending it was weak

The measuring seat white-boxed the fold with a fixture the committed row does not have — seven
PATC entries spanning {SAR page, same segment/other page, other segment} x {supervisor, user},
with **SAR deliberately not page-aligned** so a LINE address is actually exercised. Result:

* **LINE = PAGE is EXACT, not merely safe.** A LINE flush drops only the entry on the SAR page;
  same-segment-different-page and other-segment entries survive. The PATC is page-granular, so
  PAGE is the minimum representable unit and LINE over-invalidates by nothing at all.
* **SEGMENT = ALL over-invalidates, in the safe direction only** — a strict superset, never a
  subset, across all eight commands.
* **The supervisor extension is correct**: zero wrong-privilege invalidations in any command.

*** BUT ELEVEN OF TWENTY-ONE MUTANTS SURVIVED THE FIFTEEN SHIPPED ROWS, and the cheapest was ONE
DELETED CHARACTER. *** Removing the `!` from `if (!all && ...)` turns every `FLUSH_*_ALL` into a
single-page flush — the exact under-invalidating TLB the fold exists to prevent — and every row
passed, because D1 seeds ONE entry at the flushed address and so can only ever show that a
MATCHING entry goes away. Second worst: deleting the `invalidate_translation_caches()` call
leaves the PATC correct while the emulator's OWN dyntrans cache keeps the torn-down mapping,
reaching the same failure by another route — **and the differential was already counting that
callback and never asserting on it.**

Eight rows now close it (D3-D10): flush scope in both privilege directions, the superset
property, the dyntrans purge and its control, and the two coupled write-drop rows. Census after:
**12 mutants, 12 killed, 0 survived, 0 faults.**

**One row of mine went red on correct code and was fixed as a TEST defect**, not a code change:
D6 first asserted that a SEGMENT flush spares another segment's entry. It does not, and is not
meant to — SEGMENT is deliberately mapped to ALL. "Did it fail for the reason under test?" It did
not. The row now pins the safe direction (SEGMENT is a superset of PAGE), which is the property
actually claimed.

### Two records in the shipped source were wrong, and are corrected

1. The latch comment claimed the first unmodelled access "of each kind" is reported in full.
   **Measured, 1 of 4 kinds**: one `reported_offset` flag covers unhandled offsets, IDR writes,
   SCR reads and SSR writes, so a guest that writes IDR once permanently demotes the diagnostic
   for every offset it later touches. A per-kind latch is FILED, not done — widening it is a
   behaviour change and this round's claim is only that the host stops dying.
2. The SSR arm said SSR is "written by the MODEL". **Nothing in the tree ever writes
   `reg[CMMU_SSR]`** — only PFSR and PFAR are model-written. The conclusion held; the reason did
   not, and the right reason is stronger: dropping the write is what makes the command arm's
   argument true, because a guest that could store there could set the V bit and turn a dropped
   PROBE into a plausible-looking valid translation.

### Two residuals filed from the same pass

* The unhandled-access message is built with `snprintf` on EVERY access even when latched and
  discarded — measured 27.7 ns/read and 54.7 ns/write on the latched path.
* `regress/diff_m8820x.c` only links because of `-Wl,--gc-sections` (it pulls in `devinit_m8820x`
  → `memory_device_register`). On a linker without it the gate row goes **red, not skipped** —
  and the sibling `diff_sh4_tmu` compile in the same gate does not use those flags.

### ns16550: the divide-by-zero is REAL but DOES NOT FIRE IN THE SHIPPED BUILD

Filed by two seats as a guest-reachable host kill on the live arc rig, and ranked as the cheapest
remaining host kill. **Measured test-first, that ranking is wrong.**

`dev_ns16550.c:181` computes `(int)(115200 / d->divisor)` as an ARGUMENT to `debug()`, and both
divisor bytes are guest-writable (`:154` low, `:179` high). An offline driver reproduced the exact
guest sequence — set DLAB via `com_lctl` 0x80, write 0 to the low byte, write 0 to the high byte —
and confirmed by read-back that `dlab == 1` and `divisor == 0` at the division, with `debug()`
reached twice, so the path is genuinely exercised rather than skipped.

| optimisation | result |
|---|---|
| `-O0` | **SIGFPE, core dumped** |
| `-O1` | **SIGFPE, core dumped** |
| `-O2` | survives |
| `-O3` | survives |
| `-Os` | survives |
| **the tree's own flags** (`-fgnu89-inline -O3 -DNDEBUG`) | **survives** |

**So the host does not die in the configuration this project actually builds.** At `-O2` and above
gcc exploits the undefined behaviour and elides the division; the guest gets a garbage bps figure
in a debug message nobody reads at default verbosity.

This does NOT make it a non-defect. It is undefined behaviour on a guest-reachable path, and which
way it resolves is a property of the compiler rather than of the code — a `-O0` debug build, a
different gcc, or a different compiler can restore the crash at any time. But it is **not** the
cheapest remaining host kill, and it should not be worked ahead of items whose severity does not
depend on build flags.

*** THIS IS THE `optrow` CLASS AGAIN, ON THE OTHER SIDE OF THE GLASS. *** `optrow` recorded that a
row measuring a RESOURCE is only as good as the optimisation it pins — a detector following the
compiler. Here it is the DEFECT that follows the compiler: the same UB is fatal at `-O1` and
invisible at `-O2`. Any severity claim about undefined behaviour has to name the build flags it
was measured under, and neither of the two seats that filed this one did.

**And the reproduction caught its own harness first**, which is why the numbers above can be
trusted: the first run reported all three probes dying, INCLUDING the control with a legal divisor
of 12. The cause was `d->addrmult` left 0 by `calloc`, and `dev_ns16550_access:138` divides
`relative_addr` by it — so the harness produced **SIGFPE for the wrong reason**, indistinguishable
from the defect under test. The control row is the only thing that separated them.

### A panel-completeness audit found a surviving mutant, and the audit is the finding

Asked what remained to complete the panels, I audited all eight fired today rather than asserting
they were done. **Every seat produced a substantial answer in every panel — no seat failures.**
But several answers had never been READ: codex and kimi on two panels, and **the entire seven-seat
script panel for R7 pass 2**, where I had acted only on the Opus agent's report.

An unread answer is worse than a seat failure. A failure is recorded honestly and counted as
absence; an unread answer is silently discarded while the round is reported as reviewed.

Reading them changed something. All seven independently traced the fold and confirmed it correct,
converging with the measuring seat — but **agy named a mutant my own census had never run**:
deleting `cmd == CMMU_FLUSH_USER_SEGMENT` from the `all = 1` set, which makes a USER segment flush
page-granular instead of full-table. Run against the 23-row differential it **SURVIVED**.

The cause is an asymmetry worth remembering: every flush-scope row drove a SUPER command except
one, which was USER *ALL* rather than USER SEGMENT. The supervisor half of the property was
pinned and the user half was not — exactly the shape a single-sided row hides. Row D6b closes it,
and the census is now **14 mutants, 14 killed, 0 survived, 0 faults**.

**The rule this yields: a panel is not complete when its seats have answered, only when they have
been READ.** Firing nine seats and reading four is a four-seat review reported as nine.

- **m8seg — SEGMENT flush maps to ALL, and the over-invalidation is guest-visible.** (filed
  2026-08-16 from the R7 pass-2 grok seat, which attacked its OWN pass-1 advice.) The fold sends
  `CMMU_FLUSH_{USER,SUPER}_SEGMENT` to the `all = 1` arm. That is the safe direction — under-
  invalidation is the one that leaves a stale translation — but it is **not** free of guest-
  visible effect, and the shipped comment said it was. `memory_m88k.c:356-365` writes `PG_U`
  (and `PG_M` on a write) back into the page descriptor **in emulated memory** on every walk,
  while a PATC hit sets those bits only in the PATC copy (`:348-350`). So a guest that clears U
  on a page in segment B, issues a segment-A flush, and then touches B observes a U bit that a
  correctly-scoped flush would have left clear. The tighter mapping needs no manual: match on
  the walker's own 4 MB segment size, `(sar ^ vaddr) & 0xffc00000`. Not done in R7 because it is
  a behaviour change and the round's claim was only that the host stops dying. The comment at
  `dev_m8820x.c:161` is corrected; what real silicon does at segment granularity is UNKNOWN.

- **ASSESSED, NOT CHANGED — the ns16550 shape is singular in this tree.** A task the R6 pass-2
  kimi seat named, in an answer that had gone unread for a day: *"a one-grep sweep for other
  divisions in `debug()`/`fatal()` argument position with guest-writable operands — ns16550 is
  unlikely to be the only instance of that specific shape."* A grep cannot answer it — the
  operator has to be in ARGUMENT position with literals and comments already stripped, and the
  call may span lines — so `regress/diag_div_sweep.py` balances the parens and does it properly.
  **MEASURED: 24 sites, 22 with a compile-time-constant divisor (which cannot be zero, so are
  not the shape), 2 non-constant.** Those two are `dev_ns16550.c:79` (`115200 / d->divisor`, the
  known one, filed as `ns16550`) and `diskimage.c:543` (`bytes_left % ct->sector_size`), and the
  second is **not drivable**: every unrecognised TRACK mode does `goto fail` at `:819` while
  `nr_of_pt` is incremented only at `:823`, so a counted track always carries 2048/2336/2352 —
  and the plain division at `:974` would fault first regardless of any diagnostic. So kimi's
  hypothesis is **refuted by measurement**, which is a result worth having rather than a
  non-event. The sweep is committed and wired into gate 6 as a two-row class ratchet (the count
  AND the denominator, so a sweep that silently stopped finding anything cannot read green), and
  negative-controlled in both directions: planting one instance moves it to 3/25.

- **RECORDS CORRECTED from the R6 pass-2 codex answer, which had gone unread for a day.** Three
  findings, each CHECKED rather than judged, with three different outcomes — which is itself the
  argument for reading a seat instead of scoring it.
  1. **"21 handled offsets" was wrong — it is 18** (`CONFIRMED`; the `DEVICE_ACCESS(m8820x)`
     switch has 18 `case` labels). Corrected above. The measured survival counts are a *third*
     set of numbers and do not contradict it: pre-fix, 17 of 1024 offsets survived a READ and 15
     survived a WRITE, because some labelled offsets still exited — `CMMU_SCR` on read, `CMMU_IDR`
     and `CMMU_SSR` on write. Case labels, surviving reads and surviving writes are three
     different quantities and this record now names all three so it cannot be re-broken.
  2. **"A legitimate guest write of 0x1000000 — one full wrap" was overstated** — withdrawn,
     `CONFIRMED` against the local datasheet rather than accepted on the seat's word: §7.3.39
     gives TimerNLoad as bits 23:0 R/W with **"31:24 — R Read only as 0"**, so bit 24 is not a
     truncated write, it is outside the writable field. There is no wrap to be continuous across.
     Zero → 2^24 now rests on the three-way argument alone; silicon behaviour stays UNKNOWN.
  3. **The 8253 aliasing finding was ALREADY FIXED** in `84f442d`, one commit after the `35302f2`
     the seat reviewed. Its citation landed on the retraction rather than the claim — the same
     shape as the grok "of each kind" finding earlier the same day, and the second time in one
     round that a seat cited a correction as the defect. Worth naming as a pattern: **when a
     comment quotes its own earlier wording in order to disclaim it, that quotation is a
     grep-magnet.** No action.
  The seat also disclosed its own conflict unprompted (it was one of the original one-helper
  advocates) and graded every number it had not run as `UNKNOWN` rather than asserting it — the
  honest form, and the reason its three findings were worth checking one at a time.

- **`m8sarpurge` — 98% of the CMMU register arm's write-side purges are gratuitous, and the
  biggest one is `CMMU_SAR`.** (filed 2026-08-16 from the #434 measure seat, which instrumented
  a luna88k boot per register rather than in aggregate.) Measured, per boot-to-login:

  | register | reads | writes |
  |---|---:|---:|
  | **PFSR** | **292,281** | 2 |
  | PFAR | **0** | 0 |
  | **SAR** | 0 | **612,186** |
  | SCTR | 0 | 2 |
  | SAPR | 0 | 5 |
  | UAPR | 2 | 13,026 |

  Three things fall out, and the second is the item:
  1. **The read side is 99.999% `PFSR`, and the cost really is TWICE per fault — but not for
     the reason first given, and the correction to it was ALSO wrong.** Draft 1 said "a fault
     handler reads PFSR and PFAR, so twice"; `PFAR` is read **zero** times, which refutes the
     REASON. Draft 2 therefore said "once" — an over-correction a second seat caught, because
     PFAR's absence rules out the reason, not the count. Measured: `PFSR` is read 286,519 times
     and **49.98% of those return nonzero**. The mechanism is `memory_m88k.c:382-384`, which on
     every fault sets the faulting CMMU's PFSR and **explicitly zeroes the other CMMU's**
     (`CMMU_PFSR_SUCCESS` is 0) so the handler can tell them apart — so it must read **both**,
     and exactly half of those reads see zero. Right number, wrong reason; then right reason,
     wrong number. **A correction is a claim too, and needs the same evidence as the claim it
     replaces.**
  2. **The write side is 98% `SAR` — 612,186 purges per boot — and `SAR` is never consulted by
     the translation path.** `m88k_translate_v2p` reads only `SAPR`/`UAPR` (`memory_m88k.c:135,137`),
     BATC and PATC. `SAR` is read at exactly one place, `dev_m8820x.c:110`, as the *address
     operand of a flush command* — and that command's own arm already purges at `:187`. So a
     write to `SAR` owes no purge, **by exactly the argument #434 makes for reads**.
  3. Registers that genuinely can change a translation are **`SAPR` and `UAPR` ONLY** — 13,028
     of 917,504 accesses to this arm, about **1.4%**. #434 removes 32% of the arm's purges; this
     item is worth **2.1× as much** and is the same one-line shape.

     ***`SCTR` WAS LISTED HERE AND THAT WAS WRONG***, caught by a pass-1 seat on the round that
     acted on this filing. `SCTR` appears **nowhere in `src/` outside its own case label** — the
     translation path never reads it, so a write to it cannot change a translation and it belongs
     with `SAR`/`PFSR`/`PFAR`, not with the area pointers. The error did not reach the code (the
     round split the arm on the measured consumer table, not on this sentence), but it would have
     put `SCTR` on the wrong side of the argument for anyone reading the filing afterwards.

  Not folded into #434 because it is a second behaviour change on the write side, and #434's
  claim is the one that was A/B measured. The detector rows already exist (`diff_m8invread.c`
  section E) and would need their per-register expectations re-pinned rather than rewritten.

### The dashboard rendered three different failures as one blank cell, and one of them was real

The owner spotted blank cells and asked. Three distinct causes, only findable by looking at each:

1. **A rendering bug, and the worst-placed one possible.** 59 ledger entries were keyed `opus`
   while the column is declared `opus5`, so `cell()`'s `x["seat"] == seat["id"]` matched nothing
   and **every one of them rendered nowhere** — the measure seat, the one that overturns
   conclusions by compiling and running. Its work was simply not on the dashboard, and the blanks
   read as "that seat never answered", the exact opposite of the truth. `gen_dashboard.py` now
   REFUSES to render and exits 2 when any entry names an undeclared seat, listing each offender
   and its entry count. Negative-controlled both ways.
2. **Legitimately blank, now said out loud.** `tfreq` has no assessment phase because it was
   raised *during* the n2/n4 assessment and folded into that round. Recorded as an explicit
   entry, because a blank cell and a seat failure must never look alike.
3. **THREE PANELS WHOSE SEATS ANSWERED AND WERE NEVER RECORDED.** The dangerous class. Two were
   caught by the owner's eye; the third by the check written in response.

**What the three unread panels contained, all real:**
- `panel_20260815_202720` / kimi, 192 KB → **gate 2 has ZERO coverage of `dev_rtc.c`** (no
  compile, no row, `grep -c rtc gate_offline.sh` = 0), so #429's fix can be reverted and gate 2
  stays green. Filed `rtcgate`. The vacuity class in its purest form, proven by construction.
- `panel_20260816_024410` / kimi, 99 KB, **in a round that had already shipped** →
  `diff_m8invread`'s spy counts *callback calls*, so a mutant clearing the dyntrans arrays
  directly passes all 21 rows. Filed `m8invground`.
- `panel_20260815_020427` / **six seats** on the closed `r420` → `drive_guest.py`'s `absorb()`
  docstring claimed "a newline or a `]` releases it" while `split_stream()`'s docstring thirty
  lines below says the opposite explicitly and the code agrees with the lower one. **Fixed.**
  Two seats independently found the `3.57 %` spread quoted without its population; `lib.sh:211`
  states both figures correctly (3.57 % over eight idle runs, 6.42 % over an 8× host-speed
  range) but downstream citations drop the qualifier — **including two I wrote in R8 this week**,
  now corrected. Filed `xfamscope` for two smaller crossfamily residuals.

**The fix that makes it not recur:** `pipeline/check_seats_read.py`, wired into
`precommit_check.sh` as a HARD section G. Once a ledger entry cites a panel directory, every
seat in it that produced a substantial answer (≥ 800 b, the same threshold `panel.sh` uses) must
be cited by some entry for that seat. It found the `r420` case within a minute of being written.

**The rule:** *a check a human has to remember is a check that eventually does not happen.* Both
of the first two were found by a person noticing a blank square on a web page.


- **`m8patc` — a `SAPR`/`UAPR` write does not invalidate the guest's PATC.** (filed 2026-08-16
  from the #435 pass-1 grok seat.) The area pointers are what `m88k_translate_v2p` reads to find
  the page tables (`memory_m88k.c:135,137`), so changing one re-points translation at a different
  table — but only the emulator's dyntrans mapping is purged; the guest's 56-entry PATC keeps its
  cached entries from the OLD tables. Pre-existing, and **`SAR`'s purge never covered it either**,
  so #435 removes nothing that was protecting against it. Worth a round of its own: the fix is a
  PATC invalidation on those two writes, which is a behaviour change in the *safe* direction and
  needs its own detector rows and its own argument.

### The Fable regression adjudication (R1–R9, 2026-08-16): a green battery, read honestly

REGRESS_PASS, 16/16, 0 failed, **0 skipped**, 1,043 `ok` rows — and the flagship seat verified the
arithmetic: 1,043 is exactly the sum of the sixteen per-gate counts, so there are no phantom rows.
It also confirmed the chain that lets offline rows speak for rig binaries is closed: the diffs
compile SEC repo source, gate 1 proves both build trees are byte-synced to SEC, and the rigs run
the build binaries.

Its verdict is deliberately deflationary, and it is the useful kind:

> This green licenses *"every R1–R9 detector still passes against today's source, and the normal
> boot paths of four rigs still work"*. It does **not** license *"every R1–R9 fix is still
> present"* — two shipped hunks can be reverted under a green battery — and it does **not**
> license *"the new detectors can still fail"*.

**#431 IS A SECOND `rtcgate`, AND IT WAS NOT FILED.** R5's second hunk deleted a PPC page-crossing
halt in `LS_GENERIC_N`. Gates 13 and 15 drive FP encodings only; `gate_ppc_halt.sh` and
`ppc_halt_probe.py` contain **zero** references to alignment or page-crossing (grepped and
confirmed here), and nothing else in the battery executes a PPC unaligned crossing. **Reinstating
the halt — the exact guest-reachable `cpu->running = false` that #431 exists to prevent — passes
all sixteen gates.** Filed below as `pcchalt`.

**The lesson is sharper than the finding: `rtcgate`'s own reasoning catches this only when applied
PER-HUNK, not per-round.** The audit that filed `rtcgate` stopped one commit short, and my brief
for this very adjudication reproduced the error by tabulating R1–R9 *by round* — which hid both
naked hunks behind round names that were otherwise well covered. R4's timer half is among the
best-covered code in gate 2 while its RTC half has nothing; calling "R4 weak" would smear a strong
detector and calling it strong would bury a hole. **The unit of coverage is the hunk.**

**THE BATTERY RE-PROVES THAT DETECTORS PASS; IT NEVER RE-PROVES THEY CAN FAIL.** Gate 3 is the
only failability control, and all seven of its mutants target `float_emul.c` — none of the five
harnesses R4–R9 added. Every one of those censuses ran **once, at round time, and never again**.
Presence checks and identity row counts guard deletion and stale copies; they do not guard stub
drift, which is exactly the class `m8invground` instantiates. Gate 3's name reads as
"gate 2 is falsifiable" while it demonstrates that for 7 mutants against 213 checks — **an
overclaim that grows every time gate 2 gains a check.**

**Coverage growth tracks volume, not risk.** Gate 2 went 157 → 171 → 198 → 213 across these
rounds; every one of those ~56 checks attached to the file the round had just touched. Zero went
to `dev_rtc.c`, the hole the project had already confirmed. Zero went to gate 3's roster. R8/R9
added 27 rows to a device that already had 34; `dev_rtc.c` has 0. Good coverage accumulating
where the last round made it easy.

Ranked least-defended, by hunk: **#429 (nothing) ≈ #431 (nothing) > R6** (the only code round with
no reachability witness of any kind — no rig, no probe, ASAN constructs footbridge machines but
runs no guest code) **> R8/R9** (deep rows, but spy-level observable) **> R5 flavoured text**
(the `MEM_MIPS`/`MEM_M88K`/`MEM_ALPHA` blocks compile *different text* than the diff build, so
they ride on boots that sat green over this very bug for months) **> R1–R3 > R7**, which is the
best-defended of the nine: three independent layers including nine real guest instructions through
the real address decode.

- **`pcchalt` — #431's deleted PPC page-crossing halt has NO detector; reinstating it passes all
  sixteen gates.** (filed 2026-08-16 from the Fable regression adjudication.) Same class as
  `rtcgate`, found only by asking the question per-hunk. A real detector needs a testppc unaligned
  page-crossing probe. Moderate cost; can ride the next PPC round. The ship-time record for #431
  already said "no gate, probe or record mentions it" — the sentence was written and its
  implication was not acted on, which is its own lesson about honest records being necessary but
  not sufficient.

- **`gate3scope` — the battery's only failability control covers 7 float mutants out of 213
  checks, and its name implies more.** (filed 2026-08-16.) Not vacuous today; an overclaim that
  widens with every check gate 2 gains. Two fixes, and the second is the real one: rename it to
  what it demonstrates, and add ONE in-battery self-mutant row per new diff harness — the pattern
  gate 2 already owns for absorb and autodev — so the five new detectors re-prove failability on
  every run instead of once at birth, for a few seconds of battery time.

- **`m8invground` is BROADER than filed: it covers `diff_m8820x.c` D7/D8 too**, which use the same
  `noop_invalidate` callback-counting spy (`:72-74, 158, 396-404`). One filing, two harnesses.

### A dissent recorded as agreement, and an item filed only in this file

The owner looked at the dashboard and said deepseek "didn't run or didn't get marked off that it
ran". Neither, exactly — and what it actually was is worse than either.

**deepseek ran, answered 8.3 KB, and returned HOLD. I recorded it as "BELIEVED safe."** That is a
dissent softened into agreement in the record, by me, in the round it was written. It answered in
all six of the most recent panels (2.6–8.3 KB, with real verdicts: HOLD, SHIP-WITH-FIX,
FIX-AS-PROPOSED, FIX-DIFFERENTLY), so nothing was wrong with the seat at all.

**Its objection was a genuine contradiction in my own brief.** Packet §2 said `PFSR` is
*"WRITTEN by the fault path; never read"*, while packet §3's measured table, in the same document,
reported **PFSR reads = 320,243**. Both sentences were mine. The resolution — which I knew and the
packet never said — is that `PFSR` is never read **by the translation path** but is read 320,243
times **by the guest through this handler**. Two different senses of "read", written with the same
word. **A packet-fed seat can only see what the packet says, and what the packet said contradicted
itself, so HOLD was the correct verdict on the evidence supplied.**

It graded honestly throughout, which is why the HOLD was worth reading rather than discounting:
CONFIRMED for the arithmetic (it re-added the six write counts to 627,383 itself), UNKNOWN for
consumer-table completeness — naming `memcpy`, pointer arithmetic, indexed access through
`cd.m88k.cmmu[]`, and aliasing, the same four shapes glm and minimax raised and the measure seat
later closed — and BELIEVED for the SAR ordering *while noting the packet never showed the SCR arm*
to confirm the purge is unconditional and per-CMMU. That request was also correct: it had not.

**The lesson for packet construction:** when a brief uses one word in two senses, the seats that
cannot read the repo are the ones that will catch it, and they will catch it as a HOLD rather than
as a question. That is the packet-fed class working as designed, and softening the result throws
away the only signal they can give.

**Separately, `m8patc` had been filed in this file and never added to `pipeline/ledger.json`.**
The dashboard is the guide; an item that lives only here is an item the guide cannot show. Now in
both. A sweep of every item filed by the bullet convention found no others missing.


### CORRECTION: backgrounding does NOT kill the grok seat. I diagnosed that wrong and shipped it.

Committed in `840de82` and written into `panel.sh`, `CHECKPOINT.md` and this file: *"a backgrounded
launch loses the waiter and truncates at least the grok seat"*, with 523 and 265 byte files as the
evidence and a 10,431-byte foreground run as the control.

**The files finished.** Timestamps on `panel_20260816_024410`: `grok.txt` completed at 02:53:27 at
**10,226 bytes**, `grok_retry.txt` at 02:57:00 at **12,579 bytes**, both ending in real verdicts. I
read them at ~02:4x, mid-stream, and called a partial file a truncated one. The foreground run
finished at 02:54:34 — *between the two backgrounded runs it was supposed to disprove*.

**What actually happened, and it is a different defect:** double-backgrounding (`nohup ./panel.sh &`
inside a tool call) killed **`panel.sh` itself** — the waiter — not the seats. The seats ran to
completion unattended. With the waiter dead, the seat check never printed, so nothing told me the
answers were still arriving, and I read files that were still being written.

**The `SEATS.txt` fix stands and is worth more, not less.** The real failure mode is "the waiter
died, so nothing reported the seats' state" — which is precisely what a persisted verdict plus a
`PANEL_COMPLETE` sentinel fixes. Absent that sentinel, a partial file is indistinguishable from a
finished one. What was wrong was only the *causal story* attached to it.

**The lesson: a control run does not license a causal claim when the thing it controls for is TIME.**
Foreground vs background differed by launch mode *and* by when I looked. I attributed the whole
difference to the first and never checked the second, though the file's own mtime would have said
so in one command.

- **`m8invpred` — grok's pass-1 answer on `panel_20260816_024410` PREDICTED the mutant class that
  later cost two rounds, and went unread.** It said the planned detector was *"too clean and will
  green-light state-dependent mutants that still purge on the only path a guest takes"* — which is
  exactly the value-guard family (E9/E10) and the selector family (G6–G9) that pass-2 seats found
  the hard way across #434 and #435. It also observed that the I and D CMMUs have separate PATCs
  but share one dyntrans cache. Nothing to fix; recorded because the cost of not reading it was two
  rounds of rediscovery, and because it is the sharpest available answer to "what does a reading
  seat buy that a measuring seat does not" — it buys the class, before the instance.

### Full panel on every stage (owner directive, 2026-08-16) — and it is now mechanical

**The rule:** every stage — assess, research **and** review — runs all nine seats before the round
moves on. If a seat cannot be run, **stop and ask the owner**. This SUPERSEDES the carrier's
"ONE full panel per ROUND, pass 2 = Codex + Opus".

**Why the old rule expired:** it was written around two dead seats. Grok's free tier had died after
~4 substantial invocations and Kimi was 403-quota-dead, so a second panel in a round could not be
staffed. **Both are healthy now** — all seven scriptable seats answered the last three panels — and
the only live constraint is the Ollama seats' ~20-minute 429 window, which real stages already
exceed. The caution was right for its moment and outlived its moment by about a week.

**Grandfathering, forward-only by owner decision.** 13 stages ran short under the old policy,
including three on closed rounds (`m8sarpurge` review at 2/9, `b47` and `b27` at 3/9). They are not
re-panelled; each carries an explicit annotation entry naming the policy and the missing seats, so
the dashboard does not render them as seat failures. A blank cell and a seat failure must never
look alike.

**Enforced by `pipeline/check_stage_panels.py`**, wired into `precommit_check.sh` as hard section H,
negative-controlled both ways (a planted 8/9 stage fails; restoring it passes).

**It complements section G rather than duplicating it, and the distinction is load-bearing:**

> **G verifies that a seat which ANSWERED was recorded. H verifies the seat was FIRED at all.**
> Neither catches the other's failure — a seat that never ran leaves no file for G to notice, and a
> seat that ran and went unread is fully staffed as far as H can see.

**One honest carve-out, reported rather than waved through:** a stage with exactly ONE seat is a
FILING, not a panel that came up short. Items enter the queue when a seat raises them during some
other round's panel, leaving a one-seat `assess` entry; the item has not started. The check counts
these separately and prints the count (48 today), because "filed, awaiting its panel" and "we ran a
panel and it came up short" are different states, and the entire purpose of this layer is that
different states must not render the same.

- **`selfmutant6` — six of eleven differentials still have no failability control.** (filed
  2026-08-16 with #436, deliberately named rather than fixed silently.) #436 gave five
  differentials a self-mutant and added a manifest so a twelfth cannot arrive uncovered. The
  remaining six are **`ieee_store`, `sh4_tmu`, `wdc_identify`, `diskimage_io`, `diskimage_geom`,
  `diskimage_parse`**, carried on a dated exemption list. **Deadlines are 2026-08-31, set by the owner and
  tighter than the Oct/Nov I proposed** -- asked, they judged 148 uncovered rows a fortnight's
  work rather than a Q4 item. The gate reddens on that date whether or not the work is done.

  `ieee_store` is a genuine exemption — gate 3 covers it, and it is the only differential that
  has ever had a failability control. **The other five are real debt**: each is a detector whose
  rows could all be inert with the battery green, which is the exact defect #436 measured and
  closed for the first five. They inherit the in-detector `SELFCHECK` row for free once it is
  added to them (it needs no mutant design work), so the cheap half can land in one edit; the
  self-mutants need one anchor and one named row each.

  Filed rather than folded because doing them silently in the round that built the helper would
  break the stopping rule, and leaving them unnamed after building it would repeat the
  "grep for its siblings" miss this project keeps making. A seat said both of those out loud
  before I could get them wrong.

### #436 — the detectors could all have stopped detecting, and nothing in the battery would say

**MEASURED, not argued.** Gate 3 is the battery's only failability control and it mutates one
file, `src/core/float_emul.c`. Eleven differentials live in `regress/`; gate 3 names one. Stub
`check()` so it never compares — keeping the row names the gate greps for, the row counts, the
identity rows, the failure counts and the verdict tokens — and **118 rows across five detectors
print `ok` and detect nothing, with every gate-2 assertion green.**

The reason is structural rather than an oversight in any one row, and a seat put it better than the
reproduction did: **every assertion in gate 2 greps the detector's own stdout, and all of that
stdout is downstream of the single comparison the stub removes.** They are one equivalence class,
and the stub steps over all of it at once. Only a check that VARIES THE INPUT and demands the
output track it escapes.

**Two controls, covering different failures, neither substituting for the other:**

| control | covers | scope |
|---|---|---|
| in-detector `SELFCHECK` row | the comparator dying | **every row** in its file |
| gate-2 self-mutant | a fixture that has stopped reaching the code | **one named row** |

Measured as genuinely complementary: the `SELFCHECK` is blind to a row rewritten to compare the
subject against itself; a mutant pinned to that row is not.

**THE HONEST SCOPE, which is the part most likely to rot.** A measure seat stubbed every row
*except* the ones each mutant kills, and **both gate 2 and the self-mutant stayed green** — 23 of
24 rows inert for `timer`, 25 of 27 for `m8invread`. So a self-mutant licenses *"one named row
still fires"*, never *"the detector is fine"*. Going from 0 to 1 is not false comfort; **calling 1
"the detector works" is.** The rows are named and commented as liveness sentinels for that reason.

**Three ways the control could have been vacuous, all found by seats and all closed:**
1. Asserting *"the PASS token is absent"* rather than *"the FAIL token is present"* — a build
   failure emits **neither**, so the negative form is satisfied by a control that never ran.
2. Asserting the **verdict** rather than the **named row** — vacuous on 4 of 5 harnesses: stub the
   row the mutant was chosen to certify and other rows still kill it, so the control stays green
   while the row it vouches for is dead.
3. A **non-unique anchor** — `count() != 1` is scored `SETUP`, never a detection. Gate 3's applier
   tests membership and replaces the first hit, so a future duplication would silently mutate the
   wrong site; that exact trap produced a false result on this project earlier the same day.

**The manifest is the part that makes it more than a five-instance fix.** Every `diff_*.c` must
have a self-mutant or a dated exemption, or gate 2 reddens by name. Negative-controlled: dropping
a twelfth differential in makes the gate fail and print its name. Without it, differential #12
arrives uncovered exactly as R4–R9 added five without once touching gate 3.

Also in this round: **`memory_rw`'s floor 17 → 23** (six rows silently deletable under a comment
insisting the floor is exact — a seat demonstrated it by deleting them and getting 13/13 green),
and **gate 3 renamed to its true scope** — it claimed "does gate 2 actually fail" while proving it
for one of eleven differentials, a gap that widened every time gate 2 gained a check. The general
claim now lives in the manifest, where it is **checked** rather than asserted. A name asserts; a
manifest verifies.

Gate 2: **PASS, 220 checks** (was 213). Filed rather than folded: `selfmutant6`.


### #436 pass 2 — four defeats, and the worst one was in the control I had just added

Pass 2 attacked the round's own controls and found **four ways they could be vacuous**, all measured
on private copies. Every one is a defect in work committed hours earlier, and the sharpest is a
defect in the design the same seat had helped shape on pass 1 — which is the direction worth having.

**F1 — the SELFCHECK row had no presence check, and this is the bad one.** Deleting the block from
all five detectors left gate 2 at **PASS with the same check count and zero red rows, byte-identical
to baseline**, and all five self-mutants still OK. It is unprotected *precisely because the
bookkeeping is correct*: restoring `rows` is what makes the row free, and the row floor is the only
mechanism this gate has for noticing a deleted row. This file already says *"name each row that is
the SOLE detector of something, so deleting one is a red row rather than a quieter file"* — and the
row added by #436 is the sole detector of comparator death in five files and was named nowhere.
**The doctrine was written down and then not applied to the next row added.**

**F2 — the round's two new controls interfered, re-opening a defeat the same commit claimed to
close.** The sentinel's probe rows are deliberate mismatches, so `check()` prints `FAIL` for them on
the **healthy** path — and `selfmutant.py` selected kills by `startswith("FAIL") and rowid in l`. A
rowid as ordinary as `fail` matched the sentinel's own line and returned **`SELFMUTANT_OK` for a
mutant nothing had caught.** The obvious cure was worse than the disease: suppressing the print
inside `check()` requires a name test in the comparator, which is exactly the whitelist the same
seat demonstrated defeats the sentinel. So the comparator is untouched, the probe rows carry a
`@@SELFCHECK@@` token no real row would use, and the helper filters it.

**F3 — the manifest verified the ledger, not the work.** `SM_COVERED` was a hand-written string
never cross-checked against the `selfmutant_one` calls, so **both** directions measured green:
delete a call and leave the name → GREEN; promote an exempt stem, retune the count, write no mutant
→ GREEN, *with the gate printing the paper shrink as evidence*. Same G-vs-H distinction this project
already wrote into `precommit_check.sh`: **the manifest was a G with no H.**

**F4 — the sentinel fed alphabetic strings while every real row compares numbers.** One line
(`isdigit(got[0]) || strcmp(...)`) left 118 rows inert, the sentinel blind, and four of five
self-mutants green. It now feeds both `"a"/"b"` and `"1"/"2"`.

**F5 — a mutant that died by signal was scored as a verdict.** Right colour, wrong diagnosis, and
the same class as filed `#55`. A negative return code is now `SETUP`.

**The exemption count actively obstructed its own stated goal:** shrinking the list was RED
(`got=5 want=6`) under a row named *"6, shrinking not growing"*, and the name embedded the constant
so a legitimate shrink would print *"the exemption list is 6 … 5"*. Replaced with dated deadlines.
**A count pins; a date expires.**

**THE DENOMINATOR THE FIRST RECORDS OMITTED.** #436 reported 118 rows covered without saying out of
how many. A seat measured it: the eleven differentials carry **290 rows**; the six exempt carry
**172**; excluding `ieee_store`'s 24 (which gate 3 covers, against total comparator death only and
by the vacuity-prone form this helper avoids), **148 rows across five differentials remain in exactly
the pre-#436 condition**. Demonstrated rather than inferred — stubbing `diskimage_io` and
`diskimage_parse` left **82 rows inert with the whole battery green**. So the round fixed **118 of
266 coverable rows, under half**, and the honest sentence is the one with both numbers in it.

All eight fixes are negative-controlled in both directions, and one of those controls initially
**passed for the wrong reason** — the healthy and deleted cases produced identical output because
my test tree omitted `config.h` and every build failed. Rule 4 applies to a control as much as to a
gate: *did it pass for the reason under test?*

### The agy seat ran a gate, deadlocked, and its failure was the most useful of the pass

**The seat failure first, because the cause was fixable and the fix generalises.** Given a
diff-review brief, agy decided to run `gate_offline.sh` itself, backgrounded it, and then printed
*"I am waiting for `gate_offline.sh` to complete"* eleven times until its own timeout killed it at
657 bytes. No review in it. Re-fired with one added instruction — **do not run the gates, the
measurements are inlined** — it returned 11.6 KB and said so explicitly in its conflict
disclosure.

Two harms, and the second is worse than the lost seat:
- a gate takes minutes, longer than a seat's response budget, so the seat deadlocks itself;
- **it ran concurrently with my own gate 2 in the same `$LOGDIR`**, which is the one thing this
  harness cannot survive. The `PASS (222 checks)` I had already committed was read from a log
  directory another process was writing. Re-run alone with an isolated `LOGDIR` it was identical
  — **so the claim held by luck rather than by process**, which is not a thing to leave standing.

`panel.sh` now appends an operational rule to a **derived** copy of every brief it sends (the
caller's file is never modified, and the derived copy is kept in the panel directory so what each
seat was actually sent stays recoverable). Building one detector or mutant in a private temp
directory is explicitly still encouraged; driving the harness is not.

**Then the review itself found three defects the other seats had not, all confirmed:**

**Two of the five shipped row-id pins were wrong, and it is the anchor-uniqueness trap on the
other side of the fence.** The helper matched row ids by substring:
- footbridge's `"zero"` **does not appear in row A1 at all** (`A1 load 0 becomes the full 24-bit
  span` — the digit, not the word). It matched **B2, E3 and F1**, so that mutant vouched for rows
  it was never chosen for, and A1 could have been dead with the control green.
- memory_rw's `"1 KB"` matched **four** rows (G1, G2, Z1, F3) — a family, not a row.

The fix is the same shape as the code-anchor rule that already exists: **a row id must name
exactly ONE row in the pristine run, or it is `SETUP`.** It caught `"zero"` naming three rows on
its first execution.

**The pristine arm never checked that the named row was GREEN.** It only checked the run PASSed
overall. A detector carrying a stray or permanent `FAIL` line matching the row id would satisfy
the mutant arm's pin **without the mutant causing anything** — a decoy, and the mirror image of
the sentinel-pollution defect this same round had already fixed. Now `SETUP`.

**The helper compiled `memory_rw` differently from the battery.** gate 2 builds it with
`-fno-optimize-sibling-calls`, which this gate's own comment calls load-bearing: gcc 15.2.1
eliminated the tail call and the loop-not-recursion row passed *under the very defect it exists
for*. The helper hardcoded one flag set. **The pristine control arm cannot detect that** — both
arms are consistently wrong, so the control agrees with itself, which is exactly the shape this
round exists to remove. Flags now come from the caller, which owns the real compile line.

Gate 2 re-run alone: **PASS, 222 checks**, all five pins green on the corrected row ids.


## 2026-08-19 — residuals from the R4-detector round (#429), eight seats; codex rate-limited

The round shipped a detector for a correction that had none, in **three passes**, because the
panel broke the first two. Nothing was found wrong with #429 itself — every seat that could
trace the code confirmed the range check. What they found was in the **instrument**, twice, and
in the **records**, six times. These are the items FILED rather than fixed, under the standing
stopping rule (only a measured false pass or a wrong record is fixed in-round).

Ranked. The first is a live guest-drivable defect inside a shipped correction.

1. **`rtcflood` — `dev_rtc.c:132`'s clamp diagnostic is unlatched, and a guest can drive it.**
   MEASURED by the measure seat: **1000 alternating out-of-range / in-range guest writes
   produced 1003 stderr lines.** This is the #265/#269 guest-drivable flood class and the
   `cflood` rule, recurring *inside a correction that shipped four days earlier*. The precedent
   is exact: `dev_wdc.c` already carried three `warned_*` latches added by #337 and one path was
   simply missed — filed here as `wdcflood`. The fix is the established one-line latch idiom.
   **The detector cannot see this today**: `diff_rtc_range.c` stubs `fatal()` to `vfprintf` and
   no row counts the calls, so a latch needs a counting stub and a row — which is the cheap
   part. A CODE change to a shipped correction, so it gets its own round with a reproduction,
   not a fold-in.

   *A claim about this path was REFUTED BY SOURCE and is recorded because it would have changed
   the severity.* A reading seat wrote that production `fatal()` **exits**, which would make
   #429's clamp a guest-reachable process death rather than a flood. `debugmsg.c:384` shows
   `fatal()` is byte-for-byte `debug()` — `va_start`, `va_debug`, `va_end`, no exit. So the
   detector's print-and-return stub is FAITHFUL, not a fidelity gap, and the flood is the whole
   consequence. Two minutes of looking moved this from "process death" to "noise".

2. **`rtcnarrow` — the guest-rate narrowing design item, whose three-device premise is STALE.**
   The original filing argued the narrowing belongs in the timer core, naming `dev_footbridge`,
   `dev_vr41xx` and `dev_jazz` as deriving a rate from a guest value with no wide-domain range
   check. **Two seats re-derived that independently and it does not hold:** `dev_jazz.c:432-434`
   computes `1000.0 / ((double) idata + 1.0)`, bounded above by 1000 and bounded BY CONSTRUCTION
   since `b679170` (#257, 2026-07-18); `dev_vr41xx.c:604-612` is `int hz = RTCL1_L_HZ / idata`
   with `RTCL1_L_HZ == 0x8000` (`vr_rtcreg.h:90`), an unsigned divide so `hz <= 32768`;
   footbridge's `+INF` path is already fixed. **None of the three can exceed
   `TIMER_MAX_FREQUENCY`,** so the four-device round that premise justified does not exist.

   What they DO share is **the opposite end**: all three can land *below*
   `TIMER_MIN_FREQUENCY`, which `timer_clamp_freq` floors **silently** — `timer.c:100-108` sets
   `was_clamped` only on the ceiling. That is the surviving item, and it is smaller and
   differently shaped than what was filed. Not reproduced; no witness at rung 2-4, so it stays
   a design item.

   *** THE COMMIT THAT FILED THIS ALSO MIS-CITED IT. *** `17de78a` said the residual was
   "already filed as n2/n4/tfreq". Those three rows never mention `vr41xx` or `jazz` at all, and
   are closed R4 rows about other sites. The only place the three-device sentence existed was
   `rtcdet`'s own assess note — **the row the round was about to close**, which would have
   orphaned it. The flagship seat caught that and insisted the residual be filed BEFORE the
   closure. It was.

3. **`scunbacked` — the SELFCHECK manifest's presence check is satisfied by an explanatory
   COMMENT.** MEASURED: `gate_offline.sh`'s H greps each differential's source for the bare
   token `@@SELFCHECK@@`; in `diff_rtc_range.c` that token also appears in the sentinel's own
   explanatory comment, so **deleting the entire executable sentinel leaves the H green.** The
   check's own comment claims "a block gutted down to its printf still fails this" — false for
   any file whose comment names the token. **Not a live hole**: the G (the log grep for the
   summary line) catches it, so the pair still holds. But the H is doing less than it says,
   which is the "a check whose blindness is reported as a green line" class *in the gate built
   to close that class*. The wrong COMMENT is the more urgent half. Candidate fix: grep for the
   token in a CODE context (a `chk`/`check` call), not anywhere in the file.

4. **`cmtattr` — the ledger did not know about work that had shipped.** Of the 40 most recent
   commits, **33 were named by no ledger row**. Most legitimately (receipts, records fixes,
   harness work that closes nothing); two sharply: `6014b7e`'s subject reads *"selfmutant6
   CLOSED"* against a row that read `held` with empty commits, and `gate3scope`'s `commits`
   named `2a5bc48` — the **R9/#435 m8820x device round**, which touches zero selfmutant lines
   (`git show 2a5bc48 -- regress/gate_offline.sh | grep -c selfmutant` is 0). The board renders
   from the ledger, so that drift shows finished work as open queue: the direction that matters,
   because it is invisible. Both hard rows corrected; **12 soft rows remain and want per-row
   adjudication, not a sweep.** Instrument shipped as
   `tools/pipeline/check_commit_attribution.py` + precommit **section L**.

### Two things this round did to itself, kept because they are cheaper to read than to repeat

**The escape that forced pass 3 is a class already documented in CHANGELOG.md, three blocks
below, about the SAME PAIR OF MACROS.** The `R4 follow-up` block records three seats measuring
`TIMER_MAX_CATCHUP` → 65536 and `TIMER_MAX_FREQUENCY` → 32768.0 passing every row of
`diff_timer.c`, and prescribes asserting an absolute consequence derived from outside the header.
The new detector did not apply it, and `TIMER_MAX_FREQUENCY` → `TIMER_MAX_CATCHUP` — **one
identifier, the macros two lines apart in `timer.h`** — passed 12 of 12 rows. This is the same
failure `gate_offline.sh` names about its own SELFCHECK row: *"the doctrine was written down and
then not applied to the next row added."*

**A mutant that PASSES can be the correct answer.** The panel's only DEFECTIVE verdict rested on
*"replace `TIMER_MAX_FREQUENCY` with `0x7fffffff` and the limit is gone for everything in
`(TIMER_MAX_FREQUENCY, 0x7fffffff]`"*. That interval is **empty** — `timer.h:81` defines the
constant AS `2147483647.0`. The mutant is a no-op and passing it is right. A packet-fed seat
cannot read the constant; its *second* point, the clamp target, was correct and forced pass 2.
Both halves in one 3.6 KB answer, which is the seat class stated in a single document.

Final: detector **17 rows / 0 failures**, gate 2 **PASS at 258 checks** (245 before).
`rtcgate` closed credited; `rtcdet` closed documented-only as its duplicate, so the work counts
once. Codex was RATE-LIMITED — its 26,992-byte file was the echoed brief plus the 429, **the
largest file in the panel** — recorded with a HELD marker and a queue entry.


---

## 2026-08-20 — `pitflip` (#440): the 8253's 16-bit selector was one-way, and the latch never released

Shipped as #440 (`dev_8253.c` + `regress/pit8253_latch_probe.py`). Full story in the CHANGELOG
R12 block; what belongs in the queue is below.

**Closed by this round**

* `pitflip` — the 16-bit LSB/MSB selector cleared `I8253_TIMER_LSB` in `mode_byte` and nothing
  set it back, so it stuck at MSB after one access and destroyed the programmed format with it.
  Now a per-counter flip-flop that ALTERNATES, with separate read and write halves as the i8254
  datasheet's p. 8 interleave requires. Witness: rung 3, `pit8253_latch_probe.py` arms P/Z/I.
* The sticky latch in #439, found by **Codex 5.6-SOL on the #439 pass-2 panel** (six seats said
  SOUND; glm gestured at it). `latched[]` was cleared only by a mode write, so one latch command
  made every later read of that counter return 0. Now consumed per the programmed byte format.
  Witness: arms L and M — M is the mid-pair case, where a latch lands BETWEEN the two halves of
  a 16-bit read and both fixes have to agree.

**STILL OPEN — and the first of these is why the round was ranked where it was**

* **`i8253zero` is NOT fixed.** #440 removed the only known way a guest reaches count 0 — the
  one-way selector reprogrammed the counter to 0 on its own, which arm Z measured as
  `100 Hz, 0 Hz, 101 Hz` from a guest that only ever asked for `0x2e00`. The underlying defect
  stands: `else d->hz[...] = 0` is wrong against the 8254 convention that a count of 0 means
  65536 (p. 17, quoted in the 2026-08-1x entry above), and `timer_clamp_freq()` then floors it
  to `TIMER_MIN_FREQUENCY`, i.e. a timer that never fires. **The door is closed, the hole is
  not.** Anyone reopening it should note the reachability argument has changed: after #440 a
  guest must write count 0 deliberately, and no in-tree guest does.
* **`pitclobber` — `mode_byte` is still ONE global for all three counters.** A control word for
  counter 2 changes the format counter 0's accesses are decoded under. #440 deliberately did not
  touch it (different semantic class, and the fix is a per-counter `mode_byte[3]`). Note the
  flip-flops #440 added ARE per counter, so they are already the right shape for that fix and
  will not need redoing. Not witnessed by this round's probe.
* **Does a COUNT write release the latch?** Not decided by #440, deliberately. i8254 p. 7 says
  the OL holds "until it is read by the CPU (**or until the Counter is reprogrammed**)", and
  #439 already clears `latched[]` on a control-word write. Whether a bare count write (no new
  control word) also counts as "reprogrammed" is **not resolvable from the text I have**, so the
  smallest defensible thing was done: it does not clear. Flagged rather than guessed, per the
  round's own constraint against reconstructing a rule from memory. No guest is known to do it.
* **`d->mode[]` remains behaviourally inert** — written in three places, read only inside a
  `debug()` printf. Unchanged, re-confirmed by reading during this round.
* **There is still no running count.** The file's own TODO says so. #439 and #440 both refuse to
  synthesise one, and the latched read still returns 0 rather than the reload, because a guest
  dividing by `(reload - latched)` would divide by zero — measured as candidate C1 in #439 and
  still guarded by row R3.
* **`pit8253_latch_probe.py` still ships UNWIRED** into any gate — carried forward from #439
  unchanged, and `gate_hygiene.sh`'s own comment at its `EXPECT_CONVERTED` pin says why that
  matters: nothing forces the probe to fire, so the pin is doing the whole job. Wiring it into
  `gate_arm.sh` beside `footbridge_sites_probe.py` still wants an operator who can run gate 6.
  #440 makes this MORE valuable, not less: the file now carries ten verdict rows and six
  controls, six of the rows with measured kills.

**Two records defects found while doing this, one fixed, one flagged**

* **FIXED:** `pit8253_latch_probe.py` was committed with CRLF — the only such file in the repo
  (`git ls-files --eol`). Its `#!/usr/bin/env python3` would die as `bad interpreter: ...^M`
  under a direct exec; it works today only because the documented invocation is
  `python3 <file>`. Normalised to LF, which is most of its diff.
* **FLAGGED, not invented:** #439 (`020a672`) shipped with **no CHANGELOG round block**. The
  ethos calls for one per correction, and #440's is R12 with no R-numbered block for #439. Only
  that round's operator knows what it meant to record, so this is left as a note rather than
  written for them.

## 2026-08-20 — twenty rounds' worth of residuals that went to the ledger and not here

**This block exists because the same gap was hand-fixed one round ago and recurred immediately.**
`f7eac43` is titled, in full, *"OUTSTANDING_BUGS: the R4-detector round's residuals, which went to
the ledger and not here."* One round later, twenty-one open rows were filed into `ledger.json` and
none into this file — so a fresh session following CLAUDE.md's own instruction to read this file
first would have missed a day's work entirely.

A catch-up commit is not a fix for that; it is the same fix twice. So this block ships alongside
`tools/pipeline/check_bugfile_sync.py` and precommit section **P**, which fails on an OPEN ledger
row that this file does not name. Forward-only by date, like section O — 66 older rows are
reported and not failed, because a rule that retro-fails the archive gets switched off.

**Why both files exist**, since the obvious reaction is to delete one: `ledger.json` is the
pipeline's machine-read truth (per-seat, per-phase; a round with no row is invisible to section H)
and this file is the human queue. This project has been bitten from *both* directions — `es438` was
a round with no ledger row, and fixing it produced `lunafuse`, which was filed here and given no
ledger row, reproducing the defect one layer in. Only OPEN rows are required here; the charter
above says resolved items are removed, not annotated.

Full per-seat detail for every row below is in `tools/pipeline/ledger.json` and the dashboard.

### `sh4pcicexit` — held
**Eight measured one-instruction kills remain in `dev_sh4.c` after #441.** `sh4_pcic` has ELEVEN `exit(1)` sites with ~116 word offsets reaching its `default:`, and `DEVICE_ACCESS(sh4)` itself carries five more value guards (ICR bit 7, RCR1 bit 3, DMATCR0's top 8 bits, plus two). Measured with matched surviving controls. Bigger than the round that found it and cheaper to reach -- ONE instruction, not two.

### `m8batc` — held
**A mutant that stops updating the shadow `batc[]` passes BOTH m88k differentials green, 27/27 and 25/25.** `dev_m8820x.c:479`; the shadow is read at `memory_m88k.c:152` BEFORE the PATC and before the walk, so a stale entry silently returns a wrong physical address for a 512 KB block. Of the three arms in that device touching translation inputs, two are covered and this one has ZERO executable rows.

### `hpcabort` — held
**Three of eight `hpcmips` subtypes core-dump at construction** (e105, be300, vr3 -- rc=134), from three bad `irq` arguments in `machine_hpcmips.c:84,114,242`, 1:1 with the aborting subtypes. Upstream defect, inherited. `hpcmips` appears NOWHERE under `regress/`, so the binary advertises eight subtypes and dies on three with no gate able to say so.

### `pitcount` — held
**The 8253 models no decrementing count, so OpenBSD's `delay()` never returns** -- under every design discussed for #439/#440 including the one that shipped. `clock.c:266-275` loops while `n > 0` subtracting `tick - otick`; a constant `gettick()` makes that zero forever. The five filed PIT rows are surface manifestations of this one.

### `wdcoracle` — held
**Deleting one line from `dev_wdc_tick()` leaves a controller that can never raise an interrupt, and a struct-reading opcode detector stays 100% green.** The oracle for `wdcnoirq` is the wrong variable: it must count real `INTERRUPT_ASSERT` calls through `d->irq.interrupt_assert`, not read `d->int_assert`. Two more escaping mutants recorded with it, including one that silently re-enables the interrupt `:559` deliberately suppresses.

### `smfalsegreen` — held
**The `smnotland` fix opened a false green**: with the detector ITSELF as subject, `selfmutant` returns OK while the code under test is untouched. Latent (all 12 lanes use `src/` subjects) but `selfmutant.py:221-225` advertises the capability, so the invitation is written down and the guardrail is not.

### `m88kexit` — held
`memory_m88k.c` still calls `exit(1)` on the `CMMU_PFSR_SUCCESS` internal-error branch -- the host-kill shape #433 removed from this same device family, left behind because that sweep was scoped to the device file rather than the translation path.

### `hlen` — held
**`hlen` and `devexit` intersect at 23 lines** and neither filing seat saw the other's row: `dev_pcc2.c` 11, `dev_sgi_re.c` 6, `dev_sh4.c` 2, three more at 1 each. A handler that cannot service a width whose failure mode is process termination is ONE defect on one line. #441 took the first two; the rest are siblings.

### `smsetuprow` — held
`selfmutant`'s three-way SETUP/OK/FAIL split is flattened back to two-way at the gate (`gate_offline.sh:833-838` greps `SELFMUTANT_OK == 1`), so an apparatus failure and a genuine detection failure print the SAME red row -- the shape the helper fixes internally, reproduced one layer up.

### `witnessunwired` — held
**Section K passes a row whose witness artefact no gate ever executes.** `pit8253_latch_probe.py` runs in no gate and two rows name it as their witness. Fourth recurrence of a pattern `gate_hygiene.sh` already logs three times.

### `warnnotfail` — held
Deleting a pipeline checker still yields `PRECOMMIT_PASS` -- the MISSING branches call `warn`, which increments `warn` and not `fail`. Announcing works; blocking does not. Filed rather than fixed because a missing checker in a FRESH CLONE is normal and one deleted from a working tree is a gate being switched off, and the branch cannot tell them apart.

### `ledgerboiler` — held
**The ledger recorded seats as AGREEING when it only knew they were FIRED** -- 52 rows carry one summary stamped across five seat cells. On `wdcnoirq` five cells differed only in the leading seat name, and three of those seats had argued the opposite in their own files. Check shipped (precommit O, forward-only); re-harvesting the 52 archived rows is the open part, and the seat files still exist under `_scratchpad/panel_*/`.

### `stalecopies` — held
**Three unpatched pre-#337 copies of `dev_wdc.c` live under the project root** (`./src/`, `./build-asan/src/`, `./_archive/...`), and a file-reading seat cited one as "root", producing line numbers that match no tracked file. Live for any seat given `--add-dir` at the project root. Needs an owner decision: retarget, delete, or amend the brief template.

### `rtclen` — held
**A one-token edit to `dev_rtc.c:92` (`len` -> `4`) re-creates #429's own ADD-becomes-REMOVE defect and passes all 18 detector rows.** Came out of a census that found TEN survivors, including a NULL-deref the table survives because no row writes 0 with `d.timer == NULL` -- the ordinary reset path.

### `rtcbranch` — held
`diff_rtc_range.c:239` claims a `>=` there "would fail this row and nothing else". Measured: it fails NOTHING, because the clamp target EQUALS the boundary and the row asserts the value rather than the branch.

### `rtcstale18` — held
Three records say the RTC table has 17 rows; it has 18 -- including `selfmutants/rtc_range.why:11`, INSIDE the paragraph that flags this staleness class.

### `sh4partialread` — held
#441 drops a partial READ of BCR2/BCR3 where it could be serviced exactly. Not a regression -- that access used to kill the host -- so it files rather than blocks.

### `sh4bsclane` — held
#441 cites PCR/RTCSR/RTCOR/RFCR as precedent for servicing, then differs from them on BOTH byte-lane resolution and partial-width promotion. No SH-4 document exists in this tree to settle which convention is right, so the divergence is recorded rather than guessed.

### `sh4markspell` — held
Gate 6's fresh-mark census keys on the exact local name `_mark`, so a correct guard spelled `mark` is PRESENT and uncounted -- two counts green, the third red, a signature that reads like a defect and is not one.

### `pitlatch2` — held
**Does a Counter Latch Command rewind the read flip-flop?** Codex says consuming the latch after one post-latch read contradicts p.8's "two bytes must be read"; the measuring seat reached the same fact and the opposite reading. BOTH agree the local `i8254.txt` does not settle it and there is no second source in the tree. An honest UNKNOWN, not decided by vote.

## 2026-08-21 — #442's residuals, and the first row section P ever caught

*Four rows named in #442's commit message and filed nowhere a tool could see them — the
`lunafuse` shape, one round after section P was written to stop exactly that. `check_bugfile_sync.py`
flagged all four the moment they entered the ledger, which is the check earning its keep on its
first real use rather than on a negative control.*

### `fbdisabled` — held
**A DISABLED footbridge timer keeps accruing ticks forever.** `dev_footbridge.c` never calls
`timer_remove()` and never lowers the frequency on disable — `:583` zeroes the counter once and
leaves the `struct timer` running at full rate. MEASURED: arm / disable / free-run 4 s / re-enable
/ drain gives backlog **3051, identical to the enabled arm**.

This is a second independent rung-3 reproduction, not a variant. It is also the measurement that
turned #442's unanimous Q1 answer from a preference into a proof — a consumer-side bound is
bypassed entirely, delivering **zero** ticks after a 46 s disabled interval. And **a guest that
disables then re-enables gets an interrupt storm proportional to the gap — **100 pending after 46 s even with #442 shipped**.

*CORRECTED 2026-08-21. This first read "2772 pending", which is arithmetically impossible: the bound is 762 and the counter cannot exceed it. The 2772 was a PRE-FIX projection carried into a post-fix sentence without re-measuring; the real figure is 100, measured on the shipped build. The clause that followed it — "because #442 bounds the rate and not a legitimately accrued debt" — was backwards too: `pending_timer_interrupts` **is** the accrued debt and #442 bounds exactly that. What survives is the defect itself, which #442 does not close: a disabled timer still accrues at full rate, so the storm on re-enable is real — just bounded.*

### `fbclearread` — held
`case TIMER_1_CLEAR:` never tests `writeflag`, so **a guest READ of the clear register acknowledges
an interrupt**. A fidelity defect, and a hazard for probes: this project deliberately uses guest
loads rather than debugger `dump` because `dump` does not route through device handlers — so a
probe reading this register would silently drain the backlog it was measuring.

### `fbvolatile` — held
Two footbridge counters cross the SIGALRM boundary as plain `int` (#442 added the second) while
`dev_mc146818.c:80` declares the identically-used counter `volatile int`. **The tree already holds
both conventions for one hazard.** Nothing hoists today at -O3 because `random()` is a compiler
barrier — which is luck, not design, since the fix does not control that call.

### `fbsmlane` — held
The `fbpending_bound` self-mutant lane does not run; shipped as a dated `SM_EXEMPT` (2026-09-20)
rather than left red, because a registered-but-broken lane reports SETUP forever and trains the
reader to ignore it. **Not untested:** the harness carries its own `@@SELFCHECK@@` control, and all
four mutants were built and run by hand, each killed by a named row. It is the only differential
that *links* against ~221 build objects rather than compiling standalone, and `selfmutant.py`
builds in a mirrored tree — so it is a wiring job with a known shape.

## 2026-08-21 — #443's residuals: what the round did NOT do, and one line it cannot prove

### `sh4valguards` — held
**Four guest-reachable value-guard `exit(1)`s remain in `DEVICE_ACCESS(sh4)` itself** — the switch
`#443` did not touch. Measured with matched surviving controls, and **re-derived, because every
line number in circulation was wrong**: `#441` had shifted the file and the numbers had been
copied rather than opened.

```
:1692  ICR bit 7 set                    kills -- "IRLM not yet supported"
:1963  RCR1 mask 0x18                   kills -- bits 3 AND 4, not bit 3
:1453  DMATCR0 top 8 bits set           kills
:1369  TCR write with ICPF|ICPE1|...    kills
```

**Two claims removed rather than carried forward:** `:1343` is `pclock == 0`, an *internal* error
rather than a guest value guard, unreachable on landisk which sets pclock at
`machine_landisk.c:81`. And `DEVICE_ACCESS(sh4)`'s own `default:` **does not kill at all** — its
`exit(1)` is inside `#ifdef SH4_DEBUG`, and `grep -rn SH4_DEBUG src/` returns only the two
`#ifdef`s, so it is defined nowhere. A read of `0xff000004` returns 0 and survives. `#443`'s
witness keeps that as a control row so the claim cannot drift back in. **The sibling cluster is
four, not six.**

### `bscunwired` — held
**`#441`'s `sh4_bsc_width_probe.py` still runs in no gate**, two rounds after shipping — the fifth
recorded instance of the `witnessunwired` class. `#443` wired *its* probe into gate 10 in the same
commit; `#441`'s is referenced by nothing but the probe census. The cost is concrete: a regression
in BCR2/BCR3 width handling would be caught by no gate. `#443`'s wiring is a two-block template
that applies almost verbatim.

### `sh4pcicvoid` — held (records-only)
**One line of `#443`'s fix is genuinely void and the detector says so rather than claiming
coverage**: `odata = 0` in the unimplemented-CPU PCICONF0 arm cannot be distinguished from its
absence, because that slot cannot be made non-zero while the restores hold. Recorded so a later
reader does not count row P10 as covering it, and so a future change to the restore logic does not
silently make the line matter again with nothing watching. Likewise `& 31` in the latch is
UB-avoidance rather than behaviour on x86-64 — a mutant dropping it would be an equivalent mutant,
and the measuring seat correctly declined to build one and said why.

### `pcicmergeA` — held
Of the two measured reproductions of `#443`'s latch-merge defect, only one became a detector row.
**The other could not have, and the reason is the interesting part: writing it against the
two-class code would have *cemented* the defect** — the row would have asserted the merged
behaviour as correct. The seat said so rather than writing a row that passed. The third fault class
now exists, so the row is three lines; filed rather than written because it needs a probe run made
*after* that class landed, and writing an untested row is the same mistake in the other direction.

### `ctorabortclass` — held
**The same construction abort fires on EIGHT subtypes across FOUR machines**, not three across one
— measured by sweeping every advertised type/subtype rather than suspected. Besides `hpcmips`'s
three: `decstation/5400` (`irq="irq? TODO"`), `decstation/5500` (`"TODO: irq"`),
`mvmeppc/mvme2100` (`"0"`), `sgi/ip19`, `sgi/ip27`. Inside `hpcmips` there are no latent copies —
the file has exactly three `device_add` calls and all three are in the aborting arms.

One genuinely *latent* instance is worth distinguishing from the eight: `machine_alpha.c:71`
(`z8530`, `irq=0`) sits in `case ST_DEC_3000_300:`, which `-H` never advertises, and all three
alpha subtypes construct. Latent is not reachable, and the row says so.

Separate round from `hpcabort` under the reopening rule — different machines, different files, and
the correct interrupt path differs per machine — but `hpcabort`'s witness enumerates subtypes from
the binary's own `-H` rather than a hardcoded list, so pointing it at these costs almost nothing.

### `asansweepblind` — held
**Two independent defects in gate 9**, both measured while establishing that it does not cover
`hpcabort`.

**It cannot see an abort at all.** `sanhit()` greps only for ASan/UBSan/SEGV text, so `Aborting.`
scores zero hits. The only construction assertion is a *floor* (`check_min "machine types
constructed" 20`), which a few aborting types cannot breach. And it tries only each type's **first**
subtype. Eight subtypes across four machines currently abort and gate 9 is green.

**Its awk silently re-attributes SGI's twelve subtypes to `rpi`.** `gate_asan_sweep.sh:50-55`
requires the primary alias to match `[a-z0-9_.-]+`, and SGI's is `"silicon graphics"` — with a
space. Verified in the gate's own output: rows read `S rpi ip12` through `S rpi ip35`, and the count
for type `sgi` is **zero**. A reader checking "is SGI covered" sees a type with no rows; a reader
checking `rpi` sees twelve rows that are not `rpi`'s. Both readings are wrong and neither is red.

## 2026-08-21 — the flagship's batched regress pass

*Fable fired on the queued backlog. Two entries DISCHARGED (`m8online`, `fbpending`), four HELD,
and three new rows — one of which is a live gate defect it found in a checker I wrote.*

### `queuesubstr` — held (fixed in the same pass; the row is the record)
**`check_fable_queue.py` matched ids by SUBSTRING, so the gate was green over exactly the state it
exists to redden.** It printed `ok sh4pcicexit regress owed and queued` while the only occurrence of
that id in `fable_queue.md` was a **parenthetical cross-reference inside a different entry**. A
*mention* satisfied "named in the queue" — for the round with the worst detector prior in this
project's history (seven of seven mutants escaped, one reinstating a host kill verbatim).

**The fix idiom already existed three files away and had already been paid for**: `gate_offline`'s
SM/SC manifests match stems exactly in a loop, after being bitten by "a stem that is merely a prefix
of another". Same genus, one directory up, never carried across.

Tightening it revealed a second thing worth keeping: matching **headings alone** turned 0 unqueued
holds into **35**, because most held stages are legitimately carried by the machine-generated wall
block rather than prose entries. *A check that reddens on correct state is as useless as one that
greens on wrong state.* The shipped matcher accepts entry headings and the generated block, nothing
else. Negative-controlled both ways.

### `probewiring` — held
**Nothing makes "no gate runs this probe" a red row or a dated debt.** Measured against `run.sh`'s
manifest: `#441`'s 13 rows and `#439`/`#440`'s 11 rows execute in **no gate**; `#442`'s rung-3 probe
is report-only by default. **Twenty-four committed detector rows currently defend nothing between
batteries.** Gate 6's structural note covers a probe's *census pin* — that the count moved — and says
nothing about whether anything runs it.

The proven pattern is three files away: a probe→gate **wiring manifest with dated exemptions**,
exactly like `SM_EXEMPT`/`SC_EXEMPT`. That turns the silent unwired state into the same honest,
expiring debt `fbpending_bound:2026-09-20` already is. Distinct from `witnessunwired` (which is about
a *witness* artefact a ledger row names); both are real and the manifest closes both.

### `smcovered12` — held (records-only)
A closure note says `SM_COVERED` lists thirteen stems. Measured at two commits: **it lists twelve.**
All twelve are backed by real `selfmutant_one` calls, and 12 covered + 2 dated-exempt = the 14
differentials on disk — so the manifest is internally consistent and the closure's *direction* was
right. Its **number** is wrong by one: a count nobody re-derived.

## 2026-08-21 — fixing gate 9 surfaced a real memory-safety defect it had been hiding

### `sgiarcbiosoob` — held
**A heap-buffer-overflow in `arcbios.c:2391` `set_env()` ← `machine_setup_sgi()`, on four SGI
subtypes no harness had ever executed.** `sgi/ip12`, `ip28`, `ip30`, `ip35`, four ASan hits each.

They were invisible for a mechanical reason unrelated to the defect: gate 9's awk required a
machine's primary alias to match `[a-z0-9_.-]+`, and **SGI's is `"silicon graphics"` — with a
space** — so SGI was dropped as a type and its subtypes silently re-attributed to `rpi`.

Second time this session that fixing an instrument surfaced a real bug its blindness was
concealing. Not diagnosed here — the round that found it was a harness round and stayed in its
file. Reachability (construction-only vs guest-reachable) is unmeasured and decides the rung.

### `asanstale` — held
**Both ASan binaries were built 2026-07-29**, many rounds behind HEAD. Every "HEAD" row gate 9
prints is *HEAD-as-of-that-build*. It now **prints** the dates — which is how this was noticed —
but nothing **asserts** freshness, so a year-old pair would read identically. Concretely: this
session shipped `#440`–`#444` touching four devices and gate 9 graded **none** of that code. Its
green means "the July binary is clean" — a true statement about the wrong artefact. Same class as
the dead-man switch already built for the nightly battery.

### `stdbufasan` — held (records-only)
Two traps, each defeating a technique this project relies on. **`stdbuf`'s `LD_PRELOAD` preempts
the ASan runtime**, so the obvious fix for `abort()`-not-flushing breaks the binary instead; it
needs `verify_asan_link_order=0`, and that had to be proven *behaviourally* because **this ASan
silently ignores bogus options** — so the pass-a-nonsense-value discriminator that CLAUDE.md
prescribes for proving a flag is real **fails here**. And the shell's `Aborted (core dumped)` line
is emitted at the *call site*, so `( … ) 2>/dev/null` does not suppress it.

### `m8saprspy` — held
The SAPR/UAPR arm has the **same callback-pointer blindness** J6 just closed for the BWP arm:
`c->` → `cpu->` on the purge callback changes the *pointer*, not the argument, and with one spy on
both cpus it is invisible. The two-spy fixture now exists, so this is **one row**. Grade it as J6
was — a shape pin, not a live defect, since `cpu_m88k.c:121-122` gives every m88k cpu the same
function — but note that is **not architectural**: `cpu_mips.c` and `cpu_ppc.c` install *different*
callbacks per cpu width.

### `m8lanecomment` — held (records-only)
`gate_offline`'s m8820x lane is titled *"compiles against the real `dev_m8820x.c`"*. It now also
compiles the real `memory_m88k.c` — deliberately, since that is what makes the oracle ask the real
translator rather than a re-implementation — and **ten of the census's kills land in the translator
rather than the device**. A reader trusting the title would attribute translator coverage to the
device file. One line.

### `killedreports0` — held
**A battery killed mid-run reported exit code 0.** It was started as `bash run.sh 2>&1 | tail -45`;
a pipeline's status is the *last* command's, so the code belonged to `tail`, which succeeded in
reading a truncated stream. Two failures compounded: the verdict was **false**, and `| tail` buffers
until the pipeline ends, so the output file sat at **0 bytes** for the whole run and was still empty
afterwards — no mid-run progress, no post-mortem.

Same genus as `cmd | head` reporting head's status, which this project already records and which bit
twice more the same day. What is new is the **scale**: not a check inside a gate, but the invocation
of the entire 16-gate battery. Fixed in practice by `exec > log 2>&1`; the re-run gave `REGRESS_PASS`
across all 16 gates in 48 minutes.

**What would make it mechanical:** a verdict is believable only if its log ends in a terminal token.
`nightly_check.sh` already treats a missing or stale verdict as failure — the same reasoning one
level in would refuse a verdict whose log carries no `REGRESS_PASS`/`REGRESS_FAIL` line, which is
exactly what a killed run leaves behind.

## 2026-08-21 — the #446 pass 2: a vacuous detector, and a class hiding inside a count

### `arcbiosubsan` — held

**Filed as two sites; it is ten.** The #446 round reported "TWO left-shift UB defects at
`arcbios.c:737/784`", found because gate 9's `sanhit()` is a `grep -acE` and counts LINES
rather than errors. Both halves of that filing were wrong.

The measuring seat found ip32 never reaches `:737`/`:784` at all — its two lines are `:570`
and `:590` — which made it four sites. A grep for the idiom then found **ten unguarded
`(buf[3]<<24)` sites and four correctly cast `((uint32_t)buf[3]<<24)`**.

*** Line 580 sits BETWEEN 570 and 590 and is the only one of the three that is cast. ***
The author knew the idiom and applied it to 4 of 14 sites. `buf[]` is `unsigned char`,
integer-promoted to `int`; `buf[3] << 24` with `buf[3] >= 0x80` is not representable in
`int` — C99 6.5.7p4, real UB, not a sanitizer artefact.

**`:737` is the damaging one, and it is not merely UB-on-paper.** The sign-extended low
word is *added* to `((uint64_t)buf[4]<<32)` and higher terms, so the assembled 64-bit
pointer's high word comes out **off by one for every address with bit 31 set** — i.e. for
every KSEG0/KSEG1 address. `:784` is UB but value-benign: the following `tmp &= 0xfffff`
discards the sign extension.

Fix is one cast per site. Not started: a round should confirm each site's dest type before
editing, because four of the fourteen are already correct and must not be "fixed" twice.

### `nulheredoc` — held

**A shell heredoc wrote three literal NUL bytes into two tracked text files**, and they
survived precommit, a 265-check gate run and the commit, because bash does not care about a
NUL inside a comment. Self-inflicted in `bcdbfb8`: comments quoting the mutant
`eaddr_string[0] = '\0'` went in through a heredoc that interpreted the escape.
`CHANGELOG.md` lines 4254/4260 and `regress/gate_offline.sh` line 1803.

**What it breaks is this harness's core idiom.** `grep` auto-detects such a file as binary
and answers `Binary file ... matches` — on stdout, **with exit 0**. So `grep -q` still works
and `grep -c` still counts, while every check that parses a FIELD out of the matched line
silently receives that sentence instead of the row. Measured: `grep 'sgi_eaddr: the buffer'
gate_offline.sh` returned the sentence, exit 0. Not a wrong value — a wrong *shape*.

*** The first sweep run to scope it was itself void, and its result was reported. *** It
found ZERO NULs, including the one already located by hand, because the nested `bash -c` ate
its `$'\x00'`. A sweep that finds nothing and a sweep that *cannot* find anything are
indistinguishable in the output. The real sweep found three bytes across two files.

Fixed in the working tree; guard shipped as precommit section **S**, negative-controlled both
ways. Its own first draft used `grep -qU "$(printf '\000')"` and put a fresh NUL into
`precommit_check.sh` — the check forbidding the byte introduced the byte. `tr -d` takes the
escape as a two-character argument interpreted at runtime, so nothing in the file is ever a
zero byte. **`git ls-files --eol` cannot be the oracle**: it reports `i/-text` for a PNG and
for a corrupted text file identically, so deriving the domain from git would exempt exactly
the broken files.

## 2026-08-21 — reviewing #447's fix found six MORE guest-reachable host deaths in the same file

### `sh4chcr` — held

*** Essentially any guest CHCR write with TD=1 ends the host process. *** Five `exit(1)` sites,
and this is **easier to hit than anything `#447` repaired** — those each needed the guest to
write a specific unimplemented bit; this needs only that the guest enable a DMA channel.

MEASURED, rung 3, unmodified `-E landisk`, shipped-fix binary, one ordinary guest store each,
`started=True alive=False` with the matching diagnostic:

| store | site | result |
|---|---|---|
| `CHCR0 = 0x0000c001` (DM=3) | `dev_sh4.c:445` | host dies |
| `CHCR0 = 0x00003001` (SM=3) | `dev_sh4.c:454` | host dies |
| `CHCR0 = 0x00000051` / `0x00000071` (TS=5/7) | `dev_sh4.c:436` | host dies |
| `CHCR3 = 0x0000c001` | `dev_sh4.c:445` | host dies — all eight channels |
| `CHCR0 = 0x00005141` — **a sane config** (TS=4byte, DM/SM=increment, TD=1) | `dev_sh4.c:491` | host dies |
| `CHCR0 = 0x00000005` (IE\|TD) | `dev_sh4.c:491` | host dies |
| `CHCR0 = 0x0000c000` (TD clear) | — | **survives — control** |

**The mechanism is why it is broad:** only `RS == 0x200` survives the `CHCR_RS` switch, and
`CHCR_IE` then kills at `:493`. The control is what makes this a measurement rather than a claim
— clearing TD alone leaves the host alive through the identical store.

Scope, stated so this does not read as a defect in `#447`'s record: that round's in-file wording
is *"four value guards in `DEVICE_ACCESS(sh4)`"*, which is literally true. This is a **residual
filed before any record claims the FILE is repaired.**

### `sh4rtcsr` — held

*** The store returns normally and the process dies milliseconds later, from a host timer. ***
`RTCSR` (`0xff80001c`) is guest-writable (`d->bsc_rtcsr = idata & 0x00ff`), and
`sh4_timer_tick()` reaches `exit(1)` at `dev_sh4.c:253-259` — at 110 Hz.

MEASURED with a `dt`/`bf` spin loop under `continue`, every halfword checked against the
emulator's own disassembler:

```
RTCSR CMIE 0x40  -> alive=False   "sh4: RTCSR_CMIE | RTCSR_OVIE: TODO"
RTCSR OVIE 0x02  -> alive=False   same
CONTROL   0x00   -> alive=True
CONTROL CMF 0x80 -> alive=True    (different bit, SAME register and width)
```

**The second control is the one that matters:** a different bit of the same register at the same
width leaves the host alive, so the kill is attributable to the *bit*, not to the access.

**Why this is a distinct round rather than a `sh4chcr` sibling:** every SH-4 probe this project
has written observes the *store site* — issue the store, see whether the host survived the
instruction. **That design cannot see this.** The instruction completes, the prompt returns, and
the host dies from a callback afterwards. Detecting it needs a free-running spin with a liveness
check *after* the fact — a different probe shape and a different oracle.

Also unmeasured, same family, filed here rather than lost: two more sites in `sh4_sci_cmd()` at
`:518` and `:527`, reached on guest-written SCI bytes. **[2026-08-22: those are `sh4sci`, below.
Measured, and there are THREE reachable bytes rather than the two this note assumed.]**

### `sh4sci` — held

*** The first SH-4 host death in this tree that a single guest store cannot reach. *** The two
`exit(1)` calls in `sh4_sci_cmd()` are reached only by CLOCKING a byte in through
`SHREG_SCSPTR` (`0xffe0001c`) — seventeen ordinary `mov.b` stores, one priming store and two per
bit, with only the **eighth rising edge** calling the function. Every SH-4 probe written before
this one observes a store site, so all of them were blind to it by construction, exactly as
`sh4rtcsr` was blind for the opposite reason (it dies *after* the store, from a timer).

MEASURED on an unmodified `-E landisk`, rung 3 — and there are **three** killing bytes, not the
two the `sh4rtcsr` note assumed:

```
0x00  start bit clear                  -> alive=False  "SCI cmd bit 7 not set"
0x80  transfer field 0x00 ("neither")  -> alive=False  "Neither data nor address transfer"
0xb0  transfer field 0x30 ("BOTH")     -> alive=False  same message, and it is WRONG for 0xb0
0xa0  bit 7 set, address transfer      -> alive=True   (same address, width, 17 stores)
```

The third was found by a pass-1 seat after the witness had already been written for two:
`(cmd & 0x30)` reaches the else arm for BOTH `0x00` and `0x30`, so the site has two faults and
one had never been driven. The shipped diagnostic called `0x30` "neither transfer bit" when it
is in fact both.

**Fixed and gate-green** (see the R20 round block): the diagnostic is kept and now names the
byte, the command is DECLINED with an unconditional `return`, and the latch is keyed on the
discriminating field — three lines for the device lifetime where the byte itself would have
allowed 192. The round also fires the standing `sh4latchcollide` disposition, converting the
`SH4_VAL_*` defines to a C99 enum, because `SH4_VAL_SCICMD` is the tenth class.

**Held open, not closed:** both stages carry a deliberate `fable5` omission per the owner's
standing batching directive, and section H refuses a CLOSED row with a HELD stage. The two
questions queued for that seat are in `tools/pipeline/fable_queue.md`.

#### Residual, MEASURED and deliberately FILED: one escape a runtime row cannot see

`1u << (cmd & 0x30)` — the site-2 key with its `>> 4` normalisation dropped — shifts by 48 for
byte `0xb0`. That is undefined behaviour, and it **survives the detector at 14/14**: on x86 the
count is masked to five bits and lands on bit 16, which collides with nothing, so the observable
behaviour is identical to the correct code. No runtime row can distinguish it.

UBSan *could*, but `gate_asan_sweep.sh` constructs machines and never drives guest instructions,
so nothing in this harness reaches this site under instrumentation. **That is the real gap, and
it is wider than this one shift:** every UB site that needs a guest instruction to reach it is
outside the sweep's view. Filed with that reason rather than papered over with a source-text
check — this project replaced `sgi_eaddr_probe.py`'s source-text census for being exactly that
kind of substitute.

### `sh4tlbda2` — held

*** A DEVICE ANSWERED FOR EIGHT MEGABYTES IT COULD NOT SERVICE, AND ENDED THE HOST THERE. ***
`dev_sh4.c`. Both TLB data-array devices register `0x01000000` -- SIXTEEN megabytes -- and
each handler opened with `if (relative_addr & 0x800000) { fatal(...); exit(1); }`. That bit
is EIGHT megabytes: the upper half of the range the device itself claimed. The guard sat
above the `writeflag` test, so a load and a store both died.

MEASURED on an unmodified `-E landisk`, one guest access each:

```
mov.l @r1,r2   r1 = 0xf3800000  -> alive=False  "sh4_itlb_da1: TODO: da2 area"
mov.l @r1,r2   r1 = 0xf7800000  -> alive=False  "sh4_utlb_da1: TODO: da2 area"
mov.l r0,@r1   r1 = 0xf3800000  -> alive=False  same (direction does not matter)
same store+load at 0xf3000000   -> alive=True,  readback EXACTLY 0x1ffffdfa
same store+load at 0xf7000000   -> alive=True,  readback EXACTLY 0x1ffffdff
```

**The discriminator is a single address bit** -- sharper than any earlier SH-4 round here.
The controls are the SAME device at the SAME width, and they assert EQUALITY with the value
each device's own mask folds `0xffffffff` to. Those two values DIFFER, so neither control
can be satisfied by the other device.

**FIXED and gate-green** (R21 round block): diagnostic kept and latched, `exit(1)` dropped,
the access consumed with a defined result -- reads produce 0, stores discarded, and
explicitly NOT serviced as array 1, because `e` comes from the same masked bits and
aliasing would let a guest probing array 2 corrupt real translation entries.

Held open, not closed: both stages carry a deliberate `fable5` omission per the owner's
standing batching directive, and section H refuses a CLOSED row with a HELD stage.

#### Assessed and NOT changed, with the measurement

* **`e` is bounded across the whole window.** `SH4_ITLB_E_MASK = 0x300 >> 8` gives 0..3
  against a 4-entry array; `0x3f00 >> 8` gives 0..63 against 64. Neither mask contains bit
  23, so the bound holds for all 16 MB and not merely the serviced half. No second defect.
* **The `aa` windows (`0xf2000000`, `0xf6000000`) do NOT share the defect.** Also 16 MB,
  but their handlers carry no guard and no `exit(1)`. Their upper halves alias the lower
  ones silently. That is a different and much milder question -- an aliasing read, not a
  host death -- so it is NOT filed as a defect: nothing measured says the aliasing is
  wrong, and with no usable SH-4 manual in this tree nothing here can say what bit 23 of
  an `aa` window is supposed to mean.

  **`sh4aaalias` WAS FILED HERE AND IS WITHDRAWN — the manual says both handlers are
  right.** The reasoning was that `da1` treats bit 23 as selecting a second array while
  `aa` ignores it, so one must be wrong. A real SH7750 Hardware Manual was obtained the
  same day (`_scratchpad/sh7750_hardware.txt`, Rev.7.00 REJ09B0366-0700) and its P4 map
  settles it: `H'F200 0000`–`H'F2FF FFFF` is the instruction TLB **address** array as ONE
  undivided 16 MB region, while `H'F300 0000`–`H'F3FF FFFF` holds data arrays **1 AND 2**,
  split at `H'F380 0000`. The address windows are not split; the data windows are. The
  emulator matches the hardware at both.

  **Kept as a record rather than deleted, because the shape of the mistake is worth
  having:** an asymmetry between two handlers is evidence of a question, not of a defect,
  and this one was one download away from being answered.

### Rows adjudicated by the 2026-08-22 flagship batch, still open

These are live queue items, each with a verdict from that batch recorded in
`tools/pipeline/ledger.json`. They are listed here because the bug file is half of the
live queue by charter, and a row that exists only in the ledger is invisible from here --
which is the exact failure this list exists to prevent.

| row | state | the batch's ruling, in one line |
|---|---|---|
| `gcsections` | held | Real and small -- a linker-behaviour dependence that would present as a PHANTOM RED, the 'green row means nothing' class inverted. Ride the next m8820x round. |
| `isaorder` | held | READ-only, reproduction first; init-order defects are witnessable at rung 2/3. |
| `landiskdisk` | in work | **RANK IT UP** -- an instrument gap that BLOCKS four other rows' witnesses (idesync, wdcflood, wdcnoirq, wdcstandby). Attaching a scratch disk to the landisk rig is cheap and must precede any wdc round. |
| `ledgerwitness` | in work | CLOSE WITH NOTE -- nothing MECHANICALLY requires the witness field on a row closing with commits after the cutover. An optional field on an auditability rule re-creates the gap the row exists to close: wire a one-line post-cutover check, or record the decision not to. |
| `m8latch` | held | Filed-not-widened-mid-round was right; the fix shape already exists in-tree as #447's (class, instance, bit) three-part latch key. |
| `m8sarseq` | held | Legitimate coverage debt on a closed round; the two composed-sequence rows ride the next m88k round. |
| `pitlatch` | in work | The 8253 treats the standard LATCH command as an error, and a real guest issues it in microtime() |
| `strad` | held | Filing the three mutant shapes NAMED, not implied, is the doctrine's FILE arm done properly. |
| `wdcstandby` | in work | Real (every powerdown issues it), small (accept + status + IRQ). Same wdc round, same witness vehicle. |

### `detectorescapes` — open, MEASURED, ranked

*** SEVEN ESCAPES, BUILT AND MEASURED AGAINST FOUR SHIPPED DETECTORS ON 2026-08-22. ***

**A wording precision first, because it changes what the reader should be alarmed about.**
These are escapes from the DETECTORS. The emulator itself never shipped with any of these
defects -- each is a mutant built to test whether a detector would notice. "A safety breach
in shipped material", said elsewhere about `C-M3`, means *the shipped detector had a
safety-relevant escape*, not that the emulator shipped with a host death. A seat flagged the
looser phrasing as risking exactly that misreading.
Found by the measuring seat when it was fired on four review stages that had run 8-of-9
without it. Fourteen mutants built, thirteen measured: seven escapes, four deaths, one
provably equivalent, one that would not compile.

**One was fixed in-round and is not in this list**: `C-M3` moved a `return;` inside the
latch guard at `sh4_chcr`'s RS arm — two characters, 18/18, and it RE-REACHED the `exit(1)`
that `#448` removed, on the second store of the same word. That is vacuity-floor clause (b),
so L2 licensed the in-round fix (row `L0`, measured: clean 19/19, mutant 18/19). One wrong
record was corrected the same way (`dev_sh4.c:159`, L4).

**The rest are coverage debt, in the seat's own ranking:**

| # | escape | detector score | what it admits |
|---|---|---|---|
| 1 | `S-M3` delete `net_generate_unique_mac` (`machine_sgi.c:97`) | 10/10 | The guest is handed an **uninitialised-stack MAC**. Green because the string and the bytes agree *with each other* — the check is RELATIVE and nothing pins arg5. Needs an ABSOLUTE row. |
| 2 | `A-M2` `uint64_t` → `uint32_t` at `arcbios.c:707` | 2/2, **zero warnings** | A 64-bit ARC peer pointer stored with its high word zeroed — the round's own headline class, worsened. |
| 3 | `C-M1` `SH4_VAL_DMACSM` → `SH4_VAL_DMACDM` (`dev_sh4.c:634`) | 18/18 | One identifier, a copy-paste between adjacent identical blocks. Both arms' only unmodelled encoding is 3, so both keys collide exactly. **TS and SM have no latch row at all.** |
| 4 | `R-M4` whole-register latch key | 10/10 | The repeat-flood the latch exists to prevent, breaking the "reported once" contract the diagnostic asserts. |
| 5 | `R-M3` joint growth into `RTCSR_OVF` | 10/10 | An unpinned accept-side bit, and the *more* realistic growth: OVF/OVIE is an adjacent flag/enable pair. Severity low — the guard only prints. |

**The class statement is worth more than any instance.** `arcbiosubsan`'s census pins
**text**; its unstated gap is **text-preserving semantic change** — the declaration types of
`buf` and of the destinations — which is neither "a rewrite that changes the statement" nor
"a statement not in the table". A lexical assertion pinning the `uint64_t` declaration WOULD
catch this exact mutation, so "no regex can close it" would be too absolute -- a seat said
so. What no regex closes is the CLASS, because the next text-preserving semantic change need
not touch a declaration at all. It needs a type assertion or a
behavioural row on a 64-bit ARC path. The flagship batch had just ruled the frozen-table
form correct for idiom classes *within stated conditions*; this names a condition it did
not state.

#### The hole GENERALISES, and a keyword scan says where to look first

`C-M3` was invisible for a structural reason, not an oversight: **every `R` row stores
once, so they only ever take the FRESH path.** The fall-through happens on the LATCHED
path, which by definition prints nothing — so an "exactly one diagnostic" oracle cannot see
it. `L1`/`L2`/`L3` store twice but with *different* words, testing which KEY the latch uses,
never what happens after it suppresses. **Any latched-diagnostic detector in this tree can
have the same hole**, and the discriminator is cheap: does it drive the SAME offending value
twice in one process and assert the host is still alive afterwards?

A keyword scan across the five SH-4 detectors — a scan, NOT a proof, and recorded as such:

| detector | same-word repeat rows | note |
|---|---|---|
| `sh4_sci_probe.py` (#451) | RPT, RPT1 | covered, and both assert `alive` |
| `sh4_tlbda2_probe.py` (#452) | RPT, RPTu | covered, both assert `alive` |
| `sh4_rtcsr_probe.py` (#449) | L1, F1 | covered — F1 is a many-tick flood on one condition |
| `sh4_val_probe.py` (#447) | **none found** | **check it** |
| `sh4_pcic_probe.py` (#443) | **none found** | **check it** |

The two rounds that shipped *after* this hazard was understood happen to be covered; the two
older ones are the ones to build `L0`-shaped rows against. That is a scan of row names, so it
must be confirmed by reading before either is called a hole — but it says where to spend the
two builds.

**And two measured deaths are recorded because they are evidence too.** `R-M2` (an early
`return` in `sh4_timer_tick`) scores 10/10 on its own probe — blind — and the SIBLING
offline row in `diff_sh4_tmu.c` catches it, so that two-detector split is verified rather
than asserted. `S-M1` (a shrunk `malloc`) reddens its gate but **not for the reason under
test**: gcc caught it at compile time and glibc `_FORTIFY_SOURCE` killed the process before
`arcbios_init` ran, so the allocation size is outside that detector's field of view.

### `floodclass` — held

**A guest that loops on a rejected operation can burn host CPU through an unlatched
`fatal()`, and the class spans many device files.** Filed as a class rather than a sweep
because the fix is per-path POLICY -- which of those `fatal()` paths are genuinely
guest-drivable -- and that needs a panel per path, not a regex.

**Severity was raised after this row was first filed**, by a measurement from a different
round: `fatal()` has no `quiet_mode` early-out (unlike `debug()`, which returns at
`debugmsg.c:375`), so an unlatched complaint **cannot be silenced even with `-q`**. A guest
looping on a rejected write therefore trades a host kill for an unstoppable host-CPU burn.

The latch idiom that fixes an instance already exists in-tree and is cheap to reuse:
`sh4_val_first()`'s three-part `(class, instance, bits)` key, as shipped by `#447` and
extended by `#448`/`#449`/`#451`/`#452`. Known instances are filed under their own names
(`rtcflood`, `wdcflood`); this row is the class they belong to.

### `sh4sqexpevt` — open, from the manual re-check, UNWITNESSED

*** THE STORE-QUEUE PREF PATH MAY RAISE THE WRONG EXCEPTION KIND, AND THE TREE ALREADY HAS
THE RIGHT CODE FOR IT. *** Two review seats named this independently while reviewing a
different finding; neither built anything, and neither has this been witnessed.

`cpu_sh_instr.c`, `X(pref_rn)`, the MMU-on SQMD arm:

```c
		if (cpu->cd.sh.mmucr & SH4_MMUCR_SQMD) {
			if (!(cpu->cd.sh.sr & SH_SR_MD)) {
				sh_exception(cpu, EXPEVT_RES_INST, 0, 0);
				return;
			}
		}
```

`EXPEVT_RES_INST` is `0x180`, *Illegal instruction*. The SH7750 Hardware Manual §4.7.4 SQ
Protection says, verbatim:

> "However, if SQ access is enabled, in privileged mode only, by MMUCR.SQMD, **an address
> error will be flagged** in user mode even if address translation is successful."

This tree already defines `EXPEVT_ADDR_ERR_LD` (`0x0e0`) and `EXPEVT_ADDR_ERR_ST` (`0x100`)
in `thirdparty/sh4_exception.h`. A guest dispatches on `EXPEVT`, so `0x180` and `0x0e0` send
it down entirely different handlers.

**A second question in the same function, and it may bear on the first.** §4.7.4 distinguishes
the two directions:

> "Write type exception judgment is performed for writes to the SQs, and **read type for
> transfer from the SQs to external memory (PREF instruction)**"

The code calls `sh_translate_sq_v2p(cpu, addr, &paddr, FLAG_WRITEFLAG)` — write type — for
the PREF path. **That may be deliberate:** the `#318` comment immediately above it explains
the flag choice in terms of what the translator returns ("with the write flag set this
returns either 0, having raised the fault itself, or 2 — there is no read-only success to
mishandle"), which is an argument about the helper's contract rather than about exception
kind. Whether the resulting fault kind matches the manual is not addressed there.

**Third, and softest:** it is not shown that `sh_translate_sq_v2p` raises all three of the
exceptions §4.7.4 names — TLB miss, protection violation, initial page write — rather than
some subset. The comment in the tree says "the translation faults raise themselves", which
is a statement of intent.

**Not a defect until witnessed, and stated that way deliberately.** Everything above is
reading.

#### What a witness costs — MEASURED, and it is not what this row first said

*** THE ORACLE ALREADY EXISTS, AND SAYING OTHERWISE WAS WRONG. *** This row first claimed a
witness needs "a different oracle from every SH probe in this tree". It does not.
`SH4_EXPEVT` is at `0xff000024` and `dev_sh4.c:1791` serves it, so an ORDINARY GUEST LOAD
reads the exception code — the same `mov.l @r1,r2` shape every probe here already uses.
Measured: a load from `0xff000024` into a pre-poisoned scratch word returns `00000000`,
distinguishable from the `11111111` poison, so the read genuinely happened and the register
genuinely is zero before any exception. `SH4_INTEVT` sits beside it at `0xff000028`.

**That correction also applies to `sh4dmacie`,** which this project had been scheduling as
"needs an interrupt-delivery oracle: a NEW capability". Its ORACLE is equally available; what
that row actually lacks is interrupt DELIVERY in the device, which is the FIX, not a test
capability. The two are different things and conflating them mis-ranked the queue.

**What IS hard is reaching the path, and the first attempt to do it was VOID.** The arm needs
all three of: MMU on (`MMUCR.AT`), `MMUCR.SQMD` set, and user mode (`SR.MD` clear). The
attempt put the guest code at `0x8c010010` — which is **P1, privileged-only** — so in user
mode the instruction FETCH faulted before `PREF` ever ran. The observed
`[ exception 0x180, pc=0x8c000400 ]` was that fetch fault, not the SQMD arm, and `EXPEVT`
read `0` in both the test and its control. Rule 4 caught it: *it did not fail for the reason
under test.*

So a real witness needs user-mode code in P0/U0, which with the MMU on needs a **UTLB entry**
mapping it. That is buildable and the route is now well understood — `#452` established
exactly how the memory-mapped UTLB windows at `0xf6000000`/`0xf7000000` behave — but it is a
substantially bigger probe than any in this tree, and it is honest to say so rather than to
imply the oracle was the obstacle.

### `landiskdisk` — SCOPED and measured. Cheap, zero-edit, and a harder blocker than filed.

*** THE FOUR BLOCKED ROWS ARE NOT MERELY UNDRIVEN — THEY ARE STRUCTURALLY UNREACHABLE. ***
`dev_wdc.c:461-468` returns from `wdc_command()` **before the opcode switch** when no IDE
image exists. Measured at rung 3, one guest `mov.b` into the ATA command register at
`0xb400000e`, real SH-4 decode, unmodified `-E landisk`:

| opcode | no disk | with an IDE disk |
|---|---|---|
| `0xE0` STANDBY | `[ wdc: command 0xe0 drive 0, but no disk image ]` | `[ wdc: WARNING! Unimplemented command 0xe0 … ]` |
| `0xE7` FLUSH | same no-disk line | same `Unimplemented` line |
| `0xEC` IDENTIFY | same no-disk line | `[ wdc: IDENTIFY drive 0 ]` |

**And the no-disk arm sets `int_assert = 1`** — the *opposite* of `wdcnoirq`'s symptom. A
diskless witness would have measured the wrong thing and looked green.

#### The change is ZERO-EDIT for the probes, which is the part worth knowing

`sh4_pcic_probe.py:227`'s shared `session()` already places `extra` before the kernel, so a
new probe attaches a disk with **no edit to that line at all**:

```python
P.write_arm(0xb400000e, 0xe0, "E0", kw, op=0x2100,
            extra=["-d", "i:/…/landisk-wd0-63M.img"])
```

That matters because **one `session()` is shared by eleven artefacts** — the `sh4_val`,
`sh4_chcr`, `sh4_rtcsr`, `sh4_sci` and `sh4_tlbda2` probes plus their five witnesses. None
of them acquires a dependency on an image file existing.

For the boot rig, `drive_guest.py:84` takes `"-d", "R:" + IMAGES + "/landisk-wd0-63M.img"`.
`R:` for the reason `images.md` already gives for luna88k. `i:` is *redundant* on landisk —
`get_default_disk_type_for_machine()` omits landisk from the SCSI list, so a bare `-d`
already yields IDE — but keep it for explicitness. The `prefix_d` gap at `diskimage.c:1763`
does not bite unless someone spells `di:`.

#### The image must be created, and CYLINDER-ALIGNED

```
dd if=/dev/zero of=_images/landisk-wd0-63M.img bs=512 count=129024   # 66,060,288 B
```

Non-floppy geometry is heads=16, spt=63 → 516,096 B per cylinder, and advertised capacity
rounds **up**. Measured: a plain 64 MiB image (131,072 blocks) advertises **132,048** — 976
phantom blocks that read zero and refuse writes, which is the `#416` residual showing up
again. 129,024 advertises exactly 129,024, and the guest agrees:
`wd0: … 63MB, 128 cyl, 16 head, 63 sec, 129024 sectors`.

**Avoid 737280 / 1228800 / 1474560 / 2949120 bytes exactly** — measured, a 1.44M image with
a bare `-d` becomes a FLOPPY and is invisible to `wdc`.

#### Risk to the eleven green probes: MEASURED NIL, with a negative control

Eight probes and five witnesses, run with and without a disk against one **pinned** binary:
every row **byte-identical**. And the control that makes that a measurement rather than a
no-op: pointing the same argv at a *nonexistent* image collapses `sh4_pcic` to **3/38 FAIL**,
so the argument really does reach gxemul.

**The boot rig also passes with a disk** — `BOOT_REACHED=1`, `VALUES=SH7751R,42`,
`VERDICT=PASS`, all eight `gate_hygiene` distress patterns still 0 — which refutes the
2026-08-19 panel's "trap" prediction *for the rig as it stands*, because its oracle is
markers and values rather than a transcript diff. Honest limit: **n=1** on the disk boot.

One real transcript delta: unmapped byte writes to `paddr=0x1400002c` go 6 → 12 and
**interleave into guest text** — `wd0 at wdc0 chan[ memory WRITE… ]nel 0 drive 0:`. Any
future marker must survive that splitting.

#### What each blocked row then needs

* **`wdcstandby` — cheapest, and the anchor.** With a disk `0xE0` reaches `default:` and
  emits its `Unimplemented command` line; a rung-3 witness is one store. A rung-4 boot
  witness needs `MAKEDEV`+`newfs`+`halt -p`, because the current rig conversation stops
  short: a plain boot drives **14 command writes over 7 opcodes** (`0xEC 0xF5 0x10 0x91 0xC6
  0x20 0xC4`) and **zero** without a disk. A prior panel line — *"`-d i:` does not replay
  `0xE0`"* — is measured **TRUE**; that seat's 10-opcode figure is the full-lifecycle number
  and its first seven reproduce exactly.
* **`wdcnoirq` — a rung-3 oracle now EXISTS and its mutant kill is MEASURED.**
  *** INTERRUPTS ARE SUPPRESSED WHILE SINGLE-STEPPING *** (`cpu_dyntrans.c:206`,
  `if (!single_step)`), so a `step`-based PC oracle cannot see delivery at all — every arm
  reads "no". **Free-running works**: `sr=0x40000000` (IRQ10's level is 5, hardcoded at
  `cpu_sh.c:255-258`), `vbr` in RAM, a `bra .` self-loop after the store, a breakpoint at
  `VBR+0x600`, then `continue`. Clean build: RECAL → delivered; `0xE0` with a disk → not
  delivered. Deleting `INTERRUPT_ASSERT(d->irq)` from `dev_wdc.c:113` flips the RECAL row to
  not-delivered while leaving `0xE0` unchanged — **a measured kill of the exact escape
  `wdcoracle` names**, needing no offline harness.
* **`wdcflood`** — 100 guest stores of `0xE7` give **100** lines with a disk and **0**
  without; host alive throughout. A one-line `warned_*` latch matches `#337`'s three
  existing ones. **Sibling worth its own row: the NO-DISK arm floods identically** (100 `but
  no disk image` lines) through `debug()` — invisible free-running at verbosity 0, visible in
  every cold-debugger probe.
* **`idesync`** — lowest value of the four. `0xE7` is defined at `wdcreg.h:130` and never
  referenced; no OpenBSD 7.6 path issues it, and a `dd`-through-`/dev/rwd0c` attempt failed
  because the ramdisk has no node. Reachability stays where the earlier seat left it.

### `landiskaux` — open, NEW, and adjacent to `wdcnoirq`

**The wdc device-control register is unmapped on landisk.** `dev_wdc.c:1056` places
alt-status/device-control at `addr + 0x206` under a machine switch covering MACPPC, HPCMIPS
and IQ80321 — **not landisk**. OpenBSD writes `0x1400002c` via `obio_iomem_write_1` and it
lands nowhere: 6 unmapped writes diskless, 12 with a disk. **So the guest's nIEN and SRST
are no-ops today**, which bears directly on `wdcnoirq`'s interrupt behaviour.

### `imagesmd` — records only

`regress/images.md`'s landisk section still says *"the rig deliberately sends no input"*,
which `#293` fixed; `gate_crossfamily.sh:186-192` already annotates it as having been untrue
for far longer than it was true.

### `sh4prio0` — ~~open~~ **FIXED as #455 (`dc0c9d5`)**. One guest store, unpreventable.

*Kept in full rather than trimmed, because the design recorded below was REFUTED before it was built and a future reader needs to see that it was caught. The state line is corrected here rather than left to the ledger alone: a row reading `open` on shipped, witnessed, gated work tells a future reader it was never done.*

`src/cpus/cpu_sh.c:312-316` ends the host process when any interrupt is asserted at priority 0:

```c
	if (prio == 0) {
		/*  Interrupt not implemented? Hm.  */
		fatal("[ SH interrupt 0x%x, prio 0 (?), aborting ]\n", irq_nr);
		exit(1);
	}
```

**The comment is a wrong record in its own right: nothing is unimplemented.** Priority 0 is a
documented, guest-selectable, RESET-DEFAULT state. Quoted verbatim, and corroborated four
separate ways in the same manual:

> "Each interrupt has a priority level (16-0) ... **When level 0 is set, the interrupt is
> masked and interrupt requests are ignored.**" — §19.2, `_scratchpad/sh7750_hardware.txt:39887-39888`

> "**IPRA to IPRC are initialized to H'0000** and IPRD is to H'DA74 by a reset."
> — §19.3.1, `:40193-40194`

So **every on-chip source is priority 0 out of reset**, and the model's own init agrees:
`cpu_sh.c:204-218` sets `intc_iprd`, the INTPRI/INTMSK words and comments *"All others are
zero"*, then bakes that into the array at `:220`.

#### TWO ROUTES, and the second is the one that changes the ranking

**Route A — `-E landisk`, ordinary driver ordering.** Enable the TMU0 underflow interrupt
(`TCR0 = 0x0020` — and note it PASSES `#447`'s guard, because `TCR_UNIMPLEMENTED` is `0x02DC`
and `TCR_UNIE` is `0x0020`, not in the mask), set TCOR0/TCNT0, start it with `TSTR = 1`, and
never touch IPRA. The host timer underflows, `dev_sh4.c:585` asserts, `prio = (0 >> 12) & 0xf
= 0`, and the process dies. A guest that enables before prioritising is doing something
perfectly ordinary.

*** Route B — `-E testsh`, ONE STORE, AND NO GUEST WRITE CAN PREVENT IT. ***
`machine_test.c:98-99` wires the **entire test-machine interrupt tree** to
`SH4_INTEVT_IRQ15` (`0x3e0`, array index 31). `sh_update_interrupt_priorities()`'s IRQ loop
(`cpu_sh.c:255`) is bounded `i <= SH4_INTEVT_IRQ14`, so index 31 is **never assigned** — and
extending the loop would not help, because the formula `15 - ((i - IRQ0)/0x20)` gives
`15 - 15 = 0` for that very line. `dev_irqc.c:185` defaults to all interrupts enabled, so one
store to `0x110000a0` (`DEV_MP_IPI_ONE`) reaches `dev_mp.c:206` → `dev_irqc.c:63` → the prio-0
kill, synchronously, inside the store instruction.

**In practice: the SH test machine's interrupt controller cannot be used at all** — any
interrupt it delivers ends the emulator. All three line numbers checked by hand.

#### *** THE WITNESS IS CHEAP, AND THE REASON CORRECTS THIS PROJECT'S OWN RULE ***

The carrier said a stepping probe cannot observe interrupts. **The exact word is DELIVERY.**
`cpu_dyntrans.c:204-206` guards the exception DISPATCH; this `exit(1)` sits in the **assert**
path, upstream of it. And asserts reach it while stepping by two routes: a device handler
asserts synchronously inside the guest's own store, and **tick functions run under stepping
too** — `machine.c:726-728` is `ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT`.

So the host simply dying IS the observable, and rows P1-P3 need no `vbr`, no handler, no
breakpoint and no `continue`. The carrier bullet has been corrected. *A scoping seat caught
the main loop about to build the full free-running rig for a defect that a `step` would show.*

Probe `regress/sh_intprio_probe.py`, rung 3. ~~on unmodified `-E landisk`, importing
`session()` / `write_arm()` / `row()` from `sh4_pcic_probe.py`~~ **NEITHER HALF IS WHAT
SHIPPED.** The primary rows run on `-E testsh`, not landisk, and the probe defines its
OWN `session()` rather than importing one, because it needs a promptless free-running
driver that `sh4_pcic_probe.py` has no notion of. Verified it does NOT trip
`gate_hygiene.sh`'s readiness-idiom census, so the pin bump feared below was never owed — `gate_hygiene.sh`
pins the count of the three `#392` readiness idioms across `regress/*.py`, so a copy silently
needs that pin bumped.

| row | pre-fix | post-fix |
|---|---|---|
| ~~**P1** — TCR0/TCOR0/TCNT0/TSTR stores, then `step 40000`~~ **REFUTED — see the correction below** | — | — |
| **P2 liveness** — known word to scratch, read back through the same decode | — | `0x12345678` returns — **the value was changed from `0x5a5a5a5a` during construction: a palindrome under byte swap cannot see a byte-order defect, and one was hiding** |
| **P3 device signature** — read TCR0 back as `0x0020`, TSTR as 1 | — | proves the stores reached `DEVICE_ACCESS(sh4)`, not a hole |
| **P4 accept row** — IPRA first, then the prologue; free-running; handler reads INTEVT | — | INTEVT reads `0x400`: selected AND delivered |


> *** CORRECTION, 2026-08-22, BEFORE ANY OF THIS WAS BUILT. *** The `step 40000` design
> above is REFUTED and the shipped probe does not use it. A TMU underflow is produced by
> a HOST timer, and `debugger.c:800` stops host timers with the step command returning at
> `:835-836` before `timer_start()` at `:840` — so a step-based timer row scores a correct
> PRE-FIX build ALIVE and fails vacuity floor clause (a) in silence. The shipped witness is
> a SYNCHRONOUS one guest store on `-E testsh`; the TMU route is covered by two rows that
> FREE-RUN. Left visible rather than deleted, because this entry is where the wrong design
> was written down and a future reader needs to see it was caught, not quietly replaced.

**P4 is the de-escalation clause's cost, not future strengthening.** Enumerated from the diff,
`prio == 0` is the only predicate that gated death, so exactly one accept row is owed.
**Failability, per the accept-row rule:** the growth mutant is `if (prio <= 1) return;`. The
store arm at `dev_sh4.c:2389` stores `intc_ipra = idata` **unmasked** and `cpu_sh.c:263-264`
loads `(intc_ipra >> 12) & 0xf` straight into the predicate's operand, so a guest can place
any value 0..15 there and guard-only growth is non-equivalent. Pin P4 at **prio 1**
(`IPRA = 0x1000`) so it reddens. There is no latch operand, so the JOINT form does not exist
here and guard-only is the least-observable non-equivalent form.

#### THE FIX IS A BARE `return`, AND THE LATCH IDIOM DELIBERATELY DOES NOT APPLY

The `sh4_val_first` family (`#438`/`#441`/`#443`/`#447`/`#449`) exists for one shape: *the
guest asked for a feature this model does not implement, so say so once and decline.*
**Priority 0 is not an unmodelled feature — it is a modelled state whose defined meaning is
"masked".** A latched diagnostic would fire on correct guest behaviour, and `fatal()` has no
`quiet_mode` early-out (`debugmsg.c:384-390`), so it could not even be silenced. Three more
reasons: the latch array lives in `struct sh4_data`, a DEVICE, while this is `cpu_sh.c`, the
CPU; the existing comment is itself false; and the manual prescribes silence.

Leave `SH_INT_ASSERTED` set: masking blocks ACCEPTANCE, not the request.
`sh_update_interrupt_priorities()` preserves that bit on purpose (`cpu_sh.c:250-253`) and the
deassert rescan (`:373-386`) can never select a prio-0 entry, since `prio > int_level` is
`0 > 0`.

### `sh4tlbmulti` — *** CLOSED, shipped as `0678450`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

*** A GUEST UTLB WRITE THAT PRODUCES TWO MATCHING ENTRIES ENDS THE HOST PROCESS. ***
`dev_sh4.c:1158-1159` raises `sh_exception(cpu, EXPEVT_RESET_TLB_MULTI_HIT, 0, 0)` when an
associative-array write finds `n_hits > 1`. `sh_exception()`'s switch has **no case for
`EXPEVT_RESET_TLB_MULTI_HIT`** (`0x140`, `sh4_exception.h:59`), so it falls to the `default:`
arm at `cpu_sh.c:768-770`:

```c
	default:fatal("sh_exception(): exception 0x%x is not yet implemented.\n", expevt);
		exit(1);
```

**TLB multiple-hit is a documented SH-4 reset exception** — a legal, guest-triggerable
hardware condition, reachable by storing to the UTLB address array so that two entries match
one VPN/ASID. The model ends the host instead of vectoring the guest.

Found by a records seat sweeping for siblings of `sh4prio0` rather than by looking for it,
which is the argument for that sweep: **it is the same family** (a documented legal state
reaching `exit(1)`) in the **same file**, and the `sh4prio0` brief had missed it entirely.

Its own round under the scope rule: different exception, different detector, no shared
oracle. Ranked with `sh4prio0` because a round that fixes one should not leave a reader
believing the family is closed.

**Also swept and found NOT to be kills, recorded so the blanks do not read as unchecked:**
`cpu_sh.c:100-101` (SH64, construction-time), `cpu_sh.c:647` (`fatal()` with no exit),
`dev_sh4.c:2703` (under `#ifdef SH4_DEBUG`, defined nowhere in the tree), `dev_sh4.c:2877-2890`
(devinit wiring), all five `dev_irqc.c` sites and both `dev_mp.c` sites (`fatal()` only).
`dev_sh4.c:1970` is a real kill but is already filed as `sh4pclock`.

### `sh4irq15` — *** CLOSED, shipped as `9d5fd69`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

`machine_test.c:99` selects `SH4_INTEVT_IRQ15`, the one line number that is priority 0 by
construction. **After `sh4prio0` lands, `-E testsh` goes from LOUDLY unusable to SILENTLY
unusable**, which is strictly harder to notice — the de-escalation hazard in its literal form.
One identifier: `SH4_INTEVT_IRQ14`. Separate file, separate device, so a separate round; the
row exists now so the transition is not invisible.

The manual supports the change independently: §19.2.2 (`:39908`) says an IRL value of 15
"indicates **no interrupt request** (interrupt priority level 0)", and Table 19.5 (`:40071`)
tops out at `H'3C0`. **There is no `H'3E0` source in the SH7750 at all.**

### `sh4iprbcd` — *** CLOSED, shipped as `7e5c0f6 bb05ce7`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

`sh_update_interrupt_priorities()` (`cpu_sh.c:246-281`) consults only `intc_ipra` and
`intc_intpri08`. `dev_sh4.c:2394-2418` stores `intc_iprb`, `intc_iprc` and `intc_iprd` and
calls the recompute, which ignores all three. **So WDT, REF, SCI, GPIO, DMAC, H-UDI and the
IRL lines are priority 0 permanently, and IPRB/IPRC/IPRD writes are inert.** Latent only
because nothing asserts those lines in-tree today — which is precisely the condition
`sh4prio0` shows can change.


> *** PASS-1 FINDINGS, 2026-08-22, and two of them change the round. ***
>
> **THE SCIF SOURCE IS SETTLED, and it is not INTPRI08.** Table 19.5 (`:40142`) gives the
> per-source answer verbatim: `SCIF ERI H'700 ... IPRC (7-4)`. Table 19.6 agrees. And **the
> only INTPRI register in the whole 1074-page manual is INTPRI00** (19.3.3, `:40348`,
> "SH7750R Only"), which covers TMU3/TMU4 -- not SCIF. There is no INTPRI04/08/0C anywhere.
> The code says where it came from: `cpu_sh.c:204-206` reads *"according to the SH7760
> manual"*, and the machines emulated are SH7750 and SH7751R. Neither is an SH7760.
>
> **AND THE INTPRI CASES ARE UNREACHABLE DEAD CODE.** `dev_sh4.c:2421-2455` handles
> `SH4_INTPRI00` and friends, but the only registered window is `SH4_REG_BASE` + 0x01000000
> = `0xff000000`-`0xffffffff`, and `SH4_INTPRI00` is `0xfe080000` -- outside it. **So
> `intc_intpri08` is its init value `0x33333333` forever, and SCIF's priority is a
> guest-immutable constant 3 on every SH4 machine in this tree.** #456's round block already
> measured the symptom without naming the mechanism: *"the register that would lower it is
> unmapped -- non-existant paddr=0xfe080008"*. Verified: window and address both opened.
>
> **DO NOT "read all four registers per Table 19.6" -- IPRD IS A HAZARD.** Its only function
> is per-pin IRL priorities in IRLM=1 mode, which this model deliberately refuses and latches
> (`SH4_VAL_ICRIRLM`). Worse, the per-pin IRL slots **alias** encoded-mode IRQ slots
> (`0x240`=IRQ2, `0x2a0`=IRQ5, `0x300`=IRQ8, `0x360`=IRQ11) that the hardwired 15..1 loop
> already owns and that the dreamcast ASIC drives through today. Writing IPRD priorities into
> aliased slots would fight the encoded loop, order-dependently. IPRD stays out, documented.
>
> **FIVE SOURCES HAVE NO INTEVT CONSTANT** -- RTC, REF, GPIO, DMAC, H-UDI -- and nothing
> in-tree asserts any of them. So the only BEHAVIOURALLY WITNESSABLE payload here is the SCIF
> re-source; the rest is honest state. The record must claim exactly that and no more.
>
> *** REGRESSION RISK, to be measured BEFORE the edit: *** re-sourcing SCIF to IPRC drops its
> effective reset priority from the phantom 3 to the manual's 0 (IPRA-C reset `H'0000`). If a
> rig's guest never writes IPRC, its SCIF interrupt path goes SILENT -- the de-escalation
> shape. Cheap pre-check: log `SH4_IPRC` (`0xffd0000c`) writes during landisk and dreamcast
> boots first.
>
> Two more L4s to fix in the same diff: the SH7760-attributed init comment
> (`cpu_sh.c:204-206`) and the wrong-chip register table above the recompute (`:230-244`),
> whose IPRA[3:0], IPRB[7:4] and IPRC[7:4] all say "Reserved" where the manual says RTC, SCI
> and SCIF.

### `sh4prioraise` — *** CLOSED, shipped as `7e5c0f6 bb05ce7`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

`sh_update_interrupt_priorities()` rewrites the priority nibbles but never recomputes
`int_to_assert` / `int_level`. A guest that asserts while masked and then raises IPRA gets
nothing until the next assert/deassert edge. Pre-existing; `sh4prio0` makes it *reachable*
rather than fatal, which is why it is filed in the same breath. The natural completion is to
run the `:373-386` rescan at the end of the recompute — a second design question, its own
round.

### `shprotld` — open. #454's one un-fixed escape, filed rather than chased.

*** EVERY SH TLB ROW IN THE TREE RUNS PRIVILEGED, so the READ-side protection code is
never reached and corrupting it changes nothing any detector can see. *** Found by the
ask-again on #454's pass 2, after the kill table was already clean.

The mutant: change `EXPEVT_TLB_PROT_LD` at `memory_sh.c`'s `protection_violation:` label
to any other value. It passes **all 31** rows of `sh_halt_probe.py`. The reason is
structural rather than accidental — in privileged mode a read to a `PR=00` page is
*permitted*, so `sq pr00 rdok` and `sq pr00 evt` both expect success and never reach the
protection arm at all; `sq miss evt` pins only the miss code; the ITLB rows involve no
protection case.

**FILED, not fixed, and the three reasons are the floor rules doing their job:** the
mutation is in the general TLB table rather than at #454's call site, so it is not this
round's material; #454's detector is already ABOVE the vacuity floor with (a), (b) and
(c) all measured green, which makes a measured escape coverage DEBT rather than a floor
breach; and the row that would close it is a user-mode row, which carries a trap this
project has already paid for once — *the instruction fetch needs a user-accessible page,
and an earlier SQMD witness put its code at `0x8c010010`, which is P1 and
privileged-only, so the fetch faulted before the access under test ever ran and the
`0x180` it measured came from the fetch.*

Closing it also closes a second escape a different seat named independently at pass 1
("return 2 on any UTLB hit, skipping the PR/D logic"), which is invisible for the same
reason: the caller treats 1 and 2 alike, so only a user-mode row separates them. **One
row, two measured escapes** — which is what makes it worth its own entry rather than a
footnote.

### `sh4sqwrite` — open. PROMOTED, not new: the archived audit already named it, and `sqreadtype` makes it the sole carrier.

*** THIS ROW IS NOT A DISCOVERY AND SAYING SO MATTERS. *** A records seat caught an earlier
draft of this entry calling itself NEW. The gap is already named, one clause deep inside the
archived audit block at the head of this file (`:441-443`): *"queue-filling stores under AT=1
take the identity map and skip UTLB judgment entirely, where real hardware exception-judges
SQ-area writes too."* What changes today is its RANK, not its existence — `sqreadtype` makes
it the **sole carrier of SQ-page IPW and protection semantics**, so a clause buried in an
archive is no longer the right home for it.

**A sibling in the same archived bullet, from the same seat's sweep:** `:437-439` writes the
SQMD address error as `EXPEVT_ADDR_ERR_ST`. Under read-type judgement the PREF path owes the
**`_LD`** form (H'0E0). That parenthesis silently presumed the write direction, so it is part
of this correction's sibling set and not a separate finding.

*** 4.7.4 GIVES THE STORE-QUEUE TWO JUDGEMENTS AND THIS MODEL PERFORMS NEITHER CORRECTLY. ***
The manual sentence covers both halves in one breath:

> "**Write type exception judgment is performed for writes to the SQs**, and read type for
> transfer from the SQs to external memory (PREF instruction), and a TLB miss exception,
> protection violation exception, or initial page write exception is generated."
> — SH7750 Hardware Manual Rev.7.00, §4.7.4, `_scratchpad/sh7750_hardware.txt:11744-11746`

`sqreadtype` fixes the **read** half. The **write** half has no judgement at all:
`sh_translate_v2p()` maps `0xe0000000..0xe3ffffff` identically and unconditionally, because
that identity mapping is how an ordinary guest store reaches the modelled queue SRAM.

**So the interim state this round deliberately ships is: the WRITE half raises nothing,
while the PREF still raises the READ-side set — TLB miss, and user-mode read
protection.**

*** THAT SENTENCE READ "an SQ page raises NO MMU fault of any kind" AND THE ROUND'S OWN
DETECTOR DISPROVES IT: `sq miss evt` observes a read-type TLB miss (0x040) on the FIXED
build. ***  The claim was corrected in `memory_sh.c:296-303` during the round and
survived here and in the ledger row's TITLE — mechanical rule 2's
corrected-in-one-place-survived-in-two, in the round that celebrated a seven-site sibling
sweep. The sweep covered the OLD claim's sites; nobody grepped the round's own NEW claim.
Found by the regress seat, which read the kill table rather than the prose.
the wrong instruction with the wrong semantics but did fault; after it, the read half
*correctly cannot* raise IPW (§3.6.7 requires "a data access (write)") and the write half
still never runs. A guest kernel tracking the D bit on an SQ page through PREF-time IPW loses
that until this row lands. **Stated out loud so the next round is motivated by a named gap
rather than rediscovered by a confused seat** — five panel seats reached that conclusion
independently and one (codex) dissented, holding that C1 is an "unshippable intermediate
state". Its dissent is recorded here rather than resolved: the round-scope rule decided this,
not a majority.

**Why it could not join `sqreadtype`'s round**, by the rule's own clauses — grok's table,
which codex's own answer confirms against codex's own recommendation, because the witness it
proposes IS a new oracle:

| clause | the PREF flag (shipped) | the SQ-write judgement (this row) |
|---|---|---|
| witnessed | yes — the five R81 rows | **NO** — nothing in the tree witnesses a guest store to the window |
| same class | 4.7.4 PREF half | 4.7.4 store half — related, not the same site |
| same detector, no new oracle | re-pins existing rows | **new** sequence AND new observation. FAILS |

**The smallest correct implementation, recorded now so the next round does not re-derive it**
(three seats converged on the same shape): on a store into `0xe0000000..0xe3ffffff` with
`MMUCR.AT` set, run `translate_via_mmu()` with `FLAG_WRITEFLAG` against the SQ virtual
address; on fault, return without touching queue SRAM; on success **discard the translated
PPN and deposit into the identity-mapped queue SRAM as today** — the PPN is PREF's
destination, and writing it here would corrupt the destination at fill time. Do not apply the
check when AT is clear, nor to PREF's own `PHYSICAL` reads of the queue.

**The witness that would license it** (rung 3, and note it needs a REAL guest store — the
existing `sq_seq()` fills the queue with debugger `put w`, which bypasses translation
entirely and therefore cannot witness this): privileged, UTLB entry PR=11 D=0, a guest store
into the SQ window. Pre-fix the word lands and no EXPEVT is set; post-fix `EXPEVT` reads
`H'080` (`EXPEVT_TLB_MOD`) and the queue word is unchanged. Liveness control: a D=1 neighbour
entry through the same decode. Same machine description, no `device_add`.

**Fold in with it — the SQMD exception type, same semantic class.** 4.7.4's last sentence
says that with `MMUCR.SQMD` set, user mode takes an **address error** even when translation
succeeds. `X(pref_rn)` HAS that arm and raises `EXPEVT_RES_INST` (illegal instruction)
instead. *A panel seat claimed the check was absent entirely; that is refuted — it is present,
and only its exception code is wrong.* Already filed as `sh4sqexpevt`; cross-referenced here
because one round should close both.

### `sh4itlbpr` — open, NEW. One bit too wide, and SIX shipped rows require it.

`dev_sh4_itlb_da1()` (`src/devices/dev_sh4.c:999-1001`) builds its field mask by reusing the
**UTLB's** two-bit PR mask:

```c
uint32_t mask = SH4_PTEL_SH | SH4_PTEL_C | SH4_PTEL_SZ_MASK |
    SH4_PTEL_PR_MASK | SH4_PTEL_V | 0x1ffffc00;
```

`SH4_PTEL_PR_MASK` is `0x00000060` — bits [6:5] (`include/thirdparty/sh4_mmu.h:54`). **The
ITLB has only one PR bit.** Two independent manual sentences:

> "In the data field, PPN is indicated by bits [28:10], V by bit [8], SZ by bits [7] and [4],
> **PR by bit [6]**, C by bit [3], and SH by bit [1]."
> — §3.7.2 ITLB Data Array 1, `_scratchpad/sh7750_hardware.txt:10035-10036`

> "There is only one PR bit, corresponding to the upper of the PR bits in the UTLB."
> — §3.4.2 ITLB Configuration, `:9402`

Union of the documented fields: `0x1ffffc00 | 0x100 | 0x90 | 0x40 | 0x08 | 0x02` =
**`0x1ffffdda`**. The model uses `0x1ffffdfa`. The difference is exactly **bit 5**, which is
reserved in ITLB data array 1 with an undefined read value. Both directions are affected: the
write path stores it (`:1060`) and the read path returns it (`:1076`).

*** SEVERITY IS LOWER THAN THE SWEEP RANKED IT, AND THE REASON IS WORTH KEEPING: NO
TRANSLATION DECISION DEPENDS ON THE BIT. *** Traced rather than assumed. `itlb_lo` IS live —
`memory_sh.c:113-122` scans the ITLB first for instruction accesses via the negative-index
hack — but the instruction arm tests only `if (!(pr & 2))`, i.e. bit 1 of the extracted
field, i.e. **bit 6**, the real PR bit. Data accesses start at `i_start = 0` and never reach
the ITLB entries at all. So bit 5 in `itlb_lo` is inert everywhere: storable, readable, and
without effect.

**The live cost is therefore the ORACLE, and it is the same shape as `sqreadtype`.** `#452`
strengthened these rows to EQUALITY precisely to make them falsifiable, and the value they
were pinned to is one the manual does not license — so **six rows now REQUIRE the emulator to
return a bit the hardware leaves undefined**: probe `A1`/`A3`/`A4i`/`R3`/`O` and witness `C1`,
all against `ITLB_MASK = 0x1ffffdfa` (`regress/sh4_tlbda2_probe.py:71` and the witness).

**Two detectors in one family pinned the model's behaviour rather than the architecture's**
— *`gate 10`'s was corrected by `#454`; this ITLB one is the survivor, and it is why the
pattern is recorded rather than the individual bit* —
(this and gate 10's `sq at1 clean`), which is the pattern to watch for, not the individual
bit. Fix under the ORACLE-CORRECTION RULE: re-pin the six rows to `0x1ffffdda` FIRST, measure
the committed build RED, then narrow the device mask. Returning 0 for a reserved bit is a
legitimate reading of "undefined"; modelling it as storage is a fiction that a probe then
enforced.

### `shsweep` — the exhaustive manual audit, ranked. Several items are LIVE.

*** ~250 SuperH architectural claims graded against the two real manuals, 2026-08-22, at
the owner's direction. *** The CONFIRMED mass is large and mostly uninteresting — **all 17
EXPEVT constants, every INTEVT but one, every FPSCR/SR bit position, every TMU/RTC/SCIF/
SCI/DMAC/BSC register address and width, the whole `#297` FTRC ladder, `#300`, `#315`,
`#317`, and `#318`'s address composition all hold exactly**, several of them written when
no manual was in the tree. What follows is only what did not hold.

#### 1. *** A SHIPPED GATE ROW PINS THE OPPOSITE OF THE MANUAL AND WOULD REDDEN A CORRECT
BUILD. *** This is the one to fix first.

`regress/gate_sh_rounding.sh:161-163`:

> `# `sq at1 clean` pins the WRITE-type judgement the panel split on: a clean page`
> `# owes an initial-page-write fault, so a build that judged this access as a read`
> `# would complete the copy and fail this row alone.`

SH7750 Hardware Manual §4.7.4, verbatim:

> "Write type exception judgment is performed for writes to the SQs, and **read type for
> transfer from the SQs to external memory (PREF instruction)**, and a TLB miss exception,
> protection violation exception, or initial page write exception is generated."

**The PREF transfer is READ type.** `cpu_sh_instr.c:3745` passes `FLAG_WRITEFLAG`. So a
clean page owes nothing, `sq at1 prot` (PR=00, "can be read only, in privileged mode") is
likewise wrong, and **the row is written so that correcting the code turns it red**. A
detector that enforces a defect is worse than no detector.

The same reasoning is asserted in `CHANGELOG.md:13600-02`, in a retrospective saying it was
*"re-reviewed against the SH7750 manual"* — **at a date when no SH manual was in the tree.**
That is the `#357`/`#362`/`#365` shape again, and this time it reached a gate.

`sh4sqexpevt` (below) already quotes the same passage CORRECTLY, so the tree currently holds
both readings and the gate implements the wrong one.

#### 2. A shipped oracle constant is one bit too wide — and it is `#452`'s

`sh4_tlbda2_probe.py:71` and `sh4_tlbda2_witness.py` use `ITLB_MASK = 0x1ffffdfa`. The
manual gives the ITLB data-array-1 layout as *"PPN … V by bit [8], SZ by bits [7] and [4],
**PR by bit [6]**, C by bit [3], and SH by bit [1]"*, and separately: *"There is only one PR
bit, corresponding to the upper of the PR bits in the UTLB."* **Bit 5 is reserved with an
undefined read value.** The correct mask is `0x1ffffdda`.

**BUT THE PRECISE STATEMENT MATTERS, AND THE SUMMARY ABOVE OVERSTATES IT — corrected here
rather than repeated.** `#452`'s rows do not claim to be a hardware oracle. Their comment
says the expected value is *"the value THIS DEVICE'S OWN MASK folds 0xffffffff to"*, which
is accurate and is the right thing for a REGRESSION detector to pin: it fails when the
emulator changes, which is its job.

So this is **not a wrong record in the probe**. It is a one-bit **fidelity gap in the
device**: `dev_sh4.c`'s `sh4_itlb_da1` handler masks with `SH4_PTEL_PR_MASK` (`0x60`, both
PR bits) where the manual gives the ITLB **one** PR bit at [6] — the UTLB is the one with
two, *"PR by bits [6:5]"* at `:10180`. A guest can therefore store bit 5 into an ITLB entry
and read it back, where hardware leaves it reserved with an undefined read value.

Severity: low and stated as such. Nothing observed is wrong today, no in-tree guest writes
that bit, and the six rows would simply move with the mask if the device is corrected. What
it costs is that `#452`'s equality rows currently pin the emulator's behaviour at a point
where the emulator and the hardware differ — which is fine for regression, and worth knowing
before anyone cites those constants as architectural.

#### 3. REFUTED and guest-reachable — these change behaviour

| site | what it does | what the manual says |
|---|---|---|
| `cpu_sh.c:312-316` | priority 0 → `fatal()` + **`exit(1)`**, commented *"Interrupt not implemented? Hm."* | Priority 0 is **legal and documented** — *"When level 0 is set, the interrupt is masked and interrupt requests are ignored"* — and IPRA/IPRB/IPRC **reset to `H'0000`**, so everything is priority 0 out of reset. A guest-reachable host kill, latent only because landisk kernels program IPRA before starting the timer. |
| `cpu_sh.c:653` | BL already set → `EXPEVT_RESET_POWER` (`0x000`) | *"a manual reset is executed. The value in EXPEVT at this time is **H'0000 0020**"* → `EXPEVT_RESET_MANUAL`. Found independently by two sweeps. |
| `memory_sh.c:328-333` | user access ≥ `0x80000000` → `EXPEVT_TLB_MISS_LD/ST` | Listed under **Data Address Error**: *"Exception code H'0E0 (for a read access) or H'100"*. Guest kernels dispatch on EXPEVT. |
| `cpu_sh_instr.c:3057` | `X(fcnvsd_fpul_drn)` does `cpu->cd.sh.fpul = (int32_t) op1.f;` | FCNVSD reads FPUL and never writes it. **The emulator destroys FPUL on every FCNVSD**, with the same UB `(int32_t)` cast `#297` removed from FTRC. New, unfiled, and the smallest fix in the list. |
| `memory_sh.c:358-364` | kernel access to `0xe4000000..0xefffffff` → `fatal()` + `exit(1)` | *"Reserved area"*, and *"Operation is not guaranteed"*. Undefined is not process death. |
| `dev_sh4.c:2899` | BSC reset `WCR3 = 0x77777777` | *"WCR3 is initialized to **H'07777777**"*. BCR2/WCR1/WCR2 on the same lines are correct. |
| `dev_sh4.c:2023` | TCR write stores UNF verbatim | *"Writing 1 does not change the value."* A guest can fabricate an underflow and a spurious interrupt. |
| `dev_sh4.c:596` | DMA count masked `0x1fffffff` | *"Bits 31-24 of these registers are reserved"* — DMATCR is 24-bit. (The 29-bit SAR/DAR masks are correct.) |

#### 4. A claim this project made twice, refuted

`cpu_sh_instr.c:150-151` and its sibling `float_emul.c:653` say the SH-4 never delivers a
subnormal arithmetic result, and that with `DN=0` the silicon raises an FPU error instead.
**Refuted:** *"When FPSCR.DN = 0, a denormalized number with the same sign as the unrounded
value, or zero with the same sign as the unrounded value, is generated."* The FPU error is
raised on a denormalized **input**, not a denormalized result. The **code is right and the
justification is wrong** — `cpu_sh_instr.c:159-162` calls the DN=0 pass-through "a NAMED
divergence" when the manual shows hardware doing the same thing.

Rule 2 in action: the claim lives in two files, and only one carries the correction. The
same happened to `#316`'s FSRRA claim at `cpu_sh_instr.c:3281`, whose sibling at `:3309`
was corrected while it was not.

#### 5. UNSUPPORTED — absent, which is not the same as contradicted

**The entire PCIC** (`sh4_pcicreg.h`, `dev_sh4.c:2806`, both PCIC probes): *"PCI controller"*
has **zero hits** in the hardware manual, and the programming manual footnotes it
*"SH7751 exceptions only. Not provided in the SH7750 Series."* The register block lives in
the SH7751 manual, which this tree does not hold. **So those probes' standing decision to
cite headers rather than a manual is correct, and now verifiably so.**

**SH7751R**: zero hits in both. `SH4_PVR_SH7751`, `SH4_PRR_7751R`, and
`sh_halt_probe.py:21`'s *"the SH7751R this rig models"* are unsourceable here.

**The SZ bit ordering** (`sh4_mmu.h:135-136`): both manuals say only *"SZ by bits [7] and
[4]"* and label the field `SZ [1:0]`. **No sentence assigns SZ1 to a bit.** It is
load-bearing — consumed by `memory_sh.c`, `cpu_sh_instr.c:2794` and five `dev_sh4.c` sites —
so it needs an **empirical pin, not a citation**.

#### 6. Other probe oracles pinning values the manual contradicts

`sh4_bsc_width_probe.py` D8 expects `03c0ffff` where only bits 15/14/13/0 are R/W;
`sh4_val_probe.py` V17/V18 write `0x01` to RCR1 and expect it back, but bit 0 is AF
(*"Writing 1 does not change the value"*); `sh4_rtcsr_probe.py` A3 and its witness use a
bare `mov.w` to RTCSR where the manual mandates a word access **with `B'10100101` in the
upper byte** — which also settles the open question at `dev_sh4.c:1590` that says *"there is
no SH-4 document in this tree to settle which convention is right"*.

#### 7. Attribution slips worth one records pass

`dev_sh4.c:592`, `:2891-2894` and `sh4_dmacreg.h:31-32` cite *"the SH7760 manual"* —
`SH7760` appears **zero times** in either document. The "8 DMA channels on SH7760" claim is
really **SH7750R**, at exactly the addresses the header uses. `CHCR_TD` names a bit the
manual calls **DE**; `CHCR_CHSET` names one that is Reserved; `SH_RCR2_ENABLE` is **RTCEN**.

**Ordering, from the sweep and endorsed here:** (1) the gate row, (2) the `ITLB_MASK` bit,
(3) `cpu_sh.c:312` priority-0 host kill — it is the only *new* guest-reachable `exit(1)` in
the list — then `cpu_sh.c:653` and `memory_sh.c:328`, then `fcnvsd`, then the single-token
register corrections, then the records pass.

### `sh4a4gate` — open, found by the manual re-check, not yet witnessed

*** THIS TREE MODELS NO SH-4A CPU, YET DECODES TWO SH-4A-ONLY INSTRUCTIONS FOR EVERY SH-4
IT MODELS. *** Found 2026-08-22 while re-checking earlier SH claims against the manuals
obtained by owner directive.

`cpu_sh.h:61-67` defines exactly four CPU types: `SH7708R` (arch 3), `SH7750`, `SH7750R`
and `SH7751R` (all arch 4). There is no SH-4A entry; the `SH5` line is commented out.

`cpu_sh_instr.c` decodes both of these with no CPU-type gate at all:

```c
        } else if (lo8 == 0x7d) {
                /*  FSRRA FRn  */
                ic->f = instr(fsrra_frn);
        ...
                        ic->f = instr(fsca_fpul_drn);
```

**Neither instruction exists in either manual.** `FSRRA` and `FSCA` each appear ZERO times
in the SH-4 Software Manual (Rev. 5.0) and ZERO times in the SH7750 Hardware Manual
(Rev. 7.00) — and the SH-4 opcode table has no entry for `1111nnnn01111101`, although its
immediate neighbours are all there:

| encoding | instruction | in the SH-4 table? |
|---|---|---|
| `1111nnnn00001101` | FSTS | yes |
| `1111nnnn01001101` | FNEG | yes |
| `1111nnnn01011101` | FABS | yes |
| `1111nnnn01101101` | FSQRT | yes |
| `1111nnnn01111101` | **FSRRA** | **absent** |

So a guest executing `0xF?7D` on a modelled SH7750 gets FSRRA semantics where real silicon
would raise an illegal-instruction exception. That is guest-visible divergence in the
*detection* of illegal instructions.

**Severity is honestly low and stated as such:** no in-tree guest is known to execute either
encoding, so nothing observed is wrong today. This is a fidelity gap, not a live defect, and
it is filed rather than fixed because the fix is a design question — gate the decode on
`cpu_type.arch`, or add an SH-4A type, or decide the tree deliberately models a superset and
say so where a reader will find it. **Deciding needs a round; the evidence is already here.**

Unmeasured and named as such: whether a witness is constructible. It would need the illegal
-instruction path to be observable, which is a different oracle from every SH probe here.

### `sh4fmtcast` — open, a class, not yet started

`dev_sh4.c` passes an `(int)`-cast argument to an `%x`-family conversion at **eighteen**
call sites. `%x` requires `unsigned int`; passing `int` is a varargs type mismatch. Found
by a pass-2 seat on `#452`'s two new sites, then grepped for siblings per the standing
rule — and the siblings are the point:

```
:413 :648 :649 :650 :651 :733 :766 :957 :1129 :1448 :1453 :1914 :2205 :2286 :2576 :2593
:2602 :2605
```

Most predate this project's work (`:648`-`:651`, `:1448`, `:1453`, `:2205`, `:2593`,
`:2602`, `:2605` are upstream or early). `fatal()` is declared `void fatal(const char *fmt,
...)` in `misc.h:262` with **no format attribute**, so no compiler warns and the build is
clean at zero warnings.

**Filed as a class rather than fixed in-round, on the `#450` precedent.** That round found
fourteen `buf[3] << 24` sites, four already cast correctly, and did all ten remaining
*together* — because fixing a subset of an idiom leaves the file inconsistent and the next
reader unable to tell which spelling is intended. Fixing 2 of 18 here would be exactly that
half-fix.

Nothing observable is at stake on any ABI this tree builds for — `int` and `unsigned int`
are the same width and pass identically — so this is correctness-by-the-standard, not a
measurable defect. It needs no witness; it needs one mechanical sweep and a census row.

### `sh4pclock` — *** CLOSED, shipped as `0bb8be2 2965aa1`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

*** A GUEST STORE ENDS THE HOST ON `hpcsh`, AND THE SITE READS LIKE IT CANNOT BE REACHED. ***
`dev_sh4.c:1813-1817`, in the `SH4_TCR0` write handler:

```c
			if (cpu->cd.sh.pclock == 0) {
				fatal("INTERNAL ERROR: pclock must be set"
				    " for this machine. Aborting.\n");
				exit(1);
			}
```

"INTERNAL ERROR ... Aborting" is the wording of a construction fault, and that is why this
site survived four rounds of SH-4 `exit(1)` work — it does not look guest-drivable. It is.

**The chain, all four links checked:**

1. `cpu_sh.c:200` adds the device from the **CPU**, not from any machine:
   `if (cpu->cd.sh.cpu_type.arch == 4) cpu->cd.sh.pcic_pcibus = device_add(machine, "sh4");`
   — unconditional for every SH-4, so the TCR handler exists on every SH-4 machine.
2. Only **two** machines ever assign `pclock`: `machine_dreamcast.c:51` (50000000) and
   `machine_landisk.c:81` (33333333). A tree-wide grep finds no third.
3. `machine_hpcsh.c` sets `machine->cpu_name = strdup("SH7750")` at `:89`, and `SH7750` is
   **arch 4** (`cpu_sh.h:63`). So hpcsh constructs an SH-4, gets the device, and never sets
   `pclock`.
4. MEASURED, one guest instruction, on an unmodified `-e jornada680`:

```
GXemul> r1=0xffd80010          <- SH4_TCR0, sh4_tmureg.h:54
GXemul> r0=1
GXemul> put w 0x8c010000, 0x00092102
GXemul> pc=0x8c010000
GXemul> step 2
8c010000:  2102        mov.l	r0,@r1	; r1 = 0xffd80010
INTERNAL ERROR: pclock must be set for this machine. Aborting.
```

Both hpcsh subtypes are affected (`jornada680`, `jornada690`) — the `pclock` assignment is
absent from the whole file, not from one subtype.

**This is NOT a sibling of `sh4tlbda2` and must not be folded into that round.** Different
semantic class: `da2` is a device answering for an address range it cannot service, fixed by
declining the access; this is a machine constructing a device without a parameter the device
requires. It also needs a different oracle — `-e jornada680` rather than `-E landisk` — so it
fails the reopening rule on both arms.

**The fix is a design question, not an obvious edit,** which is why this is filed rather than
done: setting `pclock` in `machine_hpcsh.c` invents a clock rate for hardware nobody here has
documentation for (there is no usable SH-4 manual in this tree, and the Jornada's actual
peripheral clock is not derivable from the source). Declining the TCR write instead keeps the
model honest but silently changes timer behaviour. The panel should choose.

**THREE machines are affected, not one — `testsh` reproduces as well.** `machine_test.c:512`
also names `SH7750` and `default_test()` never assigns `pclock`. That matters more than one
more machine: `testsh` is a machine THIS HARNESS drives, so the defect sits inside the
project's own test surface.

```
GXemul> pc=0x80010000
GXemul> step 2
80010000:  2102        mov.l	r0,@r1	; r1 = 0xffd80010
INTERNAL ERROR: pclock must be set for this machine. Aborting.
```

*** THE FIRST testsh ATTEMPT WAS VOID AND IS RECORDED HERE BECAUSE IT NEARLY READ AS A
CLEAN RESULT. *** It reused landisk's scratch address `0x8c010000`; testsh has its RAM at
`0x00000000`, so the emulator answered `memory READ: from non-existant paddr=0x0c010000` and
the store never executed. Nothing died, and "testsh does not reproduce" would have been the
obvious and wrong conclusion. Rule 4 — *did it fail for the reason under test?* — is what
caught it; the retry at `0x80010000` and at `0x00010000` both reproduce.

**And the CONTROL is what makes the attribution sound:** the identical store on `-E landisk`,
which does set `pclock`, prints `[ sh4 timer 0 clock set to 2083333.312500 Hz ]` and runs on.
Same instruction, same address, same width — only the machine differs.

### `sh4valrows` — held

*** Nine measured mutants score 33/33 against `#447`'s shipped detector, seven of them real
defects. *** Filed rather than fixed in-round for a stated reason: this detector is **weak, not
vacuous** — it kills 25 of 33 rows on the pre-fix build and kills six real mutants. That is
categorically unlike `#446`'s detector, which a 217-byte comment-only file passed and which was
therefore replaced in-round.

**Four structural holes, and they are a product rather than a list:**

| hole | what it is | mutants |
|---|---|---|
| H1 | state is read back at **instance 0 only** — V11/V12 walk the others but only *count* lines | M23, M24, Mbrk |
| H2 | read back on a **first offence only**, except at RCR1 | M21, M22 |
| H3 | masks are pinned only **from below** — V28 proves six bits are IN, nothing proves others are OUT | M20, M20b, M25, Mdma |
| H4 | width × instance is a **product**; the census covers only the diagonal | M33 |

The two that matter most:

- **`M20` — one identifier.** Adding `| TCR_UNIE` to `TCR_UNIMPLEMENTED`. On the fix, `TCR0=0x0022`
  reads back `0x22` with a clock line at `520833.328125 Hz`; with M20 it reads back `0x00000000`
  and there is **no clock line**. `TCR_UNIE` is modelled, so the guest can never enable the timer
  interrupt.
- **`M33` — a guest-reachable host death that scores full marks.**
  `if (timer_nr == 2 && len == 4) exit(1);`. A `mov.l` to TCR2 gives `alive=False`. It survives at
  len 2 — the only width V11 issues — which is *precisely why* it scores 33/33.

*** The fix changed H3's failure mode from loud to silent, and that is the finding inside the
finding. *** Pre-`#447`, a widened mask meant `exit(1)` on a legal write — unmissable. Post-`#447`
it means a silently refused write. The round improved the failure and degraded its own
detectability in the same edit.

**One question is open rather than confirmed.** V28 writes all six unimplemented TCR bits *as a
union* (`0x02dc`). Delete one bit and the union still trips on the other five, so V28 stays green
while a **singleton** write of the deleted bit reaches the prescaler and the store. The seat that
raised it was explicit that it could not confirm the score — it needs the fourteen
mask-minus-one-bit mutants run. Note this is a **different test** from H3-from-above: one requires
a *modelled* bit to be accepted, the other requires each unimplemented bit to be rejected *alone*,
and they fail to different mutants.

*** A process note worth more than the rows: the probe refused to pass in a half-edited state. ***
An attempt at this work died mid-edit having bumped `EXPECT_ROWS` to 43 and registered three new
opcodes without writing the rows that plant them. The probe reported `31/33 FAIL` through **two
independent rows** — V31 caught the row-count intent, V30 caught the opcode intent. The tree was
restored to a verified 33/33 rather than left broken.

## 2026-08-21 — #448 shipped, and reviewing it found two more things in the same function

### `sh4dmacintr` — open, filed by #453 with everything the round needs

*** THE SH-4 DMAC CANNOT DELIVER A TRANSFER-END INTERRUPT AT ALL, AND
`sh4_exception.h` DEFINES NO DMAC VECTOR. *** Split out of `#453` deliberately, on an
argument two review seats made independently, and filed with the facts so the round does not
have to re-derive them.

**The manual's codes** (SH7750 Hardware Manual, interrupt table):

| source | meaning | INTEVT |
|---|---|---|
| DMTE0 | CH0 transfer-end interrupt | `H'640` |
| DMTE1 | CH1 transfer-end interrupt | `H'660` |
| DMTE2 | CH2 transfer-end interrupt | `H'680` |
| DMTE3 | CH3 transfer-end interrupt | `H'6A0` |
| DMTE4..7 | CH4..7 transfer-end | `H'780/7A0/7C0/7E0` |
| DMAE | Address error interrupt | `H'6C0` |

> "Note: DMTE4–DMTE7: These codes are not used in the SH7750 or SH7750S."

**The rule to implement**, verbatim: *"Bit 1 — Transfer End (TE): This bit is set to 1 after
the number of transfers specified in DMATCR. If the IE bit is set to 1 at this time, an
interrupt request (DMTE) is generated."*

**Why it was NOT done in `#453`.** The helper's only consumer would be `dev_pvr.c:300` — the
Dreamcast PVR DMA, which already sets `CHCR_TE` by hand and carries its own
`// TODO: _EXACTLY_ what happens at the end of a transfer?`. That is a **different device**,
which the reopening rule excludes. Two seats put it the same way: *if the infrastructure's
only consumer is out of scope, the infrastructure is out of scope too, or it ships as dead
code to satisfy a completeness instinct.*

**Resolutions already settled by the pass-1 panel, so the round need not re-argue them:**

* **Look up four lines, indexed 0–3.** Do not alias channels 4–7 to another DMTE code or to
  DMAE — DMAE has a different meaning. Use an explicit implemented-channel count rather than
  assuming `N_SH4_DMA_CHANNELS` (which is 8, "4 on 7750, 8 on 7760") equals the interrupt
  count. If a completion path meets an IRQ-unmapped channel, bounds-check, leave the line
  inactive, and emit a latched modelling-gap diagnostic rather than fabricating a code.
* **DMTE4–7 only with a CPU subtype whose manuals establish them.** The obtained manual does
  not establish channel capabilities for every modelled SH7750R/SH7751R variant.
* **An `IE` snapshot taken at function entry is NOT equivalent to `IE` at completion** for an
  asynchronous external transfer. A completion helper must inspect live CHCR state — a seat
  named this and it is easy to get wrong.
* **Deassert-on-TE-clear is plausible but NOT established** by the quoted text; interrupt-line
  lifetime when `IE` is cleared or changed after completion needs settling in that round.

**Related and separate:** the guest `CHCR` write is a plain assignment
(`cpu->cd.sh.dmac_chcr[dma_channel] = idata;`), so a guest can set `TE` to 1 directly, which
the manual forbids — *"The TE bit can only be written with 0 after being read as 1, to clear
the flag."* A seat noted that enforcing this is more than masking a written 1: "read 1 before
write 0" needs per-channel read-observed state. **Filed as `sh4tewrite`, its own defect with
its own witness.**

### `sh4dmacie` — FIXED by #453 (kept for the record)

*** `CHCR_IE` on the one **accepted** resource select still ends the host, and `#448`
deliberately left it. *** MEASURED: a guest `mov.l` of `0x00000205` to CHCR0
(`RS=0x200 | IE | TD`) dies at the `if (cause_interrupt)` arm. Its control survives — the same
store **without IE** (`0x00000201`) leaves the host alive — so the kill is attributable to `IE`
and not to the transfer.

**And the reachability is now EXHAUSTIVE rather than sampled.** All sixteen RS encodings were
driven with `IE | TD` set, on the shipped binary, one guest store each:

```
  RS  chcr      alive  what came out
   0  00000005  True   declined at the RS switch (latched diagnostic)
   1  00000105  True   declined at the RS switch
   2  00000205  False  *** REACHED THE INTERRUPT SITE ***
   3..15        True   declined at the RS switch
```

Exactly one of sixteen reaches the site, and it is the one the model ACCEPTS. That confirms by
measurement what was previously a reading of the `switch`, and it is the fact the fix design
turns on: **the only arm that reaches `if (cause_interrupt)` is `case 0x200:`, which performs
no transfer at all** — *"Note: No transfer is done here! It is up to the external device to do
the transfer itself!"* So at the `exit(1)`, DMATCR's count has not been consumed, while the
manual conditions DMTE on exactly that count completing.

**Two pass-1 seats independently ruled it out of `#448`, on the round rule rather than on
convenience.** The other four sites are unimplemented **encodings**, where declining is correct.
This is a **legal request** — `RS=0x200` is the one configuration the model accepts — asking for a
notification the model has not implemented. Declining it isn't correct behaviour; it's a different
unimplemented feature, with interrupt delivery as its oracle rather than absence-of-transfer.
*"The same five `exit(1)`s" is a symptom class, not a semantic class.*

*** The exclusion was PINNED, not merely stated: *** `sh4_chcr_probe.py` row **X1 required this
site to still be fatal**, so the day it was repaired the gate reddened and named this row. A scope
decision no row asserts is indistinguishable from an oversight.

**AND THAT IS EXACTLY HOW IT PLAYED OUT.** `#453` landed, X1 went red, and its own message said
what to do: *"delete the row rather than the fix"*. Five rows replaced it. The pin did the job it
was built for — the repair could not land silently.

**FIXED by `#453`:** the diagnostic is latched and the `exit(1)` is gone, and the interrupt is
deliberately NOT generated, because the only arm reaching the site performs no transfer and the
manual conditions DMTE on the transfer having happened. The deferred interrupt infrastructure is
filed as `sh4dmacintr` above.

One honest trade, named by a pass-1 seat: pre-fix the host dies before any driver can wait;
post-fix an interrupt-driven driver could wait forever. Better for the host, and a real change —
which is why raising a *fake* interrupt was explicitly rejected as out of scope.

### `sh4dmanop` — held

*** The function called `sh4_dmac_transfer()` does not transfer. *** Found while settling a
pass-1 seat's question about body ordering — and it refuted the question rather than answering it.

`sar`, `dar`, `count` and `chcr` are **local copies**; there is no `cpu->cd.sh.dmac_*` assignment
anywhere in the function; and the only arm that returns normally, `case 0x200:`, is literally
`(void)sar; (void)dar;` under the comment *"Note: No transfer is done here! It is up to the
external device to do the transfer itself!"*. No bytes move, SAR/DAR/DMATCR are never advanced,
and TE is never set.

Two consequences, and the second is why this is filed rather than shrugged at:

1. It made `#448` trivially safe — every site is side-effect-free before it dies, so there is
   nothing to un-commit and no store had to move.
2. *** A guest that enables DMA and polls for completion already waits forever, on the one
   configuration the model accepts, before and after `#448` alike. *** Two pass-1 seats raised
   that hang as something `#448` might **create**; measurement shows it **pre-exists**, and the
   round neither causes nor worsens it.

**Honest limit: READ, not executed.** No guest here has been observed waiting — landisk's kernel
may never enable a DMA channel at all. Whether any guest this project boots reaches it is
unmeasured, so this is a capability gap of unknown reachability rather than a witnessed defect.

## 2026-08-21 — #449 shipped, and its pass 2 found a defect in the brief rather than the code

### `sh4rtcflags` — held

RTCSR's **CMF and OVF are never set on any path**, and **RTCNT (`0xff800020`) has no `case`** in
the device at all. The tick increments `bsc_rfcr` and stores CKS/LMTS/RTCOR without consulting
them. So a guest polling for a refresh compare-match waits forever.

*** `#449` does not make this worse and deliberately does not fix it. *** A guest polling CMF
already waits forever with the enables **clear**; `#449` only stops the host dying, so a guest
with them **set** now survives to wait the same way. Setting CMF as a consolation would be
inventing a compare-match with no RTCNT to match against — a pass-1 seat argued that explicitly.

Honest limit: **READ, not executed.** Whether any guest this project boots ever polls CMF is
unmeasured.

### `sh4latchcollide` — held

A pass-2 seat named the smallest undetected mutation: swap `#449`'s latch class from
`SH4_VAL_RTCSRINT` to `SH4_VAL_RCR1INT`. It **conditioned the claim correctly** — it matters
only if an earlier RCR1 complaint with an *overlapping bit* suppressed the RTCSR one.

MEASURED: the mutant scores 10/10. But the bit sets are **disjoint** — RCR1 `CIE|AIE = 0x18`,
RTCSR `CMIE|OVIE = 0x42` — and `sh4_val_first` keys on **bits**, so a shared class slot cannot
suppress anything. *** The mutant is EQUIVALENT, not surviving, and that is a different
diagnosis from "the detector is weak". ***

**The fragility is what is worth keeping.** Nine classes now share one `val_reported[cls][inst]`
array, and the correctness of every class assignment is guaranteed by nothing except that no two
classes' bit sets overlap. Renumber one header constant, or add a tenth class sharing bits with
an existing one, and a wrong assignment becomes a **silent suppression of a real diagnostic** —
with no row able to see it, because while the sets stay disjoint there is nothing observable to
assert.

Candidates for a round to weigh: a compile-time assertion that the class bit-domains are
disjoint; or making the class a property of the register rather than a hand-written argument at
each call site.

## 2026-08-21 — #450 shipped the shift-UB class; reviewing it found the walker reads the wrong field

### `arcbioswalk64` — held

*** The 64-bit component walker reads `peeraddr + 0x34` for "IdentifierLength", and that offset
is a slice of AffinityMask. ***  In-RAM layout: a 0x18-byte pointer header
(`ptr_peer/ptr_child/ptr_parent`) then `arcbios_component64` — Class `+0x18`, Key `+0x28`,
**AffinityMask `+0x30`**, ConfigurationDataSize `+0x38`, **IdentifierLength `+0x40`**,
Identifier `+0x48`, total `0x50` — which is exactly the walker's own step, corroborating the
arithmetic. The walker masks the mis-read with `0xfffff` and skips accordingly; with
AffinityMask `0xffffffff` that is a **~1 MiB skip per node**, so the walk leaves the component
list after the first node.

**One-way coupling, recorded before anyone trips it:** `#450`'s mis-link hazard at `:751` is a
counterfactual *partly because this bug keeps the walk from ever reaching a node that would
exercise it*. Fixing this row may make that site live — the `ctorabortclass` shape again.

**Honest limit: layout arithmetic, not execution.** And the 32-bit walker's offsets (`+0x28`
read, `+0x30` step) should be checked in the same round rather than trusted by symmetry.

## 2026-08-23 — #458 shipped the IPR table; its sibling is one line past the loop bound

### `sh4pcic15` — open

*** PCIC interrupt line 15 can never be delivered, and the obvious fix is a NO-OP. ***

`dev_sh4.c:73` sets `N_PCIC_IRQS 16`, and `:2822-2836` wires every one of them:
`SH4_INTEVT_IRQ0 + 0x20 * i` for `i` in `0..15`. With `SH4_INTEVT_IRQ0 = 0x200`
(`sh4_exception.h:142`) line 15 lands on **`0x3e0`**, which the header names
`SH4_INTEVT_IRQ15` at `:157`.

The priority loop stops one slot short — `cpu_sh.c:352`, `i <= SH4_INTEVT_IRQ14` (`0x3c0`).
So slot `0x3e0` keeps priority 0 for the life of the machine. Same class as `#456`, which
established that this loop never assigns that slot; different device reaching it.

**Why extending the bound fixes nothing.** The loop body is
`prio = 15 - ((i - SH4_INTEVT_IRQ0) / 0x20)`, so it hands IRQ0 priority 15 and walks down to
IRQ14 at priority 1. Feed it IRQ15 and the arithmetic yields **priority 0** — exactly the
state the line is already in. *The bound is not an off-by-one; it is the point at which this
formula runs out of nonzero priorities.* A round here has to decide what IRQ15's priority
ought to BE, which is a hardware question, not an arithmetic one.

**And `#455` changed the symptom class.** Before it, an assert on a priority-0 line ran
`fatal()` then `exit(1)` — this line was a guest-reachable host kill. After it, the assert
returns early and the interrupt is **silently dropped**. That is the de-escalation clause's
own hazard arriving on schedule: the fix was right, and it removed the noise that would have
announced this line. Recorded here so the trade is visible rather than inferred.

**Honest limit: NOT witnessed.** This is header-and-loop-bound arithmetic, three files read
directly. No probe has driven a PCIC line 15 assert, and whether any guest in `_images/` ever
raises one is unmeasured. It is eligible for a round only once someone builds that witness —
`dev_sh4.c`'s `sh4_pcic_interrupt_assert` is the entry point to aim at.

### `sh4iprunpinned` — open (coverage debt from #458)

*** FIVE SEATS INDEPENDENTLY FOUND THE SAME ESCAPE CLASS, AND IT IS A REAL LIMIT ON WHAT
`sh_iprbcd_probe.py` CAN SEE. *** Filed, not fixed: `#447`'s precedent governs — these are
hypothetical edits in uncovered product cells against a detector measured ABOVE the vacuity
floor, which is coverage debt, and the round's ask-again is capped at one finding.

`#458` maps every Table 19.6 source, but only three slots are ever READ by a row —
`iprio_560` (WDT), `iprio_480` (RTC ATI) and, from the ask-again, `iprio_240` (IRQ2/IRL0).
Delete any single mapping line for a slot no row reads and the detector scores full marks:

| escape | what it leaves wrong | named by |
|---|---|---|
| drop `SH_INTEVT_HUDI` | H-UDI (`0x600`) stuck at 0 | grok, glm |
| drop `SH_INTEVT_GPIOI` | GPIO (`0x620`) stuck at 0 | deepseek, agy |
| drop `RTC_PRI` / `RTC_CUI` | `0x4a0`/`0x4c0` stuck at 0; `ipra rtc` reads only ATI | minimax, agy |
| drop the `REF` pair | `0x580`/`0x5a0` stuck at 0; `iprb wdt` reads only WDT | agy |
| drop the DMAC loop | DMTE0..DMAE (`0x640`-`0x6c0`) all 0 | minimax |
| drop the SCI loop | SCI ERI/RXI/TXI/TEI (`0x4e0`-`0x540`) all 0 | minimax, codex |
| `i<=SH_INTEVT_SCI_TEI` -> `i<` | SCI TEI (`0x540`) alone | codex |
| map only `SCIF_TXI` | ERI/RXI/BRI untested; the probe drives TXI only | grok |

**The root cause is structural, not sloppiness.** None of those sources has an
`INTERRUPT_ASSERT` anywhere in this tree, so no behavioural row can reach them; and the
probe reads the table only where a row was written to. The general fix is one of:

* a **table-driven row** that writes each IPR to a distinct pattern and checks EVERY slot
  Table 19.6 assigns — one session, ~30 reads, and it subsumes every line above; or
* a debugger **interrupt-inject** command (`INTERRUPT_ASSERT` by name on
  `machine[0].cpu[0].irq[0x560]`, which `cpu_sh.c:210-223` already registers), which would
  promote these from table reads to real delivery rows. **grok notes this makes the probe's
  "no behavioural test can ever replace these" claim too strong** — it is true only of the
  Python probe as it stands, because no such command exists today.

The first is cheap and should come first. The second is the one that does not rot.

### `sh4standinglower` — open (predicted, NOT measured)

grok's third mutant: guard the new rescan as `if (cpu->cd.sh.int_to_assert == 0)
sh_recalc_int_to_assert(cpu);`. Predicted 12/12, because `raise` asserts at priority 0 so
the guard still fires, `lower` writes both IPR values BEFORE asserting, and `deassert` uses
the other path entirely. The guest-visible miss: assert SCIF at 15, then `IPRC[7:4] := 1`
with IMASK=1 — hardware must drop it, the mutant keeps a stale level 15. **The kill row is
one line**: `run_deliver(0x00f0, 1, raise_iprc(0x0010))` wanting `refused`. Standing-LOWER,
which no current row performs. Reading, not measurement — grok said so itself.

### `sh4irlm` — open

`dev_sh4.c:2376-2382` refuses ICR IRLM=1 outright. `#458` links the two decisions in a
comment because they are one decision: implementing IRLM=1 makes declining IPRD wrong on
the same day, and would need IPRD applied *gated on the live IRLM bit* with an explicit
policy for the IRQ2/5/8/11 aliasing. Note the chip scope while doing it — IPRD is
**SH7750S/SH7750R only** (Rev.7.00 note 3, `:39881` and `:40247`), and
`machine_dreamcast.c:165` asks for plain `SH7750`, where the register does not exist.

**Escape list addendum (pass 2, fable5):** a mutant of a DIFFERENT SHAPE from the
boundary-drops above — **transpose the GPIO and H-UDI nibbles** in the IPRC block, so
`GPIOI` takes `intc_iprc & 0xf` and `HUDI` takes `(intc_iprc >> 12) & 0xf`. Predicted to
pass all **14** rows: the table-reading rows touch only slots `0x560/0x480/0x240/0x340`,
nothing in the tree asserts GPIO or H-UDI, and the ten behavioural rows drive SCIF[7:4],
which a 15:12-with-3:0 swap does not reach. *It is the exact defect class `#458` corrects
— a wrong Table 19.6 nibble mapping in the very register whose SCIF nibble the round fixes
— but a wrong-DESTINATION rather than a dropped-source.* Same family: `<=SH_INTEVT_DMAE`
-> `<` (drops DMAE `0x6c0`), and deleting the `TMU2_TICPI2` line (`0x460`).

Two settings rows pinning `iprio_620` and `iprio_600` would close the IPRC family cheaply.
Filing-grade under the stopping rule: the ask-again cap for this detector is spent.

**Escape list addendum 2 (pass 2, opus5):** the DMAC loop stops at `DMAE` (`0x6c0`), omitting
**DMTE4-7** (`H'780`-`H'7E0`, also IPRC[11:8]), which exist on SH7750R/SH7751R — the type
landisk actually runs. Nothing asserts them, so it needs its own row rather than a silent
loop extension. Same file, same register, different completion question from `sh4irlm`.

## 2026-08-23 — #459 closed the last guest-reachable host kill in dev_sh4.c; four rows filed

### `sh4testclock` — open

`baresh` and `testsh` have no `pclock`, so the harness cannot test the TMU path `#459` just
de-fatalised. Held out of that round as a CAPABILITY change in a different file and semantic
class — two seats proposed it, two refused the merge. **The argument for:** they are
SYNTHETIC machines, so their parameters are the project's own *definition*, not a hardware
*fact*; assigning a clock invents nothing. **The argument against, and any round here must
answer it:** testsh's value today is precisely as the regression case for "an arch-4 CPU
whose board omitted pclock", so giving it a clock deletes the only test of the missing-clock
path. **Keep one machine clockless and say which.** A seat measured `2^25 = 33554432`
working — every TMU prescaler divides it exactly, and nobody will mistake it for a Jornada
measurement.

### `sh4cpudevscope` — open

*** The CLASS `#459` is an instance of. *** `cpu_sh.c:233-234` calls
`device_add(machine, "sh4")` from inside the CPU constructor, so a **machine-scoped device is
created once per CPU**. Three measured symptoms:

1. `sh4pclock` — the CPU brings the TMU and the board brings the clock. Closed at the guard.
2. **`-n 2 -E landisk` refuses to construct**: `ERROR! "sh4" collides with device 11 ("sh4")`.
   SMP is impossible on every SH machine, and this line is why.
3. `dev_sh4.c` hardcodes `machine[0].cpu[0].irq[...]` for the TMU interrupt lookup (the
   three `interrupt_handler_lookup` failures near the end of `devinit`; line numbers are
   omitted because same-file comment edits move them -- see the `#459` round block)
   — correct *only because* symptom 2 makes a second CPU impossible.

Fixing 2 without 3 gives a device on CPU 1 whose timer interrupts route to CPU 0.

### `sh4frqcr` — open

`dev_sh4.c`'s `case SH4_CPG_FRQCR` models it as a bare latch with **no reset value** --
`cpg_frqcr` is never initialised, so a guest reads
`0x0000` — not a legal value. Table 10.3 gives `H'0E1A`/`H'0E23`/`H'0E13`/`H'0E0A` by clock
mode. **This is the honest long-run answer to `sh4pclock`:** real hardware derives the
peripheral clock from FRQCR and the mode pins, and a seat measured that the CPU:peripheral
ratio there is only ever 4 or 6 — calibrated against dreamcast's 200/50 = 4, a legal mode this
tree independently knows. Note the bound alone is not enough: `machine_hpcsh.c` sets no
`emulated_hz`, so there is no CPU clock to divide.

### `hpcshcpu` — open

**The repo contradicts itself.** `doc/TODO.html:322-323` lists *"SH3-specific devices: Pretty
much everything!"* immediately followed by *"NetBSD/evbsh3, hpcsh!"*, grouping hpcsh with an
SH3 target; `machine_hpcsh.c:89` names SH7750, arch 4. **Two seats independently refused to
settle it from memory** — which is the `#357`/`#362`/`#365` citation failure *not* repeating.
There is no SH-3 manual in `_scratchpad`, hpcsh's platid block is entirely commented out,
`HISTORY` never mentions it, and `vripreg.h` — included by `machine_hpcsh.c` — is NEC VR41xx
**MIPS**, a copy-paste leftover from hpcmips.

If it is ever settled as SH-3, note what arch-3 removes: the whole `dev_sh4` block
(CCN/MMU, INTC, TMU, RTC, BSC, DMAC, SCIF, TLB arrays, PCIC); both SH-3 interrupt handlers
are `/* TODO */` stubs at `cpu_sh.c:527-533` that silently drop asserts; and `cpu_sh.c:224`
uses a **leftover UTLB loop counter** as `templ.line`, latent today only because that handler
is a stub. Obtain a source first.

### `sh4pclockstatic` — open (ask-again escape, #459)

codex's capped ask-again named a mutant that passes **all 16 rows**: replace `sh4_val_first()`
in the pclock guard with a function-static per-timer bitmap.

```c
static unsigned pclock_reported;
unsigned bit = 1U << timer_nr;
if (!(pclock_reported & bit)) { pclock_reported |= bit; fatal(/* unchanged */); }
break;
```

It preserves decline, `unlatch`, `once` and `pertmr` for a single device, so every row stays
green — but it suppresses TCR0's diagnostic on a **second** SH4 device in the same process.
The kill is two device instances and one TCR0 write to each, expecting two diagnostics.

**FILED, not fixed, and it is currently EQUIVALENT IN PRACTICE** — `sh4cpudevscope`'s `-n 2`
collision means a second SH4 device cannot be constructed today, so no probe can build the
kill. *That is the argument for `sh4cpudevscope` rather than a reason to dismiss this:* the
moment that collision is fixed, this mutant becomes live and the row becomes buildable. The
two should be done in that order.

### A METHODOLOGY FINDING worth more than any of the above

*** A COMMENT THAT CITES LINE NUMBERS IN ITS OWN FILE INVALIDATES THEM EACH TIME IT IS
EDITED, AND `#459` DID EXACTLY THAT TO ITSELF. ***

The round enumerated the four remaining `exit(1);` sites in `dev_sh4.c` to support its claim
of having closed the last guest-reachable one. Measured by a pass-2 seat:

| tree | sites |
|---|---|
| pre-fix (`bb05ce7`) | `:1972` (removed), `:2710`, `:2885`, `:2891`, `:2897` |
| shipped (`0bb8be2`) | `:2786`, `:2961`, `:2967`, `:2973` |
| **cited** | `:2772`, `:2947`, `:2953`, `:2959` |

The cited set matches **no committed tree** — it is an intermediate working state, and the
15-line paragraph correcting the false panel claim is the late addition of exactly that size.
**The correction invalidated the enumeration, and nobody re-derived it.** The same `+62`
contamination reached `sh4cpudevscope`, and `sh4frqcr` cited a location its own commit had
already moved — *a queue row born stale by the diff that filed it*.

The substance was true throughout. **Line numbers are now omitted from these records in
favour of structural descriptions** ("one wrapped in `#ifdef SH4_DEBUG`, three on
`interrupt_handler_lookup` construction failures"), which cannot rot. Cite line numbers across
files, never within one.

### `sh4pclockquiet` — open (five ask-again escapes, #459 pass 2, all MEASURED)

A measuring seat built six mutants of `#459`'s guard and **five scored 16/16**. Filed as
coverage debt — the detector is above the vacuity floor (6/16 pre-fix; that *is* the verbatim
reinstatement, one site; `live`/`devsig` are real identity rows) — but the family has a single
root cause worth naming.

| mutant | one-line change | what no row sees |
|---|---|---|
| **`m_unie`** | `pclock == 0 && !(idata & TCR_UNIE)` | `TCR0 <- 0x0020` on jornada680: read-back `0x20`, the write LANDS, `clock set to 0.000000 Hz`, **zero** diagnostics |
| `m_below_switch` | guard moved verbatim below the `debug()` line | 4 stores → **4** `clock set to 0.000000 Hz` lines (fix: 0) |
| `m_valkey` | key `1` → `idata ? idata : 1u` | 4 different values to TCR0 → **3** lines (fix: 1) |
| `m_tmr2` | `&& timer_nr != 2` | TCR2 silently accepted, 0 Hz installed, no diagnostic |
| `m_wrongnr` | `fatal(…, timer_nr)` → `fatal(…, 0)` | every line says "timer 0" |
| `m_valnarrow` | `&& (idata & 3) == 0` | **KILLED 15/16** by `unlatch` |

*** THE ROOT CAUSE: the declining-write value set is exactly `{0x0000, 0x0001}`. *** The three
`kill` rows and `says`/`once`/`pertmr` all write `0x0000`; `unlatch` writes `TCR_TPSC_P16`.
**Any narrowing predicate that admits both escapes.** `m_valnarrow`'s death is the detector's
real strength here and shows what fixes the family: a *second distinct value*.

**`m_unie` is the one that reaches live functionality**, and it is the realistic narrowing —
"if the guest isn't asking for an interrupt, refusing is fine; if it is, let the register latch
so read-back works". It lands a TCR with `timer_hz == 0` for **exactly the value a guest must
write to use a TMU at all**, while going *quieter* than the fix.

**Four of the five rows cost ZERO extra sessions**, which is why this should be a short round:
assert `clock set to` appears zero times in the existing `says` session (kills
`m_below_switch`); capture the timer number from the diagnostic and check it is `["0"]` /
`["0","1"]` (kills `m_wrongnr`); extend `pertmr` to TCR0/1/2 expecting **3** (kills `m_tmr2`);
give `tcr_writes` a per-write value list so `once` stores two *different* values and still
expects 1 (kills `m_valkey`). Only `unlatch2` at `TCR_UNIE|TCR_TPSC_P4` needs a new session,
and it kills `m_unie` and the rest of the narrowing family.

*Related record defect, already corrected:* the CHANGELOG cited "measured `0x0` versus `0x20`"
for the read-back, but **no shipped row writes `0x20`** — `unlatch` and `accept tcr` both use
`TCR_TPSC_P16` (`0x0001`). Adding `unlatch2` makes that citation true.

*Probe hygiene, same seat:* `dumped()` is dead (never called), and `CODE["landisk"]` /
`CODE["dreamcast"]` duplicate `LANDISK_CODE`/`DREAMCAST_CODE` — the same "dead weight that
reads like coverage" the `SCRATCH` comment two lines below records a seat already pruning.

### `sh4gdromexit` — *** CLOSED, shipped as `98a3408 16f06a0`.  This heading said `open`. ***

*Heading corrected 2026-08-23 in a sweep: **six** headings in this file said `open` on
work the ledger recorded as closed.  The carrier's first-stop procedure reads THIS FILE
as the live queue, so each one presented shipped work as available.  The body below is
the original and is left as written.*

`#459` closed the last guest-reachable `exit(` in `dev_sh4.c`. **The SH surface as a whole is
not clear.** Census of *code* exits — excluding `#ifdef` blocks and construction-time
failures:

| file | live exits |
|---|---|
| `dev_dreamcast_gdrom.c` | **14** |
| `dev_dreamcast_g2.c` | 6 |
| `dev_dreamcast_maple.c` | 3 |
| `dev_dreamcast_asic.c` | 1 |
| `cpu_sh_instr.c` | 2 |
| `cpu_sh.c` | 1 (`sh_exception`) |

*** COUNT CODE, NOT TEXT. *** `grep -c 'exit(1)'` scores `dev_sh4.c` at **21** and the truth
is **0** — this tree's hardened comments discuss `exit(1)` constantly, and `#459`'s own
comment mentions it four times. A census that does not strip comments ranks the *best*
documented file as the worst.

**The GDROM ones are the most guest-reachable in the tree.** `handle_command()` switches on
`d->cmd[0]`, a byte the guest writes, and its arms call `exit(1)` on an unimplemented command,
on a Read-TOC length that is not 408, and on a data format that is not `0x20` — each an
ordinary guest-supplied value, no privilege or unusual state required.

**The witness shape is already proven** by `#459`: a rung-3 cold-debugger probe on
`-E dreamcast -x`. The `-x` is *required* — Dreamcast brings up two console inputs and
`console.c:994-1007` makes that fatal without it, which is the false-positive that nearly
cost `#459` a fourth machine. **Not yet witnessed:** no dreamcast image exists in `_images/`,
so the probe must drive the GDROM registers by planted guest stores rather than by booting.

### `gdromoob` — ASSESSED, NOT A DEFECT (2026-08-23, during `sh4gdromexit` pass 1)

Recorded so nobody re-raises it. The GDROM read path at `:318-320` looks like a heap
over-read:

```c
if (d->cur_data_offset < d->data_len) {
        odata  =  d->data[d->cur_data_offset ++];
        odata |= (d->data[d->cur_data_offset ++] << 8);   /* second increment */
```

**The bound is checked once and the index advances twice.** At `cur_data_offset ==
data_len - 1` the check passes and the second read is `d->data[data_len]` — one byte past a
`malloc(data_len)` buffer. And `data_len` comes straight from `d->cnt` (`alloc_data`, `:89`),
which is **fully guest-settable**: `GDROM_CNTLO` at `:393` and `GDROM_CNTHI` at `:401` let a
guest write any 16-bit value.

**It is not reachable, because both `alloc_data` call sites force an EVEN count:**

* `:120` — Read TOC requires `d->cnt == 408` exactly, or it faults first.
* `:194` — the sector read requires `sector_count * 2048 == d->cnt`, so `cnt` is a multiple
  of 2048.

With `data_len` even and `cur_data_offset` stepping by two from zero, the offset is always
even, so `offset < data_len` implies `offset <= data_len - 2` and the second index is at most
`data_len - 1`. In bounds.

**What would make it live**, recorded because it is one edit away: any third `alloc_data`
caller that does not constrain `cnt` to an even value, or relaxing either guard above. A
round that adds a command to this device must check that before anything else. *The guards
that make this safe are doing load-bearing work they do not advertise* — neither mentions
the read path they protect.

*Marginal, noted not filed:* `:191-194` admits `sector_count == 0` with `cnt == 0`, giving
`malloc(0)`. Harmless on glibc (unique non-NULL), implementation-defined in principle, and it
lands on the `:334` exit anyway, which this round's scope already covers.

### In-tree precedent for the width question, which the pass-1 brief did not cite

The panel split A/B/C on whether a wrong-width access should be DECLINED or EMULATED. **This
project has already answered it twice, once in the same machine and once in the same file:**

* `dev_pvr.c:1577-1581` — *the same class, on the Dreamcast* — carries `#187`'s note:
  *"guest-reachable; the masked access below is bounded to the TA buffer, so log and
  continue, don't exit(1)."* It neither declines nor emulates: it logs and **proceeds**.
* `dev_dreamcast_gdrom.c:197` — *this very file* — already carries
  `break;  /* OB-20: was exit(1) */`, so one site here has been de-fatalised before.

**But `#187`'s warrant does not transfer unexamined.** Its reason was that *the continuation
was bounded*. At `GDROM_DATA` the code below the width check assumes 16 bits throughout —
`memory_writemax64(cpu, data, len, odata)` at `:451` and the paired byte reads at `:319-320`
— so "log and continue" needs its own bounded-ness argument here, not an inherited one.
Recorded as the question the fix must answer rather than as a precedent that settles it.

### `gdromdefault` — *** CLOSED, shipped as `ba30e64` + `a7b103d`. This heading said `open` for hours afterwards. ***

*Caught by a measuring seat, not by a gate. The ledger said `closed`, a commit was
titled "close gdromdefault", and a LATER commit touched this very file without fixing
the heading — and **the carrier's first-stop procedure reads OUTSTANDING_BUGS.md as the
live queue**, so this is the state-vs-substance mismatch pointing the expensive way: a
fresh session would have picked shipped work as its next round. `check_row_states.py`
checks the ledger against the repo; nothing checks this file against the ledger.*

`dev_dreamcast_gdrom.c:439-447`. The device registers a **0x100 window** at `0x005f7000` and
its `switch` handles about eight offsets. The `default:` arm prints and then runs `exit(1)` —
for a **read or a write**, at **any width**, at **every other offset in the window**.

**MEASURED on an unmodified `-E dreamcast -x`**, one 32-bit guest load per offset:

```
  +0x00 +0x04 +0x08 +0x0c +0x10 +0x14 +0x1c +0x20 +0x30 +0x40
  +0x50 +0x60 +0x70 +0x78 +0x7c +0xa0 +0xc0 +0xf0 +0xfc      -> DIED, "default: arm"
  +0x90 +0x94                                                 -> alive

  21 sampled, 19 DIED, 2 survived
```

*32-bit was chosen deliberately:* it reaches `default:` for unhandled offsets **without**
first tripping `GDROM_DATA`'s own width guard, so a death is attributable to this arm and not
to another. Each dead session printed `[ dreamcast_gdrom: read from addr 0x… ]` — its own
named text, so each failed for the reason under test.

*** THIS IS ONE PREDICATE WITH A LARGER BLAST RADIUS THAN THE ENTIRE `GDROM_DATA` ARM. ***
That arm needs a specific register and, for two of its three sites, specific device state.
This one needs **any address in a 256-byte window** that nobody implemented. A driver or a
diagnostic that scans the device's register space — an ordinary thing to do — dies on its
first unhandled offset.

**Ordering note, recorded so the sequencing is deliberate rather than accidental.** The
carrier says a witness makes an item *eligible* while **severity** orders the queue, and by
severity this outranks `sh4gdromexit`. It is nevertheless queued *behind* it, for one
concrete reason: `dev_dreamcast_gdrom.c` has **no once-only latch mechanism at all** today,
and `sh4gdromexit` builds it. Once that ships, this row is a cheap follow-up — one predicate,
one new latch instance, and a detector that samples the window exactly as above.

`:434` is the third of the family: any `GDROM_COND` write outside `{0xa0, 0xef}` runs
`exit(1)`, one instruction, no state required. Same disposition.

## 2026-08-23 — `sh4gdromexit` pass 1: the detector was INVERTED, and Option C resurrects a host kill

### The detector rewarded deleting the code it was written to defend

A measuring seat ran the pass-1 probe against six builds of its own:

| build | score |
|---|---|
| committed (the defect) | 3/13 |
| **whole arm replaced by `odata=0xffff; break;`** | **13/13** |
| the brief's Option C | 11/13 |
| **the intended decline+latch fix** | **8/13** |

*** The detector punished the correct fix and gave full marks to deleting the register arm. ***
Cause: six rows asserted the old `fatal()` text must be **absent**, but the `#447`/`#459`
shape this round agreed **keeps the diagnostic** and drops only `exit(1)`.

**Re-pinned in oracle-correction order** — expectations written first, committed build
measured **RED at 4/14**, and only then any code change. The discriminating shape is *drive
the same site twice in one session*: pre-fix dies, the correct fix survives with the
diagnostic **exactly once**, a deleted arm survives with **zero**. A survival-only oracle
cannot separate the last two; a count can.

### OPTION C IS NOT MERELY WRONG — IT RESURRECTS A HOST KILL, AND THAT IS MEASURED

Two seats voted for emulating narrow accesses. Built and measured: allowing narrow writes
lets `cmd_count` step by **1**, so eleven byte writes plus one word write goes 11 → 13,
**skipping the `== 12` equality**. `busy & 0x08` never clears and the next write reaches
`:340` — a site this round had assessed as unreachable. The Option C build **dies there**.
It also writes `cmd[12]`, one past `uint8_t cmd[12]`.

*A fix that re-opens a dead site is worse than the defect it replaces, and only a build
found it.*

### The width guard is BOUNDED — measured, so `#187`'s precedent transfers

`len` appears **exactly once in the entire `GDROM_DATA` arm — the guard itself**. No index
expression consults it. Confirmed behaviourally: byte, word and longword reads all consume
exactly two bytes and return identical `odata`, and six *byte* stores assemble the 12-byte
packet and dispatch the command exactly as six word stores do. Removing the guard changes
**no bound**, which is precisely `dev_pvr.c` `#187`'s stated warrant — so "log once and
continue" transfers, and that is *not* the brief's Option C.

### Use `dev_wdc.c`'s precedent, not `sh4_val_first()`

`dev_wdc.c` is this tree's **other ATA/ATAPI data port**, and `#337` fixed this exact class
there with a plain `int warned_badlen` struct field. `sh4_val_first()` is an SH4 helper; the
GD-ROM sits on the Holly/G1 bus, not the SH4. A `uint8_t warned` bitmask in the existing
struct costs nothing and couples nothing.

`dev_wdc.c:155-167` also settles the declined-read value: it returns `(uint64_t)-1` with a
diagnostic and no exit. **But no value is self-identifying here** — this device's TOC is
`memset(0xff)`, so `0xffff` is legitimate payload. *That is exactly why the diagnostic, not
the value, is the truthfulness channel, and why the latch must be per-site.*

### Census corrected: EIGHT single-access-fatal sites in this file, not three

*(The list below names NINE and the heading says eight. `:334` is the one that does not
belong: this document itself says it needs a legal command, 204 successful reads and a
four-instruction loop under `step N` — that is not single-access. The other eight are
right. Corrected rather than renumbered, because the discrepancy is the useful part.)*

14 live `exit(1)` (17 textual, 3 disabled). Single-access-fatal on a fresh device:
`:308`, `:315`, `:352` (this round), `:334`, `:374` (`GDROM_UNKNOWN_0x88`, one store of
anything ≠ 0xb), `:434` (`GDROM_COND`), `:447` (`default:`), `:505` and `:518` (DMA).

* **`:334` IS reachable AND needs no new probe shape** — measured, using the existing
  helpers plus a four-instruction loop under `step N`. It joins on the merits: `:315` and
  `:334` are the same predicate family ("read when there is nothing to give"), and fixing one
  while the other stays fatal leaves a device where a declined read is safe in one state and
  fatal in another.
* **`:340` confirmed DEAD by measurement** — three constructed paths all reached `:352`.

### The `default:` arm: SEQUENCE, and say plainly why

**34 devices in `src/devices` have an `exit(1)`-ing `default:` arm; 218 live `exit(1)` calls
in that directory.** `:447` belongs to that cross-cutting class — which this project has
already named (`c677764`, "the class is 72 files wide") — not to the `GDROM_DATA` family. Its
accept side is a *different oracle set*: all eight implemented registers, not one. So the
"no new oracle" join test fails.

**The round therefore ships the smaller defect first, and the reason is not severity.** It is
that `:447`'s fix *design* is unsettled — what should an unimplemented offset return, and is
a 0x100 window right when eight offsets are implemented? Bundling an undesigned fix into a
designed round is how scope control fails.

### Refinement to the closed `gdromoob` negative

Rather than filing it against a hypothetical third `alloc_data` caller, **pair the check with
the increments**: `cur_data_offset + 1 < data_len`. That removes the dependence on an
invariant maintained two functions away, at zero cost.

### `#460` records corrections, applied before commit

*** ALL WITHIN-FILE LINE NUMBERS IN THE `sh4gdromexit` / `gdromoob` / `gdromdefault`
ENTRIES ABOVE ARE PRE-FIX (at HEAD `e4390ea`), AND THE `#460` DIFF MOVED THEM BY +26 TO
+90 LINES. ***

They were correct when written at pass 1. A pass-2 seat measured the drift: `:197` (the
OB-20 `break`) is now `:223`; `memory_writemax64` at `:451` is now `:529`; the paired reads
at `:319-320` are now `:379-380`; `gdromoob`'s `:318-320`/`:89`/`:393`/`:401`/`:120`/`:194`
are now `:378-380`/`:115`/`:471`/`:479`/`:146`/`:220`; `gdromdefault`'s `:439-447`/`:434`
are now `:561-569`/`:556`.

*** AND THE LINE ABOVE WAS ITSELF WRONG UNTIL 2026-08-23 -- THIS IS THE THIRD TIME A
RECORDS CORRECTION HAS REPEATED THE ERROR IT CORRECTS. *** It read `:517-525`/`:510`,
which matches **no committed tree**: both `#460` commits put the default arm at
`:561-569` and COND's exit at `:556`. The numbers were measured against an uncommitted
intermediate, before the round's final records pass grew the file again -- and the
paragraph stamped the OLD revision while silently adopting coordinates from a state that
was never committed, violating its own stated rule inside the same paragraph.

**Every within-file coordinate in this file is now stamped `HEAD 16f06a0`.** A seat found
it by re-deriving against three commits rather than trusting the annotation, which is the
only method that catches this class.

**This is the same trap `#459` recorded and it repeated one file over** — there the stale
citations were in a source comment, here in the records file. The rule stands and now has a
second instance behind it: *cite line numbers across files, never within one, and where a
records file must carry them, stamp the revision they were taken at.* Annotated rather than
re-cited, because re-citing guarantees the next diff invalidates them again.

**The `0xffff -> 0` escape is CLOSED, not filed.** A pass-2 seat named it — no row pinned
what a declined read *returns*, so replacing `0xffff` with `0` passed everything while the
diagnostic still claimed `0xffff`. The `declined val` row now pins it at `0xffffffff`
(`mov.w` sign-extends), on a first-touch load, which is the one path the legal TOC sequence
cannot explain.

**The wrong-width READ escape was the sharper one.** The pass-2 rebuild wrapped the width
rows around *stores* only, and restoring `exit(1)` on wrong-width **read** alone scored a
clean **14/14** while one guest `MOV.B` from `0xa05f7080` still ended the host. `w8 load` and
`w32 load` are back, and their loss is why they now carry a comment saying they are not
decoration.

**De-escalation, stated rather than left as a gap:** four host-fatal predicates were removed
and the detector carries accept rows for **three**. The width predicate is **exempt** — it
tests the access width against a compile-time constant and no guest store reaches its
operand, the same failability carve-out this project applies to read-only and
never-set-by-device bits. That exemption is now written at the site.

**On the re-pointed regexes** — the detector's `SAYS` patterns were re-pointed at the new
diagnostic strings after the fix landed. A seat ruled that the pre-fix-RED guard alone is
**not** sufficient, and the reasoning is worth keeping: pre-fix the build reddens by *process
death*, before any count is taken, so death-red cannot distinguish "the regex matches the
correct diagnostic" from "the regex matches any survival". What actually defends the re-point
is the **surviving-but-wrong** control — a deleted arm survives and emits nothing, so the
exactly-once counts redden. Those rows are live, so the re-point is honest; the rule is that
a re-pointed regex needs a surviving-wrong negative control, not just a pre-fix red.

### `gdromcondavail` — open (residual of `#460`)

*** RENAMED 2026-08-24. THIS ENTRY AND THE LEDGER ROW `gdromcondlies` DESCRIBED TWO
DIFFERENT DEFECTS UNDER ONE NAME. ***  The ledger row is the BADVAL kills at
`GDROM_COND` and `GDROM_UNKNOWN_0x88`; THIS is the availability lie below, which is
what the name actually described.  **Closing the id on the BADVAL pair would have
hidden this one** — the dishonest-listing class `#270` exists to prevent.  Split so
neither can be closed by work on the other.  *Caught by a seat auditing a brief's
premises rather than its argument.*

After `#460`, `COND_DATA_AVAIL` **permanently lies** once a guest reads past the buffer: the
device keeps advertising that data is available while returning `0xffff` for every subsequent
read, announcing it once. Pre-fix that inconsistency was unmissable, because the same read
ended the host.

Clearing `COND_DATA_AVAIL` at exhaustion would repair the state. Deliberately out of scope for
`#460` — that round's fix design is "decline and say so", and changing what the device
*advertises* is a behaviour change with its own oracle.

*Recorded because a de-escalation makes exactly this class quieter:* the fix removed the loud
symptom of a state inconsistency without removing the inconsistency.

### `hlen` census is now stale by one

The ledger row `hlen` ("device handlers that ignore the access length") counts **8**
warn-then-service handlers. `#460` makes `GDROM_DATA` the **ninth**. Noted here rather than
silently left, because that row's own entry warns about exactly this drift.

### `#460` residual escapes, filed as coverage debt

* A declined **32-bit** read returns `0x0000ffff`, not `0xffffffff` — a small divergence from
  the cited `dev_wdc.c` `(uint64_t)-1` precedent, unpinned by any row.
* The width latch can be **spent by an access that was declined anyway**, so a later *landing*
  narrow store is silent. Inherent to warn-once — `dev_wdc.c` has the same property. Document,
  do not fix.


### `gdromdmadefault` — *** JOINED #461. Its own join condition was met, not waived.
NOT YET SHIPPED: #461 is written, measured and HELD UNCOMMITTED by owner decision
pending the Fable 5 seat. ***

The entry below said: *"Add them, measure them RED on committed HEAD first."*  That is
exactly what happened — the DMA rows were measured red on the pre-fix build before the
arm was touched, and the round ships nine DMA rows (`dma rd`, `dma rd x1`, `dma two`,
`dma shadow`, `dma seed`, `dma alias`, `dma alias x1`, `dma align16`, `dma rdleak`) plus
`both windows`, which drives the two windows in one session.

**Recorded here rather than left to be inferred from the CHANGELOG**, because an entry
that states a condition and is never updated reads as a condition that was skipped.

*The original entry follows, unaltered.*

### `gdromdmadefault` — open, and it is the SIBLING THIS ROUND'S BRIEF MISSED

*** `dev_dreamcast_gdrom.c` HAS A SECOND `default:` KILL OF EXACTLY THIS CLASS, IN THE
ADJACENT WINDOW OF THE SAME DEVICE. *** `dreamcast_gdrom_dma`, registered separately at
`0x005f7400` size `0x80`, implements five word offsets (`0x04`, `0x08`, `0x0c`, `0x14`,
`0x18`) and sends everything else to a `default:` arm that prints and then `exit(1)`s — read
or write, any width. Coordinates `:632-640` at HEAD `16f06a0`.

**It was invisible.** It sits inside the census count of 14, and it is named in no filing and
in no brief — the `gdromdefault` brief said *"two DMA sites"* when the file has **three**
(`:611`, `:627`, `:640`), and the third is the only one in this round's semantic class. A seat
found it by enumerating rather than by reading the filing.

**A seat ruled it JOINS `gdromdefault`, conditionally**, and the condition is the witness
ladder itself:

* Same class, same device, same DEVINIT, one fix design — a second small bitmap, `2 × 1` word
  for 32 word-keys. ***Do NOT share the control window's array*** — a cross-window duplicate
  key is `#451`'s hazard one level up.
* The detector extension is inside what `#460`'s `:334` join failed: **no new opcode, no new
  loop shape, no new state manipulation.** Two trigger rows at `0xa05f7400 + {0x00, 0x7c}`
  using the existing helpers, plus one regex literal, because the current pattern deliberately
  will not match `dreamcast_gdrom_dma:` — the colon sits elsewhere.
* **THE CONDITION: "same class" is an inference, not a witness.** The committed 5/16 witness
  has no DMA rows. Add them, measure them RED on committed HEAD *first*, and only then does it
  join.

**If the round declines the join, it MUST still file this by name** — shipping the control
window fixed beside an identical fatal arm in the adjacent window of the same device is
`#460`'s *"safe in one state, lethal in another"* with **state** replaced by **window**.

*Noted while checking:* `dma_reg[NREGS_GDROM_DMA]` is dimensioned `0x100/4` = 64 words while
the registered window is `0x80` = 32 words — twice the size. Harmless today, and worth knowing
**before anyone keys a latch off `NREGS_GDROM_DMA`**.


## 2026-08-23 — two findings ABOUT THE HARNESS, both about work done this session

### `probetimebased` — open, and it is bigger than the round that found it

*** SIX PTY PROBES HAVE NO PROMPT DETECTION AT ALL, AND `gate_hygiene`'s RATCHET
STRUCTURALLY CANNOT SEE THEM. EVERY ONE OF THEM WAS WRITTEN THIS SESSION. ***

| probe | `endswith(` occurrences |
|---|---|
| `gdrom_data_probe.py` | **0** |
| `gdrom_default_probe.py` | **0** |
| `sh_intprio_probe.py` | **0** |
| `sh_iprbcd_probe.py` | **0** |
| `sh_pclock_probe.py` | **0** |
| `sh_tlbmulti_probe.py` | **0** |
| every other pty probe in `regress/` | 1 or more |

They use fixed wall-clock reads — `settle=8.0`, `0.35` per command, a `spin` at the end —
rather than the prompt-anchored `wait(mark=…, echo=…)` idiom the rest of the tree uses.

**Why the ratchet misses them, and it is not a bug in the ratchet so much as an unstated
boundary.** `gate_hygiene.sh:98` collects candidates with `grep -h "endswith("` and then
partitions them. A file containing **zero** `endswith(` contributes to no counter, so all five
of them sit still and the gate passes. Its own comment (`:72-74`) says the check is
CLOSED-WORLD — *"every `.endswith()` in the tree must use…"* — and that is true as written.
**It is closed over files that already use the idiom, and silent about files that never
adopted it.**

**Why it matters rather than being tidiness.** This project's own rule is that a wall-clock
budget is a **load-sensitive oracle**; `gate_ab` once false-FAILed a 45-minute battery because
subagents loaded the host. The rows most exposed here are exactly the `x1` diagnostic-count
rows — under load a short read returns fewer bytes, the count reads 0, and a **correct build
scores a false red**. Worse in the other direction: a `survived` row is timeout-based, so a
**wedged** emulator reads as alive.

*Nothing has miscounted yet* — every measurement this session reproduced across repeated runs,
and the mutants' numbers matched two independent implementations. That is evidence the reads
are currently generous, not evidence the shape is safe.

**Two candidate repairs, and they are not equivalent.** (a) Convert the six to the
prompt-anchored idiom — correct, and six files of work. (b) Extend the ratchet to count pty
probes that have *no* prompt detection, so the blind spot becomes a red row rather than a
silence — cheap, and it stops the set growing. **(b) first**: it is the one that prevents a
seventh, and this session added six.

### `makercfalse` — ASSESSED, cause NOT established

A build that FAILED reported `MAKE_RC=0`. The compile errors were in the log
(`'GDROM_NDIR' undeclared`, four of them, then `make: *** Error 2`), and the wrapper printed
zero.

The form that failed was `cd … && rm … && make > log 2>&1; echo "MAKE_RC=$?"`. The form that
then reported correctly was `make > log 2>&1` followed by `rc=$?` on its own line. **I cannot
explain the difference and am not going to invent one** — the honest record is that one form
was observed lying once and the other was not.

**What is cheap and independent: check the binary is newer than the source.**
`[ build/gxemul -nt src/…/file.c ]` cannot be fooled by a status-propagation subtlety, and it
answers the question the round actually cares about — *did my edit get compiled into the thing
I am about to measure?* That check is now in the build wrapper.

*This is worth more than the incident.* Every round this session has claimed "build clean,
`MAKE_RC=0`, zero warnings" in its commit message. If that check can read 0 on a failure, the
claim is weaker than it sounds — and the freshness check is the corroboration that makes it
mean something again.


## 2026-08-23 — `gdromdmawidth`: the DMA tail store ignores `len`

**ASSESSED, FILED, NOT FIXED — pre-existing upstream and untouched by `#461`.**

`dev_dreamcast_gdrom.c`'s DMA tail store is `d->dma_reg[relative_addr / sizeof(uint32_t)]
 = idata;` with **no width discrimination**. An *aligned* byte or 16-bit write at `+0x04`
matches `case 0x04`, reaches the store, and **clobbers all 32 bits** of `dma_reg[1]` with
a value the guest only wrote 8 or 16 bits of.

**Why it is filed rather than fixed, and the reason is the reopening rule, not triage
fatigue.** `#461`'s semantic class is *unimplemented offset*; this is *implemented offset,
wrong width*, so it is a separate round by the round-scope rule.

*** THE NEXT SENTENCE USED TO PRESUME THE FIX: "a read-modify-write honouring `len`,
which raises an endianness question the default arm never has to answer".  THAT
PRESUMPTION IS REFUTED ON BOTH FLANKS, and the pass-1 adjudication is recorded here so a
future round re-derives nothing. ***

**A seven-seat panel converged unanimously on declining narrow writes. The flagship seat
then overturned that from source.**  Mainline Linux `drivers/cdrom/gdrom.c` BYTE-WRITES
this window's `+0x18` to trigger every DMA transfer (`:622`) and BYTE-READS it to poll for
completion (`:618`), while the four value registers it uses are always 32-bit (`:585-589`).
So a blanket decline **would break a booting Linux**, and the width-blind code delivers
exactly what the one real narrow user needs.

**The read-modify-write is refuted differently — not by derivability but by an ABSENT
ORACLE.**  The endianness question turns out to be answerable: `cpu_sh.c:96` sets
`EMUL_LITTLE_ENDIAN` *unconditionally*, so there is no big-endian SH in this tree and the
merge is always the low lane.  The real objection is that `0x005f74xx` is Sega's Holly
ASIC, outside the SH7750 manual, and this project holds **no** documentation for it.  The
original filing's own words — "real hardware leaves the upper 24 bits" — were an
**unsourced claim**, the `#357`/`#362` shape this tree has already been burned by once.
A read-modify-write would ship an invented behaviour and then pin the invention with a
detector row.

**THE DECIDED DESIGN, if a fix is ever warranted:** decline with a latched diagnostic at
the four VALUE registers ONLY, keeping `+0x18` byte-capable.  The Linux byte-contract is a
standing constraint on anything that ships here.

**MEASURED on the committed build** (`dmawidth_measure.py`, reported not pinned): seed
`+0x04` with `0x11223344`, byte-write `0xff` at `+0x04`, read back → `0xff`, i.e.
`0x000000ff`; liveness control in the same run returned `0x12345678`.  The discriminating
row is that sequence — `0x000000ff` today, `0x11223344` declined, `0x112233ff` merged —
and **it must not ship as a green row pinning `0x000000ff`**, which would enshrine this
model's own behaviour as an oracle.

*Also noted by the seat, for whoever picks this up: the probe row that would pin the REAL
contract (byte trigger arms, byte poll reads 0) is currently UNBUILDABLE — any nonzero
store at `+0x18` today lands on one of `sh4gdromexit`'s filed `exit(1)` kills unless the
full command path is staged.  So this item is gated behind that round by
probe-buildability, not merely by priority.*

**It is the same FAMILY as the alias `#461` did fix, and that is worth stating plainly:**
the new rule *"alignment alone separates unimplemented word from misaligned access to an
implemented one"* is true and does **not** cover this — an aligned narrow write to an
implemented offset is neither. A future reader applying that rule to this site would
conclude it is safe. It is not.

Found by the pass-2 measuring seat while building mutants against the alias fix. Witness:
none built yet; `gdrom_default_probe.py`'s `dma seed` row is one store away from being one.


## 2026-08-23 — `verdictprose`: the extractor still sweeps prose into a verdict

**FILED, not fixed — coverage debt against a detector that is now above the vacuity
floor (24 rows, 11 mutants, every mutant red).**

Two measured escapes, both from the pass-2 panel, both real and neither a false pass:

```
VERDICT: SHIP I think this is ready.        ->  SHIP I THINK THIS
VERDICT: DO NOT SHIP is what I would say    ->  DO NOT SHIP IS
```

The value capture takes up to four whitespace-separated words, so a verdict followed by
prose on the same line sweeps the prose in. It is visible in production today: codex's
answer on `panel_20260823_173510` reports
`SHIP WITH CHANGES | SHIP I THINK THIS | SHIP | DO NOT SHIP`.

**Why it is filed rather than fixed, and the reason is not triage fatigue.** The obvious
repairs each break something measured: stopping at sentence punctuation breaks nothing
*here* but is untested against 406 real answers; matching a fixed verdict vocabulary
would reject the real answers this project has actually recorded — `KEEP THE SPLIT`,
`MEASUREMENT SOUND`, `PARTIALLY CORRECT`, `DEPENDS ON FINDINGS`, `OPTION A/B/C` — which
are seats answering a question the brief asked, not malformed verdicts.

**And the damage is bounded by the split reporting shipped alongside it.** A swept value
now appears as one entry in a `SPLIT, read the file` list rather than as the answer, so
it is loud rather than silent. That is the property that matters; the tidiness is not.

Three more escapes measured and filed with it, none of which changes a verdict today:
a verdict inside a markdown table row (`| VERDICT | SHIP |`) returns nothing; a seat that
states its verdict twice with different values is reported as a split with no ordering
preference (deliberate — last-wins was measured no better, and on this round's own pass 2
it would have reported codex as DO NOT SHIP by reading an illustrative example); and
`**Verdict:** **GO-WITH-CHANGES**`, two emphasis runs split by a space, still misses on
nine pre-2026-08-19 agy files.

## 2026-08-23 — `verdictstate`: the selftest covers `verdict_of` and nothing else

**FILED. Named by the flagship seat, and it is the sharper of its two scope findings.**

All 24 selftest rows exercise verdict extraction. The wall / DOWN / echo-only state
machine has **zero** rows — and *** ALL THREE HISTORICAL MISCLASSIFICATION CLASSES THIS
FILE RECORDS LIVED THERE ***: a walled codex producing the LARGEST file in the panel, a
live seat reported as walled because its reasoning mentioned a quota word, and three
Ollama seats filed as "answered, format miss" when the daemon was not running at all.

So precommit section V can fire, pass, and prove nothing about the part of the file that
has actually failed before. The rows are cheap — a synthetic tail carrying a quota notice,
one with the notice mid-reasoning, one `ConnectionRefusedError` error file — and the
positive controls already exist as committed panel directories.

Related, same seat: **section V is edge-triggered with no level check.** It fires only
when the extractor is staged, unstaged or untracked. Commit a defective revision in a
session that skips precommit and every later run reports "extractor unchanged" forever,
because the defect is now the baseline. The selftest is sub-second; the fix is to drop the
condition and run it unconditionally, which dissolves the class rather than patching it.
Also: a `git mv` of the extractor takes the `[ ! -f ]` branch, which is a **soft warn**,
so precommit can still PASS with the selftest never having run. That branch should be
hard.


## 2026-08-23 — `gdromexitsix`: six live host-kill sites that had no open carrier

**FOUND BY FOLLOWING A FLAGSHIP SEAT'S POINTER AND CHECKING IT RATHER THAN TAKING IT.**

The `gdromdmawidth` adjudication said to let `sh4gdromexit` take this file's next round,
describing it as OPEN. **It is CLOSED** (`98a3408 16f06a0`), and its scope is specifically
`#460`'s GDROM_DATA arm — it was never an umbrella for the file. `#461`'s own CHANGELOG
says twice that the eight surviving `exit(1)` sites are *"filed under the `sh4gdromexit`
umbrella"*.

**Checked, rather than assumed.**  Of the eight, `gdromcondlies` covers exactly TWO —
`:639` (`GDROM_UNKNOWN_0x88`) and `:699` (`GDROM_COND`), the BADVAL pair. The other six
had **no open carrier at all**.

So a census that read as *filed* was really six live, guest-reachable host-kill sites
sitting in nobody's queue. It is the "half a census reads as a whole one" hazard one
level up: `#461` did the hard part — it enumerated all eight rather than naming the four
it had touched — and then the QUEUE, not the census, was the incomplete half.

### The six

*Line numbers re-derived 2026-08-23 after the last edit to the file. They have now moved
three times in this round, every time because a later comment insertion of my own sat
above them — the uniform offset is the tell.*

*** LINE NUMBERS CORRECTED 2026-08-24: every one below was 25 too low, and the
drift is UNIFORM across all eight. ***  They were derived from a working tree 25
lines shorter than HEAD.  A uniform offset is exactly the tell this section already
names one paragraph above — unapplied to itself.  Re-derived from
`git show HEAD:src/devices/dev_dreamcast_gdrom.c`.  **Each site is named by its
DIAGNOSTIC, which survives an edit; the number is only a locator.**

| on HEAD | diagnostic | class |
|---|---|---|
| `:319` | `GDROM Read TOC not 408 bytes?` | command layer |
| `:371` | `GDROM unimplemented data format 0x%02x` | command layer |
| `:449` | `handle_command` default, `unimplemented command 0x%02x` | command layer |
| `:625` | `Too much GDROM_DATA?` | **NOT guest-reachable — keep fatal** |
| `:664` | `[ Write to GDROM_UNKNOWN_0x88: TODO ]` (`idata != 0xb`) | carried by `gdromcondlies` |
| `:724` | `unimplemented GDROM_COND = 0x%02x` | carried by `gdromcondlies` |
| `:829` | `DMA transfer but d->data is NULL` | DMA `+0x18` — **#462** |
| `:845` | DMA arming-mismatch report | DMA `+0x18` — **#462** |

*The last two rows used to sit BELOW the prose block that follows, orphaned from the
header, so markdown rendered them as plain text and the table showed four of eight.
**A table split by prose is a table that silently loses rows.**  The two
`gdromcondlies` sites were named only in prose and are now rows, so the table is the
whole census rather than a subset of it.*

*** `:625` IS NOT REACHABLE AND SHOULD STAY FATAL, so the heading's "six
guest-reachable" is wrong by one. ***  A flagship seat traced the invariant:
`busy & 0x08` is set only by `COND=0xa0`, which zeroes `cmd_count`; the only
increments are +2 per store; at exactly 12 the flag clears and the command
dispatches. So `cmd_count >= 12 && (busy & 0x08)` cannot be reached from any guest
input sequence — no witness can exist, and the ladder says document, not change.

**And it has MEASURED value as an invariant tripwire**: `#460`'s rejected Option C
(step-by-1 width emulation) was caught *precisely because* it made `:625` reachable.
De-fatalising it would delete the one accidental detector of the `cmd_count`
invariant while buying no guest-facing safety.

**Census correction, also from that seat:** the file has **eight** live `exit(1)`,
not six. `:664` and `:724` are each ONE store from death — more reachable than four
of the six here — and are carried by the open `gdromcondlies` row. The arithmetic
was defensible; **the exclusion was never stated**, and the seat had to consult the
ledger to stop itself re-filing them. One sentence prevents the next seat repeating
that.

### Why the DMA pair is the interesting half

**`#461` made the surrounding window survivable**, so a guest can now reach `+0x18`
without dying on the way — and **one nonzero store there still ends the host**. That is
the de-escalation clause's shape read forwards: removing one host-fatal class makes the
next one *easier* to reach, not harder.

It is also the blocker `gdromdmawidth` is gated behind: the row that would pin that
item's real contract — Linux's byte trigger arms, byte poll reads status — cannot be
built until these two exits go. **So this is the round that unblocks that one**, which is
a scheduling fact rather than a severity claim.

*Not witnessed yet, and the claim is checkable rather than asserted: the DMA pair looks
cheap now that the window survives, and the four command-layer sites need a GDROM_DATA
packet sequence that `#460`'s probe already knows how to build.*

## 2026-08-24 — the `#462` pass-2 harvest: one NEW site more reachable than the six

*All nine seats fired on the `#462` diff. Seven scriptable answered, Opus answered,
*** BOTH HALVES OF THIS SENTENCE ARE NOW FALSE AND ARE CORRECTED IN PLACE. *** Fable was
outstanding at the time of writing and **has since answered** — its verdict is in the
CHANGELOG's nine-seat list. And the finding-attribution is refuted by that same table:
`arm halfarm` was found by **deepseek, an APPROVING seat**, and the Opus seat
(ship-the-code-fix-the-detector) found three rows. *A claim that only the dissenters found
anything is the kind that gets quoted to justify weighting dissent, so it earns the
correction rather than a footnote.* Superseded text: the two DISSENTING verdicts carried every
finding below**; the five approving seats were right about the code and wrong about
what the detector proved, which is why verdicts are not counted here.*

### `asicbadaddr` — CLOSED at f1fa6a0, and it was a SINGLE GUEST LOAD

*Heading corrected 2026-08-25. It still read `open` after the fix, the 13-row detector and the gate wiring had all shipped — and **this file is the carrier's FIRST-STOP live queue**, so a fresh session would have been offered work that was already done. Section W exists because `gdromdefault` did exactly this, and it caught this one too.*

`dev_dreamcast_asic.c:118-123`, verified by opening the file:

```c
	r = (relative_addr / 4) & 3;
	if (r == 3) {
		fatal("[ dreamcast_asic: Bad address ]\n");
		r = 0;
		exit(1);	// TODO?
	}
```

**It runs BEFORE the `switch` and BEFORE any `writeflag` test**, so a guest LOAD kills
the host just as a store does — no staging, no command sequence, no arming. Every
address in the registered window with `(relative_addr / 4) & 3 == 3` qualifies:
`SYSASIC_BASE + 0x0c, 0x1c, 0x2c … 0xfc`.

**This is strictly more reachable than all six GD-ROM sites**, which need at minimum a
store and mostly a staging sequence. The dead `r = 0;` immediately before `exit(1)` is
a tell: someone intended to recover and the `// TODO?` says so.

**A witness costs one constant.** *** OVERTAKEN 2026-08-24: THE WITNESS IS DRAFTED AND
DESIGN-REVIEWED — `_scratchpad/asic_badaddr_witness.py`, 9 rows, unrun. *** The review
found two owed adds, both now applied: `kill far` at `+0xfc` (the first draft's three
killing rows were ALL inside one 16-byte group, so a group-narrowing mutant would have
left every row green — the witness would have committed the exact sin its own header
names) and `safe 4` at `+0x04` (r==1 was pinned by nothing, so a mutant narrowing to
`(relative_addr / 4) & 1` escaped both existing accept rows). *`one constant` was true of
the ADDRESS and false of the WITNESS.* Original text: `gdrom_default_probe.py` already reads
`SYSASIC_PEND = 0xa05f6900` through real address decode in two sessions
(`:743`, `:760`). `0xa05f690c` is the same window, `(0x0c/4) & 3 == 3`. That is a
rung-3 cold-debugger probe in an existing harness — the cheapest witness on the queue.

*Found by the Opus seat while answering a question about a different file. It is a
SEPARATE ROUND under the one-site rule — do not fold it into `#462`.*

### `gdromdmaguard` — filed, coverage debt above the floor

Codex: `count == 1 && enable == 1` → `count <= 1 && enable == 1`. **One character.**
Both decline blocks and both diagnostics survive; the only tested mismatch `(0,0)`
still declines because `enable == 1` fails, so it stays green. But `(count, enable) =
(0, 1)` is then ACCEPTED and a transfer runs for a guest that programmed no blocks.

`arm halfarm` does NOT catch it — that row uses `(1, 0)`, which `count <= 1` also
declines. Closing it needs a row that stages data, arms `(0, 1)`, and pins that the
transfer does NOT run.

**Filed rather than fixed** because it is neither a measured false pass of a shipped
claim nor a wrong record: it tests *the guard does not accept too much*, which is a
different property from the two this round repairs. The stopping rule governs. *** GROUND
CORRECTED BELOW, AND THE CORRECTION WAS ORDERED AND NEVER EXECUTED UNTIL NOW. *** The
TWO-DISPOSITIONS section rules that these are the **same property, on the same
predicate**, that this filing reason was wrong, and that the row should stand FILED on
the correct ground — above-floor coverage debt, with `(0,1)` named as the uncovered
point. *The disposition never changed; only its warrant did. A wrong reason is reused,
which is why it is annotated here at its origin rather than left to be discovered 1,250
lines away.*

### `gdromdmasilent` — filed, and it is the quietest escape named

Opus: `if (idata != 0)` at the head of `case 0x18` → `if (idata == 1)`. **Four
characters.** *** CLOSED BY `arm bytetrig`, ADDED IN PASS 2 — THIS FILING ADVERTISES AN
ESCAPE THE ROUND'S OWN SHIPPED ROW ALREADY CLOSES, WHICH IS PRECOMMIT SECTION W's
DIRECTION. *** `arm bytetrig` triggers with a BYTE STORE OF 0x5a, so the premise below —
that every write uses the value 1 — is false of the shipped probe, and the row's own
comment names `idata &= ~1u` as the mutant it was built to close. The `== 1` form dies
too, by derivation: 0x5a skips the block, the tail store lands 0x5a in the shadow, and
the row (want `0x0`) reddens — M1's MEASURED `0x5a` vs `0x0` kill proves that exact
observation channel works. *The `== 1` closure is a READING, not a measurement; it can
ride the next table if anyone wants it measured.* The row count below is also stale (58,
not 51). Superseded text follows: every write to `DMA + 0x18` anywhere in the probe uses
the value 1, so all 51 rows stay green — while a guest trigger of 2, or `0x80000000`,
skips the whole
block, reaches the tail store, and leaves `+0x18` reading BUSY FOREVER **with neither
diagnostic printed**. Sticky *and* silent, and it reads as a tightening.

Runner-up, same blind spot, five characters: `idata = 0;` → `idata &= ~1u;`.

### `gdromxfrflood` — filed, pre-existing, and the round touched the line

`fatal("[ dreamcast_gdrom_dma: Transfering …")` is NOT latched, so a guest looping
legal DMA floods host stderr — while the two ILLEGAL paths `#462` just latched stay
quiet. The inversion sits three lines from a new comment block arguing that flooding
"is the one behaviour every latch here exists to prevent."

### `gdromdriverclaims` — open, and it is the DDI-0100I shape exactly

`#462`'s design rests on three claims about guest drivers:
*`gdrom_dma_interrupt()` clears `gd.transfer` UNCONDITIONALLY and inspects no error
bit*; *`HZ*7` after the trigger, `HZ/2` before it*; *NetBSD's status waits are
unbounded spins*. **There is no copy of Linux's `drivers/cdrom/gdrom.c` or NetBSD's
`sys/arch/dreamcast/dev/gdrom.c` anywhere in this tree.** Every one is seat-reported.

If the first is wrong, the decline-without-event choice is wrong. If the second is
wrong, the "a decline is safe, it will not hang" premise is wrong.

*** AND ONE OF THE THREE WAS MEASURED FALSE THE SAME DAY IT WAS FILED. ***
The NetBSD exhibit `while ((GDROM_BUSY & 0x88) != 0x08) ;` was quoted in FOUR
records to support *"a sticky +0x18 hangs NetBSD for real"*. It is not a poll of
+0x18, on two independent grounds:

* **Arithmetic, from the quoted line alone.** It exits only when bit 3 is SET and
  bit 7 CLEAR. `+0x18` is {0 idle, 1 busy}; `0 & 0x88` and `1 & 0x88` are both
  0, never 0x08 -- **the loop would hang on CORRECT hardware.**
* **This tree already documented it, in code the round never touched.**
  `dev_dreamcast_gdrom.c:722-737`: NetBSD writes 0xa0 to `GDROM_COND` to START A
  COMMAND and then *"expects (BUSY & 0x88) to be 0x08"*; `:737` sets
  `d->busy |= 0x08` in reply. It is the command-start handshake on the CONTROL
  window's BUSY register.

**The exhibit was lifted from that comment and re-pointed at a register it says
nothing about.** The conclusion survives on Linux; the reason does not. *The seat
that caught it did so by doing the bit arithmetic on a line four records had
copied without checking -- which is the cheapest possible check, and none of the
four had run it.*

**This is `#357`/`#362`/`#365` again** — page numbers from panel output rather than a
local manual, which held by luck and good seats rather than by process. Obtaining the
SH manual refuted a wrong finding the same session it was raised; obtaining these two
driver sources is the same cheap move. Until then the comments must say
SEAT-REPORTED, not state them as fact.

### `probeslow` — open, and it is `probetimebased` seen from the other end

**Two ledger rows, ONE cause, and neither entry said so.** `probeslow` was filed as "the
probe may not fit its budget"; `probetimebased` was filed as "six pty probes have no
prompt detection at all". `gdrom_default_probe.py` is on BOTH lists, and the second is
why the first is true.

**Measured 2026-08-24, AT THE 51-ROW STATE — the probe has since grown and these numbers
are date-qualified rather than current:** 51 rows were driven by **35 `session()` calls**, *(CURRENT AT #462: **58 rows, 39 `session()` call sites** — and note the call-site
count is NOT the emulator count, since three sites sit inside loops; conflating the two
is an error this project has already made once, reporting 35 where 52 emulators forked.)*
and every one
forks a fresh emulator and then sleeps a FIXED `settle=8.0` regardless of when the guest
is actually ready, plus `0.35` per command and a `spin` at the end. That is ~280 s of
pure settle before a single useful read. The other pty probes in `regress/` detect the
prompt with `endswith(">")` and proceed as soon as it appears.

**So the fix for both rows is the same one**, and it is the one the tree already uses
everywhere else: adopt prompt detection here. That converts a fixed 8 s into however
long the guest actually takes.

**And the right unit for this row is SESSIONS, not rows.** Rows are nearly free when
they share a session -- the accept group is 5 rows on 1 session, and it was restructured
that way precisely because independent staging was what pushed this probe past its
budget in the first place. A row added to an existing session costs almost nothing; a
row that opens a session costs ~8 s minimum. The `#462` pass-2 additions could be
consolidated on that principle: `arm quiet` and `arm twice` both drive a FRESH device
with a trigger, so one session that triggers twice and then reads BOTH `+0x18` and
`SYSASIC_PEND` serves both rows -- and, per the accept group's own argument, makes them
two facts about ONE event rather than two similar events.

*Not done in `#462`: the round's probe was mid-measurement when this was worked out, and
editing a probe while measuring it is how a table ends up describing a file that no
longer exists. Consolidation is a follow-up, and it is behaviour-preserving.*

**No gate timeout was found on this probe** -- `gate_sh_rounding.sh:513` (**the citation
said `:501`; the invocation moved when the 58-row pin and the `-u` flags landed, and :501
is now a comment line**) runs it with
`|| true` and no `timeout`, and `run.sh` sets none for the gate -- so the failure mode
is a slow weekly battery, not a truncated log. That is the benign direction, and it is
worth stating explicitly because "the probe exceeds its budget" implies a red gate and
there is no budget to exceed.

#### `asicbadaddr` pass-1 panel, 2026-08-24 03:06 (`panel_20260824_030624`)

Seven scriptable seats answered; the two Agent seats were still running when this was
written. Verdicts: agy **GO-WITH-CHANGES**, grok PROCEED, deepseek ACCEPT, glm and
minimax both "the fix is safe", codex and kimi answered without a verdict line.

**The reachability claim was verified independently**, which matters because the whole
fix rests on it: every implemented `case` indexes a three-element array, and each maps
to `r` in {0,1,2} (`0x10`→0, `0x14`→1, `0x18`→2, `0x20`→0, `0x24`→1, `0x28`→2, `0x30`→0,
`0x34`→1, `0x38`→2). `r == 3` matches no case, so falling through to `default:` cannot
index out of bounds. A seat re-derived this from the source rather than taking the
brief's word.

**THE ONE CHANGE THE PANEL REQUIRED: delete the WHOLE `if (r == 3)` block, not just the
`exit(1)`.** Keeping the `fatal()` converts a host kill into a **guest-drivable output
flood** — sixteen unlatched addresses a guest can hammer. That is the same class already
filed as `gdromxfrflood`, and it would have been introduced by the obvious fix. *The
brief proposed deleting only the `exit(1)` and saying the dead `r = 0;` "becomes
harmless"; harmless is not the test.*

**Three mutants that defeat the detector the brief described** (load all 16 killing
offsets, confirm survival, read back one implemented register):

| mutant | why it passes |
|---|---|
| `if (r == 3 && writeflag == MEM_WRITE) exit(1);` | **the detector only LOADS.** Stores still kill. Directional asymmetry is invisible to a one-direction probe |
| `(relative_addr / 4) & 3` → `(relative_addr & 3) == 3` | changes WHICH addresses are affected; a probe that only checks the original sixteen sees nothing |
| delete any non-probed `case` (e.g. `case 0x14:`) | that offset silently falls to `default:` and reads 0 instead of its mask value |

**So the detector owes, at minimum:** both directions at every killing offset, and a
store-then-readback on **each of the four register groups** rather than one — plus a scan
asserting all twelve implemented offsets still route to their own case rather than to
`default:`.

**And an honest UNKNOWN, which outranks a confident guess:** there is **no Holly/SYSASIC
documentation anywhere in this tree**, so nothing here establishes what real hardware
returns for these sixteen offsets. `odata = 0` is GXemul's uniform convention for
unimplemented device reads, not a sourced value. Recorded as convention, not as fact —
the same discipline `gdromdriverclaims` exists to enforce.

#### *** THE CENSUS IN THIS ROW WAS WRONG BY 4x, AND SIX OF SEVEN SEATS CONFIRMED IT. ***

The filing and the pass-1 brief both said **sixteen** killing offsets. The true number is
**sixty-four**, because `relative_addr` is NOT necessarily word-aligned: a BYTE access at
`+0x0d` gives `0x0d / 4 == 3`, `3 & 3 == 3`, and dies exactly like `+0x0c`. The killing
set is four contiguous byte ranges per 16-byte group -- `0x0c-0x0f`, `0x1c-0x1f`,
`0x2c-0x2f`, ... `0xfc-0xff` -- of which the sixteen originally cited are only the
word-aligned quarter.

**ONE SEAT OF SEVEN CHECKED THE PREMISE.** The rest verified the arithmetic *as the brief
framed it* -- and one of them verified every other claim against the source, correctly,
and still reported "exactly 16", because it checked the derivation rather than the
assumption underneath it.

> **A WRONG FACT IN A BRIEF COMES BACK CONFIRMED.** This project already has the rule that
> packet-fed seats can only know what the brief inlines. The sharper form is that they
> cannot know what it inlines *wrongly*: a stated premise is load-bearing for every seat,
> and agreement with it is not evidence. The one seat that caught it did so by asking a
> question the brief never posed -- *is `relative_addr` word-aligned?* -- which is the
> only kind of check that can find this class.

**Consequence for the detector, and it is the reason this matters rather than a tidy-up:**
a probe that walks the sixteen word-aligned addresses covers **a quarter of the defect**,
and would report full coverage. The detector must walk byte offsets, and must do so in
BOTH directions -- a seat separately named `if (r == 3 && writeflag == MEM_WRITE)` as a
mutant that a loads-only probe cannot see.

*Also corrected from the same seat: deleting the `fatal()` along with the `exit(1)` is
right, and the reason is not that `fatal()` kills -- it does not, it has no early-out and
is not `exit` -- but that sixty-four guest-drivable unlatched addresses are a flood.*

#### `asicbadaddr`: the ABSENT ORACLE is already on the record, in this tree, from a prior round

**Q2 does not need an honest "I do not know" — it has a documented precedent.**
`dev_dreamcast_gdrom.c:1091-1095`, written by this project in an earlier round, records:

> *"0x005f74xx is Sega's Holly ASIC, outside the SH7750 manual, and this project holds NO
> documentation for it -- so 'real hardware preserves the upper bits' would be an oracle
> from plausibility, the `#357`/`#362` shape this tree has already been burned by once."*

**`SYSASIC` is at `0x5f69xx` — the same Holly ASIC.** The `_scratchpad` manuals are SH7750
and SH-4 *CPU* documentation, not Sega's chipset. So what real hardware returns at these
addresses is unknowable from what is held, and that was established before this round
began.

> **THE DETECTOR CONSEQUENCE, and it is the whole reason this matters:** the rows must pin
> **host survival and harmlessness**, and must NOT pin `odata == 0` as an architectural
> oracle. `odata = 0` is GXemul's uniform convention for an unmodelled read and is the
> right engineering default — pinning it as *truth about the hardware* would manufacture
> exactly the plausibility oracle the cited comment refuses.

*This is what the `gdromdmawidth` round bought: a precedent that transfers. The rule is
that a precedent transfers by its WARRANT, not its shape — and the warrant here is
identical, because it is literally the same undocumented chip.*

#### Accept rows, with the guard-growth mutant that makes them failable

The predicate that gated death is `r == 3`. Its adjacent modelled values are `r` in
{0,1,2}, each an array index — so the realistic growth mutants are `r == 3` → `r >= 2`
and → `r >= 1`, and the accept rows must REDDEN under them:

| row | offset | dies under |
|---|---|---|
| readback at `r == 2` | `0x08` or `0x18` | `r >= 2` |
| readback at `r == 1` | `0x04` or `0x14` | `r >= 1` |

`pending_irq` at `0x00/0x04/0x08` is guest-readable without a prior write; the mask groups
need write-then-readback. **Rows must span more than one group** — a detector that reads
back a single implemented offset is passed by an edit breaking a different group.

#### The sharpest escape named: a STORE-path re-kill

Re-add the host kill on the write branch only — e.g. in `default:`, `else { debug(...);
exit(1); }`. **All sixteen word-aligned LOADS survive, so a loads-only detector is green,
while every one of the sixty-four addresses still kills on a STORE.** It mirrors the
original defect's own load/store asymmetry, which is why the detector owes both directions
at every killing address, plus at least one unaligned probe inside a killing span.

*Checked and cleared in passing: `dev_dreamcast_asic.c:49`'s `// #define debug fatal` is
COMMENTED OUT, so the `default:` arm's `debug()` cannot become a `fatal()` by that route.*

#### `asicbadaddr`: the invariant is STRUCTURAL, and the sharpest mutant is one character

**State the invariant, not the enumeration.** `r == 3` is exactly
`(relative_addr & 0x0c) == 0x0c` — *the fourth word of every 16-byte group* — while all
twelve implemented cases are three CONSECUTIVE words at group bases
`0x00/0x10/0x20/0x30`. The enumeration says what is true today; the invariant says what a
future edit must not do. **The round record must carry it**, because without it,
deleting `r = 0;` looks like cleanup and adding `case 0x0c:` looks safe.

*And the domain was checked, which the brief only asserted:* `relative_addr` is exactly
`[0, 0x100)` — `memory_rw.c:480-481` bounds it, `:494` subtracts the base,
`core/memory.c:466-468` sets `endaddr = baseaddr + len` with **no page rounding**, and the
device registers `DM_DEFAULT` with no fast path. Internal callers cannot reach `r == 3`
either: `SYSASIC_TRIGGER_EVENT` lands at `SYSASIC_BASE + 4*(e >> 5)`, and the largest
defined event is 67, so `67 >> 5 == 2`.

> **AND THE CHECK PROTECTS NOTHING EVEN BEFORE THE FIX.** No reachable `case` yields
> `r == 3`, so it is not a bounds check the fix weakens — it is **a diagnostic wearing a
> bounds check's clothes**. Say so in the round record, or a future reader sees "a bounds
> check was deleted" and re-adds it.

**THE SHARPEST ESCAPE OF THE WHOLE PANEL — ONE CHARACTER:** `& 3` → `& 1`.

* `r` becomes {0,1}, so `r == 3` is never true → **all sixteen trigger rows green**.
* The harness's known implemented offset is `0xa05f6900` → `relative_addr == 0` → `r == 0`
  under both → **read-back row green**.
* Meanwhile `0x08/0x18/0x28/0x38` select index **0** instead of 2: the third register of
  every group aliases the first, **in both directions**, and `[2]` becomes permanently
  unreachable.
* **And it reads like a tidy-up**, which is precisely the clause-(d) test.

**A row-design constraint that would have bitten whoever wrote the rows**, verified by
opening the file: `pending_irq` **cannot be write-then-read-back tested from a guest**.
The write arm gates on `idata & 0x100000000ULL` — **bit 32**, which no 32-bit guest store
can produce — so `:135`'s set-branch is unreachable from a guest and `:138` only ever
CLEARS. The `pending_irq` accept rows must come from a **triggered event**; the
`mask_13/11/9` groups are plain read/write and are where the index-distinguishing rows
belong.

**Post-fix, the failure mode of widening this guard gets WORSE, not better.** `r == 3` →
`r >= 2` currently announces itself with `exit(1)` on the first legal access. After the
fix — *if `r = 0;` is left in place* — offsets `0x08/0x18/0x28/0x38` silently alias onto
index 0. That is an argument for deleting the whole block rather than just the `exit(1)`,
independent of the flood argument.

**Do NOT convert the invariant into a runtime guard.** It cannot fire today, and this tree
has already rejected exactly that move: *"A guard that cannot fire is not insurance; it is
a claim that something is checked when nothing is."* Comment plus accept rows is the
artifact.

*Why an out-of-range index would be invisible to the usual tool:* `pending_irq[3]`,
`mask_13[3]`, `mask_11[3]`, `mask_9[3]` are declared consecutively, so `pending_irq[3]`
lands on `mask_13[0]` under any normal ABI — **member-to-member inside one allocation,
which ASan does not see.**

### `asicdefaultflood` — open, filed not fixed (pre-existing, different property)

The `default:` arm is unlatched. It is silent at default verbosity, but under `-v` a guest
scanning the window floods — and this fix routes **sixty-four more byte offsets into that
arm** than before. Different property from the host kill; separate disposition.

### `verdictprose` — a NAMED, REPRODUCIBLE instance, and a discriminator that works

**The kimi seat's output file contains its full reasoning trace, including candidate
verdicts it drafted and rejected.** Measured on two panels the same day:

```
  Now format: VERDICT first line. What verdict? Something like:
  VERDICT: APPROVE / PASS -- the fix is correct; accept rows are failable ...
  Maybe: "VERDICT: PASS with two named measurement gaps" -- the questions are ...
  The verdict line must survive truncation -- put the core verdict in the first line.
```

Every one of those is deliberation. `seat_verdicts.py` swept them and reported
**`APPROVE | PASS <- SPLIT, read the file`** for a seat that gave exactly ONE verdict.

*The trace's own last line is it reminding itself that the verdict must survive
truncation. Its deliberation about verdict format is what broke the verdict extractor.*

> **THE DISCRIMINATOR, and it is structural rather than semantic: kimi's FINAL answer is
> marked with a `•` bullet at column 0; every trace line is plain, indented two spaces.**

| panel | plain-trace VERDICT lines | `•`-marked | real verdict |
|---|---|---|---|
| `panel_20260824_023342` (`#462` pass 2) | 7 | 1 (`:653`) | PASS |
| `panel_20260824_030624` (`asicbadaddr` pass 1) | 1 | 1 (`:45`) | Approve the fix |

**Observed twice, not proven stable** — recorded as an observation about this CLI's
rendering, not as a guaranteed contract. Two instances is enough to act on and not enough
to assert.

**FILED, NOT FIXED, deliberately.** `seat_verdicts.py` is harness code with its own
selftest and a precommit section that fires when it is touched; changing it inside a round
whose subject is a device is the scope creep the stopping rule exists to refuse. It is
also not a MEASURED FALSE PASS — the extractor reported a SPLIT and told the reader to
open the file, which is the safe direction and is exactly what the earlier
report-disagreement-rather-than-resolve fix was for.

**Two records corrected by this finding:** kimi's `#462` verdict is PASS, not a split; and
its `asicbadaddr` verdict is *"Approve the fix"*, which an earlier note recorded as "no
verdict line".

### `asicbadaddr` — the CONVERGED design, from all nine pass-1 seats

*Adjudicated in the main loop. Where seats disagreed I say which measurement or reading
settled it; where they agreed I say so rather than counting votes.*

**THE FIX — delete the whole `if (r == 3) { ... }` block**, all five lines, not just the
`exit(1)`. Two independent seats reached this and a third supplied a second reason:

* keeping the `fatal()` converts a host kill into **sixty-four guest-drivable unlatched
  addresses**, which is `gdromxfrflood`'s class introduced by the fix itself;
* keeping `r = 0;` makes a *future* widening of the guard SILENTLY ALIAS legal registers
  onto index 0, which is a worse failure than the one being removed;
* `default:` already prints a strictly better message — it names the address.

**THE ROUND RECORD MUST SAY THE CHECK PROTECTED NOTHING.** No reachable `case` yields
`r == 3`, so this is not a bounds check being weakened — it is a diagnostic wearing a
bounds check's clothes. Without that sentence a future reader sees "a bounds check was
deleted" and re-adds it.

**THE INVARIANT, stated structurally rather than as an enumeration**, because an
enumeration only describes today:

> `r` is the word index within a 16-byte group; `r == 3` is exactly
> `(relative_addr & 0x0c) == 0x0c`, the FOURTH word of every group. Every implemented
> register group is three CONSECUTIVE words at bases `0x00/0x10/0x20/0x30`. **If a `case`
> is ever added at a `+0x0c`-style offset it must not index these three-element arrays.**

**Do NOT convert that invariant into a runtime guard.** It cannot fire today, and this
tree already rejected exactly that move: *"A guard that cannot fire is not insurance; it
is a claim that something is checked when nothing is."*

#### The detector, and every requirement below came from a named escape

| requirement | the escape it closes |
|---|---|
| trigger rows at **byte** offsets (`+0x0c..0x0f`) in at least two groups | `if (r == 3 && (relative_addr & 3))` — invisible to word-aligned probes |
| trigger rows in **both directions** | `if (r == 3 && writeflag == MEM_WRITE)` — invisible to a loads-only probe |
| write+readback on a **mask** group at `r == 0, 1, 2` | `& 3` → `& 1`, one character: index 2 aliases index 0 in both directions while every trigger row stays green |
| readback spanning **more than one group** | deleting a non-probed `case` |
| rows must pin **survival**, never `odata == 0` as a hardware value | the absent-oracle trap |

**`pending_irq` CANNOT carry a write-then-readback row.** Verified by opening the file:
the write arm gates on `idata & 0x100000000ULL` — **bit 32** — which no 32-bit guest store
can produce, so the set-branch is guest-unreachable and a store can only CLEAR. Those rows
must come from a triggered event; the `mask_*` groups are plain read/write and are where
the index-distinguishing rows belong.

**The accept rows' failability discriminator is GUARD-ONLY (`r == 3` → `r >= 2`), not
joint.** The rule says build the form the latch operand cannot mask; here that operand is
the literal `r = 0;`, a constant the guard cannot feed, so guard-only is non-equivalent
*and* quieter. A row at `r == 2` (`+0x18`) reddens under it; rows at `r == 0` and `r == 1`
are the controls that make the red attributable.

**Consolidate into existing sessions.** `probeslow`/`probetimebased` are open on the very
probe this would extend — 35 sessions at a fixed 8 s settle each. Rows sharing a session
are nearly free; a row opening one costs ~8 s minimum.

**Absent oracle, and it is already on the record.** `dev_dreamcast_gdrom.c:1091-1095`
establishes that the Holly ASIC has no documentation in this project; `SYSASIC` at
`0x5f69xx` is the same chip. `odata = 0` is GXemul's convention for an unmodelled read and
matches `#461`'s reasoning that a declined read returns *the value claiming least*. Ship
it as convention, and **do not write a row asserting `0x00000000` as the hardware answer.**

#### `asicbadaddr`: the ATTACK panel broke the converged detector in four places

*The brief asked ONE question -- "what is the smallest edit a guest can detect that these
rows cannot?" -- and said plainly that ratification was not wanted and "looks good is not
an answer". **Four seats returned INCOMPLETE and one GO-WITH-CHANGES.** That framing is
the difference between this pass and the one before it, which produced agreement.*

**A. The `pending_irq` write-arm gate — TWO seats, independently, and it is the sharpest.**

```c
if (idata & 0x100000000ULL)   ->   if (idata & 1)
```

One token. Today that bit-32 gate makes the SET branch **guest-unreachable**, so a guest
store can only CLEAR. After the edit a guest can SET pending bits — i.e. **forge interrupt
assertions**. *And it is plausible precisely because the bit-32 constant looks like an
oddity a maintainer would tidy up.*

None of the five rows sees it: rows 1 and 5 work on `r == 3` holes and the address guard,
rows 2 and 3 exercise the mask groups, and a READ of `pending_irq` cannot exercise a
changed WRITE predicate — the stimulus is missing, not the observation.

**REQUIRED ROW:** store `1` to `+0x00`, read back, and require the bit **stays clear**.
That pins the guest-unreachability of the SET branch, which is currently an unrecorded
invariant this design leans on.

**B. The unmapped-read VALUE is entirely unpinned — TWO seats, and it corrects ME.**

`default: odata = ~0ULL;` — or, smaller still, changing `odata`'s initializer — is
invisible: row 1 asserts only SURVIVAL at the killing offsets, and rows 2-3 use implemented
cases that overwrite `odata`.

*** MY DESIGN SAID "rows pin survival, NEVER `odata == 0` as a hardware value", AND I
OVER-APPLIED MY OWN RULE INTO "do not pin it at all". ***  The seat that first raised the
absent oracle had already given the resolution and I dropped half of it: pin it as **this
model's DECLARED DECLINE VALUE, per the `#461`/`#452` convention, and say so in the row
comment.** That detects a changed convention without claiming to know the hardware.

**C. `switch (relative_addr)` -> `switch (relative_addr & ~3)`** — a plausible refactor to
"handle byte accesses within a word". A byte read at `+0x01` would then hit `case 0` and
return `pending_irq[0]` instead of the default. Row 1 tests only `+0x0c..0x0f`, which stay
in `default:` either way. **REQUIRED ROW:** a byte read at `+0x01` returning the decline
value, not `pending_irq[0]`.

**D. A newly added case in the unused window**, e.g. `case 0x40: odata = d->mask_13[0];`.
Rows 1-3 cover only the chosen holes and the existing groups. **The pattern that catches
this already exists in the sibling probe:** `scan uniq` counts how many offsets decline, so
a new case changes the count. An identity row of that shape belongs here.

#### And the framing worth keeping: COMPLETENESS IS RELATIVE TO A STATED CONTRACT

One seat closed with it: *"the detector can only be called complete under a narrow mutation
contract."* This project's vacuity floor already implies it — clauses (a)-(d) name exactly
which mutants must kill — but no round has yet WRITTEN the contract down next to the
detector. **A detector that says which edits it is designed to catch is falsifiable; one
that claims completeness is not.**

#### The attack panel's sharpest answer, and it names the INFERENCE rather than the gap

> **"Untestable positively" was read as "needs no row", and that inference is where a
> plausible cleanup edit walks straight through.**

The design reasoned correctly that `pending_irq` cannot carry a *positive* write-then-
readback row, because the SET branch is guest-unreachable — and then wrote no row at all.
**But reading 0 IS the invariant worth pinning: it reads 0 BECAUSE of the gate, not by
accident.** Three seats reached the same missing row from three directions; this is the
strongest form of it:

> **`pending_irq` clear-only row:** store `0xffffffff` to `+0x00` (and `+0x04`, `+0x08`),
> read back, require **`0`**. It reddens under every candidate mutant at once —
> `|= idata` reads back `0xffffffff`; bit-32 → bit-31 reads back `0x80000000`.

**AND A ROW-ORDERING GAP THAT WOULD HAVE SILENTLY WEAKENED ROW 2.** Its power to catch an
index-aliasing mutant (`(relative_addr / 4) & 3` → `relative_addr & 3`, collapsing
`0x10/0x14/0x18` onto index 0) **depends on an ordering the design never specified.**
Write-0x10/read-0x10, write-0x14/read-0x14, … lets an aliasing mutant round-trip each
sentinel in isolation and pass. **The three distinct sentinels only mean anything if ALL
are written BEFORE ANY readback.** Specify write-all-then-read-all, or the distinctness is
decoration.

*This is the `dma alias` shape again at one level up: a row whose stimulus is right and
whose SEQUENCING defeats its own purpose.*

**Row 2 covers only `mask_13`.** `mask_11` and `mask_9` write arms are untested — a
width-truncating or wrong-index edit on either is invisible. *"The design tests one group
thoroughly and assumes the other two are identical, but a maintenance edit touches one arm
at a time."*

**THE LARGEST STRUCTURAL BLIND SPOT: no row observes INTERRUPT ASSERTION at all.** The
device exists to forward events as IRQ 13/11/9; that behaviour — the product's whole
function — is untested by the entire ensemble. Removing a `dev_dreamcast_asic_tick()` call
from a write arm is invisible to every row (its witness is weak, since the periodic
DEVICE_TICK re-evaluates, so the effect is bounded latency rather than divergence — but
the blind spot is structural regardless of that one mutant's strength).

**Two conditions on the row-5 discriminator, to check in the script rather than assume:**
(a) the `r == 2` row must assert **SURVIVAL** — reddening by host death — not a readback
value; (b) it must **not** sit on `pending_irq[2]` expecting a positive readback, because
that arm cannot round-trip. *Had the accept row been placed on `pending_irq`, it would have
been vacuous by construction.*

**One confirmation worth recording as a confirmation:** the mask registers ARE plain
read/write for a 32-bit guest store (`:144-175`, plain assignment both directions, no gate)
— checked independently by the main loop and by a seat that tried to break it and could
not. **Row 2 is not vacuous.** The assertion was flagged as suspect precisely because the
analogous `pending_irq` assertion had come back wrong; this time it held, and saying so is
part of knowing what the coverage is.

#### *** THE PENDING ARM IS NOT UNTESTABLE, AND A SHIPPED ROW ALREADY PROVES IT. ***

Both the design and the seat that refined it reasoned from *"a guest can only CLEAR"* to
*"this arm is hard to pin"*. **A third seat opened the files and refuted the premise:
DEVICES set it, synchronously, inside a guest store.**

`dev_dreamcast_gdrom.c` reaches `SYSASIC_TRIGGER_EVENT` from `handle_command`, which runs
inside the guest's own store — and **`gdrom_default_probe.py`'s `accept event` row already
reads bit 14 at `0xa05f6900` and requires it SET.** A non-zero device-signature value is
available today, single-steppable, with shipped in-tree precedent.

*So the correction chain ran: I inferred "no positive row is possible" and wrote no row;
one seat corrected that to "pin the clear-only invariant"; a second corrected BOTH of us by
pointing at a row that has been pinning the device-set value all along.*

**And the MECHANISM behind the bit-32 gate, verified from source:** SH4 register-pair
stores are issued as **two 4-byte `memory_rw` calls** (`cpu_sh_instr.c:1478-1501`), so no
guest access can ever carry bit 32 — `len == 8` at this device has exactly one producer and
it is internal. That is why the gate works, and it means any `len`- or width-conditional
edit splits internal from guest traffic **in a way no guest-side row can express**.

#### Row 4 was the reason the pending arm went uncovered — amend the rule, not just the row

*"Pin survival, never `odata == 0` as a hardware value"* is right and it is what produced
the gap. Amended: **"...and where a DEVICE sets the register, pin the DEVICE-SET value."**
There is a live in-tree example to copy.

#### *** ROW 5 IS MIS-CLASSIFIED, AND THE ROUND HAS NO CLAUSE-(d) MUTANT AT ALL ***

The fix is a **pure deletion**. It introduces no predicate. So `r == 3` → `r >= 2` is not
guard GROWTH — it is **re-inserting a widened form of the REMOVED guard, which is floor
clause (b)**, not (d). Letting the round record claim (d) coverage on that row would be a
wrong record about the round's own floor compliance.

> **The honest (d)-analogue for a DELETION fix is: keep the deletion, and re-introduce a
> host kill under a DIFFERENT predicate** — e.g. `if (relative_addr >= 0x3c) exit(1);`.
> No row covers that today.

**Row 5 is also an IMPURE discriminator:** `0x0c` gives `r == 3`, which is `>= 2`, so the
mutant reddens Row 1 as well — a vacuous accept row would still leave the table looking
responsive. Use `if (r == 2)` alone so only the accept row can redden.

#### The requirement that mandated its own blind spot

**Row 2's "distinct NON-ZERO sentinels" wording guarantees blindness to zero-value
guards.** `if (idata) d->mask_13[r] = idata;` escapes it by construction — and writing 0 to
a mask is the guest's *normal* way to disable a bank. **This is the exact family this
project's measuring seats have already built twice** (`&& idata`, `odata != 0`). One
zero-write-then-readback row closes it and costs nothing.

#### The one attack that CANNOT be closed by readback, stated honestly

`(relative_addr / 4) & 3` → `% 3`. **One character, and it is the edit a maintainer makes
BECAUSE the guard was deleted:** *"nothing stops `r == 3` now and these are `[3]` arrays —
use `% 3`."* Smaller than the guard it replaces; no reviewer would stop it.

It PERMUTES indices, differently per group — `mask_13` → (1,2,0), `mask_11` → (2,0,1),
`mask_9` → identity — while `pending_irq` is unchanged, so the
`pending_irq[i] & mask_13[i]` pairing in `DEVICE_TICK` breaks and a guest that unmasks bank
0 receives bank 1's events.

> **No readback row can see it: write and read share the same index expression, so ANY
> BIJECTION on {0,1,2} is invisible.** Distinct sentinels detect COLLAPSE, not PERMUTATION.

*Incidental sharpness: had row 2 been placed on the `mask_9` group, it would be the
IDENTITY under this mutant — not merely invisible, literally unchanged.*

Closing it needs either a **free-running IRQ-delivery row** (the carrier's recipe, driven
by the synchronous GDROM path) or a **source-text presence pin** on the index expression,
which this harness already uses elsewhere. **Say which in the round record; do not leave it
implied** — and if delivery is ruled out of scope, say that too, because "the detector
covers the fix" would then be false about the very index expression the deletion unguarded.

#### Row 1 samples one eighth of its own obligation

It covers **8 of 64 killing addresses and 0 of the 192 outside them**. The window is 256
byte offsets; both directions is 512 accesses. **Sampling here is an unforced choice**, and
it leaves the de-escalation obligation discharged at one-eighth coverage. Sweep the whole
window, both directions.

#### Cheapest three changes, which kill seven of the eight attacks

1. full-window survival sweep, both directions;
2. all-writes-then-all-reads over all twelve implemented offsets with distinct sentinels,
   **including a zero write**;
3. one read-twice-equal row on `0xa05f6900` (closes read-to-clear).

Only the `% 3` permutation survives — **and it survives for a reason worth recording
rather than papering over.**

*Also noted in passing and worth its own line: `dev_dreamcast_asic.c:49` carries
`// #define debug fatal` — **already written, one `//` from live**. Uncommenting it makes
every unimplemented-offset access a guest-drivable unbounded flood, and `fatal()` cannot be
silenced by `-q`. Row 1 pins survival, and `fatal()` survives.*

### `asicbadaddr` — AUTHORITATIVE SUMMARY, superseding the six sections above

*Those sections are kept because they record HOW each point was reached and by which
seat. This is what the round should be worked from. Where a point below contradicts one
above, this one wins and the contradiction is named.*

**THE FIX.** Delete the whole `if (r == 3) { ... }` block, all five lines. Not just the
`exit(1)`.

**THE ROUND RECORD MUST SAY** (a) the check protected nothing even before the fix — no
reachable `case` yields `r == 3`, so it was a diagnostic wearing a bounds check's clothes;
(b) the invariant, structurally: *`r == 3` is exactly `(relative_addr & 0x0c) == 0x0c`, the
fourth word of every 16-byte group, and every implemented group is three consecutive words
at bases `0x00/0x10/0x20/0x30`*; (c) that the invariant must NOT become a runtime guard.

**THE KILLING SET IS 64 BYTE ADDRESSES**, not the 16 the first brief said — `relative_addr`
is not word-aligned.

#### THE DETECTOR — final requirements, each traceable to a named escape

1. **Full-window survival sweep, `0x00-0xff`, BOTH directions** (512 accesses). *Supersedes
   "byte offsets in at least two groups": that sampled 8 of 64 killing addresses and 0 of
   the 192 outside, leaving the de-escalation obligation discharged at one-eighth.*
2. **All twelve implemented offsets: ALL WRITES FIRST, THEN ALL READS**, distinct
   sentinels, **including a zero write**. *Three corrections in one row: interleaved
   write/read makes any single-target redirection self-consistent (so an aliasing mutant
   passes); one group tested thoroughly assumes the other two, but maintenance edits touch
   one arm at a time; and "distinct NON-ZERO sentinels" mandated blindness to
   `if (idata) ...` guards, which is how a guest normally disables a bank.*
3. **A `pending_irq` row.** *Supersedes "pending_irq cannot carry a row". It can, two ways:
   pin the DEVICE-SET value (a shipped row already reads bit 14 at `0xa05f6900`), and pin
   the clear-only invariant (store `0xffffffff`, require `0` back).*
4. **Read the same address twice, require equal** — closes read-to-clear.
5. **Pin the declined-read value as THIS MODEL'S DECLARED CONVENTION**, with the comment
   saying so. *Supersedes "never pin it at all", which was my over-application of "never
   pin it as a HARDWARE value" and left the default read entirely unguarded.*
6. **Accept-row discriminator: `if (r == 2) { ... exit(1); }` alone**, not `r >= 2`.
   *`r >= 2` also reddens the survival rows at `0x0c`, so a vacuous accept row would leave
   the table looking responsive.*

#### An empty column check 1 found — and a FALSE claim I made about it, corrected

The path x channel grid, built mechanically: **paths** = twelve `case` labels plus
`default:`; **channels** = one grep over the enclosing function, giving `fatal(`/`exit(`/
`debug(` (diagnostics), `memory_writemax64` (odata), the four register arrays, and
**`_tick(`** — four in-line `dev_dreamcast_asic_tick(cpu, d)` calls driving
`asserted_13/11/9`.

**The ASSERTION channel has no row.** The design's `pending_irq` row reads the PENDING
REGISTER at `0xa05f6900`; nothing tests whether the tick actually asserts IRQ 13/11/9 to
the CPU. Those are different observables — a guest can read a pending bit that was never
delivered. **Owed:** a row on delivery, not merely on the register.

*** AND THE FIRST VERSION OF THIS SECTION CLAIMED THE SUMMARY HAD "ZERO MENTIONS" OF THE
CHANNEL, WHICH IS FALSE. ***  I ran an `awk` range whose start pattern **did not match**,
so it returned 0 for every query — and I read that 0 as a finding. The real range has one
match, and even that is a substring hit on `pending_irq` rather than a discussion of
assertion.

> **A range that matches nothing reports zero for everything.** That is the same class as
> the unanchored `grep FAIL` that reported a phantom red earlier today: **apparatus that
> did not measure, read as a result.** Twice in one session, in opposite directions — one
> invented a failure, one invented an absence.

**What survives the correction, stated separately from what does not:**
* the assertion channel genuinely has no row — **that part holds**, and check 1 is what
  surfaced it;
* the summary did NOT "lose" the finding, and my claim that consolidation dropped it was
  wrong. It carries a `pending_irq` row; it simply does not distinguish the register from
  delivery.

*The check earned its keep here. The narrative I hung on it did not, and the difference
was one grep at the right anchor.*

#### THE FLOOR, stated correctly for a DELETION fix

* **(a)** trivially met — the trigger rows report `died` on committed HEAD.
* **(b)** reinstate `exit(1);` verbatim at the one site.
* **(c)** identity rows — reuse the existing `live`/`devsig` names.
* **(d)** *** NOT `r == 3` -> `r >= 2`. *** That is (b) with a new name. The fix adds no
  predicate, so (d) is **re-introduce a host kill under a DIFFERENT predicate**, e.g.
  `if (relative_addr >= 0x3c) exit(1);`. **Do not let the record claim (d) coverage on the
  `r >= 2` mutant.**

#### KNOWN, ACCEPTED, AND TO BE STATED IN THE PROBE HEADER

`(relative_addr / 4) & 3` -> `% 3` **cannot be closed by any readback row**, because write
and read share the index expression and every bijection on {0,1,2} is therefore invisible.
Closing it needs a free-running IRQ-delivery row or a source-text presence pin. **Decide
which and say so; do not leave it implied** — and if it is ruled out of scope, say that
too, because "the detector covers the fix" would then be false about the very index
expression the deletion left unguarded.

**Write the MUTATION CONTRACT in the probe header**: which edits this detector is designed
to catch. A detector that says so is falsifiable; one claiming completeness is not.

### `gdromcondlies` pass 1 — and TWO of my own premises came back over-stated

*Nine seats fired. Seven scriptable answered by the time this was written; both Anthropic
seats still running. Verdicts: kimi ONE ROUND, glm FIX-BOTH-AS-ONE-ROUND, deepseek
APPROVE, minimax APPROVE, agy GO-WITH-CHANGES.*

**The brief asked seats to check its PREMISES rather than its derivations**, citing the
round where seven of nine confirmed a premise stated wrongly. That instruction worked:

**PREMISE 1 was over-read, and the correction is about PROVENANCE not conclusion.** I
wrote that Site A is *"already half-fixed and nobody noticed"* — read branch's `exit(1)`
commented out, write branch's live — and inferred *"someone already decided the kill was
wrong here"*. The asymmetry is real. **The inference is stronger than the evidence.** The
read message ends in a question mark (`"Read from GDROM_UNKNOWN_0x88?"`), which reads like
a debugging probe: someone commented out the exit to see what reads do and never restored
it. *Consistent with* that decision, not *proof of* one. **The conclusion still holds; the
warrant I gave for it does not** — which is the same class as the NetBSD exhibit, one
severity lower.

**PREMISE 5 WAS WRONG IN A WAY THAT CHANGES WHAT THE ROUND OWES.** I wrote that removing
these guards *"deletes a tripwire that used to announce itself loudly"*. It does not: the
`fatal()` REMAINS at both sites and keeps logging the unmodelled value. **What is removed
is process termination, not the announcement — the tripwire still fires, it just stops
shooting.**

> **So the de-escalation cost here is genuinely LOWER than in `#447`/`#462`**, and saying
> so is not a shortcut. There, the fix converted a loud kill into a SILENTLY refused
> write, which is exactly why those rounds owed accept rows. Here a future guard-widening
> still logs. The accept side must still prove **correct behaviour survives** — it does
> not additionally have to prove the announcement survives.

*That distinction is worth keeping as a rule: the de-escalation clause is triggered by
losing the ANNOUNCEMENT, not by losing the KILL. A fatal->survive fix that keeps its
diagnostic has paid part of the cost already.*

**AND A STRUCTURAL PROBLEM AT SITE A THAT NO ACCEPT ROW MAY BE ABLE TO SOLVE:** its write
branch contains **no store at all** — not even for the legal value `0xb`. Writing `0xb`
today does nothing observable; the register's entire write behaviour is *"kill the host
unless the value is 0xb"*. De-fatalising it makes the whole branch a no-op, so **there may
be nothing for an accept row to observe.** That is the carrier's own
*"write-1-to-keep / read-only / never-set-by-device bits cannot carry an accept row"*
situation, and if it holds the round must SAY so rather than ship a row that passes
vacuously.

### *** PREMISE 1 IS REFUTED BY GIT, NOT MERELY OVER-READ — and the truth is a BETTER argument ***

One seat called my *"someone already decided the kill was wrong"* inference over-read.
A second **settled it by measurement**: `git log -L 676,700:src/devices/dev_dreamcast_gdrom.c`
returns **exactly one commit — `39748e3 Import GXemul 0.7.0 (unmodified upstream
baseline)`.** The commented-out `exit(1)` is verbatim upstream; **this fork has never
touched those lines.** "Already half-fixed" is false.

**And the real explanation is stronger than the one I invented.** Three lines later,
`GDROM_STAT` (`:695-696`) has its commented-out exit in the **WRITE** branch — the
opposite disposition, same file, same style. That is a **reachability trace**: upstream
commented out whichever exit he happened to HIT while developing against one driver.

> So the live `exit(1)` at `:685` survived **because that driver never wrote a non-`0xb`
> value — not because such writes are unthinkable.** That is a better warrant for
> de-fatalising than "someone already decided", and it is checkable.

*Three seats, three levels: one accepted the premise, one called the inference weak, one
ran `git log -L`. **The command took seconds.***

**Site A is not half-FIXED, it is half-de-fatalised and UN-LATCHED.** `:680`'s `fatal()`
has no `warned` bit, so a guest polling `0x88` floods stderr unboundedly today. Same at
`:695`. If this round touches Site A it must latch the read branch too.

### `gdrompionull` — IN WORK: the fix and its detector shipped as #465

*This heading read "open, NEW" until 2026-08-26, after the fix had shipped. The
precommit row-state check caught it and its wording is the reason the check exists:
**this file is the carrier's FIRST-STOP live queue, so a stale `open` here offers
shipped work to a fresh session.** Same defect class as the `sh4dmacie` row settled
earlier the same day — two records disagreeing about whether something is done.*

**Shipped in `#465`:** the `free_data()` helper (releases `data` and `data_len`
together, so every release path restores the invariant before it returns), the
re-pinned detector at 13/13, and a `gate_sh_rounding.sh` section that actually runs
it — it was wired into **no gate at all** before this round.

*** THIS ENTRY CARRIED TWO CLAIMS THE PASS-2 PANEL REFUTED, AND THEY SURVIVED THE
COMMIT THAT CORRECTED THEM EVERYWHERE ELSE. *** It said the helper makes the state
"unrepresentable" — an overclaim the source comment itself now disclaims — and it
described the owed rows as **L1**, which is a category error since L1 means finish
in-round. `5b5089d` fixed both in the README, CHANGELOG, probe header and source
comment **and missed this file** — the one the carrier names as FIRST STOP each
session. That is the project's own rule 2 (*grep for a claim's siblings before
calling it fixed*) failing inside the commit that applies rule 2. Found by the opus5
seat, which read the committed tree rather than the diff.

**AND THE `m_ret415` FRAMING WAS WRONG IN A WAY ONLY A BUILD COULD SHOW.** It is not
a one-word mutant against the shipped fix — against the shipped tree it takes THREE
edits (drop the helper, restore the tail assignment, then `return`). The opus5 seat
built the real one-word mutant directly against shipped code and measured:

    Md_nolen   helper kept, only `d->data_len = 0;` deleted   10/13 + 7/9  KILLED
    Mret429    shipped + `break;`->`return;`                  13/13 + 8/9  HARMLESS
    Mtailret   the REJECTED tail design + the same `return`   13/13 + 6/9  SIGSEGV

**Same one word, opposite outcome** — the addition licence's measured delta,
reproduced against the shipped tree. `Md_nolen` is the real clause-(d) mutant AND
clause (b) at once (verbatim reinstatement at every fixed site, since both go through
the helper), and it is strongly killed. **`free_data()` runs at the ENTRY to
`handle_command`, before any switch arm, so bypassing the tail cannot reach it.**

**STILL OWED — above-floor coverage debt, now PRICED:** one anchor row per arm
(`cnt post`: read CNTHI back, require 0). It is the only row of nine that reds under
`Mret429`; every other row on that route is SURVIVE-ONLY and blind to the bypass by
construction — vacuity-floor clause (f) exactly. ~30 s per arm. **The seat measured
ONE of the two arms and said so: its `Mret420` came back clean because its probe has
no row reaching that arm — target-not-reached, NOT equivalence.** The owed rows must
cover both.

Instruments preserved at `regress/artifacts/gdrompionull/opus_p2_20260826/` — 26
artifacts including `mism_probe.py`, `mutate.py` and the frozen driver, so this table
is reproducible rather than merely checkable.

**A host death reachable with LEGAL VALUES ONLY, and with no diagnostic at all.**

* `COND_DATA_AVAIL` is `0x08`, and **`0xef & 0x08 == 0x08`** — so writing the *legal*
  value `0xef` sets the emulator's "there is data to read" flag.
* `handle_command` frees `d->data` and NULLs it, but **never resets `d->data_len`**.
* The PIO read guards only `if (d->cur_data_offset < d->data_len)` and then dereferences
  `d->data[...]` — **verified by opening `:611-613`: there is NO NULL test.** The DMA arm
  got one in `#462`; **its PIO twin did not**, because it relies on `cond & COND_DATA_AVAIL`
  — a flag the guest can set back.

Sequence, legal values throughout: stage TOC (`data_len = 408`) → stage Mount `0x70`
(frees `d->data`, `data_len` stays 408, bit 3 cleared) → write `COND = 0xef` (bit 3 back
on) → read `+0x80` → `d->data[0]` on NULL. *A reading, not a measurement — it needs a
rung-3 probe.*

*** "FOUR STORES AND A LOAD" WAS WRONG, AND THE PHRASE WAS LOAD-BEARING IN THE QUEUE
RANKING. ***  The probe is **18 guest accesses** by this route, or **9** by the cheaper
one below -- not four.  The queue table used "a four-store sequence" to argue this item
is less reachable than `asicbadaddr`; **the ranking direction survives** (that one needs
no staging at all) **but the number it rested on did not**, and a number quoted inside an
argument is part of the argument.

*** AND THERE IS A ONE-COMMAND ROUTE, NEEDING NO DISK IMAGE AND NO PRIOR STAGING. ***
Verified by opening both files: `diskimage.c:1566-1571` returns **0 non-fatally** when no
IDE disk is attached, and `dev_dreamcast_gdrom.c:441-447` frees `d->data` *after*
`alloc_data` has already set `data_len`.  So on a bare `-E dreamcast <kernel>` --
exactly how this project's own gdrom probes invoke it -- **command `0x30` ALONE reaches
(data NULL, data_len 2048)**.  The OB-20 breaks sit BEFORE `alloc_data` and need a prior
allocating command; this one does not.  *It is also the COMPLIANT-GUEST route, which is
what `#462`'s own research established Linux takes.*

> *** AND IT CONSTRAINS `gdromcondlies` DIRECTLY: the naive Site B fix — "decline, but
> keep `d->cond = idata`" — turns this from ONE legal value into EVERY unmodelled value
> with bit 3 set. That round would become the one that WIDENED a NULL-deref primitive. ***

### `gdromcondlies`: leave `d->cond` UNCHANGED on decline — and this REFUTES a seat

One seat recommended keeping `d->cond = idata` because *"the store already happens
unconditionally"*. **That is the wrong disposition, and the reason is local and
checkable rather than a matter of taste:** `cond` is not a passive shadow — **bit 3 is
INTERPRETED as a readiness flag gating a pointer path.** Storing an arbitrary guest byte
hands the guest a direct write to internal readiness state.

"Unchanged" claims strictly less than "stored": it invents no state the command sequencer
never produced. Mechanically, move `d->cond = idata;` into the two accepting arms. If
documentation ever appears saying the register latches, it is a one-line reversal.

### Two detector traps in that round, both of which produce rows that LOOK like success

**1. Do NOT pin `d->stat`.** Reading `+0x8c` calls `dreamcast_gdrom_update_stat()`, which
overwrites `d->stat` **unconditionally** before returning it. The `d->stat = 0` in the
`0xa0` arm is invisible through the register. **That row would be born vacuous.**

**2. THE LATCH-ORDERING HAZARD.** Every accept row here asserts the **absence** of a
diagnostic at a **warn-once** site. If any decline row at the same site runs earlier in the
same emulator session, the latch is already set, the growth mutant's diagnostic is
suppressed, and **the accept row stays green under its own growth mutant — vacuous, in the
direction that looks like success.** Each accept row needs its OWN session.

*Note this cuts AGAINST the probe's own one-session argument, which exists to make several
rows observe ONE event. Both rules are right for different row kinds: share a session when
rows must describe the same event; isolate when a row asserts the ABSENCE of something a
latch can suppress. The round must say which rule governs which row.*

### *** THE WARN-BIT PRE-SET TRIGGER FIRES IN THIS ROUND, NOT LATER ***

`gdromwarnbits` is filed with a trigger set **at the seventh bit**. Six of eight are used
and `warned` is `uint8_t`. `gdromcondlies` needs **two new latches, and really three**
(Site A's read branch is an unlatched flood today). **6 + 3 = 9, and `1u << 8` truncates
to 0 — the latch never sets and the diagnostic FLOODS**, which is exactly the failure the
file predicts in its own comment.

**So the enum-of-bit-positions conversion is due IN that round, not filed.** The precedent
is `dev_sh4.c:124`, where the same pre-set trigger fired on a tenth class and the
conversion happened. *A trigger that is not honoured when it fires is not a trigger.*

### Queue order after `#462`, and one item CONSTRAINS another

*Ordered by the carrier's rule — a witness makes an item eligible; SEVERITY and gate
blind-spots order it — with one hard dependency that overrides preference.*

| # | item | why here |
|---|---|---|
| 1 | **`asicbadaddr`** | single guest **LOAD**, 64 addresses, **no staging at all**. Design converged and attacked; witness is one constant away in an existing probe. Most reachable defect on the queue by a wide margin |
| 2 | **`gdrompionull`** | NULL dereference reachable with LEGAL values and **no diagnostic** — worse to diagnose than a clean `exit(1)`, but needs a four-store sequence, so less reachable than (1) |
| 3 | **`gdromcondlies`** | **DESIGN-CONSTRAINED by (2)** — see below; sequencing after (2) is safer but it is NOT gated on (2) shipping |

*** THIS TABLE SAID "BLOCKED BEHIND (2)" AND MY OWN PROSE TWO LINES DOWN CONTRADICTED
IT. ***  The adjudicating seat caught the disagreement: the row implied `gdromcondlies`
is gated on a commit that has not happened, while the paragraph below correctly says it
is not.  **It is a DESIGN CONSTRAINT, and the constraint is already written down and
checkable.**  Doing (2) first is safer SEQUENCING — it removes the primitive, so a slip
in (3) cannot widen it — but (3) may proceed whenever it honours the constraint.

> **The dependency is real and one-directional.** `gdromcondlies`' naive Site B fix —
> *decline but keep `d->cond = idata`* — would turn `gdrompionull` from ONE legal value
> into EVERY unmodelled value with bit 3 set. Shipping (3) before (2) is understood makes
> (3) *the round that widened a NULL-deref primitive*.
>
> It does not require (2) to be FIXED first, only that (3) honours the constraint: **leave
> `d->cond` unchanged on decline.** Recorded here so a future round cannot reach the
> obvious fix without meeting the reason it is wrong.

*And (3) additionally carries a hard in-round prerequisite: the `gdromwarnbits` enum
conversion, whose pre-set trigger fires there. That is a cost of (3), not a separate item.*

**Reachability is part of severity, which is why (1) outranks (2) despite (2) being a
memory-safety defect and (1) a controlled `exit(1)`.** A defect needing no staging is
available to any guest that touches the window; one needing a four-step command sequence
is available to a driver that is already doing something specific. *Stating the trade
rather than asserting the order, because the two pull in opposite directions and a future
reader deserves to see that they were weighed.*

### `gdromcondlies` pass 1, the flagship half — including a records defect in my own brief

**MY BRIEF SAID "quoted verbatim" OVER AN ABRIDGEMENT.** Site B's real comment is
**thirteen lines**; I reproduced **two**, with no ellipsis, under a heading claiming
verbatim quotation. Content-equivalent, but *"verbatim" over a condensation is this
project's own records class* — and the seat that caught it was reading the file precisely
because the brief invited premise-checking.

#### Q2 is SETTLED by in-tree precedent, not "unknowable" — and the argument is better than mine

**`dev_wdc.c` is the tree's OTHER ATA/ATAPI device and it already survives this exact
situation:** an unimplemented command sets `d->error |= WDCE_ABRT` and calls
`fatal("[ wdc: WARNING! Unimplemented command 0x%02x ... ]")` — **no `exit`**. Verified by
opening it. Unknown SET FEATURES subcodes just abort. *And `0xef` — Site B's other legal
value — IS SET FEATURES.* Surviving an unknown command is the established behaviour of
this tree's ATA modelling.

> **BUT DO NOT PORT wdc's ABRT STATUS BITS, and the reason is mechanical rather than a
> matter of taste:** this model has no error register (`0x84` is write-only-zero REGX),
> and `dreamcast_gdrom_update_stat()` regenerates `stat` on **every** STAT read — so a
> latched error bit would be overwritten before a guest could see it. **The ABRT route has
> nowhere to live without inventing modelling**, which the absent-oracle record forbids.

**AND THE SHARPEST ARGUMENT FOR "LEAVE `d->cond` UNCHANGED" IS NOT THE HAZARD — IT IS THAT
THERE IS NO BEHAVIOUR TO PRESERVE.** Pre-fix, the store at `:720` is observable only for
ACCEPTED values, because **every declined path exits the process**. So **no surviving
execution has ever observed a stored illegal value.** "Leave unchanged" therefore changes
zero observable behaviour of any execution that lives — which defuses the strongest
argument for keeping the store, without needing the NULL-deref hazard at all. *Two seats
reached the same disposition by different routes; this one needs less to be true.*

#### Site A CAN carry a failable accept row — my open structural question, answered

I recorded that Site A might have nothing to observe, since its write branch stores
nothing even for the legal `0xb`. **It can:** `0xb` reaches the predicate's operand
directly via an ordinary store, so the write-1-to-keep/read-only carve-out does not apply.
The observable is **content-keyed diagnostic ABSENCE with an in-session positive control**
— store `0xb`, then store `0x0a`, and require no line naming `0xb` and exactly one naming
`0xa`.

> **PREREQUISITE, and it is a design change not a row design: Site A's diagnostic must
> CARRY THE VALUE.** It is currently `"[ Write to GDROM_UNKNOWN_0x88: TODO ]"` with no
> `%x`, unlike COND's. Without the value, a growth mutant makes the `0xb` store consume
> the once-latch and print **the same text** a control store would — so **count-keyed rows
> stay green**. Content-keyed rows survive that interaction; count-keyed rows do not. *The
> `dma alias` structural blindness again, in a new costume.*

#### The decline set must include NEIGHBOURS, not just far-off values

The least-observable weakening of an accept-list test is a **mask widening**
(`idata == 0xa0` -> `(idata & 0xf0) == 0xa0`; `!= 0xb` -> masked forms). A far-off illegal
value like `0x77` stays declined under those and the row goes **green**. So the decline
rows must use **`0xa1` at COND and `0x0a` at 0x88** — neighbours that a widened mask
would swallow.

*And avoid qualify-mutants like `&& d->cmd_count == 0` when naming kills: on a fresh device
they are EQUIVALENT, which is the `#449` measured-equivalence hazard. The drift and width
forms are non-equivalent at these sites by construction.*

#### TWO SEATS DISAGREE ON THE READ-BRANCH FLOOD, and the stopping rule settles it

One seat: *"if this round touches Site A it must latch the read branch too"* (it is an
unlatched flood today). The other: **FILE it** — pre-existing, an unlatched diagnostic
rather than a kill, and the stopping rule fixes only a measured false pass or a wrong
record.

**FILE is right**, and the bit-budget argument that seemed to force the issue dissolves:
latching it would be the NINTH bit and `1u << 8` truncates — *but the enum conversion is
already due in-round*, after which the ninth bit is free. **So the budget does not decide
it; the stopping rule does.** Recorded because "we had to, the bits ran out" would have
been a wrong reason for a right answer.

#### Three more corrections from the same premise audit

**"Nobody noticed" was false, and the record proves it.** `#461`'s census already counted
**three disabled `exit(1)`s** in this file, and `gdromexitsix` names the WRITE kill by its
diagnostic. The asymmetry was noticed and recorded; what had not happened was a decision
to act on it. *My brief turned "not yet acted on" into "not seen", which the tree's own
records refute.*

**A THIRD in-tree precedent for decline-and-survive, in this same file:** `GDROM_REGX`
already declines unexpected values with `debug()` **and no store**. So the warrant for the
fix is **this file's own later policy** (`#447`, `#459`, `#460`, `#461`, `#462`) — not the
upstream comment I built the argument on. *Three seats independently moved the warrant off
that comment; the third supplied the replacement.*

**AND `d->cond = idata` IS NOT A NO-OP, which sharpens the disposition.** `COND_DATA_AVAIL`
is `0x08`, so the stored value directly drives the flag the data port consults: `0x08`
SETS it, `0x00` clears it, `0xa0` clears it, `0xef` sets it. Today the process dies before
a guest can observe any of that. **After a bare `exit(1)` deletion, it can** — which is
the same conclusion the NULL-deref analysis reached, arrived at without needing the deref
at all.

#### A fourth mutant shape, and a 2-1 split that the RULE settles rather than the count

**OVER-BROAD DISPATCH:** `if (idata == 0xa0)` -> `if (idata != 0xef)`. Both accept rows
still pass — `0xa0` takes the first branch, `0xef` the second — while **every illegal
value now takes the `0xa0` branch**, setting `busy |= 0x08` and zeroing `cmd_count`
instead of declining. A guest's garbage byte silently opens the packet FIFO.

A survival-only decline row cannot see it: the host survives, by design. **Only a
CONTENT-KEYED decline row catches it** — one asserting the diagnostic naming the value
actually printed. *That is the third independent argument this round has produced for
value-bearing, content-keyed diagnostics over count-keyed ones.*

**AND THE READ-BRANCH QUESTION IS NOW 2-1 FOR FIXING IN-ROUND** — two seats say latch
Site A's unlatched read `fatal()` as part of this work, one says FILE it. **The count does
not settle it and is not allowed to:** this project resolves disagreements by measurement
or by rule, never by vote, and the majority has been wrong on mechanism repeatedly.

> **The rule settles it: FILE.** The read-branch flood is pre-existing, is a diagnostic
> rather than a kill, and is neither a measured false pass nor a wrong record — so the
> stopping rule applies. *The seat arguing to file gave the weaker-looking answer and the
> correct one.*

*And the bit-budget argument that appeared to force the in-round fix dissolves once the
enum conversion lands, which is due in-round anyway — so the budget never decided it
either. Recorded because "we had to, the bits ran out" would have been a wrong reason for
a right answer, and a wrong reason gets reused.*

### `gdromcondlies` — AUTHORITATIVE SUMMARY, superseding the pass-1 sections above

*Work the round from this. The sections above record HOW each point was reached and by
which seat; where this contradicts them, this wins and says so.*

**SCOPE: ONE round, both sites** — same file, same class (unmodelled VALUE at an
implemented offset ends the host), one fix design, one detector, no new oracle. Nine seats,
no dissent on joining.

**BLOCKED BY A CONSTRAINT, not by another round finishing:** leave `d->cond` UNCHANGED on
decline. Move `d->cond = idata;` into the two accepting arms. The naive fix — decline but
keep the unconditional store — would widen `gdrompionull` from one legal value to every
unmodelled value with bit 3 set.

**THE FIX.** Both sites: keep the accept list, make the else-arm a **latched,
value-bearing** `fatal()` decline, and change no state on decline.

* **Site A's diagnostic MUST GAIN THE VALUE** (`%x`). It currently reads
  `"[ Write to GDROM_UNKNOWN_0x88: TODO ]"` with no value, and without it the legal `0xb`
  store consumes the once-latch and prints **the same text** a control store would — so
  count-keyed rows stay green under a growth mutant.
* **Site A's READ branch: FILE, do not latch in-round.** Pre-existing unlatched flood, not
  a kill; the stopping rule governs. *Two seats wanted it in-round; the rule decided, not
  the count.*

**IN-ROUND PREREQUISITE — the `gdromwarnbits` enum conversion.** Six of eight bits used,
`warned` is `uint8_t`, this round needs two more. Its pre-set trigger is AT THE SEVENTH
BIT and this round is the seventh. Precedent: `dev_sh4.c`'s enum conversion when its own
pre-set trigger fired.

**THE WARRANT IS THIS FILE'S LATER POLICY** (`#447`, `#459`, `#460`, `#461`, `#462`), and
three in-tree precedents — **not** the upstream commented-out `exit(1)`, which `git log -L`
proves this fork never touched:
* `dev_wdc.c` — the tree's other ATA/ATAPI device — survives an unimplemented command
  (`error |= WDCE_ABRT` + `fatal()`, no exit). `0xef` IS SET FEATURES.
* `GDROM_REGX` in this same file already declines unexpected values with `debug()` and no
  store.
* `#461`/`#452`: declined control-window writes are ignored.

**DO NOT port wdc's ABRT status bits** — no error register exists here, and `update_stat()`
regenerates `stat` on every read, so a latched error would be overwritten. The route has
nowhere to live without inventing modelling.

#### The detector

**Accept rows, each with the growth mutant that must redden it:**

| row | expects | reddens under |
|---|---|---|
| `0xa0` (row EXISTS) | BUSY bit 3 set | `0xa0` -> `0xa1` drift; or qualifying on `len == 1` (the row's store is 16-bit) |
| `0xef` (**must be built** — no `0xef` row exists anywhere) | SYSASIC pending bit at `0xa05f6904` | `0xef` -> `0xee`: no event fires |
| `0xb` at Site A | no line naming `0xb`; exactly one naming the control value | `!= 0xb` -> `!= 0xc` drift |

**Decline rows must use NEIGHBOUR values — `0xa1` at COND, `0x0a` at Site A.** A far-off
value like `0x77` stays declined under a mask-widening mutant and the row goes green.

**A cross-site row driving BOTH sites in one session** is mandatory: it is the only thing
that catches the two new latch bits being collapsed onto one.

**TWO TRAPS THAT PRODUCE ROWS LOOKING LIKE SUCCESS:**
1. **Do not pin `d->stat`** — reading `+0x8c` calls `update_stat()`, which overwrites it
   unconditionally. Born vacuous.
2. **Each accept row needs its OWN session.** They assert the ABSENCE of a diagnostic at a
   warn-once site, so a decline row running earlier in the same session sets the latch,
   suppresses the growth mutant's diagnostic, and leaves the accept row **green under its
   own mutant**. *This cuts against the probe's one-session rule, which exists so several
   rows describe ONE event. Both are right for different row kinds; the round must say
   which governs which row.*

**Both sites' pre-fix kills are READINGS, not witnesses.** Ladder clause (i) requires
measuring each on the committed build BEFORE the edit — one store each, and each score
names its artifact.

### The scale of this defect class, stated so the queue is not mistaken for the population

`census_exits.py` over `src/devices/`, run 2026-08-24:

| kind | direct | macro | total |
|---|---|---|---|
| **ACCESS** — inside a `DEVICE_ACCESS` handler, so a guest load/store reaches it | 86 | 5 | **91** |
| HELPER — a plain function, guest-reachable only if a handler calls it | 67 | 34 | 101 |
| INIT — device construction; terminating here is usually CORRECT | 25 | 144 | 169 |
| | | | **361** |

**Ninety-one guest-reachable process-terminating sites remain**, and the script is explicit
that HELPER reachability is unresolved — it does not walk the call graph — so the true
guest-reachable population is **at least 91 and at most 192**.

**Against that: `#462` removes 2, `asicbadaddr` removes 1, `gdromcondlies` removes 2.**
Five sites, out of ninety-one at minimum.

*Recorded because a queue of four named rounds reads like a nearly-finished job, and it is
not one. The rounds are not sampling at random — each was chosen because a guest reaches
it cheaply — but the class is large and the honest framing is that this is early work on
it, not the tail.*

**And the script declines to guess, which is why its number is usable:** it counts SITES,
not defects, and says so — *"whether a site should stop the emulator depends on its
semantics, which a script does not have"*. Every one of the five above needed a human
reading to decide it was wrong to terminate; `:625`'s `Too much GDROM_DATA?` needed the
same reading to decide it was RIGHT to keep. **A census that classified for you would be
faster and would have condemned that one.**

#### *** THE `•` DISCRIMINATOR I FILED IS REFUTED ON ITS THIRD INSTANCE. ***

I recorded that kimi's FINAL answer is marked with a `•` bullet at column 0 while trace
lines are plain — **observed twice, explicitly recorded as "not proven stable"**. The
third panel refutes it: that file has **twelve** `•` lines and they are ALL trace,
including one reading *"• VERDICT: pending three one-line premise checks I refuse to take
on faith"* — the seat declining to answer until it had checked, which is exactly the
behaviour the brief asked for and precisely what a marker-based extractor mistakes for a
verdict.

**The real structure is POSITIONAL, not typographic: kimi streams its reasoning and the
answer is at the END of the file.** That is the discriminator `seat_verdicts.py` already
uses elsewhere, so no new mechanism is needed — and it explains why the marker looked
right twice.

*Recording the refutation is the point. The filing said "two instances is enough to act on
and not enough to assert", and acting on it would have meant coding a rule that fails one
panel in three. **A hedge that is never revisited is just a wrong rule with an apology
attached.***

#### And kimi's answer, once found, carried two mutants nobody else named

* **OVERFIT DECLINE.** Accept exactly the values the detector sweeps and `exit(1)` on the
  rest. Every swept value passes; anything unswept still kills. **Defence: sweep at least
  four NON-ROUND values** — a detector using `0x00/0x01/0xff` is trivially overfitted
  against.
* **DELETE THE `0xef` ARM** (two lines), or flip `0xef` to `0xfe` (one byte). `0xef` then
  declines. Caught only by the `0xef` accept row — **which does not exist anywhere today**
  and which this round must build.

**And it reached Site A's degeneracy from the opposite direction to the flagship seat:**
since `0xb` does nothing observable, a "repair" that declines **all** values uniformly —
including `0xb` — is behaviourally indistinguishable from the correct fix. One seat argued
Site A CAN carry an accept row (content-keyed diagnostic absence); this one argues the
repair itself is degenerate there. **Both are right, and together they define exactly what
that row can and cannot claim.**

### The compiler will not catch a repair rendered DEAD — measured, not assumed

`M3` moves `#462`'s `idata = 0` to AFTER its `break`, making it statically unreachable.
**The build produced ZERO warnings**, and so did the baseline, so nothing was lost in
noise.

Characterised rather than left as "gcc did not warn":

* the actual compile line is `-Wall -Wextra -Wshadow -Wcast-align -Wstrict-aliasing`
  at `-O3 -DNDEBUG`;
* **`-Wunreachable-code` is a NO-OP in this toolchain.** Proved with a minimal case —
  `int f(void){return 1; return 2;}` under `gcc 15.2.1` with `-Wall -Wextra
  -Wunreachable-code` emits nothing. **Adding the flag would not help**, which is the
  part worth knowing: the obvious remedy is already unavailable.

> **So for the "a maintenance edit renders the repair dead" class, the DETECTOR is the
> only line of defence.** There is no build-time fallback, and there is no flag to turn
> on.

*This is why `M3` earns its place in the table even though it looks like a trivial
variant of `M1`. `M1` deletes the statement; `M3` leaves it visible in the source while
making it do nothing — and a reviewer skimming the diff sees `idata = 0;` right there.
The compiler is silent, the source LOOKS correct, and only a row that reads `+0x18` after
the decline can tell the difference.*

### `gdromdmaclear` — open. The ONE escape the capped ask-again found, and why it is FILED

**The rule was followed exactly: one ask-again against a clean 52-row table, capped at one
per detector per round.** Six seats answered, one was DOWN (below). Three reported a
surviving mutant; one of the three is real.

**THE ESCAPE.** On a decline path, CLEAR an already-pending GD-ROM DMA completion:

```c
if (d->data == NULL) {
        /* existing latched diagnostic */
        clear_pending_gdrom_dma_completion();   /* the mutant */
        idata = 0;
        break;
}
```

Plausible as "failure cleanup" — stopping a declined launch from appearing complete.

**`nodata quiet` should catch it and cannot, for a reason worth keeping:** that row proves
a decline does not **SET** the completion bit. M8 measured that transition (clear -> set).
This mutant runs the OPPOSITE transition (set -> clear), and because every `session()`
forks a fresh emulator, nothing is pending when the row runs — so clearing a bit that was
never set is unobservable. **A row can pin one direction of a two-way transition and read
as though it pinned both.**

**Codex's construction does not work as written, and checking that is what found the
cheaper one.** It proposed: complete a valid DMA, then trigger the no-data decline. But
**the success arm does not free `d->data`** — only `handle_command` does — so a second
trigger SUCCEEDS again rather than reaching the no-data arm. Reaching it after a success
needs a whole second command staging to null `d->data`.

> **But the ARMING arm is reachable cheaply, and it is the same class:** after a
> successful DMA, write `+0x0c = 0` to break the arming, trigger `+0x18`, and require the
> SYSASIC completion bit **still set**. Three stores on a session that already exists.

#### Why this is FILED and not fixed, when the ask-again rule says "add a row"

The rule reads *"something found, row added under L1, done"* — and it presumes the row can
be **measured** inside the round. Here it cannot, and that is decisive:

* the detector is **ABOVE the vacuity floor** — clauses (a), (b), (c) and (d) are
  **discharged for the `idata` and operand effects** (`M6`, `M12`, `M11`), but *** (d) IS
  NOT FULLY DISCHARGED: NO MUTANT NULLS THE **PRINT** EFFECT, and `Mf` is owed for it —
  see `lethalonly`'s reversal, which is this same file asserting the opposite. *** The
  original sentence, kept because two entries claiming opposite things about one floor
  clause is the defect worth remembering: clauses (a), (b), (c) and (d) are all
  discharged by measurement, so this is coverage debt by the carrier's own disposition;
* a row added now would ship **without a measured kill**, because proving it non-vacuous
  means building the clearing mutant and re-running the table — three hours;
* **adding an unmeasured row to satisfy a rule about rows is precisely the vacuity that
  rule exists to prevent.** This round has spent a day refusing rows that merely exist.

*Filed with the construction, the cheap variant, and the reason the existing row misses
it, so the next round starts from a design rather than a rediscovery.*

### SEAT DOWN, and it is the failure mode the carrier warns hardest about

**`ollama_glm` produced NO ANSWER in a 114,723-byte file — the LARGEST in the panel.** It
spent its whole budget on hidden reasoning and was cut off mid-sentence, with no verdict
and no answer structure. **A size check would have scored it the best answer of the nine.**

Distinct from the recorded classes: not a quota wall (no notice), not a stall (it produced
114 KB), not a transport failure (the daemon answered and the other two cloud seats
returned). `seat_verdicts.py` caught it as *"spent its whole budget on hidden reasoning"*
and reported SEAT DOWN. **Named here because a seat that did not answer is never
agreement.**

#### An ask-again candidate REFUTED by a measurement already in hand

A seat proposed, as a missed mutant, *"move the `Transfering` diagnostic back ABOVE the
`d->data == NULL` test — so the case block reads top-down"*. Plausible, and it names the
round's own third change.

**It is caught, and the proof was already taken.** `probe_pre51.raw` **IS** that build —
the fix present, the diagnostic not yet moved — and on it `nodata notx` reads
`1` against a wanted `0`, the SOLE red of that run. On the moved build the same row reads
`0`. The reversion reddens exactly one row, by construction.

> *** AND THE ARTIFACT THAT REFUTES IT IS THE ONE I MISLABELLED. ***  That log was
> captioned "PRE-FIX" in two score tables until a seat opened it and found the host
> surviving. Correcting the label to "PRE-MOVE" is what makes it legible as **a mutant
> measurement for the diagnostic-position edit** — effectively a thirteenth mutant, taken
> before the table existed.

*The correction did not merely fix a caption; it revealed what the artifact was for. A
mislabelled measurement is not just wrong about itself — it is unavailable as evidence for
anything else, because nobody looking for that evidence would think to open it.*

**Recorded as REFUTED rather than filed.** An ask-again candidate that an existing
measurement disproves is a result, not debt — and saying so costs one grep, where filing
it would have put a phantom escape on the queue for a future round to chase.

### *** TWO OF MY OWN DISPOSITIONS CONTRADICTED EACH OTHER, IN THE SAME HOUR ***

A seat caught it and it is exact:

* `arm count2` / `arm enable2` were **ADDED in-round**, pinning *"count=2 enable=1 must
  still be REFUSED, not widened into accept"*.
* `gdromdmaguard` was **FILED**, on the stated ground that *"it tests the guard does not
  accept too much, which is a DIFFERENT PROPERTY from the two this round repairs. The
  stopping rule governs."*

**Those are the same property, on the same predicate.** The filing reason was wrong, and
it is the kind of wrong that reads as principled.

**And the added rows do NOT cover the filed one** — computed, not assumed:

| point | shipped `== 1 && == 1` | `<=` variant | `count && enable` |
|---|---|---|---|
| `(2,1)` `arm count2` | refuse | **refuse** — agrees, invisible | accept — caught |
| `(1,2)` `arm enable2` | refuse | **refuse** — agrees, invisible | accept — caught |
| `(0,1)` **undriven** | refuse | **ACCEPT** — caught | refuse — agrees |

So the `<=` variant is visible only at `(0,1)`, which **no row drives**. Three points, one
class, and the detector now covers two of them.

#### The honest accounting, which is less flattering than either disposition

The consistent choices were **all three in-round** or **all three filed**. What happened
was two and one — and the two rode along on a re-measure that was **independently
justified by `nodata stale` alone**, which is a floor breach under the corrected clause (d)
(the guard's operand swapped for a field the guarded body reads).

> **So the second table was bought by ONE row, not three.** `arm count2` and `arm enable2`
> were opportunistic passengers. They are good rows — M10 kills them at 55/57 — but they
> did not justify the four hours, and saying they did would be a wrong record about the
> round's own cost.

**Disposition: keep the two, correct the filed row's reason, and name `(0,1)` as the
uncovered point.** Not adding a third row now: it would force another re-measure for a
variant strictly weaker than the one already measured, which is the trade this round has
just been told it got wrong.

#### And the de-escalation clause is ONE-SIDED, which is why this was ambiguous at all

The clause says the detector must pin the **ACCEPT SIDE** of each de-fatalised predicate —
that legal writes still land. **Nothing anywhere requires a REFUSE-SIDE row**, failable
under guard *shrink*.

But the clause's own reasoning is symmetric. Before the fix, GROWING the guard meant
`exit(1)` on a legal transfer; **SHRINKING it meant a real transfer running on garbage
arming, in a state that used to end the host** — equally unmissable, for the same
accidental reason. **The fix deleted the tripwire in both directions and the clause wrote
down one.**

> **Proposed amendment: for each de-fatalised predicate, pin BOTH sides — an accept row
> failable under growth, and a refuse row failable under shrink.** The check needs no
> measurement: tabulate the operand tuples the sessions actually drive, and if the
> predicate and its plausible weakenings agree on every one, the detector cannot see a
> widening. Here the sessions drove `(0,0)`, `(1,0)`, `(1,1)` — and `== 1`, `!= 0`, `>= 1`
> and bare truthiness **agree at all three**. Visible from the row list alone.

### FIRST TRIAL OF THE PRE-TABLE CHECK, on `asicbadaddr`, before its detector exists

**Check 3 (guard field vs body field) reproduces — from two greps — a hazard that took a
flagship seat's reading to find in pass 1.**

* the guard computes `r` at `:118`; the switch arms index `pending_irq[r]`, `mask_13[r]`,
  `mask_11[r]`, `mask_9[r]` — **guard field and body field are the same field**;
* `grep` for writers of `r` returns **TWO**: `:118` (derived from `relative_addr`) and
  **`:121` — a bare `r = 0;` inside the block being deleted.**

Two writers, one derived and one constant, so **they CAN disagree** — and the state where
they do is exactly the one pass 1 named independently: *widen `r == 3` to `r >= 2` and
offsets `0x08/0x18/0x28/0x38` silently alias onto index 0, because `r = 0;` is still
sitting there.* A worse failure than the one being removed, and silent.

> **The check does not merely find the hazard — it confirms the design decision.** The
> converged design says delete the WHOLE five-line block, not just the `exit(1)`. Post-fix
> `r` has one writer and no third state, so the check goes from "finds a hazard" to
> "nothing owed" **because of that choice**. Deleting only the `exit(1)` would leave it
> live.

*I first wrote "CHECK PASSES, nothing owed" after looking only at the derivation at `:118`
— and the second writer is four lines below it. **A two-writer check that stops at the
first writer always passes.*** Recorded because the check's value depends entirely on
running the grep rather than reading the obvious line, and I nearly demonstrated the
failure mode in the act of trialling the rule.

**Cost of the trial: about two minutes.** It found one thing, and that thing was already
known — which is the right outcome for a first trial. A check that turned up something
nobody had found would be luck; one that reproduces a flagship seat's finding mechanically
is what it claims to be.

### The pre-table check, TRIALLED END TO END on `asicbadaddr` — result and cost

Run before that round's detector exists, which is the only time it is worth running.

| check | denominator | result |
|---|---|---|
| **1 path x channel** | 13 paths x 9 channels, both from greps | **found an empty COLUMN**: the ASSERTION channel (`_tick()` -> `asserted_13/11/9`) has no row. Distinct from the `pending_irq` REGISTER the design already covers — a guest can read a pending bit that was never delivered |
| **2 claim -> row** | **96 lines** selected | **0 hits.** No claim verb in the design lacks a row |
| **3 guard field vs body field** | 2 writers of `r` found | **confirmed the design decision**: `r` is written twice — derived at `:118`, constant `0` at `:121` — so deleting only the `exit(1)` leaves a future guard-widening silently aliasing onto index 0. The design already deletes the whole block; the check says WHY that is load-bearing |

**Total cost: under ten minutes.** One real gap, one design confirmation, and one mechanical
reproduction of a finding that had taken a flagship seat's reading.

#### The uncomfortable half, which is the useful half

**Two of the three checks caught me making the exact error they exist to prevent.**

* On check 3 I wrote *"CHECK PASSES, nothing owed"* after reading the derivation at `:118`
  — **the second writer is four lines below it.** A two-writer check that stops at the
  first writer always passes.
* On check 1 I ran a range whose start pattern did not match, got `0`, and reported that
  the design had **lost** a finding. It had not. **A range that selects nothing reports
  zero for everything.**

Both were caught by follow-up greps, not by gates. So the honest claim for this checklist
is narrower than "it works": **it is cheap, it is mechanical, and running it carelessly
reproduces precisely the defects it targets.** The denominator habit — print how many lines
the search considered, next to what it found — is what separates the two, and it was added
to the carrier because of these two incidents rather than in anticipation of them.

*Recorded now, with its cost, so a future round can judge whether it earned its ten minutes
rather than inheriting it as doctrine.*

---

## 2026-08-24 — `lethalonly`: a row whose ONLY kill is a LETHAL mutant is not proven to observe what it claims

**DISPOSITION: FIX IN-ROUND** (originally FILED as coverage debt above the vacuity floor; **reversed the same day** — see the reversal section below, which found the FILE call cited the stopping rule against material that rule does not govern). *The head of an entry is what a reader and a grep both take, so the superseded disposition may not stand here.* Raised by the kimi seat in
`panel_20260824_055023` — the round's single capped ask-again — and it is a vacuity class
none of the other **seven ANSWERING** seats named. *(This said `eight`. `glm` was DOWN on that panel — no answer inside a 114,723-byte file, the largest in it — and a seat that did not answer cannot be counted among those that failed to name something. Counting a down seat in the denominator of an agreement claim is the seat-failure-as-agreement shape in miniature, which is the one thing the seat ledger exists to refuse.)*

**The mechanism.** Under a mutant that kills the host, every row IN THE DYING SESSION reads `died`. *(This said `EVERY row in the probe`, which is measured false: 46 and 47 of 57 rows still PASS under `Mb2` and `Mb1`, because the probe forks a fresh emulator per session. The effect is real and confined — which is exactly how `arm says` acquired its only red, by sharing `arm survive`'s session.)*
So a row's red under a lethal mutant says only *"the host died"*; it says nothing about
whether that row observes its own stated subject. A row validated exclusively by lethal
mutants therefore looks covered and is not.

**Two rows nominated. Checking settled them in OPPOSITE directions, which is why the class
is worth keeping and the nomination alone was not enough.**

| row | claim | only kill in the 57-row table | non-lethal kill? | verdict |
|---|---|---|---|---|
| `nodata notx` | a declined transfer must not ANNOUNCE itself | Mb1 (lethal) | **YES** — the pre-move build | **REFUTED** |
| `arm says` | and the decline SPEAKS | Mb2 (lethal) | **no** | **HOLDS** |

`nodata notx` does have a non-lethal kill: `probe_pre51.raw` is the pre-move build, where
`arm survive` and `nodata live` both read `survived` — the host is alive — and `nodata notx`
reads `1` against a wanted `0`. **The seat could not have known**: that measurement is not in
the kill table the ask-again brief inlined. *That is a defect in the brief, not in the seat's
reasoning, and it is the same shape as the standing "inline every fact" rule — what was
withheld here was the evidence that would have refuted the seat's own hypothesis.*

`arm says` reads `1` against `1` on that same pre-move build — green — and its only red
anywhere is Mb2. **So the row claims the decline SPEAKS, and has never been shown to redden
when the decline goes SILENT without the host dying.**

**The closing mutant is cheap and obvious once named**, which is the usual signature of a real
gap: delete the `fatal()` from the arming arm, keep the latch and keep `idata = 0`. Host
survives, no diagnostic, `arm says` reads `0` against `1`. One build.

### *** DISPOSITION REVERSED, 2026-08-24: FIX IN-ROUND. The FILE call cited the stopping
### rule against material the stopping rule does not govern. ***

**This entry originally said "Not fixed in-round … the stopping rule FILES it." That was
wrong, and the rule's own text says so:** *"The stopping rule governs findings against SHIPPED
material only. A row measured vacuous before commit is unfinished, not a reopening"* (L1).
**Nothing here has shipped** — the round is uncommitted and table 3 is still measuring the
deliverable. Citing the stopping rule to file a defect in a detector still under construction
is a category error by the round's own taxonomy, and `#448` and `#449` fixed exactly this
class in-round on exactly this ground.

**A second, independent ground — clause (d) as this same round corrected it.** The repair at
each arm is {latch + print, `idata = 0`}. The table nulls the `idata` effect four ways (`M1`,
`M3`, `M6`, `M12`) and the latch two ways (`M2`, `M4`), and adds completion two ways (`M8`,
`M9`) — but **no mutant nulls the PRINT.** "Guard kept, its effect removed" applied to the
print is a one-statement mutant that does not exist. *This round measured that (b) does not
imply (d); this is the same lesson one effect over.*

**The premise that made FILE look defensible was also overstated, and the record is corrected
here rather than quietly dropped.** `arm says` is NOT the only row asserting that declines
speak — `nodata says` (`:722`), `stale says` (`:964`), `both decl` (`:694`), `arm count2`
(`:800`) and `arm enable2` (`:808`) all do. **It is the sole carrier of the ARMING-side
message only.** That narrower claim is the true one, and it is still enough to owe a mutant.

**The work is bounded to ONE build**, because the no-data side is already discharged at row
level: under `M5`, `nodata says` and `stale says` measured red as `0` against a wanted `1` —
message absent while the process lives, which is precisely the message-gone shape. The shared
channel machinery is exercised non-lethally too (`M4` killed `arm once` at `2` vs `1`; `M2`
killed `both decl` at `1` vs `2`). **What has never been measured is the arming diagnostic
going 0-red in a LIVE session.**

> **THE OWED MUTANT (`Mf`), to run after the driver prints RESTORED:** delete the `fatal()`
> call in the ARMING arm, keep the latch and keep `idata = 0`. Build, one 58-row run, archived
> under the stamped-path discipline. Expected reds: `arm says` (0≠1), `both decl` (1≠2),
> `arm once` (0≠1), `arm count2` and `arm enable2`. **If `arm says` does NOT redden, the row is
> genuinely defective and gets re-cut under L1** — capped at that one loop.
>
> *This is not a second ask-again and the anti-`#392` cap is untouched:* it raises no new
> adversarial query, it discharges a named finding that has already been adjudicated.

**The class generalises past this probe, and that is the part to keep:** any detector whose
mutant set is mostly lethal will show rows that look validated and are not. **The
discriminator is one question — does this row have a kill that leaves the host ALIVE?** It is
answerable from a kill table that already exists and costs nothing.

### *** THE AUDIT THE CLASS ASKS FOR, RUN ACROSS ALL 57 ROWS — AND IT ADDS A CARVE-OUT THE
### SEAT'S VERSION DOES NOT HAVE. ***

Asking that question of every row (not just the two nominated) took one script over the
preserved table-2 logs. Of 57 rows: **21 have a non-lethal kill, 4 have only lethal kills, 32
have no kill in THIS table** — the last group being rows from earlier rounds whose mutants
live in the `#459`/`#461` tables, so "no kill here" is not "no kill".

The **four** lethal-only rows are (this sentence said *three*, and its own table was missing `nodata stale` — the census correction above was applied to the numbers and not to the prose beside them):

| row | its own claim | verdict |
|---|---|---|
| `arm survive` | *one store to +0x18 no longer ends the host* | **correctly covered** |
| `nodata live` | *arming with no staged data no longer ends the host* | **correctly covered** |
| `nodata stale` | *FAILED-COMMAND state: data NULL, `data_len` STALE* | **correctly covered** |
| `arm says` | *and the decline SPEAKS* | **the real instance** |

> **THE CARVE-OUT: a lethal-only kill is the CORRECT pairing when the row's PREDICATE
> COMPUTES NOTHING BUT NON-TERMINATION.** For `arm survive`, `nodata live` and `nodata stale`
> the lethal mutant is the on-point mutant — the row asserts the host process did not END, so
> the mutant that ends it is precisely what must redden it.

*** THIS SAID "COMPUTES NOTHING BUT LIVENESS … the row asserts the host LIVES" UNTIL
2026-08-24. THE WORD WAS WRONG AND IT IS CORRECTED IN PLACE, WITH THE OLD TEXT QUOTED, because
a correction that silently swaps a word leaves no trail and a correction carries more authority
than the error it replaces. ***

`probetimebased` establishes that `rd()` returns `False` only on EOF, so **`alive` stays true
for an emulator that is HUNG but has not exited**. Green therefore proves *"did not
terminate"*, never *"is healthy"* — these rows are ONE-DIRECTIONAL.

**And that STRENGTHENS the carve-out rather than undermining it**, which is the opposite of
what I expected when I raised it. The row reddens iff the process terminated, so the set of
mutants able to kill it is still exactly the terminating ones — the finding shows that even
the one interesting non-lethal failure, a hang, cannot redden them either. *"A non-lethal kill
is impossible for these rows" was true as stated and is now true for a sharper reason.*

**What was actually overclaimed was never the rule.** The row NOTES are calibrated exactly
right — "one store to +0x18 no longer **ENDS** the host", "no longer **ENDS** the host" — and
"ends" is termination, which is what not-EOF observes. The overclaim is in the row NAMES
(`arm survive`, `nodata live`, which connote health) and in the adjudicating seat's own gloss
*"proves the host lives"*, quoted here as corrected rather than quietly dropped. **L4 wording,
not a re-disposition.**

**The names are NOT being changed**: they are wired into `gate_sh_rounding.sh`'s 58-name list,
and a mid-round rename is precisely the wrong-section/list-destruction trap this project has
already paid for. *Annotate, do not rename.*

*** THE FIRST WORDING SAID "when the row's own SUBJECT is survival", AND THAT IS
SELF-CERTIFYING — the same author wrote the rows, wrote their descriptions, and wrote the rule
that reads those descriptions. Replaced 2026-08-24 with two MECHANICAL conditions, both
grep-checkable and both already satisfied here: ***

* **(i) a PREDICATE test, not a subject test.** The row's got-expression is literally
  `"survived" if alive else "died"` and computes nothing else (`gdrom_default_probe.py:623`,
  `:720`, `:962`). For such a row a non-lethal kill is not merely unnecessary, it is
  **impossible** — there is no value, count or text in the predicate for a non-lethal mutant to
  perturb. Lethal-only is the EXHAUSTIVE kill type, not a concession. *So stated, the rule
  cannot be stretched to excuse a content-bearing row, which is what the subject-based wording
  left wide open.*
* **(ii) the kill must DISCRIMINATE.** Red under the lethal mutant at the row's own arm, GREEN
  under the sibling arm's lethal mutant. That separates *"my store kills the host"* from *"I sit
  downstream of something that dies."*

**Condition (ii) is measured, and the cross-pattern is clean:**  *** RE-MEASURED AT 58 ROWS IN TABLE 3 AND IDENTICAL — so this evidence now points at the table the round PUBLISHES, not at a superseded one (`table3_58rows/probe_Mb1.raw`, `probe_Mb2.raw`; table 2's figures were the same). The adjudication required this re-check and named the alternative outcome plainly: had the pattern differed, that would have been a FINDING, not a substitution. It did not differ.***

| row | `Mb1` (exit at the NO-DATA arm) | `Mb2` (exit at the ARMING arm) |
|---|---|---|
| `arm survive` | **ok** | FAIL |
| `arm says` | **ok** | FAIL |
| `nodata live` | FAIL | **ok** |
| `nodata stale` | FAIL | **ok** |

Each survival row dies **only** under the mutant re-fatalising the arm its own trigger reaches,
and stays green under the sibling's. That is localisation, measured — and it answers the sharper
objection this entry raised against itself (*do they redden for the stated reason, or merely
because everything reddens?*). **They redden for the stated reason.** It also scopes kimi's
class correctly: the collateral effect is real but confined WITHIN a dying session, which is
exactly how `arm says` got its only red — it shares `arm survive`'s session at `:621-626`, so
under `Mb2` its count predicate was never evaluated at all.

So the class as stated is too broad by exactly the rows it should protect, and the usable form
is: **only-lethal kills, AND the row's predicate computes more than non-termination.** In this table that is one
row — `arm says` — which is the row the seat named. *Its instance was right and its criterion
was too wide; the criterion is what generalises, so the correction is the useful half.*

**Cost of the audit: one script, no builds, no host load.** It is derivable from any kill table
already on disk, which makes it the cheapest check in this file — and three tables were built
before anyone asked the question.

### *** RUN ACROSS BOTH TABLES, THE GAP IS PERSISTENT — AND THE DETECTOR IS OTHERWISE
### IMPROVING ON EXACTLY THIS AXIS. ***

The same audit on table 1's preserved logs (`table1_52rows/`, 52 rows, 10 mutants, one lethal)
against table 2's (`table2_57rows/`, 57 rows, **13 mutants** in 14 archived files — the fourteenth is `probe_pre51.raw`, a historical BUILD and not a mutant — two lethal):

| | table 1 | table 2 |
|---|---|---|
| rows with a non-lethal kill | 16 | **21** |
| only-lethal | 2 | **4** |
| no kill in that table | 34 | **32** |

*** THE 22/3 SPLIT FIRST WRITTEN HERE WAS WRONG, AND THE ERROR IS THE INTERESTING PART.
Corrected 2026-08-24 by the fable5 adjudication, verified from the got-columns. ***
In **table 2** (`table2_57rows/probe_M11.raw`, `probe_Mb1.raw`) `nodata stale` has exactly
two kills, `M11` and `Mb1`, and **both read `died`** — so its
only kills are host-death kills and it belongs in the set. I classified by **MUTANT
IDENTITY** (`Mb*` = the floor-(b) reinstatements = lethal) instead of by the row's
**OBSERVED FAILURE MODE** (the got column). `M11` is lethal-in-effect — its `data_len`
guard-swap sends the stale state into `memory_rw(..., NULL, 408, ...)` — but it is not
named `Mb`, so my oracle scored it `alive`.

> **THE ORACLE'S DEFECT, stated generally: LETHALITY IS PER-SESSION, NOT PER-MUTANT.** My
> test asked whether `arm survive` or `nodata live` read `died`, and under `M11` neither
> does — because the probe forks a **fresh emulator per session**, so a mutant can kill
> some sessions and leave others untouched. A per-mutant lethality flag cannot represent
> that. *The intent-based rule produced the miscount; the mechanical form finds the fourth
> member immediately.*

*** AND TABLE 3 FALSIFIED THE TIMELESS FORM OF THE M11 CLAIM, so it is bound to its
table above. *** Re-run at 58 rows, `M11` scored **56/58 with `nodata stale` GREEN**: the
NULL-source `memory_rw` fault did not fire, all nine liveness rows read `survived`, and
M11's kill moved to the value rows `stale says` (0 vs 1) and `stale idle` (`absent` vs
`0x0`). **KILL STABLE ACROSS BOTH RUNS; FAILURE MODE NOT.** Established as genuine
non-determinism rather than an effect of the added row: the three stale rows share ONE
session and `nodata twice` sits in a different, earlier one. *Consequence for the census:
`nodata stale`'s only RELIABLE kill is `Mb1`, a lethal one — so its membership holds on
the stronger warrant, `the only kill that reproduces is lethal`.*

**Every row that changed class improved**, which is the opposite of what the rising
only-lethal count suggests at a glance:

    arm count2, arm enable2, nodata stale, stale idle, stale says   <absent> -> nonlethal
    nodata notx                                            no-kill -> nonlethal
    nodata live                                            no-kill -> ONLY-LETHAL

*The only-lethal count went 2 -> 4, and `nodata live` climbing UP out of `no-kill` is one of the two moves that did it — the other being `nodata stale`, whose M11 kill reads `died` and which the first pass mis-filed as `nonlethal`.*
Going from untested to tested is progress, and under the carve-out above that row is then
correctly covered, because its own subject is survival. **A count that rises while every
underlying move is an improvement is exactly the kind of number that gets reported as a
regression by anyone who does not separate `only-lethal` from `no-kill` — my own first pass
conflated them and read it as the detector getting worse.**

**What survives the comparison is the one real finding, and it is stronger stated this way:**

> `arm says` has carried a lethal-only kill through **both tables** — 14 measurement points
> in table 2 alone (13 mutant logs plus the non-lethal pre-move build; nearer 24 across
> both, and the `14` as first written read as the both-tables total) — and no mutant has
> ever reddened it with the host
> left alive. It is not an artefact of one table's mutant selection.

**And the retrospective version of this audit is already impossible for `#461`** — see
`killartifacts`. Its one lethal mutant's per-row result was never preserved (0 candidate lines
across every `.out` file in both scratchpads), so that round's detector cannot be checked for
this class at all.

## 2026-08-25 — `asicbadaddr`: one guest LOAD ended the host, and the detector needed four seats to finish it

**DISPOSITION: FIXED, detector shipped, five residuals FILED.** `dev_dreamcast_asic.c` computed
`r = (relative_addr / 4) & 3` and ran `exit(1)` when `r == 3` — **above the switch and above the
writeflag test**, so the kill needed no store, no staging and no command sequence.

**The census in the pass-1 brief was wrong by 4x and six of nine seats ratified it.** The brief
said sixteen killing offsets; the true number is **sixty-four**, because `relative_addr` is a
`uint64_t` raw sub-word offset (`memory_rw.c` subtracts `baseaddr` with no mask), so a BYTE access
at `+0x0d` dies exactly like `+0x0c`. One seat "corrected" it by silently narrowing the claim to
"sixteen *word-aligned*" — repairing the sentence while hiding the defect. `kill byte` is the row
that pins the correction.

### Measured in both directions, then defended by four tables

| | |
|---|---|
| committed HEAD `3710d41` (recorded as `6cae5e4`; identical source) | **scored 5 of 9 — FOUR rows red** |
| with the fix | **scored 9 of 9 — none red** |

**Fourteen distinct mutants, twenty-eight runs, five tables**, artifacts under
`regress/artifacts/asic463/`. Every prediction matched name-for-name.

*** THE SINGLE CAPPED ASK-AGAIN BROKE A CLEAN TWELVE-ROW TABLE, and the reason is the
finding: `alias`, `alias2` and `crossarr` are DISTINCTNESS tests, so they are invariant
under any INJECTIVE re-map. *** `r = ((relative_addr / 4) + 1) & 3` slides every address one
word, all three pairs stay distinct, and it scored a clean 12/12 -- while every `+0x?8`
register moved one past a `[3]` array and `mask_9[3]` IS `int asserted_13` (verified by
`offsetof`), so a documented register's store lands on the interrupt latch and the device
drops a pending IRQ13.

It ships a thirteenth row, `mask9 rt`, because it passes the de-escalation clause's own
membership test -- apply the edit to the PRE-FIX code and the old `exit(1)` fires on
legitimate traffic, so the defect used to announce this edit and the fix de-announced it.
An accept obligation is discharged by a MEASURED KILL, never by prose. **Measured: 12/13,
reddening `mask9 rt` ALONE.** Its oracle is ANCHORED -- tied to a cell by a channel outside
the decode under test (the tick zeroes the latch). **It is NOT thereby independent of struct
layout**, and an earlier version of this sentence said it was: `mask_9[3]` lands on
`asserted_13` by adjacency, so a struct reorder unpins it like any collision row. Anchoring
buys decode-absoluteness, not layout-independence.

The final table is **13 rows, 12 mutants, NO ESCAPES**. Generalised into the carrier as
vacuity-floor clause **(f), the ANCHOR RULE**, with the two-second reviewer check: *"if every
address in this device shifted one word, which row reds?"*

| exact edit | score | reddened |
|---|---|---|
| verbatim reinstatement of the whole block | 8/12 | kill word, kill byte, kill store, kill far |
| `if (r == 2)`, mask intact | 10/12 | safe 8, alias2 |
| `if (r == 1)`, mask intact | 9/12 | safe 4, alias, crossarr |
| `if (r == 0)`, mask intact | 8/12 | asic ok, alias, crossarr, alias2 |
| device answers 0 for all reads | 8/12 | asic ok, alias, crossarr, alias2 |
| `& 3` -> `& 2` | 11/12 | **alias** |
| `& 3` -> `& 1` | 11/12 | **alias2** |
| `& 3` -> `& 7` | 11/12 | **crossarr** |
| `/ 4` -> `/ 2` | 11/12 | **alias2** |

**THE UNIT OF COVERAGE IS THE COLLISION PAIR.** Three register words admit distinct pairs and one
distinctness row pins exactly one. The first aliasing row pinned words 0 and 1; `& 1` and `/ 2`
both collide words 0 and **2** and escaped it. Four seats found four escapes against a table that
was already green — three of them after the round believed it was finished.

**"Reddens ALONE" is a property of the ROW SET, not the mutant.** At 9 rows each accept mutant
isolated one row, which is what proves a row carries something by itself. At 12 they no longer do,
because the new rows legitimately share selectors. DISCHARGE survives the row set growing;
ISOLATION does not, and is cited as a nine-row result.

### The deleted guard was ALSO a bounds check

`r == 3` is out of range for `uint32_t[3]`, so the block did two jobs and the round had reasoned
about one. **Before this commit the switch had never once executed with `r == 3`.** Verified by
enumeration rather than assertion: all twelve labels (three of them DECIMAL — `case 0:`, `case 4:`,
`case 8:`, which a `case 0x` regex misses) give **max r = 2**, and `default:` indexes nothing.
A seat corrected the round's wording here too — computing 3 is not an out-of-bounds access; only
`array[r]` would be.

### Residuals FILED

* `asicpermute` — `% 3` permutes bijectively; no round-trip row can see it; needs a free-running
  assertion probe.
* `asicindexcase` — an INDEXING case added at an r==3 offset is now a silent OOB, and this fix
  deleted the tripwire that made such an edit self-announcing.
* `asicoffsetkill` — a per-offset kill (`if (relative_addr == 0x1c) exit(1)`) at an offset no row
  touches.
* `asickillsurvive` — the four `kill *` rows are SURVIVE-ONLY and do not check the returned value.
* `asicarray4` — sizing the four arrays `[4]` would de-fang the whole OOB class for 16 bytes.
* `asiceventaddr` — **corrected this round**: the header macro reaches a fourth word whenever
  `(e>>5) & 3 == 3`, not "any event >= 96" as three records had it. Latent: max defined event is
  67 and `67>>5 == 2`.

### Two seat-failure notes

**The kimi CLI was quota-walled (403) for this entire round** and ran as `kimi-k3:cloud` — a
DIFFERENT TRANSPORT, recorded as a substitute, never as the CLI seat. `panel.sh` reported that
403 as "RATE-LIMITED (HTTP 429)" and tallied `6/7 scriptable` while the substitute's 17 KB answer
sat in the same directory. Filed as `panelseatlabel`.

**And a fifth seat-failure class was measured**: `deepseek-v4-pro:cloud` returned an EMPTY
response inside 265 KB of `thinking`, `done_reason: length`, `eval_count: 65536`. It is none of
the four recorded classes, and **a size check scores it the panel's best answer**. Filed as
`seatthinkburn`, with the contributing cause recorded honestly — the brief inlined an entire
18 KB document and asked for an exhaustive audit of it.


### 2026-08-27 -- `baretitle`: a fifth of the open queue is a TITLE with no evidence

A census of the ledger found a large population of open rows whose `state_note` is empty or
near-empty: a one-line title, no evidence, no witness, no disposition. They are not dormant
because they were judged low -- **they were never assessed at all**, so nothing in the queue
can rank them against the rows that were.

**This is the unread-review class one level up.** A row with a title and no note reads, to any
later session, exactly like a row that was looked at and found unimportant. Neither the ledger
nor the gates can tell the two apart, so the queue silently reports coverage it does not have.

**The class is cheap to work and it parallelises**, which is why it is filed as a class rather
than as N separate rounds. Most of these are settleable by READING -- a source trace, a manual
citation, a reachability argument -- so they need no build, no rig and no wall-clock oracle, and
they can be farmed to read-only seats while the machine is embargoed for timing work.

**Worked so far, each verified locally before recording rather than transcribed from the seat:**

* `makercfalse` -- culprit read directly; the build gate asserts existence, never freshness.
* `sh4pcic15` -- TRUE and LATENT. Sixteen PCIC lines registered, priority init stops at IRQ14,
  so line 15 can never be delivered. Nothing connects to it today.
* `sh4itlbpr` -- mask arithmetic confirmed exactly; severity DOWNGRADED, because the manual
  makes the reserved bit's read value *undefined*, so the present behaviour is permitted. The
  latent coupling was recorded instead: the bit is inert by one arm's specific test, not by
  construction.

**The disposition matters as much as the finding.** Two of the three came back TRUE and were
still NOT FIXED -- one for want of a measured delta, one because correcting it owes the
oracle-correction order and therefore a build. *Establishing that a row is true, latent and
correctly deferred is a complete result for this class*; the failure mode being repaired is the
blank note, not the open state.


### 2026-08-27 -- `mb89352halt`: an unimplemented SCSI command stops the emulated CPU

Found by an adversarial pass that was trying to REFUTE a different row's mechanism, and it did
refute it -- then produced this as a by-product.

On `dev_mb89352.c`, an unimplemented SCSI command leaves `data_in == NULL`, so the controller
enters the status phase. The guest's status read then takes a NULL buffer of length 0 with the
transfer position at 0, so the `read longer than buffer?` guard sees `0 >= 0`, fires, and sets
`cpu->running = 0`. **A guest that issues an unimplemented command to that controller halts the
emulated CPU.**

It is the same omission as the unknown-opcode row -- no status buffer is ever populated -- but
a worse outcome than that row's false success, so it ranks above it on harm. One fix covers
both; two detectors are needed, because the observables differ (a status byte there, the CPU
still running here).

**The by-product is the point.** The pass was asked to break a claim, not to find defects. It
broke the claim -- the status field is a POINTER, so zeroing the struct leaves NULL rather than
a GOOD status byte, and the original explanation was false for every controller -- and the
corrected picture is four different wrong outcomes from one omitted completion step, of which
this halt is the most severe.


### 2026-08-27 -- `m8sarrows`: a one-identifier edit sweeps both m88k detectors 79/79

Successor to `m8sarseq`, filed so a measured specification could stop living in one seat entry.

Changing a single identifier in the CMMU command path -- indexing the register base by a fixed
zero instead of the device's own CMMU number -- passes every row of both shipped offline
detectors, seventy-nine of them. The controls are what make that evidence rather than an
assertion: one mutant reddens the consumer-side rows and another reddens the producer-side
rows, so both ends are covered and only the SEAM is blind. The reason is mechanical -- every
flush row runs after a reset that zeroes both the CPU and CMMU numbers, and issues from CPU
zero, and at that pair every candidate register base coincides.

It is a live class on the shipped rig, not a shape pin: both CMMUs are registered on every
boot, the CMMU number is guest-addressable from an address bit, and the data CMMU takes about
fifty-two percent of the flush writes. Under the mutant, roughly half the machine's page-table
flushes never dispatch.

The fix is three rows with three measured kills on two INDEPENDENT axes -- neither subsumes the
other, which is sharper than the original filing knew. About twenty lines, in the differential
that already has the two-CPU two-CMMU fixture.  Ranked as coverage debt: the shipped code is
correct.

### 2026-08-27 -- `exitdenom`: the terminating-site census counts sites, not defects

Rescued from `exitsweep` at the moment that row closed, because it was a question addressed to
a future seat and closing a row retires every question inside it.

The census reports three hundred and sixty terminating sites, ninety inside device access
handlers, and its own output says it counts sites rather than defects.  It counts termination
with any status rather than only failure, plus aborts and allocation-check macros, and it
includes known non-defects: an intended clean exit in the console device, an unreachable site
in the RAM device, and init-time failures where terminating is the correct behaviour.  It also
does not resolve helper reachability, and helpers are the largest bucket.

The number has had three generations -- one hundred and fourteen, then one hundred and seventy,
then three hundred and sixty -- and two further superseded figures sit on a neighbouring row.
Five numbers for one quantity, and the drift is mostly a changing definition rather than a
changing tree.  That is the substantive point: the scheduling questions the parent row asked
cannot be answered against a number that includes an intended clean exit on purpose.

What would settle it is a classification of the sites into defect, non-defect and unreachable,
with the rule for each written down and the classifier folded into the tool so the answer
re-derives instead of being transcribed.  Read-only: no build, no rig, no timing oracle.


### 2026-08-27 -- `sh4valm33`: the one escape that survived checking

Carried out of `sh4valrows` as that row was dropped, so that dropping a wrong row did not drop
a right finding inside it.

The parent row claimed a shipped detector was escapable by nine measured mutants.  Re-reading
the adjudication it drew from, the seat found it enumerates ten rather than nine -- a row whose
entire content is a count of escapes, miscounting its own -- and that the escapes do not stand
as a group.  So the row was dropped as titled.

One member survived.  A guest long-word store to the third timer control register dispatches
with the timer index set to two and reaches an embedded terminating site.  The observable is
whether the emulator process is still alive after the store: binary, with no value to decode.

It is cheap, because the apparatus already exists -- the detector carries a byte/word/long width
census and a separate per-instance census for the three timer control registers, so this needs a
row rather than new machinery.  Blocked only on a build.


### 2026-08-27 -- `offlinescope`: the embargo was over-scoped, and it was my error

Eleven of fourteen offline differentials compile and run in ten seconds total -- each one a
single source file compiled by a single compiler invocation, including the real shipping
source.  No emulator build, no build tree, no rig, no wall-clock oracle.  A full battery is
three quarters of an hour and needs the machine to itself; this needs nothing.

Six of the top eight ranked defects sit in source files those differentials already pull in.
Only one of the eight has no differential covering it.  So most of the queue was workable all
along, and the thing actually embargoed -- timing work -- was never what blocked it.

The honest limit is the witness ladder's own: a direct-call harness is a DETECTOR, never a
reproduction.  This unblocks measuring and detecting, not witnessing.

THE APPARATUS LESSON COST FOUR WRONG ANSWERS.  There is no uniform flag set -- each
differential has its own invocation.  A first sweep with one flag set reported half of them as
failing to compile; two extra flags fixed most of that.

Then one of them read as a genuine pre-existing red: five failures, identical under two
different flag sets, which is exactly the pattern that normally means the apparatus is not at
fault.  It was still the apparatus.  That harness is linked with symbol-wrapping flags, on a
continuation line a narrow grep had dropped; without them the interception never installs, so
every row expecting a call sequence saw nothing -- and the status row failed too, because the
harness arms its injected failure through that same interception.  With the flags it exits
clean.

What stopped a false report was asking what would make it fail for a reason other than the one
under test.  The tell was that every failing row wanted a call SEQUENCE while every row
checking a value passed.  A set of failures that all share one shape is an apparatus failure
until proven otherwise.


### 2026-08-27 -- `b115` FIXED in round 472: an unaligned overlay read took the wrong layer

The overlay read helper picked a layer for the block containing the current offset, then read
up to a whole block from it without clamping to what REMAINED in that block.  With an unaligned
offset it ran past the block's end into blocks belonging to a different layer, while the output
pointer advanced on a fixed stride.

Measured before any edit: a 1024-byte read at offset 511, on a disk whose overlay held only
block 0, returned 512 overlay bytes where exactly one was correct -- and returned SUCCESS, so
nothing surfaced to the caller.

The asymmetry that makes it unambiguous: the WRITE helper explicitly refuses a non-multiple
length and an unaligned offset.  The read helper never had that guard, and the loop's own
advance expression rounds up to a block boundary -- which is only meaningful if unaligned
starts were expected.

Fixed by clamping to the block remainder and advancing by what was consumed.  Seven detector
rows, two of which exist only because panel passes found mutants that escaped earlier drafts --
one keeping the fixed stride, one relaxing the introduced predicate.  The second was a vacuity
floor breach and was fixed in-round.

Residual filed separately as `shortread`.

### 2026-08-27 -- `shortread`: the short-read path in the overlay read helper

Split out of the row above BEFORE it closed, because a row covering two defects buries one when
the other closes.  Three related items, all previously inside it.

On a short read the length counter is decremented by the amount REQUESTED while the total is
grown by the amount ACTUALLY read, so a short read in a non-final iteration leaves the caller's
zero-fill covering the wrong region.  Pre-existing; round 472 weakly helps -- the hole shrinks
-- but does not close it.

A one-identifier mutant of that round's fix -- advancing by the amount read rather than the
amount requested -- is an IDENTITY outside a short read, so it escapes every row that round
ships and diverges only here.

And a seat claim about the flat, non-overlay path, recorded as unverified.

Not silent: an incomplete-read diagnostic already announces the condition.  Wrong-region data
WITH a warning, not the silent corruption round 472 closed.

One row discharges all three: a truncated overlay data file forcing a short read in a
non-final iteration.  Offline-buildable in the existing fixture -- no build, no rig, no timing
oracle.

## 2026-08-27 — #473 residuals, and a seat-roster finding made while it ran

**#473 closed `wdcringambig` + `wdcrearmzero` with one diff.** Three edits in the ATAPI DATAIN
chunking: move the existing 32768 clamp BEFORE the initial push loop, clamp the re-arm to 32768
instead of 0, and refill the next chunk from `data_in[atapi_received + j]`. Kill table 8/8,
`regress/artifacts/wdcchunking/killtable_20260827/`. Detector 22 rows, 0 failures.

### Residuals -- open

- **`wdcaddtoinbufbound`** — `wdc_addtoinbuf()` **is still unbounded**. #473 bounded its
  CALLER; the primitive itself has no capacity check, and `head == tail` still means both
  empty and full. Any future caller that pushes without its own clamp reproduces the same
  overrun, and **no row in the shipped detector would see it** -- written into the
  clause-(e) contract rather than left implicit. Filed, not fixed: the fix that exists is
  correct and complete for every caller in the tree today.

- **`wdcrearmwalk`** — the detector pins the FIRST re-arm only. A transfer crossing several
  re-arms is not walked end to end, so a defect that appears on the second or third chunk
  boundary is outside contract. A loop-to-exhaustion row is the obvious closer.

- **`wdcrearmzero` still owes a rung-3/4 witness.** A rung-1 direct-call harness is a
  DETECTOR, never a reproduction. Both ledger rows close with `witness: none`, which is the
  honest value; the obligation is recorded, not discharged.

### *** SEAT FINDING: ONE SEAT, BOTH TRANSPORTS DOWN AT ONCE, FOR TWO UNRELATED REASONS.
### Measured 2026-08-27. ***

The carrier's sixth seat-failure class says a walled CLI seat is usually reachable on another
transport, and that the cheap check is `api/tags`. **Both halves held and the seat was still
lost.**

```
  kimi (CLI)              403  You've reached your weekly (7-day) usage limit
  kimi-k3:cloud           503  Service Unavailable
  glm-5.2:cloud           SEAT_ALIVE_20260827
  deepseek-v4-pro:cloud   SEAT_ALIVE_20260827
  minimax-m3:cloud        SEAT_ALIVE_20260827
```

`api/tags` LISTED `kimi-k3:cloud` throughout -- the daemon was up and the model was
advertised. **The listing answers "which models does this daemon know about", not "which
models will answer"**, and those came apart here. The other three cloud seats answering in
the same minute rules out the shared-transport class: this is one model's outage.

> **A LISTING IS NOT A LIVENESS TEST.** The carrier already says this about walled seats --
> *do not reason about whether a seat is back, fire it* -- and the substitute rule quietly
> relies on `api/tags` for exactly the reasoning it forbids. One tiny prompt per cloud seat
> settles it in seconds, and that is what settled it here.

**AND THE FIRST FAILURE WAS NOT THIS ONE.** The substitute's original 346-byte non-answer was
a STALL, not the 503: it opens *"I'll work the questions in the order given, reading the
fork's actual post-fix tree"* and stops. The brief's question 4 said **"Read it rather than
reasoning from the code"** about a datasheet file -- and a packet-fed transport cannot read
files. That is the documented brief defect, mine, not a seat outage. The 503 appeared only
on the re-fire. *Two different failures on one seat in one round, and the first was
self-inflicted.*

- **`panelsubcoverage`** — ✅ **FIXED the same day.** `panel.sh` printed *"the kimi CLI is
  walled but kimi-k3:cloud ANSWERED -- that seat is COVERED by its substitute transport, not
  lost"* **two lines after printing `kimi(sub): SUSPECT (only 346b)`**. The guard excluded
  `kimi_sub` by grepping `$rated` -- the list of seats carrying QUOTA/AUTH text. A seat that
  STALLS never enters `$rated`; it enters `$miss`. **So the exclusion was unreachable for the
  commonest substitute failure**, which is the check-that-cannot-fail shape in its worst form:
  a claim of COVERAGE asserted at the moment coverage was lost, telling the one person who
  could re-fire the seat that it had already answered. Re-pointed at `$miss` and given an
  explicit LOST branch; negative-controlled in both directions.

- **`ollamaseatprefix`** — minor, filed. The liveness probe returned `AT_ALIVE_20260827` from
  `minimax-m3:cloud` where the other two returned `SEAT_ALIVE_20260827` — **two leading
  characters missing**. The seat answered, so this is not a seat failure, but a transport that
  can drop leading characters would corrupt a VERDICT LINE, and this project's policy is
  verdict-line-first precisely so the answer survives truncation. Worth one look at
  `panel_ollama.py`'s stream assembly.

## 2026-08-27 — `asanstaletree`: the ASan tree is silently behind the other three

**`build-asan/` was measured FOUR ROUNDS STALE on 2 of 4 sampled device files** while
`GXEMUL-SEC`, `est/` and `build/` were byte-identical. It was deliberately NOT synced, and
that decision is the owner's to make -- syncing it silently would change what a sanitiser run
measures without anyone asking for it.

**Why it matters more than an out-of-date copy usually would:** the twin-tree rule exists
because a NO-VPATH build tree measures whatever source it happens to hold. An ASan run against
a four-round-old tree reports on code that is not shipping -- and it reports CLEAN, which reads
as evidence about the current tree. *A stale sanitiser tree is a green row that means nothing,* 
which is the vacuity class aimed at a whole build rather than at one detector.

**OPEN QUESTION FOR THE OWNER, and work continues either way:** should `build-asan/` be brought
into the twin-tree propagation set, so every shared-file edit lands in four trees instead of
three? The cost is one more copy per edit. The alternative -- leaving it out -- is defensible
only if nobody reads its results as current, and nothing enforces that today.

## 2026-08-27 — #474 residuals

**#474 closed `fbclearread`:** `case TIMER_1_CLEAR:` had no `writeflag` test, so a guest READ
reloaded the counter, decremented the pending count and deasserted the interrupt. Guarded the
body, kept the `break`. Kill table 5/5, `regress/artifacts/fbclearread/killtable_20260827/`.

- **`fbclearidempotent`** — OPEN, and it is PRE-EXISTING rather than anything #474 introduced.
  The DC21285 says a clear *"has no effect if the associated interrupt was already clear"*,
  while the write arm reloads a periodic timer **unconditionally** — so a write to
  TimerNClear with nothing pending still restarts the counter. Named by the pass-2 codex seat,
  which explicitly said it *"deserves a separate filing, not an untested expansion of #474"*,
  and that is the disposition taken. Needs a row of its own and a reading of what the reload
  is actually for.

- **`fbclearaliases`** — OPEN, coverage debt, low. The four-address fold
  (0x30C/0x32C/0x34C/0x36C → this case, timer indices 0–3) is read from the code and is **not
  detector-backed**: every row exercises timer 1. One nonzero alias row would close it. Filed
  rather than fixed because the fold is shared with every other timer case in the file and is
  not specific to this repair.

### The process finding, recorded because it was measured rather than argued

**#474 skipped pass 1, disclosed that in the pass-2 brief, and the panel found what a design
pass would have caught.** The codex seat returned DO NOT SHIP on an already-green detector and
named two live gaps — an untested early-`return` (the very defect the fix's own comment argues
against) and a guard widened to admit a PERIODIC read. Both were built, both escaped the
shipped rows, and both are now killed.

> **A stated rationale with no row behind it is a claim, not a property.** The fix comment said
> the `break` is deliberate because an early `return` would skip the common tail. Nothing tested
> it: `buf` was memset to `0xff` and never examined. The mutant that exercises a fix's own
> stated reason is a cheap and obvious row, and it was missing.

*This is the second measured case for the same rule in two days — #473's re-arm row carried a
length check where its sibling arm row carried a corruption oracle. Both gaps were asymmetries
between a fix's claim and its rows, and both were found by asking what the OTHER arm already had.*

## 2026-08-27 — `rung1exempt`: three rounds have shipped on rung-1 evidence and no witness term fits

`b115` (#472), `wdcringambig`/`wdcrearmzero` (#473) and `fbclearread` (#474) each shipped a REAL
FIX whose only evidence is an offline differential plus a measured kill table. The witness ladder
classes a rung-1 direct-call harness as a **DETECTOR, never a reproduction**, and none of the five
terms fits: `boot:`/`probe:`/`construction:` are false (and `probe:` is actively dangerous — the
shape regex scores it rung-3, which its own header calls laundering); `harness:` is admitted only
when the round's SUBJECT is the test apparatus, and all three fix emulator code; and `none` is
defined as DOCUMENTED-ONLY, so on a round that shipped a fix it asserts that no code changed.

So each round parks at `held` carrying a prose note — **the note doing work a schema value should
do.** Survivable once; at three it is a pattern, and a fourth will copy whichever note it finds.

**OWNER QUESTION:** per-round exemption, or a new ladder term? A candidate is `detector:<path>` —
honest about what exists, structurally distinct from `probe:`, and it would let
`check_witness.py` tell "fixed with a detector" from "documented only", which it cannot do today.
**Not proposing it unilaterally:** adding a rung changes what every future round may claim, and
the existing terms were adjudicated rather than invented. The three rows are `held` with honest
notes meanwhile, which is correct under the current schema.

## 2026-08-27 — #473 pass-2 findings (post-commit): one regression, one live floor breach, four new rows

The pass-2 panel on `1f1a02b` ran after the round had shipped. Eight of nine seats answered;
**the kimi seat was LOST on both transports** (CLI 403 weekly limit, `kimi-k3:cloud` HTTP 503)
while glm/deepseek/minimax answered in the same minute, so it was that model's outage.

- **`wdcoddstep`** — OPEN, and **MEASURED** on the committed tree. `atapi_len -= consumed` STEPS
  PAST ZERO on an odd-length chunk: with `atapi_len = 3` and a four-byte read, `atapi_len` lands
  on **-1** and `atapi_received` on **4 where `data_in_len` is 3**. So `== 0` never fires again
  and the device claims it delivered more bytes than the transfer holds. This is the `#341` class
  surviving at the same site — that round fixed `consumed` to match what is POPPED, but did not
  make the subtraction saturate, and its own comment describes exactly this symptom as the thing
  being fixed. **Pre-existing**: a small odd transfer reaches it with no re-arm at all. `#473`
  adds a second road (an odd FINAL chunk of a multi-chunk transfer, which before that round could
  never be walked to). *Strictly fewer transfers break than before.* The fix is one line —
  saturate, or test `<= 0` — but **which one is a real question**, because saturating hides the
  over-count in `atapi_received` while `<= 0` completes the command still reporting 4 of 3 bytes.
  This fork's own precedents (`#283` ASC, `#338` mb89352, `#341` here) all say the count reported
  has to be the count that happened, so the truthfulness half needs its own answer.

- **`wdccdbmidxfer`** and **`wdcdataoutdrain`** — filed from READING by the Opus seat, which
  flagged both as **not measured**. The first: `inbuf_len == 12` is an EQUALITY reachable
  mid-transfer, so in PHASE_DATAOUT twelve bytes of guest payload can be dispatched as a SCSI
  CDB. The second: `write_in_progress` and `atapi_cmd_in_progress` can be live together, and the
  write-back block's `0 % 512 == 0` then drains 512 bytes of just-armed ATAPI data **to the disk
  image** at a guest-chosen offset — the `#280`–`#285` family, which corrupted the arc image.

### Two things the panel found in `#473` itself, both fixed in the follow-up commit

**The "ring is empty at the re-arm" premise is FALSE, and it is a REGRESSION rather than merely
an overclaim.** The data-port WRITE arm pushes guest bytes with no phase guard, and its
unexpected-write latch is suppressed *precisely because* `atapi_cmd_in_progress` is set. Opus
measured it end-to-end: one 2-byte guest store, 65536-byte transfer — committed build **32768 of
32768 bytes wrong**, pre-fix build **0 wrong**. The comment is corrected in place and the case is
tracked under `wdcaddtoinbufbound`.

**A fifth and a sixth clause-(d) mutant escaped a table that had already closed four**, and both
came from asking one more time after the table was clean:

- `Md_emptyguard` (grok) — `if (head == tail)` around the refill: **this round's own safety
  sentence turned into a predicate.** Swept 23 rows clean.
- `Md5_chunkconst` (Opus) — the refill's bound relaxed to the constant `32768` instead of
  `atapi_len`. Swept **24** rows clean — including the row just added for the first escape — and
  under ASan on a short last chunk it is a **heap-buffer-overflow READ**.

> **Both hid for the same structural reason: every re-arm row sat where the remainder EXCEEDS
> 32768, so `atapi_len` and the constant were the same number, and every row was written under
> the premise the mutants attack.** The rows were not weak. They were all on one side of a
> boundary, and all downstream of one assumption.

Kill table now **10 of 10**, detector 26 rows, 0 failures.

## 2026-08-27 — `bugfileledgerdir`: the sync check runs one way only

Section P (`check_bugfile_sync.py`) fails when an OPEN **ledger** row has no entry in this
file. **Nothing checks the reverse.** Found by the codex seat on `#473`'s pass 2 and confirmed
by grepping both: four rows — `wdcaddtoinbufbound`, `wdcrearmwalk`, `fbclearidempotent`,
`fbclearaliases` — existed as prose here with no ledger row at all.

**That direction matters more than it looks.** The ledger is the single source of truth and
`matrix.html` renders it, so a row filed only in prose is **invisible to every tool in the
pipeline**: no seat-coverage tracking, no stage panel, no dashboard line, and section H never
asks whether it ran a panel. *A row that exists only in prose is filed in the sense that a
reader could find it, and unfiled in every sense a tool cares about.* It is the unread-review
class one level up — the work is recorded, and the machinery that exists to act on records
cannot see it.

The check should reuse P's shape: scan this file for backticked row-id tokens and fail when one
names no ledger row. **Dated-cutoff and forward-only**, like `check_bugfile_sync.py` itself — a
rule that retro-fails the whole file blocks the next commit on reconstruction nobody scheduled,
and a rule that does that gets switched off.

**NOT BUILT YET, deliberately.** It changes the script every commit runs and owes two negative
controls: red on a bugfile-only row, green once the ledger row exists. The four instances are
already fixed by hand.

## 2026-08-27 — #475 `wdcoddstep` fixed; two seat-named escapes were real

`atapi_len -= consumed` had no bound against what REMAINS, so an odd remainder plus a four-byte
read drove the counter negative — `== 0` never fired again, the command never completed, and
`atapi_received` claimed more bytes than the transfer holds. **The length is a single
guest-chosen byte** (INQUIRY's allocation length, clamped to a minimum of 36 and never to an
even value), so this is not an edge case.

Fixed by clamping `consumed` to the remainder before both updates — **the tree's own idiom**,
verified: `dev_asc.c:610-614` is `#283`'s clamp half in the same shape. Kill table 7 killed +
1 measured equivalence, detector 32 rows, `regress/artifacts/wdcoddstep/killtable_20260827/`.

### The part worth carrying: two seats each named an escape the table did not have

- **`consumed = d->atapi_len;`** (Fable) — the min degraded to a plain assignment. **Sweeps both
  end-state rows**, because the transfer does still end at 0 of 37; what changes is *when*. Killed
  only by the intermediate-state rows, which exist solely because a seat predicted this.
- **`len == 4 && consumed > atapi_len`** (codex) — the clamp narrowed to one access width.
  **Swept all six rows then present**, because every row in the file issued a four-byte read.

> **A detector whose rows all use one access width cannot see a fix narrowed to that width.**
> The rows were present, ran, and were structurally unable to fail — the padded-column trap's
> cousin, and the padded-column assert in the gate patch caught a *literal* instance in the same
> session (a 40-char label in a 38-wide column).

### Residuals — open

- **`wdcwidthmatrix`** — the detector now covers widths 4 and 2 at remainders {1,2,3} and {1}.
  A panel seat recommended the full matrix plus exact-fit controls, and one-byte reads are still
  unexercised. Filed rather than shipped: the two widths present are the ones that can overshoot
  (a 1-byte read consumes 1 and cannot step past a remainder of ≥1), so the gap is completeness,
  not a live hole. Worth one row if the fix is ever touched again.

- **`wdcoddstep` still owes a rung-3 witness, and a seat says one is BUILDABLE** — real guest
  stores of a CDB, then real four-byte data-port loads through decode on an in-tree wdc machine.
  Recorded against `rung1exempt`, which it sharpens: the ladder gap may be a habit of reaching
  for the one-second differential rather than a genuine hole. **Nobody has tried.**

### Three constraints adopted from the panel and deliberately NOT implemented

Each would have looked like tidying and each is wrong:

- no floor for an already-negative `atapi_len` — from a clean command the fix maintains `>= 0`,
  so an extra saturate is unlicensed by the addition rule;
- no clamping `received` to `data_in_len` as a companion to saturation — mid-chunk that
  completes **early** and drops the rest of the transfer;
- no even-padding at the SCSI layer.

## 2026-08-27 — `wdcnullxfer` (#476): `#475` shipped a host kill, found one commit later

```
d894e35 (before #475)   a DATA read with no transfer survives   exit 0
d64a1fc (with #475)     a DATA read with no transfer survives   host killed, signal 11
```

**The mechanism is entirely `#475`'s.** Before it, a data-port read with `atapi_len` already 0
drove the counter **negative**, so `if (atapi_len == 0)` never fired again and the
`d->atapi_st->data_in_len` dereference on the next line was **dead code**. The clamp makes
`atapi_len` *stay* 0. The test fires. `atapi_st` is NULL.

Two guest register accesses from a fresh device — write ATAPI_PKT_CMD to COMMAND, then read
DATA. Measured `SIGSEGV at address 0x48`, which is `offsetof(struct scsi_transfer,
data_in_len)`. The seat's control (same command, no data read) survives on both blobs, so it is
the **read**.

> **A FIX THAT STOPS A COUNTER GOING NEGATIVE CAN MAKE A PREVIOUSLY-UNREACHABLE BRANCH
> REACHABLE.** The clamp was right; the branch it woke was never NULL-safe. *Repairing a counter
> can enable code that was only ever protected by the broken value.*

**And `#475`'s own kill table could not have caught it.** Eleven mutants, every one attacking
the clamp — none attacking what the clamp let *through*. A kill table asks "what edit breaks
this fix"; it never asks "what does this fix now reach".

Fixed by declining with this file's latch idiom. That is the `#337`/`#184`/`#186`/`#315`/`#316`/
`#326` halt class the fork has spent many rounds closing, and which I had just reopened.

*The row FORKS: the defect is a SIGNAL, and an in-process oracle would take the differential
down with it and report nothing at all.*

### Held out of the committed detector, deliberately

> *** THIS PARAGRAPH WAS TRUE WHEN WRITTEN AND EVERY CLAUSE OF IT IS NOW FALSE.
> Corrected 2026-08-27; the citation had been dangling for two rounds. ***
>
> It read: *"Three reproduction rows -- `row_cdb_midxfer`, `row_dataout_drain`,
> `row_cdb_already12` -- are in `_scratchpad/held_repro_rows.c`, not in the tree. They
> reproduce `wdccdbmidxfer` and `wdcdataoutdrain`, which have **no fix yet**, so they are RED
> and a red detector blocks the gate."*
>
> **All three rows are DEFINED, REGISTERED and GREEN in the committed detector**, the file
> `_scratchpad/held_repro_rows.c` **does not exist**, and both defects are FIXED:
> `wdccdbmidxfer` by the phase conjunct in `0922465` (#477), `wdcdataoutdrain` by
> `inbuf_len > 0 && !badlen_this` in `832bed7` (#478) -- the exact condition its own entry
> names. Verified by `git log -S` on each fix text before the rows were closed.
>
> *Found by a read-only research subagent that noticed the dangling path while censusing
> something else. Nothing systematically re-checks a citation after the thing it cites
> moves -- which is the same class as the line numbers this file keeps correcting, one
> level up: **a path is a citation too.***
A detector ships WITH its fix. The stub instrumentation they need (`stub_frees`,
`stub_disk_writes`/`_bytes`/`_offset` and the counting bodies) **stays in the committed file** —
inert without the rows, and the fiddly part to re-add.

## 2026-08-27 — `wdccdbmidxfer` fixed as #477; the panel chose against my preference

`atapi_cmd_in_progress` is set when a packet command arrives and cleared only when the **next**
one does — so it stays 1 through the whole of DATAIN and past `PHASE_COMPLETED`. A guest write
that brought ring occupancy to exactly 12 therefore re-entered the CDB dispatch, **freed the live
transfer**, and issued a SCSI command built from the guest's own returned DATA-IN payload.

Fixed by keying the dispatch on `atapi_phase == PHASE_CMDOUT`. Kill table 6/6, detector 42 rows,
`regress/artifacts/wdccdbmidxfer/killtable_20260827/`.

### The mechanism I stated was wrong, and one row settles it

A **len-3 write pushes zero bytes** — the width switch's `default:` arm only latches — and
control falls straight through to the dispatch, which frees the transfer anyway.

> **The defect was never "writes push foreign bytes into the ring."** It is that *the dispatch
> runs on every data-port write regardless of what the write did.*

That is why **option A — guarding the pushes, which I preferred — was measured WORSE than no
fix**: with occupancy already 12, the suppressed push leaves it at 12, so A creates a free on an
input the unfixed code survives. A fix that makes a state worse is not coverage debt.

And the sharper diagnosis, which I had missed: `atapi_cmd_in_progress` **conflates two roles** —
"a packet command is active" (read at four register sites through completion, so it must stay
set) and "I am collecting a 12-byte CDB" (what the dispatch actually wants). Option C would have
damaged the first to patch the second, breaking the ATAPI completion handshake.

### Residuals — open

- **`wdccdbaccum`** — the structural fix, filed not shipped. `dev_mb89352.c` gives the CDB its
  **own accumulator**, switching on phase to select a destination buffer and dispatching on
  *"this phase's own buffer is full"* rather than a shared occupancy count. That removes the
  aliasing which makes a phase guard necessary at all: `inbuf_len == 12` cannot tell CDB bytes
  from DATA-IN payload from disk-write payload. **A seat measured its migration cost honestly:**
  it relocates where a CDB lives, so every existing probe that fakes one stops working.

- **`wdcdataoutdrain`** — *** CLOSED. The words "still open, still unfixed, and its row
  stays held in `_scratchpad/held_repro_rows.c`" stood here for two rounds after the fix
  shipped in `832bed7` (#478) and after `row_dataout_drain` was ported into the committed
  detector, where it is green today. *** The measurement below is the PRE-FIX one and is
  kept as the historical record of what was wrong. Measured: `1 write(s), 512 bytes to 0x8000` **to the disk
  image**. Option B does not touch it — different block, different flag (`write_in_progress`).
  A seat found a **worse sibling** with no ATAPI involved at all: a single 3-byte data-port write
  pushes nothing, `inbuf_len` is 0, `0 % 512 == 0`, and 512 bytes of an **empty ring** go to the
  image — after which `inbuf_tail` has advanced 512 past `inbuf_head`, occupancy reads 262144 of
  262656, and DRQ is asserted forever. **One guest write, no ATAPI command, no live transfer.**
  Both reduce to one condition: `inbuf_len > 0 &&`.

- **`wdcaltctrlbit`** — NEW, 2026-08-27, READ from source and UNMEASURED. The ALT-CTRL
  write arm reads:

  ```c
  if (idata & WDCTL_4BIT)
          d->cur_command = COMMAND_RESET;
  ```

  `WDCTL_4BIT` is `0x08` — *"use four head bits (wd1003)"*, a head-addressing mode
  selector. The reset bit is **`WDCTL_RST`, `0x04`**.

  *** MY FIRST FILING OF THIS SAID "a guest selecting 4-bit head mode is treated as
  issuing a controller reset, and a guest issuing a real soft reset is ignored -- two
  wrong behaviours from one wrong constant." THAT OVERSTATED IT, and I caught it by
  reading what COMMAND_RESET actually drives instead of stopping at the constant. ***

  **`COMMAND_RESET` is not a reset ACTION.** It is read at exactly two sites, and both
  do the same thing: make CYL_LO return `0x14` and CYL_HI return `0xEB` *for a CDROM*.
  That is the **ATAPI signature `0xEB14`**, which a real drive presents after a reset so
  the driver can tell an ATAPI device from an ATA one. Nothing is reset; no state is
  cleared; the latch only changes what two registers report.

  **And the common path works by accident.** The conventional soft-reset sequence writes
  `0x0C` (bit 3 | bit 2) and then `0x08` to release it — **bit 3 is set in both**, so the
  signature is presented exactly when a real driver expects it. That is why this has
  never been noticed.

  **What is genuinely wrong:** a driver that writes `WDCTL_RST` (`0x04`) *alone*, with
  bit 3 clear, performs a soft reset and is never shown the ATAPI signature — so it can
  fail to detect the CDROM. And a driver writing `0x08` for its documented purpose gets
  the signature latched without asking for a reset.

  **Severity: LOW**, and lower than the constant makes it look. Filed below live defects.
  `git log -L` on these lines returns ONE commit — the upstream import — so this is
  inherited, not a fork regression.

- **`wdcsrstnoabort`** — NEW, 2026-08-27, same arm, READ. It sets
  `cur_command = COMMAND_RESET` and does **not** clear `atapi_cmd_in_progress` (the only
  clear is inside `wdc_command`), so an in-flight packet command survives it.

  *** RE-SCOPED THE SAME DAY, for the same reason as the row above: since `COMMAND_RESET`
  is only a signature latch and not a reset action, "survives a reset" was the wrong
  framing. The device performs NO reset here to survive. ***

  The defensible statement is narrower and still real: **this device has no soft-reset
  path at all.** ATA SRST should abort the in-flight command, clear the ring and reset the
  phase; this arm does none of those, and no other code does either. The measured
  consequence is [[wdcringnoflush]] — the Opus seat confirmed neither `ATAPI_SOFT_RESET`
  nor this arm flushes the ring, so a guest has no way to recover a wedged device.

  **Provenance is worth recording, because it is the ask-again working as designed.** Both
  fell out of checking *why* `M2_curcmd` escaped `#477`'s table. The comfortable reading was
  "redundant conjunct, provably equivalent" — and that reading is wrong: this arm is exactly
  the reachable state that distinguishes the mutant. **An escape chased is worth more than an
  escape classified**, and classifying it as an equivalence would have buried both defects.

  They are the same conflation family the `#475`/`#476`/`#477` chain has been working:
  a flag outliving the thing it describes. See `wdccdbaccum` for the structural closure.

- **`wdcringnoflush`** — NEW, 2026-08-27, **MEASURED by the Opus seat**, pre-existing on
  `d894e35`, `1cec2da` and the live tree. `ATAPI_PKT_CMD` **never flushes the input ring**.
  Under-drain a DATA-IN transfer and every subsequent CDB is dropped forever, because
  occupancy can never again EQUAL 12: measured `occ 32 -> 44 -> 56 -> 68`. Neither reset
  path recovers it — **`ATAPI_SOFT_RESET` does not flush** (occ stays 32) and the ALT-CTRL
  device reset does not flush (occ 44).

  **This is the OTHER entrance to `#477`'s wedge, and `#477`'s own comment gets it wrong.**
  That comment states *"the 12-byte residue means occupancy can never EQUAL 12 again"* as a
  property of the regression it describes. It is a property of the **device** — reachable
  without any stray read at all. Corrected in place; recorded here because a wrong reason
  gets reused.

  **The in-tree idiom already exists:** `dev_asc.c`'s `dev_asc_fifo_flush()`, called from
  `NCRCMD_FLUSH` and `NCRCMD_RSTCHIP`. So the fix is a transferred warrant, not a design.

  It also **upgrades `wdcsrstnoabort` from READ-and-UNMEASURED to MEASURED**: the same
  measurement shows the reset paths leaving both the flag and the ring untouched.

- **`wdca0abort` — ASSESSED, NOT CHANGED. REFUTED by reading, 2026-08-27.** The kimi seat
  raised a candidate use-after-free as a disjunction: writing `0xA0` mid-transfer either
  (a) NULLs `atapi_st` while `atapi_len > 0`, so the next read derefs NULL in the
  consume-copy at a LOWER offset than the `0x48` `#476` measured, or (b) leaves the pointer
  **dangling**, in which case `#476`'s `atapi_st == NULL` test passes a freed pointer
  straight through. Its sharpest point stands and is worth keeping: **the `0x48` crash
  proves only that the consume-copy does not deref NULL when `atapi_len == 0`; it says
  nothing about `len > 0 && st == NULL`.**

  Both halves are refuted **by construction**, not by argument:

  * **(b)** `scsi_transfer_free` occurs **exactly once** in the device, and the very next
    statement is `d->atapi_st = scsi_transfer_alloc();`. No code runs between them, so the
    pointer is never observable in a freed state. `0xA0` itself frees nothing — the
    `ATAPI_PKT_CMD` arm assigns only the flag and the phase.
  * **(a)** every assignment that makes `atapi_len` positive either **dereferences
    `atapi_st` in the same expression** (so it is non-NULL by construction) or runs after
    the allocation. The remaining writes only decrease it or set it to zero. So
    `atapi_len > 0 && atapi_st == NULL` is not producible.

  **READ, not MEASURED** — recorded as an enumeration a future reader can re-derive rather
  than as an assurance. The stale-pointer consequence the seat was circling IS real and is
  what `#477`'s read-arm repair addresses; it is staleness, not a dangling free.

- **`wdcxferleak`** — NEW, 2026-08-27, READ. Falls directly out of the above, and the kimi
  seat's premise named it without either of us noticing: *"something must free it
  eventually, or every command leaks."* **Nothing does.** The only free is the
  replace-on-next-dispatch, and the device has **no deinit path at all**, so the last
  `atapi_st` of every wdc instance leaks along with its `data_in` and `cmd` buffers.

  Benign — bounded at one transfer per device instance, at teardown, and this emulator is
  not long-lived across many device instantiations. Filed below live defects, and noted
  because it is the kind of thing a future `wdccdbaccum` restructuring should sweep up
  rather than a round of its own.

- **`wdcdataoutparity` — ASSESSED, NOT CHANGED. REFUTED as stated, 2026-08-27; its
  INSTINCT redirects to two rows already filed.** The glm seat argued that `#476` fixed the
  NULL-deref on the READ branch (DATAIN) and that *"the DATAOUT write path must also have
  an `atapi_len == 0` check ... this is the same bug, one access type over."*

  **There is no such path to guard.** `data_out` appears **zero times** in `dev_wdc.c`,
  although `struct scsi_transfer` carries `data_out` and `data_out_len`. The device sets
  `PHASE_DATAOUT`, latches a once-only *"ATAPI DATA OUT phase not implemented"*, and never
  accumulates or dereferences anything. The write-side ATAPI epilogue that DOES dereference
  `atapi_st` sits **inside the dispatch block, after `scsi_transfer_alloc()`**, so it is
  non-NULL by construction — the same reasoning that closed the class in `#476`.

  **But the instinct is sound and points at real rows.** A guest that writes data while in
  `PHASE_DATAOUT` is not ignored: the data-port write arm pushes unconditionally, so those
  bytes enter the SHARED `inbuf` ring. From there they are reachable by
  [[wdcdataoutdrain]] (they can be written to the disk image) and are an instance of
  [[wdccdbaccum]] (one ring aliasing CDB bytes, DATA-IN payload and disk-write payload).

  *So the parity question was worth asking and the answer is that the sibling arm does not
  exist — which is itself the reason the bytes end up somewhere worse.* **READ, not
  MEASURED.**

### *** `dev_asc` IS THE HARDENED SIBLING OF `dev_wdc`, AND THE FORK ALREADY ANSWERED
### WDC'S OPEN QUESTION THERE UNDER `#265`. Found 2026-08-27 while checking a seat's
### in-tree precedent, not by design reasoning. ***

Both devices carry a byte FIFO fed by guest port writes and drained to a SCSI/IDE
backend. `dev_asc` has been hardened three times; `dev_wdc` has the same three classes
and has received only one of the fixes.

| round | what `dev_asc` did | `dev_wdc` today |
|---|---|---|
| **`#265`** | *"fifo_in==fifo_out is also true when the FIFO is exactly full (16); test
the CACHED COUNT so a full FIFO drains instead of being read as empty forever"* — an
explicit `n_bytes_in_fifo` | **UNFIXED.** `inbuf_len = head - tail` has the identical
ambiguity, and `#473`'s own comment in `dev_wdc.c` already states it: *"the latch fired
one store EARLIER than the corruption, because head==tail cannot tell full from empty"* |
| **`#197`** | an empty read must not drive the count NEGATIVE — a later path turned it
into a huge `size_t` alloc and `exit()` | fixed in **`#475`** (the clamp), which is how
`#476`'s NULL deref was woken |
| **`#269`** | warn ONCE PER DEVICE; `fatal()` kept deliberately because under `-q` the
verbosity settles at `VERBOSITY_ERROR` | has per-latch flags |

**WHY THIS MATTERS FOR THE OPEN DESIGN QUESTION.** [[wdcdataoutdrain]]'s candidate fix is
a one-line `inbuf_len > 0 &&`. The option set is wider than that and the fork has already
chosen between them once:

* **(A) one-line guard** — minimal, ships today, and is a FOURTH guard standing in for a
  missing invariant.
* **(B) an explicit cached occupancy count**, exactly `#265`'s answer. It removes the
  head==tail ambiguity that `#473` documented and left standing, and it is the shape the
  fork already reviewed and shipped in a sibling device.
* **(C) a per-phase accumulator**, per `dev_mb89352.c` (`transfer_bufpos`, bounds-checked
  `>= len` on BOTH the read and write arms before indexing) — this is [[wdccdbaccum]].

**(B) was not in the brief's option set.** That is the option-space-completeness failure
this project has now recorded three times: *a brief that lists N options gets a panel
arguing about N options, and nobody proposes the member that was never named.* It was
found by asking a seat to grep the fork rather than by reasoning — which is exactly what
the rule prescribes.

*Recorded as a finding, not a decision. The pass-1 panel is still running and its answer
to Q1 should be read against this.*

- **`wdcwipclear`** -- **REPRODUCED 2026-08-27 with a liveness control**, and it is the ROOT of
  the ring alias rather than another symptom of it. `wdc_command()` clears
  `atapi_cmd_in_progress` and does **not** clear `write_in_progress`, so a packet command
  arriving mid-WRITE leaves both live and the shared ring serving two masters at once.

  The seat built the one-line symmetric fix and measured that it closes the case outright.
  **Not merged into `#478`**: different site, different class, and the stopping rule keeps a
  new finding out of a round unless it is a measured false pass or a wrong record. It is the
  cheapest thing on this list and should be its own round.

  **REPRODUCTION BUILT (scratchpad only; the repo is untouched):**

  ```
  ok   LIVENESS: a WRITE arms write_in_prog   0x30
  FAIL a new command clears write_in_prog     still 0x30 with ATAPI live
  ```

  `0x30` is `WDCC_WRITE`. After the packet command both flags are live at once.
  Regression control clean: 1 failure of 54 rows, so the harness addition is inert.

  **The liveness row is load-bearing and is not decoration.** `diskimage_exist` returns 0
  hardcoded in the harness, so `wdc_command` takes the abort path at its
  missing-image check and `write_in_progress` is NEVER SET -- a fixture without the
  control would pass vacuously and read as a fix. A `stub_disk_exists` control (inert
  by default, following the file's own `stub_datain_len` / `stub_cdrom_poison` idiom)
  is what makes the question answerable at all.

  **Deliberately NOT merged into `#478`.** The stopping rule keeps a new finding out of
  a round that is already built, and this is a different site and a different class.

  *Incidental records defect found while building it: `row_odd_bytecount`'s comment says
  `diskimage_is_a_cdrom()` is one "which this harness does not stub". It IS stubbed, with
  a `stub_cdrom_poison` control. The row's own behaviour is unaffected -- it keeps
  `cur_command` at 0 for a reason that still holds -- but the stated warrant is wrong.*

- **`wdcaliasmeasured`** -- 2026-08-27, evidence attached to [[wdccdbaccum]] rather than a
  new row. **`#478` does NOT close the alias, and the round says so.** MEASURED with `#478`
  applied: a guest issues WRITE SECTORS, then a packet command returning 2048 bytes, then
  **256 ordinary 16-bit words of its own** -- and the disk image receives **512 CD-ROM
  payload bytes and ZERO of the guest's own bytes**.

  That is a cross-medium leak: CD content onto an IDE image, at a guest-chosen LBA, with no
  wide access and no bad-len store anywhere in the sequence. It is the strongest argument
  yet for the structural fix, and it is why `#478` is recorded as a point-guard.

- **`wdcwritecountzero`** -- NEW, 2026-08-27, **ASAN-confirmed by the Opus seat as a host
  SIGFPE** at the drain's `inbuf_len % (512 * d->write_count)`, and **UNREACHABLE**.

  Two seats independently verified the warrant: `write_count` is set only in `wdc__write` as
  `seccnt ? seccnt : 256` (so 1..256), decremented only in the drain, and the drain clears
  `write_in_progress` the instant it reaches zero. No path leaves the flag live with a zero
  count.

  **`#478` does not remove it** -- `inbuf_len > 0` only short-circuits an empty ring, and a
  one-byte push still evaluates the modulus. A `write_count > 0` co-guard would close it for
  free, **which is precisely the ADDITION LICENCE's "it cannot hurt"**, so it is filed rather
  than added. *Recorded here so a future round does not have to re-derive the unreachability
  argument, and so that if a path ever IS found the co-guard is already designed.*

- **`wdcdeclineannounce`** -- NEW, 2026-08-27, an OPEN QUESTION rather than a defect, and it
  is the fourth member of `#478`'s option set that the brief never named.

  `#478` declines the spurious drain **silently**. The Opus seat found that this fork already
  set the opposite precedent in **`#264`**, on the identical question: `dev_asc.c` handles *a
  DATA_OUT transfer with a zero-length buffer* as **decline AND announce** --
  `if (len == 0) { fatal(...); return 0; }`.

  Today the guest gets **zero notice** that its write vanished: `warned_badlen` fires at most
  once per device, the WRITE+PKT door touches no latch at all, and the drain itself emits
  nothing. Against adding it: it is product code, and the licence wants a measured delta or a
  transferred warrant rather than "it cannot hurt" -- though `#264` arguably IS the
  transferred warrant. **Put to the owner; not decided unilaterally.**

### *** THE PANEL CONVERGED ON A FIX THAT WAS NOT ENOUGH, AND THAT IS THE FINDING WORTH
### KEEPING FROM THIS ROUND. Measured 2026-08-27. ***

Four seats independently answered `#478`'s Q1 with *ship `inbuf_len > 0`, file the
structural fix*. It was the right disposition and **the wrong fix**: measured, that guard
leaves the LEFTOVER door open, and the bad-len decline alone leaves the WRITE+PKT door open.
Only both together close all four, and a third plausible form -- the same two conditions
with a struct-field flag -- is **worse than the defect**, silently dropping every later
legal write.

**Unanimity was available for all three wrong answers.** What separated them was a variant
table with an ACCEPT column, built after the panel had answered. *A panel is a source of
candidate mechanisms and a check on premises; it is not a vote on which edit ships, and this
round is the sharpest instance of that on record.*

### *** `wdcwipclear` + `wdcringnoflush` ARE ONE ROUND, AND THE ROUND-SCOPE RULE'S TEST
### WAS ANSWERED BY MEASUREMENT RATHER THAN ASSUMED. Built 2026-08-27. ***

The rule says a second site joins a round only if it is **witnessed**, in the **same
device and same semantic class** under one fix design, and covered by the **same detector
with no new oracle**. All four conditions are now demonstrated rather than argued, because
both reproductions were built against ONE detector:

```
ok   LIVENESS: a WRITE arms write_in_prog   0x30
FAIL a new command clears write_in_prog     still 0x30 with ATAPI live
ok   LIVENESS: the residue is really there  20
FAIL a packet command flushes the ring      20 bytes survive the command
FAIL a soft reset flushes the ring          20 bytes survive a soft reset
```

57 rows, 3 failures; the other 54 stay green, so neither harness control perturbs
anything. **Both liveness rows pass**, which is what separates these from a fixture where
nothing happened.

* **Same function.** Both are `wdc_command()` failing to reset state the previous command
  left behind -- one a flag, one a buffer.
* **Same semantic class**, and it is a sentence rather than a family resemblance: *a new
  command must reset what the old one left.*
* **Same detector, no new oracle.** One reads a flag, one reads ring occupancy; both are
  plain reads of `struct wdc_data` in the existing harness.

**AND THE SOFT RESET IS THE PART THAT MAKES IT CRITICAL RATHER THAN UNTIDY.** A residue
the packet command ignores would still be recoverable if the guest could reset its way
out. It cannot: `ATAPI_SOFT_RESET` leaves all 20 bytes in place. Once occupancy can no
longer EQUAL 12 the CDB dispatch is dead **for the life of the device**, and no sequence
a guest can issue brings it back. Independently measured by the Opus seat as
`occ 32 -> 44 -> 56 -> 68`.

The in-tree idiom exists and is a transferred warrant, not a design: `dev_asc.c`'s
`dev_asc_fifo_flush()`, called from `NCRCMD_FLUSH` and `NCRCMD_RSTCHIP`. *`dev_asc` is the
hardened sibling of `dev_wdc` and has answered this device's open questions three times
now -- `#265`, `#197`, `#269` -- which is worth remembering before designing a fourth.*

- **`wdcstalephase`** — NEW, 2026-08-27, **MEASURED**, and it is the THIRD site of the
  `#479` sentence: *a new command does not reset what the old one left.*

  `wdc_command(ATAPI_PKT_CMD)` sets `PHASE_CMDOUT`. A following `wdc_command(WDCC_WRITE)`
  clears `atapi_cmd_in_progress` and arms the write — and **nothing resets `atapi_phase`**.
  So the device sits in `CMDOUT` with no packet command in progress and a disk write live.

  **Found by the codex seat REASONING a mutant it could not build**, on `#477`'s pass 2. It
  predicted that a phase-only dispatch guard would sweep the detector; built here, it swept
  all 52 rows. `row_stale_phase_write` now pins it, and the consequence is worse than the
  prediction: the guest's sector is not merely short by twelve bytes, it **never reaches the
  disk** (`0 w, 0 b` against a wanted one write of 512).

  **Today this is latent, not live** — the shipped guard tests the flag AND the phase, so
  the stale phase alone dispatches nothing. It is filed because it is a loaded gun: any
  future edit that trusts the phase alone re-opens it, and `#477`'s own comment ENCOURAGED
  exactly that reading until it was corrected. *A latent defect whose documentation points
  a future round straight at it is worth more than its severity suggests.*

  Ships with `wdcwipclear` and `wdcringnoflush` — same function, same sentence, one fix
  design, one detector. **Three sites now, and the round-scope rule is satisfied for all
  three by measurement rather than assertion.**

- **`wdcdatainnull`** — NEW, 2026-08-27, READ, found by the Fable seat on `#477`'s pass 2.
  A structural asymmetry between two refill sites that do the same job:

  * the **dispatch** refill checks `if (d->atapi_st->data_in != NULL)` before indexing;
  * the **read-arm** refill indexes `d->atapi_st->data_in[...]` with **no NULL check at
    all**.

  `#476` closed `atapi_st == NULL`. **Nothing closes `atapi_st->data_in == NULL`**, and
  `dev_wdc.c` holds no invariant coupling the two.

  **Not currently reachable, and the warrant is CROSS-FILE — which is the point.**

  *** MY FIRST FILING OF THAT WARRANT WAS WRONG IN TWO DETAILS, both corrected by a farmed
  seat and then VERIFIED by reading. Recorded because the wrong version was the stronger-
  sounding one, and a warrant that sounds stronger than it is will be leaned on harder. ***

  * I wrote that `scsi_transfer_allocbuf()` **"sets pointer and length together"**. It does
    not: `(*lenp) = want_len` at `:147`, `(*pp) = p` at `:161` — fourteen lines apart, with
    a `malloc` and a possible `exit(1)` between them. **The invariant is a FUNCTION-BOUNDARY
    property, not a continuous one.** Nothing observes that window (no callback and no
    return to the device runs inside it), but "set together" was false.
  * I wrote that `data_in_len` is mutated outside the helper **"at exactly one site"**.
    There are **THREE**: `diskimage_scsicmd.c:599` (MODE_SENSE), `:1169` (READ_TOC), and
    `dev_asc.c:529` — **which is a different device entirely**. All three only shrink or
    preserve a live allocation, so the conclusion survives; the census did not.

  **DISPOSITION: a COMMENT at the unchecked site, not a guard** — now written. The ADDITION
  LICENCE wants a measured delta or a transferred warrant and there is neither, because the
  state is not producible today. What was missing is not a check that would silently never
  fire, but **a reason an edit in another file can break**. A guard would have hidden the
  cross-file coupling; the comment names it. So `data_in == NULL && data_in_len > 0` is unproducible **today, in
  another file** — which is exactly the shape of warrant that decays without anyone
  touching `dev_wdc.c`.

  Filed below live defects. *The cheap disposition is not a guard but a sentence: record
  the cross-file invariant at the unchecked site, so a future edit to `diskimage_scsicmd.c`
  has something to break rather than nothing to notice.*

### *** PREMISE 5 WAS WRONG IN BOTH DIRECTIONS AT ONCE, AND A PACKET-FED SEAT FOUND IT
### FROM THE BRIEF'S OWN INLINED FACTS. Measured 2026-08-27. ***

`#479`'s brief asserted the ring residue is **unrecoverable**, having measured that neither
`ATAPI_PKT_CMD` nor `ATAPI_SOFT_RESET` flushes it. `ollama_kimi` -- which **cannot read the
tree at all** -- replied that the brief's own inlined facts admit a drain path nobody had
examined. It was right:

```
ok   P5: a write drains the residue         0
FAIL P5: recovered sector is the guest's    first=0xaa, guest wrote 0x55
```

A guest holding 20 bytes of residue arms WRITE SECTORS and streams 492 of its own bytes.
Occupancy reaches 512, the drain fires, the tail advances, **and the ring clears**. So
"unrecoverable" is FALSE.

**And the recovery corrupts the sector it recovers through.** The drain writes the ring's
first 512 bytes, and the first 20 of those are the residue -- so the disk receives `0xaa`
where the guest wrote `0x55`.

> **RE-SCOPED: [[wdcringnoflush]] is not a pure denial-of-service. It is a DATA-INTEGRITY
> defect with a denial-of-service face**, and the only way out of the denial runs through
> the corruption. Both dispositions the round considered were wrong.

*This is the packet-fed seats doing exactly what the doctrine says they are for: blind to
the repository, so they attack the ARGUMENT. No file-reading seat produced it, and the two
flagship seats did not either. **Their blindness is a feature** -- and the concrete lesson
is that a brief which inlines its facts honestly gives them enough to refute it with.*

**And the option set had the same shape of hole.** Four seats independently found that the
brief added a THIRD site (`wdcstalephase`) to its header and never updated options A-E, so
none of them fixes all three. The sixth member they converge on: **one helper clearing flag
+ ring + phase**, called from command entry and every reset path. *That is the
grep-for-siblings rule failing inside a brief written to teach it.*

The clause-(d) mutant for that fix is already named, by `deepseek`: **move the ring flush
from the top of `wdc_command` to the end.** It passes every pinned row and destroys the
IDENTIFY response, because IDENTIFY loads its 512-byte answer INTO the ring as part of the
command.

### *** `wdcaltctrlbit` IS NOT LOW SEVERITY IN THE ROUND THAT MATTERS -- IT IS A
### PRECONDITION. Settled 2026-08-27 by a farmed seat with CITED driver source. ***

Re-scoped LOW this morning on the reasoning that the wrong bit works BY ACCIDENT, because
the conventional reset value `0x0C` has bit 3 set anyway. **That reasoning was measured
against the wrong question.**

The grok seat was asked whether real drivers write `0x08` to Device Control, and answered
with source rather than recollection:

| driver | reset write | steady state |
|---|---|---|
| Linux libata (`ata_bus_softreset`) | `ap->ctl \| ATA_SRST` | `ap->ctl`, initialised to `ATA_DEVCTL_OBS` = **`0x08`** |
| NetBSD `wdc_do_reset` | `WDCTL_RST\|WDCTL_IDS\|WDCTL_4BIT` = `0x0E` | — |
| OpenBSD 3.4-era `__wdcdo_reset` | `WDCTL_4BIT\|WDCTL_RST` = `0x0C` | — |
| **older OpenBSD** | **`WDCTL_RST\|WDCTL_IDS` = `0x06`** — bit 3 CLEAR | then `WDCTL_4BIT` = `0x08` |

**Two consequences the LOW scoping did not see:**

1. **An older-OpenBSD reset is MISSED ENTIRELY** (`0x06` has bit 3 clear), and the `0x08`
   that follows is then treated AS the reset. The device latches the ATAPI signature on
   the release rather than on the reset -- backwards, on a real driver.
2. **libata holds `0x08` as its STEADY-STATE control value.** So `0x08` is not an unusual
   write; it is the value the register spends most of its life holding.

> *** THIS DECIDES `#479`'s SCOPE. *** Option F-wide -- extending the reset helper to the
> ALT-CTRL arm -- would flush the ring and cancel a pending write **every time a driver
> writes its ordinary control value**, possibly mid-transfer. That is a far worse
> regression than the three defects being fixed, and it would pass any row that only
> exercises the reset path.
>
> **So F-wide REQUIRES fixing this bit in the same round.** `wdcaltctrlbit` is low as a
> standalone defect and LOAD-BEARING as a precondition, and those are different numbers
> for different questions.

*Recorded because the earlier LOW is still true of the standalone defect and would
otherwise be read as settling the scope question too. **A severity is an answer to a
question, and this row now carries two.***

*And this is what the fan-out bought: a CITED answer about driver behaviour that no amount
of reading the emulator source could produce. The emulator cannot tell you what a real
driver writes.*

### *** `#479` SCOPE SETTLED: F-NARROW. And a SHIPPED ROW WILL GO RED WHEN THE FIX LANDS,
### which puts this round under the ORACLE-CORRECTION RULE before a line of code changes. ***

**The scope.** Three seats converged on **F-narrow**, and the argument is better than the
count. grok put it exactly: *"The three command-register sites are one round; **ALT-CTRL is
not a fourth site of the same sentence.**"* Build one named abort helper, call it from the
TOP of `wdc_command()` only, and let it absorb the existing `atapi_cmd_in_progress = 0`.
Real SRST (`wdcaltctrlbit` + `wdcsrstnoabort`) becomes a LATER round that may **call** the
same helper -- which is why F-narrow is not a compromise: it builds the thing the ALT-CTRL
round will need.

minimax named the obligation: **an accept row pinning that a legal `0x08` Device Control
write does NOT flush the ring or clear `write_in_progress`.** That row is what stops a
future round walking into the trap grok's driver citations identified.

**AND THE ROUND'S OWN DETECTOR OPPOSES ITS FIX.** `row_stale_phase_write` -- shipped in
`832bed7` -- carries a LIVENESS assertion that the phase is still `PHASE_CMDOUT` after a
WRITE command. That is the DEFECT state, deliberately pinned so the row could not pass
vacuously. **Option F resets the phase, so that assertion inverts and the row goes red.**

> That is not a reason to weaken the row. It is the ORACLE-CORRECTION RULE's exact case, and
> the rule is about ORDER:
>
> **Re-pin the oracle FIRST. Measure the COMMITTED build RED under the new expectation.
> THEN change the code.** Same scripts, opposite colour. Without that red, re-pinning is
> observationally identical to fitting the test to the binary.

Three obligations follow, and they are cheap:

* the re-pinned comment must quote the source VERBATIM with its construct name, so a future
  seat can re-derive it without trusting this round;
* the OLD pin's claim is corrected in place, not silently superseded;
* **a re-pin that removes the last failing row is not finished** -- the row's other two
  assertions (no CDB dispatch, the sector survives) stay valid and must still red under the
  phase-only mutant, or the round has traded a real oracle for a tautology.

*Recorded before any code is written. A seat asked whether the fix would break this row; the
answer is yes, and finding that BEFORE the edit is the whole difference between an
oracle correction and a laundering.*

### *** `#479` DECIDED BY A FIVE-VARIANT MATRIX, NOT BY THE 4-1 SPLIT. Measured 2026-08-27. ***

The panel divided: three seats for F-narrow, codex for a seventh option **G** (F-wide plus
the accept row, with the helper hung off a CORRECTED `WDCTL_RST`). The carrier's rule is
that disagreements are settled empirically, and the Fable seat built the matrix:

| variant | non-P5 rows RED |
|---|---|
| `v1_narrow` — helper at the **TOP** of `wdc_command` | ctl-SRST still unflushed (matrix obs., not a shipped row) |
| `v2_widecur` — flush off `WDCTL_4BIT` | **ctl write mid-transfer `0 w, 0 b`** + 256 orphaned bytes |
| `v3_widerst` — flush off `WDCTL_RST` | **none — the cleanest variant** |
| `v4_endflush` — flush at the **END** | **IDENTIFY destroyed 256/256 words**, READ destroyed, SRST |

**FOUR THINGS THIS SETTLES THAT ARGUMENT COULD NOT:**

1. **The end-flush mutant is a regression the shipped detector CANNOT SEE.** Strip the new
   rows and `v1_narrow` and `v4_endflush` have **identical failure sets**. It is the
   reads-as-an-improvement shape — clean-up-on-exit looks *more* principled — and it
   destroys the IDENTIFY response, which the command loads INTO the ring.
2. **grok's citation-based warning is confirmed empirically.** `v2` cancels a legal
   transfer on a routine `0x08` write. Reproduced independently by
   `row_devctl_preserves_write` here: GREEN on HEAD, RED under the v2 shape.
3. **F-narrow does NOT fully establish its own invariant** — Device-Control SRST bypasses
   `wdc_command`. That **strengthens [[wdcringnoflush]]**: the canonical reset a real
   driver uses does not recover either.
4. **A new corruption path on the READ side** — a guest READ after an under-drain is handed
   the previous transfer's residue at the head of its sector. The defect is not confined to
   the write-drain.

**DECISION: F-narrow this round**, with the accept rows, and **the SRST gap recorded as a
RED ROW rather than as silence**. `wdcaltctrlbit` + F-wide-RST becomes the follow-up.

*codex's G is not refuted — `v3` proves it is the cleanest end state. It is a BIGGER ROUND,
and the matrix is what turns that from a preference into a schedule.*

**AND THE BATTERY IS BLIND TO ALL OF IT.** Measured: no gate in this tree arms a CDROM, so
the ALT-CTRL/`COMMAND_RESET` path is never exercised by any rig. The offline accept row is
the ONLY instrument that will ever see this class — which is why it was built before the
option was chosen rather than after.

**A SECOND ORACLE CORRECTION IS OWED.** `row_residue_recovery`'s two P5 rows pin the
DEFECT's shape and therefore go red under *every* fix, for the fixture's reason rather than
the code's. They must be REPLACED by the re-cut form, not left beside it — the same
order rule already applied to `row_stale_phase_write`. **Two oracle corrections in one
round, both identified before any product code changed.**

### *** THE FOLLOW-UP ROUND IS NOT `wdcaltctrlbit`. IT IS `SRST DOES NOT EXIST`, and the
### bit is a rider. Sharpened 2026-08-27 by farmed research read late. ***

A 2.1 MB farmed answer sat unread for two hours while the round it informs was being
designed. **Third instance of the unread-review class this project has recorded, and the
content changed the next round's scope.**

**It CONFIRMS the LOW rank on the wrong bit** -- signature latching only, Linux and NetBSD
reset sequences carry both bits, OpenBSD reaches the same endpoint accidentally, and no rig
has IDE-CDROM coverage. So `wdcaltctrlbit` stays LOW as a standalone decode defect.

**AND IT REFUSES TO LET THAT RANK SUBSUME THE REAL DEFECT:**

> *"Do not let that LOW rank subsume the missing SRST behavior. A reset that cannot abort
> or discard stale transfer state undermines the guest's recovery mechanism and deserves a
> separate, higher-severity assessment -- likely medium impact."*

**AND IT CORRECTS MY CLASSIFICATION.** I had SRST filed as a fourth instance of `#479`'s
sentence -- *a new command does not reset what the old one left*. It is not:

* the three `#479` sites belong to `wdc_command()` and **command-boundary initialisation**;
* SRST enters through the **sibling ALT-CTRL handler**, is a **channel/device recovery**
  operation, and has **assertion/deassertion semantics**;
* **the code does not remember the previous Device Control value, so it cannot distinguish
  assertion from deassertion at all.** SRST is a LEVEL signal -- asserted, then released --
  and a device blind to the edge cannot implement it however much state it clears.

*That last point is the one I had not considered, and it means the follow-up round is not
"call the helper from the ALT-CTRL arm". It has to give the device an edge to act on first.*

> **SCOPE FOR THE FOLLOW-UP: `wdcsrstnoedge` -- SRST is not implemented, only latched.**
> The round owes an edge (remember the previous control value), an abort (what SRST must
> discard), and only then the shared cleanup helper `#479` builds. `wdcaltctrlbit` rides
> along as the predicate fix, because the edge cannot be detected on the wrong bit.

*The decomposition itself is unchanged and now has two independent derivations: grok
reached it from "ALT-CTRL is not a fourth site of the same sentence", codex from
"it merits its own issue and tests, though it can share a cleanup helper". `#479` building
the helper is what makes that round cheap.*

### *** `landiskaux` AND `wdcaltctrlbit` MUST SHIP TOGETHER, OR THE CHEAP ONE ACTIVATES
### THE OTHER'S BUG ON A REAL RIG. Verified by construction 2026-08-27. ***

`landiskaux` looks like the easiest fix on the queue: `dev_wdc.c` computes
`alt_status_addr = devinit->addr + 0x206` and then carries a switch labelled *"Special
hacks for individual machines"* with cases for MACPPC (`+0x160`), HPCMIPS (a hardcoded
address) and IQ80321 (`+0x402`). **There is no LANDISK case**, so it falls through to the
default while a seat MEASURED the OpenBSD 7.6 driver writing `+0x2c` — twelve Device
Control writes during probe, all landing on unmapped memory.

One `case MACHINE_LANDISK:` line fixes it.

> *** AND SHIPPING THAT LINE ALONE WOULD MAKE THE ALT-CTRL ARM LIVE ON THAT MACHINE, WITH
> ITS PREDICATE STILL WRONG. ***
>
> Of the twelve measured writes, **six are `0x08`** — `WDCTL_4BIT`, the exact bit the arm
> triggers on, and one of them falls between two commands. Today all twelve are unmapped,
> so the wrong predicate is inert on landisk. Map the register and the device starts
> latching `COMMAND_RESET` on six routine control writes per probe.

**So the ranking inverts against intuition.** `landiskaux` is a one-line mapping fix and
`wdcaltctrlbit` is LOW — and doing the cheap one first ships the LOW one's bug into a rig
that currently cannot reach it. They are one round, and the bit fix is the prerequisite,
not the rider.

*This is the second time today a severity has turned out to be an answer to a question
rather than a property of a row: `wdcaltctrlbit` is LOW standalone, LOAD-BEARING as a
precondition for F-wide, and now a PREREQUISITE for a one-line mapping fix. Three numbers,
three questions, one defect.*

*Found by verifying a seat's measurement rather than transcribing it — the switch's own
comment says "Special hacks for individual machines", which is what made the missing case
obvious once the file was open.*

---

## 2026-08-27 -- three findings from `#479`'s pass 2, filed rather than fixed

The round was already committed when this panel returned. Under the **late-dissent rule**
that changes the licence, never the truth-value: wrong records were corrected in place, the
floor breach became `#480`, and these three are **disposition 3 -- new queue items carrying
the dissent verbatim**, so no future reader sees false unanimity.

### `wdccylstale` -- the cylinder registers publish the PREVIOUS transfer's byte count

**Named by the grok seat, measured independently by opus, and reproduced here. MEDIUM.**

`dev_wdc.c`'s CYL_LO/CYL_HI read arms override the guest's own written byte-count limit
whenever `atapi_cmd_in_progress` is set:

```c
if (d->atapi_cmd_in_progress) {
        int x = d->atapi_len;
        if (x > 32768)
                x = 32768;
        odata = x & 255;            /*  and (x >> 8) & 255 for CYL_HI  */
}
```

`#479`'s helper clears the flag, the phase, the writer and the ring. It does **not** clear
`atapi_len`, because `atapi_len` is cleared on the **dispatch** path -- and a packet sitting
in `PHASE_CMDOUT` has not reached it yet. So the window is exactly *after `ATAPI_PKT_CMD`,
before the twelfth CDB byte*, and in it the guest reads back the residue of a transfer it
already abandoned.

**Three measurements, two of them independent of this file:**

| who | what it saw |
|---|---|
| opus, register-level witness probe | `phase=0x9 cyl=0f9c (want 0000) len=3996 recv=100` -- identical on PRE, HEAD, `M4`, `M11` |
| this round, seeded reproduction | `wrote 0x800 read 0x600` -- the guest sets a 2048-byte limit and reads back 1536 |
| grok, by reading | *"Cylinder registers still expose leftover `atapi_len` ... a new packet can publish the previous transfer's byte count"* |

**The device already states the invariant it breaks here.** `dev_wdc.c` (grep `In CMDOUT the`), in the
*read* arm's own comment:

> *In CMDOUT the `atapi_len`/`atapi_received` pair describes the PREVIOUS transfer, so no
> completion state may be derived from it*

The read arm obeys that and falls through. The cylinder arms derive a guest-visible byte
count from exactly that pair. **One arm of the device documents the rule the other breaks.**

> *** THE FABLE SEAT DISSENTED, AND THE DISAGREEMENT IS RECORDED RATHER THAN AVERAGED. ***
> It answered Q1 *"no fourth thing"*, holding that `atapi_len`/`atapi_received` are *"gated
> by `atapi_cmd_in_progress`"* and therefore *"inert when stale"*. They are inert while the
> flag is **clear** -- and a new `ATAPI_PKT_CMD` **re-sets** it before the CDB completes,
> which is the whole window. That is a READING against two MEASUREMENTS, and the carrier
> settles disagreements empirically. Recorded here because a dissent that turns out wrong is
> still evidence about what the next reader will assume.

**Opus's cautions, which are why this is not a blind one-line add:** the pair must be cleared
**together** (clearing `atapi_received` alone makes the refill read from offset 0 of a stale
transfer), and `M18_clearlen` -- the obvious fix -- **also sweeps all 80 rows
byte-identically**, so the suite cannot observe this question *in either direction*. The
round that takes it owes a row first.

### `wdcatapisig` -- a stub default silences the ATAPI signature branch, on every row

**Named and measured by the fable seat. MEDIUM, and it is the endianness defect's twin.**

`stub_cdrom_poison = 0` is the memset default -- *"0 = nothing is a CD-ROM"* -- and it
silences the CD-ROM branch exactly the way `byte_order = 0` silenced the little-endian one.
Measured: `odata = 0x14;` -> `0x00;` (CYL_LO) and `odata = 0xeb;` -> `0x00;` (CYL_HI) **both
escape all 80 rows, and both escape `#480`'s 83.**

This is the ATAPI-detection signature a guest reads after reset, it is correct on the shipped
build, and no row sets `cur_command == COMMAND_RESET` with a CD-ROM present and reads the
cylinder registers with the flag clear. **A true coverage gap, not a dead branch.** Roughly
ten lines closes it.

*Honest reachability caveat, the seat's own:* reaching `COMMAND_RESET` live goes through the
ALT-CTRL `WDCTL_4BIT` path, so it is entangled with `wdcaltctrlbit`/`landiskaux`; a rung-3
probe reaches it directly.

> **THE CLASS IS WORTH MORE THAN EITHER INSTANCE: A STUB'S DEFAULT VALUE IS AN UNTESTED
> BRANCH SELECTOR.** Twice now a field left at its `memset` zero has hidden an entire arm
> from every row in the file, and in both cases the escape was byte-identical -- invisible to
> md5, to row counts, to everything except a mutant aimed at the silenced arm. **Any stub
> whose value selects a branch owes at least one row on each side.** `stub_disk_exists` was
> checked and is *not* an instance (rows set it to 1 deliberately).

### `wdcletwins` -- the endianness coverage residue, both arms of the read path

**codex, opus and fable independently. LOW-MEDIUM, and cheap.**

`#478`'s two-arm coverage rests on **exactly two rows**, both write-side. Measured
consequences:

* **The read-side byte assembly is pinned by nothing on either arm** -- `LEread <<8 -> <<0`
  and `BEread <<8 -> <<0` both escape.
* **Whichever arm is the default gets the 78-row bulk; the other gets two rows.** Flipping
  the default makes BE-arm `badlen` deletion escape while LE-arm deletion is killed by three
  rows -- exactly reversed.
* `Mbe_swap`, swapping the push order on the arm 78 rows actually run, escapes on **both**
  defaults.

**The mechanism is a palindrome census**, and it is the file's own word-47 lesson recurring
at the data port: nearly every two-byte payload in the suite is a byte-palindrome -- `0x7c7c`,
`0x6d6d`, `0x3333`, `0x7777`, `0x6b6b`, `0x5555` -- so a swap is invisible by construction.
No oracle anywhere inspects the CDB bytes the dispatch assembles, because
`diskimage_scsicommand` ignores `xferp->cmd`.

**Opus measured the cheap disposition: looping the suite over both arms costs nothing** (a
flipped run is 0 failures, byte-identical), which beats adding LE twins row by row. Keep the
default; add non-palindromic anchored rows for the push order and one per read-side arm.

---

## 2026-08-27 -- `#481` filings, and one of them was ALREADY CLAIMED IN THE PAST TENSE

> *** THE FABLE SEAT CAUGHT THIS BEFORE IT SHIPPED: `wdcponsig` was asserted as "filed with
> measurements" in TWO commit-bound artifacts while appearing in ZERO queue files. Verified:
> `OUTSTANDING_BUGS.md` 0, `CHANGELOG.md` 0, `ledger.json` 0. ***
>
> The docs step being pending is ordinary. **The defect is that the past tense shipped ahead
> of the action** -- had the commit landed as written, two durable records would have
> asserted a filing that did not exist. That is the score-claim rule one level up: *a record
> may not assert a completed action in the past tense until the artifact exists.*

### `wdcponsig` -- the device presents no ATAPI signature at power-on

**MEASURED** (`_scratchpad/ponrepro.py` -> `_scratchpad/pon/`, against `7d0b63d`):

```
FAIL a CD-ROM signs itself at power-on      0x0000 want 0xeb14
ok   control: a non-CD-ROM does not sign    0x0000
ok   control: the reset signature works     0xeb14
90 rows, 1 failures
```

Both controls are load-bearing and both green: the non-CD-ROM row stops the assertion being
satisfied by a device that signs unconditionally, and the reset-signature row separates *"the
power-on half is missing"* from *"the signature is broken"* -- two different repairs.

**Mechanism, verified by reading:** `0x14` and `0xeb` appear once each in `dev_wdc.c`, both
inside `if (d->cur_command == COMMAND_RESET && diskimage_is_a_cdrom(...))`. `DEVINIT(wdc)`
memsets, so `cur_command` is 0 and never `COMMAND_RESET` at power-on. **Both signature sites
are dark regardless of which bit the arm tests.**

**WHY IT WAS FILED RATHER THAN FOLDED INTO `#481`, and the second reason is decisive:**

1. A seat's scenario matrix shows power-on dark **both pre- and post-fix**
   (`artifacts/wdcaltctrl/killtable_20260827/scenario_matrix/sig_cur.out` vs `sig_a1.out`,
   row 1 in both). **The bit fix does not regress it.**
2. **The offline differential cannot witness it at all.** Every row builds its device with
   `memset` and none runs `DEVINIT`, so an init-time repair is invisible to the entire file.
   Folding it in would require a NEW ORACLE, which the round-scope rule forbids.

> **RIDER FROM THE FABLE SEAT, and it changes the ranking: `#481` NARROWS the accidental
> supply window.** Before it, almost any Device Control write lit the signature by accident;
> now only a real reset does. So a guest that reads the signature without ever resetting has
> fewer accidental paths to it than before. **`wdcponsig` ranks HIGHER after this round than
> before it**, even though the round did not regress it.

**What it needs:** a construction (rung-2) or rung-3 witness, since the differential cannot
see `DEVINIT`. Per the lifecycle's standing ask, one seat should be asked to attempt a rung-3
probe before it is recorded rung-1 -- that ask produced a witness in a single invocation the
last time it was made.

### `wdcaltctrlcov` -- three edits that pass all 94 rows of `#481`'s detector

**MEASURED by the fable seat**, each against the full detector and then against a defect demo
with the shipped build as green control. Filed as COVERAGE DEBT: the detector is above the
vacuity floor -- (a) five pre-fix reds, (b) `Mb_revert` killed, (c) `Mc_null` compile-fails,
(d) every fix-predicate mutant killed -- and these are new adversarial finds against a clean
table, which the stopping rule files rather than fixes.

| mutant | edit | escape | defect re-opened |
|---|---|---|---|
| **`Mq_flag`** | qualify the helper call `if (d->atapi_cmd_in_progress)` | 94/0 | **SRST no longer aborts a plain ATA write -- the MAJORITY path.** wip `0x30`, occ 16 survive the reset |
| `Mq_wip` | qualify by `write_in_progress` instead | 94/0 | SRST no longer aborts a packet-only CDB: flag 1, occ 6 survive |
| `Mw_hob` | widen the mask to `(WDCTL_RST \| 0x80)` | 94/0 | routine-write-destroys-command, re-opened for HOB ctl values: `0x88` with `0xec` executing destroys `cur_command` |

**Negative control that proves the table is not limp:** `Mn_hoist` -- the helper hoisted out
of the guard -- is KILLED by four rows, exactly the `#479`/`#480` accept rows.

> **ROOT CAUSE, and it is about how a row was CUT rather than what it asserts: the
> sole-carrier abort row bundles `write_in_progress` + `atapi_cmd_in_progress` + phase + ring
> into ONE assertion.** Any SINGLE-conjunct qualification of the call therefore still passes
> it. Separately, the detector's whole ctl vocabulary is `{0x02, 0x06, 0x08, 0x0a, 0x0c}`, so
> bits 0, 4, 5, 6 and 7 are unpinned on the accept side -- which is why `Md_widemask` catches
> only the IDS widening and not the HOB one.
>
> **This is the pre-table check's guard-field/body-field clause arriving from the mutant side
> instead of the field side.** The check asks which fields the guard reads versus which the
> body reads, and owes a state where they DISAGREE. The abort row asserts them only in
> agreement.

**Closes with three rows, already shaped by the seat's demos:** an ATA-only-in-flight abort
row, a packet-only-in-flight abort row, and an accept row `a 0x88 HOB write is not a reset`.
**Rank `Mq_flag` first** -- its re-opened defect fires on the commonest reset scenario there
is.

*Recorded honestly: the seat notes a strict reading of the pre-table guard-field check would
call the disagreement-state row OWED AT CONSTRUCTION rather than filed. Its own reading is
that the check protects the ask-again cap and is not a floor clause. That is an adjudicator's
call and is left open here rather than settled by the author of the row in question.*

### `wdcresetirq` -- `error` and the interrupt line are not cleared by a reset

Filed with its warrant and its trap, both from seats:

* **Transferred warrant:** `dev_asc_reset()`'s `#266` clause -- a chip reset releases the
  interrupt output. A channel reset legitimately clears more than a new command does, and
  `error` is the other half (a new command must preserve the previous command's error until
  the guest reads it; an SRST discards it).
* **Measured trap, and it is why this is not a one-liner:** `interrupt.h` calls through the
  deassert pointer **unconditionally**, so every detector row that writes ctl would have to
  wire `irq.interrupt_deassert` or the harness segfaults -- **in a way that reads as a
  detector defect rather than a fixture defect.** A seat hit exactly this.

Nothing in `#481` measures either, so both stay filed rather than riding along.

### `wdcaltdecode` -- THREE DECODE PATHS INTO THE CONTROL REGISTER THAT NO ROW COVERS

**All three are PRE-EXISTING and none is introduced by `#481`. But `#481` ENLARGES ALL
THREE**, and that is why they are filed together rather than separately.

The alt-ctrl handler reads `idata = data[0]` and **never consults `len` or
`relative_addr`**, while the main handler uses `memory_readmax64(cpu, data, len)`. Every one
of the detector's altstatus calls is `len=1, offset=0`, so none of this is exercised.

| # | finding | pre-fix | post-fix |
|---|---|---|---|
| 1 | **`wdc_altstatus` is registered with LENGTH 2**, so a guest store to the byte ABOVE it decodes as a Device Control write | inert for `0x06` | **latches the reset and performs a FULL CHANNEL ABORT** (`wip 0x30->0, occ 40->0`) |
| 2 | a 2-byte write with the control byte in `data[1]` | silently dropped | silently dropped |
| 3 | **`io_enabled` is checked in `DEVICE_ACCESS(wdc)` only, never in the alt-ctrl handler.** With the function disabled the taskfile goes dark and Device Control stays live | inert | **SRST still gives `wip 0x30->0, occ 40->0, atapi 1->0` on a function the guest has DISABLED** |

All three MEASURED at rung 3 by the opus seat on unmodified `evbmips -e malta`.

> **THE PATTERN, and it is the round's real cost: `#481` CONVERTS A BENIGN SIGNATURE-LATCH
> TOGGLE INTO A DESTRUCTIVE STATE ABORT, on decode paths no row covers.** Before the fix
> these paths set a latch that changed two register reads. After it they clear the writer,
> the ATAPI flag, the phase and the ring.
>
> **That is the de-escalation clause's concern arriving from the OPPOSITE DIRECTION.** The
> clause exists because removing a host-fatal makes guard growth silent. Here the round did
> not remove a diagnostic -- it gave an existing predicate TEETH, and every path that
> reaches that predicate inherited them. *A fix that makes a guard more powerful owes the
> same enumeration as one that makes it quieter: which paths reach it, and are they all
> intended?*

**Not a floor breach** -- the seat that found them says so explicitly, and the round's
detector is above the floor on all five clauses. Filing material, ranked by finding 1 (a
one-byte address error by a guest now costs it the whole channel state).

*The `0x3f7` Drive Address Register identification is READ from general ATA knowledge; there
is no ATA document in this tree, and the seat flagged that itself. What is MEASURED is that
the store lands in the Device Control handler and what it now does there.*

### `wdcaltctrlcov` -- UPDATED by `#482`: four closed, and the two flagship seats RANK THE REST DIFFERENTLY

`#482` closed the single-conjunct-qualifier family. **Both flagship seats ratified the four
rows and both then built the SAME escape independently** -- Opus's `M1_disj` and Fable's
`disj2` are the same edit, reached by different routes:

```c
if (d->write_in_progress || d->atapi_cmd_in_progress)
        wdc_new_command_reset(d);
```

> *** IT IS PRECISELY THE REPAIR A MAINTAINER WRITES AFTER READING THE FOUR NEW ROWS ***
> -- *"only abort if something is actually in flight"* -- **and it defeats all four**,
> because every one of them arms at least one of those two flags.
>
> **The state that kills it -- ring non-empty, `wip == 0`, `flag == 0` -- has no row, and it
> is GUEST-REACHABLE.** Verified by reading: the `#464` tenant test at the DATA write arm
> gates ONLY the one-shot diagnostic; the `wdc_addtoinbuf()` calls sit OUTSIDE it and push
> unconditionally. A guest can leave the ring dirty with nothing armed, then SRST.
>
> **So a row set can be individually correct and collectively misleading.** Each of the four
> is right; together they teach the wrong property. Nothing in the vacuity floor catches
> that, and it is the most useful thing this panel produced.

**MEASURED** by both seats, escaping all 100 rows:

```
  pristine:   ok   an SRST purges an orphan ring   live 16 occ 0
  disj2:    FAIL   an SRST purges an orphan ring   live 16 occ 16   (drq 1 vs 0)
```

#### *** THE TWO SEATS RANK THE REMAINDER DIFFERENTLY, AND BOTH ARE RIGHT ON THEIR OWN AXIS ***

| seat | ranks first | argument |
|---|---|---|
| **opus** | the **orphan-ring** row (kills `disj2` + two more) | it is the edit *a maintainer is most likely to write*, and the round's own rows invite it |
| **fable** | **`&& !d->lba`** | it defeats the abort on **every LBA-mode driver** -- essentially all modern ATA writes -- which is broader than the non-LBA path `#482` closed |

**That is LIKELIHOOD versus BLAST RADIUS, and neither is wrong.** Recorded as a real tension
rather than averaged into a single number, because the next round has to pick one and should
know it is choosing between two defensible axes.

*My reading, offered as a reading and not a ruling:* take the orphan-ring row first. `disj2`
is the edit that gets written; `&& !d->lba` is bizarre enough that nobody writes it by
accident. But `!d->lba` has the larger consequence if it ever lands, and `altctl_fresh()`
pins `lba = 0`, so closing it needs a new fixture variant -- a legitimate scope boundary and
a reason it was correctly filed rather than closed here.

#### Still open after `#482`, with the escapes measured

* **abort gating** -- `disj2` (both seats), `wipocc` / `M5_wip_or_ring` (both seats).
  **The ring-alone disagreement cell is the uncovered one.**
* **state qualifiers** -- `&& !d->lba` (fable, measured: `wip 0x30 occ 16` survives),
  `d->drive == 0`, `d->head == 0`, `d->seccnt == 0`. **Four of these are guards on fields
  `altctl_fresh()` PINS, and are unkillable by any row in the file by construction.**
* **free mask bits** -- `0x40` escapes (fable's `hob6`); the `0x88` row pins bit 7 only.
  **Opus's proposed 256-value sweep -- *the reset latches IFF bit 2 is set* -- replaces the
  single-value pin, closes every mask widening, and REMOVES THE APPEAL TO ATA KNOWLEDGE THIS
  TREE DOES NOT HOLD.** Best value of the four proposed rows.

#### The pre-table-check question, resolved

Fable had left open whether the guard-field/body-field disagreement row was OWED AT
CONSTRUCTION or filable. **Its own answer, now that the rows exist: "owed, and now
delivered."** But the matrix is not saturated -- the ring-alone cell remains, and `disj2`
exploits exactly it. File ring-alone as the immediate companion.

### `wdcaltfixture` -- the altctl fixture is a SINGLE POINT IN STATE SPACE

**MEASURED by the opus seat: ELEVEN single-field qualifications escape every row in the
file.** `altctl_fresh()` memsets the struct, so every altctl row runs at one point, and any
predicate true at zero escapes the lot:

```
  !d->lba          d->atapi_st == NULL   !d->int_assert    d->drive == 0    d->head == 0
  d->seccnt == 0   !d->error             d->sectorsize == 0                 d->atapi_len == 0
  d->write_offset == 0                   d->cyl_lo == 0 && d->cyl_hi == 0
```

> **FILE AS ONE ITEM, NOT ELEVEN.** `&& !d->lba` -- the fable seat's blast-radius pick -- is
> the measured EXEMPLAR of this class, not a row of its own. Closing it alone buys one of
> eleven.

**ONE "busy device" row kills all eleven, and the seat built and measured it**: every
non-tenant field non-zero, both tenants armed, 16 bytes staged, assert the abort. Pristine
104 rows / 0 failures; all eleven die at 1 failure each; `disj2` and `wipocc` kills unchanged.

**The one real cost:** it needs `scsi_transfer_alloc()` inside an altctl row, because
`altctl_free()` frees `atapi_st` and a stack struct will not do. That is the new-oracle
boundary the round-scope rule names, and it is why `#483` deferred it correctly.

#### AND THE HONEST BOUND, because this class has no natural end

A guard can be added on ANY field in `struct wdc_data`, and a row can only see it by varying
that field. There are roughly forty. **Varying all of them is the unbounded mutant-hunt the
stopping rule exists to refuse.**

> **THE PRINCIPLED SCOPE: vary the fields a REAL DRIVER SETS during ordinary operation.**
> `lba`, `drive`, `head`, `seccnt`, `cyl_lo/hi`, `sector` are all written by ordinary
> taskfile register writes before any command -- so a fixture in which they are non-zero is
> not a synthetic state, **it is the normal one.** Today every altctl row runs in a state no
> real driver is ever in.
>
> *That reframing is a better warrant than either seat's ranking, because it is a defect in
> the harness independent of whether anyone would write any particular guard.*

### `wdcaltwidth` -- the control register's ACCESS WIDTH is unpinned

Secondary, lower confidence, from the opus seat: `idata = data[0]` -> `data[len - 1]` in the
altstatus handler escapes all 103 rows. Every row uses `len == 1`, and the region is
registered TWO BYTES WIDE. Whether a guest can issue a 16-bit control write depends on the
bus, so this is filed rather than fixed -- and it is adjacent to `wdcaltdecode`, which
already records that the handler consults neither `len` nor `relative_addr`.


## 2026-08-27 -- `#484` pass 1: a committed detector row that cannot reach its target

### `wdcfloodstale` -- `overrun x2` was silently invalidated by `#479`

`regress/wdc_flood_probe.py` row **`overrun x2`** drives 1026 undrained IDENTIFY commands,
states in its own comment that they *"lap the ring TWICE"*, and asserts the latched
`wdc inbuf overrun` message appears **exactly once**. Its header records that the row closed
an **L2 floor breach**: without it the fix had six fixed sites and the detector saw five.

*** THE STIMULUS CAN NO LONGER REACH THE TARGET. ***

`#479` made `wdc_command()` call `wdc_new_command_reset()` **unconditionally**, and that
helper sets `inbuf_head = inbuf_tail = 0`. IDENTIFY is dispatched *after* that reset and
stages `sizeof(identify_struct)` = 512 bytes. So occupancy after any command is at most 512,
and 1026 commands cannot lap a 262656-byte ring. The message can never fire, so the row must
read **0, want 1**.

Found by the grok seat on `#484`'s pass 1 and **confirmed by reading both functions** before
filing. **NOT RUN** -- the probe needs a built binary and a rig. Filed at BELIEVED, as a
reading; the measurement is owed. *Two independent readings are not a run and are not
recorded as one.*

> **THE CLASS IS ONE THIS CARRIER ALREADY NAMES, REACHED FROM THE MIRROR SIDE.** The standing
> rule is *an ABSENCE record must name its warrant, and any edit touching that warrant re-runs
> the death measurement*. This is a **PRESENCE** row whose warrant -- "1026 undrained
> IDENTIFYs lap the ring" -- was falsified by an edit in a **different function**, and nothing
> re-ran anything. **The obligation is symmetric and the carrier states only half of it.**

Consequence for the round in flight: `#484` fixes the very producer this row defends, and it
must **not** read a green `overrun x2` as evidence its fix is sound. **A row that cannot
reach its target is not a row that passes.**

REMEDY, one line: re-aim the stimulus at the only surviving wrap route -- the guest data-port
WRITE arm, which takes no `wdc_command()` and therefore no reset. `#473` already performed
exactly this re-aiming once on this file's sibling row, recording *"a detector aimed at a
primitive cannot verify a fix made in its caller: right defect, wrong instrument."* Here it
is the reverse -- right instrument, a stimulus that no longer arrives.
