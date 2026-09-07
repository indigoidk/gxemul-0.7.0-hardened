# OPUS_M88KEXC_P1_20260905 -- Opus 5 measuring seat, pass 1 of round m88kexcdeliver.
# Preserved VERBATIM by the main loop from the Agent seat's final message (the harness blocks seat file writes).
# Brief: brief_m88kexc_p1.md.  Agent run: 43 tool uses, ~21 min, 267,301 tokens.  Its measurement logs (36 files) were
# copied from WSL /tmp/opusm88k_logs to _scratchpad/m88kexc/opus_logs/ at 14:55 and its scripts to opus_scripts/;
# the clone /tmp/gxopus_m88kexc was verified cmp-clean and sentinel-free by the main loop afterwards.
# (HTML entities in the seat's text -- &gt; &lt; &amp; -- are the transport's escaping of > < &; read them as such.)

OPUS_M88KEXC_P1_20260905

Verbatim first line of the brief:

> `# PASS-1 DESIGN BRIEF -- `m88kexcdeliver` (HIGH): the m88k exception core stops every guest CPU for five trap-like exception classes instead of delivering them.  Tree `GXEMUL-SEC/src/`, HEAD `ab9ae13`.  2026-09-05.`

---

# VERDICT

**D1 IS CORRECT AND SHIPPABLE — MEASURED 3/3 DELIVER with every architectural value right (pc, SXIP, SNIP, SFIP, EPSR, PSR, destination-unchanged). D2 IS CORRECTLY REJECTED — MEASURED to halt at the tail `default:`. BUT THE DETECTOR AS WRITTEN IS BELOW THE VACUITY FLOOR AND THE OPTION SET IS WRONG ON TWO MEMBERS, and both of those are measurements, not readings:**

1. **FOUR of the five value channels the brief's §6 rows claim to assert are UNIMPLEMENTED in the probe file, and I built four mutants that each score a CLEAN 3/3 SWEEP** — `M_NOSHADOW` (SXIP stale at `0x00000000`), `M_NOSFRZ` (PSR `0x8000000a`, freeze bit gone), `M_SNIPX` (SNIP = pc, wrong return address), `M_MODE` (supervisor switch deleted). Only `M_VEC4` reds. The probe *prints* `sxip`/`psr` and *asserts* neither; it never reads SNIP/SFIP at all.
2. **`M_MODE` CANNOT BE KILLED BY ANY SUPERVISOR-MODE ROW, BY CONSTRUCTION** — the PSR write ORs onto the *existing* PSR, so `| M88K_PSR_MODE` is a no-op whenever MODE is already set. The brief predicts "PSR row reds"; it does not, and no amount of asserting PSR on these three rows will make it. It needs a **user-mode** row. I built one and it works (`stcr r3,cr1 = 0x80038023`, `ldcr r2,cr1 = 0x80404020`).
3. **D1 LEAVES A LIVE, MEASURED ROUTE TO THE TAIL `default:`** — the very halt D1 exists to avoid, reached from D1's own five classes in two guest instructions via the `SFRZ`→`ERROR` re-route. Measured transcript: `[ exception ILLEGAL_INTEGER_DIVIDE: ]` → `[ exception MISALIGNED_ACCESS: ]` → `[ SFRZ already set in PSR => ERROR ]` → `[ exception m88k: internal error ]` → `emul: All machines stopped.` **This is the (d)-shaped hole reproduced inside D1's own repair.**
4. **THE RAISE-SITE CENSUS ENUMERATED THE WRONG DOMAIN.** The deriver matches only *literal* vectors. `tb0`/`tb1`/`tcnd` raise `m88k_exception(cpu, ic->arg[2], 1)` where `ic->arg[2] = iword & 0x1ff` — **a 9-bit vector straight out of a guest instruction, unfiltered in supervisor mode.** So "BOUNDS_CHECK, ERROR and SFU1_IMPRECISE have NO raise site today" is **MEASURED FALSE**: `tb1 0,r3,7` (`0xf003d807`) halts the committed build today.
5. **Q-D1b's premise "zero cost, no row can observe it" is MEASURED FALSE** — I built the row that observes it. Include BOUNDS_CHECK **and ERROR**: not for consistency, but because both are measured reachable and D1 widens the way in.

Every seat-probe row I ran, plus every extension scenario, is listed below. **Logs: `/tmp/opusm88k_logs/` in WSL Gentoo (`table_*.out`, `x_*.out`, `build_*.log`). Clone `/tmp/gxopus_m88kexc` is `cmp`-clean against GXEMUL-SEC on all five m88k sources, no `.MUTANT` sentinel, binary rebuilt and re-verified pre-fix 0/3.**

---

# 0. BASELINE AND HYGIENE (named, per the two-part clearance)

**Baseline: GXEMUL-SEC at HEAD `ab9ae13`**, all five m88k sources `cmp`-clean into the clone before mutant 1:

```
CMP_CLEAN cpu_m88k.c   CMP_CLEAN cpu_m88k_instr.c   CMP_CLEAN cpu_m88k.h
```

