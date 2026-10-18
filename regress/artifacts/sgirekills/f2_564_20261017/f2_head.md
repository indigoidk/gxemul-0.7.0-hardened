# `#564` sgirekills (MTE half) -- §F2: THE PANEL SHARES ITS PASS-2 FINDINGS

## READ THIS FIRST

This is the adjudication pass.  Pass 2 had three answering seats -- GPT-6 Astra, Grok 4.7, GLM 5.3 -- each SHIP WITH
CHANGES; Fable 5.1 was a SEAT FAILURE (HTTP 429), and its stage is held by owner ruling.  Every finding is below, with
the main loop's disposition on each.  **Please do not ratify.**  The load-bearing question is: **WHICH OF MY ELEVEN
DISPOSITIONS IS WRONG?**  A seat whose own finding is adopted is asked to be HARDER on it -- including whether the
proposed REPAIR is right, not merely whether the finding was.

**THE TREE IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED EDITS** to `src/devices/dev_sgi_re.c`,
`regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py`.  The repair proposed here is NOT applied yet: the
working tree is exactly what pass 2 reviewed.  Everything a packet-fed seat needs is inlined in section 3.

**VERDICT LINE FIRST.**

## 1. The findings and the main loop's dispositions

| # | seat(s) | finding | disposition |
|---|---|---|---|
| F1 | Astra, GLM, Grok | A START-tagged READ also runs the transfer: `if (startFlag) do_mte_transfer(cpu, d);` (3d, `:1860-1861`) has no `writeflag` test.  The pass-2 brief's settled premise "only on a WRITE" was false, and the fix's comment (3a, `:1515-1517`) says "the register store that carried START has already landed" -- true of a write only. | **ACCEPT, L4.**  The comment becomes: *"The decline returns before any TRANSFER data is written.  On a START-tagged write the register store has already landed in the caller and stays; a START-tagged READ reaches here too (filed separately), and either way the caller's common tail still answers."*  The index-bound conclusion (`regnr + 1 <= 512`) is unaffected. |
| F2 | Astra | The probe header says the paint "is read after EVERY transfer, including the repeats"; the 32-mask sweep reads it once at the end (its own row note says so). | **ACCEPT, L4.**  Header corrected; no oracle change. |
| F3 | Astra, GLM, Grok | PRETABLE errata: (a) "0 and 1 are SAMPLED" -- source 1 is never driven; (b) `after status` "cannot vary under any mutant" -- `b1` reddens it (session death); (c) `after fill` "(no mutant rowed for that shape)" -- `s5hoist` reddened it; (d) `src 3 copy` "lands the source byte" -- source mode 3 reaches the helper's default return and the PUT writes BG, still not the paint; (e) "S2 at B/C, owed: none" -- see F9. | **ACCEPT, L4.**  `PRETABLE.out` stays as written (its timestamp, before table 1, is the order proof); the corrections go in a dated `PRETABLE_ERRATA.txt` beside it, each quoting the text it corrects. |
| F4 | Astra | The enum comment promises each message carries "the value in the text"; no row checks the printed values (`ntext()` matches key phrase + suffix only). | **ACCEPT** as an explicit no-row sentence in the probe contract. |
| F5 | Grok | "`CRIME_DE_STATUS` is the constant 0x1e000000": the macro is the OFFSET 0x4000; the value read is `IDLE \| SETUP_IDLE \| PIXPIPE_IDLE \| MTE_IDLE` = 0x1e000000. | **ACCEPT**, records wording.  The probe's expected word is right. |
| F6 | GLM | "3a is not the whole diff": three hunks shown, numstat net +53, hunks net +46. | **REJECT, measured.**  The packet's section 3a carries FOUR hunks -- `@@ -162,11 +162,28`, `@@ -1493,17 +1510,36`, `@@ -1578,13 +1614,23`, `@@ -1594,8 +1640,15` -- net +17 +19 +10 +7 = +53, equal to the numstat.  The fourth (S5) was missed in reading. |
| F7 | GLM | `if (src > MTE_TLB_C \|\| src == 1)` (refuses a legal source 1) and `&& bytemask != 0x00ff00ff` (exempts one multi-zero mask) keep all 53 green. | **DISCLOSE (clause e), not floor.**  Both are equality cases at an interior value the guarded body never tests as a case; the joint-cell rule discloses those.  The two edges of `src > MTE_TLB_C` ARE rowed (`src 3` refused, `src c fill`/`src c copy` accepted at 2).  The contract will name source 1 as never driven beside the already-disclosed mask sampling. |
| F8 | GLM | A decline that also WRITES an MTE register before returning stays green: no row reads an MTE register after a declined START. | **DISCLOSE** -- PRETABLE section 2 already says so; the contract will too. |
| F9 | Grok (and the main loop, checking Astra's coverage remark) | `if (src > MTE_TLB_C && dst_tlb != MTE_TLB_B)` keeps all 53 green (likewise `MTE_TLB_C`, `MTE_TLB_LIN_B`): S2 is rowed only at A and LIN_A. | **ACCEPT, L2 -- and wider than the three labels.**  S1's and S2's `return` BYPASSES `switch (dst_tlb)` (3a), so the 2026-09-25 skipped-dispatch label clause applies (text in 3e): the floor for EACH of S1 and S2 is {A, B, C, LIN_A, LIN_B} x latch {CLEAR, SET} -- labels 3/6/7 reach `default:`, which writes nothing, so they are excluded as host-debug only.  Rowed today: S1 6 of 10 (A both; B, C, LIN_A, LIN_B SET only), S2 3 of 10 (A both; LIN_A SET).  REPAIR: rows for the 11 empty cells -- S2 SET at B, C, LIN_B appended to the S2 session AFTER its last existing check, and four new sessions each pairing one S1-CLEAR and one S2-CLEAR cell (S1 at B / S2 at C; S1 at C / S2 at B; S1 at LIN_A / S2 at LIN_B; S1 at LIN_B / S2 at LIN_A).  Kill table 3 MEASURES all 20 latch-conditioned label-swap variants, e.g. `if (src > MTE_TLB_C && !(dst_tlb == MTE_TLB_B && !(d->warned & SGIRE_W_MTE_SRC)))`; a plain label exemption exempts a superset of cells, so its detection follows from either conditioned variant's. |
| F10 | Grok | Aliasing a new latch bit onto a PRE-EXISTING one -- `SGIRE_W_MTE_STIPPLE = 1 << 10` (= `SGIRE_W_BADMODE`), `SGIRE_W_MTE_COPY = 1 << 11` (= `SGIRE_W_TEX_RD`) -- keeps all 53 green: the only pre-existing bit any session sets is `SGIRE_W_TLBA_LEN`. | **ACCEPT, L2.**  The `#490` precedent (a latch-bit collision that escaped was a clause-(d) breach) and this file's own crossbit rows (`sgi_re_width_probe.py` `tex xbit`, `sgi_re_colourdefault_probe.py` `allbits`).  REPAIR: one new session sets every pre-existing bit 0-12 FIRST, using the priming sequence the `allbits` row already proved (plus its colour decline, which sets bit 12), then drives S1-S5; rows: `xbit primed` (all 13 priming announcements seen -- the row proves its own setup) and `xbit texts` (each new site announces exactly once).  Kill table 3 measures one alias per new site (Grok's two, plus S2, S4 and S5 onto three other pre-existing bits); every other (site, bit) pair is covered BY CONSTRUCTION via `xbit primed` -- recorded in that form, not as a measurement. |
| F11 | Grok | The `*surv` rows and `after status` stay green under the d-mutants (return removed, the transfer runs). | **NO CHANGE.**  Their named mutants are the b-mutants (exit reinstated), under which they red; the paint rows catch the d-mutants.  Recorded in the errata so the channel split is explicit. |

## 2. Disagreements

* **F6:** GLM's missing-hunk reading against the packet itself -- settled by counting the packet's `@@` lines (above).
* **F9's width:** Grok asked for the three refuse-side labels (S2 at B, C, LIN_B).  The main loop reads the 2026-09-25
  clause as demanding labels x latch for BOTH S1 and S2 -- 20 cells, 11 rows, 20 measured variants.  **Is the latch
  cross owed here, or is that an over-reading?**  The clause says "the repair path tests the warning latch, so its CLEAR
  and SET states belong explicitly in the enumeration", and that "detection of the plain variant does not discharge the
  latch-conditioned variants".  It also says it was MINTED FROM ONE DEVICE and must be fit-checked on first reuse --
  this is that reuse.
* **F10's by-construction step:** is one measured alias per site plus a priming-proof row enough, or must every (site,
  pre-existing bit) pair be measured (5 x 13 = 65 builds)?
* **F7:** GLM calls the source-1 growth "outside the sample" and asks that the floor claim be scoped to the enumeration;
  the main loop agrees on the scoping and disposes it as clause (e).

