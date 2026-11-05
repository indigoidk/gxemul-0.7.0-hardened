# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 17:16:57Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-teleport-fqhs/013daa13-40bf-4278-96cf-f3c2bda08ddf.jsonl`
* session: `https://claude.ai/code/session_015fEQzGEWimm5nb84dLxqon`   trigger: `trig_01T8zD28AdLMpwbZhb4v18dr`   packet: `?`
* the answer's message: timestamp 2026-11-04T17:13:45.279Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDFINAL_QHS_20261104`: present; 24877 characters; PART markers N = 42, present 42, MISSING none; `END OF PARTS`: YES
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINAL qhslowifetch: 5 RULINGS 5 CHANGES 7 ROWS VERDICT:GO-WITH-CHANGES

---
PART 1/42
CLOUDFINAL_QHS_20261104
model: claude-fable-5-1 (configured id; the serving model may differ)
Evidence basis: the compact packet only (B source excerpts, C rung-3 witness, D A/B measurements and device census, F consolidation). No repository. Omitted and not seen: the pass-1 brief bodies, full seat answers, the readahead code in the dyntrans TAIL, cpu_ppc.h, ppc_exception's body, memory_rw.c:595-603, dev_vga.c, memory.c:645-651. Every ruling resting on those is marked REASONED or UNSETTLED and is PROVISIONAL on that point.
Verdict: GO-WITH-CHANGES. The draft's direction (no exit, slot stays TO_BE_TRANSLATED) is right. Its body (a bare return) and its comment are wrong on the only measured producer, and it has no arm for a failed fetch while the CPU still runs.

PART 2/42
1. EVIDENCE BASIS, detailed.
CHECKED-IN-PACKET: HEAD lines 4083-4127 (cpu->pc = addr written at 4089 before the read; fatal + exit(1) at 4117-4119; dead `goto bad` comment at 4120); memory_ppc.c arms 299-326; memory_rw.c 248-269 (translate, zero the buffer, return FAILED); the -T witness (BASE exit 1 after "read failed: TODO"); the A versus B table; the ISI control identical on BASE, A, B (SRR0 0x20000000, PC 0x400); B compiled and ran, so `nothing_call` resolves inside cpu_ppc_instr.c and `cpu->translation_readahead` exists.

PART 3/42
REASONED from the packet: memory.c:645-651 clears running on every CPU and returns (Fact 2 quotes the behaviour, not the lines); the dispatch PC lookup translates with FLAG_INSTR before the fetch (Fact 1, citing cpu_dyntrans.c:670-680); ppc_exception's vector is nr * 0x100 (memory_ppc.c:307-313 passes 0x10/0x11/0x12 for the 603's 0x1000/0x1100/0x1200 vectors); `bad:` parks the CPU and prints UNIMPLEMENTED (BAD block).
UNSETTLED: how the readahead tail saves and restores next_ic; whether cpu_ppc.h names MSR[ME]; whether vga_gfx's last word is reachable as an instruction fetch; what ppc_exception writes to SRR1 for an arbitrary vector number.

PART 4/42
2. THE RULING. The failure arm is entered in FOUR distinguishable states, and the draft treats them as one. I rule each.
R-A, the measured producer: -T, real mode, physical address past RAM plus the 256 KB slack. memory.c has already cleared cpu->running and printed the "non-existant paddr" line. No PowerPC exception exists and none may be invented: -T is a host debugging option of the binary, not guest-visible architecture. Disposition: honor the halt already delivered. Park with next_ic = &nothing_call, return before the decode tail, leave the slot TO_BE_TRANSLATED, leave cpu->pc at addr (already set at 4089), leave SRR0/SRR1 untouched. Menu: 2 DECLINE the fetch. The machine stop belongs to -T and memory.c, not to this arm.

