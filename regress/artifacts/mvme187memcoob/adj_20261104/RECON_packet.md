Begin your answer with the token CLOUDRECON_MEMC on its own line, then `model: <your model name>`, then your verdict line.  Do not
call any tool and do not write files; answer in plain text.

# RECONCILIATION -- `mvme187memcoob`: your two final rulings on the same packet (Claude Code Cloud; Fable 5.1)

**Framing.**  GXemul is a computer-architecture emulator (a developer tool that runs legacy operating systems in a software sandbox); this fork
is a software-correctness hardening effort, and every fix ships with a regression test.  Plain correctness language, please.

**What happened.**  You gave the final design ruling on this bug twice, from the same packet, in two independent Claude Code Cloud runs: r1
(the ruling of record) and r2 (a replication).  Their verdicts agree; their change and row lists differ.  The main loop implements ONE fix and
ONE row list, and it records and does not rule -- so the reconciliation is yours.  Below are the whole ruling (its section headings did not parse) of r1 and sections 2-4 (the ruling, the fix, the rows) of r2.  You have no
repository: cite the rulings' own items; mark claims CHECKED-IN-PACKET, REASONED or UNSETTLED.

**Answer, VERDICT LINE FIRST (`VERDICT: R1-STANDS | MERGE | R2-SUPERSEDES`), in this order -- keep it compact; code only where it changes:**
1. Every difference between r1 and r2 (disposition, code, comment sentence, row, filed item), one line each, citing each ruling's item.
2. For each: OWED (r1 is wrong or incomplete without it -- quote the r1 sentence), OPTIONAL (wording, or a row another row already covers --
   name it), or WRONG (quote the line it contradicts).  Where they CONFLICT, both sides in a line and which argument is stronger and why.
3. THE MERGED FIX: the exact final code for every hunk that differs from r1's, every product comment TRUE AS WRITTEN; say "r1 as written"
   for each hunk that does not change.
4. THE MERGED ROWS: the final row list (session, guest action, want, the wrong edit each catches), within "rows per enumerated wrong edit".
5. The weakest of these reconciliation rulings, and what would overturn it.
Final line: `CLOUDRECON_MEMC: <d> DIFFERENCES <o> OWED <c> CONFLICTS <r> ROWS VERDICT:<R1-STANDS|MERGE|R2-SUPERSEDES>`

---

## r1 -- the ruling of record (FABLE_FINAL.md)

