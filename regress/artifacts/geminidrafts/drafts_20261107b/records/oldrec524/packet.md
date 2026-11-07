# Reading task: oldrec524 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC524-3de9` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #524 armbdt (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 9081-9425 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 9081| # `#524` (armbdt): an ARM block transfer through a cold host page spliced bytes across a word boundary — the same instruction at the same unaligned base returned different bytes according to host page-cache warmth
 9082| 
 9083| **THE DEFECT.** `arm_pop()` (LDM) and `arm_push()` (STM) each hold one running
 9084| `uint32_t addr = *np` and branch on host page residency **per register**:
 9085| 
 9086| * **FAST path** (page resident): `p32[(addr & 0xfff) >> 2]` — the `>> 2` truncates the low two bits.
 9087| * **SLOW path** (cold page): passed the **RAW, UNMASKED `addr`** to `memory_rw`, whose
 9088|   `offset = paddr & offset_mask` is page-granular — **not word-rounded** — and whose transfer is a
 9089|   raw `memcpy`.
 9090| 
 9091| **So an unaligned base spliced bytes across an architectural word boundary, and which bytes a guest
 9092| got depended on whether the host page happened to be resident — a condition invisible to the guest
 9093| architecture.** Guest data corruption, on a defect that had sat with no witness for three weeks.
 9094| 
 9095| **THE FIX.** `addr & 0xfffffffc` at the two slow-path `memory_rw` call sites. **Never at function
 9096| entry:** `if (w_bit) *np = addr;` uses the unmasked running value and Mode 4 writeback derives from
 9097| unmasked `Rn`. The code generator already separates the two the same way, emitting `addr &= 0xffc;`.
 9098| 
 9099| ## The architectural warrant is QUALIFIED, and the round says so at the site
 9100| 
 9101| `ddi0100i.txt:7954-7959`: *"For `CP15_reg1_Ubit == 0`, the Load Multiple instructions ignore the
 9102| least significant two bits of the address. If an implementation includes a System Control
 9103| coprocessor (see Chapter B3 The System Control Coprocessor), an address with bits[1:0] != 0b00 causes an alignment exception **if alignment checking
 9104| is enabled**. For `CP15_reg1_Ubit == 1`, all non-word aligned accesses cause an alignment fault."* [corrected 2026-11-02, records: the quotation dropped "(see Chapter B3 The System Control Coprocessor)" after "coprocessor" with no ellipsis; restored from `ddi0100i.txt:7955-7956`]
 9105| 
 9106| **An earlier draft of the comment stated this flat, and the row's own 2026-08-29 record already said
 9107| "the record must NOT say unqualifiedly" — so the comment broke an obligation the row had already
 9108| written down.** Corrected in place.
 9109| 
 9110| **And the fork is internally inconsistent about it today**, which is why the qualification is not
 9111| academic: `cpu_arm.c:129` **SETS** `ARM_CONTROL_ALIGN` in the default control register, `:474` only
 9112| **prints** it, and nothing consults it. The model announces alignment checking and enforces none.
 9113| Modelling the fault is a separate round; this fix makes the two paths agree with each other and with
 9114| the `Ubit == 0` / checking-off reading the fork already implements on its fast path.
 9115| 
 9116| ## Witness — rung 3, and the instrument had to earn its own cold page
 9117| 
 9118| Cold debugger on the **unmodified in-tree `testarm`**, pty-driven, no `device_add`, no custom
 9119| machine. The conditioning is the point: **`put b` writes byte-wise with `CACHE_NONE|NO_EXCEPTIONS`,
 9120| populating RAM without updating the translation tables — the COLD seed; `put w` writes words with
 9121| `CACHE_DATA` and WARMS the page.** Before every transfer the probe runs `tlbdump 0,r` to confirm the
 9122| target is genuinely absent on a cold run and resident on a warm one — **without that, the core
 9123| comparison establishes nothing about which path each run took.**
 9124| 
 9125| ## The clause-(d) floor breach, measured and closed
 9126| 
 9127| **Table 2 measured `M_MASK1` — the fix present, its mask weakened `0xfffffffc` → `0xfffffffe` — at
 9128| `25/25`. A TOTAL ESCAPE**, and the canonical clause-(d) form because *the fix IS the mask* (this
 9129| project's own `#461 m_align1`, `& 3` → `& 1`).
 9130| 
 9131| **Cause: every unaligned base the probe drove was `+1`, and `x+1 & ~1 == x+1 & ~3`.**
 9132| 
 9133| It was predicted by arithmetic in adjudication and **built anyway**, because this project's rule is
 9134| that *"it would sweep the table" is a MEASUREMENT, never an inference.* The prediction was right;
 9135| a round that had accepted it unmeasured would have shipped a floor claim it never tested.
 9136| 
 9137| **CLOSED with four rows — `+2` bases for LDM and STM plus their PATH controls.** Table 3:
 9138| 
 9139| | leg | score | fails |
 9140| |---|---|---|
 9141| | `BASE` | **29/29** | none |
 9142| | `HEAD` | 19/29 | 10, including both new rows |
 9143| | **`M_MASK1`** | **27/29** | **exactly 2 — only the rows written for it** |
 9144| | `M_ENTRY` | 24/29 | 5 — **all five writeback rows, nothing else** |
 9145| | `M_POP_ONLY` / `M_PUSH_ONLY` | 24/29 | 5 each — perfect mirror images |
 9146| | `M_NULL_MEDIUM` | 8/29 | 21, including both controls |
 9147| | `RESTORED` | 19/29 | = `HEAD` |
 9148| 
 9149| **Every leg dies on a distinct, semantically correct set.** Predicted observables under `M_MASK1`
 9150| were written into `PRETABLE2.out` before the run and both hit exactly: `0x77881122` and
 9151| `0x33440000`.
 9152| 
 9153| **`+3` is deliberately NOT rowed:** `~1` dies at `+2`, `~2` already dies at `+1`, so a `+3` row
 9154| kills no ENUMERATED mutant. **Rows are owed per enumerated mutant, never per reachable value.**
 9155| Residue 3 is disclosed in the contract.
 9156| 
 9157| > **`M_ENTRY` is why the mask is at the access and not at entry, and it is not a style argument.**
 9158| > The entry-mask mutant scores 24/29 here, killed by the writeback rows — **and it is invisible BY
 9159| > CONSTRUCTION to the pre-existing `arm_writeback_probe.py`, which scopes itself to the
 9160| > single-register path and never reaches these helpers.** *An earlier draft of the comment gave a
 9161| > figure for that probe as "Measured"; the figure appears in no `.raw` and no `SCORES.txt`, only in
 9162| > briefs and seat answers. Restated by construction, with the word removed.*
 9163| 
 9164| ## Scope: the round closes the generic helpers, NOT the BDT access rule
 9165| 
 9166| **Two combined-instruction handlers replace LDM/STM outright and never reach the fixed helpers.**
 9167| `netbsd_memset` does `memset(page + (addr & 0xfff), 0, 128)` — raw page offset, no rounding, and its
 9168| guards check page bounds and source values but **never reject an unaligned address**. `netbsd_memcpy`
 9169| copies through raw `& 0xfff` offsets **while its register-publication reads use `& 0xffc`** — one
 9170| handler, two address rules, and its own comment already acknowledges *"the overlap and
 9171| unaligned-copy divergences"*.
 9172| 
 9173| **Pre-existing, so FILED (`armbdtcombined`) rather than repaired here — but the round may not claim
 9174| to have closed the class.**
 9175| 
 9176| ## Disclosed under clause (e)
 9177| 
 9178| * **Residue 3** (see above).
 9179| * **The helpers are not restricted to RAM.** An unaligned address can reach device dispatch, and
 9180|   rounding can change a device-relative offset near a device boundary.
 9181| * **`ddi0100i.txt:3256` (A2-42)** specifies additional UNPREDICTABLE behaviour for ARMv6 unaligned
 9182|   multiword accesses to Device or Strongly Ordered memory, so "all callers ignore those bits" would
 9183|   be too broad.
 9184| * **The edit rounds the VIRTUAL address, before translation**, and `memory_rw` splits translated
 9185|   accesses at 1 KB — so the old call could touch, and fault on, a page the corrected call never
 9186|   accesses. Intended, and stated rather than discovered later.
 9187| * **A separate, untouched Thumb issue:** the helper's PC handling clears both low PC bits while
 9188|   Thumb POP's specification preserves the halfword address and specifies interworking.
 9189| 
 9190| ## Records corrections and a defect in the round's own apparatus
 9191| 
 9192| **The first kill-table driver took its baseline from the MUTABLE working tree** while its own comment
 9193| claimed it verified the commit: `git log --oneline -1` gated on nothing, and the HEAD leg had **no
 9194| presence pin at all** — the one leg that would silently mismeasure. Its restoration check was also
 9195| self-referential, comparing the clone against the same tree its backup came from, which is the
 9196| carrier's named failure mode. **Filed as `killtablebaseline`; a repaired driver was written as a NEW
 9197| file — editing the preserved one would falsify the record of what ran — and negative-controlled
 9198| seven ways.**
 9199| 
 9200| **Table 1's numbers then reproduced EXACTLY on the repaired driver, 7 of 7 legs.** So that table's
 9201| *measurement* was sound and what the defect cost was *reproducibility*.
 9202| 
 9203| *`PRETABLE.out` predicted `M_NULL_MEDIUM 4/25` where the measurement was `6/25`. The two extra
 9204| survivors are `ARM_STM_COLD_CLOBBER` and `THUMB_PUSH_COLD_CLOBBER` — "neighbour not clobbered" rows
 9205| are IDENTITY rows under a medium that writes nothing, so the block's claim that every row observes
 9206| block transfer was false for those two.*
 9207| 
 9208| ## Seats
 9209| 
 9210| Panel `regress/artifacts/armbdt/panel_20260911/`: six of seven scriptable seats answered; the kimi
 9211| CLI was WALLED and its `kimi-k3:cloud` substitute answered, so that seat was COVERED. **agy
 9212| deliberately not fired** — it BUILT this round's witness and kill table. **Opus 5 deliberately not
 9213| fired.** **Fable 5 adjudicated last, after every other seat**, and its ruling reclassified this from
 9214| grok's L3 to a clause-(d) breach, which is what forced the measurement above.
 9215| 
 9216| **DISCHARGED — a WRONG RECORD, corrected 2026-09-11.**  It read *"STILL OWED: the probe is under
 9217| `regress/artifacts/`, not `regress/` proper — so 'shipped a detector with the fix' is not yet true;
 9218| promote it and pin its result in `gate_arm.sh`."*  **All three were done.**
 9219| `regress/arm_bdt_probe.py` is staged in `regress/` proper; `gate_arm.sh:672` runs it; `:674` guards
 9220| the parse; `:687-688` pin `bdt rows run 32` and `bdt rows correct`.  *Same class as the identical
 9221| stale sentence in the `#525` block above: two rounds wrote the same OWED note and neither re-read it
 9222| after discharging it.*
 9223| 
 9224| 
 9225| ## *** THE CLAUSE-(d) WORK DID NOT END AT TABLE 3.  IT TOOK THREE MORE PASSES, AN INSTRUMENT
 9226| ## REPAIR, AND A SEVEN-ROW CLASS CLOSURE -- AND THIS BLOCK RECORDED NONE OF IT UNTIL NOW. ***
 9227| 
 9228| Found by the pass-C measuring seat auditing this round's own record: within this block,
 9229| `M_MASK7`, `M_PBITCOND`, `read_mem32`, `32/32`, `BIT2` and `39` each appeared **zero** times.
 9230| The narrative stopped at *"CLOSED with four rows ... Table 3: BASE 29/29"* while the shipped
 9231| detector is 39 rows from table 6.  **A reader would not learn that a `p_bit`-conditioned mutant
 9232| was ever considered, and so would not know a `p_bit` cell exists to be left open.**  That is the
 9233| gap this section closes.
 9234| 
 9235| ### PASS B -- the first repair did not close the chain
 9236| 
 9237| `M_MASK1` (`& ~1`) was closed with two rows.  The repair-chain pass then found **`M_MASK7`**
 9238| (`& ~7`, over-alignment) and **`M_PBITCOND`** also sweeping: every base the instrument drove
 9239| -- `0x10000`, `0x2000{1,2}`, `0x2100{1,2}` -- lies in the FIRST word of its 8-byte block, where
 9240| `~3` and `~7` agree.  A base with **address bit 2 set** separates them, which is what the
 9241| `*_COLD_DATA_BIT2` rows do.
 9242| 
 9243| ### AN INSTRUMENT DEFECT, FOUND BECAUSE A **BASE** ROW WENT RED
 9244| 
 9245| Table 4 reported `BASE 31/32` -- the FIX failing `ARM_STM_COLD_DATA_BIT2`.  A red BASE row blocks
 9246| the round, so it was diagnosed rather than explained away, and **the arithmetic would not close**:
 9247| two readings of one mechanism that could not both be true.  Instrumenting settled it in one run.
 9248| 
 9249| `read_mem32()` searched for the dump line labelled `(addr & ~0xF)` -- **which matches whether or
 9250| not the dump START is aligned** -- then indexed `line[12:48].split()` by `(addr & 0xF) // 4`.  An
 9251| unaligned start BLANK-PADS the leading groups, `.split()` collapses the padding, and every index
 9252| shifts by the number of omitted groups.  **8 of 10 legs changed value when it was repaired**,
 9253| including the HEAD leg.  The store had been correct all along; the READ was wrong.  Filed as
 9254| `probereadalign`; the repair is to dump from `(addr & ~0xF)` for 16 bytes.
 9255| 
 9256| ### PASS C -- FIVE clause-(d) mutants, each a TOTAL ESCAPE, measured not read
 9257| 
 9258| `regress/artifacts/armbdt/killtable_20260911f_opus/SCORES.txt`, eight legs built in a scratch
 9259| clone against the 32-row instrument:
 9260| 
 9261|     M_POPP_NONE   p_bit ? addr : (addr & ~3)                32/32
 9262|     M_POPP_WEAK   addr & (p_bit ? ~1 : ~3)                  32/32
 9263|     M_POPW_WEAK   addr & (w_bit ? ~1 : ~3)                  32/32
 9264|     M_SBIT_NONE   s_bit ? addr : (addr & ~3)   BOTH sites   32/32
 9265|     M_NPMASK      (*np) & ~3  -- the mask on the WRONG operand  32/32
 9266| 
 9267| `M_POPP_NONE` is **clause (b)** -- the removed defect reinstated VERBATIM -- restricted to
 9268| `p_bit == 1`.  A NON-EQUIVALENCE CONTROL ran `LDMDB r0!,{r1}` (`0xe9300002`) for real
 9269| (`ldmdb_*.out`): BASE `r1 = 0x55667788`; `M_POPP_NONE` and `M_POPW_WEAK` `r1 = 0x00005566` -- the
 9270| FIX-ABSENT value -- and `M_NPMASK` `r1 = 0x00000000`, with the writeback `r0 = 0x20006` CORRECT on
 9271| all four.  **Three escaping mutants corrupt a guest register on an instruction the detector never
 9272| issues**, so "the target is dead" is excluded rather than assumed.  Not a corner case: none of
 9273| these encodings is in the 256-entry `cpu_arm_multi.txt` fast list, and `:4810-4811` disables the
 9274| optimised path entirely for a BIG-ENDIAN guest, so on BE **every** block transfer goes through
 9275| these helpers.
 9276| 
 9277| **THE CLASS:** every `p/u/s/w` partition was discharged on the STORE side and undischarged on the
 9278| LOAD side, because the only leg varying any of those bits is Thumb PUSH -- which calls
 9279| `arm_push()`.  `arm_pop()` was driven at exactly ONE `(p,u,s)` point, `(0,1,0)`.  **And it breaches
 9280| this round's OWN enumeration:** `PRETABLE3.out` declares `{site} x {residue} x {word position} x
 9281| {p_bit}` and says *"close every cell in ONE diff"* -- it then honoured `{site}` for `M_MASK7`
 9282| (adding BOTH the LDM and STM `BIT2` rows) and did NOT honour it for `p_bit`, adding only
 9283| `THUMB_PUSH_COLD_DATA_P2`.  **Three cells of a two-by-two.**
 9284| 
 9285| *Missable for a structural reason: the load-side cell could not be closed by copying the push row.
 9286| The instrument's only `p_bit=1` caller is Thumb PUSH, so closing `{load} x {p_bit=1}` needs a NEW
 9287| INSTRUCTION WORD, not a new base.*
 9288| 
 9289| ### THE CLASS CLOSURE -- seven rows in ONE diff, and the measured table that closes it
 9290| 
 9291| Per the rule that two consecutive passes finding one class owe the full enumeration in one diff:
 9292| `ARM_LDM_IB_P2` (`0xe9900002`), `ARM_LDM_DA_P2` (`0xe8100002`), `ARM_LDM_DB_P2` (`0xe9300002`),
 9293| `ARM_LDM_S_P2` (`0xe8d00002`), and a three-assertion `LDMIA r0!,{r1,r2}` leg (`0xe8b00006`) at
 9294| residue 2.  **That last is one session carrying three assertions, closing `w_bit` x residue-2 AND
 9295| register-list-length together.**  It must sit at residue 2: at the pre-existing `WB_UNAL2` base the
 9296| low bits are `01`, where `~1` and `~3` AGREE, so that row is structurally blind to a
 9297| `w_bit`-conditioned weakening.
 9298| 
 9299| `regress/artifacts/armbdt/killtable_20260911g_closure/SCORES.txt` -- SIX mutants built, SIX dead:
 9300| 
 9301|     BASE          39/39  CONTROL=OK  FAILING none
 9302|     M_POPP_NONE   37/39  ARM_LDM_IB_P2, ARM_LDM_DB_P2
 9303|     M_POPP_WEAK   37/39  ARM_LDM_IB_P2, ARM_LDM_DB_P2
 9304|     M_NPMASK      37/39  ARM_LDM_IB_P2, ARM_LDM_DB_P2
 9305|     M_POPW_WEAK   37/39  ARM_LDM_DB_P2, ARM_LDM_MULTI_P2_R1
 9306|     M_SBIT_NONE   38/39  ARM_LDM_S_P2
 9307|     M_POPU_WEAK   37/39  ARM_LDM_DA_P2, ARM_LDM_DB_P2
 9308|     RESTORE       cmp-vs-SEC CLEAN, binary FRESH, SENTINEL CLEARED
 9309| 
 9310| **`M_POPU_WEAK` was ENUMERATED by the pass-C seat and explicitly NOT BUILT** (*"derived (same
 9311| legs)"*).  Building it discharged `ARM_LDM_DA_P2`, which otherwise killed nothing -- a condemning
 9312| prediction costs one build if wrong, and this one turned a row with no measured kill into a row
 9313| with two.
 9314| 
 9315| ### DISCLOSED UNDER CLAUSE (e), not claimed
 9316| 
 9317| * `ARM_LDM_MULTI_P2_R2` and `ARM_LDM_MULTI_P2_WB` carry **no measured kill**.  *** THE REASON
 9318|   GIVEN HERE WAS WRONG -- it read "secondary assertions on a leg whose primary assertion already
 9319|   kills", which implies they COULD kill and happened not to.  They CANNOT. ***  R2 is a
 9320|   **FAST-path** observation: the first cold access warms the page, so r2 never reaches the edited
 9321|   line.  WB observes `*np`, which no mask mutant touches.  Measured twice and independently
 9322|   suspected by a reading seat that called the table *"internally impossible as stated"*.  Filed as
 9323|   the class `multiaccesswarms`: **a multi-register leg yields exactly ONE cold observation; more
 9324|   assertions mean more SESSIONS, not more registers.**
 9325| * *** THIS READ "The STORE side of the {p,u,s} product is not newly rowed: Thumb PUSH already
 9326|   varies p and u there."  THAT IS A WRONG RECORD AND IT IS WHY THE STORE GAP SURVIVED A WHOLE
 9327|   PASS. ***  **`p` and `u` are ONE SELECTOR with FOUR values -- the addressing mode**, not two
 9328|   independent bits: the code tests them NESTED (`if (p_bit) { if (u_bit)`), the architecture names
 9329|   the pair as one field, and `generate_arm_multi.c:120` switches on `p*2+u`.  Thumb PUSH is
 9330|   hardcoded **DB** (`cpu_arm.c:1670`, lines of 4dfc7165; at 987cb596 `:1720`) and every STM row was **IA** -- so the sentence stated TWO
 9331|   MODES OF FOUR as an axis, leaving **IB and DA with no row at all on the store side, at any
 9332|   residue or strength**.  The dropped-qualifier class, and the qualifier was load-bearing.
 9333|   Closed by `ARM_STM_IB_R7`, `ARM_STM_DA_R7` and `ARM_STM_S_R7`.
 9334| * *** THIS LINE SAID a joint `(p_bit && u_bit)` conditioning and `addr & (w_bit ? ~7 : ~3)` were
 9335|   "enumerated and still unbuilt".  PASS D BUILT BOTH, AS CALIBRATION KILLS, AND BOTH DIED:
 9336|   `M_PU_WEAK_BOTH` 38/39 (`ARM_LDM_IB_P2`) and `M_W_OVER7_BOTH` 38/39 (`ARM_LDM_DB_P2`). ***
 9337|   The disclosure is retired, not carried.
 9338| * Big-endian is disclosed rather than rowed, with the `:4810-4811` caveat above.
 9339| * **`ARM_LDM_S_P2` IS A SOLE CARRIER (L3):** it is the only killer of `M_SBIT_NONE`, so the whole
 9340|   `s_bit` axis rests on one row.  `ARM_LDM_DB_P2` kills five mutants but **no mutant depends on it
 9341|   alone** -- appearing in many FAILING lists is a CORRELATE of being load-bearing; being the only
 9342|   killer is the property that matters, and the two rows are opposite on it.
 9343| 
 9344| ## PASS D -- FIVE MORE ESCAPES AT 39/39, MEASURED; THEN THE FLOOR WAS RE-DERIVED AND CLOSED
 9345| 
 9346| The table-g closure above did NOT close the chain.  Pass D's kimi seat (the CLI, back from a
 9347| day-long wall) BUILT AND MEASURED five further clause-(d) mutants at 39/39 in its own clone, with
 9348| calibration kills proving its sweep could see kills (`_scratchpad/panel_20260911_193940/kimi.txt`):
 9349| 
 9350|     E1 s_bit ? addr : (addr & ~3)             PUSH only    39/39
 9351|     E2 addr & ((s_bit && w_bit) ? ~1 : ~3)    POP          39/39
 9352|     E3 addr & (s_bit ? ~7 : ~3)               POP          39/39
 9353|     E4 addr & (p_bit ? ~7 : ~3)               PUSH only    39/39
 9354|     E5 addr & ((p&&u&&w) ? ~1 : ~3)           BOTH         39/39
 9355| 
 9356| It also found `ARM_LDM_MULTI_P2_R2` VACUOUS BY CONSTRUCTION: the first cold access WARMS the page,
 9357| so the second register's access takes the FAST path and cannot see a slow-path mutant.  A reading
 9358| seat (glm) had independently called the table *"internally impossible as stated"* from the same
 9359| anomaly without knowing why.  Filed as the class `multiaccesswarms`: **a multi-register leg yields
 9360| exactly ONE cold observation; more assertions mean more SESSIONS, not more registers.**
 9361| 
 9362| ### THE FLOOR, RE-DERIVED BY THE ADJUDICATING SEAT -- and my proposed bound was wrong in both halves
 9363| 
 9364| I had graded single-axis cells as floor and joints as debt, on the premise that "all four bits are
 9365| body-tested" -- true of the ENCLOSING FUNCTIONS, which is what my grep found.  **The joint-cell
 9366| rule's "body" is the GUARDED body -- the cold `else` branch -- which tests only the `memory_rw`
 9367| return and `cpu->byte_order`.**  So p/u/s/w are SELECTORS, and the join rule is ASYMMETRIC: p,u
 9368| flow into `addr` (floor, both sites); s flows into `value` -> `data` on PUSH only; w reaches
 9369| nothing either body reads ((e)); `i == ARM_PC` flows into `value = cpu->pc + 12` on PUSH.
 9370| 
 9371| **And p/u are ONE SELECTOR WITH FOUR VALUES -- the addressing mode**: the code tests them nested,
 9372| the architecture names the pair as one field, and `generate_arm_multi.c:120` switches on `p*2+u`.
 9373| So the store side was missing TWO WHOLE MODES: STM rows were all IA and Thumb PUSH is hardcoded
 9374| DB, leaving **IB and DA with no row at all**.
 9375| 
 9376|     FLOOR = {cold first access} x {pop, push} x {IA, IB, DA, DB}
 9377|           + {push} x {s = 1}  +  {push} x {pc in list}             = TEN CELLS
 9378| 
 9379| **Regraded under that floor the four passes found 1, 1, 3, 1 breaches -- not 1, 2, 5, 5.  The
 9380| rising count was DEBT GRADED AS FLOOR.**  The real growth was geometric: every repair rowed at the
 9381| residue of the mutant it had just found, so each pass discovered the next strength.
 9382| 
 9383| ### THE GEOMETRIC FIX: EVERY ROW AT RESIDUE 7 (mod 8)
 9384| 
 9385| `0x_0007` has bits 0, 1 and 2 all set, so ONE access discriminates `~1`, `~2`, `~3` AND `~7`.  It
 9386| also closed a gap the table-g closure had SHIPPED: all three of its mode rows accessed `0x20006`
 9387| (bit 0 CLEAR), so `addr & (p_bit ? 0xfffffffd : 0xfffffffc)` escaped BY ARITHMETIC -- the round's
 9388| residue-3 disclosure went false the moment pass C admitted mode-conditioning.
 9389| 
 9390| The three pop mode rows were RE-BASED to residue 7; `ARM_LDM_S_P2` became `LDMIA r0!,{r1}^` at
 9391| `0x20007` (over-coverage, since s is (e) on pop, but free, and it closes the (s&&w) joint); and
 9392| four store rows were added: `ARM_STM_IB_R7`, `ARM_STM_DA_R7`, `ARM_STM_S_R7`, and
 9393| `ARM_STM_PC_DB_R7` -- `STMDB r0!,{r1,pc}` at `0x2100b`.  **In DB the loop starts at r15, so the PC
 9394| is accessed FIRST and its access is the cold one, at `0x21007`: one row closes both {push x pc}
 9395| and {push x DB}'s bit-2-set residue (E4).**  Its expectation (`CODE + 20`, the model's `pc + 12`)
 9396| was derived from source by a seat and cross-checked, not by me; the designing seat said plainly it
 9397| could not establish cold-path reachability from source, and **the row is green on BASE, so the
 9398| cold path was taken** -- the measurement answered what the reading could not.
 9399| 
 9400| ### TABLE 7 (`regress/artifacts/armbdt/killtable_20260911h_floor/SCORES.txt`) -- THE CHAIN CLOSES
 9401| 
 9402| `PRETABLE.out` written BEFORE the table, naming all ten cells with row, residue and mutant.
 9403| 
 9404|     BASE           43/43   CONTROL=OK   FAILING none
 9405|     M_PUSHS_NONE   42/43   ARM_STM_S_R7          <- E1, the measured L2
 9406|     M_POPP_MASK2   41/43   ARM_LDM_IB_P2, ARM_LDM_DB_P2    <- the ~2 gap
 9407|     M_PUSH_IB_WEAK 42/43   ARM_STM_IB_R7         M_PUSH_DA_WEAK 42/43  ARM_STM_DA_R7
 9408|     M_PUSHPC_NONE  42/43   ARM_STM_PC_DB_R7      M_PUSHP_OVER7  41/43  ARM_STM_IB_R7, ARM_STM_PC_DB_R7
 9409|     + all six table-g mutants, still dead
 9410|     D_PUW_WEAK     43/43   FAILING none          <- ESCAPED, as DISCLOSED in the contract
 9411|     D_POPSW_WEAK   42/43   ARM_LDM_S_P2          <- DIED, better than disclosed
 9412|     RESTORE        cmp-vs-SEC CLEAN, binary FRESH, SENTINEL CLEARED
 9413| 
 9414| **The first table in this round whose rows came from the HELPERS' INPUTS rather than from the
 9415| mutant list -- and the first in which every floor cell kills and the only escape is one the
 9416| contract named in advance.**  The gate pin moved 39 -> 43 by hand, with its reason.
 9417| 
 9418| **GATE GREEN AT THE 43 PIN** -- `gate_arm.sh` run whole on 2026-09-12, unpiped: `bdt control`
 9419| OK, `bdt rows run` 43, `bdt rows correct` 43, 0 FAIL, **gate 14 PASS (910 checks)**, log
 9420| preserved at `regress/artifacts/armbdt/killtable_20260911h_floor/gate_arm_43rows.log`.  The
 9421| shipped probe is byte-identical to that table's frozen copy (`cmp` run in the gate driver).
 9422| The gate's own comment was corrected AFTER the run (comment-only: "25 -> 29 -> 32" named three
 9423| of the five row counts).  The `arm_bdt_probe.py` MANIFEST entry, deferred while the probe was
 9424| untracked, lands in this commit with the probe and its twelve preserved instruments.
 9425| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_524: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC524: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
