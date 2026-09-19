OPUS_SEAT_ALIVE_20260918_541P1
claude-opus-5[1m]
VERDICT: 4 (ACCEPT: drop exit(1) and keep the identity mapping, with the existing message latched to print once) -- it is the only member that fixes all three cells in-round. A load returns 0, a store is dropped, and an instruction fetch never has a translation failure, so it never reaches the generic cpu_dyntrans.c:729-733 exit. It also makes 0xfffffffd80000000 behave like every one of its neighbours. DECLINE (2/3) leaves the fetch dying at :729-733 and hands loads a stale register.

# alphavmkill pass 1: Opus 5 seat

**Nothing was built or run.** The change of plan arrived before any build, and no `/tmp` clone exists from this seat. The only commands I ran were read-only: `cmp`, `ls` and `grep` on the build trees and sources, plus reading the witness artifacts. `/tmp/gxkill540` was not touched.

**Everything below is derived by reading, unless it is marked MEASURED** (only the committed-build witness artifact is measured). I name the runs that would settle each derived claim at the end. What I read:
- the brief and the witness, whose frozen copy is md5-identical to `_scratchpad/w541/`;
- `witness_HEAD_20260918/{probe_HEAD.raw, transcript_HEAD.txt}`;
- `memory_alpha.c`, `memory_rw.c`, `cpu_alpha_instr_loadstore.c` and `cpu_dyntrans.c` in full, from this session;
- beyond the brief's list, the specific lines cited: `cpu_alpha_instr.c` (`call_pal`, `to_be_translated`), `cpu_alpha_palcode.c` (the default arm), `core/emul.c` (end of run), `core/main.c` (`-V`, `-M`), and `core/memory.c` (`memory_paddr_to_hostaddr`, and the missing-address warning).

## THE THREE THINGS YOU ASKED FIRST

**1. Your reading of cpu_dyntrans.c:670-734 is right.** On Alpha, EVERY failed instruction-fetch translation ends the host.
- `DYNTRANS_PC_TO_POINTERS_GENERIC` sets `cached_pc = cpu->pc` (:629) and calls `translate_v2p(..., FLAG_INSTR)` (:679).
- On failure it assumes the translator moved the PC to an exception handler, so it re-reads `cpu->pc` (:698) and tries the fast table (:707-717) and then `translate_v2p` again (:721). On a second failure it runs `fatal(...); exit(1)` (:729-733).
- `alpha_translate_v2p` never writes `cpu->pc`. I read all 199 lines: it has no PC assignment and ignores `flags`.
- So the second lookup uses the same address. The fast table cannot have gained an entry in between, because a failed translate installs nothing. And the page walk is deterministic, reading page-table RAM that has not changed.
- Every failure therefore takes one of two exits:
  - the translator's own `exit(1)`, at this site;
  - or two "wasn't found" lines followed by the dyntrans FATAL.
- It applies to a jump, a fall-through into the next page, and any call that ends in `alpha_pc_to_pointers`.
- **So under DECLINE, the load and store cells are fixed and the fetch cell dies at :729-733.** Filing `alphaifetchkill` separately is right.

**2. Which member I would ship: 4, with the existing `fatal()` text latched to print once and `exit(1)` removed.** The reasons are in Q2. The deciding one is that ACCEPT is the only member under which a fetch from this address has no translation failure at all. That makes this round independent of `alphaifetchkill`.

**3. What member 4 actually does** (this is derived; the neighbour-address runs at the end would measure it on the committed binary):
- **Where the address goes.** Identity maps the address to 0xfffffffd80000000 & 0x3ffffffffff = 0x3fd80000000, about 4.08 TB.
  - `-M` is capped at 1048576 MB, i.e. 2^40 (main.c:415-416), so that address is past `physical_max` on every legal configuration.
  - No device sits there: the highest registered address on alphabook1 is pccmos's fake mc146818 at 0x1d00000000.
  - The access therefore takes `memory_rw`'s missing-address branch (:663-712): a WARNING-level "non-existant paddr" line on every access, which `-q` silences, then zero-fill or drop.
