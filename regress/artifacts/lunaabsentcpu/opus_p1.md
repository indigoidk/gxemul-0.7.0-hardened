# Opus 5 MEASURING seat -- lunaabsentcpu PASS 1 (design), preserved verbatim by the main loop 2026-09-06 ~09:00
# (the RE-FIRE after the first instance died on the 2026-09-05 session limit; its 22:17 logs are in opus_p1_logs/ too.
#  Logs: _scratchpad/lunaabs/opus_p1_logs/ -- R01_base.out, T_det_<V>.out, T_acc_<V>.out, diff_<V>.diff, E438_*.out, 58 files.)

OPUS_LUNAABS_P1_ALIVE_20260906

First line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\lunaabs\brief_lunaabs_p1.md`, verbatim:
> `# PASS-1 DESIGN BRIEF -- `lunaabsentcpu` (HIGH, MEASURED): dev_luna88k.c delivers an interrupt to a CPU slot that was never connected, and the emulator process dies.  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` (dev_luna88k.c last touched by cf4b083 / #438).  2026-09-05, ~21:45.`

---

# VERDICT: **PROCEED WITH (a)** — with two measured obligations the brief's detector plan does not yet carry

Option (a) is measured correct and complete for the witness. But the detector plan as written **fails vacuity-floor clause (d)**: I built the clause-(d) null-repair mutant (`d->ncpus = 1;` hardcoded) and it scored **20/20 — a total escape — on the 1-cpu detector**. It is killed by exactly one thing: the `-n 2` accept row observing cpu 1 asserting. **The accept row is mandatory, not optional.** A second mutant (`ncpus` never assigned) escapes every survival and readback row and is killed only by a free-running delivery row on the *default* 1-cpu config.

Both were measured, and the accept channel works — glm's claim that a readback cannot show it is right, but a CPU-side channel exists.

---

## 1. Witness reproduced on my own clone (baseline, rebuilt)

```
LUNAABS_ROW=live/devsig/slot0/mask1  RESULT=OK
LUNAABS_ROW=soft1   RESULT=HALT   HOST DIED (signal 11)
SYMPTOM=NULL_CALLBACK_ON_ABSENT_CPU
LUNA_ABSENTCPU_WITNESS=PRE_FIX_SYMPTOM   LUNAABS_RESULT=4/5
```
`opus_p1_logs/R01_base.out`. Clone `cmp`-clean against `GXEMUL-SEC` before the build, binary newer than source.

## 2. The kill table (28 rows across two configurations, 15 binaries)

