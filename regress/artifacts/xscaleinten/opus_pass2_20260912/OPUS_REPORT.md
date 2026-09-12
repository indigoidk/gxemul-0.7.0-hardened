OPUS_PASS2_20260912 — the Opus 5 measuring seat's final report, verbatim, saved because an Agent seat leaves no file
in a panel dir.  Fired 2026-09-12 on _scratchpad/brief_xscale_pass2_20260912.md and brief_ppc_pass2_20260912.md.
Logs: this directory (xscale) and ../../ppcrlwimiwidth/opus_pass2_20260912/ (ppc).

Everything measured, logs complete with sentinels, clone restored clean (`cmp` clean, binary fresh, sentinel removed), SEC sources untouched.

CHECKPOINT.md first line: `# CHECKPOINT -- 2026-09-12 ~09:2x   HEAD 85f8b46 (records)`

**VERDICT — xscaleinten: SURVIVOR.** `if (rd == 0) { fatal(...); exit(1); }` re-inserted on the inten read arm — 29/29 all green — and it is a *reachable, live* host kill (verified: MRC inten into r0 dies, into r9 survives). A second reachable survivor: `if (i80321_inten & 0x00400000) exit` — 29/29 (verified live). Swept and CAUGHT: the 8 brief mutants (M1, M5, M_OPCODE2, M_RD15, M_NREAD, M_OP1, M_ISTEER_WR, M_CRM) and HEAD.

**VERDICT — ppcrlwimiwidth: NO SURVIVING (d) MUTANT — swept:** `mb>=me` (RM_GE), unrotated-high-word (RM_UNROT), plus all brief-table reverts (R_ONLY_CAST/HIGH, R_POST_LOOP, R_REV_COND, R_ORIG, R_NULL).

**VERDICT — ppcrldimimask: NO SURVIVING (d) MUTANT — swept:** `n-- > 1` rotate (DM_ROT1), end-test without `&63` (DM_NOAND_END), plus all brief-table reverts (D_MUT63, D_NOCIRC, D_NOKEEP_SH, D_NOWRAP, D_NO_MERGE, D_ORIG, D_NULL).

Baseline control confirmed before any mutant: xscale 29/29, rlwimi 28/28, rldimi 27/27, all CONTROL=OK.

### Round 1 — xscaleinten

| mutant (exact C edit, in `if(l_bit){ r[rd]=inten; …}`) | score | red rows | log |
|---|---|---|---|
| `if (rd == 0) { fatal("TODO…\n"); exit(1); }` | **29/29 SURVIVOR** | none | `xscale_XM_RD0.log` (+ `live_XM_RD0_r0.log` DIES / `live_XM_RD0_r9.log` survives) |
| `if (i80321_inten & 0x00400000) { fatal; exit(1); }` | **29/29 SURVIVOR** | none | `xscale_XM_MAGICBIT.log` (+ `live_XM_MAGICBIT.log` DIES) |
| `if (i80321_isteer != 0) { fatal; exit(1); }` | 29/29 (EQUIVALENT — never fires) | none | `xscale_XM_ISTEER.log` |

XM_RD0: no row reads inten into r0 (rows use r9/r4/r5/r6/r10/r3/r7/r15). XM_MAGICBIT: body reads inten but never *tests* its value; every probed value ⊆ `S1|S2|reset|0x10000000 = 0xFFB5F05F`. XM_ISTEER: isteer≠0 is unreachable without a prior write that itself `exit(1)`s (SIB_WRITE), so it is dead code — reported honestly as an equivalent mutant, not a coverage gap.

### Round 2 — ppcrlwimiwidth / ppcrldimimask

| mutant (exact C edit) | probe | score | red rows | log |
|---|---|---|---|---|
| `if (mb > me)` → `if (mb >= me)` | rlwimi | 27/28 | census wrong | `rlwimi_RM_GE.log` |
| `(uint64_t)tmp<<32` → `(uint64_t)(uint32_t)reg(arg0)<<32` | rlwimi | 24/28 | wrap sh8 mb20, wrap sh16 mb28, alias both, census wrong | `rlwimi_RM_UNROT.log` |
| `while(n-- != 0)` → `while(n-- > 1)` | rldimi | 25/27 | pres nowrap, pres wrap | `rldimi_DM_ROT1.log` |
| `while(m != ((64-sh)&63))` → `while(m != (64-sh))` | rldimi | 17/27 CONTROL=FAIL | nowrap×4, single, pres×3, disasm total, census run (sh=0 hang) | `rldimi_DM_NOAND_END.log` |

### Contract claims found FALSE / overclaiming

1. **xscaleinten CONTRACT — undisclosed rd/inten-value gap.** It lists `rd == 15 (M_RD15)` as a covered "different predicate," implying the rd-predicate family is handled, but the symmetric `rd == 0` (and any Rd no row targets) re-introduction escapes — measured survivor + live kill. Its NOT-COVERED list also omits inten-*value* predicates (XM_MAGICBIT survives). At minimum coverage debt; XM_RD0 touches the contract's own claimed family, so arguably an L2 anchor-symmetry breach. Fix: one accept row reading inten into r0 to a marker, and/or a value-bit row — or a disclosure line scoping rd/inten-value.

2. **ppc brief Q3 claim REFUTED.** "`disasm total` / `census run` … carry no measured kill" is false: **DM_NOAND_END reddened `census run`** (its sh=0 hang aborts a census session early). So `census run` does carry a kill against session-aborting source mutants — not a floor gap and not killless.

3. **ppc rldimi census rotate-blindness (confirms brief Q2, not a contract error).** The 495-cell census uses an all-ones source, so it is blind to rotate-amount defects; the only rotate coverage is the 3 RS_VAL preservation rows (sh∈{0,8,40}). DM_ROT1 was caught *only* by `pres nowrap`/`pres wrap`. A uniform (d) rotate mutant is caught, but a rotate defect confined to an SH outside {8,40} would escape — real coverage debt, no natural uniform mutant exploits it.

Housekeeping: clone `/tmp/gxopus_p2` restored from SEC, both files `cmp`-clean, binary fresh, `.MUTANT` removed; `GXEMUL-SEC/src` and `build/`/`est/` never written (the two fixes still show only as the reviewed uncommitted diffs). All raw logs end in their `*_PROBE_DONE` sentinel.
