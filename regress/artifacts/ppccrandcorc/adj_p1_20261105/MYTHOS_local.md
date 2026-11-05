MYTHOSADJP1R575
model: Mythos 5.1 (claude-mythos-5-1)
VERDICT: APPLY-WITH-CHANGES -- the two expression edits are correct and sufficient; the probe owes four rows, the floor owes four more variants, and three premises in the brief's census are false (none touches the defect claim). `ppccrlogicshift` is FILED, not joined. GLM's "58/58 unreachable" finding is wrong.

1. THE FIX

The defect is as stated. `cpu_ppc_instr.c:2735` sets CR[BT] on `!(ba & bb)` (NAND) and `:2762` on `!(ba | bb)` (NOR); the crorc body at 2756-2764 is byte-identical to crnor at 2765-2773. Book I at `ppc_uisa_book1_v201.txt:1909` reads `CRBT <- CRBA & ~CRBB` and `CRBT <- CRBA | ~CRBB`, with prose at 1911-1914 naming the complement on BB. Walked: crandc arch 0,0,1,0 vs HEAD 1,1,1,0 (DISC at 00, 01); crorc arch 1,0,1,1 vs HEAD 1,0,0,0 (DISC at 10, 11). The witness's ten reds at `WITNESS_head.out:12-13,18-19,48-49,52-53,58-59` are exactly those cells.

[R1] The exact changes: line 2735 becomes `if (ba & !bb)` and line 2762 becomes `if (ba | !bb)`. Nothing else in either handler changes. `ba`/`bb` are masked to 0/1 at 2732-2733 and 2759-2760, so `!bb` is the exact complement and the walk gives the arch column on all four rows. Reads precede the clear (2732-2734), so BT==BA or BT==BB aliasing is order-safe. Decode is reached only via `:4638` and `:4641`; CRNAND (225, `opcodes_ppc.h:59`) is absent from the case list at 4629-4635 and falls to `default: goto bad` at 4648. There is no POWER-mode path: `cpu_ppc.c:96` sets `mode = MODE_PPC` unconditionally and the `power` flag at `cpu_ppc.c:608` lives only in the disassembler. P2 is settled.

