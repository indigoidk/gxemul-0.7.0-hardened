AGY_M88KEXC_P5_ALIVE_20260906
> # PASS 5 -- `m88kexcdeliver` (#502): the closing pass on the PASS-4 REPAIR (probe v5, 29 fault rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~09:20.  SHORT BY DESIGN: one diff, one table, one question.

**VERDICT: ONE MORE REPAIR: `resid127` (pin upper boundary of fallback window at vector 127)**

---

### 1. MEASURED TABLE (WSL Gentoo scratch clone `/tmp/gxagy502`, probe frozen md5 `96ab47a0`, BASE 29/29 before and after)

| Mutant | Exact Edit in `cpu_m88k.c` | Score | Red Rows / Defect Manifestation |
|---|---|---|---|
| **`M_FALLBACK127`** | Line 799: `vector < M88K_EXCEPTION_USER_TRAPS_START` -> `vector < 127` | **29/29** | **None (CLEAN SWEEP)**: vector 127 unrowed; bypasses fallback halt and crashes at tail default `internal error` |
| **`M_FALLBACK_NO_BOUND`** | Line 799: `vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented` -> `!implemented` | **28/29** | `usertb` HALT (user traps >= 128 halted at fallback instead of delivered to `0x400`) |
| **`M_SFRZ_EPSR_SWAP`** | Line 811: `cr[M88K_CR_PSR] & M88K_PSR_SFRZ` -> `cr[M88K_CR_EPSR] & M88K_PSR_SFRZ` | **23/29** | `error` STOP (0x20), `trapfrozen` BADREGS (bad=sxip,epsr,snip,sfip), `errovf` STOP (0x48), `errdiv0` BADREGS (bad=sxip,epsr,snip,sfip), `errpriv` STOP (0x30), `errunimpl` STOP (0x28) |
| **`M_TAIL_ERROR_DROP`** | Line 929: drop `case M88K_EXCEPTION_ERROR:` from tail switch | **23/29** | `error`, `errortb`, `errovf`, `errdiv0`, `errpriv`, `errunimpl` all TAILHALT (`internal error` at 0x50) |
| **`M_TAIL_BOUNDS_DROP`** | Line 926: drop `case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:` from tail switch | **26/29** | `bounds` TAILHALT (0x38), `vbrtb` TAILHALT (0x2038), `trapfrozen` TAILHALT (0x38) |
| **`M_SFRZ_TRAP_UPDATE`** | Line 821: `update_shadow_regs = false;` -> `update_shadow_regs = is_trap;` | **28/29** | `trapfrozen` BADREGS (bad=sxip,snip,sfip; SXIP updated to handler PC `0x40` instead of frozen `0x10004`) |

*All runs printed `M88KEXC_DONE`. Baseline: `BASE.out` 29/29, `BASE_final.out` 29/29 (`SENTINEL_CLEARED_CLEAN_BASE_29_OF_29`). Logs retained in `_scratchpad/m88kexc/agy_p5/`.*

---

### 2. THE ONE QUESTION & FLOOR BREACH ANALYSIS

**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE?**
**YES: `M_FALLBACK127` scores 29/29.**
- **Mechanism**: The MC88100 architectural specification reserves vectors 0..127 for hardware/reserved exceptions and 128..511 for user traps (`M88K_EXCEPTION_USER_TRAPS_START == 128`). Unimplemented vectors in 0..127 must halt at the fallback predicate with `unimplemented vector=0x%03x` before mutating processor state. Under `vector < 127`, supervisor trap `tb1 0,r3,127` bypasses the fallback, executes the common delivery path (overwriting PSR, EPSR, SXIP/SNIP/SFIP, VBR+0x3f8), and terminates abnormally in the tail switch (`internal error`).
- **Escape Cause**: Probe v5 tests fallback negative controls at vector 50 (`resid50`) and vector 114 (`sfu1h`), and user trap delivery at vector 128 (`usertb`). The boundary vector 127 is unrowed.
- **Required Row**: `resid127` (`[TB1_0_R3_127]`, `{"r3": 1}`, `V_RESID127 = 127`, `EXPECT_RESULT = "HALT"`, `EXPECT_VECTOR = 0x07f`).

---

### 3. MEASURING SEAT DENOMINATOR (CLOSED SPACE)

1. **Fallback Predicate Partitioning**: lower/upper bound and polarity (`M_FALLBACK_NO_BOUND` 28/29 via `usertb`, `M_DELIVERALL` 21/23 via `resid50`/`sfu1h`, `M_NOSTOP` 21/23; `M_FALLBACK127` 29/29 open).
2. **PSR Update Bitfield**: SFD1 (`M_NOSFD1` 1/29), SFRZ (`M_NOSFRZ` 2/23), IND (`M_NOIND` 22/23 via `indclr`), MODE (`M_NOMODE` 19/23 via user rows), Carry preservation (`M_CARRYCLR` 22/23 via `ovfc`).
3. **Re-Route Predicate & State Source**: PSR vs EPSR operand selection (`M_SFRZ_EPSR_SWAP` 23/29), trap exemption polarity (`M_SFRZTRAP` 21/22), shadow freeze polarity under trap exemption (`M_SFRZ_TRAP_UPDATE` 28/29 via `trapfrozen`).
4. **Tail Switch Routing Completeness**: ERROR dispatch (`M_TAIL_ERROR_DROP` 23/29), BOUNDS dispatch (`M_TAIL_BOUNDS_DROP` 26/29), user-trap boundary gating (`M_TAILLE` 21/22 via `usertb`).
5. **Two 2D Product Closures**:
   - `{class} x {MODE}`: 5 user-mode delivery routes (`udiv0`, `umisalign`, `uovf`, `priv`/`privtb`, `unimpl`).
   - `{SFRZ set, !is_trap} x {class}`: 5 frozen non-trap routes to ERROR (`error`, `errovf`, `errdiv0`, `errpriv`, `errunimpl`).
6. **Shadow & Vector Geometry**: SXIP/SNIP/SFIP offsets (`M_NOSHADOW`, `M_SNIPX`, `M_DSLOT`), VBR base offset (`M_NOVBR` via `vbrtb`).

---

### 4. REVIEW OF ELEVEN DISPOSITIONS

All eleven dispositions (2 class closures, 1 classifier refine on `halted`, 6 L4 records, 1 filing of `m88kdslotshadow`, 1 carried-wording ruling) are **technically correct and verified**. The v5 classifier refinement properly ties `halted` to `emul.c`'s `All machines stopped.` output without dead-code disjuncts.