- **LOAD:** the destination becomes 0 and execution continues.
- **STORE:** the store is dropped and execution continues. It reports success, and for STx_C the status register is set to 1.
- **FETCH:**
  1. The fetch translation succeeds (`cpu_dyntrans.c:679`, returns 2).
  2. `memory_paddr_to_hostaddr` returns NULL (the read of a missing block), so no fast-path entry is installed.
  3. `to_be_translated` reads the instruction word through `memory_rw` (cpu_alpha_instr.c:812). That is identity again, so it zero-fills and returns OK.
  4. The word is 0, i.e. `CALL_PAL 0x0000`, which is Alpha's HALT (:839-841).
  5. `alpha_palcode`'s default arm prints `[ Alpha PALcode 0x0 unimplemented! ]` and sets `cpu->running = 0` (palcode.c:522-523).
  6. What happens next depends on the options:
     - **Under `-V` or `-K`,** which both set `debugger_enter_at_end_of_run` (main.c:473-475, :406-407), the run loop enters the debugger with "All machines stopped." (emul.c:1052-1058). The process stays alive.
     - **Otherwise** the run loop breaks and gxemul exits normally with status 0 (main.c:807, :821). That is the same outcome a guest gets by executing `call_pal 0` directly today.
  - This is exactly the path VMKILL+0x2000 already takes on the committed build. Member 4 adds no new code path; it just stops making this one address an exception.
- **Messages:** if the `fatal()` is kept UNLATCHED, as a literal "drop only exit(1)" would do, it prints on every translation of the address. A fetch translates it twice: once in `PC_TO_POINTERS_GENERIC` and once in `to_be_translated`. That is a guest-drivable flood that `-q` cannot silence. **So member 4 needs the latch.**

---

## Q1 -- PREMISES

- **Is 0xfffffffd80000000 special to a guest? Yes, to NetBSD/alpha, by exact arithmetic.**
  - Take the brief's VPT base 0xfffffffc00000000. The VPT covers 2^30 page-table entries × 8 bytes = 8 GiB, i.e. 0xfffffffc00000000–0xfffffffdffffffff.
  - The address is at offset 0x180000000, which is entry 0x30000000. That entry maps VA<42:13> = 0x30000000, i.e. VA 0x60000000000 sign-extended to **0xfffffe0000000000 = `ALPHA_K1SEG_BASE`** (thirdparty/alpha_cpu.h:211).
  - So it is **the page-table entry of the first kernel-virtual page.** It is the one page this same arm already remaps: `(vaddr & ~0xffffff) == 0xfffffe0000000000 → 0x7efa000 + ...` (memory_alpha.c:83-84).
  - That reads as a deliberate tripwire for "the kernel is now reading its own page-table entry for the page GXemul was faking". That matches the message's own wording.
  - The VPT base constant itself is NOT in the tree; it lives in NetBSD's pmap.h. That the arithmetic lands exactly on a named segment base is strong corroboration.
  - The translator also ignores the guest's own VPT pointer: `wrvptptr` stores it (palcode.c:225-227), and memory_alpha.c:48 has the read commented out.
  - I did not establish that the address means anything to Linux or OSF/1.
- **Does member 4 hand the guest a wrong translation? Yes, but it is the same one the arm already hands out.** It is the identity fiction the arm gives every one of the other 2^30−1 VPT slots, all of K1SEG outside its 16 MB remap, and every other non-K0SEG address.
  - The trap guards ONE 8-byte address out of an 8 GiB region. It is a tripwire, not a correctness guard.
  - Test for the premise: a load from 0xfffffffd80000008 on the committed build already "silently succeeds" with 0.
  - That paddr always returns **0 for a load and drops a store**, with a verbosity-gated WARNING line, as described in answer 3 above.
- **Is `return 0` better or worse for the guest? Worse, in all three cells.**
  - `return 0` does not give the guest a zero. #215 abandons the access, so a **LOAD leaves the destination holding whatever it held before.** That value is non-deterministic from the guest's point of view.
  - An **STx_C** is worse: its status register keeps the DATA value, because the "set to 1" in LS_GENERIC_N (loadstore.c:120-124) is skipped. The guest reads that as success if the data is nonzero, or spins forever if it is 0.
  - Member 4's 0 is what an invalid page-table entry reads as, and it is deterministic.
  - For a **fetch**, 2/3 end the host through :729-733, while 4 executes HALT.