Second defect: yes, latent. `1 << (31-bt)` at bt=0 is a signed `1 << 31`, undefined under C11 6.5.7p4, at 14 sites across all seven handlers (2725-2727 through 2779-2781); `cr` is `uint32_t` (`cpu_ppc.h:126`). On the gcc build it behaves (the witness's edge rows ran at bt=0 and bt=31).

[R2] `ppccrlogicshift`: FILED. Same device, yes. Same semantic class, no: representation hygiene versus a wrong boolean function. Same detector, no: the un-fixed shift produces the architectural result on this toolchain, so no row of this probe can red under its reinstatement; its instrument is `-fsanitize=shift` or an unsigned-type review, not a CR truth table. Two of three legs fail. The fix must NOT switch just these two handlers to `1u <<` (codex's "unnamed alternative"); that would partially repair a 14-site defect inside this round and spoil the other round's witness. Deepseek's in-round ruling is rejected on the same grounds. `ppccrnandundec` stays out as the brief says (CPU-STOP class, xo 225 not run here, `ppc_crlogic_probe.py:27-29`).

2. THE DETECTOR

The 58-row probe is the right instrument in kind: real decoder, real guest, two widths (the second copy is the same source compiled with `DYNTRANS_DUALMODE_32`), inverse pre-set so a pass requires a write. The 58 is real: 6 apparatus + 12 (64 table) + 24 (siblings) + 4 (edge) + 12 (32 table), and 48 = 6 + 8 PIN + 24 + 2 + 8, matching `WITNESS_head.out` line by line.

[R3] GLM's finding that the crandc edge row aliases its destination with BA is FALSE. The edge row is `XL("crandc", 0, 2, 3)` at `ppc_crlogic_probe.py:238`: BT=0, BA=2, BB=3, as the comment at 231-232 says. GLM applied the truth-table pick (BA=0 for a=0) to a row that does not use it. 58/58 is reachable on the fixed build.

[R4] Rows OWED (4):
- `64 crandc hi` and `64 crorc hi`: one row per handler with BA, BB >= 16 and every proper-submask alias bit (indices `& 15`, `& 7`, `& 3`, `& 1`) seeded to the opposite value. Every current row uses BA in {0,1,2,4} and BB in {0,1,2,3,5} (`:162`, `:238`), so a one-character mask weakening `& 31` to `& 7` at 2731 or 2758 scores 58/58 today. Four seats found this independently. One width suffices; the 32-bit copy is the same source.
- `edge mfcr` and `edge disasm`: the brief's §3 claims an mfcr row and a disasm row per session. The edge session runs `MFCR(10)` and captures `edis` (`:238`) but scores neither (`:240-245`). Either the rows are added or the premise is withdrawn; I rule they are added, since `edge disasm` is the only encoder pin at the BT field extremes.

VACUOUS by construction (channel cannot vary under the named variant):
- Under every variant in the floor: the 20 sibling rows, 6 apparatus controls, 4 session rows, 3 disasm rows (disassembler is `cpu_ppc.c:823-830`, untouched), 3 mfcr rows (both channels read the one `uint32_t`; they agreed on HEAD's wrong values too, witness line 21), and 3 others rows (no floor variant writes outside BT).
- Under (d) complement-swap and under complement-drop: both edge rows. Inputs (0,0) and (1,1) are fixed points of those mutations (walked: `!0&0=0`, `0&0=0`; `!1|1=1`, `1|1=1`).
- Under a single-site (b): every row of the other handler, and the two PIN rows of the restored handler.

Null medium: identity bodies for both handlers (brief §5c) is correct. Predicted 18 red (16 truth + 2 edge), 40/58; the owed hi rows, pre-set inverse, make that 20 red of 62. It also doubles as the proof of P4: a row reds under the null exactly because the pre-set is the inverse. Grok's narrowing is right and harmless: on HEAD the DISC rows (including both edges) cannot distinguish "wrong write" from "no write"; post-fix every row can.

Controls: the six apparatus rows (`:213-222`), the session rows, the disasm rows and the 20 sibling rows (all `control=True`) feed `PPC_CRLOGIC_CONTROL`; `others`, `mfcr` and edge rows are scored but not controls (`:194-197`, `:241-245`). That split is right.

Recommended, not owed: seed background ones in bits that are neither sources nor destinations so `others` can see an extra clear (today it sees only extra sets, since the seed is 0x50000000 outside the destinations; grok's `& ~1u` escape); one preset-true row per handler to catch codex's toggle escape `cr ^= (1 << (31-bt))`; the other-diagonal edge rows (crandc bt31, crorc bt0) belong to `ppccrlogicshift`, which needs a bt=0 set-path pin that this probe lacks.

3. THE TEST-VARIANT TABLE (bounded to lines 2729-2737 and 2756-2764)

[R5] Nine variants, each from the fixed build, red rows on the 58-row denominator (the owed rows stay green under all nine):

| # | variant | red rows | n |
|---|---|---|---|
| b1 | crandc `!(ba & bb)` restored | 64/32 crandc 00, 01; edge crandc bt0 | 5 |
| b2 | crorc `!(ba \| bb)` restored | 64/32 crorc 10, 11; edge crorc bt31 | 5 |
| c | both bodies identity | 16 truth + 2 edge | 18 |
| d1 | crandc `!ba & bb` | 64/32 crandc 01, 10 | 4 |
| d2 | crorc `!ba \| bb` | 64/32 crorc 01, 10 | 4 |
| d3 | crandc `ba & bb` (complement dropped, collapses to crand) | 64/32 crandc 10, 11 | 4 |
| d4 | crorc `ba \| bb` (collapses to cror) | 64/32 crorc 00, 01 | 4 |
| d5 | crandc `ba \| !bb` (operator crossed with crorc) | 64/32 crandc 00, 11; edge bt0 | 5 |
| d6 | crorc `ba & !bb` (operator crossed with crandc) | 64/32 crorc 00, 11; edge bt31 | 5 |

d3/d4 are kimi's addition and are the defect's own class (a handler computing a sibling's function). d5/d6 are the copy-paste risk between two lines edited in one round. No predicate dominates either edited line (the `if` is the only branch), so clause 1 of the bound at `tools/CLAUDE.md:1448-1451` adds nothing. Clause 2 bt-substitutions (`bt & !bb`, `ba & !bt`, `bt | !bb`, `ba | !bt`) each red an existing row by enumeration (64/32 crandc 10 for the first two; 64/32 crorc 01 and 00 for the last two); list them in PRETABLE as predicted, not built. GLM's `~bb` is not a variant for crandc: `ba & ~bb` with 0/1 operands equals `ba & !bb` on all four rows, so it has no channel; for crorc it is caught by row 01.

4. SEAT FINDINGS AND FALSE PREMISES

Right: the two expressions (all six seats, by enumeration); the 58 census (codex, grok); the PIN overcount (codex, grok); the edge session's unscored mfcr/disasm (codex, `:238-245`); the field-mask escape (codex, grok, GLM, minimax); the complement-drop variant (kimi); `others` blind to extra clears and the toggle escape (grok, codex); the shift is real but a different class (codex, grok, GLM, kimi, minimax); POWER mode settled from `cpu_ppc.c:96` (codex, grok).

Wrong: GLM's aliased-edge finding (R3) and GLM's claim that crandc `ba & ~bb` fails at (1,0): `1 & ~0 = 1`. Minimax's claim that `!ba | bb` gives 0,1,0,1 and reds three rows: `!0 | 0 = 1`, so it reds exactly 01 and 10, and the brief's §5d prediction stands. Minimax's 50-or-70 denominator: the witness shows 58. Deepseek's in-round shift fix (R2) and its `bt != 15` mutant: BT=15 is `64 crorc 11` (witness line 19), which reds it. Kimi's ledger arithmetic is right in spirit but its 40/50 totals omit the four session rows.

[R6] False premises in the brief: (a) "the four PIN rows of each handler at each width" is two per handler per width, eight total (witness 14-17, 54-57); (b) "an mfcr row per session" and "a disasm row per session" are false for the edge session; (c) the §3 passing census omits the four session rows and does not sum to 48 as written. P1, P2 and P4 hold. P3 is not settleable read-only; the measurement to name is the post-fix full battery with every other gate unchanged green. Also note for the dependent round: `ppccrnandundec`'s draft sketches `!(ba & bb)` as the crnand body, which is today's crandc; it must not alias `instr(crandc)` once this lands.

5. VERDICT

[R7] Gate 13: keep the parse-before-score shape, CONTROL=OK and the sentinel, and equality on both halves, but re-pin at the new total (62/62) after the four owed rows land; 58 is not the number to freeze. [R8] Write PRETABLE.out with the row manifest (BT, BA, BB, seed per row) and the nine-variant table before any variant is built. [R9] Correct the three §3 premises in the brief. [R10] Ship the two expression edits exactly as proposed, with no other source change.

APPLY-WITH-CHANGES: the design stands; the changes are the four owed rows, the four added variants, the re-pin, and the census corrections.

MYTHOSADJP1R575: 10 RULINGS 4 ROWS-OWED 9 VARIANTS VERDICT:APPLY-WITH-CHANGES
