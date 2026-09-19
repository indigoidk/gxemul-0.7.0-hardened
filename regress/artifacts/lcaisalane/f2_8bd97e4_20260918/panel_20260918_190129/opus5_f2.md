OPUS_SEAT_530F2_LIVE
VERDICT: L2-CLASS-CLOSURE -- vc is a breach on both routes: lane is a partition the body tests, crossed with the width cell pass 6 put in the floor, and vc sits inside the shipped "any guard that declines a len > 8 WRITE" with no disclosure in either header covering it. That makes this pass the width class's second consecutive breach, and my pass-2 reading does not survive it.

## My own side of D1

My pass-2 ruling does not survive. Attack by attack:

- **Against codex:** my reading holds only on pass 6's sentence taken alone.
  - It has real textual support: pass 6 accepted `&byte, len` as catchable debt that a contract line could discharge, and asked for "a len>8 row", singular.
  - It fails on the rest of the record. The warrant the ruling and I both used, "every width ≥ 4 is one body class", is not how this round enumerated. The parent's own class closure rowed len 4 and len 8 separately at every lane, both in the ≥4 class. It also answered `p_q8lane` with a len-8 row. I infer `p_q8lane` is len-8-specific from its name and from the fact that only the (8,3) rows kill it.
  - The parent's own L4 records that the closure's width set omitted 16/64/256/1024. Pass 6 then rowed one cell of that incomplete closure, at the address its mutants used. That is the #499 shape.
- **Against kimi on vc:** my reading fails.
  - Pass 6 graded `len <= 8` as L2, which is a floor breach, so it put {len > 8} into the floor.
  - The joint-cells rule crosses floor partitions with the partitions the body tests. The 09-09 amendment states it as "{labels} x the guard operand's body-tested partition". The body tests lane through `data[ofs]`.
  - So ({>8}, lanes 0-2) are floor cells, and their reachability is measured (l0w16, low16, l2w64, mc2).
  - My "condition on discharge" reframing needed a floor cell to lapse once an instrument can reach it. No rule says that.
