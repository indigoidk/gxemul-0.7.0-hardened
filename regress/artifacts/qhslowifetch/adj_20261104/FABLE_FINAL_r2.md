# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 18:20:09Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpqhsf2/fe72cc7c-713d-4ff9-87f1-5507ae79bf9d.jsonl`
* session: `https://claude.ai/code/session_015fEQzGH2n2cccbGCS5esdA`   trigger: `trig_01T8zD28AdLMpwbZhb4v18dr`   packet: `_scratchpad/cloud_fable_20261103/prompt_qhslowifetch_FINAL_COMPACT.md`
* the answer's message: timestamp 2026-11-04T18:04:00.532Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDFINAL_QHS_20261104`: present; 25304 characters; PART markers N = 36, present 36, MISSING none; `END OF PARTS`: YES
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINAL qhslowifetch: 7 RULINGS 6 CHANGES 5 ROWS VERDICT:GO-WITH-CHANGES

---
PART 1/36
CLOUDFINAL_QHS_20261104
model: claude-fable-5-1 (configured id; the serving model may differ)
EVIDENCE BASIS: the compact packet only; no repository. CHECKED-IN-PACKET: the HEAD excerpts (IFETCH, XLATE, MEMRW, BAD), the draft text, the rung-3 witness (Facts 1-2), the A/B measurement table, grok's consolidation. PROVISIONAL points: ppc_exception's handling of a vector it does not list and whether it re-points next_ic (cpu_ppc.c:318-344 not quoted); PPC_MSR_ME and quick_pc_to_pointers in the PPC headers; the vga_gfx producer (reasoned, unmeasured).
VERDICT: GO-WITH-CHANGES. B's park is the fix for the measured -T halt. The draft's comment and bare return are wrong as written. A decline with running still 1 gets a machine check, provisional on the points above.

PART 2/36
EVIDENCE BASIS, detail. Omitted and not relied on: the full pass-1 briefs and the seat answers; every seat position below is taken from grok's consolidation and the verdict table. What each source settles: Fact 1 (measured) settles that the ordinary ISI route never enters the failure arm. Fact 2 and the BASE row settle the producer: -T plus a real-mode fetch past RAM and the 256 KB slack, with memory.c:645-651 clearing running and raising nothing. The A row settles what a bare return does (a skip across 8,272 slots, not a live-lock). The B row settles that the park finishes the halt on the fetch pc with SRR0 untouched. Nothing in the packet measures a failed fetch with running still 1, read-ahead entering the arm, a 64-bit CPU or a 603; every ruling on those is REASONED or UNSETTLED and marked so.

PART 3/36
THE RULING, overview. Three producers, three dispositions:
P1 the measured -T halt (running already cleared by memory.c): menu 2 DECLINE silently, as a park on the fetch pc (next_ic = &nothing_call; return). memory.c already announced the address; the core adds nothing and raises nothing.
P2 an ISI or 603 miss already delivered by the translation inside memory_rw: menu 5 FAULT, already delivered; the arm returns after refreshing next_ic. REASONED unreachable on every 32-bit session; kept as a guard.
P3 a physical decline with running still 1 (a device failing an instruction-width read): menu 7 IMPLEMENT the architectural exception: a machine check, vector 0x200, when MSR[ME] is set; a checkstop (CPU stop, process alive) when it is clear. PROVISIONAL.
Plus: read-ahead returns silently before any of the three (the bad: rule).

PART 4/36
RULING 1 (P1, the measured -T halt). Disposition: park. Warrant, CHECKED-IN-PACKET: memory.c:645-651 clears every CPU's running and returns without a PowerPC exception, so by the time the arm runs the halt is already taken and announced ('memory READ: from non-existant paddr=0x02040000'). The arm's only job is to leave the CPU parked where the halt happened. B measured that: PC 0x02040000, SRR0 0x11111111 untouched, one non-existant line under continue, prompt reached, exit 0, and a second step or continue changes nothing. A measured the alternative: the bare return leaves next_ic on the slot after the failed one (dispatch increments before calling the translator), so step lands on 0x02040004 and continue walks 8,272 distinct addresses before the run loop sees running clear.

