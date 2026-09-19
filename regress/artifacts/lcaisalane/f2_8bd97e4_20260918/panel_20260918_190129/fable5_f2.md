<!-- fable5 (Agent tool, model fable), #530 pass 2 + §F2 adjudication, 2026-09-18.  CAPTURED FROM THE AGENT'S
     COMPLETION NOTIFICATION (its transcript file did not carry the final message); the notification's XML escapes
     (&amp; &lt; &gt;) are decoded below and nothing else is changed. -->

I have verified the load-bearing facts. Notably: `p_port10` and `lcaisasize` are **pre-existing flagship-ruled disclosure classes** in the parent probe header (not inventions), the F9 producer census holds on alphabook1 (GETENV is the only guest-driven `store_buf` caller whose destination is guest-supplied and can reach the sparse window; `machine_alpha.c`'s `store_buf`s target fixed non-window addresses), and the multi-chunk arithmetic confirms the F10 pin cannot be by forwarded-byte value. Here is my adjudication.

---

`FABLE_SEAT_530F2_LIVE`
`claude-fable-5-1` (Fable 5.1)
`# CHECKPOINT -- 2026-09-18 19:3x   HEAD: 3c41f01 records: 8bd97e4's pass 2 -- DOES NOT CLOSE; the width row covers one of twelve reachable cells, and the rule question goes to the §F2 pass and fable5`

**R1: L2 for `vc` ONLY; `va/vb/ve/vg/vt1/vt2` are clause-(e) debt — warrant: the joint-cells letter (2026-09-09 label-axis) makes LANE a floor axis because `data[ofs]` distinguishes all four lanes; width/port/k/chunk-position are not body-distinguished, so they are disclosed against already-ruled classes.**

**R2: Floor closure = the four C=16 WRITE lanes {frozen(L3, shipped), l0w16(L0), low16(L1), a lane-2 cell} + an explicit store_buf chunk-list assertion. The lane-1 cell IS owed; kbc1024, k=16 and the continuation cell are NOT floor — warrant: {mc2,kbc1024} is a COVERING that a lane-1 exemption escapes, and no forwarded-byte value can pin width.**

**R3: Narrowing to escape the `vc` floor breach = NO (laundering); correcting the OVERCLAIMING contract to an honest, warranted form = REQUIRED (L4) — warrant: available iff the variant's operand is not body-distinguished, so it fits `va/vb/ve/vg/vt1/vt2` and never `vc`.**

**R4: FIX the exit code in the closure diff, not records — warrant: records TODAY (nothing consumes it) but the closure ships NEW detector rows, and one line prevents shipping them behind a runtime false-pass generator.**

**R5: Discharge the `len==0`-DROP half now (M1_lenzero 352/352, EQUIVALENT-by-no-producer, guard stays as a defensive `%0` guard); the width half is NOT independently dischargeable — it IS the D1 obligation and closes with the closure diff. Missing = the diff itself.**

**R6: The chain closes on the first VALID pass (diff delivered, roster complete, zero WITH its denominator) that VERIFIES THE ENUMERATION against the shipped composite — specifically kills the lane-1 covering-escape and confirms no lane cell open — bounded because the floor is a finite 4-cell lane cross-product closed in ONE diff.**

**R7: E-DEBT is correctly overturned (not over-correction — `vc` is a measured floor breach), but do NOT over-correct to the panel's loudest answers: {mc2,kbc1024} is refuted as a closure and "all seven are L2" over-counts. Your F5 remedy and the filed pair are the SAME #499 error the provisional made from the other side — closing at the address the mutant used, not closing the partition.**

---

## Detail

### D1 — the ruling, and why it is narrower than the panel's headline

The panel is right that E-DEBT-PLUS-L4 does not survive, and I verified the mechanism rather than counting the 8–0: `vc = && (len<=8 || (P&3)==3)` scores **frozen 3/3** because lane 3 keeps `(P&3)==3` true (forwards `s[3]=0x44`), and **l0w16 2/3** because lane 0 makes it false at `len=16>8`, dropping the store into the read arm (SCR keeps its preset). That is a *per-lane null of the repair, invisible at the lane the row occupies* — the `sgimtedepth4dead` `&& dst_tlb==MTE_TLB_A` shape exactly, and `#499`'s "repaired at the address the mutant used." Lane is the guard operand's body-distinguished partition (`byte = data[ofs]`, `ofs = P&3`), so by the 09-09 amendment `{write guard} × {lane 0-3}` is floor. **L2, class closure owed.**

But the panel splits into two errors on either side of the right answer, and both favour finishing:

- **"All seven guard-variants are L2" (glm, deepseek, minimax)** over-counts. They are right that you cannot silently narrow an overclaiming contract, and right that F5's *remedy wording* is laundering-shaped. They are wrong that `va/vb/ve/vg/vt1/vt2` need rows. Only `vc`'s operand (lane) is body-distinguished. Width thresholds (`va/vb`) are a partition the body never tests (it tests `len` only against 0); port (`ve`) is a passthrough into the forward address, not a tested partition — that is the parent's already-ruled `p_port10` class; `k`/a<4:0> (`vg/vt1`) is discarded by `>>5` — the parent's already-ruled `lcaisasize` class; chunk-position (`vt2`) is not a body-read lvalue (the handler is stateless across calls). I confirmed `p_port10` and `lcaisasize` are pre-existing flagship-ruled disclosures in `lca_isalane_probe.py:196,199,209`, measured 51/51 and 93/93 — so disclosing these six is citing settled classes, **not** inventing an escape hatch for this measurement. That is the line between honest disclosure and laundering.

- **{mc2, kbc1024} as the closure (agy, deepseek, minimax, and your filed pair)** is a covering, not a closure — and grok and glm proved it with a checkable mutant: `&& (len<=8 || (P&3)!=1)`, the *same clause-(d) form as vc*, passes both sessions, because `mc2` drives lanes 2/3 and `kbc1024` drives lane 0 — **neither drives lane 1 at a wide width.** Only `low16` (8259 IMR, port 0x21, lane 1) reds it. Shipping that pair as "class closure" replays `#499` at lane 1 on the next pass. This is the sharpest thing on the table and only grok/glm/codex reached it.

So `vc` is the only floor breach; the closure is the **lane** cross-product, not "width" and not "all seven."

### R2 — cell set, the lane-1 cell, and the F10 pin (the part with real arithmetic)

Floor-minimal set (each measured green on base by Opus, each reddens the lane class): **{frozen (L3, shipped), l0w16 (L0), low16 (L1), a lane-2 wide cell}**, in one diff. `low16` is non-negotiable — it is exactly the cell {mc2,kbc1024} omits. Prefer a **k=0** lane-2 cell (any port `P&3==2` at a 16-aligned k=0 address, e.g. 0x2fe MSR) so the floor cells do not entangle the *disclosed* k axis; `mc2`'s lane-2 chunk sits at k=16, which is convenient (it also catches `vg/vt1/vt2` for free) but couples a floor cell to a disclosed dimension. `kbc1024`, `k=16` and the continuation cell are **not** floor — they are the disclosed remainder.

The **F10 width pin cannot be by forwarded-byte value**, and this defeats "mc2 pins width by construction":
- A `a3=4` single 4-byte chunk at the frozen address forwards `(0x2ff&3)%4 = 3 → s[3] = 0x44` — identical to `a3=16`. So editing the width down is invisible to the value.
- `mc2`'s SCR readback cannot distinguish `a3=32` (16+16) from `a3=20` (16+4): both forward `s[19]` to the SCR (chunk 2's `ofs=3` picks `s[16+3]` at C=16, and `s[16+3]` at C=4 alike). codex's finding, verified.
- `mc2`'s MSR row distinguishes one-16-byte-chunk (`s[2]`) from four-4-byte-chunks (`s[14]`) but **not** from one-4-byte-chunk (`s[2]` again).