One caution worth recording, since it is the kind of thing that invalidates a baseline: **`GXEMUL-SEC` was NOT clean at HEAD when I started** — `git status --porcelain` shows ` M regress/sgi_de_primop_probe.py`. It is unrelated to this round (no m88k file), but a seat citing "HEAD `ab9ae13`" should know the working tree carries one modified probe. Part 2 of the clearance was **run, not asserted**, before every table: `[ gxemul -nt src/cpus/cpu_m88k.c ] = YES` each time. Every mutant dropped `.MUTANT` first and was restored by `cp` **from SEC** (never from a backup) with `cmp` + rebuild.

**No project tree was written.** Post-run mtimes: `GXEMUL-SEC` `2026-08-12 08:41`, `build/` `2026-08-30 18:00`, `est/` `2026-08-12 08:48` — all unchanged.

---

# 1. THE MEASURED TABLES

### Table 1 — BASE (clone at HEAD `ab9ae13`) · `table_BASE.out`

```
M88KEXC_ROW=div0      RESULT=HALT     pc=0x00010004 sxip=0x00000000 psr=0x80000002 r2=0xdeadbeef halted=True  stopped=True
M88KEXC_ROW=ovf       RESULT=HALT     pc=0x00010004 sxip=0x00000000 psr=0x80000002 r2=0xdeadbeef halted=True  stopped=True
M88KEXC_ROW=misalign  RESULT=HALT     pc=0x00010004 sxip=0x00000000 psr=0x80000002 r2=0xdeadbeef halted=True  stopped=True
M88KEXC_ROW=live      RESULT=DONE     pc=0x00010008 sxip=0x00000000 psr=0x80000002 r2=0x00000006 halted=False stopped=False
M88KEXC_ROW=attrib    RESULT=DONE     pc=0x00010008 sxip=0x00000000 psr=0x80000002 r2=0x00000001 halted=False stopped=False
M88KEXC_RESULT=0/3
```

**The brief's HALT/HALT/HALT/DONE/DONE reproduces exactly.** The witness is sound: the liveness marker fires (`r9=0x12345678` on every row), the attribution control isolates the divisor (`r2=1` vs `r2=6`), and the encodings are confirmed against the decoder (below). Re-run after all mutants (`table_BASE_final.out`): identical.

### Table 2 — D2, the naive fix · `table_D2.out`

```
M88KEXC_ROW=div0      RESULT=HALT     pc=0x00000040 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=True
M88KEXC_ROW=ovf       RESULT=HALT     pc=0x00000048 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=True
M88KEXC_ROW=misalign  RESULT=HALT     pc=0x00000020 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=True
                                      (controls unchanged: DONE / r2=6, r2=1)
M88KEXC_RESULT=0/3
```

**D2 halts, exactly as the brief predicts** — and the tail-`default:` signature is confirmed verbatim elsewhere in my runs as `[ exception m88k: internal error ]` + `emul: All machines stopped.` Note `halted=False` (the `unimplemented` text is gone — it *passed* the fallback) and `stopped=True`.

> ### THE FINDING THE D2 TABLE ACTUALLY DELIVERS, AND IT IS ABOUT THE DETECTOR, NOT ABOUT D2
>
> **Compare D2's row values with D1's below. `pc`, `sxip`, `psr` and `r2` are BYTE-IDENTICAL.** D2 reaches the tail *after* the common path has already set every architectural value correctly. So:
>
> > **Every value channel §6 proposes — `pc == 8*vector`, `SXIP == 0x10004|V`, `PSR == SFRZ|IND|SFD1|MODE`, `r2` unchanged — is INVARIANT UNDER `M_NAIVE`. Not one of them can see the round's own (d) mutant.** The *only* channel that separates the shipped fix from the naive one is the **machine-still-running bit**.
>
> That is the `#489` decline-channel lesson arriving before the table is written, which is what the PRE-TABLE CHECK's CHANNEL line is for. It is knowable at row-writing time and it should be in `PRETABLE.out`: **a single-bit oracle carries the entire (d) weight, and every other row is vacuous against it.** The probe survives only because its classifier tests `stopped` *before* `pc == 8*vector` in the `elif` chain — reorder those two lines and `M_NAIVE` scores 3/3. **Make that ordering an explicit assertion, not an accident of the chain.**

### Table 3 — D1, the proposed fix · `table_D1.out`

```
M88KEXC_ROW=div0      RESULT=DELIVER  pc=0x00000040 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=False
M88KEXC_ROW=ovf       RESULT=DELIVER  pc=0x00000048 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=False
M88KEXC_ROW=misalign  RESULT=DELIVER  pc=0x00000020 sxip=0x00010006 psr=0x8000000b r2=0xdeadbeef halted=False stopped=False
M88KEXC_ROW=live      RESULT=DONE     pc=0x00010008 ... r2=0x00000006
M88KEXC_ROW=attrib    RESULT=DONE     pc=0x00010008 ... r2=0x00000001
M88KEXC_RESULT=3/3
```

**The full control-register dump you asked for** (`x_D1_crdump.out`, div0 row — and this settles the "untested parse" worry: the parse works, and `\bPSR=` correctly does *not* match inside `EPSR=`):