PART 5/36
RULING 1, continued. No PowerPC exception is raised on P1, and none may be invented. -T is a debugger option of the binary ('halt on a non-existent memory access'); the halt is the user's request, not an architectural event, and the guest must see nothing: SRR0/SRR1 untouched, MSR untouched, pc on the fetch address. The probe pins this with the 0x11111111 sentinel; an edit that raised an ISI or a machine check here would move SRR0 and pc and fail rows 1 and 2. This also disposes of Gemini's change 5 for P1. REASONED: the same holds without -T, where memory.c returns zeros and the CPU stops on the zero word at the bad: label; that route never enters the arm (memory_rw succeeds), so the fix does not touch it.

PART 6/36
RULING 2 (P2, an ISI or 603 miss already delivered). REASONED unreachable: the dyntrans PC lookup (cpu_dyntrans.c:670-680, Fact 1) translates the fetch address with FLAG_INSTR under the same MSR, BATs and page tables before the translator runs; memory_rw's second translation of the same address cannot fail where the first succeeded, and nothing between the two changes CPU state. Grok's objection to change 6 is accepted as a fact. Fact 1 measured the consequence: on the ISI route all three binaries are identical and the arm is never entered. The draft's comment, which names this as the producer and borrows the MIPS #234 shape, is false on every measured session and must go (change 1, all four seats).

PART 7/36
RULING 2, continued. The guard stays, for one reason: ruling 3 makes the arm raise an exception when running is still 1, and ppc_exception (cpu_ppc.c:318-344, per the packet) does not clear running, so an exception delivered inside memory_rw would otherwise fall into the running-1 arm and be doubled, with SRR0 overwritten. The discriminator is cheap and true: ppc_exception moves cpu->pc to the vector (Fact 1 shows execution resuming at 0x400), while memory.c:645-651 and a device decline leave pc equal to addr (line 4089 set it). So: if pc differs from addr, refresh next_ic and return. The refresh is deliberate: whether ppc_exception itself re-points next_ic is UNSETTLED (cpu_ppc.c:318-344 is not quoted); refreshing is idempotent and makes the arm correct either way. The comment says the branch is reached on no measured session.

PART 8/36
RULING 3 (P3, a physical decline with running still 1). The only reasoned producer is dev_vga.c:617-618 ('relative_addr + len >= GFX_ADDR_WINDOW' returns 0) on prep ibm6050 with -X, fetching the window's last word 0xc00b7ffc in real mode; memory_rw.c:595-603 has no PPC exception arm, so today the process ends. Not measured. What the arm must not do is settled by A: a bare return executes the next slot, so the guest silently skips an instruction it could not fetch. GLM's 'otherwise skip' is rejected on that measurement. Astra's 'no skip, no zero-fill, no invented ISI' is accepted; its open question is closed by the fix-design rule for CPU cores: raise the exception the manual prescribes.

PART 9/36
RULING 3, warrant. REASONED from the PowerPC OEA and the 750 user's manual: an instruction fetch the bus terminates with an error (TEA) is a machine check, vector 0x00200, taken when MSR[ME] is set; with MSR[ME] clear the processor checkstops. That maps onto the emulator: ME set, ppc_exception(cpu, PPC_EXCEPTION_MC) with SRR0 = the fetch address (cpu->pc = addr at line 4089; ppc_exception saves pc into SRR0 per the draft's reading); ME clear, a message naming the address and a CPU stop. That stop is a CPU-STOP the architecture itself prescribes, not a host kill. An ISI is wrong here: ISI is a translation or protection fault, and this access translated. PROVISIONAL on: PPC_EXCEPTION_MC being new (cpu_ppc.h has no machine-check constant), PPC_MSR_ME existing, ppc_exception accepting vector 0x2.

