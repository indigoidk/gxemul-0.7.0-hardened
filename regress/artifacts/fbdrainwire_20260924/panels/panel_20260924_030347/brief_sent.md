# PASS 1 -- `#548`: wire `regress/fbpending_drain_probe.py` into gate 14 before its exemption lapses (2026-09-27)

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/` (ignore any other `src/`).
2026-09-24.  **FIRST LINE:** `VERDICT: <PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED>`, then numbered findings.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  If you cannot read files that is expected -- every fact you need is inlined; name any premise you
cannot settle from this packet.  **ENUMERATE rather than reason** where a claim is arithmetic.  Seats that read files: stay
within `GXEMUL-SEC/src/devices/dev_footbridge.c`, `GXEMUL-SEC/regress/fbpending_drain_probe.py`,
`GXEMUL-SEC/regress/gate_arm.sh` (HEAD's copy: `git show HEAD:regress/gate_arm.sh` -- the working copy carries another
unit's uncommitted section) and `GXEMUL-SEC/tools/pipeline/check_probe_wiring.py`; please do not read
`GXEMUL-SEC/regress/artifacts/` or `tools/pipeline/ledger.json`.

## 0. HAS THIS SHIPPED?  `grep -n fbpending_drain regress/gate_*.sh` at HEAD: no gate runs it.  Not shipped.

## 1. SETTLED PREMISES (read from HEAD today)

* **The exemption, verbatim** (`tools/pipeline/check_probe_wiring.py`; from 2026-09-28 a lapsed entry reds precommit
  section R on every commit, and a WIRED probe that keeps its entry reds as a STALE EXEMPTION):

```
    "fbpending_drain_probe.py": ("2026-09-27",
                                 "REPORT-ONLY by default: EXPECT_CAP must be set before a "
                                 "gate row can mean anything, so wiring is a design step first"),
```

* **The bound under test** -- `#442`'s repair in `src/devices/dev_footbridge.c`.  The callback every timer runs:

```
static void footbridge_pending(struct footbridge_data *d, int nr)
{
	if (d->pending_timer_interrupts[nr] >= d->pending_bound[nr])
		d->pending_timer_interrupts[nr] = 1;
	else
		d->pending_timer_interrupts[nr] ++;
}

static void timer_tick0(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 0); }
static void timer_tick1(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 1); }
static void timer_tick2(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 2); }
static void timer_tick3(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 3); }
```

  and where `pending_bound` is set when a timer is (re)armed, `freq` being that timer's rate in Hz:

```
	{
		double bound = freq;
		if (!(bound <= (double)TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY))
			bound = (double)TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY;
		if (!(bound >= 1.0))
			bound = 1.0;
		d->pending_bound[timer_nr] = (int) bound;
	}
```

  So the bound is ONE SECOND of that timer's ticks.  The probe arms timer N at TIMER_FCLK_256 with load 256 on `-E cats`
  (emulated_hz 50,000,000): 50e6 / (256*256) = 762.94 Hz, so `pending_bound[N]` = (int) 762.94 = **762**.

* **The probe** -- its header, verbatim:

```
#!/usr/bin/env python3
"""fbpending DRAIN PROBE -- a RUNG-3 detector that MEASURES the pending-interrupt
backlog of footbridge timer 1 in ~10 s, instead of waiting 43 s for it to overflow.

WHY THIS EXISTS.  The rung-3 witness (fbpending_witness.py) proves the defect by
running until the counter wraps, which takes 42.95 s at cats' emulated_hz and cannot
be made faster than 31.51 s on ANY machine (the delivery ceiling is
TIMER_MAX_CATCHUP x TIMER_BASE_FREQUENCY = 68,157,440 increments per wall second, and
timer_tick0 is called from nowhere else).  A gate row cannot spend that.

THE TRICK: MEASURE THE COUNTER, DO NOT WAIT FOR IT TO OVERFLOW.

  1. The guest arms timer 1 at a KNOWN SLOW rate.  cats' emulated_hz is 50,000,000 and
     reload_timer_value() asks for emulated_hz / effective_cycles(load, ctrl, 1).  With
     TIMER_FCLK_256 and load 256 that is 50e6 / (256*256) = 762.94 Hz.
  2. It free-runs for T seconds.  Nothing acks, so the backlog is rate*T -- UNLESS the
     device bounds it.
  3. It then FREEZES the timer by writing TIMER_1_LOAD = 0x00FFFFFF while keeping
     TIMER_FCLK_256: the rate falls to 50e6/(0xFFFFFF*256) = 0.0116 Hz, one tick per
     86 s.  *** A LOAD WRITE DOES NOT CLEAR pending_timer_interrupts *** (only a
     TIMER_x_CONTROL write WITHOUT TIMER_ENABLE does -- dev_footbridge.c, the
     `pending_timer_interrupts[timer_nr] = 0` store in the `else` of `if (idata &
     TIMER_ENABLE)`), so the
     backlog survives the freeze.  That turns a moving quantity into a static one.
  4. It then DRAINS AND COUNTS.  DEVICE_TICK writes timer_value = random() %
     effective_cycles(load, ctrl, 0) whenever the backlog is > 0, and with load
     0x00FFFFFF that modulus is 0xFFFFFF, so the produced value is in [0, 0xFFFFFE].
     The guest writes the sentinel 0x00FFFFFF -- which the modulo CANNOT produce and
     which survives TIMER_x_VALUE's own `idata & TIMER_MAX_VAL` mask -- and spins.  A
     changed read means one tick was delivered; the guest then writes TIMER_1_CLEAR
     (one decrement) and repeats.  When the spin budget expires with the sentinel
     intact, the backlog is 0 and the number of decrements IS the backlog.

  The measured number is the whole verdict: pre-fix it is rate*T.  No wrap, no 43 s,
  and the row reports a NUMBER rather than a boolean.

  *** POST-FIX IT IS **NOT** THE CAP, AND THE FIRST VERSION OF THIS PARAGRAPH SAID IT
  WAS. ***  Measured by a pass-2 seat on ONE binary with ONE bound of 762: backlog 3 at
  4 s, 100 at 46 s, 375 at 0.5 s.  Once the bound is first reached the number is a
  MODULAR RESIDUE of the delivered tick count, not the bound itself.

  That is why `--expect-cap` is a one-sided `bD <= CAP` and CANNOT distinguish a bound
  of 762 from one of 7: the quantity it tests is structurally <= the bound whatever the
  bound is.  The rows that actually pin the bound's VALUE live in
  regress/diff_fbpending_bound.c (R5, an equality against the timer's own rate, and R6,
  which re-arms at a different rate) -- and they exist because a one-token mutant
  (`freq / 100.0`) destroyed 99% of the guest's clock while passing this probe.

ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
  dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
  the guest DISABLES a timer: TIMER_x_CONTROL without TIMER_ENABLE zeroes the counter
  once (the same `= 0` store) and leaves the struct timer running.  So timer_tickN keeps incrementing a
  counter that DEVICE_TICK will never look at.  Arm X arms the timer, immediately
  disables it, free-runs, re-enables (which does NOT clear the counter) and then
  measures.  A non-zero result proves the counter accrues while the device is disabled
  -- which is exactly the state in which a bound placed in DEVICE_TICK cannot run.

ARMS
  D  enabled throughout.  Backlog after T seconds.
  X  disabled during the accrual.  Backlog after T seconds.  Q1's discriminator.
  T  negative control: MMU left on, so the footbridge is not mapped.  Must not return
     the device's answers.  (machine_cats.c's boot page tables map only the low 256 MB;
     the footbridge is at PA 0x42000000.)
  H1/H2 harness legs (#545) -- they REPLACED arm K, a read of IRQ_ENABLE_CLEAR (+0x18c) that
     the device used to answer with fatal() then exit(1); #545 declines it.  H1: an unknown -E
     name -- no prompt anywhere in the buffer, the diagnostic naming it, exit 1.  H2: arm D's prologue verified (21 steps, r3/r5/r6/r7),
     a fresh reg, quit, then one more reg that must fail with `dead` set BEFORE close(), exit 0.
     Every surviving arm must reap exit 0.  NOT COVERED: moving s.close() ahead of that next
     send keeps H2 green (the send fails on the closed descriptor), and the legs cannot defend
     their own predicates -- harness edits, reviewed, not rowed (footbridge_sites_probe.py).

Every RAM output word is poisoned with 0xDEADBEEF first and every verdict row requires
the values it consults to be PRESENT.  Every planted instruction is checked, as it
EXECUTES, against the emulator's own disassembly (the hand-assembled-encoding trap).

usage: fbpending_drain.py <gxemul-binary> <four-byte-raw-stub>
                          [--accrue S] [--expect-cap N] [--learn]
"""
```

  and its verdict block, verbatim:

```
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("FBDRAIN_CONTROL=%s" % ("OK" if ok else "FAILED"))
    print("FBDRAIN_BACKLOG_D=%s" % bD)
    print("FBDRAIN_BACKLOG_X=%s" % bX)
    print("FBDRAIN_CLOCK_DEAD=%s" % ("D " if deadD else "") + ("X" if deadX else ""))
    if EXPECT_CAP >= 0 and ok and bD is not None and bX is not None:
        good = (bD <= EXPECT_CAP and bX <= EXPECT_CAP
                and not deadD and not deadX)
        print("FBDRAIN_BOUNDED=%s  (cap asserted: %d)"
              % ("YES" if good else "NO", EXPECT_CAP))
        print("FBDRAIN_VERDICT=%s" % ("PASS" if good else "FAIL"))
        sys.exit(0 if good else 1)
    print("FBDRAIN_VERDICT=REPORT-ONLY")
```

* **Gate 14's existing footbridge wiring** (`regress/gate_arm.sh` at HEAD), the idiom a new block would copy:

```


# ---------------------------------------------------------------------------
#  #432: THE FOOTBRIDGE'S FIRST REACHABILITY WITNESS OF ANY KIND.
#
#  Recorded before this probe existed: R6 was the ONLY code round in this tree with no
#  reachability witness -- no rig boots a footbridge machine and there is no m8online analog.
#  regress/diff_footbridge.c calls the device functions DIRECTLY, so it proves BEHAVIOUR and
#  would stay green under a change that unmapped the device entirely.  This drives real guest
#  ldr/str through the real address decode and the real memory_rw plumbing on a COLD DEBUGGER:
#  measured 1.9 s for three arms, against a rig boot this tree does not have at all.
#
#  IT LIVES HERE, in the ARM gate, for the same reason m8820x_sites_probe.py lives in
#  gate_m88k_rounding.sh: `cats` is an ARM machine and this gate already writes the four-byte
#  raw stub that makes such a machine construct.  A new gate script would move GATE_MANIFEST,
#  which is a bigger claim than one probe is worth.
#
#  THE TRAP IT GUARDS, and it nearly produced a confident wrong answer.  machine_cats.c:131
#  maps only the low 256 MB and the footbridge is at PA 0x42000000, so under the boot-time MMU
#  every device row reads 0x0 WITH A RAM LIVENESS ROW STILL GREEN -- which is exactly what an
#  absent device looks like.  The probe's arm T runs the same program with the MMU-disable
#  instructions replaced by nops and requires that it CANNOT produce the device's answer; arm L
#  reads CP15 c1 back and requires bit 0 clear.  Negative-controlled in both directions.
FBLOG=$LOGDIR/footbridge_sites.log
python3 footbridge_sites_probe.py "$PMAX" "$STUB" > "$FBLOG" 2>&1 || true
grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|N[0-5O]) " "$FBLOG" | sed 's/^/       /'
```

## 2. THE PROPOSAL

Add, beside that block in `regress/gate_arm.sh`, a run of the drain probe with `--expect-cap 762` and three rows:
`FBDRAIN_CONTROL=OK` (the probe's own controls -- liveness, device signature, MMU, encodings, harness legs, the MMU-on
negative control, termination), `FBDRAIN_VERDICT=PASS` (the one-sided bound: both arms' backlog <= 762), and an empty
`FBDRAIN_CLOCK_DEAD`.  Delete the EXEMPT entry in the same edit.  Run gate 14 once, green, before commit.

**Test-first, before any edit:** on HEAD's binary the rows are green; on a scratch-clone MUTANT with the bound removed
(`footbridge_pending` increments unconditionally) `FBDRAIN_VERDICT` is FAIL -- predicted backlog ~ 762.94 x the accrual
seconds, ~3,050 at the default 4 s, > 762.

**The contract (clause e), stated now so a later escape has a disposition:** the rows catch the bound's REMOVAL or any
RAISE above 762 on the timer(s) run; they cannot see a bound BELOW 762 (the backlog is structurally <= the bound), nor
the reset-to-0 mutant the device comment says survives this probe -- `regress/diff_fbpending_bound.c` in gate 2 carries
the equality and trough rows.

## 3. QUESTIONS

1. **Premise audit.**  I believe the bound at the probe's rate is exactly 762 and that `--expect-cap 762` is therefore
   the tightest cap that cannot false-fail.  Check the arithmetic and the `(int)` truncation; check whether any timer can
   be armed at a DIFFERENT rate by the probe, and whether the 4 s accrual always exceeds 762 ticks on a loaded host.
2. **One timer or four?**  The probe's header says a fix applied to only one of the four callbacks passes a row that
   exercises only one timer, which is why `--timer` exists.  `footbridge_pending(d, nr)` is shared today, so a
   per-callback defect needs a callback-level edit.  Is running all four (`--timer 0..3`) worth four times the wall
   time, or is one enough?  Say whether an edit exists that passes a timer-0-only row yet leaves another timer unbounded.
3. **Does any single edit to the bound pass the proposed rows while re-opening #442's defect** (an unbounded, or
   wrapping, counter on the path a guest drives)?  Say whether one exists; name it if you can.
4. **Option set.**  Gate 14 (which already drives `-E cats` for the sites probe) versus another gate; three rows versus
   one; the `--accrue` length.  Is there an existing idiom in `gate_arm.sh` I have not named?
5. **Records.**  The EXEMPT entry goes in the same edit (a wired probe that keeps it reds as STALE).  Anything else the
   wiring owes -- `GATE_MANIFEST`, a gate pin, a count some other check derives?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
