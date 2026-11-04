# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 16:56:09Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-teleport-579m/8388f0dd-ce39-4b0c-9ae5-415510ac3e2f.jsonl`
* session: `https://claude.ai/code/session_015fEQzFPnoHuopQfimJgsQM`   trigger: `trig_01XDZS9bvZWZAxFcQBTfhfBM`   packet: `_scratchpad/mythos_20261104/packet_ppcllscrcexit_F2R_MYTHOS.md`
* the answer's message: timestamp 2026-11-04T16:53:21.296Z, model field `claude-mythos-5-1` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-mythos-5-1'])
* delivery token `MYTHOSF2R_PPCLLSCREXIT_579`: present; 25980 characters; PART markers N = 40, present 40, MISSING none; `END OF PARTS`: YES
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDF2R ppcllscrcexit #579: 25 RULINGS 21 FIX-IN-ROUND 7 FILED 5 REJECTED VERDICT:SHIP-WITH-CHANGES

---
PART 1/40
MYTHOSF2R_PPCLLSCREXIT_579
model: claude-mythos-5-1 (the configured id; the serving model may differ)
Evidence basis: six answers from the five seats on the 2026-11-04 roster (Opus 5.5 read-only, Grok 4.7, GPT-6 Astra twice, GLM 5.3, Gemini Argon), 5 of 5, so this ruling is not PROVISIONAL for seat absence. Fable is held; this seat rules in its place. §4d (the probe source) is omitted: F10, F11, F19 and the docstring wordings give replacement phrases whose exact old text sits in ppc_llsc_probe.py, and I say so where it matters. Argon's blanket 25 upholds add no argument and weigh as none.
Stage verdict: SHIP-WITH-CHANGES. The code is right (F1). 21 rulings fix comments, records or the probe in-round, 4 are INFO, 7 outside items are FILED, 5 proposed texts are REJECTED and replaced.