PART 5/42
Warrant for R-A: B measured exactly this. PC 0x02040000 under step and continue, SRR0 sentinel 0x11111111 intact, one "non-existant" line under continue, debugger prompt, exit status 0, a second step or continue changes nothing. CHECKED-IN-PACKET.
Why the bare return (A) is WRONG on R-A: A's PC moved to 0x02040004 under step and to 0x02048140 under continue, and its 8,272 lines name 8,272 distinct addresses. The dispatch loop had therefore advanced next_ic before calling the translator (Astra's reading, now CONFIRMED by measurement). A return that sets nothing makes the loop call the next slot's TO_BE_TRANSLATED, which fails the same way, through the whole batch.

PART 6/42
That is a silent skip-walk, not a live-lock. Two stories are measured false at once: GLM's and Gemini's "same-PC live-lock", and the draft's own "a re-fetch of the same address repeats the exception". A skip-walk is a correctness defect of its own kind, since the guest's PC advances past code that never executed and the CPU reports a halt at the wrong address. A cannot ship.
The probe's 17/17 for A is also evidence about the probe: as frozen it does not separate A from B. See the rows section.

PART 7/42
R-B, defensive and not reached in any session: the translation inside THIS memory_rw raised an ISI or a 603 IMISS (memory_ppc.c:307-323). ppc_exception has then saved SRR0/SRR1, moved cpu->pc to the vector, and redone pc_to_pointers, so next_ic already points at the handler. Disposition: bare return, which is the draft's story and is correct only here. Menu: 5 FAULT, already delivered upstream.