So the pin must be an **explicit assertion in the probe on the reconstructed `store_buf` chunk list** (assert the chunk that lands the observed byte has length > 8), per Opus and codex. Contract discloses, each with its warrant: widths >16 (joint-cells + the measured ladder); ports (p_port10); a<4:0>/k (lcaisasize); chunk position ≥2 (stateless handler); the READ side (F9, no wide-read producer); non-lane byte delivery (lcawidefold); data values (a wide chunk never forwards NUL — argv/basename carries no 0, and the lane byte sits at offset ≤3 while the terminator is at ≥15).

### R4, R5, R6 — the smaller calls

**R4:** Your "records" is right about today (check_probe_wiring exempts it; no Alpha gate; the convention parses `WIDEWRITE_RESULT`), but the closure ships new rows and `sys.exit(0 if ok==len(rows) else 1)` is one line. glm/grok's escalation is upheld: don't ship new detector rows behind a runtime exit-0-on-FAIL. Add it with the closure. Same bucket: the retry at `lca_widewrite_probe.py:178` fires on missing prints **without checking `alive`** (Opus F6) — the parent's detector helper retries only when alive; the width row copied the witness helper. A first-session host death gets retried rather than recorded. Fix both in the closure.

**R5:** The `len==0`-DROP sub-question discharges now: `M1_lenzero 352/352` is EQUIVALENT-by-no-producer (store_buf bottoms at 1 byte; a CPU access is ≥1 byte), the guard is a cheap defensive check against a `%0` that no producer can trigger, **it stays**, no row owed, disclosed with that warrant. The width sub-question is *not* separately dischargeable — it is the D1 floor obligation. The HELD item therefore closes when the closure diff lands with its pass 2; what is "missing" is the diff.