| variant | 1-cpu detector /20 | `-n 2` accept /8 | killed by |
|---|---|---|---|
| **BASE** (HEAD) | 5/6 **HALT at `soft1`** | 8/8 | `soft1` — floor (a) |
| **FIXA** (option a) | **20/20** | **8/8** | — |
| FIXA_CLAMP | 20/20 | 8/8 | — (identical to FIXA on every row) |
| M_REVERT (loop back to `MAX_CPUS`) | 5/6 HALT `soft1` | 8/8 | `soft1` — floor (b) |
| M_OFFBY1 (`cpu <= d->ncpus`) | 5/6 HALT `soft1` | 8/8 | `soft1` |
| M_NOASSIGN (`ncpus` never set -> 0) | **18/20** | **5/6** | `slot0 deliver`+`slot0 shadow`; `cpu1 deliver` |
| **M_HARD1 (`d->ncpus = 1;`)** | **20/20 TOTAL ESCAPE** | **5/6** | **`cpu1 deliver` ALONE** |
| M_NULLA (NULL check, assert side only) | 5/6 HALT `soft1` | 8/8 | `soft1`'s **readback** |
| **M_NULLAB (NULL check, both sides)** | **20/20** | **8/8** | **nothing — EQUIVALENT** |
| M_LATCH (decline once, then deliver) | 5/6 HALT `soft1` | 8/8 | `soft1`'s **readback** |
| M_GUARDASSERT (guard inside the branch) | 5/6 HALT `soft1` | 8/8 | `soft1`'s **readback** |
| M_NOREASSERT (SOFT arm's reassert deleted) | **20/20 escape** | 8/8 | nothing |
| M_NOREASSERT2 (+ device-line reasserts) | 18/20 | 5/6 | `slot0 deliver`; `cpu1 deliver` |
| FIXB (option b alone) | 11/20 (9 readback rows red) | 8/8 | — |
| FIXD (a+b) | 11/20 (same 9) | 8/8 | — |

Logs: `opus_p1_logs/T_det_<V>.out`, `T_acc_<V>.out`; diffs `diff_<V>.diff`.

### Option (b) vs the shipped #438 detector — the adjudication's prediction is MEASURED CORRECT

```
BASE        LUNA_INTMASK_WITNESS=PASS
FIXA        LUNA_INTMASK_WITNESS=PASS      <- (a) leaves es438 green
FIXA_CLAMP  LUNA_INTMASK_WITNESS=PASS
FIXB        FAIL  D4 readback from INT_ST_MASK1 ... ; E2 LATCH ... 4 hits/2 regs
FIXD        FAIL  D4 ... ; E2 ...
```
Exactly rows **D4 and E2**, exactly as batch-7 predicted. (b) also reds nine rows of *this* round's detector (absent-slot readbacks go to 0). `E438_*.out`.

## 3. The accept-row channel — it works, and here is the shape

glm is **right** that a MASK1 readback cannot carry it (the read path uses `d->interrupt_status & currentMask`; the software bit is OR'd only into `reassert_interrupts()`'s *local* `status`). The working channel is **cpu 1's own exception entry**:

- `-n 2 -V -e luna-88k` (committed machine description, unmodified; `machine` reports 2 running cpus)
- `focus 1`; `VBR=0x00040000`; `PSR=0x80000000` (**`M88K_PSR_IND`=0x2 must be cleared** — `cpu_m88k.c` starts CPUs with `M88K_PSR_MODE | M88K_PSR_IND`); `pc=` a `br .` park
- read state with **`reg 1,c`** / **`reg 1`**, never `print` — `print` emits a bare `0x0` with no `=`, which is what broke the earlier attempt
- arm MASK1 with **0x04000000 (bit 26 only)**: `dev_luna88k.c` connects only lines 6,5,4,3 (bits 31,30,29,28), so **nothing but `software_interrupt_status[1]` can raise bit 26**
- store 1 to SOFT_INT1, park cpu 0, `breakpoint add VBR+8`, **`continue`** (delivery is gated by `if (!single_step)` in `cpu_dyntrans.c`)

Measured under FIXA:
```
ACCEPT_ROW=cpu1 deliver  OK  cpu1 pc=0x00040008  SXIP=0x00030102  EPSR 0x00000000->0x80000000
ACCEPT_ROW=cpu1 shadow   OK  PSR=0x8000000b (IND set)
ACCEPT_ROW=cpu0 parked   OK  cpu0 pc=0x00030000
ACCEPT_RESULT=8/8
```
**Negative control** (separate session, no SOFT_INT1 store): `nodeliver ctl OK — cpu 1 does NOT enter its vector in 12 s`. Under M_HARD1: `cpu 1 never entered its vector in 40s`.

The same shape works on the **default 1-cpu config for slot 0** (`slot0 deliver`), and that row is the sole killer of M_NOASSIGN.

## 4. The exact diff I built (`opus_p1_logs/diff_FIXA.diff`, tag `#503` since HEAD's top block is `#502`)

```c
 struct luna88k_data {
+	/*  #503: nr of CPUs actually INTERRUPT_CONNECTed at DEVINIT.  Slots
+	    at or above this index were never connected, so their
+	    cpu_irq[].interrupt_assert/deassert pointers are NULL.  */
+	int		ncpus;
 	struct interrupt cpu_irq[MAX_CPUS];
@@
-	for (cpu = 0; cpu < MAX_CPUS; cpu++) {
+	for (cpu = 0; cpu < d->ncpus; cpu++) {		/*  #503  */
@@
 	memset(d, 0, sizeof(struct luna88k_data));
+	/*  #503: bound reassert_interrupts() to the slots connected below;
+	    walking all MAX_CPUS called a NULL interrupt_assert for an
+	    unpopulated slot -- a guest store to SOFT_INT1 killed the host.  */
+	d->ncpus = devinit->machine->ncpus;
```

## 5. Rows I recommend the detector ship with (each with its CHANNEL)

**Mandatory — each has a measured sole kill or a floor duty:**

| row | kills | observable that differs |
|---|---|---|
| `live`, `live2` | identity (floor c) | RAM word through the same decode |
| `devsig` | RAM-vs-device | MASK0 readback `0x00fc0000` — the handler's own `>>8` |
| `slot0` | attribution | the same two stores on the **connected** slot survive |
| `mask1` | option-(b)-shaped edits | readback `0x00fc0000` vs `0` (measured: FIXB reds it) |
| **`soft1`** | M_REVERT, M_OFFBY1, M_NULLA, M_LATCH, M_GUARDASSERT | host alive. **Two channels in one row**: the *store* exercises ASSERT, the *readback* exercises DEASSERT (read-clears the pending bit, so the next reassert takes the else arm). **Do not split it** — three mutants die on the readback, not the store |
| **`cpu0 setup` + `slot0 deliver` + `slot0 shadow`** | **M_NOASSIGN, M_NOREASSERT2** | cpu0 `pc == VBR+8`, EPSR/PSR shadows. Free-running, default config. **Sole killer** — every survival row is green under M_NOASSIGN |
| **`cpu1 deliver` + `cpu1 shadow` + `cpu0 parked` (`-n 2`)** | **M_HARD1** | cpu1 `pc == VBR+8`. **Sole killer of the clause-(d) mutant** |
| `nodeliver ctl` (`-n 2`, separate session) | makes the two above attributable | with nothing pending, no vector entry in 12 s |
| `two cpus`, `cpu1 setup`, `mask1 land`, `survive` | premise pins | 2 running cpus; IND clear; store lands on 2 cpus |

**Measured redundant under (a) — drop, or ship with an explicit "no measured kill":** `soft1x2`, `mask1 disarm`, and the entire slot-2/slot-3 block. No mutant in the table is killed by any of them alone. The reason is structural: (a) is *one loop bound*, so any mutant that reaches slot 1 reaches slots 2 and 3 too, and `soft1`'s readback already carries the deassert channel. They would earn their place only under (b)/(d), where the decline is per-arm and a missed `case` label is possible. **`mask1 disarm` as I cut it is vacuous by construction** — by the time it runs the pending bit is already cleared and `irqActive[1]` is 0, so its else arm calls nothing in *any* variant; re-cut it to disarm with no intervening read if it is kept.

**Contract (clause e):** these rows are written to the option-(a) expectation *that the store lands and reads back*. If `lunaabsentmaskdecl` later chooses (b), nine of them must be re-pinned.

## 6. Adjudicating the seats

- **glm's mechanism reasoning is right; its prescribed rows are not needed.** M_NULLA and M_LATCH both die — but **on the SOFT_INT1 readback**, inside the frozen `soft1` row. The post-trigger disarm row and the second-arming row buy nothing measured: the SOFT_INT read *is* a disarm.
- **glm's "no planned row can distinguish a both-sided NULL guard from (a)" is MEASURED TRUE.** M_NULLAB scored 20/20 + 8/8 — a genuine **equivalent mutant**, not coverage debt. The choice between (a) and a both-sided NULL guard is therefore warrant-based and permanently unmeasurable here; the only divergence (ncpus>=2 with a failed `INTERRUPT_CONNECT`) cannot be produced by a probe.
- **grok's Q4 free-running shape is exactly right** and I measured it working.
- **grok's M_STOREBUTNOREASSERT escapes — and I measured why.** M_NOREASSERT (SOFT arm's `reassert_interrupts(d)` deleted) scores 20/20 + 8/8. Deleting the *device-line* handlers' reassert calls as well (M_NOREASSERT2) reds `slot0 deliver`. **So the clock's own reassert carries the delivery**: `reassert_interrupts()` has four call sites, and any device line re-runs the whole loop. A free-running row proves *the loop delivers*, never *this call site ran*. That call site is outside the (a) diff, so it is disclosed coverage debt, not a floor cell — and it independently confirms the brief's corollary that on a running guest the next device interrupt re-enters the loop.
- **minimax prefers (d): rejected on measurement.** (d) reds D4 and E2 of the shipped #438 detector and nine rows of this one, for an unsourced board-model claim. (a) reds nothing.
- **kimi's `MIN(MAX_CPUS)` clamp: measured NOT a live hazard.** `-n 5` and `-n 8` are refused by `dev_luna88k.c` itself — `printf("LUNA 88K can't have more than 4 CPUs.\n"); exit(1);` — before any guest instruction. FIXA_CLAMP measured **identical on all 28 rows**. Under the addition licence, "cannot hurt" is not a warrant, so I do **not** recommend it as required. There is one real transferred warrant if the round wants it: that `exit(1)` sits ~40 lines *after* the assignment and is itself a candidate of this project's `exitsweep` de-fatalisation campaign; de-fatalise it into a decline and `d->ncpus` becomes unbounded, walking `cpu_irq[4..]` out of bounds.