- **Against kimi on ve:** kimi is wrong here. The body never compares the port to a constant (the parent's p_port10 class, ruled by the flagship seat). "The destination differs" would make each of 65,536 port values a cell, which the joint-cells rule excludes.
- **My own misgrade:** on pass 2 I graded the falsified DESIGNED TO CATCH sentence as L4. Clause (e), as your section 2 inlines it, grades a breach of the contract as L2.
- **Your least-certain point:** vc is the most certain L2, because it is the only escape that is L2 on both routes.

## (1) Rulings, one line each

- **F1 UPHOLD.** (d) and (h) are proved equivalent by derivation; the legs only fail to refute it. (h) is equivalent even with a wide read, because the #95 pre-zero plus ofs ≤ 3 < 8 already covers it, so "and no wide read" is unnecessary.
- **F2 REFINE.** Twelve is exact for the single-chunk (C, k, lane) projection (174,080 = 131072 + 32768 + 8192 + 2048 aligned starts). That projection drops two axes the measured escapes use: port (ve) and chunk position (vt2).
- **F3 UPHOLD.**
- **F4 UPHOLD.** The consequence nobody drew: clause (iii) is a disclosure. It takes va and vb out of the DESIGNED TO CATCH sentence, so correcting its warrant leaves them as disclosed debt, not breaches.
- **F5 OVERTURN the remedy.** A breach of the contract is L2 by your own section 2, and narrowing the contract after the measurement is the "argument about overclaiming" that (e) forbids. The finding also over-counts. Across the two headers taken together:
  - va and vb are disclosed by the width row's (iii);
  - vg and vt1 are disclosed by the parent's a<4:0> clause (lcaisasize);
  - ve is disclosed by the parent's p_port10 class;
  - only vc and vt2 are in-contract and undisclosed. They must be caught in-round; mc2 alone catches both (measured).
- **F6 REFINE.** Upheld against glm: no variant can turn `wide alive` red on its own. But it also scores only the last session. The retry at line 178 of `lca_widewrite_probe.py` fires on missing prints without checking `alive`, so a first-session host death gets retried away. The parent's detector helper `dsession()` retries only when `alive`; the width row copied the witness helper `run()` instead.
- **F7 UPHOLD.** See D3.
- **F8 UPHOLD.** Walked: 0x3ff << 5 = 0x7fe0, which is 32 mod 64. So a3 = 64 issues four 16-byte chunks, to ports 0x3ff, 0x3ff, 0x400, 0x400.
- **F9 UPHOLD (derived).** This rests on the pass-2 grep; src/ is unchanged at 3c41f01 (checked). The devices using PHYSICAL include no alphabook1 device except pccmos (1 byte, fixed address), and wdc, the only device a disk image adds, is not among them.
- **F10 REFINE.** "mc2 pins the width by construction" holds only through its MSR row: splitting chunk 1 into 4-byte chunks would leave s[14] there, not s[2].
  - Its SCR row is blind to a3 = 20, where chunk 2 becomes one 4-byte access that forwards the same s[19].
  - No single-chunk cell can pin C by its value, because a 4-byte chunk at the same address forwards the same s[lane].
  - Pin it with an assertion in the probe on the simulated chunk list.
- **F11 REFINE.** The condition is not order but observation-completeness.
  - If every chunk issued lands on an observed register whose preset differs from its shipped value, a clobbering fall-through is itself a red. Session-level detection is then sound in any order; only per-row attribution after the first red is unsound.
  - I never stated "{mc2 then kbc1024}". I said both fit in one session, and F11 was right to challenge that.
- **F12 UPHOLD.** Also, contract clause (i) under-claims: the row does pin which byte is selected (vf scored 2/3). Only delivery of other bytes before the lane byte goes unobserved.
- **F13 UPHOLD + REFINE.** An a2 that is 4-aligned but not 16-aligned issues four 4-byte chunks, so 12 of 16 bytes are dropped. The drop count is 15 / 12 / 0 for alignment 16 / 4 / other.
- **F14 CANNOT SETTLE.** `memory_alpha.c` is outside this pass's file list, and no leg of mine could observe it (ptbr == 0 throughout). It does not bear on D1.
- **F15 UPHOLD the filing.**
  - glm's direct-call harness is rung 1 and cannot see the producer axes (k, chunk order) where vg, vt1 and vt2 live.
  - My "fold into lcawidefold" option is unavailable under an L2 ruling, because it would defer an in-round obligation.
- **D1: L2-CLASS-CLOSURE** (reasoning above).
- **D2 UPHOLD.** A death before t4 always drops t4 as well, and nothing runs asynchronously at the debugger prompt. Add the retry defect from F6.
- **D3 UPHOLD F7, and I concede my pass-2 position.**
  - A device signature is a witness clause, and this row is a detector.
  - The stored byte only proves liveness.
  - The real discriminator is `wide getenv`'s 0x44 at the slot base: RAM would read s[0] = 0x41, and a missing device reads 0.

## (2) Which accepted dispositions are wrong

- **Wrong:** F5's remedy, and D1, which rests on it.
- **Wrong as stated:** F10 ("pins by construction") and F11 (the order condition).
- **Right count, wrong space:** F2.
- **The rest stand.**

## (3) What all nine of us missed

1. **The disclosures across both headers settle D1.** Clause (iii) and the parent's a<4:0> and p_port10 disclosures leave exactly vc and vt2 undisclosed. That is what makes D1 decidable.
2. **The retry discards a first-session death** (see F6).
3. **Every GETENV row anyone built reads a latch:** SCR, MCR, MSR, IMR and the 8042 command byte.
   - The parent's own rule is "a forward-count row needs a counter or an alternator, never a latch", so a len>8-gated DUPLICATE or ADD-OTHER escapes all of them.
   - The pckbc stub alternator (ports 0x61-0x6f except 0x64) can be reached by GETENV at C=16, 64 and 256 (for example 0x63, 0x62, 0x68), but not at C=1024. This is derived, not measured.
4. **Reachability is the reverse of how the debate weighted it.**
   - C=16 needs no `-o` at all: PROM_E_BOOTED_FILE returns the kernel basename, and `alpha_dummy.bin` is exactly 15 characters, which gives len 16.
   - C≥64 needs an operator-supplied string of at least 63 characters.
   - So vc, ve, vg, vt1 and vt2 are the more reachable escapes, and va and vb the least.
   - I checked the negative case too: `boot_string_argument` defaults to "" on Alpha (machine.c:508-523), so GETENV cannot hit a NULL strlen.
5. **A wide chunk never forwards a zero byte.** argv strings and basenames cannot contain NUL, and the terminator sits at offset len-1 ≥ 15 while the lane byte is at offset ≤ 3. So a variant keyed on data == 0 is equivalent at wide widths, and the contract can say "unreachable, derived".
6. **The shipped "any guard" clause was unsatisfiable when written.** A guard keyed on one exact port declines a len>8 write that no finite set of rows visits. That is a completeness claim, which (e) itself calls unfalsifiable; the replacement contract has to enumerate.
7. **No gate runs either probe** (the dated Alpha exemption in the pass-2 file summary). Every row argued about here runs only by hand, which is the #535 shape.

## The closure cell set

All of these were measured green on base in opus_p2, and each goes red under the variants named.

| Cell | Covers | Kills |
|---|---|---|
| frozen | C=16, lane 3 | vf and the two pass-6 variants (existing row) |
| l0w16 | C=16, lane 0 | vc |
| low16 | C=16, lane 1, port 0x21 | vc, ve |
| mc2 | C=16 lane 2 at k=16, then lane 3 as chunk 2 | vc, vg, vt1, vt2, vf; its MSR row pins width |
| l0w64 | C=64, lane 0 | va, vb, vc |
| l2w64 | C=64, lane 2 | va, vc |
| kbc256 | C=256, lane 0 | va, vc, ve, vw64 |
| kbc1024 | C=1024, lane 0 | every width threshold below 1024, plus vb, vc, ve |

- **Floor-minimal set:** {frozen, l0w16, low16, mc2}.
- **Minimal set that satisfies (e):** {frozen, mc2}.
- **Disclose, each with its warrant:**
  - k=16 at lanes 0, 1 and 3 (the discarded a<4:0> bits, lcaisasize);
  - ports other than those rowed (p_port10);
  - chunk position 3 and later (the handler holds no state);
  - data values (a wide chunk's forwarded byte is never 0, derived);
  - forward count at wide widths (every row is a latch; an alternator is reachable only at C ≤ 256);
  - the READ direction (no producer);
  - delivery of the non-lane bytes (lcawidefold).
- **Harness fixes owed with it:**
  - add the `alive` condition to the retry;
  - add a chunk-list assertion per cell.

I ran no new measurement. Every claim comes from the 102 legs in opus_p2 or is derived from the six allowed files, plus one targeted grep for the GETENV string defaults (item 4). I wrote nothing under GXEMUL-SEC. The scratch clone `/tmp/gxopus530p2` is clean: no `.MUTANT` sentinel, and its `dev_lca.c` matches SEC.