PART 10/36
RULING 4 (read-ahead). If cpu->translation_readahead is set, return before any other branch. Warrant: the bad: label (CHECKED-IN-PACKET) already returns silently during read-ahead because the guest has not executed that address; a failed fetch is the same situation. Without the guard, ruling 3 would deliver a machine check for an instruction the guest never reached, and ruling 1 would park a running CPU. B carried this guard and measured 17/17, so it is harmless on the measured routes; it is unscored there (read-ahead stays inside the ic page and the slack pages read zeros). Astra's change 8 accepted.
RULING 5 (goto bad, GLM's changes 3 and 4): rejected. bad: prints 'UNIMPLEMENTED instruction' and disassembles ib, which memory_rw zero-filled (#244): a false message about a fetch halt. Change 10's assertion goes into rows 1-3.

PART 11/36
RULING 6 (the draft comment). Replaced in full. Every sentence of it is false or unsupported on the measured route: no ISI was raised, SRR0 was not saved, pc did not move, pc_to_pointers did not run, 'let the CPU take the exception' names an exception that does not exist, the MIPS #234 and ARM analogies do not hold (cpu_arm_instr.c:4089-4091 is fatal then return, per grok's table), and 'a re-fetch of the same address repeats the exception' describes a live-lock that A shows does not happen. Grok's v3 consensus comment is true but says nothing about what the arm does; the per-branch comments in parts 13-16 replace it.
RULING 7 (the slot). The arm returns before the success tail, so ic->f stays TO_BE_TRANSLATED and the next attempt re-runs the arm. CHECKED: B's second step changes nothing. Row 3 pins it.

PART 12/36
THE FIX. Two files. (1) src/cpus/cpu_ppc.h: add, beside PPC_EXCEPTION_ISI,
```
#define PPC_EXCEPTION_MC   0x2   /*  Machine check, vector 0x200  */
```
(ppc_exception multiplies by 0x100, as the 603 vectors 0x10-0x12 and ISI 0x4 show in XLATE 307-323; the call sites are CHECKED-IN-PACKET, the multiplier itself REASONED.)
(2) src/cpus/cpu_ppc_instr.c, X(to_be_translated): lines 4117-4120 (the fatal, the exit(1) and the commented goto) are replaced by the block in parts 13-16. Lines 4115-4116 (the memory_rw call) and 4121-4122 stay. Indentation is the file's tabs; shown here with spaces. #NNN is this bug's number.

PART 13/36
```
        /*  #NNN: the instruction fetch failed.  This
            arm was fatal() + exit(1).  Nothing below
            marks the slot translated: it stays
            TO_BE_TRANSLATED, and a later fetch of this
            address runs this arm again.  */

        /*  Translation read-ahead: the guest has not
            reached this address.  Return with no side
            effect, as the bad: label does.  */
        if (cpu->translation_readahead)
            return;
```

PART 14/36
```
        /*  memory_rw's own translation raised a PowerPC
            exception (an ISI, or a 603 miss): pc is at
            the vector.  Reached on no measured session,
            because the dyntrans pc lookup translates
            this address under the same MSR before the
            fetch.  Kept so that an exception, once
            delivered, is never doubled by the arms
            below.  next_ic must follow pc; refresh it
            here rather than rely on ppc_exception
            having done so.  */
        if (cpu->pc != addr) {
            quick_pc_to_pointers(cpu);
            return;
        }
```

PART 15/36
```
        /*  Measured route: -T, real mode, a physical
            address past RAM and its slack.  memory.c
            has printed the address and cleared running.
            No PowerPC exception exists for this, and
            SRR0/SRR1 are untouched.  Park on this pc so
            the halt lands here.  */
        if (!cpu->running) {
            cpu->cd.ppc.next_ic = &nothing_call;
            return;
        }
```

PART 16/36
```
        /*  The physical access was declined with the
            CPU still running (a device failing an
            instruction-width read; no measured
            producer).  The OEA prescribes a machine
            check for a fetch the bus terminates with
            an error: vector 0x200 when MSR[ME] is set,
            checkstop otherwise.  */
        if (cpu->cd.ppc.msr & PPC_MSR_ME) {
            ppc_exception(cpu, PPC_EXCEPTION_MC);
            return;
        }
        fatal("[ ppc: instruction fetch from 0x%" PRIx64
            " declined with MSR[ME]=0: checkstop ]\n",
            (uint64_t) addr);
        cpu->running = 0;
        cpu->cd.ppc.next_ic = &nothing_call;
        return;
```

PART 17/36
FIX, notes. Every comment above is true as written on the packet's evidence, with these dependencies to confirm at build time: 'as the bad: label does' (CHECKED, BAD block); 'memory.c has printed the address and cleared running' (CHECKED, Fact 2); 'reached on no measured session' (CHECKED, Fact 1); 'the OEA prescribes a machine check' (REASONED, manual). Names: nothing_call compiles in this file (B was built with it: CHECKED). quick_pc_to_pointers is the dyntrans name the PPC branch instructions use (REASONED; a grep of cpu_ppc_instr.c settles it; the 32/64-bit pc_to_pointers pair is the substitute). PPC_MSR_ME is the MSR bit-12 name the header family uses (REASONED; grep). ppc_exception is already called from this file for sc and traps (REASONED). fatal() does not exit: HEAD needed the separate exit(1) (CHECKED).

PART 18/36
FIX, the fallback for ruling 3. If U1 or U2 (part 31) fails at build time, the machine-check branch is not shipped half-built. The arm then takes the checkstop branch for both MSR[ME] states, with the message changed to '[ ppc: instruction fetch from 0x... declined; no machine check modelled yet, see #MMM ]', and #MMM is FILED as the IMPLEMENT row for the machine check. That fallback is still a CPU-STOP with the process alive, strictly better than HEAD, measured-equivalent to B on rows 1-3, and its comment is true. Not acceptable in any version: a bare return (a skip), goto bad (a false message), or an ISI.

PART 19/36
CHANGES to the draft, the count the final line reports:
C1 replace the draft comment in full (ruling 6).
C2 add the read-ahead guard, first (ruling 4).
C3 add the pc-moved guard with a next_ic refresh (ruling 2).
C4 add the !running park with nothing_call (ruling 1; this is B).
C5 add the running-1 arm: machine check under MSR[ME], checkstop otherwise (ruling 3; provisional, with the part-18 fallback).
C6 add PPC_EXCEPTION_MC to cpu_ppc.h.
Not changed: the lookup at cpu_dyntrans.c:670-680, memory.c:645-651, memory_rw.c, the XLATE exits, dev_vga.c (each FILED where it is a defect, part 32).

PART 20/36
THE ROWS the fix owes. Wrong edits enumerated first; the bound is one row per wrong edit, and a row may catch several.
W1 the process still ends (an exit or abort left in, or reintroduced).
W2 a bare return: the declined slot is skipped (A).
W3 an exception invented on the -T route (ISI or machine check in the park branch).
W4 goto bad, or any message that misnames the halt as an unimplemented instruction.
W5 the arm falls through into the success tail and marks the slot translated.
W6 a silent skip when running is still 1.
W7 a wrong machine check: vector, SRR0, or MSR[ME] gating.
W8 the read-ahead guard missing. No row is deliverable for W8 (no producer reaches the arm from read-ahead on any in-tree machine); FILED, part 32.

PART 21/36
ROW 1 (-T, step). Session: -E pmppc, unmodified in-tree, 32 MB, -T, the probe's raw 'ori r0,r0,0' at 0x2000 (regress/ppc_ifetch_probe.py, md5 3826ecfb4816). Guest action: pc = 0x02040000, SRR0 = 0x11111111, step once. Want: the process alive at the debugger prompt, exit status 0; PC 0x02040000; SRR0 0x11111111; exactly 2 'non-existant paddr=0x02040000' lines (the step's disassembly read and the fetch, as BASE and B both show); 0 'read failed' lines; no 'UNIMPLEMENTED instruction'; no 'PPC Exception' line. Catches: W1 (no prompt, exit 1), W2 (PC 0x02040004), W3 (SRR0 or PC moved), W4 (the UNIMPLEMENTED line). Measured as B's step column.