## 7. Premises settled by measurement, not argument

- `m->ncpus = 1` default — `core/emul.c:490`. Confirmed.
- **`MAX_CPUS` appears exactly once as a loop bound** in `dev_luna88k.c` — there is **no second walk today**. (Both glm and codex filed this as unsettleable.)
- `reassert_interrupts` has **four** callers: the two device-line handlers (which have no cpu pointer — this is why the `d->ncpus` *field* is the right shape, not a `machine` deref) plus the MASK-write and SOFT_INT arms.
- `d->cpu_irq[]` has **no consumer outside** `dev_luna88k.c` (`dev_bebox.c` has its own unrelated `cpu_irq[2]`).
- Interrupt lines used are 6,5,4,3 -> status bits 31,30,29,28. **Bits 26 and 27 have no device**, which is what makes the bit-26 arming an attributable channel.
- **Severity HIGH stands.**

## 8. Two things I found that were not asked

1. **The codex seat DID NOT ANSWER pass 1.** Its 21,284-byte file is the echoed brief plus `ERROR: This content was flagged for possible cybersecurity risk.` twice. The panel's own `SEATS.txt` correctly calls it `ECHO-ONLY -- NOT A REVIEW`, but the header then reads `SEATS: 6/6 scriptable produced output`. **Pass 1 had FIVE answering seats**, and my own task brief inherited the "six seats have answered" wording. This is a seat failure, not agreement.
2. **Q6: the `default:` arm's `cpu->running = 0; return 0;` has no ledger row.** `grep -o '"id": "luna[a-z0-9]*"' ledger.json` returns only `lunaabsentcpu` and `lunafuse` (the fuse-ROM byte-write arm — a different defect). Not filed.

## Workspace state

Scratch clone `/tmp/gxopus_lunaabs` only. Stale clone and its sentinel removed at start. Two-part clearance at the end: **PART1 source `cmp`-clean vs GXEMUL-SEC, PART2 binary newer than source, `.MUTANT` cleared.** `build/`, `est/`, `build-asan/`, `/tmp/gxsec-build` all verified `cmp`-clean for `dev_luna88k.c`; nothing written to `GXEMUL-SEC/`. All probe outputs, diffs and the patch preserved under `_scratchpad/lunaabs/opus_p1_logs/` (58 files). No gate or battery was run. No red row needed a solo re-run — every kill was a host death or a not-delivered free-run, neither of which is load-sensitive.