- **A wrong record the brief does not mention, and it would steer the choice toward DECLINE.** memory_alpha.c:194-196 says a failed walk should "report no-translation (0) so the caller raises the fault". **No Alpha caller raises one:** loads and stores abandon (#215), and fetches exit (:729-733). Correct this comment in whichever round touches the file.

## Q2 -- WHICH MEMBER; LOAD / STORE / FETCH UNDER EACH, AND WHAT THE WITNESS PRINTS

Derived. The witness only exercises the LOAD cell.

| member | LOAD | STORE | FETCH at VMKILL | witness (MEASURED only for today's build) |
|---|---|---|---|---|
| today | host exit(1) with the message | same | same | **3/5** (MEASURED), vmmsg=1 |
| 1 DELETE the block | dest 0, WARNING | dropped, WARNING | CALL_PAL 0 → PAL default halt; alive under -V/-K, otherwise normal exit 0 | 5/5, dest=0x0, vmmsg=0 |
| 2 DECLINE silently | dest **unchanged** (0xbad1d8a), silent | abandoned, silent | **host exit(1)** at :729-733 | 5/5, dest=0xbad1d8a, vmmsg=0 |
| 3 DECLINE + latch | same as 2, plus one line | same as 2 | exit(1) at :729-733, after the one line | 5/5, dest=0xbad1d8a, vmmsg=1 |
| 4 literal (drop exit only) | dest 0, message **every access** | dropped, message every access | HALT as in 1, message ×2 | 5/5, dest=0x0, vmmsg=1 |
| **4 + latch (ship this)** | dest 0, message once | dropped | HALT as in 1; no kill text, no FATAL | 5/5, dest=0x0, vmmsg=1 |
| 5 FAULT | not available: Alpha delivers no exception here | | | |
| 6 BACKED ACCEPT | would invent storage for a page-table slot; no measured reason to add it | | | |
| 7 IMPLEMENT kernel VM | a feature, out of scope | | | |

**Why 4 + latch over its neighbours:**
- **Over 3:** it fixes the fetch cell in-round rather than handing it to `alphaifetchkill`, and loads get 0 instead of a stale register.
  - It also follows the arm's own rule, which is the strongest reason: every other address in the `ptbr == 0` window is identity-mapped. Declining would make this one address the only hole in that window.
- **Over 1:** it keeps a bounded version of the diagnostic. This follows the tree's precedent of keeping `fatal()` and latching it (dev_asc.c:250-257): `fatal()` survives `-q`, whereas the generic WARNING does not.
  - Unlike the footbridge +0x188 case, an announcement here is not a wrong record. Kernel virtual memory really is not implemented.
  - Suggested wording: "... not yet implemented; access identity-mapped to nonexistent memory (once)".
- **Latch storage:**
  - Prefer a per-CPU field in `cpu->cd.alpha`. The tree's rule favours per-instance latches (dev_lca.c's #516 comment).
  - A function-static latch would join the already-filed `staticlatchscope` class. Its excuse would be that this is a machine-wide limitation, and that excuse should be written down if it is chosen.

## Q3 -- THE SECOND LEFTOVER (`fatal("AYONA3\n")`, memory_alpha.c:94)

**It is its own row, not part of this round.** It fails the reopening rule on three counts:
- **A different class:** an unlatched, meaningless line that `-q` cannot silence (a flood) rather than a host kill.
- **A different vehicle:** it is reached only on the walk path, i.e. `ptbr != 0`, or user mode even at ptbr == 0, since both identity arms require `!userMode`. The ptbr == 0 witness cannot see it.
- **No witness** yet.

Its witness is cheap: the #540 witness's `swpctx` all-zero-L1 vehicle, plus one load of the address, should print `AYONA3` and then "wasn't found".

Two notes on the walk case:
- VMKILL's first-level index there is 0x3fe, the same entry as 0xfffffffc00000000, which is where a self-mapping table would sit.
- A fetch at VMKILL on that path is `alphaifetchkill`'s case, not this row's.

LOW, file under the flood class.

## Q4 -- THE WITNESS

- **Do the controls prove what they claim? Yes, and slightly more than the notes say.**
  - `live` (VAL_A) proves the raw-VA load path works.
  - `hwrpb sig` (0x4250525748, "HWRPB") can only come from the arm's `(vaddr & ~0x7fff) == 0x10000000` remap. 0x10000008 is past `-M 64` RAM, so plain identity would read 0.
  - Because that remap sits inside `if (!userMode && base == 0)`, the signature also proves **kernel mode and ptbr == 0** at step 1. Nothing between the two steps changes either.
- **Is the attribution guard sufficient? For this witness, yes.**
  - The text "Alpha kernel virtual memory seems to want to be used" appears only at memory_alpha.c:76 (grep over `src/`).
  - `exit(1)` follows it immediately, so text plus death means this site. The transcript shows it right after `ldq t4,0(t1)`.
- **But do not carry the guard into the DETECTOR.**
  - `DIED_ELSEWHERE` prints `RESULT=0/0` and exits with status 2. A kill-table scorer that counts "passed rows equal total rows" as an escape will count 0/0 as an escape. That is the same trap I flagged on #540.
  - Under the chosen member, any death under a mutant is a KILL. Examples: a mutant that re-adds the exit with different text, or a fetch variant that reaches :729-733. Score them red.
- **Rows the detector owes under 4 + latch:**
  - **LOAD:** dest == 0, continued, alive. The dest value is what tells ACCEPT apart from a DECLINE regression, which would leave 0xbad1d8a.
  - **STORE:** `STQ` to VMKILL, continued, alive. Then a load of VMKILL returns 0, which shows no invented storage (rules out member 6).
  - **FETCH:** `jmp` to VMKILL under `-V`. The transcript must show `PALcode 0x0 unimplemented`, and must NOT show the kill text or `could not find physical address`. The process must be alive at the prompt, and `pc` should read VMKILL.
  - **LATCH:** two or more accesses, and the message appears exactly once.
  - **ANCHOR:** a load at VMKILL+8 behaves exactly like one at VMKILL. This pins the width of the special case against a mutant keyed on `(vaddr & ~7)` or the page.
  - **Controls:** `live` and `sig`, as now.
- **Mutants that follow from the change.** The change is a deletion plus an added latch condition:
  - **(b)** put `exit(1)` back → every cell red.
  - **(d), latch never set** → the latch row reds.
  - **(d), the removed behaviour re-added under a different condition:**
    - exit only on `FLAG_INSTR` → the fetch row;
    - exit only on writes → the store row;
    - exit at VMKILL+8 → the anchor row;
    - `return 0` instead of identity → the LOAD row's dest value.
- **Cells not witnessed yet.** On the committed build, STORE and FETCH are unwitnessed. They are trivial to add: the same site is reached, because `translate_v2p` runs for stores and for `PC_TO_POINTERS`.

## Q5 -- ORDER OF ROUNDS

- **Under member 4 the two rounds are independent.** A fetch at this address has no translation failure, so it never reaches `alphaifetchkill`'s path.
  - This round closes its fetch cell. Measurable: the fetch row is green on this round's commit alone.
  - `alphaifetchkill` remains a real HIGH row for walk-path and user-mode fetch failures, and can go in either order.
- **Under member 2/3 the order matters:**
  - **This round first:** the fetch cell must be DISCLOSED. The outcome is still a host `exit(1)`; only the text changes, from the kill message to `FATAL: could not find physical address of the exception handler?`. The detector cannot row it green.
  - **`alphaifetchkill` first:** whatever that round chooses decides what this cell does. It needs an Alpha-specific decision, because :729-733 is shared with architectures whose translator does move the PC. Only then can this round row the cell.
  - Member 4 makes this ordering question disappear, which is itself a reason to choose it.

## FOUND SOMETHING ELSE

1. **memory_alpha.c:194-196 (#194) is a wrong record** that argues for DECLINE: "so the caller raises the fault". No Alpha caller does (see Q1).
2. **The fetch path skips the `physical_max` check.**
   - `PC_TO_POINTERS_GENERIC` (:747) calls `memory_paddr_to_hostaddr` without checking `physical_max`. That function keeps only 40 bits of the address (`MAX_BITS` 40; index = (paddr >> 20) & 0xfffff), so the 42-bit identity address 0x3fd80000000 aliases the entry for 0xfd80000000.
   - It returns NULL unless RAM exists there, which needs `-M` ≥ ~1038849. That is legal, since the maximum is 1048576.
   - This already applies to every identity-mapped K1SEG/VPT fetch today. It is exotic: file it, do not fix it here.
3. **`-V` implies entering the debugger at end of run** (main.c:473-475). A detector fetch row under ACCEPT therefore sees the process alive at the prompt. A normal run would exit with status 0 instead. The row should say which of the two it asserts.
4. `build/src/devices/dev_lca.c` is currently byte-identical to SEC's working tree, i.e. it carries #540's uncommitted `| PHYSICAL`. The vmkill path does not touch it, but the next two-part clearance should record it.

## MEASUREMENTS TO RUN AFTER THE GATE (none were run here)

1. **Member 4's behaviour, measured with NO build**, on the committed binary, at neighbour addresses the trap does not cover:
   - a load from 0xfffffffd80000008: expect dest 0x0, continued, a WARNING line;
   - a store to it: expect continued;
   - a `jmp` to 0xfffffffd80002000 under `-V`: expect `[ Alpha PALcode 0x0 unimplemented! ]`, "All machines stopped.", alive at the prompt, and `pc` = that address.
2. **Your reading, witnessed on the committed binary:** the #540 vehicle (`swpctx` to an all-zero first-level table), then a `jmp` to any raw address. Expect two "wasn't found" lines, then `FATAL: could not find physical address of the exception handler?`, then death. That is `alphaifetchkill`'s witness.
3. **In a scratch clone,** four binaries: base, DELETE, DECLINE (silent), and ACCEPT + latch. Run the witness plus STORE and FETCH cells against each. Expected:
   - dest 0x0 for DELETE and ACCEPT, versus 0xbad1d8a for DECLINE;
   - DECLINE's fetch dies with the dyntrans FATAL text;
   - ACCEPT's fetch halts through PAL 0.
