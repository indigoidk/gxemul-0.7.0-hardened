MYTHOSREGMEMC
model: Mythos 5.1 (claude-mythos-5-1)
VERDICT: REGRESS-BREACH. Eight green table-5 variants write a repair path's own latch under that path's own predicates (or under no gate) and were never classed by the ruling: it scanned the 517 UNFIRED/UNOBSERVED by family and treated the 148 NOCHANGE as no-ops. By the ruling's own test ("whether the gate's predicates and the target are the path's own") they are floor cells, and one short session closes all eight. Plus nine record findings, three of them wording.

**1. Evidence basis**

Packet blocks read in full: A, B, C1, C2, E, F1, F2, F3, G, H1, H2. Files opened in GXEMUL-SEC (read-only): src/devices/dev_mvme187.c (whole file); src/include/thirdparty/mvme_memcreg.h; regress/gate_arm.sh:76, :2086-2118; regress/lib.sh:70-88, :326-331; regress/mvme187_memc_probe.py (grep of :2, :8, :204-205, :241, :289, :425, :599, :662, :667); r5_20261105/table5/SCORES.txt:1-8, :17, :317, :570, :1334, :2886-2887, :2916-2919, :2931, :2936-2937, :2990, :2999, :3019, :3028, :3073, :3077, :3206, :3579-3580; table5/TALLY.txt; r5_20261105/PRETABLE_5.out:7788-7798, every `exact: none -- NOCHANGE` line (151 hits), :9455-9699; r5_20261105/memc_variants_5.py:78-134, :680-752; r6_20261105/gate_memc_comment.patch; r6_20261105/RECORDS6_NOTE.md:79, :156-185; r6_20261105/FILING_memccoverdebt.md:96-101; wiring_20261105/gate14_mvme187_memc.log:78-80. In the scratchpad kit: PROBE_IDENTITY_memc.md, staged/mvme187_memc_probe.py:1-12, DRYRUN_memc.out:3-42. Bash was denied, so no hash or count was run; every count below is read from an artifact or derived from block A.