PART 22/36
ROW 2 (-T, continue). Same session as row 1; guest action: continue instead of step. Want: prompt, exit 0; PC 0x02040000; SRR0 0x11111111; exactly 1 'non-existant' line; 0 'read failed'; no 'UNIMPLEMENTED instruction'; no 'PPC Exception'. Catches: W2 in its loud form (A printed 8,272 lines naming 0x02040000 to 0x0204813c), and any ordering edit that lets the dispatch loop pass the park (a line count above 1 is the signal). Measured as B's continue column.

PART 23/36
ROW 3 (-T, repeat after the halt). After row 1 or row 2: step again, then continue again. Want: PC still 0x02040000; SRR0 still 0x11111111; one more 'non-existant' line per attempt and nothing else; no 'read failed'. Catches: W5. An arm that reaches the success tail would have marked the slot translated with a zero-filled ib (#244), and the second attempt would execute that half-translated slot instead of re-running the arm: PC would move or an 'UNIMPLEMENTED' line would appear. The packet reports 'a second step/continue changes nothing' for B; this row keeps that true.

PART 24/36
ROW 4 (the ISI control). Session: -E pmppc as above, MSR[IR] set, pc = 0x20000000 (a reset-BAT gap), SRR0 = 0x11111111. Guest action: step; in a second session, continue. Want, under both: SRR0 0x20000000; PC 0x400; no 'read failed'; no 'non-existant'; transcript identical to HEAD's. Catches: an edit that widens the fix into the lookup at cpu_dyntrans.c:670-680 or routes the ISI through the arm, where the pc-moved guard would pass by design but a misplaced park or machine check would not. This is also the control that pins Fact 1; it was among the probe's 17 and all three binaries pass it.

PART 25/36
ROW 5 (a decline with running still 1; PROVISIONAL, blocked on an X11 build). Session: -E prep -e ibm6050 -X, real mode, MSR[ME] set, SRR0 = 0x11111111, pc = 0xc00b7ffc (the last word of the vga_gfx window; dev_vga.c:617-618 declines it). Guest action: step. Want: process alive; PC 0x200; SRR0 0xc00b7ffc; running still 1 (a following continue runs from 0x200); no 'read failed'; no 'non-existant'. Variant, MSR[ME] clear: the checkstop message naming 0xc00b7ffc, prompt, PC 0xc00b7ffc, SRR0 sentinel. Catches: W6 (PC 0xc00b8000, SRR0 sentinel, nothing printed) and W7 (another vector, SRR0 not the fetch address, or a machine check taken with ME clear). Caveat: fixing dev_vga's off-by-one (F1) removes this producer; the row then needs a synthetic declining device (part 32).

PART 26/36
ROWS, tally. Five rows against eight enumerated wrong edits; no wrong edit has more than one row; W8 has none and is filed. Rows 1-4 are measurable now on pmppc with the frozen probe (rows 1, 2 and 4 are its existing -T and ISI checks; row 3 is a two-line extension of the same session). Row 5 is owed but cannot be measured in the current harness. The final-line count is 5.

PART 27/36
DISAGREEMENTS SETTLED.
D1 the comment. All four seats: rewrite; the draft: 'ISI already raised, return into it'. Settled for the rewrite by the A/B rows (SRR0 untouched, pc unmoved) and memory.c:645-651 (no exception); the ARM analogy fails on grok's reading of cpu_arm_instr.c:4089-4091.
D2 what a bare return does. GLM and Gemini: a same-pc live-lock; Astra and Grok: dispatch has already incremented next_ic, so a skip. Settled for Astra and Grok by A: step lands on 0x02040004 and continue names 8,272 distinct addresses.
D3 the replacement on the -T route. Astra and Grok: park with nothing_call; GLM: goto bad; Gemini: halt or raise by architecture. Settled for the park by B's measurement; goto bad loses on its false message and on disassembling a zero-filled buffer; a raise loses on the sentinel row.

PART 28/36
D4 the exception-delivered branch (change 6). Astra and Gemini: branch on it; Grok: a translate failure here would have failed in the lookup first. Both accepted: Grok's reason is a fact (Fact 1, and the same MSR for both translations), so the branch is reached on no measured session and its comment says so; it stays because ruling 3 makes the arm raise, and a delivered exception must never be doubled.
D5 the running-1 result (change 7). Astra: no skip, no zero-fill, no invented ISI, result open; GLM: skip; Grok: not settled. Settled against the skip by A; the open result is closed by the fix-design rule and the manual: machine check under MSR[ME], checkstop otherwise. Provisional (part 31).
D6 the read-ahead guard (U1 in grok's list). Astra alone asked; nobody disputed. Accepted on bad:'s own rule; B carried it and measured clean.

PART 29/36
D7 Gemini's change 5 (halt or MCE/ISI by architecture). Accepted only for P3 and only as a machine check; rejected for P1, where no architectural event occurred and the sentinel row would fail; an ISI is rejected everywhere the access translated.
D8 change 10 (no 'UNIMPLEMENTED instruction' in the -T transcripts). Astra and Grok asked; GLM's goto bad would print it. Settled for the assertion; it is in rows 1-3.
D9 the pass-1 split. Grok and Astra: NO-GO on the bug review; GLM: GO-WITH-CHANGES; Argon: draftable. The bug review's producer story (the ISI route) was wrong, as Fact 1 shows; the defect is real and measured on the -T route (Fact 2, BASE 11/17 with exit 1). The bug stands with its producer corrected; the review's text is amended to Fact 2, not withdrawn.

PART 30/36
D10 ordering inside the arm. Argon's six fix checks left four UNSETTLED, and the consolidation shows the seats never agreed on the order of the guards. Ruled: read-ahead first (no side effects for an address the guest has not reached), the pc-moved guard second (never double an exception), the !running park third (the halt already taken), the raise last (only a running CPU with no exception can take a new one). Each later branch's precondition is what the earlier branches exclude, which is why the comments can be true as written. Measured-equivalent to B on rows 1-3: on the -T route the first two guards are no-ops (read-ahead clear, pc equal to addr), REASONED from Fact 2 and confirmed by rerunning the probe after the edit.

PART 31/36
UNSETTLED, and what settles each.
U1 ppc_exception(cpu, 0x2): does cpu_ppc.c:318-344 accept a vector it does not list (its SRR1 arm), and does it re-point next_ic? Settles: read those lines; build and run row 5. The fix tolerates the second answer either way (the refresh in C3); the first is required for C5.
U2 the names PPC_MSR_ME and quick_pc_to_pointers in the PPC header and instr file. Settles: grep; substitutes named in part 17.
U3 the vga_gfx producer's reachability with -X. Settles: an X11 build running row 5.
U4 a 64-bit CPU or a PPC603 on the -T route. The arm is mode-independent (next_ic and nothing_call are shared) but unmeasured; with IR on, the 64-bit translation exits in the lookup first (XLATE 279-289). Settles: a 64-bit machine in the harness.
U5 the 750 manual reading that a fetch TEA is a machine check: from memory of the manual. Settles: its exception chapter.

PART 32/36
TO FILE as separate rows.
F1 dev_vga.c:617-618 uses '>=', so the window's last word is declined on a read that fits: an off-by-one in the device. Fixing it removes the only reasoned P3 producer; row 5 then needs a synthetic device that declines an instruction-width read.
F2 XLATE's two host kills, the BAT 'TODO' exit (memory_ppc.c:268-277) and the 64-bit translation exit (279-289): the same family as this bug, reached from the lookup, not from this arm.
F3 read-ahead fetches reach memory_rw with side effects: under -T a read-ahead past RAM halts the machine and announces an address the guest never executed. Read-ahead should fetch with no side effects.
F4 the W8 row: no read-ahead producer for this arm exists in tree; it needs F3's harness or F1's synthetic device.
F5 the probe: note that the step column's second 'non-existant' line is the debugger's disassembly read.

PART 33/36
THE WEAKEST RULING is ruling 3, the machine-check arm. It rests on three things the packet does not check: U1 (ppc_exception accepts vector 0x2 and sets SRR0 from pc), U2 (the names), and U5 (the manual: a fetch bus error is a machine check, checkstop with ME clear). It is also the one ruling with no measurement behind it and no row runnable today. Overturned by: a row-5 run landing anywhere but 0x200 with SRR0 0xc00b7ffc, or ppc_exception exiting on an unknown vector, or a manual citation that the 750 handles a fetch TEA otherwise. If overturned, part 18's fallback applies: both ME states take the checkstop branch with an honest message, and the machine check is filed as an IMPLEMENT row. Nothing else in the fix changes.

PART 34/36
Second-weakest: the pc-moved guard (ruling 2). It is cheap and its comment is true, but it reads 'pc equals addr' as 'no exception', which misclassifies the one pathological case where the vector address itself is the failing fetch (an ISI whose vector cannot be fetched; real hardware loops there too). Overturned by a producer for that case; the remedy would be a flag set by ppc_exception, a larger change than this bug warrants. Third: the claim that read-ahead never reaches 0x02040000 on the -T route rests on read-ahead staying inside the ic page (REASONED from the BAD block and B's clean line counts); a grep of the read-ahead loop in cpu_dyntrans.c settles it.

PART 35/36
WHAT THE IMPLEMENTER DOES, in order. Apply C6, then C1-C5 from parts 12-16. Confirm U1 and U2 by reading cpu_ppc.c:318-344 and grepping the two names; if either fails, apply part 18's fallback and file #MMM. Rebuild. Run the frozen probe: expect 17/17 ABSENT and the B columns on rows 1 and 2 (PC 0x02040000, SRR0 0x11111111, 2 and 1 'non-existant' lines, 0 'read failed'). Add row 3 to the probe. Keep row 4 as the ISI control. Bank row 5 as owed and blocked on -X, with F1 noted beside it. File F1-F5. Amend the bug review's producer paragraph to Fact 2.

PART 36/36
Rulings 1-7, changes C1-C6, rows 1-5. The draft as written is not shippable: its comment is false on the measured route and its bare return turns a halt into a skip. With the changes above it is.
CLOUDFINAL qhslowifetch: 7 RULINGS 6 CHANGES 5 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS
