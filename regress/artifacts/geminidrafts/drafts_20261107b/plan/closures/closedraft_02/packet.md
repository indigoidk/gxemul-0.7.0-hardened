# Reading task: closedraft_02 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE02-8375` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `strad` -- state `held`, severity `-`; PROPOSED: **DROP**

**title:** strad  The budget straddle cannot see three mutant shapes (named, not implied)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** The assessor explicitly ruled to drop strad as currently filed.

### ROW `fbvolatile` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** fbvolatile  Two footbridge counters cross the SIGALRM boundary as plain `int` while the identically-used counter in dev_mc146818.c is `volatile int`

**state_note (head):** *** EVIDENCE 2026-08-27: TRUE and LATENT -- and the answer contains a separate finding about an EXISTING DETECTOR BEING VACUOUS, which is worth more than the row. ***

**True, and VERIFIED HERE by opening the file:** `:73` is `int pending_timer_interrupts[N_FOOTBRIDGE_TIMERS];` and `:76` is `int pending_bound[N_FOOTBRIDGE_TIMERS];` -- both plain `int`, no `volatile` anywhere in `dev_footbridge.c`. `dev_footbridge.c` declares `pending_timer_interrupts[4]` (`:73`) and `pending_bound[4]` (`:76`) as plain `int`, and both are used from the SIGALRM callback `footbridge_pending` (`:114-120`), which `timer.c:284` invokes from `timer_tick`. The exact analog elsewhere in the tree IS painted: `dev_mc146818.c:80` is `volatile int pending_timer_interrupts`.

**LATENT, and the seat was careful about why:** the access path is live (NetBSD/cats uses it), but **missing `volatile` is not what that path currently fails on** -- no miscompile is demonstrated. A caveat it raised rather than hid: `pending_bound` is a THRESHOLD the handler READS, not a pending-count, so mc146818 has no twin of it and the analogy is partial.

**And a sharp negative point: `volatile` would NOT make the CLEAR `--` versus handler `++` atomic.** That is a different, still-latent read-modify-write, and it is NOT this row. Worth keeping separate so a `volatile` paint is not mistaken for fixing it.

*** I NEARLY FILED A DUPLI [... 1723 more characters not shown]