```
cpu0:   PID=0x00000101   PSR=0x8000000b  EPSR=0x80000002  SSBR=0x00000000
cpu0:  SXIP=0x00010006  SNIP=0x0001000a  SFIP=0x0001000e   VBR=0x00000000
cpu0:  DMT0..DMA2 all 0x00000000
```

Walking the arithmetic rather than reasoning about it:

| register | measured | expected | check |
|---|---|---|---|
| `pc` | `0x40` | `VBR + 8*8 = 0 + 64` | ✓ (misalign `0x20 = 8*4`, ovf `0x48 = 8*9`) |
| `SXIP` | `0x00010006` | `0x10004 \| M88K_XIP_V(0x2)` | ✓ faulting instruction, V set, E clear |
| `SNIP` | `0x0001000a` | `(pc+4) \| NIP_V = 0x10008\|2` | ✓ rte resumes *after* the divide |
| `SFIP` | `0x0001000e` | `SNIP + 4 = 0x1000c\|2` | ✓ |
| `EPSR` | `0x80000002` | pre-exception PSR (`MODE\|IND`) | ✓ |
| `PSR` | `0x8000000b` | `MODE(0x80000000)\|SFD1(0x8)\|IND(0x2)\|SFRZ(0x1)` | ✓ all four |
| `SSBR` | `0` | scoreboard not modelled | ✓ (declared divergence) |
| `DMT/DMD/DMA` | all `0` | precise, detected pre-dispatch | ✓ manual 9236-9237 |
| `r2` | `0xdeadbeef` | "the destination register is not changed" | ✓ |

**Controls stay DONE.** D1 is right on every channel.

---

# 2. QUESTION 2 — THE SMALLEST EDIT THAT BREAKS D1 AND STILL PASSES

I built five. **Four of them sweep the probe clean.**

| mutant | the edit | measured | verdict |
|---|---|---|---|
| `M_VEC4` | `+ 8 * vector` → `+ 4 * vector` | `0/3`, pc `0x20/0x24/0x10` | **RED — caught** |
| `M_NOMODE` | drop `\| M88K_PSR_MODE` from the PSR write | **`3/3`**, `psr=0x8000000b` | **TOTAL ESCAPE** |
| `M_SNIPX` | `SNIP = (pc+4)\|V` → `SNIP = pc\|V` | **`3/3`** | **TOTAL ESCAPE** |
| `M_NOSHADOW` | skip the shadow update for the three | **`3/3`**, `sxip=0x00000000` | **TOTAL ESCAPE** |
| `M_NOSFRZ` | drop `\| M88K_PSR_SFRZ` | **`3/3`**, `psr=0x8000000a` | **TOTAL ESCAPE** |

Three of these are simply **rows the brief specifies and the probe file does not implement**: §6 says the rows assert `SXIP` and `PSR`, but `m88k_exc_probe.py` only *prints* them, and it never reads `SNIP`/`SFIP` at all. Implementing the assertions kills `M_NOSHADOW` and `M_NOSFRZ`; adding `SNIP`/`SFIP` to the parse and asserting them kills `M_SNIPX`. Cheap, and owed.

> ### BUT `M_MODE` IS THE ONE THAT MATTERS, AND ASSERTING PSR HARDER WILL NOT KILL IT
>
> The brief predicts *"M_MODE (skip the PSR supervisor switch): PSR row reds"*. **Measured: it does not red, and `psr` still reads `0x8000000b` — MODE apparently intact.** The reason is structural, and it is one line:
>
> ```
> m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR] | SFRZ | IND | SFD1 | MODE, M88K_CR_PSR, 0);
> ```
>
> **The write ORs onto the EXISTING PSR.** Every row in the probe faults from reset PSR = `MODE|IND`, so MODE is *already set* and `| M88K_PSR_MODE` contributes nothing. **The mutant is EQUIVALENT on this row set by construction, not by luck.** No supervisor-mode row — however many, however strictly it asserts PSR — can ever observe that term.
>
> **THE ROW THE PROBE SHOULD ADD, and I have measured that it works:** a **user-mode** fault. `x_D1_priv.out`:
>
> ```
> [ cpu m88k: stcr: WARNING! the PSR_MODE bit is being cleared; ... Continuing anyway. ]
> [ exception PRIVILEGE_VIOLATION:  ]
> BREAKPOINT: pc = 0x30
> PSR=0x8000000b  EPSR=0x00000002  SXIP=0x0001000a  SNIP=0x0001000e  r2=0xdeadbeef
> ```
>
> **`EPSR = 0x00000002`** is the discriminator: the *saved* PSR has MODE **clear** (the fault was taken in user mode) while the *live* PSR has MODE **set** — so `| M88K_PSR_MODE` is load-bearing on this row and nowhere else. `M_NOMODE` must red here.
>
> This is clause (f)'s lesson on a new axis: **a row that always starts in the state the fix installs cannot see the fix install it.** The reviewer question is *"if this OR-term were deleted, which row reds?"* — and for four of the five terms in that one statement, today's answer is **none**.

