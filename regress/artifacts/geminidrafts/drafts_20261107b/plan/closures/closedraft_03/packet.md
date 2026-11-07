# Reading task: closedraft_03 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE03-d481` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `stalecopies` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** stalecopies  Three unpatched pre-#337 copies of dev_wdc.c live under the project root, and a file-reading seat cited one of them as "root"

**state_note (head):** *** EVIDENCE 2026-08-27: CONFIRMED, exactly three, and each one is EXPECTED to be stale. The hazard is real but it is a READING hazard, not a BUILD hazard. ***

**Census (deriver: `find . -name 'dev_wdc.c'`, then `grep -c warned_badlen` per copy -- `warned_badlen` is `#337`'s latch, so its presence dates the file):**

```
  CURRENT (1191 lines, warned_badlen x6)
    GXEMUL-SEC/src/devices/dev_wdc.c      the fork
    est/src/devices/dev_wdc.c             the non-git twin
    build/src/devices/dev_wdc.c           in-place build tree
    build-asan/src/devices/dev_wdc.c      in-place build tree

  STALE pre-#337 (966 lines, warned_badlen x0)
    ./src/devices/dev_wdc.c                                    pristine 2021 upstream
    _archive/audit-results-20260625_203645/builds/est-asanonly/...   June audit build
    _archive/audit-results-20260625_203645/builds/orig-asan/...      June audit build
```

**Three stale copies -- the row's count is exactly right.** And all four live trees carry the fix, so **no build tree is stale**: the twin-tree propagation held.

*** THE HAZARD IS READING, NOT BUILDING, and one of the three is ALREADY a documented carrier hazard: *** `./src/` is the pristine April-2021 upstream that the carrier warns file-reading seats about by name -- a seat pointed at the project root reads it and is *confidently, detailedly wrong*. **The NEW information in this row [... 524 more characters not shown]

**hold_question:** OWNER DECIDED 2026-09-13: MOVE THEM OUT, nothing deleted.  DONE the same day: the project-root src/ and the two _archive/audit-results-20260625_203645/builds/{est-asanonly,orig-asan} trees were moved to C:\DocumentNoSnc\CC\GXEMUL_upstream_2021\ (README.txt there; pointer notes left at both old places).  Checked first: no gate or script read them (gate_ab builds its pristine tree from `git archive 39748e3`; every regress/ `../src` is GXEMUL-SEC/src).  The deriver now finds only the four fork copi [... 314 more characters not shown]

**the triage pass's reason:** documentation gap, files were already moved out

### ROW `pcicmergeA` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** pcicmergeA  The PCICONF0 latch-merge reproduction has no detector row, and could not have had one until the third fault class landed

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** No row was created because it would have cemented the defect, which is documented.

### ROW `queuesubstr` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** queuesubstr  check_fable_queue matched ids by SUBSTRING, so the gate was green over exactly the state it exists to redden

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** The substring matching defect was found and fixed immediately.

### ROW `sh4pcicvoid` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** sh4pcicvoid  One line of #443's fix is genuinely void: `odata = 0` in the unimplemented-CPU PCICONF0 arm cannot be distinguished from its absence

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** recorded as a proof gap, not a defect in the fix

### ROW `stdbufasan` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** stdbufasan  `stdbuf` silently breaks an ASan binary, and this ASan ignores bogus flags so the usual accept/reject discriminator cannot detect it

**state_note (head):** *** EVIDENCE 2026-08-27: TRUE, HARNESS-ONLY, and ALREADY DOCUMENTED AND FIXED IN-TREE -- in THREE places in the same gate. Recommend CLOSE. ***

**The mechanism:** `stdbuf` works by `LD_PRELOAD`ing `libstdbuf.so`, which then precedes the ASan runtime in the initial library list; ASan rejects that startup order and aborts with *'ASan runtime does not come first in initial library list'*. The host process dies at launch, **before the guest CPU powers on**, so there is no guest observable at all.

**All three already in `regress/gate_asan_sweep.sh`, verified by reading:**
  * `:104-105` -- *"verify_asan_link_order=0 is REQUIRED, not cosmetic. `stdbuf` works by LD_PRELOADing libstdbuf.so, which then precedes the ASan runtime..."*
  * `:117` -- the remedy: `export ASAN_OPTIONS=detect_leaks=0:abort_on_error=0:print_summary=1:verify_asan_link_order=0`
  * `:115` -- **the second hazard, recorded verbatim**: *"ASan silently ignores `no_such_asan_flag_xyz=0` and runs normally."*

*** THAT SECOND ONE IS THE SHARPER FINDING AND IT IS ALREADY WRITTEN DOWN: because this ASan silently ignores bogus options, ANY check that validates `ASAN_OPTIONS` by asking whether ASan ACCEPTS them is vacuous. *** It answers identically for a valid and an invalid flag -- the check-that-cannot-fail shape, in the environment rather than in a script. The gate knew and said so.

*Ninth row today describing work a [... 123 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** already documented and fixed in-tree in three places

### ROW `hpcshcpu` -- state `open`, severity `-`; PROPOSED: **DROP**

**title:** hpcshcpu  the repo contradicts itself about whether hpcsh is an SH-3 or an SH-4 machine, and neither claim is settleable in this tree

**state_note (head):** *** DISPOSITION 2026-08-24 (fable5 queue ranking): DROP FROM THE ACTIONABLE QUEUE, KEEP AS A RECORD. *** Two seats independently refuse to settle it and the row's own entry says neither claim is settleable in this tree. **A defect that cannot be reproduced cannot be test-first'd, and a round that cannot be test-first'd is not a round** -- it is a document, which the witness ladder already says plainly ('no witness at rung 2-4 -> document instead, stop'). Converted to: *assessed, cannot settle without an external SH3/SH4 identity source*. RE-OPEN ONLY if such documentation is obtained -- and that is not hypothetical, because obtaining the SH7750 manual on 2026-08-22 settled an SH question in the same session it was raised and refuted a finding this project was about to file.

**hold_question:** (none)

**the triage pass's reason:** cannot settle without an external SH3/SH4 identity source

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_03: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE03: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