Premises P1-P5, answered up front:
- P1 (floor list). CHECKED-IN-TREE dev_mvme187.c:70-141. Predicates: write :70 (head), fold :73, switch :93, write :105, !M :112, !D :127, write :132 (the value print), read :140 (tail). State read: chipid :96, chiprev :100, memconf :104, M :112, D :127. Nothing missing from the ruler's list except the default body's own direction test at :132, which the CONTRACT already counts as a "position's own test" and which the notice rows cover (R4/R14/R13 line texts, table 3's direction swap). The fold does rejoin at :73-76 before :93, so `controller` dominates no arm. I accept controller, len and idata bits as non-floor predicates. Note, though, that the floor's own cells still contain green variants (P2).
- P2 (no green variant inside the floor). FALSE. See section 2(d).
- P3 (B3 spelling). The source regex sees the verbatim spelling only. REASONED: `*((uint8_t *)&d->memcreg + relative_addr)`, `((uint8_t *)d)[relative_addr]`, or an `off = relative_addr; p[off]` rewrite carry neither pattern. The run-time rows are spelling-independent but layout-dependent, so only the joint (new spelling × latches moved away from +0x7c) escapes both. Clause (b) is verbatim, so this is a contract disclosure, not a floor matter. The gate comment should say "the old read's spelling" (record item 9).
- P4 (null medium). The three binary media are measured, CHECKED-IN-TREE SCORES.txt:3-5, each CONTROL=FAIL. A build without the device is NOT a CONTROL=FAIL medium: the control rows are the session and pc rows (block A :415, :417), and a device-less build exits 0 with pc advanced. It reds the four `ctl * r2` rows instead (memory_rw zero-fills, per H2). The record should read `(c): measured at r5_20261105/table5/SCORES.txt:3-5 (binary media); a device-less build reds ctl chipid/chiprev/memconf/ctl1id r2 by construction, unmeasured`.
- P5 (every pin can fail). True by reasoning, but H1 does not replay it for four pins: "probe completed", "sentinel once", "rows run" and "rows emitted" are green in all twelve H1 legs (DRYRUN_memc.out, every leg printed the sentinel and ran 206). Their failability is REASONED from block B :788-794, :801. See section 3.

**2. The vacuity floor, clause by clause**

(a) Pre-fix build fails. CHECKED-IN-TREE SCORES.txt:2: HEAD 29/206, SYMPTOM=PRESENT. H1: 181 of 216 checks red, and the count reconciles (177 rows + rows correct + symptom + green + red). Discharged.

(b) Verbatim reinstatements. B1: SCORES.txt:6, 79/206; B2: :7, 42/206; B3: :8, 202/206, RED = R3 7c r4, R8 7c r4, R8 80 r8, R11 180 r4, exactly the four the header names. H1's B3 leg shows 7 fails: those four rows plus rows correct, green, red. Discharged. The mechanism is sound: struct memcreg is 31 registers × 4 bytes = 124 bytes (mvme_memcreg.h:31-98), the two `int` latches sit at +0x7c and +0x80 (dev_mvme187.c:54-55), so on a little-endian host +0x7c reads 1 after a memconf store and +0x80 reads 1 after a default access; R8 7f/83 cover the big-endian byte. +0xff is 123 bytes past the 132-byte allocation, as the header says. Layout dependence is pinned by the struct comment (:49-53) and disclosed (block A :228-230). The source check (block B :805) catches the verbatim spelling only (P3).

(c) Null medium. Discharged for the binary forms (SCORES.txt:3-5); the device-less form is reasoned (P4). The row arithmetic matches: /bin/true passes the 23 "exit0" session rows plus the four negative-text rows (R3 no 0x5, R3 no 0x0, R9 no wide, R6 lines) = 27; an absent binary passes only those four; /bin/false adds neg apparatus = 5.

(d) Null-repair over the DEPENDS-ON floor. BREACH. The 148 variants PRETABLE_5 classes NOCHANGE were never placed family by family; the ruling's (b) justification reads "Each has a foreign target, a foreign latch in the gate, or an untested idata/offset bit as its only discriminator" (block F1). CHECKED-IN-TREE, eight NOCHANGE variants have none of those and all score 206/206:

| variant | position | gate | target | SCORES.txt |
|---|---|---|---|---|
| L_MB_M_xori_any | after `warned_memconf = 1` | none | M | :2916 |
| L_ME_M_xori_any | memconf arm's end | none | M | :2917 |
| L_DB_D_xori_any | after `warned_default = 1` | none | D | :2918 |
| L_DA_D_xori_any | default arm's end | none | D | :2919 |
| L_MT_M_xori_M | memconf arm, before the write block | M | M | :2936 |
| L_MW_M_xori_M | inside the write block | M | M | :2937 |
| L_DT_D_xori_D | default arm, before the latch test | D | D | :2931 |
| L_DT_D_idat_W.D | default arm, before the latch test | W.D | D | :2990 |

Positions per memc_variants_5.py:82-98, :116-125. Each is a nonvacuous insertion (built, so it passed semantic_vacuous at :703-728) that writes the path's own latch under the path's own guard predicates or none. That is the cell (write, M) or (!D, D) of the ruler's own product, and the ruler applied exactly this test to NB4: "memconf is the memconf path's own state, so the ungated and write-gated `&=` keeps ARE floor" (F1 (d)). None is a semantic no-op. REASONED from block G: a first store of 0x01 to either category leaves the latch at 1 ^ 1 = 0 under the four ungated toggles, so the next access re-announces; a non-first store of 0x01 does the same under the three gated toggles; a non-first default store of 0x00 clears D under L_DT_D_idat_W.D. The probe's store values (0x00, 0x05, 0x07, 0x5a, 0xff, 0xffffffff) never XOR a set latch back to zero and never make a non-first default store of zero, which is why all eight are green. Contrast SCORES.txt:317: L_DB_D_idat_W (the same assign without the D conjunct) is red on R14 lines because R14's first store is zero; the W.D form moves the clearing to a non-first store, which no row makes.

This is one measurement away from settled, and the main loop can run it: add one session, say R18, with ST_B 0x01, ST_B 0x01, ST_B 0x00 to +0x18 then LD +0x18, and the same three stores and a load at +0x08 (seeds r5 = 0x01, source r0 for the zero). Rows: `R18 lines` want "2", `R18 18 rN` want 0, `R18 08 rN` want 3, both notice texts (": 0x1 (once) ]" and "memconf write 0x1 (controller 0)"), pc CODE + 32. REASONED: the fix announces once per category; each of the eight re-announces at least once (walked statement by statement above), so `R18 lines` reds every one. Then re-run the 665 green representatives against the widened probe.

Rows owed per enumerated wrong version, never per state: these are eight enumerated, built, measured variants, not states. If the owner instead holds codex's narrower bound (an insertion is in bound only if it restores a removed operation or is a direct null repair, block F2), all eight become debt and this review's verdict drops to REGRESS-WITH-FINDINGS. The ruling of record rejected that bound (F1, "On codex's bound argument"), so I rule by it.

(e) Contract true and complete. Three sentences are false as written:
- The COVERED clause (block A :146-151) claims red for "any NONVACUOUS single statement ... that ... toggles or value-assigns either announce latch ... under no gate or under a conjunction of the position's own tests (direction; ...; the latch the position's arm reads)" except cells disclosed below. L_DT_D_idat_W.D (direction × own latch, value-assign) is green and disclosed nowhere: family (2)'s only latch clause is "a latch written from an arm that does not read it", and DT's arm reads D.
- The same clause claims red for keeps "under a single store-value or offset bit the probe's values drive". About a hundred NOCHANGE keeps (K_*_or/xor_ib0c, K_*_and_ib0s/ib1s/ib10s, K_*_or/xor_ib1c/ob0s, PRETABLE_5.out:8214-8574) are green because the only driven value is the operator's identity (e.g. K_MW_memconf_or_ib0c: bit 0 clear only on 0x00 stores). They are debt by the ruler's rule but belong to none of the five families as worded.
- The cross-call caveat (:179-183) and FILING item 6 ("one inside the 665") name L_ME_M_xori_any alone; PRETABLE_5.out:7789-7798 has four ungated `^= idata` toggles inside the 665. The seven toggles are swept into family (2) only by the clause "or which lands on a set latch", added at records 6 without the foreign-target/foreign-gate argument that justifies the rest of (2).
NB3, NB4 and the two undriven contexts check out against the instruction lists (no controller-0 memconf store in state (1,0); no controller-1 default store in (1,1)); the arithmetic 112 + 3,463 = 3,575, 2,798 + 665 = 3,463 and 3,518 + 56 + 1 = 3,575 reconciles with TALLY.txt.

(f) Anchors. The four `ctl * r2` rows and R6's six pin which offset reaches which field; R12 w00 and h08 pin width. If every offset shifted one word, ctl chipid r2 reads 0 and R4 0c reads 3: red. If the fold mask narrowed, D7_fold shows the rows (SCORES.txt:17, 31 red, led by ctl ctl1id r2 and R6 100/104/108). If the window shrank below 0x200, the controller-1 rows zero-fill and red, while R11 180 r4 would turn green rather than red, which is why that row is a B3 anchor, not a window anchor.

**3. Gate 14's memc block**

CHECKED-IN-TREE: the working tree's checks at gate_arm.sh:2099-2118 are byte-for-byte block B's; the comment differs exactly by gate_memc_comment.patch, whose hunks produce block B's text. `check` is string equality (lib.sh:80-88); `count` is plain `grep -ac --` (lib.sh:326-331), so the per-row pattern `^$v  .*ok$` is BRE with no metacharacters in any row name, and the two-space anchor works because `%-18s` pads every name of at most 16 characters (probe :205, :308).
(i) Dead probe: no sentinel, "probe completed" no≠yes, red. (ii) Silently lost rows: RESULT=205/205, "rows run" 205≠206, red, plus the missing row's own pin. (iii) Added row: "rows run" and "rows emitted" 207, red. (iv) Sentinel without RESULT: mcres is empty, "rows run" ""≠206 and "rows correct" ""≠"206", both red.
Pin that cannot fail: none by name, but the else-branch instantiation `check "mvme187 memc probe completed" "yes" "yes"` (block B :791) is a tautology; the pin's red form is the if-branch only. Cosmetic.
H1 shows what it claims for the legs it lists; DRYRUN_memc.out:3-4 matches. It does not demonstrate failability of the four pins named under P5. The comment is true after the patch (206, fifteen sessions, R3-R17, R8's twelve bytes) except its last parenthesis, "every one in a debt family the probe's CONTRACT discloses ... zero floor cells survive", which section 2(d) and 2(e) contradict. In-situ status: the only in-situ run is 74/74 (wiring_20261105 log :79); RECORDS6_NOTE.md:160-161 owes the 206-row run at landing. UNSETTLED until that run prints 216 checks, 0 fails.

**4. The tables**

No row is vacuous by construction: every row's observable varies under some table-5 variant, including the negative-text rows (red under per-controller latches) and R6 lines (red under served-read latch sets). R8 84-87 vary only with allocator contents under B3 and were green there (SCORES.txt:8); the header discloses this. B3's credit matches SCORES.txt:8 exactly; D7_fold's MISS is a stale R7 lines prediction, as VERDICT.md says, and SCORES.txt:17 confirms R7 lines is not in its red set. The 665: 517 UNFIRED/UNOBSERVED representatives are each in a family with a foreign gate, foreign target or untested bit (survivor summary :9461-9697 read line by line; every gate carries nD, M, C or an ib/ob literal, or sits at a served arm, H or TL). The 148 NOCHANGE are not: eight are floor (2(d)), roughly a hundred are undisclosed identity-driven keeps (2(e)), and the rest are foreign-gated toggles and assigns that fit (1) or (2).

**5. Records**

1. CONTRACT COVERED clause false for L_DT_D_idat_W.D (green, undisclosed). L4.
2. CONTRACT and FILING item 6: "one inside the 665" is four (PRETABLE_5.out:7789, :7792, :7795, :7798). L4.
3. FILING item 6's R19 (stores 0x03 then 0x02) closes only L_DA_D_xori_any and L_ME_M_xori_any; at MB and DB the second store never reaches the inserted line, and the gated toggles need a non-first 0x01. No remedy is filed for the "lands on a set latch" group. L4; superseded by the R18 sketch above if 2(d) is upheld.
4. Ruling F1 (b)'s universal justification sentence is false for the seven own-latch toggles; the gate comment's "zero floor cells survive" and VERDICT errata item 3 inherit it. L4 (L2 upstream).
5. The ~100 identity-driven NOCHANGE keeps are green and in no disclosed family; the COVERED clause's "bit the probe's values drive" needs "nonvacuously". L4.
6. H1's caption and packet :34-35 cite regress/artifacts/mvme187memcoob/landing_20261105/, which does not exist in the tree (Glob: no such directory); the dry-run, identity proof and staged diffs live only in _scratchpad/wmemc/landing/. L3: bank them before the commit.
7. P5's "block H1 replays it": four pins never red in H1. Wording.
8. Clause (c) record form per P4. Wording.
9. Gate comment "layout-free guard against the old indexed read": add "in its old spelling". Wording.
Other ruling sentences the probe still carries (the two undriven contexts, R10's 0x5a, R17's even word stores, NB3, NB4 arithmetic) check true against the instruction lists.

**6. The main loop's dispositions**

The zero-floor disposition is wrong by the ruling's own test, on the eight variants above; everything codex, Gemini and the ruler argued about the 517 stands. rec6-rec9 were scoped to the 517's records and to ME's one variant (RECORDS6_NOTE.md:178), so the chain never asked whether the NOCHANGE class contained own-gate/own-target cells. The codex rec7 finding that the filing's reasons "cover every survivor" was fixed by deletion; the gap it pointed at (L_ME_M_idat_W.nC fitting no reason) is the same gap these eight sit in.

**7. Weakest finding**

The floor classification in 2(d). It rests on the F1 test being the operative definition and on reading "never per possible state" as not excluding a value-specific catch of an enumerated variant. It is overturned if the owner adopts codex's bound (insertions in bound only when they restore a removed operation or are a direct null repair); then the eight are debt, record items 1-5 still stand, and the verdict is REGRESS-WITH-FINDINGS. The measurement that settles the rows is the R18 session against the eight rebuilt variants.

MYTHOSREGMEMC: 20 CHECKS 2 FLOOR-BREACHES 9 RECORD-FINDINGS VERDICT:REGRESS-BREACH