**Exact encodings, derived from the decoder and confirmed by execution** (`case 0x20`, `cr6 = (iword >> 5) & 0x3f`, `M88K_CR_PSR = 1`):

* `stcr r3, cr1` = **`0x80038023`** — needs `(iword & 0x03e0f800) == 0x00008000` and `s1 == s2`, hence `r3` in *both* the `s1` and `s2` fields.
* `ldcr r2, cr1` = **`0x80404020`** — needs `(iword & 0x001ff81f) == 0x00004000`, so `s1` and `s2` fields must be **zero**.
* Second route, also measured (`x_D1_privtb.out`): a user-mode `tb1 0,r4,8` = **`0xf004d808`** → PRIVILEGE_VIOLATION at `0x30`, confirming manual 9264.

**And the translation-cache question in §6 is answered by the source, not by hope:** `m88k_stcr` contains `if ((old & M88K_PSR_MODE) != (value & M88K_PSR_MODE)) cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);`. The caches are **not mode-tagged**; the mode change flushes all of them explicitly. The route is safe, and it executes correctly.

---

# 3. QUESTION 1 — THE PREMISE AUDIT

### Premises that HOLD (re-derived, not ratified)

* **The two switches read correctly.** D1 delivers; D2 halts. Both measured.
* **Vector constants** (`src/include/cpu_m88k.h`): MISALIGNED 4, UNIMPLEMENTED_OPCODE 5, PRIVILEGE 6, BOUNDS_CHECK 7, ILLEGAL_INTEGER_DIVIDE 8, INTEGER_OVERFLOW 9, ERROR 10, USER_TRAPS_START 128. Offsets `8*v` = `0x20/0x28/0x30/0x38/0x40/0x48/0x50` — confirmed by three measured `pc` values.
* **Reset PSR** — `cpu->cd.m88k.cr[M88K_CR_PSR] = M88K_PSR_MODE | M88K_PSR_IND` = `0x80000002`; `M88K_PSR_SFD1 = 0x8` is **clear**. Measured `psr=0x80000002` on every control row. ✓
* **Encodings.** `case 0x3d`, `switch ((iword >> 8) & 0xff)`, `0x68 = divu`, `0x70 = add`. `divu r2,r3,r0 = 0xf4436800` and `add r2,r3,r4 = 0xf4437004` decode field-for-field. `X(add)` raises on `d != dx` with `s1/s2` sign-extended into `uint64_t` — `0x7fffffff + 1` gives `d = 0x0000000080000000`, `dx = 0xffffffff80000000`, unequal → raise. ✓ `ld r2,r3,0 = 0x14430000` → opcode 5 → the load/store template's `if (addr & (LS_SIZE - 1))`. ✓ *(One nit: the probe's docstring calls this "opcode 0x15 form"; `0x14430000 >> 26 = 0x05`. The encoding is right, the comment is wrong.)*
* **`rte` resumes at SNIP.** Measured `SNIP = 0x1000a = (pc+4)|V`.

### Premise REFUTED — the census enumerated the wrong domain

The deriver `grep -o -E 'm88k_exception\(cpu, *M88K_EXCEPTION_[A-Z0-9_]+'` matches **77 literal sites**, and its class breakdown reproduces the brief exactly. **But it matches only sites whose vector is a compile-time constant.** Running the complement:

```
grep -n 'm88k_exception(' src/cpus/cpu_m88k*.c | grep -v 'M88K_EXCEPTION_'
  cpu_m88k_instr.c:2529:  m88k_exception(cpu, ic->arg[2], 1);      <- X(tcnd)
  cpu_m88k_instr.c:2551:  m88k_exception(cpu, ic->arg[2], 1);      <- X(tb0)
  cpu_m88k_instr.c:2564:  m88k_exception(cpu, ic->arg[2], 1);      <- X(tb1)
```

and `ic->arg[2] = iword & 0x1ff` (decoder, `case 0x3c`, `op10` `0x34`/`0x36`/`0x3a`). **The producer emits any 9-bit value, 0..511.** The only filter is:

```c
if (!(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_MODE)
    && ic->arg[2] < M88K_EXCEPTION_USER_TRAPS_START) { ...PRIVILEGE_VIOLATION... }
```

— **user mode only. In supervisor mode there is no filter at all.**

**The deriver's glob also misses three files**: `memory_m88k.c:417` (`m88k_exception(cpu, exception_type, 0)` — also computed), `cpu_dyntrans.c:214` (INTERRUPT), `memory_rw.c:620`.

**MEASURED CONSEQUENCE — the brief's "BOUNDS_CHECK, ERROR and SFU1_IMPRECISE have NO raise site today" is false.** `x_BASE_tb1v7.out`, supervisor `tb1 0,r3,7` = `0xf003d807` with `r3=1`, on the **committed HEAD build**:

```
[ exception BOUNDS_CHECK_VIOLATION:  ]
[ exception unimplemented: vector=0x007 pc=0x00010004 ]      (25 repeats in the captured tail)
emul: All machines stopped.
```

**A second one, and D1 does not fix it either** — `x_BASE_tb1v0.out`, supervisor `tb1 0,r3,0`:

