# Reading task: nextstep_04 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT04-27a8` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `cxseatcheck` -- state `open`, severity `med`

**title:** tools/cxlaunch.sh: a codex seat check that could report a REFUSED seat as a clean run, and a wall-grep over stderr that matched the project's own ledger text

**state_note:** [2026-09-19 06:2x] #544 IN WORK (e8a2bc): the fix is drafted with 20 launcher controls and a 38-row / 21-variant tally self-test; pass 2 in flight on panel_20260919_060945.  Built 2026-09-07 after the `lcaconfwidth` census was REFUSED by codex's content filter and my
launcher reported it as a completed run.  **Three defects, all mine, all found within an hour of
each other, and all of one family: a check that answers the same whether or not the thing it tests
is true.**

1. **The refusal check read the wrong stream.**  A content-filter refusal writes NOTHING to stdout
   and puts `ERROR: This content was flagged for possible cybersecurity risk.` on STDERR.  The check
   grepped stdout and printed `refusal hits: 0` on a refusal that had already destroyed 108,432
   tokens of completed work.
2. **The script exited 0 while holding `rc=1`.**  It captured codex's status, printed it, and ended
   on a successful command, so the harness reported the task COMPLETED.  Failure laundered into a
   clean completion -- the fourth instance of that class recorded here.
3. **The FIX introduced a third defect, measured on its first real run.**  Grepping stderr freely
   for wall text reported `wall: 3` on a HEALTHY seat, because **codex streams the source it reads
   into stderr** -- and all three hits were this project's own ledger prose about seat walls, one of
   them the line *"whose quotation of the pattern MATCHES"*.  That is the carrier's
   quoting-a-machine-read-marker rule, landing on a tool written by someone who had just read it.

> **THE DISCRIMINATOR: codex's OWN diagnostics are `ERROR:` at line start; everything else on stderr
> is echoed content.**  Anchor stderr tests on `^ERROR:`; grep stdout freely.  Exit 7 refusal, 8
> wall, 6 empty-with-neither, else `rc`.

**Controlled in four states**, and (b) is the one that matters: a stderr line containing *usage
limit* inside echoed source must NOT trip the wall check.

    a  ERROR: flagged...           -> REFUSED   (want REFUSED)
    b  echoed source w/ 'usage limit', good stdout -> answered  (want answered)
    c  ERROR: usage limit          -> WALLED    (want WALLED)
    d  ordinary reasoning, good stdout          -> answered  (want answered)

*** THE CLAIM I ORIGINALLY CLOSED THIS ROW WITH WAS FALSE, AND I MADE IT IN A ROW ABOUT CHECKS THAT
DO NOT CHECK.  Corrected within the hour, by reading `panel.sh` instead of assuming. ***

I wrote that *"`panel.sh` fires the same seat with its own check and has NOT been given this
discriminator."*  **It has had one longer than mine, and a better one.**  Its `check()` anchors error
sentinels to the **first 400 bytes** and its wall test to the **last 400 bytes**, with the reason in
its own comment: *"a review that merely quotes 'was retired' or 'usage:' gets mis-flagged (it did, on
the first live run)."*

**So the tree already held the lesson and I re-learned it by breaking it.**  The two discriminators
differ and both are sound:

    panel.sh    POSITION -- he

**hold_question:** (none)

### ROW `gdrommappedvacuous` -- state `open`, severity `med`

