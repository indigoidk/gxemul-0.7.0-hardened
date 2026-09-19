# FABLE 5 -- flagship adjudication of `#530`'s pass 2 and its §F2 pass (you rule LAST; every other seat has answered)

## IDENTITY FIRST (required -- this project verifies the flagship seat by content, not by assumption)

Line 1 of your answer: `FABLE_SEAT_530F2_LIVE`.
Line 2: your exact model identifier, as you know it (the project records it, e.g. `claude-fable-5-1`).
Line 3: the FIRST LINE of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, quoted verbatim.
If you are not Fable 5, say so on line 2 and stop.

## WHAT YOU ARE RULING ON

The tree is `GXEMUL-SEC/src/` at `3c41f01`.  `#530` (8bd97e4) removed a process-ending call from
`DEVICE_ACCESS(lca_isa)` in `src/devices/dev_lca.c` and shipped a WIDTH ROW, `regress/lca_widewrite_probe.py`,
that pass 6's flagship ruling owed (`regress/artifacts/lcaisalane/table7_20260916/CLOSE6_VERDICT.md` -- your
own earlier ruling; re-read its "catchable / uncatchable" paragraph).  The row drives one 16-byte PROM GETENV
write at (C=16, k=0, lane 3).

Read, in this order (all are files you can open):
1. The pass-2 brief and the §F2 packet: `_scratchpad/brief_530p2_20260918.md`, `_scratchpad/brief_530f2_20260918.md`.
2. The Opus seat's measurement: `GXEMUL-SEC/regress/artifacts/lcalenzerodrop/opus_p2_20260918/{README.md,RESULTS.txt}`
   (102 legs, every value predicted first).
3. The §F2 answers: `_scratchpad/panel_20260918_190129/{codex,agy,grok,ollama_glm,ollama_deepseek,ollama_minimax,
   ollama_kimi}.txt` and `opus5_f2.md`; the Opus seat's pass-2 answer is `_scratchpad/panel_20260918_180558/opus5_p2.md`.
4. The row and the handler: `GXEMUL-SEC/regress/lca_widewrite_probe.py`, `GXEMUL-SEC/src/devices/dev_lca.c`.

## WHERE THE PANEL STANDS (so you can check my summary against the files, not trust it)

Pass 2: 7 of 8 scriptable seats DOES NOT CLOSE; the split was L2-vs-debt.  My provisional ruling was
E-DEBT-PLUS-L4 (the measuring seat's reading: pass 6's "uncatchable" is a condition on discharge by contract,
now met because a shipped instrument reaches every wide cell).  **The §F2 pass overturned it 8 of 8** (all seven
scriptable seats and the Opus seat):
L2-CLASS-CLOSURE.  The grounds differ -- the contract's own "any guard that declines a len > 8 WRITE" plus
clause (e)'s "an in-contract variant undetected is itself L2" (codex, deepseek, minimax, kimi, glm, agy); vc as a
floor breach on a body-distinguished operand, the `#499` shape (grok, agy, kimi); va/vb as clause (d)'s own
"bound relaxed" (glm, minimax).  **They disagree on the CELL SET:**

    agy, deepseek, minimax, kimi   {mc2, kbc1024}
    glm                            {mc2, kbc1024, low16}
    grok                           the four C=16 WRITE lanes + the F10 width pin; va/vb/ve/vg/vt* stay clause (e)
    codex                          {l0w16, low16, mc2}; the larger widths are debt by clause (iii)'s explicit exclusion

grok and glm independently showed {mc2, kbc1024} is a COVERING of the listed variants, not a closure: a
lane-1-only exemption `&& (len <= 8 || (P & 3) != 1)` passes both.  codex showed mc2's readbacks cannot
distinguish a 32-byte request (16+16) from a 20-byte one (16+4).  agy showed GETENV clamps len to
strlen(-o string)+1, so C=64/256/1024 rows need a long `-o`.

**The Opus seat (measuring; it reversed its own pass-2 reading) -- read it in full at `_scratchpad/panel_20260918_190129/opus5_f2.md`.**  Its load-bearing claims, for you to check against the headers:
* vc is L2 on BOTH routes: lane is body-tested (via `data[ofs]`), crossed with the {len > 8} cell pass 6 put in the floor; and vc is inside the shipped "any guard" with no disclosure covering it.
* ACROSS BOTH HEADERS most escapes are already DISCLOSED: va/vb by the width row's clause (iii); vg/vt1 by the parent probe's a<4:0> clause (lcaisasize); ve by the parent's p_port10 port class.  **Only vc and vt2 are in-contract AND undisclosed**, and mc2 alone catches both (measured).
* Floor-minimal cell set {frozen, l0w16, low16, mc2}; minimal set satisfying (e) {frozen, mc2}; disclose the rest with warrants (k=16 at lanes 0/1/3, other ports, chunk position >= 3, data values -- a wide chunk never forwards 0, forward COUNT -- every GETENV row reads a latch, the READ side, non-lane delivery).
* HARNESS DEFECTS in the shipped row, owed with the closure: the retry fires on missing prints WITHOUT checking `alive`, so a first-session host death is retried away; the width pin needs a chunk-list assertion (mc2 pins C only through its MSR row; its SCR row is blind to a3 = 20).
* Reachability runs the other way from the debate: C=16 needs no `-o` (BOOTED_FILE returns the 15-char basename `alpha_dummy.bin`, len 16), while C>=64 needs an operator string of >= 63 chars -- so vc/ve/vg/vt1/vt2 are the MORE reachable escapes and va/vb the least.


## YOUR RULINGS, each with its warrant

R1. D1: L2 or debt -- and for WHICH variants (va vb vc ve vg vt1 vt2)?  Name the rule that decides each.
R2. The CELL SET the closure diff must row, and what its contract discloses.  Is the lane-1 cell owed?  kbc1024?
    k=16?  a two-chunk continuation cell?  How is the F10 width pin achieved, given codex's 20-byte ambiguity?
R3. F5's remedy: is narrowing the contract ever available once an in-contract variant is measured undetected?
R4. F12: the row exits 0 on FAIL -- records, or fixed in the closure diff?
R5. The older HELD research question on `lcaisalane` (DROP of `if (len == 0) return 0;`): both halves now have
    measured answers -- M1_lenzero 352/352 (equivalent by no producer; `regress/artifacts/lcalenzerodrop/
    killtable_20260918/logs/TABLE.out`) and your pass-6 L2 on the width class.  Discharge it, or say what is missing.
R6. After the closure diff lands with its own pass 2, what closes the chain (denominator)?
R7. WHICH OF MY DISPOSITIONS IS WRONG?  I accepted 14 of 15 findings and was overturned 8-0 on D1 -- say whether I
    have now over-corrected toward the panel.

Be harder on any ruling that favours finishing.  Anything checkable in two minutes: check it, do not judge it.

**READ ONLY.** Write nothing under GXEMUL-SEC or anywhere else; report inline.  Open with the three identity lines, then one line per ruling R1-R7 in the form `R<n>: <ruling> -- <warrant>`, then your detail.