```
[ m88k_exception: reset ]
BREAKPOINT: pc = 0x0
emul: All machines stopped.
```

Vector 0 is *already* `implemented = true`, so it sails past the fallback and dies in the tail's `case M88K_EXCEPTION_RESET:` arm — an **unlatched, guest-drivable `fatal()`** plus `running = false` on every CPU. Neither the census nor D1 sees it.

**The arithmetic over the whole domain, since it is the right way to state the residual.** Of the 128 vectors in `[0,128)` a supervisor `tb0/tb1/tcnd` can name:

| | today (HEAD) | under D1 |
|---|---|---|
| deliver | 3 (vectors 1, 2, 3) | **8** (1,2,3,4,5,6,8,9) |
| halt in the tail `RESET` arm | 1 (vector 0) | 1 (vector 0) |
| halt at the `unimplemented` fallback | 124 | **119** |

D1 converts five of 128. That is the right scope for one round — **but the round's records must say 8-of-128, not "the five are fixed"**, or the next reader inherits a false completeness claim.

### The `#if 0` doubt — RESOLVED by the manual, in D1's favour

Upstream asks *"Is it correct to continue on the instruction after the division by zero?"* The manual answers it twice: 10300-10305 *"The SXIP points to the instruction that caused the exception"* and 8983-8985 *"an rte instruction resumes execution at the instruction pointed to by the SNIP."* Measured `SXIP = 0x10004|V`, `SNIP = 0x10008|V`. **The common path's default is already correct for all five, and a handler that wants re-execution copies SXIP into SNIP itself.** D1 is right to add a bare `break` and delete the `#if 0` block.

One honest divergence to record rather than gloss: the manual adds *"the scoreboard bit is set for the destination register."* The fork writes `SSBR = 0` — measured. That is **more forgiving** than hardware (a handler that does nothing still returns cleanly), never less, so it cannot cause a hang. Worth one CHANGELOG sentence.

### A premise TRUE at reset and FALSE where it matters most

The brief states *"PSR at reset is MODE|IND ... FPU ENABLED (SFD1 clear) — so `divu` by zero reaches ILLEGAL_INTEGER_DIVIDE, not SFU1."* Correct for the probe's rows. **But `X(divu)` tests SFD1 FIRST:**

```c
X(divu) {
    if (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFD1) { ... SFU1_PRECISE ... }
    else if (reg(ic->arg[2]) == 0)                     { ... ILLEGAL_INTEGER_DIVIDE ... }
```

and the exception common path **sets SFD1**. So inside *any* handler, a `divu` raises **SFU1_PRECISE (114)**, not vector 8. Measured (`x_D1_dblfault.out`): `[ exception SFU1_PRECISE: ] [ exception unimplemented: vector=0x072 pc=0x00000040 ]`, 28 repeats, then halt. **The premise is not wrong so much as unscoped, and the unscoped form is the one a future round will reuse.**

---

# 4. QUESTION 3 — OPTION-SET COMPLETENESS

### The in-tree precedent settles this, and it is D1 exactly

I grepped the other cores as instructed. **`cpu_mips.c` contains zero `exit(`/`running = false`. `cpu_ppc.c` has one, unrelated to exception dispatch. Both deliver everything.** And `cpu_sh.c` is not merely a precedent — it is **the same code shape, and this fork has already fixed it three times by exactly D1's edit**:

```c
case EXPEVT_RES_INST:
    /*  #217: (Codex/Fable) a guest reserved instruction must take the
        illegal-instruction exception (the general vector is set up
        above), not exit() the host.  */
    break;
case EXPEVT_SLOT_INST:
case EXPEVT_FPU_SLOT_DISABLE:
    /*  #315: ... neither had a case here, so each fell to the default
        below and called exit(). A guest putting a trapa or an FP
        instruction in a branch delay slot killed the host process
        outright ...  */
    break;
case EXPEVT_ADDR_ERR_LD:
case EXPEVT_ADDR_ERR_ST:
    cpu->cd.sh.tea = vaddr;
    break;
default:fatal("sh_exception(): exception 0x%x is not yet implemented.\n", expevt);
    exit(1);
```

`sh_exception()` has a common path that sets `pc = vbr + <generic vector>`, then a "Specific cases" switch with a killing `default:` — **structurally identical to `m88k_exception()`** — and `#217`, `#315` and `#457` each fixed it by adding bare `case` labels with `break;`. **`EXPEVT_ADDR_ERR_LD/ST` is the SH misaligned class, and it is delivered.** D1 is not a novel design; it is the house idiom with a transferred warrant and three precedents. **This settles Q3 and it settles Q-D1b/c in favour of inclusion**, because the SH precedent groups *by architectural category*, not by "which ones did we get round to".

### The member the brief did not name

**D4 — `default:` DELIVERS instead of stopping.** The brief's set is {D1 enumerate, D2 naive, D3 decline (rejected)}. There is a fourth: make the tail `default:` a bare `break` (or a *latched* announce) and let *every* recognised vector take `VBR + 8*vector`, since the common path has already done all the architectural work correctly for any vector. The `default:` would then catch nothing but genuinely unknown vectors.

I am **not** recommending D4 for this round — it is a bigger blast radius than a witnessed round should take, and the enumerated form is the one with three in-tree precedents. But it must be *named*, because it is the member that makes the residual-119 problem go away, and a panel that never hears it will re-derive it next round. **File it as `m88kexctaildefault`.**

### Q-D1a — message level. Recommend VERBOSITY_INFO, and the measurement supports it two ways

I confirmed by execution that `VERBOSITY_ERROR` lines print at default verbosity (the probe passes no verbosity flag; `-V` is the debugger switch). So under D1-as-written, **every delivered exception prints an ERROR line**, and on a booted guest a userland divide-by-zero would emit one per SIGFPE. I also measured the *flood*: 25 and 28 repeats respectively before `running = false` takes effect, because the dyntrans loop runs `N_SAFE_DYNTRANS_LIMIT` instructions between checks. **Two arguments for INFO:** parity with the four already-implemented classes, and the fact that a routine guest-handled trap is not an emulator error. **I found no hygiene-gate row keying on these lines** (`grep 'exception' regress/gate_hygiene.sh` returns one unrelated comment at `:92`), so nothing reds either way — which makes `M_LEVEL` genuinely **DISCLOSED under clause (e)**, and the brief is right about that one.

### Q-D1b and Q-D1c — INCLUDE BOTH, and the reason is measured, not aesthetic

* **BOUNDS_CHECK (7).** The brief's "zero cost, no row can observe it" rests on "no raise site". **Refuted above by measurement.** A row observes it: supervisor `tb1 0,r3,7`, breakpoint at `0x38`. Under D1-as-written it still floods and halts (`x_D1_tb1v7.out`).
* **ERROR (10) — this is the important one, and OUT OF SCOPE IS NOT SAFE.** `x_D1_errroute.out`, D1 build, two guest instructions:

```
[ exception ILLEGAL_INTEGER_DIVIDE:  ]        <- fault 1: D1 delivers correctly
[ exception MISALIGNED_ACCESS:  ]             <- fault 2, inside the handler
[ SFRZ already set in PSR => ERROR ]          <- common path re-routes vector := 10
[ exception m88k: internal error ]            <- THE TAIL `default:` ARM
emul: All machines stopped.
counts: internal error 1 | SFRZ already set 1 | All machines stopped 1 | unimplemented 0
final: pc=0x00000050  PSR=0x8000000b  EPSR=0x80000002  SXIP=0x00010006
```

> **D1's own repair contains the defect D1 exists to remove.** The brief rejects D2 precisely because it reaches the tail `default:`; D1 reaches the same arm, from D1's own five classes, whenever a handler faults before `rte`.

Being scrupulous about the attribution, because it changes the grading: **the route pre-exists.** A nested DATA_ACCESS (page fault inside a page-fault handler) reaches it on HEAD today, since DATA_ACCESS is already `implemented`. **What D1 does is widen the entry set from 4 classes to 9** — and it does so for exactly the classes whose handlers do the most work (a misaligned-access handler emulating the access is *itself* liable to fault). So it is not a defect the round introduces from nothing, but it is one the round makes materially more reachable while claiming to remove tail-`default:` halts.

**Disposition: add `case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:` and `case M88K_EXCEPTION_ERROR:` to BOTH switches, in the same diff.** Cost: two `implemented = true` and two `case` labels. `pc = VBR + 0x38` / `+ 0x50` is already computed correctly by the common path — I measured `pc=0x50` on the errroute run, arrived at correctly and *then* thrown away by the `default:`. OpenBSD's error handler panicking is the guest's business and is exactly this round's thesis: the guest's panic is the guest's, the emulator's halt is ours.

**This also satisfies the class-closure amendment** rather than converging one cell per pass: the class is *"a vector the first switch recognises but the tail switch has no arm for"*, and closing it means enumerating the first switch's own case list. Do it in one diff and write into the contract that vectors 11..113 and 116..127 remain fallback-halts by design.

### Q-D1d — MISALIGNED: nothing wrong beyond the declared divergence

`DMT0/DMD0/DMA0` are zeroed for every vector but DATA_ACCESS — **correct**, and the manual says why (9231-9240: the condition is *"detected before the memory access is dispatched to the data unit"*, so there is no memory transaction to report). Measured all-zero. The scoreboard bit is the one real gap and it errs safe.

**A sibling defect I found while checking this, and it is one function away from the round's subject.** `m88k_stcr`:

```c
if (value & M88K_PSR_MXM) {
    debugmsg_cpu(..., VERBOSITY_ERROR, "stcr: TODO: MXM support");
    cpu->running = false;
    return;
}
```

