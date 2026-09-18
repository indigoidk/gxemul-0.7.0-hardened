# lcaisalane F2 -- the Fable 5 seat, FIRING LAST as adjudicator (Agent tool)

*** TRANSCRIBED BY THE MAIN LOOP (the Agent seats leave no file).  VERBATIM from the returned answer. ***

Liveness, three lines as required:
```
FABLE_SEAT_ALIVE_20260914_LCAISALANE_F2
MODEL: claude-fable-5-1
`# CHECKPOINT -- 2026-09-13 ~23:2x   HEAD 9c91999 (records)   crimewidthkill #529: TABLE 7 PROBES RUNNING; rung-3 seat out`
```
The MODEL line is the verification the owner asked for (fable, not a substitute); the CHECKPOINT quote proves file access.

**RULING: B (accept by folding), on 8 of 9 mandated seats** -- codex, grok, kimi (both transports), glm, deepseek, minimax,
opus5, plus this seat; agy DELIBERATELY NOT FIRED. Tally checked against the files: six B, glm OTHER (clamp), opus5 C.
deepseek's token IS present (line 1); the seat check's "no verdict token" is a parse miss, not a seat failure. This is
partly self-review of my pass-1 B, and two of my pass-1 claims are struck below.

## R1 -- Disposition and warrant

Counting arguments, not seats. The measuring seat's TABLE is decisive; its VERDICT does not follow from it.

1. **A is dead on measurement** (`f2_A.out`: `w11_ier 0x3a -> 0x0`, `w22_msr 0xf0 -> 0xb0`). Every former A backer concedes.
2. **B's only measured "cost" is HEAD's own rule.** Opus calls `w23 -> SCR 0x7e (data[1])` an incoherence. But HEAD's served
   cell (2,1) already puts port 0x3fd's byte at position 1 (`r21_sparse 0x6000`, identical under HEAD/A/B/C).
   `(P & 3) % len` for len 1/2/4 is `P mod len` -- the little-endian position of address P inside a len-aligned access --
   and (2,1) and (2,3) are the same case (odd port, word access). B does not invent a contract; it applies the one the
   function already runs at every served cell, including the hardware-legal len-4 lane. glm's clamp is the incoherent
   option: it puts one odd-port word byte at position 1 and the other at position 0.
3. **The equality READ cells are member 4 literally.** The port is fetched today (side effects fire) and the packing loop
   discards the byte -- "the model already computes the right value and then discards it". C keeps that discard on the
   LSR-poll cell every 8250 driver hits.
4. **The oracle exists and is hardware-free: self-coherence** (minimax, the strongest argument on the record).
   `stb X; ldbu` at the same address on a r/w byte register (IER 0x3f9, SCR 0x3ff). HEAD/C: lands, reads 0. A: neither.
   B: round-trips. HEAD's len-4 path already satisfies this invariant; B extends it, C preserves a violation of it.
5. **C's deferral is not round scope.** F2 is not a second site; it is the other output of the same predicate on the same
   cell table, witnessed by the same rung-3 probe with no new oracle. The F2 row C files would reopen this function,
   choose B-for-reads anyway, and force a full re-table (#462's cost).
6. **The addition licence does not discriminate** (grok, glm): C's decline is also a new contract -- latch, message,
   `return 0` -- for cells with no HRM definition. B additionally has a measured delta (the round trip) and an in-function
   transferred warrant that does NOT rest on intent.

**Rejected:** A (regression); C (ships F2, splits one site into two rounds); glm's clamp (incoherent with (2,1)); the
asymmetric guard (clause-(d) shape, and it replaces a false 0 with a stale register on the LSR poll -- worse for a
polling driver, since a stale 0x60 passes the poll).

**Struck from my own pass-1:** "upstream wrote it precisely to accept" (unprovable; B stands without it), and my sketch's
`PHYSICAL` and nested-return check -- those are F6/F5, filed rows, and do not ride on this diff.

**FILED as a result:** F2 closes in-round. File: `alphabwxgate` (BWX opcodes undecoded on a 21066 -- kimi's root-cause
row; NOT a substitute, see R4.4); `lcaisaunaligned` (below). F5/F6/F7 stay filed.

## R2 -- What the fix carries

* Compute `ofs = (relative_addr & 3) % len` ONCE; both arms use `data[ofs]` (Opus's variant leaves a harmless double
  modulo -- drop it).
* `if (len == 0) return 0;` BEFORE the modulo. HEAD's write arm already divides by zero on a len-0 call; no producer
  exists; disclosed under (e), not rowed. A's `>=` got this for free -- B and C must add it.
* **No latch bit, no `fatal`, no `LCA_W_ISA_LANE`.** Member 4 has no event to announce. Bit 8 stays free; do not define a
  dead constant.
* Return values unchanged: write arm returns the downstream result, read arm `return 1`.
* The `/* #NNN: */` comment states the contract: byte for port P at buffer position `P mod len` (the lane for len 4); one
  byte forwarded (F7 owns width); producers are emulator-only -- ungated BWX AND unaligned LDL/LDQ (see R4.3).
* Nothing else: no `PHYSICAL`, no nested-read check, no a<4:3>.

## R3 -- What the detector pins

Rows per enumerated mutant (channel named). The Opus `lca_f2_probe.py` rows are most of this and already have a measured base.

| mutant | shape | row / channel |
|---|---|---|
| `m_exit` (b) | verbatim `ofs > len` exit | six exit cells alive: R(1,2),(1,3),(2,3) + W(1,2),(1,3),(2,3) -- the WRITE three are new rows |
| `m_declinebeyond` = variant C (d) | `ofs > len -> return 0` | `w13` SCR readback 0x3c, `w12` MSR 0xf0, `r12` 0xb0 (accept rows; C is their growth mutant, already measured 6 cells apart) |
| `m_declineeq` = variant A (d) | `ofs >= len -> return 0` | `w11 0x3a`, `w22 0xf0`, `r11 0x60` full-register |
| `m_writeonlyfold` | read keeps unfolded `i == ofs` | `ofs1 zero` (existing) |
| `m_readonlyfold` | write `data[ofs]` unfolded | `w13`/`w23` readback (buffer over-read yields not-X) |
| `m_clamp` (glm) | position `0` | `r23`/`w23` want `0x7e00` / `0x7e` PAIRED with `r21 0x6000` -- the anchor row: two odd-port word cells under one rule (sibling parity) |
| `m_andmask` | `% len` -> `& (len-1)` | needs a len-3 cell: unaligned LDL in sparse space at offset 1021 mod 1024 (head len 3, ofs 3): B `data[0]`, mutant `data[2]` |
| `m_lane1` | `& 3` -> `& 1` | `ofs2 wide`/`ofs3 wide` (existing) |
| `m_replicate` | pack byte in every lane | `ofs1 wide` wants exactly 0x60 (existing) |
| `m_nomask` | drop `& 3` | len-8 row at a port 5 mod 8; pins HEAD identity, flagged as owned by `lcaisasize` |
| len-0 path | delete the guard | no producer -- disclosed (e) |

**Oracle correction:** the shipped witness's oracles (`ofs1 zero` wants 0x60, `ofs1 answer` wants completed) are ALREADY
B's contract -- no re-pin of expectations. Only the sentinel changes: `0x0bad1dea & 0x60 == 0x60`, so pick one with bits
5-6 clear (e.g. `0x0bad1d8a`) and compare full registers. Note Opus's `0x11335577` ALSO has bits 5-6 set (`0x77`); it is
safe only because that probe compares full values. Order: re-pin sentinel, re-run HEAD (must stay 13/16 with the same
reds -- `ofs1 answer` is unaffected, since 0 != any sentinel), THEN edit. Contract line (e) in the header: the three-cell
exit family and the equality family are covered; len 5-7 heads and the qword lane are disclosed.

## R4 -- Findings dropped as wrong

1. **kimi: "B is the minimal option at the behaviour level; B < C < A."** False by the table: C changes six cells, B nine.
2. **kimi: "stuck interrupt forever" under decline.** Real class, unobservable here: `[ lca: ISA interrupt assert not
   implemented ... (once) ]` is in the witness evidence. Refine to "lost clear", not a cost on alphabook1.
3. **glm's F4 OVERTURN ("if alignment is gated, (3,3) is unreachable").** Settled by reading
   `cpu_alpha_instr_loadstore.c:62-64`: only `LS_UNALIGNED` (LDQ_U) masks the address; LDL/LDQ go to `memory_rw` unaligned
   and untrapped. So the split IS a producer -- and glm's own arithmetic then holds: with `LCA_PCI_SIO` 1 KB-aligned,
   every straddling head lands on port 31 mod 32, ofs 3, so **(1,3) and (2,3) kill without any BWX instruction**. F4
   UPHELD, F1 STRENGTHENED; the brief's "the guard can never fire" is true at instruction level only. Still emulator-only
   (real Alpha takes an alignment trap).
4. **kimi: BWX gating is "the hardware-faithful fix".** Worth its own row; not a substitute -- item 3 reaches the same
   cells without BWX.
5. **deepseek/minimax: "the witness scores 16/16 under B" as the primary warrant.** Circular -- the witness encodes accept
   (glm, correctly). Their verdict survives on other grounds; this warrant does not.
6. **Opus: "(2,3) wrong-byte incoherence" and "C invents no semantics."** Both wrong per R1.2 and R1.6. The table is the
   seat's contribution; the ruling is not.
7. **glm: "S2's store clause is false."** Overstated: S2 is about the instruction-level channel; downstream readback is a
   separate channel the brief already uses. Reword S2, do not strike.
8. **F8: REFINE and CLOSE** -- (2,1)'s `data[1]` is right under the `P mod len` rule, identical under every option, and
   it is the anchor for (2,3).

Nothing built, nothing run, nothing written.

---
*Main-loop verification, 2026-09-14 ~00:3x:* R4.3's source claim was re-read -- `LS_GENERIC_N` applies `addr &= ~7` only
under `#ifdef LS_UNALIGNED`, so an unaligned LDL/LDQ reaches `memory_rw` untrapped.  Whether the 1 KB split actually fires
for a sparse-space access depends on the access being TRANSLATED (the Opus seat could not witness a split on the
identity-mapped K0SEG path) -- so the no-BWX route is source-verified, not measured.