PART 8/42
Reachability of R-B is REASONED unreachable on PPC: the dispatch lookup translated the same PC with FLAG_INSTR under the same MMU state an instant earlier, so a second translation cannot fail (Grok's #6 argument stands). Astra and Gemini are right that the body differs when it does happen. I keep the arm because its test is of observable state and costs one compare: `cpu->pc != addr` is true exactly when an exception moved the PC inside this call. No new field in struct cpu, no invented flag. This settles D4 of the consolidation.

PART 9/42
Corner of R-B: if the failing fetch IS the vector address (IR on, vector page untranslatable), pc equals addr after the exception and control falls to R-C/R-D. Real hardware loops on the same state forever. Acceptable; no special case.
R-C, speculative: cpu->translation_readahead is set. The translator is being called ahead of execution for later slots of the current page. It must touch nothing: no next_ic (that would clobber the live one), no print, no exception. Disposition: return silently, slot stays TO_BE_TRANSLATED so a real fetch re-enters the arm. Menu: 2 DECLINE silently. Astra's #8 was one seat; I adopt it on the argument, which is structural: `bad:` itself returns early under readahead for the same reason (BAD block, CHECKED).

PART 10/42
Reachability of R-C: REASONED reachable only on the device producer. Readahead starts after a SUCCESSFUL translation in the same page. Past RAM every fetch fails under -T or decodes a zero word to `bad:` without -T, so readahead never begins there. On a device page such as vga_gfx's, slots before the last word translate, and readahead walks into 0xc00b7ffc.
Order: R-C must precede R-A's park. Under -T a readahead fetch past RAM would also clear running inside memory.c; parking then overwrites next_ic in the middle of translating a live instruction. That -T-under-readahead halt is a pre-existing wart of memory.c plus readahead, outside this bug (filed as F1).

PART 11/42
R-D, reasoned producer, unmeasured: cpu->running still 1, no exception delivered, not readahead. A device's access function declined an instruction-width read. The census found exactly one: vga_gfx's last word (dev_vga.c:617-618) on prep ibm6050 with -X, fetch at physical 0xc00b7ffc in real mode, no -T. memory_rw.c:595-603 has no PPC exception arm, so HEAD exits. Disposition: the manual's exception for an instruction fetch the bus declines is a Machine Check, vector 0x200. Menu: 5 FAULT. Code: `ppc_exception(cpu, PPC_EXCEPTION_MC)` with `#define PPC_EXCEPTION_MC 0x2` added to cpu_ppc.h, which the packet says has no such constant. SRR0/SRR1 are whatever ppc_exception saves for every other vector; manual-exact SRR1 status bits are NOT claimed. PROVISIONAL: ppc_exception's body is not in the packet.

PART 12/42
Why FAULT rather than an explicit CPU-STOP for R-D, both sides. For a stop: it is honest, measurable by construction, and GLM's "follow the data path" accepts it. Against a stop: the design rule for a CPU core is to raise the architectural exception and never stop the machine; the guest OS may own a machine-check handler (NetBSD/prep does); and a wrong MC is never silent, since ppc_exception prints its "[ PPC Exception ]" line. Against FAULT: it is unmeasured (needs an X11 build), and real hardware with MSR[ME]=0 checkstops, which the arm does not model. I rule FAULT and name it my weakest ruling in section 7.

PART 13/42
Rejected for every arm: falling through to decode the zeroed buffer. memory_rw zeroes ib on failure (#244), so the tail would decode 0x00000000, reach `bad:`, and print "UNIMPLEMENTED instruction" for a word that was never read. That misdescribes the failure, which is consolidation #10's argument; adopted.
Final order of the arms: R-B (pc moved), R-C (readahead), R-A (!running), R-D (running, no exception). R-B first because next_ic is already right and nothing may touch it. R-C before R-A for the clobber in PART 10. R-A before R-D because a cleared running IS the -T halt and must not become an MC the guest never asked for; that is what Gemini's row-5 body would do, and the -T rows' SRR0 sentinel assertion is what catches it.

PART 14/42
3. THE FIX. Replace the failure arm at HEAD 4117-4120 with the following. Every comment is written to be TRUE AS WRITTEN against the packet.

```
		} else {
			if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
			    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
				/*  #NNN: the instruction fetch failed.  This
				    used to be fatal() + exit(1).  Four states
				    reach here; none may run this slot, and
				    the slot stays TO_BE_TRANSLATED.  */
```

PART 15/42
```
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
```

PART 16/42
```
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
```

PART 17/42
Second hunk, src/cpus/cpu_ppc.h, beside PPC_EXCEPTION_ISI and PPC_EXCEPTION_DSI:

```
#define	PPC_EXCEPTION_MC	0x2	/*  Machine check, vector 0x200  */
```

The dead `/*  goto bad;  */` at 4120 goes with the old arm. Nothing else changes: the decode tail, DYNTRANS_TO_BE_TRANSLATED_HEAD at 4130, and the success path are untouched. The slot stays TO_BE_TRANSLATED in all four arms because ic->f is only assigned by the tail, which none of them reaches.

PART 18/42
Comment audit against the draft (consolidation #1, all four seats, adopted in full). Removed: "Return and let the CPU take the exception" (false on the measured route; no exception exists). Removed: the #234 MIPS analogy (that arm follows a delivered exception; ours mostly does not) and "as cpu_arm_instr.c always did" (ARM is fatal then return, cpu_arm_instr.c:4089-4091 per the consolidation, a different disposition). Removed: "a re-fetch of the same address repeats the exception" (A measured a skip, not a re-fetch). grok's v3 one-paragraph comment is true but under-specified: it names only the measured route and does not say why the code does four things. Mine supersedes it.

PART 19/42
Why `cpu->pc != addr` is a safe test (REASONED). Line 4089 wrote cpu->pc = addr immediately before the read, and nothing shown between 4089 and the memory_rw call writes pc. ppc_exception writes pc to the vector (nr * 0x100, with the IP-bit base), inferred from the 603 arms. memory.c's -T path and a device decline do not write pc. So pc != addr holds if and only if an exception was delivered inside this memory_rw, with the single false negative of PART 9. Overturned by any pc write in 4090-4115; none appears in the packet.

PART 20/42
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

PART 21/42
ROW 1, -T step. Session: `-T`, pc=0x02040000, SRR0=0x11111111, step once. Want: process alive, debugger prompt, pc=0x02040000, SRR0=0x11111111, zero "read failed" lines, "non-existant" lines at most 2 (B measured 2; the second is REASONED to be the debugger's own display read, see U5), exit status 0 at quit. Catches W1 (exit 1), W2 (pc 0x02040004), W4 (SRR0 changed).
ROW 2, -T continue. Same session, continue instead of step. Want: pc=0x02040000, SRR0 sentinel, exactly 1 "non-existant" line, zero "read failed", prompt, alive. Catches W2 decisively (A: 8,272 lines, pc 0x02048140). This is the A/B separator (consolidation #9); adopted.

PART 22/42
ROW 3, the halt is stable. After ROW 1 or ROW 2, issue a second step and then a second continue. Want: pc, SRR0 and line counts unchanged, no new "non-existant" lines, process alive. Catches W5. Measured for both A and B ("a second step/continue changes nothing"), so the row also documents that the park does not re-enter memory.c.
ROW 4, text assertions over the ROW 1-3 transcripts. Want: no "UNIMPLEMENTED instruction", no "read failed: TODO", no "[ PPC Exception". Catches W3, W6 (the zero word decodes to UNIMPLEMENTED), W1, W4. Consolidation #10, adopted.

PART 23/42
ROW 5, ISI control, behaviour unchanged. Session: IR on, pc=0x20000000 (a reset-BAT gap), step; then the same under continue. Want: SRR0=0x20000000, pc=0x400, alive, identical to BASE. Catches W7 and freezes Fact 1: this route never enters the arm. Measured identical on BASE, A and B.
ROW 6, no -T control. Session: no -T, pc=0x02040000, step. Want: HEAD's behaviour unchanged. The fetch reads zeros (memory_rw returns success), the zero word reaches `bad:`, the CPU stops with "UNIMPLEMENTED instruction", process alive. Catches an edit that lets the no -T route enter the arm. REASONED from Fact 2; the exact transcript text is frozen from the first run.

PART 24/42
ROW 7, FILED, not runnable in this harness. Session: `-E prep -e ibm6050 -X` on an X11 build with a display, real mode, pc=0xc00b7ffc. Want: alive, running still 1, pc=0x200 (0xfff00200 with MSR[IP]), SRR0=0xc00b7ffc, one "[ PPC Exception 0x2" line, no UNIMPLEMENTED, no exit. Catches W9; with a successful slot at 0xc00b7ff8 and readahead on, also W8 (a clobbered next_ic shows as the wrong pc after the handler's rfi). The producer's reachability is REASONED from the census, so this ships as a filed row marked pending-X11, never as a green row.
Controls: null.out (/bin/true) and nobin.out stay FAIL/ABSENT as in the witness.

PART 25/42
Bound check: nine wrong edits, seven rows plus two controls. Every W has at least one row; W2 and W4 have two; no row exists without a named W. Bound met.
Probe note: A and B both scored 17/17, yet A is wrong. The frozen probe therefore does not separate the skip-walk from the park. ROW 2's pc and line-count assertions and ROW 3 are NEW checks; the md5 must be re-frozen after adding them, and until then "17/17" is not evidence of a correct arm. CHECKED-IN-PACKET.

PART 26/42
5. DISAGREEMENTS SETTLED.
D1 (consolidation #2). "Bare return is a same-PC live-lock" (GLM, Gemini) versus "dispatch advanced next_ic, so it skips" (Astra, Grok). Settled AGAINST live-lock by A's measurement: 8,272 distinct addresses, pc advanced. Both camps agreed the bare return is wrong; only the failure mode was in dispute.
D2 (#3, #4, #5). Park with nothing_call (Astra, Grok; measured as B) versus goto bad (GLM) versus halt or raise MCE/ISI (Gemini). Settled FOR the park on the -T route: B measured pc and SRR0 right; goto bad prints UNIMPLEMENTED for a word never read (BAD block); an exception on the -T route invents architecture for a host option. Gemini's MC survives only for R-D, where it is the manual's answer.

PART 27/42
D3 (#6). "Branch on an exception already delivered" (Astra, Gemini) versus "cannot happen, the lookup fails first" (Grok). Settled BOTH ways: Grok is right on reachability (PART 8), Astra is right that the body differs when it happens. Resolution: a guard on observable state, pc != addr, with a comment that says it is not reached. One compare; nothing true is lost on either side.
D4 (#7). Running still 1: "no skip, no zero-fill, no invented ISI; result open" (Astra) versus "park only when !running, otherwise skip" (GLM). Settled AGAINST skip (W2's defect again) and AGAINST leaving it open: the manual prescribes a machine check for a bus-declined fetch. FAULT, unmeasured (PARTs 11-12).

PART 28/42
D5 (#8). Readahead guard, Astra alone. Adopted on argument, not seats: `bad:` does the same, and the producer is REASONED real on a device page (PART 10).
D6 (#1). Comment rewrite, all four seats. Adopted and extended (PART 18).
D7, the pass-1 split (GLM GO/NO-GO, Grok NO-GO/GO, Astra NO-GO/NO-GO, Argon DRAFTABLE YES/NO). Reconciled: the bug is real and measured (exit 1 on guest input), so the bug review is GO; the draft is NO-GO as written and GO with the four-arm body. No NO-GO on the bug itself cited a measurement; Grok's and Astra's were about the fix shape, which the A/B rows now decide.

PART 29/42
D8. Opus 5.5's reading of the briefs ("the bare return is right only for an already-delivered ISI; it needs a park when running is clear and a silent return during read-ahead") matches R-B, R-A and R-C exactly and is adopted. It did not rule on R-D; this ruling adds it.
D9. grok's DRAFT-WRONG versus the other three's DRAFT-NEEDS-CHANGES is a wording split. The draft's direction survives; its body and comment do not. GO-WITH-CHANGES is the honest label.

PART 30/42
6. UNSETTLED, and what settles each.
U1. R-D's machine check is not measured. Settled by ROW 7 on an X11 build with a display. Until then the arm is PROVISIONAL and the row is filed.
U2. ppc_exception's SRR1 for vector 0x2, and whether it consults MSR[ME]: cpu_ppc.c:318-344 is not in the packet. Settled by reading those lines. If it does nothing MC-specific, the comment "SRR1 status bits are not modelled" is already true.
U3. Whether cpu_ppc.h names MSR[ME], and whether ME=0 should checkstop. Settled by grep; out of scope either way (F2).

PART 31/42
U4. How the dyntrans TAIL saves and restores next_ic and pc around readahead. If it restores next_ic, placing R-C before R-A is merely cheap; if it does not, the order is necessary. Settled by reading the TAIL. The order ships regardless.
U5. Why B shows 2 "non-existant" lines under step and 1 under continue. REASONED: the debugger's display read of the current instruction after the halt. Settled by a transcript diff; ROW 1 asserts "at most 2" so as not to freeze a guess.

PART 32/42
U6. 64-bit PPC and 603-class CPUs: Fact 3 says not established. The 64-bit translation path is itself fatal + exit at memory_ppc.c:279-289 before this arm can matter; a separate defect (F3). The 603's IMISS path enters R-B's story and is REASONED unreachable for the same lookup-first reason.
U7. IR-on fetches whose translation succeeds onto non-existent memory under -T: REASONED to take R-A unchanged (memory.c clears running the same way; pc is the virtual address and stays put). Not measured; a cheap extra row if the probe can program a BAT.

PART 33/42
To FILE as separate rows, not this bug's debt:
F1. memory.c:645-651 under -T halts on READ-AHEAD fetches, which are accesses the guest never made. Either -T ignores accesses made with translation_readahead set, or readahead stops at the end of RAM.
F2. A machine-check model for PPC: SRR1 status bits, MSR[ME]=0 checkstop semantics, and the data side (memory_rw.c:595-603 has no PPC arm for data either; what a device-declined data read returns is UNSETTLED).
F3. memory_ppc.c:268-277 (BAT, "res == 0") and 279-289 (64-bit) are two more fatal + exit arms on guest input, the same hardening class as this bug.
F4. Re-freeze the probe after adding ROWs 1-3's pc and line-count assertions, since the frozen probe passes the skip-walk.

PART 34/42
7. WEAKEST RULING: R-D's machine check. It is unmeasured; its producer is a reading of dev_vga.c; it adds a constant to cpu_ppc.h on the strength of a vector-numbering convention inferred from three 603 call sites; and it does not model ME=0. What overturns it: (i) ROW 7 on an X11 build showing ppc_exception(cpu, 0x2) leaves the guest worse off than a stop, for instance the handler re-faulting on the same fetch forever with no debugger access; then R-D becomes an explicit CPU-STOP with a true message, and the MC moves to F2.

PART 35/42
(ii) A reading of ppc_exception showing it rejects or mis-vectors nr = 0x2. (iii) A reading of memory_rw.c:595-603 showing another architecture's arm already returns success with a defined word for a device-declined instruction read, which would make "return a defined word and decode it" the house convention this fix should follow instead.
Second-weakest: the pc != addr guard (R-B). It rests on no pc write between 4089 and the call and on ppc_exception writing pc; both REASONED from quoted lines. A reachable producer would make the guard load-bearing, which it is built to survive.
Strongest: R-A, measured end to end as B, with its separator rows.

PART 36/42
Counts for the bank.
Rulings (5): R-A disposition, R-B disposition, R-C disposition, R-D disposition, and the order of the arms.
Changes to the draft (5): C1 replace the comment with the four-state comment, no analogies, no ISI story on the measured route (the dead `goto bad` comment goes with it); C2 add the pc-moved guard; C3 add the readahead guard; C4 add the !running park with nothing_call; C5 add the machine-check arm and PPC_EXCEPTION_MC in cpu_ppc.h.
Rows (7): six runnable now (ROWs 1-6), one filed pending X11 (ROW 7). The two existing controls are not counted.

PART 37/42
Dispositions in menu terms, one line each:
- measured -T halt, running already 0: 2 DECLINE the fetch; honor the halt memory.c delivered; park; no exception.
- already-delivered ISI or 603 miss: 5 FAULT already delivered; bare return; guard not reached in any session.
- read-ahead: 2 DECLINE silently.
- device decline with running 1: 5 FAULT, machine check 0x200; PROVISIONAL pending ROW 7.
Not chosen anywhere: 1 DELETE (the arm is needed); 3 announce-once (memory.c and ppc_exception already print what there is to say); 4 and 6 ACCEPT (a fetch that failed must not yield a word); 7 IMPLEMENT (a full MC model is F2).

PART 38/42
What the fix does NOT claim, so the bank does not over-read it: it does not make -T on PPC equivalent to other architectures' -T handling (unexamined); it does not touch memory.c, memory_rw.c or the dyntrans TAIL; it does not change what a guest sees on any route that does not already end the process at HEAD. On every session measured in the packet (ISI route, no -T zero-word route, null and nobin controls) the fixed binary must be byte-identical in transcript to BASE, and ROWs 5 and 6 assert that.

PART 39/42
Note for the parallel Mythos 5.1 adjudication of the share-findings and route A. This ruling independently reaches the two conclusions the consolidation reports as consensus (the draft comment is false; the bare return does not finish the -T halt) and rules the three items it reports open: D2 for the park on -T, D3 (running still 1) for a machine check pending measurement, D4 for a state-based guard rather than a flag. If the Mythos ruling lands on a CPU-STOP for running-still-1, the two rulings differ only on R-D, and ROW 7 is the tiebreak.

PART 40/42
Dependence on omitted text, named as required. Section 5's attributions (who asked what) rest on grok's consolidation, not on the seats' own words; the omitted 75 KB could move an attribution, not a measured ruling, because no seat's text outweighs the A/B rows. One exception: if any omitted brief contains a MEASUREMENT of a running-still-1 producer, R-D must be re-read against it before the bank accepts this file.

PART 41/42
Reviewer checklist for the committer, in order: (1) apply the two hunks; (2) build; (3) run ROWs 1-6 and both controls; (4) add the pc and line-count assertions and re-freeze the probe md5; (5) read cpu_ppc.c:318-344 and the dyntrans TAIL to close U2 and U4, and record whether anything in the comment became false (none expected); (6) file F1-F4 and ROW 7 as separate rows; (7) ship. Any red in step 3 returns the design here, not to the draft.

PART 42/42
Bank as regress/artifacts/qhslowifetch/adj_20261104/FABLE_FINAL.md.
CLOUDFINAL qhslowifetch: 5 RULINGS 5 CHANGES 7 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS
