# #529 crimewidthkill -- pass 2, Opus 5 compile-and-measure seat (2026-09-13)

Liveness token: `OPUS_CRIME_P2_20260913`

**VERDICT: HOLD -- the detector, not the fix.**  `if (relative_addr < CRIME_INTSTAT) goto crime_declined;` in
place of `goto crime_declined;` scores **40/40, CONTROL=OK** on the shipped detector (`logs/probe_a_lo10.raw`),
while a refused `lb`/`sb` at +0x10 or +0x18 now raises cause.IP2 and a refused `lb`/`sb` at +0x38 advances
CRIME_TIME (`logs/esc_a_lo10.raw`, 6 diffs).  The one-label forms at INTMASK, INTSTAT and TIME also score 40/40.
That is a narrower decline, which contract item 3 claims, and the DISCLOSED bullet saying no observable separates
those cells is measured false.  The product fix itself: no defect found.

## Apparatus

* Scratch clone `/tmp/gxopus529p2` = `cp -a /tmp/gxopuscrime`; `dev_sgi_ip32.c` `cmp`-clean against
  GXEMUL-SEC (md5 5919a5a7...) before mutant 1; baseline rebuilt in the clone, `[ gxemul -nt src ]` checked.
* Clone-local `.MUTANT` sentinel per mutant; after the table: source restored from SEC, `RESTORE_CMP CLEAN`,
  rebuilt, restored binary byte-identical to base, sentinel removed (`logs/table.out`).
* Detector: frozen copy of `regress/crime_width_probe.py`, md5 a338b7ae... (= table 1's instrument).
  Extra observation probe `scripts/crime_p2_escape.py` (frozen, md5 in `logs/INSTRUMENT.md5`): every channel
  has a CONTROL on an accepted width showing it varies; base scores 21/21 (`logs/esc_base_standalone.raw`).
  (Its docstring says "fix: s1 == 0" for E3; the row actually tests `< 0.1 s of ticks` because the one tick after
  step 1 adds 66-132 -- measured, see below.  The docstring is stale, the row is what ran.)
* Mutant generator `scripts/mutants_p2.py` (find-text exactly once, else refuse).  Every build rc 0 and fresh.
  Every `probe_*.raw` ends `CRIMEP_DONE`, every `esc_*.raw` ends `P2ESC_DONE` (checked before copying).

## Kill table (pass 2, 17 mutants)

| mutant | exact edit (post-fix `dev_sgi_ip32.c`) | detector | failing rows | escape probe | disposition |
|---|---|---|---|---|---|
| a_ctl | `goto crime_declined;` -> `if (relative_addr != CRIME_CONTROL) goto crime_declined;` | 37/40 | sh08 pc, sh08 run, sb08 msg | 21/21 | KILLED |
| a_rev | ... `if (relative_addr != CRIME_REV) goto crime_declined;` | 38/40 | lb rev pc, lh rev pc | 19/21 (revw sh/sb pc) | KILLED |
| a_al8 | ... `if (relative_addr & 7) goto crime_declined;` | 35/40 | sh08 pc/run, sb08 msg, lb/lh rev pc | 13/21 | KILLED |
| **a_lo10** | ... `if (relative_addr < CRIME_INTSTAT) goto crime_declined;` | **40/40** | none | **15/21**: imask lb/sb, istat lb/sb, time s1, time sb s1 | **REAL ESCAPE** |
| **a_imask** | ... `if (relative_addr != CRIME_INTMASK) goto crime_declined;` | **40/40** | none | 19/21: imask lb, imask sb | **REAL ESCAPE** |
| **a_istat** | ... `if (relative_addr != CRIME_INTSTAT) goto crime_declined;` | **40/40** | none | 19/21: istat lb, istat sb | **REAL ESCAPE** |
| **a_time** | ... `if (relative_addr != CRIME_TIME) goto crime_declined;` | **40/40** | none | 19/21: time s1, time sb s1 | **REAL ESCAPE** |
| a_revw | ... `if (writeflag == MEM_READ \|\| relative_addr != CRIME_REV) goto crime_declined;` | 40/40 | none | 19/21: revw sh pc, revw sb pc | REAL ESCAPE (joint cell, see Q3) |
| t_nohint | label ` crime_declined:` moved from above the HARDINT restore to just above `if (writeflag == MEM_READ)` | 40/40 | none | 21/21 | EQUIVALENT (nothing on the declined path writes HARDINT/SOFTINT; prelude already set INTSTAT to the same value) |
| t_ret | label moved to just above `return 1;` (skips the tail's `memory_writemax64`) | 40/40 | none | 21/21 | EQUIVALENT (#95 pre-zero; same as table 1's return1) |
| l_noonce | `"  (once) ]\n"` -> `" ]\n"` | 40/40 | none | 21/21 | records-only escape: text loses the house `(once)` marker (`logs/text_probe.out`) -- contract 6 does not claim it |
| l_assign | `d->warned \|= CRIME_W_LEN;` -> `d->warned = CRIME_W_LEN;` | 40/40 | none | 21/21 | EQUIVALENT today (only one bit exists); latent for a second site |
| l_static | per-instance latch -> `static int w529` function-local latch | 40/40 | none | 21/21 | EQUIVALENT on ip32 (one CRIME instance) |
| l_addrmask | `(int) relative_addr` -> `(int) (relative_addr & 0x3f)` in the announce | 40/40 | none | 21/21 | records escape: `lb +0x48` announces `at 0x8`, `lb +0x208` announces `at 0x8` (`logs/text_probe.out`); every rowed offset is < 0x40 |
| x_mc4 | `} else if (len == 4) {` -> `} else if (len == 4 && relative_addr < 0x200) {` | 40/40 | none | 20/21: `lw +0x214` (bank 1 ctrl) = 0 not 1 | REAL ESCAPE, outside contract 5's stated CRIME_DOG scope |
| x_mc8 | `if (len == 8) {` -> `if (len == 8 && relative_addr < 0x200) {` | 40/40 | none | 20/21: `ld +0x210` = 0 not 1 | REAL ESCAPE, same |
| x_sext | 4R arm `(int32_t)` -> `(uint32_t)` (both halves) | 40/40 | none | 21/21 | EQUIVALENT (memory_writemax64 writes only `len` bytes; the CPU sign-extends) |

### The observables, with values

* **INTMASK / INTSTAT (reassert).**  Session: `sd` INTMASK = 0x10000000 (INTMASK arm, reassert, status 0);
  `sd` SOFTINT = 0x10000000 (DEFAULT arm -- stored, **no reassert**, so the CPU line stays low: `print cause`
  shows IP2 clear); then one access AT the label.  CONTROL: an accepted `lw +0x18` / `lw +0x10` sets cause
  IP2 (0x400) at once (`crime_interrupt_reassert` -> `INTERRUPT_ASSERT` -> `mips_cpu_interrupt_assert` ORs the
  line into CAUSE synchronously, visible while stepping).  FIX: refused `lb`/`sb` there leave IP2 clear.
  a_lo10 / a_imask / a_istat: IP2 **set**.  Reassert is NOT idempotent: the line is stale whenever SOFTINT (or
  anything else reaching the default arm) changed without a reassert, and the tick that would fix it runs every
  2^14 instructions.  Guest-visible: an interrupt becomes pending at the refused instruction.
* **TIME (update).**  An accepted `ld` returns odata read BEFORE the switch's `crime_update_crime_time()`, so it
  returns the value left by the PREVIOUS update.  Session: `ld +0x38` (first update only latches last_us),
  refused `lb`/`sb +0x38`, `ld +0x38` -> s1.  FIX and every fix-equivalent binary: s1 = **66 or 132** (the one
  device tick right after step 1).  a_lo10 / a_time: s1 = **143,121,924 .. 143,682,792** (the ~2 s since the
  first update).  CONTROL: the next accepted `ld` reads ~286M on every binary.
* **REV write.**  The CRIME_REV arm does not test writeflag: an accepted `sw +0` from pc 0xbfc05180 sets pc = ra
  (control); refused `sh`/`sb` there: fix pc 0xbfc05184, a_revw / a_rev / a_al8 pc = 0x80004000.
* **DEFAULT arm (host trace only).**  `logs/dbg_probe.out`: under a_lo10 the detector's own `sb +0x1f` session
  prints `[ crime: write to 0x1f: ff (len=1) ]` (a `debug()` line; single-stepping raises verbosity so it
  prints); the fix prints only the announce.  Not guest-visible, but a zero-cost channel in existing sessions.

## Answers

**Q1 (the fix).**  Read every path: a refused width runs the prelude (REV/CONTROL/INTSTAT refresh, RAM-size
checks, bank loop -- the same work an accepted access does, nothing specific to the refusal), announces once
(`d->warned`, per instance, memset(0) at `dev_crime_init`), jumps to the tail, whose HARDINT restore and INTSTAT
recompute are no-ops on this path (t_nohint measured equivalent), answers a read with odata = 0, drops a write,
returns 1 (pc advances, no DBE).  The only prelude hazard is the filed one (bad `-M` exits before the width arm).
`int warned` + `CRIME_W_LEN (1 << 0)` + `(once)` matches the gdrom/sgi_re idiom; `warned` has exactly one writer
(the width arm) and one clearer (the init memset) in the file.  **No defect in the product change.**

**Q2.**  Smallest: `goto crime_declined;` -> `if (relative_addr != CRIME_TIME) goto crime_declined;` (or
`!= CRIME_INTMASK`, `!= CRIME_INTSTAT`), and the most plausible-looking: `if (relative_addr < CRIME_INTSTAT)
goto crime_declined;`.  All 40/40.  Expected catchers and why they cannot: the refusal rows land at +0x7, +0x6,
+0x1f, +0x1e, +0x3f, +0x37, +0x36 (default arm, no effect) and at +0x08 / +0x00 (the only two labels rowed);
no row ever issues a refused access AT +0x10, +0x18 or +0x38, and `latch x5` / `<op> said` count text the
announce prints before the goto, so they are blind to what follows it.  Address-keyed fall-throughs at +0x08 or
+0x00 ARE caught (a_ctl 37/40, a_rev 38/40, a_al8 35/40).

**Q3.**  Accept cells: each reds under its own single-cell mutant (table 1) -- but only on CRIME_DOG; an
address-keyed accept shrink (x_mc4, x_mc8) is outside the rows and should be DISCLOSED as such.  Refusal cells:
the {1,2} x {R,W} cells are each pinned, but only through labels 0x00 and 0x08.  By the carrier's JOIN rule
the skipped switch re-tests `relative_addr` after the join, so each side-effecting label is a floor cell: REV,
CONTROL (rowed) and **INTSTAT, INTMASK, TIME (unrowed, measured non-equivalent, measured 40/40) -- a floor
breach, L2.**  REV x WRITE (a_revw) is a joint of the label with writeflag, which the REV arm does not test:
clause-(e) debt, one session to row if wanted.  DOG and default: equivalent guest-side.
Cheapest repair: two sessions -- (i) the reassert session above with `lb +0x18` then `sb +0x10`, want IP2 clear,
control `lw +0x18` sets IP2; (ii) the TIME session, want s1 < 6.6M (0.1 s of ticks), control next `ld` large --
plus optionally a zero-cost row counting `crime: write to` / `crime: read from` == 0 in the existing refused
sessions (kills a_lo10 via `sb +0x1f`).  Contract item 3 must then name the labels it covers.

**Q4 (records).**
* Probe header DISCLOSED bullet 3 -- "effects are idempotent or overwritten by the tail, and no observable here
  separates them" -- **measured false**: reassert changes cause.IP2; the TIME update is not touched by the tail
  and changes the next TIME read by ~143M.  Only INTSTAT and HARDINT are rewritten by the tail.
* Contract item 3 "(the goto lost, or a narrower decline), at each width x direction cell" -- overclaims: a
  narrower decline keyed on the address escapes at three labels.
* Fix comment: true as written (the two named fall-through effects are real), but incomplete -- a narrow WRITE at
  REV also redirects the PC from the PROM window, and INTMASK/INTSTAT/TIME have effects too.
* Contract 5's scope ("on CRIME_DOG") is stated honestly; add that address-keyed shrinks are outside it.

**Q5 (the brief).**
* Wrong: the DISCLOSED bullet 3 claim above (the brief reproduces it verbatim).
* Wrong as a reason: "the goto is kept ... because the tail also restores HARDINT and recomputes INTSTAT" -- on
  the declined path both are no-ops (nothing between entry and the label writes HARDINT or SOFTINT; the prelude
  already set INTSTAT to the same value); t_nohint measures equivalent.  The house-shape reason stands alone.
* Verified: the #95 pre-zero at `src/cpus/memory_rw.c` (`if (writeflag == MEM_READ) memset(data, 0, len);`
  immediately above `paddr -= mem->devices[i].baseaddr;`); `return 0` -> DBE via the `res <= 0 &&
  !no_exceptions` arm; the POSTTABLE's "NOT swept: address-conditioned fall-throughs" is accurate and is exactly
  where the escape was.  Note the device maps 0x280 bytes (`DEV_CRIME_LENGTH`), not the 0x80 of the function's
  upstream comment, so the decline also covers memory control (`lb +0x208` announces `at 0x208`).
