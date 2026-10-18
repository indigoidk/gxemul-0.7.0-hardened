# #564 pass 1 -- convergence (main loop, 2026-10-17 15:4x)

Seats: GPT-6 Astra (ultra, via tools/cxlaunch.sh 7aa2c41f, `ran: model: gpt-6-astra`) PROCEED WITH CHANGES (4) --
codex_mte564p1.txt; Grok 4.7 (xhigh, plan mode, file-reading) PROCEED WITH CHANGES (4) -- grok_mte564p1.txt; GLM 5.3
(glm-5.3:cloud, packet-fed) PROCEED WITH CHANGES (5) -- glm_mte564p1.txt.  Fable 5.1: SEAT FAILURE (HTTP 429, "You've
reached your Fable limit", req_011Cg8RkZDcS56XMtS1tjjKV) -- fable5_SEAT_FAILURE.txt; stage HELD by owner ruling
2026-10-17, re-fired once before the round closes.  Opus, agy, kimi, deepseek, minimax not fired (owner's roster).

## THE DESIGN -- unanimous among the three answering seats

* **Member 3 at all five sites** (decline + latched announce), predicates and order unchanged, `return` OUTSIDE the
  latch condition (Astra Q-e) -- every refused transfer is refused, only the announcement is once.
* **S2 stays `src > MTE_TLB_C`** for fills and copies (all three).  Narrowing it to COPY would turn five refused source
  values into successful fills with no hardware warrant (NetBSD's fill paths program src TLB_A -- Grok); FILED as its
  own row, with GLM's over-breadth note (src 4 = LIN_A is a source the helper implements, case 4).
* **IMPLEMENT (member 7) at S4/S5 is a separate row** (all three): no warrant for pattern width or mask semantics.
* **One latch bit per SITE**, `1 << 13` .. `1 << 17`, label-agnostic (all three; GLM endorses 5 with the reading of the
  width-bit precedent stated; Grok cites BADMODE's one-bit-per-guard shape); the "next free bit" sentence moves and says
  `1 << 18` (Astra).
* **Messages carry the bracket prefix, the refused value and `-- transfer declined (once)`** (Grok, "Else"); S3-S5 name
  `dst_tlb`, S2 names `src`, S4 names `depth`, S5 names the mask.  The old key phrases are KEPT
  (`unimplemented MTE_MODE_STIPPLE`, `unimplemented SRC`, `unimplemented MTE_MODE_COPY`, `unimplemented MTE_DEPTH_x`,
  `unimplemented MTE bytemask`) so the HEAD witness script attributes the same text post-fix and turns green with the
  same script (witness clause (i)).

## DISPOSITIONS OF EVERY OTHER FINDING

| # | seat | finding | disposition |
|---|---|---|---|
| 1 | Astra C1 | promise "no transfer data writes", not "no memory writes" (the register store and the latch are writes) | ACCEPTED -- wording in the code comment, probe contract and records |
| 2 | Astra Q3, GLM Q3, Grok Q3 | unnamed members: device-level error completion / abort with an interrupt (asc, wdc precedents); unlatched announce + decline; latched announce + fall through (gdrom's recorded warning) | ACCEPTED as named and REJECTED for this round -- `sgi_de_status` has no error bit and no interrupt; inventing one needs an MTE warrant |
| 3 | GLM Q2, Grok Q2, Astra C4 | `&& bytemask != 0` (the reset default) escapes every proposed row | ACCEPTED -- `bytemask unwritten` row in a fresh session (BYTEMASK never stored) |
| 4 | Grok Q2 | `&& src != 7` escapes: rows drove only src 3 and 6 | ACCEPTED -- the refused domain {3,4,5,6,7} exhausted (the field is 3 bits) |
| 5 | GLM 5, Grok, Astra C3 | S1/S2 fire before the switch for ANY destination; a repair scoped to the tiled cases escapes | ACCEPTED -- S1 at tiled A/B/C, tiled A COPY, LIN_A and LIN_B at depth 8 with a full mask (Grok: at depth 32 S4 would mask the escape); S2 at tiled A fill and COPY and at LIN_A |
| 6 | GLM 4, Astra C4 | no row drives S2's active side (COPY with src > 2), and no accepted COPY at src C | ACCEPTED -- `src 3 copy` decline, `src c copy` accept |
| 7 | all three | `<site> once` cannot see a `return` moved inside the latch, nor a shared bit | ACCEPTED -- paint checked after BOTH transfers; one session S1, S2, S3, S4, S5, S1 expecting five distinct texts once each |
| 8 | Astra C2 | prime an EXISTING latch bit first, to catch `d->warned = X` (assignment clearing old bits) | ACCEPTED in bounded form -- one existing bit (BADMODE) set, then the five new sites, then BADMODE's trigger again: its text must not repeat |
| 9 | Grok Q6 | depth 32 and 64 at LIN_B unrowed | ACCEPTED -- S4 at LIN_B for 16/32/64 |
| 10 | Grok Q6, Astra C3 | the witness's `lin fill` control never wrote (no linear TLB entry); a linear row needs `0x80000000 \| page` in the array the arm reads, and only that array | ACCEPTED -- fixture: `sd 0x8000003000000000` to `CRIME_RE_LINEAR_A` or `_B` only, paint at phys 0x30000, DST0 0x30000 DST1 0x30003; the accept row asserts the fill LANDED |
| 11 | Grok Q6 | the PROM's real linear mode is `0x11` (DST_ECC) | ACCEPTED -- `lin fill ecc` accept row at mode 0x11 |
| 12 | Astra C4 | tiled COPY/fill with a non-full BYTEMASK (catches the linear restrictions moving out of their branch) | ACCEPTED |
| 13 | Astra C4 | a decline followed by a supported transfer and a status read | ACCEPTED -- `after decline` row |
| 14 | Astra C4 | sweep all 32 single-zero masks | ACCEPTED, cheap form: one session, BYTEMASK + START only per mask, paint checked at the end (one row); edges 0, 0xfffffffe, 0x7fffffff, 0x0000ffff as their own rows |
| 15 | Grok Q-e | move S5 above the linear arm's `debug(LINEAR TRANSFER)` | DECLINED -- host-debug only, and the debug line prints the transfer's parameters before the decline says why; minimal diff |
| 16 | Astra extra | START is honoured on a READ of a START-tagged address too (`startFlag` ignores `writeflag`) | FILED as its own row; not this round |
| 17 | GLM extra | the `dst_y_step` site is member-1-shaped today (announces, then the linear loop ignores the step) | NOTED on `mtetlbflood` for its round |
| 18 | GLM nit | "src 3 (B+1)" labelling | ACCEPTED -- rows are labelled by value, not by B |
| 19 | Grok Else | S1-S4's strings lack `\n`, S5's lacks the bracket prefix | ACCEPTED -- the new strings are uniform |

## Clause (c), (e), PRETABLE

The null medium (an absent / non-emulator binary) is MEASURED, not claimed.  The contract goes in the probe header.
`PRETABLE.out` is written before table 1, carrying every row above with the mutant it catches and its channel.