**R6:** Per the repair-chain rule as amended for `#499`: the closure is ONE diff rowing the whole lane cross-product (not cell-by-cell), the contract enumerates covered (4 lanes) vs disclosed (the six classes above), and the closing pass VERIFIES THE ENUMERATION — it must (a) have the diff delivered (guard against the `git show | head` blinding), (b) full roster or misses named, (c) report zero WITH the denominator, and specifically (d) kill the lane-1 covering-escape `&& (P&3)!=1` and confirm no lane cell open. It is bounded because the floor is a finite 4-cell partition closed at once; it cannot become `#392`. One enabling artifact kimi flagged and I uphold: **ship mc2's per-row labels** so the lane-2/lane-3 attribution inside its 5/5 is auditable — the current table's aggregate is not.

### R7 — have you over-corrected? No on the direction, yes if you rubber-stamp the panel

Overturning E-DEBT is correct: `vc` is a measured floor breach on the joint-cells letter itself, independent of any contract wording, so your provisional "uncatchable is now a discharge condition" reading does not survive (no rule lets a floor cell lapse once an instrument reaches it). That is not over-correction.

The over-correction risk is *adopting the panel's modal outputs*. The provisional let one lane-3 row stand (too little); {mc2,kbc1024} covers the listed variants without closing the lane partition (the `#499` shape again, from the other side). Both close **at the address the mutant used** rather than closing the partition. The disposition of yours most wrong is **F5's remedy as phrased** ("narrow to what the rows measure") — that justification is laundering-shaped and cannot touch `vc` — together with **filing {mc2,kbc1024} as the closure**. The finding F5 is right (contract breached); its remedy and its D1 consequence are wrong. Correct ruling: one floor class (lane), four cells + a chunk-list pin, exit-code and retry fixes, and an honestly-warranted disclosure of the other six variants — narrower than the loudest seats, and it is grok's cell set with Opus's construction fixes.

**What all nine (and I, until I checked) under-weighted:** the disclosure warrants for `ve/vg/vt1` are only legitimate because `p_port10`/`lcaisasize` are *already-ruled* classes — if they were not, F5's narrowing would be indistinguishable from laundering and glm/deepseek/minimax would be right that all seven need rows. The ruling therefore rests on those two parent-header classes being sound; they are (measured 51/51, 93/93), so the disclosure holds — but the closure's contract must **cite them by name**, or a future reader sees six variants "narrowed away" with no warrant and reopens the whole argument.