**title:** four `gdrom map' controls convert any 0x... print to "mapped", so the memory fallback's zero-filled read satisfies them

**state_note:** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

### ROW `negrowclass` -- state `open`, severity `med`

**title:** an inequality row scores every NON-OBSERVATION green -- five ungated instances repaired and measured, two GATED ones still open

**state_note:** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

### ROW `printedvariants` -- state `open`, severity `low`

**title:** 20 copies of printed() with FOUR different contracts, and two of them document their normalisation as matching a helper that does not mask

**state_note:** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

### ROW `probeneedleterm` -- state `open`, severity `med`

**title:** unterminated needles accept longer numbers -- pcc2_default, sh4_val V22, m88k_exc captures

**state_note:** Filed 2026-09-07.  Full record in OUTSTANDING_BUGS.md under the same id.

*** THIS ROW EXISTS BECAUSE THE LEDGER<->BUGFILE SYNC IS ONE-DIRECTIONAL AND ITS WARRANT HAS DECAYED -- see [[bugfilereverse]].  It was filed into OUTSTANDING_BUGS and given no ledger row, which is precisely the failure check_bugfile_sync.py was written to stop, in the direction it does not check. ***

**hold_question:** (none)

### ROW `ubsanshiftlane` -- state `open`, severity `med`

**title:** a UBSAN differential would pin the shift-UB class that a guest-value probe provably cannot see

**state_note:** Filed 2026-09-07 from `#510`'s pass 2.  Full record in OUTSTANDING_BUGS.md under the same id.

grok showed two one-line regressions that re-open real UB and score FULL MARKS on a 12-row guest-value probe, and the reason is STRUCTURAL: both are DEFINEDNESS repairs, and definedness has no guest-visible value on a non-trapping host.  `1 << 31' and `1U << 31' give the same mask after the `- 1'; with a correct 32-bit mask `x |= ~mask' is `x |= 0'.

**build-asan already carries `-fsanitize=address,undefined`** -- established AFTER I wrote "unchecked" about it in the probe header, one grep from the answer.  So the class IS pinnable, as a DIFFERENTIAL: fixed source produces no shift diagnostic, the `1U'->`1' mutant produces one.

**Not bolted onto #510**: a second binary and a STDERR oracle is a new measurement lane, and #510's pass 2 had already run.  A lane added after a pass is a lane nobody reviewed.

Covers the same species at [[lcashiftub]], [[sgirebufshiftub]], m88k_rot:513, cpu_mips_instr.c:1757 [2026-11-02, records: not the same species -- `rs` is `uint32_t` (:1756), so nothing there shifts into a signed sign bit; its undefined behaviour is the shift count `32-lsb-size` going negative when lsb + size > 32 (C99 6.5.7p3), which a value oracle cannot see either] and the two is_userpage sites -- EIGHT sites across three CPUs, none directly visible to a value oracle.

*** THE FILED QUESTION IS ANSWERED, AND THE ANSWER COMES WITH A FREE VEHICLE: THE PROBE SHIPPED FOR
[[lcaconfbus1kill]] ALREADY EVALUATES THIS EXPRESSION ON EVERY RUN. ***

This row asks *"whether a UBSan sweep already flags it, and if not, why not."*  Both halves settled
by reading, 2026-09-07.

**UBSAN IS PRESENT.**  `build-asan/Makefile:9` carries
`-fsanitize=address,undefined -fno-omit-frame-pointer -g`.

**BUT THE SWEEP CANNOT REACH THIS SITE, AND THE REASON IS STRUCTURAL RATHER THAN AN OVERSIGHT.**
`gate_asan_sweep.sh` runs, per machine type and subtype:

    timeout 25 stdbuf -o0 -e0 "$bin" -V -E "$t" -e "$s" "$DUMMY" </dev/null

That is a **CONSTRUCTION** sweep -- it builds each machine and lets it start.  The shift lives in
`DEVICE_ACCESS(lca_pci_conf)`'s device-scan loop, which runs only when a guest performs a PCI
CONFIG-SPACE ACCESS.  **Constructing `alphabook1` never executes that loop**, so no amount of
sweeping flags it.  *This is the witness-ladder distinction one level down: rung 2 (construction)
cannot reach an access-path defect, which is exactly what the ladder says about registration
proving presence and not reachability.*

*** AND THE VEHICLE ALREADY EXISTS, WHICH IS THE PART WORTH ACTING ON. ***
`regress/lca_confbus_probe.py` (shipped 2026-09-07 as the witness for [[lcaconfbus1kill]]) drives a
guest `ldq` into the PCI config window with `ioc_conf == 0`.  That takes the `bus == 0` branch:

    for (dev=0; dev<21; dev++)
            if (tag & (0x800 << dev))
                    break;

Its control read uses `relative_addr == 0`, so `tag = (relative_addr >> 5) & ~0xf

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_04: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT04: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