```
CLOUDFINAL_MEMC_20261104
model: claude-fable-5-1
Evidence basis: CHECKED-IN-PACKET = the HEAD listing of dev_mvme187.c and the memcreg/MACH summaries (B), the rung-3 witness with ASAN fact 1 (C), the Opus 5.5 A1/A2/A3 measurement and its fatal()-returns and memset findings (D), grok's consolidation with per-change seats (F). NOT in hand: the header text, the probe script, the build flags, any manual page, any 187Bug or OpenBSD run, the full seat readings (Astra's manual quote, Argon's truncated file). Rulings resting on those are marked PROVISIONAL.
VERDICT: GO-WITH-CHANGES. The draft's bound is right and measured. It ships after 7 changes and owes 6 rows, one per enumerated wrong edit, ASAN leg included.

Evidence basis, continued. Omitted text my rulings would touch: (1) Astra's manual sentence "Writes to this register are ignored" was not re-read, so the memconf ruling does not rest on it. (2) Argon's DRAFT-STANDS is truncated and carries no argument I can count. (3) The header's bit names are not quoted; I use only what B gives: RTOB(x) = 4 MiB << (x & 7), 31 byte registers at 4-byte stride, 124 bytes. Three facts I use are REASONED from B rather than seen in full source: nothing stores into the struct except DEVINIT (the memconf arm exits before any store, the default arm exits, 0x00/0x04 have no store); the switch arms are the only readers besides line 68; GXemul treats a 0 return from an access function as a bus fault to the guest, which is what menu item 5 FAULT means.

RULING 1, the bound. Disposition: the handler performs NO indexed read of the register image at all. The draft moves the read into the served arms; I go one step further and split case 0x00 and 0x04 into field reads, so the pointer cast disappears from the file. Warrant: relative_addr after the fold is 0..0xff (CHECKED-IN-PACKET, lines 63-68); the image is 124 bytes; HEAD's line 68 is an out-of-bounds read in the C source for 0x7c..0xff. ASAN fact 1 and A1 show the read can be elided when its value is dead, A2 shows it goes live at line 68 the moment the exit is removed and the byte is forwarded (CHECKED-IN-PACKET, D). A bound that depends on what the optimizer drops is not a bound. With field reads per arm the invariant is inspectable by eye and holds at every -O level. Behaviour is identical to the draft (A3 values unchanged).

RULING 2, memconf write at 0x08: DECLINE, no store, once-latched announce (menu 3). NOT "ACCEPT idata & 0x07". Warrant: the model's byte is the size code: DEVINIT computes r so that RTOB(r) fits RAM/2 and stores r (CHECKED-IN-PACKET, 115-125). Bits 0-2 are precisely the bits a store must not alter, because the register exists to report the installed size; storing idata & 0x07 would let one guest store make the register lie about RAM. So that option masks in exactly the wrong bits. Whether real hardware ignores the write (Astra's manual line) is UNSETTLED and not needed: a model whose only content is the size code has nothing writable to model. GLM's read-back-compare worry is answered by row R3, whose once-notice would show a real guest storing; no such guest is in evidence (no 187Bug run). PROVISIONAL on the manual only for the announce wording, not for the decline.

RULING 3, the value an unimplemented read returns: 0, with return 1 (menu 3), not the struct byte, not FAULT. Warrant: in this tree every byte of the image other than chipid, chiprev and memconf is 0 and stays 0: DEVINIT memsets the struct and assigns only those three; no store path exists (REASONED from B, every arm). So for in-range unserved offsets 0x01..0x7b "the struct byte" and "0" are the same number; the dispute Gemini raised has no measurable content, and the constant is the one that stays true after any later store is added. For 0x7c..0xff there is no struct byte. The old code never delivered any byte to the guest (it exited before the tail; memory_rw.c zeroes the buffer anyway), so no guest contract is broken by 0. FAULT has no evidence behind it: nothing in the packet says the chip fails to respond inside its window; declining keeps the guest running, which is the hardening goal.

RULING 4, the announce and its latch grain: two latches, one per category (memconf write, unimplemented offset), once per device instance, spanning both controller aliases. Warrant: the latch is a noise bound, not a log; the notice names the offset and controller, so the first line carries what a reader needs. A per-slot latch (Grok withdrew it) adds 256 bits of state to bound a line that costs nothing. Astra's "once per category per shared allocation" is what the draft already is, since the struct is one allocation. The latch fields start at 0 because DEVINIT memsets the whole struct (CHECKED-IN-PACKET, line 108), so GLM's explicit zero is unneeded. fatal() returns (CHECKED-IN-PACKET, debugmsg.c:384-391 via the Opus seat), so it is a fit announce; GLM's conditional objection is REFUTED.

RULING 5, controller 1 (0x100..0x1ff): keep the fold onto the one image; print the controller number in both notices. Warrant: HEAD already folds (lines 63-65) and the witness reads 0x80 at +0x100 (CHECKED-IN-PACKET). DEVINIT gives both controllers the same size code, RAM/2, so one image is a faithful model of two identical register files for even RAM. Splitting is a feature, not this fix. Using `controller` in the notices does three things at once: restores the controller number HEAD's memconf message carried (GLM), gives the variable a reader so the "set but not used" warning cannot red the zero-warnings gate (Opus; PROVISIONAL on -Wall being in the build flags, which I have not seen), and retires Astra's "remove or use" either way. The "TODO: not used yet" comment is replaced by one that is true.

RULINGS 6-8, the text. (6) The over-read comment is QUALIFIED, not kept and not deleted: the source performed an out-of-bounds read; the measured HEAD binary did not (ASAN fact 1, A1); it becomes live when the exit goes (A2). Gemini's "confirmed by the ld.bu rows" is wrong: those rows confirm the exit, not the read. (7) Delete "187Bug writes memconf during startup" (no run) and the causal DEVINIT sentence; Astra is right that initialisation establishes a value, not write permission. Replace with the size-code warrant of RULING 2, which is true of the code. (8) The default-arm write notice prints idata again, as HEAD did (GLM): parity of diagnostic content with the message being removed, at no cost. #NNN becomes the bug name mvme187memcoob unless a tracker id exists (UNSETTLED which).

THE FIX. Every comment below is true of the code as written and of the packet's measurements. Hunk headers are regenerated against HEAD (struct at 47, handler 52, subscript 68).
'''
struct mvme187_data {
    struct memcreg    memcreg;
    /*  mvme187memcoob: once-per-device announce latches.
        DEVINIT memsets this struct, so they start at 0.  */
    int        warned_memconf;
    int        warned_default;
};
'''

Handler head (replaces lines 57-58 and 63-68):
'''
    /*  Controller 1 (offsets 0x100-0x1ff) presents the same
        register image as controller 0: DEVINIT derives one size
        code from RAM/2 for both, and the model keeps one image.
        The number is reported in the notices below.  */
    int controller = 0;

    if (writeflag == MEM_WRITE)
        idata = memory_readmax64(cpu, data, len);

    if (relative_addr & 0x100) {
        controller = 1;
        relative_addr &= ~0x100;
    }
'''

The bound comment, placed where line 68 was:
'''
    /*  mvme187memcoob: struct memcreg is 124 bytes, but after the
        fold relative_addr is 0..0xff.  The old code indexed the
        struct with it before the switch for every access: for
        0x7c..0xff an out-of-bounds read in the C source, whose
        value the exiting default arm never used, so the compiler
        could omit it (no AddressSanitizer report on the old build
        at -O3) and it became a live over-read as soon as the exit
        was removed and the byte forwarded (measured).  No indexed
        read remains: each arm reads its own field.  */
    switch (relative_addr) {
'''

The served arms:
'''
    case 0x00:    /*  chipid  */
        odata = d->memcreg.memc_chipid;
        break;

    case 0x04:    /*  chiprev  */
        odata = d->memcreg.memc_chiprev;
        break;

    case 0x08:    /*  memconf  */
        odata = d->memcreg.memc_memconf;
        if (writeflag == MEM_WRITE) {
            /*  Bits 0-2 are the size code (MEMC_MEMCONF_RTOB)
                that DEVINIT fixes from the configured RAM; no
                other bit of this register is modelled.  A store
                is therefore not kept.  Announced once per
                device; it used to end the emulator.  */
            if (!d->warned_memconf) {
                fatal("[ mvme187_memc: memconf write 0x%x"
                    " (controller %i) ignored, not modelled"
                    " (once) ]\n", (int)idata, controller);
                d->warned_memconf = 1;
            }
        }
        break;
'''

The default arm and tail:
'''
    default:
        /*  Unimplemented offset: a read returns 0, which is also
            every byte of the register image other than chipid,
            chiprev and memconf (DEVINIT zeroes the struct and
            nothing stores into it); a write is not kept.
            Announced once per device; it used to end the
            emulator.  */
        if (!d->warned_default) {
            fatal("[ mvme187_memc: unimplemented %s offset 0x%x"
                " (controller %i)", writeflag == MEM_WRITE ?
                "write to" : "read from", (int)relative_addr,
                controller);
            if (writeflag == MEM_WRITE)
                fatal(": 0x%x", (int)idata);
            fatal(" (once) ]\n");
            d->warned_default = 1;
        }
        break;
    }

    if (writeflag == MEM_READ)
        memory_writemax64(cpu, data, len, odata);

    return 1;
'''

The 7 CHANGES to the draft, enumerated: C1 regenerate hunk headers (consensus). C2 split case 0x00/0x04 into field reads, deleting the cast (mine; behaviour-neutral). C3 replace the bound comment with the qualified wording of PART 11 (settles the DISPUTED row). C4 replace the memconf comment: drop the 187Bug sentence and the causal DEVINIT sentence, state the size-code warrant (consensus plus mine). C5 print `controller` in both notices and rewrite its TODO comment (resolves Astra, GLM and the warning in one edit). C6 default-arm write notice prints idata (GLM). C7 #NNN becomes mvme187memcoob (Astra). Nothing else in the draft body moves; the once-latch fields, the fatal() announce, the fold and the memset-reliant zero stay as drafted.

ROWS the fix owes (bound: one row per enumerated wrong edit; all on `-E mvme88k -e mvme187 -M 64`, r3 = 0xfff43000, one real m88k instruction placed with put w and stepped once, as the frozen probe does). Negative control stays `-E nosuchmachine` WITHOUT `-e` (witness fact 2) so the device is not constructed.
R1 (ASAN leg, -O3 -fsanitize=address,undefined): ld.bu r2,r3,0x7c and ld.bu r2,r3,0xff. Want: 0 sanitizer reports, r2 = 0, pc 0x10004, reg and quit reached, exit 0. Catches A2 (measured: heap-buffer-overflow at the subscript line, 0 and 131 bytes past the 124-byte region). Measured GREEN on A3.

R2 (ASAN leg, -O0 -fsanitize=address): the same two loads. Want: 0 reports, r2 = 0, exit 0. Catches A1: at -O0 the dead pre-switch read is not eliminated, so ASAN instruments and reports it. A1-sensitivity is REASONED, not measured (the packet measured A1 only at -O3); the detector owes one self-test run of R2 against A1 before the row is banked, and if -O0 still shows nothing, R2 falls back to a source-shape row: no `[relative_addr]` subscript in dev_mvme187.c.
R3 (plain): st.b to +0x08 with r2 = 0x07, then ld.bu +0x08 in the same session. Want: r2 = 0x3 after the load; stderr carries exactly one line matching "memconf write 0x7 (controller 0) ignored"; exit 0. Catches ACCEPT (would read 0x7) and any later latent store. Measured GREEN on A3 for the value.

R4 (plain): ld.bu +0x0c. Want: r2 = 0, pc = 0x10004, no exception taken, exit 0. Catches FAULT (return 0 would vector the CPU, pc not 0x10004) and a re-introduced exit. Measured GREEN on A3.
R5 (plain): ld.bu +0x0c then ld.bu +0x10c in ONE session. Want: both r2 = 0, exactly one "unimplemented read from offset 0xc" line, and it names controller 0. Catches a missing latch, a per-slot latch, a per-controller latch; also exercises the alias. Not yet measured by any session in the packet (no session issues a second access).
R6 (plain): ld.bu +0x100, +0x104, +0x108. Want: 0x80, 0x1, 0x3. Catches a broken fold or a split image left half-initialised. +0x100 is already a control row; +0x104 and +0x108 are new.

Rows that already exist and the fix must keep green, not counted above: the frozen probe's 21/21 (CONTROL OK, SYMPTOM ABSENT, the four formerly fatal sessions exit0) and gate 1's zero-warnings build row, which is the detector for the `controller` warning. Each new row should be shown RED once on its named wrong edit (A1 for R2, A2 for R1, ACCEPT for R3, FAULT for R4, no-latch for R5, broken fold for R6) before banking; R1, R3, R4 have that evidence in D already, R2, R5, R6 do not.
Row count: 6 owed, 2 existing cited.

DISAGREEMENTS SETTLED.
S1 Over-read comment, Grok/Astra (did not execute on the measured build) vs Gemini (confirmed by ld.bu rows): settled by measurement. Fact 1 and A1 show no report, A2 shows the read at line 68. Both halves true, so the comment says both (C3).
S2 memconf DECLINE vs ACCEPT, Astra (manual: ignored) and Grok (neither proved) vs GLM (read-back compare): settled by the code itself. Bits 0-2 are the size code the model derives from RAM; storing them is wrong whatever the chip does. DECLINE, with R3 as the sentinel for a real guest that stores.
S3 Unimplemented read value, Gemini (struct byte or fault) vs the draft's 0: settled by DEVINIT. Every unserved byte of the image is 0 and nothing stores, so struct byte = 0; FAULT has no evidence. 0 stays.

S4 The controller local, Astra (remove or use) vs GLM (notice lost the number): settled by using it in both notices, which satisfies both and removes the warning risk (C5).
S5 Latch grain, Astra (per category per allocation) vs Gemini (per device folds controller 1 in): the two descriptions name the same thing, since the device holds one allocation. Grok's withdrawn per-slot latch stays withdrawn. Once per category per device, across both aliases.
S6 fatal() as announce, GLM (if it exits) vs Astra: REFUTED by debugmsg.c:384-391 and by the witness line's closing " ]", which is a third fatal() printed before exit(1).
S7 Explicit zero of latches, GLM vs Astra: REFUTED by line 108's memset of the whole struct.

S8 The DEVINIT causal sentence, Astra (initialisation is not permission) vs the draft: Astra is right as logic, so the sentence goes, but the draft's instinct was right as fact; the replacement states the size-code reason instead (C4).
S9 GLM's "code 4 for 64 MB": false in this tree. RAM/2 = 32 MiB = RTOB(3), and the control row reads 0x3 at +0x08 (CHECKED-IN-PACKET). Nothing in the fix depends on it, but any row that wants 0x4 is wrong.
S10 Dropping the memconf announce (Opus reading a, on the manual): not adopted. The manual line is unread, and the model does not implement the register's other bits, so a guest that writes it is doing something the model does not do; one line per run is the right amount of noise.

UNSETTLED, with what settles each.
U1 Hardware memconf write semantics (ignored? partly writable?): the MVME187 programmer's reference, memory configuration register page, re-read and quoted; or a 187Bug boot under the fix, where R3's notice would show a store. Changes only the announce wording, not the decline.
U2 Hardware response to unlisted offsets inside the window (value vs bus error): the same manual. Would move RULING 3 from 0 to FAULT.
U3 R2's sensitivity to A1 at -O0: one run of R2 on the A1 variant.
U4 Whether the build carries -Wall (the warning claim): the gate 1 build log. C5 is correct either way.
U5 The tracker id for #NNN.
U6 Astra's manual quote: re-read the (source) excerpt; until then it is a reading, not evidence.

FILE as separate rows, outside this fix (behaviour unchanged by it):
F1 Access widths other than a byte: a 32-bit ld at +0x00 returns 0x80 as a 32-bit value; HEAD does the same; unmeasured against hardware.
F2 Stores to chipid and chiprev are silently dropped (HEAD and fix alike); decide whether they deserve the same once-notice.
F3 Odd RAM sizes: -M 48 gives RAM/2 = 24 MiB, RTOB(2) = 16 MiB per controller, so the two controllers under-report 32 of 48 MiB. Pre-existing DEVINIT behaviour.
F4 A second mvme187 instance would carry its own latches and image; MACH adds one, so untested.
F5 Continuation past the stepped instruction: the next word is 0 and the m88k fetch of 0 stops the CPU (cpu_m88k_instr.c:3047-3048), so no row can claim "the guest keeps running" beyond one instruction without a real payload.

WEAKEST RULING: RULING 3, the unimplemented read returns 0 with a normal completion rather than a fault. It rests on the absence of evidence for a bus error and on the hardening preference to keep the guest running, not on any statement about the chip. What would overturn it: the manual saying the MEMC040 does not acknowledge cycles to unlisted offsets, or a guest (OpenBSD mvme88k memc attach, 187Bug sizing) shown to probe those offsets and depend on a specific non-zero value. If overturned, the change is one line (return 0 in the default arm) and R4 is the row that flips.

Second weakest: RULING 2's announce on memconf writes. The decline is firm; the once-line could be noise if the chip simply ignores the write and firmware writes it on every boot. One 187Bug run under the fix settles it either way: no notice means the question is moot, one notice means the comment should name the firmware and the manual. Neither outcome changes the code.

Self-check against the packet's numbers: the fix leaves A3's measured values intact (+0x00 0x80, +0x04 0x1, +0x08 0x3, +0x100 0x80, +0x0c/+0x7c/+0xff/+0x10c r2 0 with pc 0x10004, st.b 0x07 then 0x3 read back). The only observable differences from the draft are the notice texts (controller number, idata on default writes, "ignored, not modelled" wording), which the 21/21 score does not key on, and the removal of the cast, which has no runtime effect. If the detector's grep for "declined (once)" is literal, update it to the new texts before running R3 and R5.

Tallies for the final line: RULINGS 8 (bound; memconf DECLINE; unimplemented read 0; announce and latch grain; controller 1 fold plus number in notices; over-read comment qualified; 187Bug and DEVINIT sentences replaced; default write notice prints idata). CHANGES 7 (C1-C7 in PART 14). ROWS 6 owed (R1-R6), 2 existing cited.

CLOUDFINAL mvme187memcoob: 8 RULINGS 7 CHANGES 6 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS

```