**hold_question:** OWNER DECIDED 2026-09-13 (default adopted by owner leave, reversible): ONE tree-wide convention for fb-device shared state (the stricter of the two existing devices'), applied when either device is next edited -- not a sweep round of its own.

**the triage pass's reason:** 'assessed, not covered' property requires load-sensitive test, explicitly recorded with no filing needed.

### ROW `m8invpred` -- state `held`, severity `-`; PROPOSED: **DROP**

**title:** m8invpred  A reading seat predicted the state-dependent mutant class in pass 1, and it went unread for a day

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** unanimous drop for a row whose only residual value is a lesson already recorded in the carrier.

### ROW `dfreq` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** dfreq  A one-shot deadline is modelled as a repeating rate (design item)

**state_note (head):** [2026-10-22] WIDENED by the external-fixes research (regress/artifacts/research_20261022/TRIAGE.md T93; regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): two residuals no row carried -- the host-timer Compare rate ignores that Count runs at CPU/2 (cpu_mips_coproc.c:808-809 at de8c7547), and compare_interrupts_pending is an uncapped int (:422; include/cpu_mips.h:277) that re-asserts IP7 back to back while it stays above 0 (cpu_dyntrans.c:433-436) -- the uncapped-counter shape #442 bounded in dev_footbridge.c only.  Ports: jroark/GXemul 2fa3853 (rate halved, backlog capped at 1), 4729fb6, dabf5ce (report rows A3-26, A3-27; https://github.com/jroark/GXemul/commit/2fa38531d41426151943758faa46a2d3297b8c3f).  The wrap-reprogramming half stays `n1`'s.  witness: none -- research finding, not yet reproduced here.  ||  

*** 2026-09-13 CODEX RESEARCH (read-only, gpt-6-astra max): DOCUMENT-ONLY -- see regress/artifacts/codex_research_20260913/dfreq.answer.md.  Premises it corrected are in the entry; the row stays HELD pending the named next step and the batched flagship close pass. ***

**hold_question:** A one-shot deadline is modelled as a repeating rate. The hold says 'a design change, per the stopping rule'. QUESTION: is there a GUEST-OBSERVABLE consequence that makes this a defect rather than a modelling difference? This matters because the carrier records that dfreq's earlier 'no witness of either kind' claim was MEASURED FALSE -- a witness was built in one session. So: what does that witness actually show, and does it show a wrong VALUE reaching the guest or only a different internal repre [... 99 more characters not shown]

**the triage pass's reason:** stopping rule invoked because the witness does not reproduce the defect and a guest witness is outstanding.

### ROW `killartifacts` -- state `open`, severity `-`; PROPOSED: **DROP**

**title:** killartifacts  kill-table drivers preserve no per-row artifact, so a retrospective audit of a PAST round's detector is already impossible -- measured by trying one and failing

**state_note (head):** MAIN-LOOP, 2026-08-24. The `lethalonly` class (see that row) is checked by one question -- does a row have a kill that leaves the host ALIVE? -- and it is answerable from any kill table already on disk, at zero cost. *** I TRIED TO RUN IT ON #461 AND COULD NOT. *** Its only lethal mutant is `m_dmarevert` (floor (b), the verbatim `exit(1)` reinstatement, recorded at 22/31), and NO PRESERVED FILE CARRIES ITS PER-ROW RESULT: 0 candidate lines across every `.out` in both scratchpads. The score survives only as prose in the round block. So #461's detector cannot be audited for this class at all, and that is not a hypothetical cost -- it is a retrospective audit that was attempted today and blocked. *** THE SAME GAP IS LIVE IN #462's DRIVER: *** `table462.sh` writes `probe_<M>.raw` and archives nothing, so the third table has been overwriting the second's logs as it runs, and table 2's `base` log was already lost before it was noticed. Fourteen survivors were preserved by hand into `table2_57rows/` and every score re-verified against the written record. *THE ASYMMETRY THAT MATTERS: losing a BASE log is worse than losing a mutant log, because base is the denominator for every score in the table.* This is the immutable-artifact rule (carrier, 2026-08-24) meeting its own retrospective case: that rule was written after a citation decayed forward; this is the same defect found by reaching [... 1708 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** explicitly folded into killdriverunTracked

### ROW `m88kexit` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** m88kexit  memory_m88k.c still calls exit(1) on the CMMU_PFSR_SUCCESS internal-error branch -- the host-kill shape #433 removed from this same device

**state_note (head):** *** EVIDENCE 2026-08-27: the CALLS EXIST (claim true) but BOTH SITES ARE UNREACHABLE. This is dormant defensive code, NOT a live host kill -- a real severity downgrade, and the point of establishing it is to stop a round being opened on 'a surviving exit(1)'. ***

`src/cpus/memory_m88k.c` contains exactly **two** `exit(1)` calls, both inside the `switch (pfsr_status)` that runs after the `exception:` label:
  * `:390-394` -- `case CMMU_PFSR_SUCCESS:`, whose own diagnostic reads *"HUH? CMMU_PFSR_SUCCESS:, but exception? TODO"*;
  * `:408-413` -- `default:`, *"Internal error in memory_m88k?"*.

**Both are internal-invariant assertions, and the invariant holds structurally.** `pfsr_status` is initialised to `CMMU_PFSR_SUCCESS` at `:118`, which is what makes the first case look live. But the exception block is reached ONLY through the `exception:` label at `:373`, and:

  * there are **seven** `goto exception` sites -- `:173`, `:213`, `:267`, `:275`, `:300`, `:309`, `:341` -- and **each is preceded, ONE LINE ABOVE, by a fault assignment** at `:172`, `:212`, `:266`, `:274`, `:299`, `:308`, `:340`. Seven gotos, seven assignments, gap of 1 in every case.
  * **control cannot FALL THROUGH into the label**: `:370` is `return (accumulated_flags & PG_RO)? 1 : 2;`, immediately above it.

So `pfsr_status` is never `CMMU_PFSR_SUCCESS` at `:388`, and the `default:` arm is unreachable for the  [... 1184 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** Not a live defect; sites are unreachable without code change.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_02: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE02: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
