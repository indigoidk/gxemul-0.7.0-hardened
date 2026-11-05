Begin your answer with the token CLOUDRECON_QHS on its own line, then `model: <your model name>`, then your verdict line.  Do not
call any tool and do not write files; answer in plain text.

# RECONCILIATION -- `qhslowifetch`: your two final rulings on the same packet (Claude Code Cloud; Fable 5.1)

**Framing.**  GXemul is a computer-architecture emulator (a developer tool that runs legacy operating systems in a software sandbox); this fork
is a software-correctness hardening effort, and every fix ships with a regression test.  Plain correctness language, please.

**What happened.**  You gave the final design ruling on this bug twice, from the same packet, in two independent Claude Code Cloud runs: r1
(the ruling of record) and r2 (a replication).  Their verdicts agree; their change and row lists differ.  The main loop implements ONE fix and
ONE row list, and it records and does not rule -- so the reconciliation is yours.  Below are sections 2-4 (the ruling, the fix, the rows) of r1 and the whole ruling (its section headings did not parse) of r2.  You have no
repository: cite the rulings' own items; mark claims CHECKED-IN-PACKET, REASONED or UNSETTLED.

**Answer, VERDICT LINE FIRST (`VERDICT: R1-STANDS | MERGE | R2-SUPERSEDES`), in this order -- keep it compact; code only where it changes:**
1. Every difference between r1 and r2 (disposition, code, comment sentence, row, filed item), one line each, citing each ruling's item.
2. For each: OWED (r1 is wrong or incomplete without it -- quote the r1 sentence), OPTIONAL (wording, or a row another row already covers --
   name it), or WRONG (quote the line it contradicts).  Where they CONFLICT, both sides in a line and which argument is stronger and why.
3. THE MERGED FIX: the exact final code for every hunk that differs from r1's, every product comment TRUE AS WRITTEN; say "r1 as written"
   for each hunk that does not change.
4. THE MERGED ROWS: the final row list (session, guest action, want, the wrong edit each catches), within "rows per enumerated wrong edit".
5. The weakest of these reconciliation rulings, and what would overturn it.
Final line: `CLOUDRECON_QHS: <d> DIFFERENCES <o> OWED <c> CONFLICTS <r> ROWS VERDICT:<R1-STANDS|MERGE|R2-SUPERSEDES>`

---

## r1 -- the ruling of record (FABLE_FINAL.md)

```
2. THE RULING. The failure arm is entered in FOUR distinguishable states, and the draft treats them as one. I rule each.
R-A, the measured producer: -T, real mode, physical address past RAM plus the 256 KB slack. memory.c has already cleared cpu->running and printed the "non-existant paddr" line. No PowerPC exception exists and none may be invented: -T is a host debugging option of the binary, not guest-visible architecture. Disposition: honor the halt already delivered. Park with next_ic = &nothing_call, return before the decode tail, leave the slot TO_BE_TRANSLATED, leave cpu->pc at addr (already set at 4089), leave SRR0/SRR1 untouched. Menu: 2 DECLINE the fetch. The machine stop belongs to -T and memory.c, not to this arm.

Warrant for R-A: B measured exactly this. PC 0x02040000 under step and continue, SRR0 sentinel 0x11111111 intact, one "non-existant" line under continue, debugger prompt, exit status 0, a second step or continue changes nothing. CHECKED-IN-PACKET.
Why the bare return (A) is WRONG on R-A: A's PC moved to 0x02040004 under step and to 0x02048140 under continue, and its 8,272 lines name 8,272 distinct addresses. The dispatch loop had therefore advanced next_ic before calling the translator (Astra's reading, now CONFIRMED by measurement). A return that sets nothing makes the loop call the next slot's TO_BE_TRANSLATED, which fails the same way, through the whole batch.

That is a silent skip-walk, not a live-lock. Two stories are measured false at once: GLM's and Gemini's "same-PC live-lock", and the draft's own "a re-fetch of the same address repeats the exception". A skip-walk is a correctness defect of its own kind, since the guest's PC advances past code that never executed and the CPU reports a halt at the wrong address. A cannot ship.
The probe's 17/17 for A is also evidence about the probe: as frozen it does not separate A from B. See the rows section.

R-B, defensive and not reached in any session: the translation inside THIS memory_rw raised an ISI or a 603 IMISS (memory_ppc.c:307-323). ppc_exception has then saved SRR0/SRR1, moved cpu->pc to the vector, and redone pc_to_pointers, so next_ic already points at the handler. Disposition: bare return, which is the draft's story and is correct only here. Menu: 5 FAULT, already delivered upstream.

Reachability of R-B is REASONED unreachable on PPC: the dispatch lookup translated the same PC with FLAG_INSTR under the same MMU state an instant earlier, so a second translation cannot fail (Grok's #6 argument stands). Astra and Gemini are right that the body differs when it does happen. I keep the arm because its test is of observable state and costs one compare: `cpu->pc != addr` is true exactly when an exception moved the PC inside this call. No new field in struct cpu, no invented flag. This settles D4 of the consolidation.

Corner of R-B: if the failing fetch IS the vector address (IR on, vector page untranslatable), pc equals addr after the exception and control falls to R-C/R-D. Real hardware loops on the same state forever. Acceptable; no special case.
R-C, speculative: cpu->translation_readahead is set. The translator is being called ahead of execution for later slots of the current page. It must touch nothing: no next_ic (that would clobber the live one), no print, no exception. Disposition: return silently, slot stays TO_BE_TRANSLATED so a real fetch re-enters the arm. Menu: 2 DECLINE silently. Astra's #8 was one seat; I adopt it on the argument, which is structural: `bad:` itself returns early under readahead for the same reason (BAD block, CHECKED).

Reachability of R-C: REASONED reachable only on the device producer. Readahead starts after a SUCCESSFUL translation in the same page. Past RAM every fetch fails under -T or decodes a zero word to `bad:` without -T, so readahead never begins there. On a device page such as vga_gfx's, slots before the last word translate, and readahead walks into 0xc00b7ffc.
Order: R-C must precede R-A's park. Under -T a readahead fetch past RAM would also clear running inside memory.c; parking then overwrites next_ic in the middle of translating a live instruction. That -T-under-readahead halt is a pre-existing wart of memory.c plus readahead, outside this bug (filed as F1).

R-D, reasoned producer, unmeasured: cpu->running still 1, no exception delivered, not readahead. A device's access function declined an instruction-width read. The census found exactly one: vga_gfx's last word (dev_vga.c:617-618) on prep ibm6050 with -X, fetch at physical 0xc00b7ffc in real mode, no -T. memory_rw.c:595-603 has no PPC exception arm, so HEAD exits. Disposition: the manual's exception for an instruction fetch the bus declines is a Machine Check, vector 0x200. Menu: 5 FAULT. Code: `ppc_exception(cpu, PPC_EXCEPTION_MC)` with `#define PPC_EXCEPTION_MC 0x2` added to cpu_ppc.h, which the packet says has no such constant. SRR0/SRR1 are whatever ppc_exception saves for every other vector; manual-exact SRR1 status bits are NOT claimed. PROVISIONAL: ppc_exception's body is not in the packet.