**MXM is the misaligned-exception mask.** Manual 9243-9246: a guest masks this very exception by setting MXM, whereupon the processor rounds the address down. **So the guest response the manual prescribes for the class this round is fixing stops the machine.** It is a different function and a different fix (implement the rounding, or decline the bit), so it is **not** in scope — but it is the same semantic class, it is guest-drivable, and a round that delivers MISALIGNED without noting it leaves the obvious next guest action fatal. **File as `m88kmxmkill`.** (Note the header comment calls MXM *"misaligned access enable"*, which reads backwards against the manual's masking semantics — worth one look when that row runs.)

### Q-D1e — fcr2/fcr4/fcr5: follow-up row, not this round. Agreed

Out of scope, and the brief's framing is right. I cannot check OpenBSD's SIGFPE path — **no `sys/arch/m88k` source is on disk** — so I record that as a premise I could not settle rather than agreeing with it. Note `X(divu)` *does* already write `M88K_FPCR_FPECR = M88K_FPECR_FUNIMP` on the SFU1 branch, so the file has the idiom for a future row to follow.

---

# 5. QUESTION 4 — THE GUEST

**OpenBSD/luna88k boots today without this fix**, so no boot path raises any of the five — otherwise the rig would already be dead. That is consistent and it bounds the blast radius: **this fix cannot regress the boot, because the code it changes is unreachable on the boot path** (if it were reachable, the boot would halt today).

What would raise them on a *booted* system:

* **ILLEGAL_INTEGER_DIVIDE** — any userland `a/0`. The commonest of the five by far, and today it kills the emulator rather than delivering SIGFPE.
* **MISALIGNED_ACCESS** — a userland unaligned `ld`/`st` with MXM clear (and MXM is unusable, per the sibling defect above).
* **PRIVILEGE_VIOLATION** — userland `ldcr`/`stcr`/`rte`/`ld.usr`/`st.usr`/`tb0`/`tb1`/`tcnd`. **This is the one a kernel does deliberately**, in feature probes and in `ptrace`/emulator paths.
* **INTEGER_OVERFLOW** — `add`/`sub` (trapping forms), rare from C but emitted by hand-written assembly and by other language runtimes.
* **UNIMPLEMENTED_OPCODE** — `prom_call` from user mode.

**Is there a gate row whose behaviour could change?** `grep -ln luna88k regress/*.sh` gives `gate_ab.sh`, `gate_crossfamily.sh`, `gate_hygiene.sh`, `gate_m88k_rounding.sh`, `gate_offline.sh`. Since none of the five is raised on the boot path today, **no existing row can change** — with one caveat worth stating rather than assuming: `gate_hygiene.sh` grades boot-log content, so **if** any of the five *is* raised during boot and currently ends the run before the log is written, delivering it would produce a *longer* log with new `[ exception ... ]` lines in it. That is exactly the case Q-D1a's INFO change makes moot.

**What a measuring seat should run, in this order:**
1. `gate_m88k_rounding.sh` alone, before and after — it is the gate the new section joins, and it is the cheapest attribution.
2. `gate_ab.sh` alone, nothing else on the machine — it carries the load-sensitive wall-clock oracle, and it is the only row that boots the guest end to end.
3. `gate_hygiene.sh` — the only gate that could notice a longer boot log.
4. Then the full weekly battery, alone.

---

# 6. QUESTION 5 — RECORDS

The CHANGELOG round block owes, at minimum:

1. **The `#if 0` doubt resolved by citation, not by fiat.** Quote 8983-8985 and 10300-10305 and say the default (SXIP = faulting instruction, SNIP = next) is what the manual requires — so the block is *deleted as answered*, not merely as dead.
2. **The retrospective provenance** — filed 2026-09-05 from the Astra + Fable batch-2 retrospective of `#380`; `git log -L` on the fallback returns only the 0.7.0 import, so this is **pre-existing upstream code, not fork regression.** State that explicitly; it is the difference between "we broke it" and "we inherited it".
3. **The split from `m88kexcsfu1`**, with the measured reason and not just a scope note: SFU1_PRECISE has **58 raise sites** (the largest class by an order of magnitude), needs FP exception registers the fork never writes, and — the sharp bit — **is what `divu` raises inside any handler**, because the common path sets SFD1 and `X(divu)` tests it first. The two rows are coupled, and the CHANGELOG should say how.
4. **The census correction, with its deriver.** Record that the literal-vector deriver matches 77 sites and is *blind to computed vectors*, name the four it misses (`tcnd`/`tb0`/`tb1` at `ic->arg[2] = iword & 0x1ff`, and `memory_m88k.c:417`), and state the **8-of-128** figure rather than "the five are fixed".
5. **The two sibling defects found while verifying, each as a filed row**: `m88kexcresetkill` (supervisor `tb1 ...,0` → the tail RESET arm's unlatched `fatal()` + all-CPU stop, **measured on HEAD**) and `m88kmxmkill` (`m88k_stcr`'s `MXM` → `running = false`).
6. **The detector's contract, honestly bounded.** Catches: a class returned to the fallback; a class reaching the tail `default:`; a wrong vector base; a stale SXIP; a wrong PSR; a wrong return address; and — only if the user-mode row ships — a deleted supervisor switch. **Does not catch:** message level (disclosed, no hygiene row exists — *checked*); fcr2/fcr4/fcr5; scoreboard bits; the delay-slot arms.
7. **The delay-slot question, answered.** The brief asks whether a row should fault in a delay slot. **Yes, and it is cheap** — the common path has a three-way delay-slot branch (`DATA_ACCESS` / `INSTRUCTION_ACCESS` / *else*), and the *else* arm is the one all five newly-delivered classes take. It is a distinct, uncovered cell of the same function, its comment literally reads `/* Perhaps something like this could work: */`, and the encoding is one word (`br.n` + the faulting instruction in the slot). **One row, one session.** If it is not rowed, it must be disclosed by name.

---

# 7. THINGS I FOUND WHILE VERIFYING SOMETHING ELSE

* **My own apparatus lied once, and the traceback caught it.** I edited `xprobe.py` from a Windows heredoc; `python3` does not exist on Windows here, so it printed *"Python was not found"* and **the edit silently did not apply**. The next run raised `KeyError`. Had the scenario name been one that already existed, I would have measured the wrong program and reported it. Re-done under WSL with an `assert s.count(old) == 1`. This is the *check the apparatus selected something* rule, and my patch helper asserts occurrence counts for exactly this reason — the one edit that skipped the assert is the one that failed.
* **The probe's classifier reports `HALT` for `M_VEC4`.** `M_VEC4` is a wrong-vector-base defect, not a halt, but the pc lands in zeroed RAM, the CPU executes `0x00000000`, and the machine stops for an unrelated reason. The row correctly **reds**, so the detector works — but the *diagnosis* is misleading, and a future reader will chase a fallback regression that is not there. Add a `WRONGPC` result distinct from `HALT`.
* **`M88K_CR_*` numbering** is PSR 1, EPSR 2, SSBR 3, SXIP 4, SNIP 5, SFIP 6, VBR 7 — needed for the user-mode row's encodings and not in the packet.
* **`MVMEPROM_VECTOR = 496`** (`thirdparty/mvmeprom.h`), and the syscall vectors are `0x80 = 128` and `0x1c2 = 450`. All three are `>= USER_TRAPS_START`, so they skip the tail switch entirely — which is why syscalls work today and why the tail `default:` has never been hit in normal operation. Worth one sentence, because it explains why this defect survived to 2026.

---

# 8. CLONE STATE (as required)

```
CMP_CLEAN  src/cpus/cpu_m88k.c
CMP_CLEAN  src/cpus/cpu_m88k_instr.c
CMP_CLEAN  src/cpus/cpu_m88k_instr_loadstore.c
CMP_CLEAN  src/include/cpu_m88k.h
CMP_CLEAN  src/cpus/memory_m88k.c
NO SENTINEL
PART2 binary -nt source: YES
```

Every mutant was restored by `cp` **from GXEMUL-SEC** (never from a backup), `cmp`-verified, and **rebuilt** before the sentinel was cleared — the restore is not finished until the binary is rebuilt. The clone's re-run of the seat probe reproduces the pre-fix `0/3` HALT table (`table_BASE_final.out`), so the restore is proven by measurement and not only by `cmp`. The only remaining differences between the clone and SEC are `.o` object files and the three declared divergence-set paths (`src/devices/.index`, `Makefile.skel`, `autodev.c`) — the clone is a copy of `build/` (the pmax tree), so those are expected and **must not be "restored"**.

**No write touched `GXEMUL-SEC`, `build/`, `est/`, `build-asan/` or `/tmp/gxsec-build`** — post-run mtimes confirm.

**Logs, all under `/tmp/opusm88k_logs/` in WSL Gentoo** (volatile — copy anything a durable record cites into `regress/artifacts/`):

| file | what |
|---|---|
| `table_BASE.out`, `table_BASE_final.out` | HEAD, before and after all mutants — `0/3` both |
| `table_D2.out` | D2 — `0/3`, values already correct |
| `table_D1.out` | D1 — `3/3` |
| `table_D1_VEC4.out` | `0/3` — the one mutant caught |
| `table_D1_NOMODE.out`, `table_D1_SNIPX.out`, `table_D1_NOSHADOW.out`, `table_D1_NOSFRZ.out` | **`3/3` each — four clean sweeps** |
| `x_BASE_tb1v7.out` | BOUNDS_CHECK raised on HEAD — refutes "no raise site" |
| `x_BASE_tb1v0.out` | supervisor `tb1 ...,0` → RESET arm → all CPUs stopped |
| `x_D1_crdump.out` | the full `reg 0,0` dump |
| `x_D1_errroute.out` | **D1 → tail `default:` → `internal error` → halt** |
| `x_D1_priv.out`, `x_D1_privtb.out` | the user-mode PRIVILEGE route, both encodings |
| `x_D1_dblfault.out` | SFD1 → `divu` raises SFU1_PRECISE (`0x72`) inside a handler |
| `x_D1_tb1v8.out`, `x_D1_tb1v7.out` | trap-raised delivery vs. residual halt under D1 |

Scripts (durable, on the Windows side): `C:\Users\User00\AppData\Local\Temp\claude\opusm88k\` — `patch.py` (the five mutants, with occurrence asserts), `xprobe.py` (the seven extension scenarios), `run_mutant.sh` (sentinel → patch → build → probe → restore-from-SEC → rebuild → clear).