## r2 -- the replication (FABLE_FINAL_r2.md)

```
2. THE RULING. Counting arguments, not seats. The bug has two independent defects: a host out-of-bounds read (offsets 124..255 of a 124-byte struct, every access, before the switch) and four guest-triggerable process exits (reads at any offset without an arm; a write to memconf). The fix must land the bound WITH or BEFORE the exit removal, never after: A2 measured that removing the exits alone turns a latent over-read into a reported one (line 68, "0 bytes after 124-byte region" at +0x7c, "131 bytes after" at +0xff). CHECKED-IN-PACKET.

RULING R1, the bound: delete the pre-switch read of `((uint8_t*)&d->memcreg)[relative_addr]`; only the arms that serve a register read the image (chipid, chiprev by subscript 0x00/0x04; memconf by field). Warrant: after the 0x100 fold relative_addr is 0..0xff (window 0x200, line 127-129), so no range check is needed once the subscript is confined to constants below 124. A3 measured 0 ASAN reports. CHECKED-IN-PACKET.

R1 continued, why not a range test. `if (relative_addr < sizeof(d->memcreg))` would also be safe but keeps serving struct bytes for 0x0c..0x7b that no arm models, and makes the comment harder to keep true. The arm-local read is the smaller change and matches the draft (A3). Menu class for the over-read: 1 DELETE (the unconditional read is deleted; nothing replaces it).

RULING R2, memconf write: DECLINE with a once-latched announce (menu 3), NOT ACCEPT `idata & 0x07` (menu 4). Warrant, REASONED: the only memconf bits this model implements are the size code, and the size is a property of the emulated machine fixed by -M (DEVINIT 115-125: RAM/2 per controller, RTOB(3) = 32 MiB at -M 64, witness reads 0x3). Storing a guest value there would let the register claim RAM the emulator does not have, which is a worse model than keeping the reset byte. A3 measured: st.b 0x07 then ld.bu reads 0x3, one notice, exit 0.

R2 continued. GLM's objection (a firmware read-back compare would make decline wrong) is a hypothesis with no run behind it; no 187Bug or OpenBSD boot is in the packet. If such a compare exists it most likely writes back the value just read (a probe), which decline also satisfies. UNSETTLED until a firmware boot is measured; see section 6. Astra's manual line ("writes are ignored") would support the same disposition but is not re-read, so the product comment must not cite it. The announce stays (not menu 2, silent): it costs one line per device instance and tells a user why a guest's memconf programming had no effect. The word "declined" in the message is replaced by "not modelled; reset value kept", which is what the code does.

RULING R3, the value an unimplemented READ returns: 0, DECLINE announced once (menu 3). Warrant, CHECKED-IN-PACKET: DEVINIT memsets the struct (line 108) and sets only chipid, chiprev, memconf (123-125).

R3 continued. Therefore for every in-range offset without an arm (0x0c..0x7b) the struct byte IS 0 today, so "the draft's 0" and "the struct byte" are the same value on this tree; the dispute Gemini raised has no observable content until some arm stores into those fields, and over-range offsets (124..255) have no struct byte at all. Draft brief open point (c) is thereby closed, not merely chosen. FAULT (menu 5, return 0 from the handler so the guest takes a bus error) is rejected for lack of evidence that the hardware faults inside its own chip-select; a bus error during firmware probing would be a new guest-visible behaviour with no measurement behind it. The old code never delivered anything to the guest (exit before writemax64), so 0 is also the least-surprising continuation.

RULING R4, an unimplemented WRITE: not stored, announced once with the value (menu 3). Warrant: the HEAD message printed idata (line 88); the draft's default notice dropped it. GLM's ask is granted: at one line per device instance the value is free and is the only diagnostic a user gets for, say, a memc_control write that went nowhere. REASONED (no default-arm store was measured; row 6 below adds one).

RULING R5, latch grain: one latch per category (memconf write; unimplemented offset) per device instance, shared by both controller aliases, and the message prints the controller number and offset of the FIRST occurrence. Warrant: there is one allocation per machine (DEVINIT), so "per device instance" and Astra's "per category per shared allocation" name the same object; Gemini's objection that this folds controller 1 into controller 0 is met by printing the controller in the notice. Grok withdrew per-slot latching; nothing in the packet needs it.

RULING R6, controller 1: stays folded onto controller 0's image in this fix (status quo at HEAD; the control +0x100 = 0x80 proves the fold is already guest-visible), and the comment says so plainly. Separate modelling of two register images is FILED as its own row (section 6); it is not a robustness defect. The `controller` local is now READ (in both announces), which removes the -Wunused-but-set-variable that the draft would introduce once the two fatal() calls that used it are gone; the "TODO: not used yet" comment is rewritten because it would be false. REASONED on the warning (gate 1 flags not in hand), CHECKED on the draft text.

RULING R7, the announce mechanism: fatal() is the right call; it returns (debugmsg.c 384-391, and the witness line's closing " ]" is a third fatal() before exit(1)). GLM's conditional objection is REFUTED. CHECKED-IN-PACKET.

RULING R8, latch initialisation: no explicit zeroing in DEVINIT; the memset at line 108 covers the new fields. GLM's ask is REFUTED by the source. CHECKED-IN-PACKET. (A second-order note: if a later change replaced malloc+memset with calloc or a designated initialiser, the latches stay zero either way.)

Summary of dispositions per former exit and direction:
- read, any offset without an arm (0x0c..0xff after the fold): DECLINE, return 0, announce once (menu 3).
- write, any offset without an arm: DECLINE, no store, announce once with value (menu 3).
- write to memconf (0x08): DECLINE, no store, announce once with value (menu 3).
- read of chipid, chiprev, memconf: unchanged, served from the image.
- write to chipid/chiprev (0x00/0x04): unchanged (silently ignored at HEAD; not in scope).
- the over-read itself: DELETE (menu 1).
Eight rulings: R1..R8.

3. THE FIX. Exact code for dev_mvme187.c, replacing lines 47-49 and 52-97; DEVINIT is unchanged. Hunk headers are to be regenerated from this tree (struct at 47, handler at 52, subscript at 68). Every comment below is written to be true of the code as shipped and of the measurements in the packet, nothing more. NNN = the issue number (replace in all three places).

'''c
struct mvme187_data {
    /*  One register image; controller 1 (offsets 0x100-0x1ff)
        is folded onto it, see the access function.  */
    struct memcreg    memcreg;
    /*  #NNN: once-per-device latches for the two announces.
        Zeroed by the memset in DEVINIT.  */
    int        warned_memconf;
    int        warned_default;
};
'''

Fix, continued (handler, part 1 of 4):

'''c
DEVICE_ACCESS(mvme187_memc)
{
    uint64_t idata = 0, odata = 0;
    struct mvme187_data *d = (struct mvme187_data *) extra;
    int controller = 0;

    if (writeflag == MEM_WRITE)
        idata = memory_readmax64(cpu, data, len);

    /*  The two controllers are not modelled separately: an
        access to controller 1 is served from the same image
        and the controller number is only reported.  */
    if (relative_addr & 0x100) {
        controller = 1;
        relative_addr &= ~0x100;
    }
'''

Fix, continued (handler, part 2 of 4):

'''c
    /*  #NNN: struct memcreg is 124 bytes but relative_addr runs
        to 0xff after the fold.  The old code read
        ((uint8_t*)&d->memcreg)[relative_addr] here for every
        access, an out-of-bounds read for offsets 124..255 whose
        value the default arm's exit(1) then discarded.  The -O3
        sanitizer build showed no report for it while the exit
        followed, and reported a heap over-read at that line as
        soon as the exit was removed.  Only the arms that serve a
        register read the image now.  */
    switch (relative_addr) {

    case 0x00:    /*  chipid  */
    case 0x04:    /*  chiprev  */
        odata = ((uint8_t*)&d->memcreg)[relative_addr];
        break;
'''

Fix, continued (handler, part 3 of 4):

'''c
    case 0x08:    /*  memconf  */
        odata = d->memcreg.memc_memconf;
        if (writeflag == MEM_WRITE) {
            /*  The store is not modelled: memc_memconf keeps
                the reset value DEVINIT computes from the
                configured RAM size.  The write is announced
                once per device and otherwise completes
                normally; it used to end the emulator.  */
            if (!d->warned_memconf) {
                fatal("[ mvme187_memc: memconf write 0x%x"
                    " (controller %i) not modelled, reset"
                    " value kept (announced once) ]\n",
                    (int) idata, controller);
                d->warned_memconf = 1;
            }
        }
        break;
'''

Fix, continued (handler, part 4 of 4):

'''c
    default:
        /*  No register is modelled at this offset.  A read
            returns 0, which is also the reset image of every
            in-range register DEVINIT does not set; a write is
            not stored.  Announced once per device; it used to
            end the emulator.  */
        if (!d->warned_default) {
            fatal("[ mvme187_memc: unimplemented %s offset"
                " 0x%x (controller %i)", writeflag == MEM_WRITE ?
                "write to" : "read from", (int) relative_addr,
                controller);
            if (writeflag == MEM_WRITE)
                fatal(": 0x%x", (int) idata);
            fatal(" (announced once) ]\n");
            d->warned_default = 1;
        }
        break;
    }

    if (writeflag == MEM_READ)
        memory_writemax64(cpu, data, len, odata);

    return 1;
}
'''

The seven CHANGES to the draft, each with its warrant:
C1 Regenerate the hunk headers against this tree (struct 47, handler 52, subscript 68). Consensus; the BEFORE text matches HEAD.
C2 Delete "187Bug writes memconf during startup." No 187Bug run exists in the packet; the sentence is unverified.
C3 Rewrite the memconf comment and message: drop the causal "derived from RAM size, so the write is DECLINED" and the word "declined"; say the store is not modelled and the reset value is kept. Astra's point stands: initialisation establishes a value, not write permission. No manual citation (not re-read).
C4 Qualify the over-read comment: the read was out of bounds in the source; the -O3 sanitizer build showed no report while the exit followed; it reported once the exit was removed. Grok and Astra right, Gemini's "confirmed by the ld.bu rows" conflated the exit symptom with the read.

Changes, continued:
C5 Read `controller` in both announces and rewrite the "TODO: not used yet" comment and the struct comment to say the fold is deliberate and only reported. Removes the set-but-unused warning the draft introduces; answers GLM's "the new notice drops the controller number".
C6 The default-arm write notice prints idata again (HEAD did; the draft dropped it). GLM, one seat, granted on the merits.
C7 Replace the #NNN placeholders with the issue number in the struct comment and the switch comment.
NOT changed (refuted asks): no explicit zeroing in DEVINIT (memset covers it); fatal() stays as the announce (it returns); no per-slot latch; no ACCEPT of `idata & 0x07`; no FAULT return.

4. THE ROWS the fix owes. Harness as in the witness: -E mvme88k -e mvme187 -M 64, r3 = 0xfff43000, each access one m88k ld.bu or st.b placed with put w and stepped once; the negative control passes no -e (witness fact 2). The enumerated wrong edits: A1 (exits to declines, default arm zeroes odata, no bound), A2 (as A1 but odata not reset, struct byte forwarded), plus W3 (exit left in an arm), W4 (ACCEPT: memconf stores idata), W5 (announce not latched), W6 (bound misplaced so a served register loses its read), W7 (default arm stores a write into the image), W8 (FAULT: handler returns 0). One row per wrong edit, two where a row also doubles as a control; six rows plus gate 1's existing zero-warnings row.

Row 1 (ASAN leg). Build -fsanitize=address,undefined at -O0 (not -O3). Session: ld.bu at +0x7c, then +0xff, reg, quit. Want: 0 sanitizer reports, exit 0, r2 = 0x0 both times, pc advances.

Row 1, continued. Catches A2 (measured: heap-buffer-overflow at line 68 even at -O3) and A1 (REASONED: at -O0 the dead load at line 68 is still emitted, so the sanitizer sees it; at -O3 A1 measured 0 reports and would escape). Negative control for the row: the A2 image must red it; the -O0 claim for A1 is UNSETTLED until run once (section 6). If the gate cannot build at -O0, run the leg at -O1 -fno-tree-dce as a fallback and record which.

Row 2 (plain build). Session: ld.bu at +0x0c, +0x7c, +0xff, +0x10c in one run; reg; quit. Want: r2 = 0x0 after each, pc = 0x10004 after each, exit 0, stderr contains exactly ONE "mvme187_memc: unimplemented read from offset 0xc (controller 0)" line and no other unimplemented line. Catches W3 (process ends), W8 (pc does not advance / exception), and W5 (four lines instead of one). HEAD reds it (exit 1 at +0x0c).

Row 3 (plain). Session: st.b 0x07 to +0x08; ld.bu +0x08; st.b 0x05 to +0x08; reg; quit. Want: the store shows [0xfff43008] = 0x07 in the debugger trace (as A3 did), r2 = 0x3 after the load, exit 0, stderr contains exactly ONE "memconf write 0x7 (controller 0) not modelled" line and NO line for 0x5. Catches W4 (r2 would read 0x7), W3 (exit), W5 (a second line). HEAD reds it (exit 1).

Row 4 (plain, controls). Session: ld.bu +0x00, +0x04, +0x08, +0x100, +0x104, +0x108; quit. Want: 0x80, 0x1, 0x3, 0x80, 0x1, 0x3; no stderr announce at all; exit 0. Catches W6 (a bound placed in front of the served arms, or a subscript typo, returns 0 for a real register) and a latch that fires on served offsets. Passes on HEAD by design (it is the control; its job is to stay green).

Row 5 (plain). Session: st.b 0x5a to +0x18 (memc_control, no arm); ld.bu +0x18; st.b 0x5a to +0x118; quit. Want: r2 = 0x0, exit 0, stderr has exactly ONE line "unimplemented write to offset 0x18 (controller 0): 0x5a (announced once)" and no line for the controller-1 store. Catches W7 (r2 would read 0x5a), C6 regressions (value missing from the line), W5, and verifies R5's grain across the alias. HEAD reds it (exit 1).

Row 6 (plain, mixed categories). Session: ld.bu +0x7c; st.b 0x01 to +0x08; ld.bu +0xff; st.b 0x02 to +0x08; quit. Want: exactly two announce lines, one per category, the first offset/value of each (0x7c; 0x1), exit 0. Catches a single shared latch (one line) and an unlatched one (four lines). HEAD reds it.

Rows, bookkeeping. Gate 1's zero-warnings build is an existing row; the fix is expected green there only with C5 applied (the draft without C5 is expected red under -Wall on GCC 4.6 or later; REASONED, gate flags not in hand). Each row records the exit status and the stderr line count so that "symptom absent" is a count, not an absence of a grep hit (the witness noted memory_rw.c zeroes the caller's buffer, so r2 = 0 alone cannot distinguish a served 0 from a skipped writemax64; row 4's 0x80 is what proves the tail stores). Per wrong edit: A1 one row (1), A2 one (1), W3 three (2,3,5), W4 one (3), W5 three (2,3,6), W6 one (4), W7 one (5), W8 one (2). Within the bound if the bound is at least three rows per wrong edit; if the bound is one, keep rows 1-5 and fold row 6 into row 3 (its second store becomes a +0x7c load).

```

Now write the reconciliation in the order given at the top.