Why FAULT rather than an explicit CPU-STOP for R-D, both sides. For a stop: it is honest, measurable by construction, and GLM's "follow the data path" accepts it. Against a stop: the design rule for a CPU core is to raise the architectural exception and never stop the machine; the guest OS may own a machine-check handler (NetBSD/prep does); and a wrong MC is never silent, since ppc_exception prints its "[ PPC Exception ]" line. Against FAULT: it is unmeasured (needs an X11 build), and real hardware with MSR[ME]=0 checkstops, which the arm does not model. I rule FAULT and name it my weakest ruling in section 7.

Rejected for every arm: falling through to decode the zeroed buffer. memory_rw zeroes ib on failure (#244), so the tail would decode 0x00000000, reach `bad:`, and print "UNIMPLEMENTED instruction" for a word that was never read. That misdescribes the failure, which is consolidation #10's argument; adopted.
Final order of the arms: R-B (pc moved), R-C (readahead), R-A (!running), R-D (running, no exception). R-B first because next_ic is already right and nothing may touch it. R-C before R-A for the clobber in PART 10. R-A before R-D because a cleared running IS the -T halt and must not become an MC the guest never asked for; that is what Gemini's row-5 body would do, and the -T rows' SRR0 sentinel assertion is what catches it.

3. THE FIX. Replace the failure arm at HEAD 4117-4120 with the following. Every comment is written to be TRUE AS WRITTEN against the packet.

'''
        } else {
            if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
                sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
                /*  #NNN: the instruction fetch failed.  This
                    used to be fatal() + exit(1).  Four states
                    reach here; none may run this slot, and
                    the slot stays TO_BE_TRANSLATED.  */
'''

'''
                /*  (a) The translation in memory_rw raised an
                    ISI or 603 IMISS: ppc_exception() saved
                    SRR0/SRR1, moved pc to the vector and redid
                    pc_to_pointers, so next_ic is the handler.
                    Not seen in any session (the dispatch PC
                    lookup translates first); kept as a guard.  */
                if (cpu->pc != addr)
                    return;
                /*  (b) Read-ahead: speculative. Touch nothing.  */
                if (cpu->translation_readahead)
                    return;
'''

'''
                /*  (c) -T: memory.c cleared running and printed
                    the non-existant line.  No PowerPC exception
                    is involved.  Park at this pc (set above) so
                    the debugger shows the failing fetch.  */
                if (!cpu->running) {
                    cpu->cd.ppc.next_ic = &nothing_call;
                    return;
                }
                /*  (d) A device declined an instruction-width
                    read while running: machine check (0x200).
                    SRR1 status bits are not modelled.  */
                ppc_exception(cpu, PPC_EXCEPTION_MC);
                return;
            }
        }
'''

Second hunk, src/cpus/cpu_ppc.h, beside PPC_EXCEPTION_ISI and PPC_EXCEPTION_DSI:

'''
#define    PPC_EXCEPTION_MC    0x2    /*  Machine check, vector 0x200  */
'''

The dead `/*  goto bad;  */` at 4120 goes with the old arm. Nothing else changes: the decode tail, DYNTRANS_TO_BE_TRANSLATED_HEAD at 4130, and the success path are untouched. The slot stays TO_BE_TRANSLATED in all four arms because ic->f is only assigned by the tail, which none of them reaches.

Comment audit against the draft (consolidation #1, all four seats, adopted in full). Removed: "Return and let the CPU take the exception" (false on the measured route; no exception exists). Removed: the #234 MIPS analogy (that arm follows a delivered exception; ours mostly does not) and "as cpu_arm_instr.c always did" (ARM is fatal then return, cpu_arm_instr.c:4089-4091 per the consolidation, a different disposition). Removed: "a re-fetch of the same address repeats the exception" (A measured a skip, not a re-fetch). grok's v3 one-paragraph comment is true but under-specified: it names only the measured route and does not say why the code does four things. Mine supersedes it.

Why `cpu->pc != addr` is a safe test (REASONED). Line 4089 wrote cpu->pc = addr immediately before the read, and nothing shown between 4089 and the memory_rw call writes pc. ppc_exception writes pc to the vector (nr * 0x100, with the IP-bit base), inferred from the 603 arms. memory.c's -T path and a device decline do not write pc. So pc != addr holds if and only if an exception was delivered inside this memory_rw, with the single false negative of PART 9. Overturned by any pc write in 4090-4115; none appears in the packet.

4. THE ROWS the fix owes. Harness: regress/ppc_ifetch_probe.py (frozen md5 3826ecfb4816), -E pmppc unmodified, `ori r0,r0,0` raw at 0x2000, SRR0 preset to the sentinel 0x11111111. Enumerated wrong edits first, so the bound "rows per wrong edit" is auditable:
W1 HEAD: fatal + exit(1).
W2 bare return (draft A): skip-walk.
W3 goto bad: prints UNIMPLEMENTED and disassembles a word never read.
W4 invent an ISI or MC on the -T route (Gemini's row-5 body).
W5 the park re-arms or re-fires on a second step/continue.
W6 fall through to decode the zeroed buffer.
W7 disturb the dispatch-lookup ISI route.
W8 omit the readahead guard (clobbers next_ic on a device page).
W9 omit the running-still-1 arm (R-D exits or stops).

ROW 1, -T step. Session: `-T`, pc=0x02040000, SRR0=0x11111111, step once. Want: process alive, debugger prompt, pc=0x02040000, SRR0=0x11111111, zero "read failed" lines, "non-existant" lines at most 2 (B measured 2; the second is REASONED to be the debugger's own display read, see U5), exit status 0 at quit. Catches W1 (exit 1), W2 (pc 0x02040004), W4 (SRR0 changed).
ROW 2, -T continue. Same session, continue instead of step. Want: pc=0x02040000, SRR0 sentinel, exactly 1 "non-existant" line, zero "read failed", prompt, alive. Catches W2 decisively (A: 8,272 lines, pc 0x02048140). This is the A/B separator (consolidation #9); adopted.

ROW 3, the halt is stable. After ROW 1 or ROW 2, issue a second step and then a second continue. Want: pc, SRR0 and line counts unchanged, no new "non-existant" lines, process alive. Catches W5. Measured for both A and B ("a second step/continue changes nothing"), so the row also documents that the park does not re-enter memory.c.
ROW 4, text assertions over the ROW 1-3 transcripts. Want: no "UNIMPLEMENTED instruction", no "read failed: TODO", no "[ PPC Exception". Catches W3, W6 (the zero word decodes to UNIMPLEMENTED), W1, W4. Consolidation #10, adopted.

ROW 5, ISI control, behaviour unchanged. Session: IR on, pc=0x20000000 (a reset-BAT gap), step; then the same under continue. Want: SRR0=0x20000000, pc=0x400, alive, identical to BASE. Catches W7 and freezes Fact 1: this route never enters the arm. Measured identical on BASE, A and B.
ROW 6, no -T control. Session: no -T, pc=0x02040000, step. Want: HEAD's behaviour unchanged. The fetch reads zeros (memory_rw returns success), the zero word reaches `bad:`, the CPU stops with "UNIMPLEMENTED instruction", process alive. Catches an edit that lets the no -T route enter the arm. REASONED from Fact 2; the exact transcript text is frozen from the first run.

ROW 7, FILED, not runnable in this harness. Session: `-E prep -e ibm6050 -X` on an X11 build with a display, real mode, pc=0xc00b7ffc. Want: alive, running still 1, pc=0x200 (0xfff00200 with MSR[IP]), SRR0=0xc00b7ffc, one "[ PPC Exception 0x2" line, no UNIMPLEMENTED, no exit. Catches W9; with a successful slot at 0xc00b7ff8 and readahead on, also W8 (a clobbered next_ic shows as the wrong pc after the handler's rfi). The producer's reachability is REASONED from the census, so this ships as a filed row marked pending-X11, never as a green row.
Controls: null.out (/bin/true) and nobin.out stay FAIL/ABSENT as in the witness.

Bound check: nine wrong edits, seven rows plus two controls. Every W has at least one row; W2 and W4 have two; no row exists without a named W. Bound met.
Probe note: A and B both scored 17/17, yet A is wrong. The frozen probe therefore does not separate the skip-walk from the park. ROW 2's pc and line-count assertions and ROW 3 are NEW checks; the md5 must be re-frozen after adding them, and until then "17/17" is not evidence of a correct arm. CHECKED-IN-PACKET.

```

## r2 -- the replication (FABLE_FINAL_r2.md)

```
CLOUDFINAL_QHS_20261104
model: claude-fable-5-1 (configured id; the serving model may differ)
EVIDENCE BASIS: the compact packet only; no repository. CHECKED-IN-PACKET: the HEAD excerpts (IFETCH, XLATE, MEMRW, BAD), the draft text, the rung-3 witness (Facts 1-2), the A/B measurement table, grok's consolidation. PROVISIONAL points: ppc_exception's handling of a vector it does not list and whether it re-points next_ic (cpu_ppc.c:318-344 not quoted); PPC_MSR_ME and quick_pc_to_pointers in the PPC headers; the vga_gfx producer (reasoned, unmeasured).
VERDICT: GO-WITH-CHANGES. B's park is the fix for the measured -T halt. The draft's comment and bare return are wrong as written. A decline with running still 1 gets a machine check, provisional on the points above.

EVIDENCE BASIS, detail. Omitted and not relied on: the full pass-1 briefs and the seat answers; every seat position below is taken from grok's consolidation and the verdict table. What each source settles: Fact 1 (measured) settles that the ordinary ISI route never enters the failure arm. Fact 2 and the BASE row settle the producer: -T plus a real-mode fetch past RAM and the 256 KB slack, with memory.c:645-651 clearing running and raising nothing. The A row settles what a bare return does (a skip across 8,272 slots, not a live-lock). The B row settles that the park finishes the halt on the fetch pc with SRR0 untouched. Nothing in the packet measures a failed fetch with running still 1, read-ahead entering the arm, a 64-bit CPU or a 603; every ruling on those is REASONED or UNSETTLED and marked so.

THE RULING, overview. Three producers, three dispositions:
P1 the measured -T halt (running already cleared by memory.c): menu 2 DECLINE silently, as a park on the fetch pc (next_ic = &nothing_call; return). memory.c already announced the address; the core adds nothing and raises nothing.
P2 an ISI or 603 miss already delivered by the translation inside memory_rw: menu 5 FAULT, already delivered; the arm returns after refreshing next_ic. REASONED unreachable on every 32-bit session; kept as a guard.
P3 a physical decline with running still 1 (a device failing an instruction-width read): menu 7 IMPLEMENT the architectural exception: a machine check, vector 0x200, when MSR[ME] is set; a checkstop (CPU stop, process alive) when it is clear. PROVISIONAL.
Plus: read-ahead returns silently before any of the three (the bad: rule).

RULING 1 (P1, the measured -T halt). Disposition: park. Warrant, CHECKED-IN-PACKET: memory.c:645-651 clears every CPU's running and returns without a PowerPC exception, so by the time the arm runs the halt is already taken and announced ('memory READ: from non-existant paddr=0x02040000'). The arm's only job is to leave the CPU parked where the halt happened. B measured that: PC 0x02040000, SRR0 0x11111111 untouched, one non-existant line under continue, prompt reached, exit 0, and a second step or continue changes nothing. A measured the alternative: the bare return leaves next_ic on the slot after the failed one (dispatch increments before calling the translator), so step lands on 0x02040004 and continue walks 8,272 distinct addresses before the run loop sees running clear.

RULING 1, continued. No PowerPC exception is raised on P1, and none may be invented. -T is a debugger option of the binary ('halt on a non-existent memory access'); the halt is the user's request, not an architectural event, and the guest must see nothing: SRR0/SRR1 untouched, MSR untouched, pc on the fetch address. The probe pins this with the 0x11111111 sentinel; an edit that raised an ISI or a machine check here would move SRR0 and pc and fail rows 1 and 2. This also disposes of Gemini's change 5 for P1. REASONED: the same holds without -T, where memory.c returns zeros and the CPU stops on the zero word at the bad: label; that route never enters the arm (memory_rw succeeds), so the fix does not touch it.

RULING 2 (P2, an ISI or 603 miss already delivered). REASONED unreachable: the dyntrans PC lookup (cpu_dyntrans.c:670-680, Fact 1) translates the fetch address with FLAG_INSTR under the same MSR, BATs and page tables before the translator runs; memory_rw's second translation of the same address cannot fail where the first succeeded, and nothing between the two changes CPU state. Grok's objection to change 6 is accepted as a fact. Fact 1 measured the consequence: on the ISI route all three binaries are identical and the arm is never entered. The draft's comment, which names this as the producer and borrows the MIPS #234 shape, is false on every measured session and must go (change 1, all four seats).

RULING 2, continued. The guard stays, for one reason: ruling 3 makes the arm raise an exception when running is still 1, and ppc_exception (cpu_ppc.c:318-344, per the packet) does not clear running, so an exception delivered inside memory_rw would otherwise fall into the running-1 arm and be doubled, with SRR0 overwritten. The discriminator is cheap and true: ppc_exception moves cpu->pc to the vector (Fact 1 shows execution resuming at 0x400), while memory.c:645-651 and a device decline leave pc equal to addr (line 4089 set it). So: if pc differs from addr, refresh next_ic and return. The refresh is deliberate: whether ppc_exception itself re-points next_ic is UNSETTLED (cpu_ppc.c:318-344 is not quoted); refreshing is idempotent and makes the arm correct either way. The comment says the branch is reached on no measured session.

RULING 3 (P3, a physical decline with running still 1). The only reasoned producer is dev_vga.c:617-618 ('relative_addr + len >= GFX_ADDR_WINDOW' returns 0) on prep ibm6050 with -X, fetching the window's last word 0xc00b7ffc in real mode; memory_rw.c:595-603 has no PPC exception arm, so today the process ends. Not measured. What the arm must not do is settled by A: a bare return executes the next slot, so the guest silently skips an instruction it could not fetch. GLM's 'otherwise skip' is rejected on that measurement. Astra's 'no skip, no zero-fill, no invented ISI' is accepted; its open question is closed by the fix-design rule for CPU cores: raise the exception the manual prescribes.

RULING 3, warrant. REASONED from the PowerPC OEA and the 750 user's manual: an instruction fetch the bus terminates with an error (TEA) is a machine check, vector 0x00200, taken when MSR[ME] is set; with MSR[ME] clear the processor checkstops. That maps onto the emulator: ME set, ppc_exception(cpu, PPC_EXCEPTION_MC) with SRR0 = the fetch address (cpu->pc = addr at line 4089; ppc_exception saves pc into SRR0 per the draft's reading); ME clear, a message naming the address and a CPU stop. That stop is a CPU-STOP the architecture itself prescribes, not a host kill. An ISI is wrong here: ISI is a translation or protection fault, and this access translated. PROVISIONAL on: PPC_EXCEPTION_MC being new (cpu_ppc.h has no machine-check constant), PPC_MSR_ME existing, ppc_exception accepting vector 0x2.

RULING 4 (read-ahead). If cpu->translation_readahead is set, return before any other branch. Warrant: the bad: label (CHECKED-IN-PACKET) already returns silently during read-ahead because the guest has not executed that address; a failed fetch is the same situation. Without the guard, ruling 3 would deliver a machine check for an instruction the guest never reached, and ruling 1 would park a running CPU. B carried this guard and measured 17/17, so it is harmless on the measured routes; it is unscored there (read-ahead stays inside the ic page and the slack pages read zeros). Astra's change 8 accepted.
RULING 5 (goto bad, GLM's changes 3 and 4): rejected. bad: prints 'UNIMPLEMENTED instruction' and disassembles ib, which memory_rw zero-filled (#244): a false message about a fetch halt. Change 10's assertion goes into rows 1-3.

RULING 6 (the draft comment). Replaced in full. Every sentence of it is false or unsupported on the measured route: no ISI was raised, SRR0 was not saved, pc did not move, pc_to_pointers did not run, 'let the CPU take the exception' names an exception that does not exist, the MIPS #234 and ARM analogies do not hold (cpu_arm_instr.c:4089-4091 is fatal then return, per grok's table), and 'a re-fetch of the same address repeats the exception' describes a live-lock that A shows does not happen. Grok's v3 consensus comment is true but says nothing about what the arm does; the per-branch comments in parts 13-16 replace it.
RULING 7 (the slot). The arm returns before the success tail, so ic->f stays TO_BE_TRANSLATED and the next attempt re-runs the arm. CHECKED: B's second step changes nothing. Row 3 pins it.

THE FIX. Two files. (1) src/cpus/cpu_ppc.h: add, beside PPC_EXCEPTION_ISI,
'''
#define PPC_EXCEPTION_MC   0x2   /*  Machine check, vector 0x200  */
'''
(ppc_exception multiplies by 0x100, as the 603 vectors 0x10-0x12 and ISI 0x4 show in XLATE 307-323; the call sites are CHECKED-IN-PACKET, the multiplier itself REASONED.)
(2) src/cpus/cpu_ppc_instr.c, X(to_be_translated): lines 4117-4120 (the fatal, the exit(1) and the commented goto) are replaced by the block in parts 13-16. Lines 4115-4116 (the memory_rw call) and 4121-4122 stay. Indentation is the file's tabs; shown here with spaces. #NNN is this bug's number.

'''
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
'''

'''
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
'''

'''
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
'''

'''
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
'''

FIX, notes. Every comment above is true as written on the packet's evidence, with these dependencies to confirm at build time: 'as the bad: label does' (CHECKED, BAD block); 'memory.c has printed the address and cleared running' (CHECKED, Fact 2); 'reached on no measured session' (CHECKED, Fact 1); 'the OEA prescribes a machine check' (REASONED, manual). Names: nothing_call compiles in this file (B was built with it: CHECKED). quick_pc_to_pointers is the dyntrans name the PPC branch instructions use (REASONED; a grep of cpu_ppc_instr.c settles it; the 32/64-bit pc_to_pointers pair is the substitute). PPC_MSR_ME is the MSR bit-12 name the header family uses (REASONED; grep). ppc_exception is already called from this file for sc and traps (REASONED). fatal() does not exit: HEAD needed the separate exit(1) (CHECKED).

FIX, the fallback for ruling 3. If U1 or U2 (part 31) fails at build time, the machine-check branch is not shipped half-built. The arm then takes the checkstop branch for both MSR[ME] states, with the message changed to '[ ppc: instruction fetch from 0x... declined; no machine check modelled yet, see #MMM ]', and #MMM is FILED as the IMPLEMENT row for the machine check. That fallback is still a CPU-STOP with the process alive, strictly better than HEAD, measured-equivalent to B on rows 1-3, and its comment is true. Not acceptable in any version: a bare return (a skip), goto bad (a false message), or an ISI.

CHANGES to the draft, the count the final line reports:
C1 replace the draft comment in full (ruling 6).
C2 add the read-ahead guard, first (ruling 4).
C3 add the pc-moved guard with a next_ic refresh (ruling 2).
C4 add the !running park with nothing_call (ruling 1; this is B).
C5 add the running-1 arm: machine check under MSR[ME], checkstop otherwise (ruling 3; provisional, with the part-18 fallback).
C6 add PPC_EXCEPTION_MC to cpu_ppc.h.
Not changed: the lookup at cpu_dyntrans.c:670-680, memory.c:645-651, memory_rw.c, the XLATE exits, dev_vga.c (each FILED where it is a defect, part 32).

THE ROWS the fix owes. Wrong edits enumerated first; the bound is one row per wrong edit, and a row may catch several.
W1 the process still ends (an exit or abort left in, or reintroduced).
W2 a bare return: the declined slot is skipped (A).
W3 an exception invented on the -T route (ISI or machine check in the park branch).
W4 goto bad, or any message that misnames the halt as an unimplemented instruction.
W5 the arm falls through into the success tail and marks the slot translated.
W6 a silent skip when running is still 1.
W7 a wrong machine check: vector, SRR0, or MSR[ME] gating.
W8 the read-ahead guard missing. No row is deliverable for W8 (no producer reaches the arm from read-ahead on any in-tree machine); FILED, part 32.

ROW 1 (-T, step). Session: -E pmppc, unmodified in-tree, 32 MB, -T, the probe's raw 'ori r0,r0,0' at 0x2000 (regress/ppc_ifetch_probe.py, md5 3826ecfb4816). Guest action: pc = 0x02040000, SRR0 = 0x11111111, step once. Want: the process alive at the debugger prompt, exit status 0; PC 0x02040000; SRR0 0x11111111; exactly 2 'non-existant paddr=0x02040000' lines (the step's disassembly read and the fetch, as BASE and B both show); 0 'read failed' lines; no 'UNIMPLEMENTED instruction'; no 'PPC Exception' line. Catches: W1 (no prompt, exit 1), W2 (PC 0x02040004), W3 (SRR0 or PC moved), W4 (the UNIMPLEMENTED line). Measured as B's step column.

ROW 2 (-T, continue). Same session as row 1; guest action: continue instead of step. Want: prompt, exit 0; PC 0x02040000; SRR0 0x11111111; exactly 1 'non-existant' line; 0 'read failed'; no 'UNIMPLEMENTED instruction'; no 'PPC Exception'. Catches: W2 in its loud form (A printed 8,272 lines naming 0x02040000 to 0x0204813c), and any ordering edit that lets the dispatch loop pass the park (a line count above 1 is the signal). Measured as B's continue column.

ROW 3 (-T, repeat after the halt). After row 1 or row 2: step again, then continue again. Want: PC still 0x02040000; SRR0 still 0x11111111; one more 'non-existant' line per attempt and nothing else; no 'read failed'. Catches: W5. An arm that reaches the success tail would have marked the slot translated with a zero-filled ib (#244), and the second attempt would execute that half-translated slot instead of re-running the arm: PC would move or an 'UNIMPLEMENTED' line would appear. The packet reports 'a second step/continue changes nothing' for B; this row keeps that true.

ROW 4 (the ISI control). Session: -E pmppc as above, MSR[IR] set, pc = 0x20000000 (a reset-BAT gap), SRR0 = 0x11111111. Guest action: step; in a second session, continue. Want, under both: SRR0 0x20000000; PC 0x400; no 'read failed'; no 'non-existant'; transcript identical to HEAD's. Catches: an edit that widens the fix into the lookup at cpu_dyntrans.c:670-680 or routes the ISI through the arm, where the pc-moved guard would pass by design but a misplaced park or machine check would not. This is also the control that pins Fact 1; it was among the probe's 17 and all three binaries pass it.

ROW 5 (a decline with running still 1; PROVISIONAL, blocked on an X11 build). Session: -E prep -e ibm6050 -X, real mode, MSR[ME] set, SRR0 = 0x11111111, pc = 0xc00b7ffc (the last word of the vga_gfx window; dev_vga.c:617-618 declines it). Guest action: step. Want: process alive; PC 0x200; SRR0 0xc00b7ffc; running still 1 (a following continue runs from 0x200); no 'read failed'; no 'non-existant'. Variant, MSR[ME] clear: the checkstop message naming 0xc00b7ffc, prompt, PC 0xc00b7ffc, SRR0 sentinel. Catches: W6 (PC 0xc00b8000, SRR0 sentinel, nothing printed) and W7 (another vector, SRR0 not the fetch address, or a machine check taken with ME clear). Caveat: fixing dev_vga's off-by-one (F1) removes this producer; the row then needs a synthetic declining device (part 32).

ROWS, tally. Five rows against eight enumerated wrong edits; no wrong edit has more than one row; W8 has none and is filed. Rows 1-4 are measurable now on pmppc with the frozen probe (rows 1, 2 and 4 are its existing -T and ISI checks; row 3 is a two-line extension of the same session). Row 5 is owed but cannot be measured in the current harness. The final-line count is 5.

DISAGREEMENTS SETTLED.
D1 the comment. All four seats: rewrite; the draft: 'ISI already raised, return into it'. Settled for the rewrite by the A/B rows (SRR0 untouched, pc unmoved) and memory.c:645-651 (no exception); the ARM analogy fails on grok's reading of cpu_arm_instr.c:4089-4091.
D2 what a bare return does. GLM and Gemini: a same-pc live-lock; Astra and Grok: dispatch has already incremented next_ic, so a skip. Settled for Astra and Grok by A: step lands on 0x02040004 and continue names 8,272 distinct addresses.
D3 the replacement on the -T route. Astra and Grok: park with nothing_call; GLM: goto bad; Gemini: halt or raise by architecture. Settled for the park by B's measurement; goto bad loses on its false message and on disassembling a zero-filled buffer; a raise loses on the sentinel row.

D4 the exception-delivered branch (change 6). Astra and Gemini: branch on it; Grok: a translate failure here would have failed in the lookup first. Both accepted: Grok's reason is a fact (Fact 1, and the same MSR for both translations), so the branch is reached on no measured session and its comment says so; it stays because ruling 3 makes the arm raise, and a delivered exception must never be doubled.
D5 the running-1 result (change 7). Astra: no skip, no zero-fill, no invented ISI, result open; GLM: skip; Grok: not settled. Settled against the skip by A; the open result is closed by the fix-design rule and the manual: machine check under MSR[ME], checkstop otherwise. Provisional (part 31).
D6 the read-ahead guard (U1 in grok's list). Astra alone asked; nobody disputed. Accepted on bad:'s own rule; B carried it and measured clean.

D7 Gemini's change 5 (halt or MCE/ISI by architecture). Accepted only for P3 and only as a machine check; rejected for P1, where no architectural event occurred and the sentinel row would fail; an ISI is rejected everywhere the access translated.
D8 change 10 (no 'UNIMPLEMENTED instruction' in the -T transcripts). Astra and Grok asked; GLM's goto bad would print it. Settled for the assertion; it is in rows 1-3.
D9 the pass-1 split. Grok and Astra: NO-GO on the bug review; GLM: GO-WITH-CHANGES; Argon: draftable. The bug review's producer story (the ISI route) was wrong, as Fact 1 shows; the defect is real and measured on the -T route (Fact 2, BASE 11/17 with exit 1). The bug stands with its producer corrected; the review's text is amended to Fact 2, not withdrawn.

D10 ordering inside the arm. Argon's six fix checks left four UNSETTLED, and the consolidation shows the seats never agreed on the order of the guards. Ruled: read-ahead first (no side effects for an address the guest has not reached), the pc-moved guard second (never double an exception), the !running park third (the halt already taken), the raise last (only a running CPU with no exception can take a new one). Each later branch's precondition is what the earlier branches exclude, which is why the comments can be true as written. Measured-equivalent to B on rows 1-3: on the -T route the first two guards are no-ops (read-ahead clear, pc equal to addr), REASONED from Fact 2 and confirmed by rerunning the probe after the edit.

UNSETTLED, and what settles each.
U1 ppc_exception(cpu, 0x2): does cpu_ppc.c:318-344 accept a vector it does not list (its SRR1 arm), and does it re-point next_ic? Settles: read those lines; build and run row 5. The fix tolerates the second answer either way (the refresh in C3); the first is required for C5.
U2 the names PPC_MSR_ME and quick_pc_to_pointers in the PPC header and instr file. Settles: grep; substitutes named in part 17.
U3 the vga_gfx producer's reachability with -X. Settles: an X11 build running row 5.
U4 a 64-bit CPU or a PPC603 on the -T route. The arm is mode-independent (next_ic and nothing_call are shared) but unmeasured; with IR on, the 64-bit translation exits in the lookup first (XLATE 279-289). Settles: a 64-bit machine in the harness.
U5 the 750 manual reading that a fetch TEA is a machine check: from memory of the manual. Settles: its exception chapter.

TO FILE as separate rows.
F1 dev_vga.c:617-618 uses '>=', so the window's last word is declined on a read that fits: an off-by-one in the device. Fixing it removes the only reasoned P3 producer; row 5 then needs a synthetic device that declines an instruction-width read.
F2 XLATE's two host kills, the BAT 'TODO' exit (memory_ppc.c:268-277) and the 64-bit translation exit (279-289): the same family as this bug, reached from the lookup, not from this arm.
F3 read-ahead fetches reach memory_rw with side effects: under -T a read-ahead past RAM halts the machine and announces an address the guest never executed. Read-ahead should fetch with no side effects.
F4 the W8 row: no read-ahead producer for this arm exists in tree; it needs F3's harness or F1's synthetic device.
F5 the probe: note that the step column's second 'non-existant' line is the debugger's disassembly read.

THE WEAKEST RULING is ruling 3, the machine-check arm. It rests on three things the packet does not check: U1 (ppc_exception accepts vector 0x2 and sets SRR0 from pc), U2 (the names), and U5 (the manual: a fetch bus error is a machine check, checkstop with ME clear). It is also the one ruling with no measurement behind it and no row runnable today. Overturned by: a row-5 run landing anywhere but 0x200 with SRR0 0xc00b7ffc, or ppc_exception exiting on an unknown vector, or a manual citation that the 750 handles a fetch TEA otherwise. If overturned, part 18's fallback applies: both ME states take the checkstop branch with an honest message, and the machine check is filed as an IMPLEMENT row. Nothing else in the fix changes.

Second-weakest: the pc-moved guard (ruling 2). It is cheap and its comment is true, but it reads 'pc equals addr' as 'no exception', which misclassifies the one pathological case where the vector address itself is the failing fetch (an ISI whose vector cannot be fetched; real hardware loops there too). Overturned by a producer for that case; the remedy would be a flag set by ppc_exception, a larger change than this bug warrants. Third: the claim that read-ahead never reaches 0x02040000 on the -T route rests on read-ahead staying inside the ic page (REASONED from the BAD block and B's clean line counts); a grep of the read-ahead loop in cpu_dyntrans.c settles it.

WHAT THE IMPLEMENTER DOES, in order. Apply C6, then C1-C5 from parts 12-16. Confirm U1 and U2 by reading cpu_ppc.c:318-344 and grepping the two names; if either fails, apply part 18's fallback and file #MMM. Rebuild. Run the frozen probe: expect 17/17 ABSENT and the B columns on rows 1 and 2 (PC 0x02040000, SRR0 0x11111111, 2 and 1 'non-existant' lines, 0 'read failed'). Add row 3 to the probe. Keep row 4 as the ISI control. Bank row 5 as owed and blocked on -X, with F1 noted beside it. File F1-F5. Amend the bug review's producer paragraph to Fact 2.

Rulings 1-7, changes C1-C6, rows 1-5. The draft as written is not shippable: its comment is false on the measured route and its bare return turns a halt into a skip. With the changes above it is.
CLOUDFINAL qhslowifetch: 7 RULINGS 6 CHANGES 5 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS

```

Now write the reconciliation in the order given at the top.
