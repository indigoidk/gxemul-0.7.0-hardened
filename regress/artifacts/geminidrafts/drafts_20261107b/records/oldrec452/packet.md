# Reading task: oldrec452 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC452-9b7e` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #452 sh4tlbda2 (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 29217-29389 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
29217| ## R21 (#452) — a device answered for eight megabytes it could not service
29218| 
29219| `src/devices/dev_sh4.c`. Both TLB data-array devices are registered for **16 MB**:
29220| 
29221| ```c
29222| 	memory_device_register(machine->memory, "sh4_itlb_da1", SH4_ITLB_DA1,
29223| 	    0x01000000, dev_sh4_itlb_da1_access, d, DM_DEFAULT, NULL);
29224| 	memory_device_register(machine->memory, "sh4_utlb_da1", SH4_UTLB_DA1,
29225| 	    0x01000000, dev_sh4_utlb_da1_access, d, DM_DEFAULT, NULL);
29226| ```
29227| 
29228| and each handler opened by ending the host process on `relative_addr & 0x800000` — **8 MB,
29229| the upper half of the range the device itself had claimed.** The guard sat above the
29230| `writeflag` test, so a load and a store both died.
29231| 
29232| *** THE DISCRIMINATOR IS A SINGLE ADDRESS BIT, WHICH IS SHARPER THAN ANY EARLIER SH-4
29233| ROUND HERE. *** `#443` needed a particular PCIC transaction, `#447` a particular register
29234| value, `#448` a particular field encoding, `#451` an entire clocked-in byte. Here the same
29235| device at the same width answers at `0xf3000000` and died at `0xf3800000`.
29236| 
29237| Fixed on the family pattern: keep the diagnostic, latch it, drop `exit(1)`, and consume the
29238| access with a defined result — reads produce 0, stores are discarded. Explicitly NOT
29239| serviced as array 1: `e` comes from the same masked bits, so aliasing would let a guest
29240| probing array 2 read and **corrupt real translation entries**.
29241| 
29242| ### Three questions the round answered by measuring instead of asking
29243| 
29244| * **`e` is bounded, so there is no second defect.** `SH4_ITLB_E_MASK = 0x300 >> 8` gives
29245|   0..3 against a 4-entry array; `0x3f00 >> 8` gives 0..63 against 64. Neither mask contains
29246|   bit 23, so the bound holds across the whole 16 MB window and not merely the lower half —
29247|   which is the stricter form a seat asked for.
29248| * **The `aa` windows do NOT share the defect.** Also 16 MB, but their handlers carry no
29249|   guard and no `exit(1)`; they alias silently. Two-site round, not four.
29250| * **The latch key must not come from the address.** A seat warned, before the edit existed,
29251|   that `relative_addr & 0x800000` is the SAME value at both sites, so whichever complained
29252|   first would silence the other for the device lifetime. Two explicit site bits instead;
29253|   ceiling two lines per device lifetime.
29254| 
29255| ### The mutant that refuted three seats
29256| 
29257| All three pass-1 seats that proposed a mutant proposed the same one: drop the
29258| `memory_writemax64(cpu, data, len, 0)` call on the declined-read path, and the guest gets
29259| stale host bytes. **It was built, and it does not.**
29260| 
29261| `memory_rw.c:484-492` [corrected 2026-11-02, records: said `:484-491`; the `memset(data, 0, len);` is `:492` at 927553fa and at 987cb596] — **correction `#95` in this same tree** — already zeroes the caller's
29262| buffer before every device read, described there as the *"root-cause fix for the uninit-read
29263| class"*. Measured in five contexts: a bare read; one primed by a non-zero array-1 read; one
29264| with the destination register pre-set to `0xdeadbeef`; one primed through RAM; one primed
29265| through the **other** TLB device. All returned `00000000` on the mutant and on the fix
29266| alike.
29267| 
29268| So the call stays — a handler should not lean on a guarantee enforced two files away — but
29269| it carries **no detector row**, because a mutant measured equivalent cannot be killed and a
29270| row written as though it could is decoration. **Both the source comment and the detector
29271| docstring had asserted the stale-bytes claim as fact, and both were corrected.** The three
29272| seats were reasoning correctly about C; they simply could not know this tree had already
29273| closed the class four hundred corrections earlier.
29274| 
29275| ### And a second reason was wrong in the same way
29276| 
29277| An earlier draft of the comment said `return 0` "raises an architecture-specific bus-error
29278| exception". A pass-1 seat read the arms rather than the summary: `memory_rw.c`'s failure
29279| block has `MEM_MIPS` and `MEM_M88K` only, and **`MEM_SH` appears nowhere in that file**. On
29280| SH nothing is raised — the access returns `MEMORY_ACCESS_FAILED` and `cpu_sh_instr.c`'s
29281| `X(load_l_rm_rn)` (`:739`) returns without ever assigning the destination register, leaving
29282| it stale, under a comment of its own that claims an Exception.
29283| 
29284| The conclusion survived and got stronger — a silently stale register is worse than a clean
29285| fault — but the reason was wrong, and this project has already recorded what happens to a
29286| wrong reason: *it gets reused.* The kill table then confirmed the corrected mechanism from
29287| the other side, because M3 (`return 0`) reddens R1 by leaving the register holding the
29288| earlier array-1 value, which is what a stale register looks like and not what an exception
29289| looks like.
29290| 
29291| ### The detector, and the row that carries the de-escalation obligation
29292| 
29293| `regress/sh4_tlbda2_probe.py`, 15 rows, wired into gate 10.
29294| `regress/sh4_tlbda2_witness.py` asserts the PRE-FIX symptom and is deliberately ungated:
29295| **7/7 before, 4/7 after**, the three differences being exactly the three kill rows.
29296| 
29297| **The witness's controls were strengthened mid-round after a seat called them weak, and it
29298| was right.** They had asserted *inequality* against three wrong values — which any fourth
29299| wrong value passes, a mutated mask included. They now assert **equality** with the value
29300| each device's own mask folds `0xffffffff` to, and the two DIFFER (`0x1ffffdfa` for ITLB,
29301| `0x1ffffdff` for UTLB, because the UTLB mask adds `WT|D`), so neither row can be satisfied
29302| by the other device.
29303| 
29304| | mutant | result | rows that redden |
29305| |---|---|---|
29306| | V1/V2 `exit(1)` restored, each site | DIES | R1,R3,X,RPT / R2,X |
29307| | M1 `memory_writemax64` dropped | **EQUIVALENT** (see above) | — |
29308| | M2 early `return 1` dropped | DIES | R1,R3 |
29309| | M3 `return 0` instead of 1 | DIES | R1 |
29310| | M4 key derived from the address | DIES | X |
29311| | M5 latch guard removed | DIES | RPT |
29312| | M6 only the ITLB site fixed | DIES | R2,X |
29313| | M7 declined read returns `mask` | DIES | R1 |
29314| | C1 guard `& 0x800100` (ITLB) | DIES | A4i |
29315| | C2 guard `== 0x800000` (ITLB) | DIES | R4 |
29316| | K1 guard `& 0x802000` (UTLB) | DIES | A4u |
29317| | G1u growth at the UTLB site only | DIES | A4u |
29318| | W1 write-only fallthrough at UTLB | DIES | R3u |
29319| | M5u latch guard removed at UTLB only | DIES | RPTu |
29320| | G1 guard grown to `0xc00000`, JOINT | DIES | A3, A4i |
29321| 
29322| ### Pass 2 found the same shape as #451 did, mirrored — and then generalised past it
29323| 
29324| **Six of those rows did not exist when the diff was reviewed.** Three seats found two
29325| independent holes, and the second one is a class rather than an instance.
29326| 
29327| **The structural half is #451's lesson with the sites swapped.** R3, RPT and A3 were all
29328| built on the **ITLB** site, so the UTLB copies of three already-known mutants had no
29329| coverage — including a *write-only fallthrough* (`return 1` moved inside the `MEM_READ`
29330| arm) that is read-clean and therefore invisible to every read row, while a declined store
29331| lands in `utlb_lo[e]` for the entry array 1 just used. In #451 the FIRST site was
29332| under-exercised; here the second. **A two-site round builds its rows on whichever site it
29333| wrote first**, and that is now twice.
29334| 
29335| **The general half is sharper.** The guard is a bitwise-OR predicate, so growth into ANY
29336| bit is as realistic an edit as G1's growth into bit 22 — and A3, sitting at `+0x400000`,
29337| trips on bit 22 and *only* bit 22. Three measured instances all passed ten rows: `&
29338| 0x800100` and `== 0x800000` at the ITLB site, and `& 0x802000` at the UTLB site. The middle
29339| one is the nastiest — it declines nothing extra, it *narrows* the guard to one address so
29340| the rest of array 2 silently aliases array 1.
29341| 
29342| **Bits 8–13 are the entry selector** (SH7750 manual §3.7.3: *"the entry is selected by bits
29343| [9:8]"*, six bits for the UTLB), so a growth into that span silently refuses **real
29344| translation entries**. The fix is one row per device at offset `+0x7ffffc` — bits 2..22 all
29345| set, entry 3 of the ITLB and entry 63 of the UTLB, both legal — which trips on OR-growth
29346| into any of them at once. `A4i` and `A4u` are those rows, and they killed four of the six
29347| new mutants between them.
29348| 
29349| **"G1 discharges the de-escalation clause" was itself an overclaim, and a seat said so.**
29350| It discharged the clause for one bit position at one site. The obligation is per-predicate,
29351| and there are two predicates.
29352| 
29353| ### Two more of this round's own claims were measured false
29354| 
29355| * R1/R2 were named *"array 1 answered 0x1ffffdfa in the same session"*. **It does not.**
29356|   The array-1 result lands in `r2` and the array-2 load overwrites it before anything
29357|   stores `r2` — so the value was never observed in those sessions. Two seats caught it
29358|   independently. The name now says what the row checks; A1/A2/O prove array 1 works, in
29359|   their own sessions.
29360| * *"M1 is equivalent"* is true only **under the current universal pre-zeroing invariant**.
29361|   Five measurements establish survival in five contexts, not equivalence in principle. If
29362|   `#95` were ever narrowed, the mutant would become live and this detector would not see
29363|   it.
29364| 
29365| ### And the manual arrived mid-round, which settled a question and refuted a finding
29366| 
29367| By owner directive, a real **SH7750 Hardware Manual** (Rev.7.00, REJ09B0366-0700, 1074
29368| pages) was obtained and extracted to `_scratchpad/sh7750_hardware.txt`. It is the first SH
29369| documentation this project has ever had; the carrier's standing note said flatly that there
29370| was none.
29371| 
29372| It confirmed the fix and **refuted a finding this round had already filed.** The loop had
29373| argued that the `aa` handlers ignoring bit 23, while the `da1` handlers treat it as
29374| selecting a second array, meant one of them must be wrong. §3.3.1's P4 map says both are
29375| right: `H'F200 0000`–`H'F2FF FFFF` is the instruction TLB **address** array as one
29376| undivided 16 MB region, while `H'F300 0000`–`H'F3FF FFFF` holds instruction TLB data arrays
29377| **1 and 2**, split at `H'F380 0000`. The `aa` windows are not split; the `da1` windows are.
29378| 
29379| §3.7.3 also confirms two things the fix depends on: the entry is *"selected by bits [9:8]"*
29380| — matching `SH4_ITLB_E_MASK` — and array 2 holds **SA and TC**, which are *different
29381| fields* from array 1's PPN/V/SZ/PR/C/SH. That is precisely why declining is right and
29382| aliasing array 2 onto array 1 would have been wrong.
29383| 
29384| `sh4aaalias` was withdrawn on that reading. **One download refuted a wrong finding in the
29385| same session it was raised** — which is the argument for the standing rule that an SH round
29386| must cite the source, and now may also cite this manual, but never a search result about it.
29387| 
29388| Build rc=0, zero warnings. Gate 10 PASS, 62 checks (was 60), run singly.
29389| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_452: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC452: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