PART 2/40
Method applied. Every claim is tagged CHECKED-IN-PACKET (walked in the inlined text), REASONED (follows from inlined text plus a seat's quoted file read, or from my own reading) or UNSETTLED (names what settles it). Arithmetic was enumerated, not taken from totals: every table-4 score reconciles to its red list (M1 17 reds = 66, M2 16 = 67, M3 36 = 47, M12 12 = 71, M9 7 = 76, M10 8 = 75; the pre-fix witness 33 reds = 50/83). Final-line counts: FIX-IN-ROUND = rulings whose L1-L4 edit is applied before commit; FILED = outside-round items given a queue note; REJECTED = proposed texts or conditions overturned (each replaced inside a fix-in-round ruling); INFO rulings are counted in none of the three.

PART 3/40
F1 — UPHOLD, INFO, no code change. CHECKED-IN-PACKET. Diff 2a removes `rc` from the declaration (:2279) and both guards; AFTER:2276-2383 has no remaining use of bit 0 of `iw`. Load path: memory_rw failure returns (:2311-2317), else the value is assembled and gpr[rt], ll_addr, ll_bit=1 are written (:2328-2330). Store path: old_so captured first (:2332), value read (:2345), reservation miss clears CR0 and copies SO (:2351-2356), store failure returns (:2366-2372), success sets 0b001 plus SO and clears every CPU's ll_bit (:2374-2381). Register extraction (:2296-2298) and the decoder are untouched. All five pass-2 seats and all six F2 answers agree.

PART 4/40
F2 — REFINE, L4 (a comment in product source). CHECKED-IN-PACKET: the shipped sentence at AFTER:2340-2341 says "returns below" (plural) but only one #216 return sits below it (:2368-2371; the load one at :2313 is above — C.3). REASONED from Astra-f2b's quoted memory_rw.c:603-611 (the failure branch raises under MEM_MIPS and M88K only) and the seats' reads of core/memory.c:645-651 and memory_ppc.c:307-313: a failed PPC access may have raised a DSI, a 603 TLB-miss interrupt, stopped the CPUs, or raised nothing. The PROPOSED reword ("has already raised whatever exception or stop applies") still asserts something was raised — REJECTED (Opus, Grok, Astra x2, GLM).

PART 5/40
F2 replacement, exact text for AFTER:2340-2341, replacing "The #216 returns below stay: they follow a DSI memory_rw has already raised.":
"The #216 return below stays: it follows a failed memory access, after which the memory path may already have raised an exception or stopped the CPUs, or raised nothing at all (a failed device access raises no PPC exception); this handler adds nothing either way."
The older #216 comments at :2313-2315 and :2368-2370 carry the same "raised a DSI" universal. They predate this diff and are FILED to #216's ledger row (section 4), not edited here, so this round's record claims no audit of them.

PART 6/40
F3 — REFINE, L4. REASONED (Astra, GLM P3; Astra-f2b confirms by file read): ppc_exception() multiplies the number by 0x100, so "no Program vector" overstates; what is absent is a Program-interrupt constant and an illegal-instruction SRR1 cause bit. Keep ", and none is required" — it is the warrant (Book I 1.9.2, either outcome permitted) and the PROPOSED text dropped it. Drop the cpu->pc clause: a separate pre-existing limitation (Astra-f2) that would go false when a pc-sync row lands (Opus). Replace AFTER:2338-2339 "ppc_exception() has no Program vector and no illegal-instruction cause bit, and none is required." with:
"this core defines no Program-interrupt constant and sets no illegal-instruction cause bit in SRR1, and none is required."

PART 7/40
F4 — UPHOLD, L4 (ruling record and round block). CHECKED-IN-PACKET: the removed store guard (diff 2a) exited before `value = gpr[rt]`, so "computes the right value and then discards it" (member 4) is false of it.
D2 — REFINE. The menu's text is not in the packet, so a member number is UNSETTLED here (settled by the menu file); Opus's DELETE (member 1) may fit mechanically, but a number carries no warrant. Record in words: "the guard is deleted and the core executes the defined store-conditional, CR0 update included — a permitted outcome of the invalid form (Book I v2.01 1.9.2); the illegal-instruction outcome is unavailable on this core and not required." A number may be appended by whoever holds the menu; it must not replace the sentence.

PART 8/40
F5 — UPHOLD rows `rc1 resv bytes` / `rc1 resv cr`, L1 (applied). CHECKED-IN-PACKET: M17 77/77 (table 3), then 81/83 red on exactly those two rows (table 4). Warrant REFINED: clause (d)'s text is not inlined (UNSETTLED as a label), and the warrant does not need it. M17 is the removed predicate re-introduced (`ll_bit = !(iw & 1)`), and the shipped comment at AFTER:2307 claims the bit-set form "runs this one body"; a reservation it never creates falsifies that comment. A row that pins a shipped comment's own claim is inside the DEPENDS-ON bound. Grok's "sibling parity with stw ok / noresv" is a second warrant, not a competing one; Grok is right that M17 re-introduces no process end, so write "the removed predicate re-introduced", not "(d)".

PART 9/40
F5 row, as the record should carry it: `rc1 resv` — lwarx with bit 31 set, then stwcx. to the same address; want: the store lands (bytes) and CR = 0x2fffffff; detects M17, where the store does not land and CR0 reads 0b000.
F6 — UPHOLD rows `nso bytes` / `nso cr`, L1 (applied). CHECKED-IN-PACKET: M18 77/77, then 82/83 red on `nso cr`; `nso bytes` cannot vary under M18 (nothing is stored either way) and is red under M12 (table 4), so it is not a dead row. Warrant: the ruling's own `sc-so` asked for both outcomes and the docstring claimed the SO copy — an obligation of this round (L3 shape) discharged by an L1 row. Row: stwcx. with no reservation and XER[SO] set; want nothing stored, CR = 0x1fffffff; detects M18 (CR = 0x0fffffff).

PART 10/40
F7 — UPHOLD rows `rc0 nr bytes` / `rc0 nr cr`, L1 (applied). CHECKED-IN-PACKET: M21 81/83, red on exactly those two rows. In bound by the same rule as F5: the shipped comment at :2336-2337 says the bit-clear word "performs the defined store-conditional, the CR0 update below included"; skipping the reservation test for bit-clear words is the removed predicate re-introduced on the store side. Row: bit-clear stwcx. with no reservation; want nothing stored, CR = 0x0fffffff; detects M21 (the store lands, CR0 0b001). Record: M21's 77-row undetection is a prediction, not a measurement (no 77-row session runs a bit-clear stwcx. without a reservation); the packet states it as one — keep that wording.

PART 11/40
F8 — UPHOLD, INFO. CHECKED-IN-PACKET: M19 75/77 red on `twice bytes` / `twice cr`; 81/83 the same two rows. Closed by rows added after pass 2.
F9 — UPHOLD INFO; REJECT the conditional "FILE only if a seat argues it is in-bound" (Astra: backwards; GLM: leave it untriggered). CHECKED-IN-PACKET: M20 83/83 undetected; the deleted return is the #216 load-side return at :2316, which the diff shows as context, not as a change, so it is outside this round's DEPENDS-ON bound and a filter may not demand a row for it. Replace the clause with: "the #216 returns in X(llsc) have no detecting variant in this instrument (M20 83/83); this round verifies nothing about them." FILE a one-line note to #216's ledger row (section 4); no new row for #579.

PART 12/40
F10 — UPHOLD as L1, REFINE the repair. CHECKED-IN-PACKET (section C's measured table): as shipped the census row prints "0/0 ok" on /bin/true and on a missing binary — a MEASURED FALSE PASS of a row, caught before the detector ships. Repair A (count words placed, `neg` included) reds a correct build (35/36 FAIL, CONTROL=FAIL) — REJECTED, as Grok and Astra predicted. Repair B (count words placed, the bogus-machine `neg` session excluded) gives 35/35 on the correct build, 0/35 FAIL on both null media, RESULT 14/83 and 0/83, with a 0-byte diff in the build outputs; replicated by a second Opus seat. Apply B exactly as measured (its text is in `_scratchpad/opus_census579/`; the probe source is omitted §4d). The gate's 35/35 and 83/83 pins are unchanged; its null-medium pins never matched, so nothing is re-pinned.

PART 13/40
F10, record edits in the same commit: (1) the docstring's "passes 15 rows" → "a non-emulator binary passes the 14 exit-status rows; an absent binary passes none"; (2) the comment at ppc_llsc_probe.py:158 ("every row fails" for an absent binary) is false as shipped (NOBIN 1/83) and true under B — keep it, but only because B lands first in the order below; (3) table 4's NULL4 15/83 and NOBIN4 1/83 go stale — re-run both null legs with the repaired probe and record 14/83 and 0/83 as a dated table-4 addendum, or cite the Opus census table as that measurement; (4) the `neg apparatus` row (F21) is unchanged by B: it wants exit1/none and is excluded from the count, not from the probe.

PART 14/40
F11 — UPHOLD, L4, REFINE the list. Disclose in the docstring: "RA is 0 in every session but `lw ra`; RT is 3 but for `lw ra`; two of eleven CPU models; one privilege level; one CR seed; two XER seeds (SO clear, SO set)." Astra's XER count replaces the packet's "one CR/XER seed". Astra's point that narrowing only the RA mask to four bits is undetected (RA never exceeds 15) is REASONED from the sampling and goes in as a coverage limit, not a row: :2296-2298 are untouched by the diff, so no row is owed. Which field M16_mask15 narrows is UNSETTLED from the packet (the variant source settles it); it reds `ra value`, so it is not the RA-only narrowing Astra describes.

PART 15/40
F12 — UPHOLD, L4 brief defect, recorded. CHECKED-IN-PACKET: KEY:4652 and ARM:4904-4910 are the working-tree lines; the pass-2 brief's pre-diff cut is a record defect only, already corrected by this packet.
F13 — UPHOLD the correction (":2354 after" → :2355; CHECKED: AFTER:2355 is `ll_bit = 0` on the failure path) and add a second L4: the packet's "APPLIED in FABLE_ADJ.md" was a WRONG RECORD (C.1: 2354 and 2355 occur 0 times there). Apply now: write :2355 into the round block, change the "APPLIED" line to "applied 2026-11-04 under MYTHOS_F2R", and leave the HEAD :2346 citations alone (they address the pre-diff file).

PART 16/40
F14 — UPHOLD the finding; REJECT the proposed wording ("other instructions" is a new unverified claim — Opus, Grok, Astra, GLM). CHECKED-IN-PACKET (C.4): the v2.01 extract has no entry for 31/532 or 31/596 while 31/533 and 31/20 each have two, so the zero is real. Opus's Appendix G reading (unused opcode-31 XOs are illegal) is REASONED, not inlined; the shipped text stays within what the grep checked. Replacement for the docstring sentence:
"the XOs 532 and 596 (20 and 84 with XO bit 9 set) are unassigned in Book I v2.01 and this decoder sends them to `goto bad`; they are not this handler's words. The later architecture's hint is bit 31 of XO 20/84, which `lw rc1` / `ld rc1` already run."

PART 17/40
F15 — UPHOLD, L4. CHECKED-IN-PACKET: NULL 15/77 and 15/83, NOBIN 1/77 and 1/83. Replacement for FABLE_ADJ.md section 5:
"Null medium: no emulator, no prompt — every value, bytes, CR, pc and seed row fails; the exit-status `session` rows and (until the census repair) the 0/0 census pass: /bin/true 15/83, a missing binary 1/83 (14/83 and 0/83 after repair B). RESULT, pinned by equality, and CONTROL=FAIL reject both."
Grok's PRETABLE.out:38 carries the same false sentence — covered by the errata file under F18.
F16 — UPHOLD, L4: delete "doubles the detector" from ground 3. REASONED (Astra: the same eight classes either way; section 3 is not inlined, but deleting an unsupported clause cannot make the record false). Grounds 1 and 2 stand.

PART 18/40
F17 — UPHOLD, L4, with the enumeration. CHECKED-IN-PACKET at AFTER:2283-2294: the STWCX_DOT arm is `break` alone; a stwcx. word that matches no label leaves load=0, len=4 — the same state — so re-keying that label alone is equivalent and no row can red it. The other three labels set state and each has a detecting variant in table 4: LWARX (load stays 0 → M4, 75/83), LDARX (len stays 4 → M5, 81/83), STDCX_DOT (len stays 4 → M6, 81/83). Narrow (d) to: "a case label re-keyed among those whose arms set `load` or `len` (LWARX, LDARX, STDCX_DOT)". For the record only: the STDCX_DOT arm falls through to STWCX_DOT without a fall-through comment, unlike LDARX at :2286 — pre-existing, DROP.

PART 19/40
F18 — UPHOLD, L4 erratum beside PRETABLE.out (the file is not edited; its mtime is the order proof). One file `PRETABLE.errata.md` beside it, two lines:
"PRETABLE.out: 'the store arm has a reservation state the load arm has not' — wrong: the load arm creates it (AFTER:2329-2330); the store arm consumes it (:2351)."
"PRETABLE.out:38: 'the null medium fails every session' — wrong: /bin/true passed 15/77 and 15/83 (14/83 after repair B); a missing binary 1/77 and 1/83 (0/83 after B)."
F19 — UPHOLD, L4 (old text in omitted §4d): replace "the session ran to `quit'" with "the session's exit status was 0 (`exit0` proves the status, not that `quit` ran)".

PART 20/40
F20 — UPHOLD, L4. Round block: "every fixed row demands the value, the bytes or the CR" → "every fixed form's row group demands the value, the bytes or the CR; its `session`, `pc` and `seed` rows carry the exit status, the program counter and the seed".
F21 — UPHOLD, INFO. The `neg apparatus` row wants exit1/none; a dead medium satisfies it by the negative control's own shape; RESULT and the `session` rows carry the red (CHECKED: NULL 15/83 with CONTROL=FAIL). Unchanged by repair B (part 13).

PART 21/40
F22 — UPHOLD INFO (no row dropped); REFINE the count, L4. CHECKED-IN-PACKET by enumeration: M4, M5 and M6's red lists are subsets of M3's 36 names; M7 adds the four `tail` rows (stw ok, stw rc0, sw32 ok, sw32 rc0), so the M3-M7 union is 40 and the rows that cannot vary under the routing/width edits number 43, not 40 (Grok and Astra, independently; C.2 agrees). Write "43" and name the set as "the complement of the M3-M7 red union". The packet's list ("apparatus, session, pc, seed and three no-store bytes rows") undercounts: at 83 rows there are four no-store bytes rows (noresv, mismatch, nso, rc0 nr), and the list should not be reused.

PART 22/40
D1 — UPHOLD, with two refinements. CHECKED-IN-PACKET: the definition is the LEFT column of BOOKI:451-458; the right column is a Programming Note on reserved bits in System Registers, interleaved by the two-column extract — an enumeration hazard, so the record should quote the left column alone. A single valid stwcx. is "an arbitrary finite sequence of instructions (none of which yields boundedly undefined results)" executed from the prior state, so the defined operation is inside the bound; that settles the store-pair warrant. The empty-sequence point (doing nothing is inside the bound) is REASONED, not quoted, and nothing in the core rests on it; the record should say so (GLM's point).

PART 23/40
D1, the L3 addition. The shipped comments at :2305-2307 (bit 31 reserved on lwarx/ldarx, ignored by the processor) and :2333-2336 (bit 31 "1" on stwcx./stdcx.; invalid-form outcomes) rest on four extract lines the packet never inlines — GLM names them: Book II :1264, Book I :432-433, Book II :1305-1307, Book I :1116-1120. The F2 pass verified code against probe (measured) but probe against architecture only by citation convergence. My own reading of the PEM layouts agrees (REASONED): lwarx X-form bit 31 is "/", stwcx. bit 31 is "1". Obligation: the main loop inlines those four lines into the round block before commit (four sed calls); if any does not say what the comment claims, HOLD. This is the one place a ruling of mine can hold the round, deliberately.

PART 24/40
D3 — REFINE. CHECKED-IN-PACKET: ARM:4904-4910 lists all four XOs with no width test, and KEY:4651-4653 has none at the case head; three file-reading seats (Grok, Astra, Opus) read none elsewhere. That is a READ claim about decoder text, not a measurement: the 32-bit leg runs XO 20/150 only (`lw32` / `sw32` rows), so the instrument does not touch it. GLM's objection to "Grok settles it" is upheld as to the word. Record: "read by three file-reading seats (no width test at :4651-4653 or :4904-4910), not measured by this instrument; the 32-bit ldarx/stdcx. forms are disclosed as #571 left opcodes 58/62". The shipped comment at :2341-2343 states an open question and is true as written; no change. A measurement, if wanted, is #571's (FILED, section 4).

PART 25/40
Section 3 — the open items, cross-referenced. F2/F3/F14 wordings: parts 4-6 and 16 (F2 and F14 proposals REJECTED and replaced; F3's proposal true today but REFINED to keep the warrant and drop the pc clause). The census repair and its `neg` exclusion: parts 12-13 (B, not A). The F5/F7 warrant: parts 8 and 10 (the removed predicate re-introduced against a shipped comment's claim; "(d)" struck). F9's filing condition: part 11 (struck; note to #216). F11: part 14. The errata: parts 17 and 19 (one file beside PRETABLE.out; FABLE_ADJ.md corrected in a dated addendum, not silently). D2: part 7 (words). D3: part 24 (read, not measured).

PART 26/40
Section 3, the docstring wordings not yet ruled (all L4; old text in omitted §4d; C.5 confirms one match each):
- "one or two" words per session → "one to three words per session (`stw chain` and `stw twice` place three)".
- "differ in every byte" → "the 4-byte and 8-byte patterns differ in value; they share their first four bytes".
- the load comment's "valid form" (AFTER:2305-2307): no comment change. The warrant lines (Book I reserved-field rule, Opus :1110-1112 and GLM :432-433; Book II :1264) go into the round block under the D1 L3 item. A section number goes into the comment only if the main loop reads it from the extract; a scratchpad line number never does.
- the absent-binary comment at :158: part 13 (true once repair B lands, so B lands first).

PART 27/40
Section 3, two wordings the seats flagged in the packet itself. "The #216 returns below" (plural, C.3): fixed by the F2 text in part 5. F13's "APPLIED": part 15. One more the record should carry: the packet's F7 line "NOT measured against the 77-row probe ... stated as a prediction" is correct and stays; the packet's F5 line "clause (d)'s shape for a deletion" is replaced by the part-8 warrant. And the F2 packet's section 1 says "all sixteen test variants red" for table 2 — CHECKED-IN-PACKET, M1-M16 each below 77/77; true as written.

PART 28/40
Section 4 — outside the round, one line each:
1. Older #216 comments at :2313-2315 and :2368-2370 ("raised a DSI" universal) — FILE to #216; not edited here.
2. The #216 returns have no detecting variant (M20 83/83) — FILE a note to #216.
3. 32-bit ldarx/stdcx. delivery (D3) is read, not measured — FILE to #571's disclosure.
4. Opus: the 0x87c0ffff SRR1 mask drops MSR's upper half on 64-bit CPUs — FILE, UNSETTLED (settled by cpu_ppc.c:318-339 and the MSR width per model).
5. Opus: the reservation compares effective addresses (:2329, :2351) where Book II compares real addresses — FILE, pre-existing.

PART 29/40
Section 4, continued:
6. Grok: MODE32 `reg()` on a big-endian host reads the high half of gpr[rt] — FILE, pre-existing, UNSETTLED here.
7. X(llsc) never synchronises cpu->pc before an exception could be raised — FILE if no row exists (Opus named `ppcllscsrr0`; UNSETTLED whether that row is in the queue).
DROP: the missing fall-through comment on the STDCX_DOT arm (cosmetic, pre-existing); Opus's device-handler-stops-CPU path as a separate item (absorbed into the F2 text, "stopped the CPUs"); extra CPU models and privilege levels as rows (disclosure only, F11); GLM's four citations as an outside item (they are the in-round L3 of part 23).

PART 30/40
Section 5 — the weakest ruling is F2's replacement sentence (part 5). Its truth rests on memory_rw.c:603-643 and core/memory.c:645-651 as read by seats; the packet inlines only :603-611. What overturns it: a PPC branch in the failure path between :612 and :643 (an `#ifdef MEM_PPC` that raises a DSI there). Then "a failed device access raises no PPC exception" is false, the parenthetical goes, and the sentence stays true without it. Settle it before the comment ships with: sed -n 603,643p src/cpus/memory_rw.c (the GXEMUL-SEC tree, not the pristine copies).

PART 31/40
Section 5, the second weakest: the D1 L3 item (part 23), which can HOLD the round on four sed lines. What overturns it: the lines say what the comments say — then it costs four quotes and nothing else. I keep it because the whole fix's warrant is those lines, no seat quoted them, and the brief's own warning (seven of nine seats confirming a wrong premise) is about exactly this shape: everyone verified the derivation (code vs probe, measured) and nobody verified the premise (probe vs architecture). Third: F5/F7's in-bound warrant (parts 8, 10) rests on my rule that a row pinning a shipped comment's claim is in the bound; the DEPENDS-ON text is not inlined, and if it excludes comment claims, those rows keep their L1 status only as pre-ship construction (the packet's own class), which the verdict does not depend on.

PART 32/40
Section 6 — STAGE VERDICT: SHIP-WITH-CHANGES, applied in this order.
1. Record checks first: inline the four Book I/II extract lines (D1 L3, part 23) and memory_rw.c:603-643 (part 30) into the round block; HOLD if either disagrees with the comments as ruled.
2. cpu_ppc_instr.c comments only: the F2 sentence at :2340-2341 (part 5) and the F3 clause at :2338-2339 (part 6), exact texts as given. No executable change. Rebuild and re-run the 83-row witness on the build-tree binary (expect 83/83, CONTROL=OK).

PART 33/40
3. Probe: repair B (F10, part 12) and the docstring edits — F11 (part 14), F14 (part 16), F19 (part 19), "one to three words", "differ in value", "14 / none" (parts 26, 13); the :158 comment kept. Run the correct build (expect 83/83, census 35/35 ok) and both null media (expect 14/83 and 0/83, census 0/35 FAIL, CONTROL=FAIL). Re-run gate 13 (pins 83/83 and 35/35 unchanged; expect PASS, 290 checks).
4. Round block: the F4/D2 sentence (part 7), the F5-F7 warrants and rows (parts 8-10), the F9 clause replaced (part 11), :2355 (part 15), F20 (part 20), "43" (part 21), the D1 left-column quote and empty-sequence note (part 22), the D3 "read, not measured" record (part 24).

PART 34/40
5. FABLE_ADJ.md: a dated addendum section (not silent edits) carrying the F13 "APPLIED" correction (part 15), the F15 null-medium text (part 17), the F16 deletion (part 17) and the F17 narrowing (part 18).
6. `PRETABLE.errata.md` beside PRETABLE.out with the two F15/F18 lines (part 19); PRETABLE.out untouched.
7. A dated table-4 addendum with the repaired null legs (14/83, 0/83) or a citation of the Opus census table as that measurement (part 13).
8. File the seven section-4 items (parts 28-29) as queue notes with their warrants.
9. Commit.

PART 35/40
Ruling tally, F1-F22. INFO (4): F1, F8, F9, F21. FIX-IN-ROUND (18 of the 22): F2 L4, F3 L4, F4 L4, F5 L1, F6 L1, F7 L1, F10 L1, F11 L4, F12 L4, F13 L4 (twice), F14 L4, F15 L4, F16 L4, F17 L4, F18 L4, F19 L4, F20 L4, F22 L4. None of the 22 is FILED instead of handled; the filed items are the outside-round notes of section 4.

PART 36/40
Ruling tally, D1-D3. FIX-IN-ROUND (3): D1 (record refinement plus the L3 inline), D2 (L4, the sentence in words), D3 (L4, "read, not measured"). Total FIX-IN-ROUND: 21. REJECTED proposals (5), each replaced inside one of those rulings: the F2 proposed text, the F14 proposed text, F9's conditional FILE clause, census repair A, and D3's "Grok settles it". FILED outside-round items: 7 (section 4, items 1-7). DROPPED: 4 (part 29).

PART 37/40
Two notes for the record that are not rulings. First, the compact packet omitted §4d; every replacement phrase I gave for the probe (F10's "14 / none", F11, F14, F19, "one to three", "differ in value") must be matched against the file's actual sentence before it is applied, and C.5's "1 match each" says the first two of the docstring items will match. Second, the F2 packet's own F7 line already records M21's 77-row undetection as a prediction; nothing in table 3 contradicts F5, F6, F8 or F9 — M17, M18, M20 at 77/77 and M19 at 75/77 are exactly as predicted, and table 4 closes M17, M18, M21 on exactly the rows added for them.

PART 38/40
A reader who sees only this ruling: the executable fix in X(llsc) is correct and ships unchanged. What changes before commit is prose and the probe: two comment sentences in the handler that overclaimed what the memory path raises and what ppc_exception() lacks; a probe census row that passed on an empty medium; a docstring with a wrong encoding claim and undisclosed sampling; and several record lines (a wrong "APPLIED", a wrong count of 40, a wrong member label, a wrong "settles it"). One record obligation can still hold the round: quoting the four architecture lines the comments rest on.

PART 39/40
Final counts, as defined in part 2: 25 rulings (F1-F22, D1-D3); 21 FIX-IN-ROUND; 7 FILED outside the round; 5 REJECTED proposed texts or conditions, all replaced; 4 INFO. Verdict SHIP-WITH-CHANGES in the order of parts 32-34, with the HOLD trigger in step 1.

PART 40/40
CLOUDF2R ppcllscrcexit #579: 25 RULINGS 21 FIX-IN-ROUND 7 FILED 5 REJECTED VERDICT:SHIP-WITH-CHANGES
END OF PARTS
