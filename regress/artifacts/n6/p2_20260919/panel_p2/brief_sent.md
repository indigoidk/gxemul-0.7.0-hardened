# PASS 2 (THE REAL DIFF) -- `n6` / #539: footbridge IRQ_ENABLE_SET read ACCEPTED; kill arm bridged to +0x18c; seven ACCEPT rows

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this project's brief stated wrongly, and this round's OWN
pass 1 found seven defects in its brief (Q was stated two ways; a Q2 item was cited but absent; the E5/E6 order
would have reddened a correct build; "seven invalid-direction sites" was false; the MMU-on zero was mis-explained;
the drain/witness controls discard the exit status; the register dump reads only r0-r7).  **Check the premises,
not just the derivations.**  Where you can settle a claim by opening a file, do that and say READ (file, anchor);
where you reasoned, say REASONED; where you could not, say NOT CHECKED.  VERDICT LINE FIRST.  Counts with
denominators.  If, while verifying a claim, you found something ELSE -- say so.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (WORKING TREE on HEAD a11eaac, the #539 edits
uncommitted); ignore any other `src/` under the project root -- `_scratchpad/r6pass2_fb/` holds a 744-line STALE
FORK copy of `dev_footbridge.c` (lines off by tens), and the fork's file is 897 lines.  Scope your reading to
`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`; do not read `regress/artifacts/` or
`tools/pipeline/ledger.json`.  Ordinary engineering language: the sites are terminating calls; the rows are
error-handling checks.  Do not build anything; do not run gates.  The packet-fed seats cannot open files: every
fact they need is inlined below, and a premise you cannot settle from the packet is reported as NOT CHECKABLE,
not guessed.

## 1. WHAT SHIPPED (uncommitted, in the working tree), in one paragraph
`dev_footbridge.c` `case IRQ_ENABLE_SET`, read branch: the `fatal("... ENABLE SET? ...")` and `exit(1)` are deleted;
`odata = d->irq_enable;` is kept, with a `/* #539 */` comment quoting the datasheet (IRQEnable 188h is read-only,
changed only via EnableSet/EnableClear, reset 0 -- DC21285 Table 7-10, 7.3.31).  Option-set member 4, ACCEPT: the
model already held the right value.  Three probes used that read as their "the device can still end the process"
control; all three move to `+0x18c` (IRQ_ENABLE_CLEAR read, write-only per 7.3.32, `ldr r7,[r0,#396]` =
`0xE590718C`, text `ENABLE CLEAR`), in the same commit.  `footbridge_sites_probe.py` gains a FOURTH arm, E, with
its own C1/A1 controls and rows E0,E1,E2,E3,E6,E5 (execution order) + E4; `gate_arm.sh`'s footbridge section
gains three checks (E0-E6 count 7; E0 got=0; E2 got=0x60002002) and echoes E rows.  `fbpending_drain_probe.py`
and `fbpending_witness.py` now DRAIN the pty to EOF (bounded, 5 s) BEFORE closing it, then reap and keep the
status (`exit`, `signal`) on every session-return path; their K rows require the device's complaint AND exit 1,
and every SURVIVING arm must reap exit 0 (`survived()` in R0/T/E and the K row) -- the codex L3 reading's draft,
adopted verbatim, then the kill word and text retargeted to +0x18c.  Stale
`dev_footbridge.c:NNN` citations in the three probes and the gate section are replaced by construct names.

## 2. SETTLED PREMISES (pass 1, nine seats + five codex readings + fable5 adjudication; re-derive any you doubt)
* DC21285 datasheet, verbatim (`_scratchpad/dc21285.txt`):
 6826| 188h                                            IRQEnable     IRQEnableSet
 6827| 18Ch                                            --            IRQEnableClear
 6828| 190h                                            --            IRQSoft
 6913|         This read-only register is used to mask the interrupt input sources and defines which active sources
 6914|         generate an interrupt request to the SA-110 on nIRQ/nFIQ. The value of this register can only be
 6915|         changed by writing to the EnableSet and EnableClear registers.
 6924|                                             Reset value: 0.
 6940|         This write-only register is used to clear bits in the IRQEnable/FIQEnable register.
 1651|        The selected CSR (the CSR with offset equal to SA-110 address A[10:2]) read data is driven onto
 1652|        D[31:0]. If a nonexistent CSR is selected within the CSR address range, zeros are read (no error
 1653|        action is taken). The SA-110 normally stalls for three cycles.
* P = 0x00002002 (bits 1, 13), Q = 0x60000000 (bits 29, 30); P|Q = 0x60002002.  Both loaded from RAM (DATA+8,
  DATA+12) -- P is not a rotated immediate.  MEASURED (Opus, pass 1): `d->irq_status == 0` at every read under
  single-step, so any enable pattern is inert; `cpu_dyntrans.c` suppresses interrupt delivery under `step`.
* The register dump (`reg`) names r10-r12 `sl`,`fp`,`ip` (`cpu_arm.h` ARM_REG_NAMES); the probe's parser now
  reads r0-r9, sl, fp, ip.  ldrh immediates cap at 255, hence `add sl,r0,#0x180` + `ldrh fp,[sl,#8]`.
* E6 (halfword, want 0x2002) is true only while P is set, so E6 runs BEFORE E5 (Clear <- P).
* Mutant (j) (`irq_status | irq_enable` in the SET write arm's assert) is DISCLOSED in the contract, not rowed:
  no step-based row can see the IRQ line; a free-running arm with IRQSoft as its positive control is FILED.
* The +0x18c bridge is TEMPORARY: the round that declines +0x18c retires it and builds the harness legs (startup
  rejection through each probe's own helper; mid-session `quit` with status reaped) in the same commit --
  fable5's D1 ruling, spec = the codex M1 reading.  Not this round.
* The five invalid-direction declines are the NEXT round (one round); the SDRAM_BA_MASK/OFFSET pair is a
  separate round (member 3 by default; member 6 only on a warrant).  Not this round.
* `dev_footbridge.c` under the project root: `./src/` does NOT exist, `_archive/` holds no copy; the hazard is
  `_scratchpad/r6pass2_fb/` (744 lines, stale fork).  `_scratchpad/src/` mirrors the fork.

## 3. THE MEASUREMENTS -- kill table in a scratch clone (/tmp/gx539, cp -a of build/ with every uncommitted src/
##    file restored to HEAD; baseline binary rebuilt there BEFORE mutant 1; the probe FROZEN for the whole table)
Artifacts: `GXEMUL-SEC/regress/artifacts/n6/killtable_20260919/` (PRETABLE.out written at 01:59:21, BEFORE table
1; per-mutant `probe_<name>.raw`; `TABLE.log`).  Pre-fix witness = the NEW probe on the HEAD-source baseline.

| run | rows | verdict | red rows | what it is |
|---|---|---|---|---|
| prefix_HEAD | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | PRE-FIX WITNESS: the new probe on the HEAD-source baseline (E arm HOST-DIED at E0, exit 1, ENABLE SET) |
| base_fixed | 19 of 19 | PASS | none | POST-FIX BASE: the fix applied, rebuilt (gxemul 7f3293e4) |
| a_verbatim | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (a) floor (b): the removed fatal()+exit(1) reinstated verbatim |
| b_ifzero | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (b) exit reinstated only when irq_enable == 0 (E0 sole carrier) |
| c_status | 14 of 19 | FAIL | E1,E2,E3,E6,E5 | (c) body field swapped: odata = d->irq_status |
| d_fiqen | 14 of 19 | FAIL | E1,E2,E3,E6,E5 | (d) body field swapped: odata = d->fiq_enable |
| e_fatalonly | 18 of 19 | FAIL | E4 | (e) fatal() kept, exit(1) dropped |
| f_width | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (f) a width guard: sub-word reads refused with the old death |
| g_mask | 17 of 19 | FAIL | E2,E5 | (g) readback masked to the low 16 bits |
| h_assign | 16 of 19 | FAIL | E2,E3,E6 | (h) SET write arm: |= -> = |
| i_andidata | 18 of 19 | FAIL | E5 | (i) CLEAR write arm: &= ~idata -> &= idata |
| j_orassert | 19 of 19 | PASS | none | (j) DISCLOSED: SET write arm assert condition irq_status & -> | |
| k_clearexit | 18 of 19 | FAIL | K1 | (k) the exit also removed from the CLEAR read (K1 sole carrier) |
| l_topbits | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (l) fatal()+exit(1) kept only for bits 30/31 of the value |

Pre-fix witness RED (10/19: the E arm dies at E0 so every E row and its two controls are absent), post-fix base 19/19
GREEN, 11 of 12 mutants KILLED, and (j) ESCAPED 19/19 exactly as the contract discloses.  Every restore was cmp'd
CLEAN against SEC and rebuilt fresh before the next mutant (sentinel cleared only then).  Kills by channel: (a)(b)(f)(l)
by HOST DEATH in arm E; (c)(d) by value (E1: 0 != P -- indistinguishable from each other, as PRETABLE said);
(e) by E4 only (fatals=6 -- E4 IS the sole carrier in this arm layout); (g) E2+E5; (h) E2+E3+E6; (i) E5 only;
(k) K1 only.  A first launch of the same driver was aborted mid-(b) (Bash-tool timeout hygiene, not a defect) and its
partial logs are kept under `aborted_first_launch/`; the table above is the complete second run (TABLE.log).

The two pending probes, run post-fix against the same clone binary (7f3293e4) with the moved K arm and the
status binding: `fbpending_drain_probe.py` 11/11 controls ok (K=HOST-DIED exit=1 complaint seen; D/X/T/E
SURVIVED exit=0), `fbpending_witness.py` 12/12 ok, FBPENDING_VERDICT=PASS (K exit=1; A/E/T exit=0; 23/23
samples).  Logs: `regress/artifacts/n6/killtable_20260919/pending_probes_postfix/`.

## 4. THE DIFF -- INLINED IN FULL (git diff of the working tree against HEAD a11eaac; frozen copies at
##    `_scratchpad/n6/p2/diff539_4files.patch` md5 1ffb5507 and `diff539_gate.patch` md5 e8a7c3f4)
`git diff --numstat`: dev_footbridge.c INLINED; footbridge_sites_probe.py INLINED; fbpending_drain_probe.py
INLINED; fbpending_witness.py INLINED; gate_arm.sh INLINED (its footbridge hunks only -- the file also carries an
unrelated 59-line hunk at :1728+ from #529's crime_width section, which this round does NOT ship and which is
NOT SHOWN).  `est/src/devices/dev_footbridge.c` is byte-identical to SEC's (cmp) and is NOT SHOWN.

    1| diff --git a/regress/fbpending_drain_probe.py b/regress/fbpending_drain_probe.py
    2| index 4666001..5f39951 100644
    3| --- a/regress/fbpending_drain_probe.py
    4| +++ b/regress/fbpending_drain_probe.py
    5| @@ -18,7 +18,8 @@ THE TRICK: MEASURE THE COUNTER, DO NOT WAIT FOR IT TO OVERFLOW.
    6|    3. It then FREEZES the timer by writing TIMER_1_LOAD = 0x00FFFFFF while keeping
    7|       TIMER_FCLK_256: the rate falls to 50e6/(0xFFFFFF*256) = 0.0116 Hz, one tick per
    8|       86 s.  *** A LOAD WRITE DOES NOT CLEAR pending_timer_interrupts *** (only a
    9| -     TIMER_x_CONTROL write WITHOUT TIMER_ENABLE does, dev_footbridge.c:583), so the
   10| +     TIMER_x_CONTROL write WITHOUT TIMER_ENABLE does -- dev_footbridge.c, the
   11| +     `pending_timer_interrupts[timer_nr] = 0` under `!(idata & TIMER_ENABLE)`), so the
   12|       backlog survives the freeze.  That turns a moving quantity into a static one.
   13|    4. It then DRAINS AND COUNTS.  DEVICE_TICK writes timer_value = random() %
   14|       effective_cycles(load, ctrl, 0) whenever the backlog is > 0, and with load
   15| @@ -47,7 +48,7 @@ THE TRICK: MEASURE THE COUNTER, DO NOT WAIT FOR IT TO OVERFLOW.
   16|  ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
   17|    dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
   18|    the guest DISABLES a timer: TIMER_x_CONTROL without TIMER_ENABLE zeroes the counter
   19| -  once (:583) and leaves the struct timer running.  So timer_tickN keeps incrementing a
   20| +  once (the same `= 0` store) and leaves the struct timer running.  So timer_tickN keeps incrementing a
   21|    counter that DEVICE_TICK will never look at.  Arm X arms the timer, immediately
   22|    disables it, free-runs, re-enables (which does NOT clear the counter) and then
   23|    measures.  A non-zero result proves the counter accrues while the device is disabled
   24| @@ -223,8 +224,8 @@ def build(mmu_on=False, disable_during_accrual=False, kill=False):
   25|          emit(0x54, NOP, "")
   26|          emit(0x58, NOP, "")
   27|      if kill:
   28| -        p.append((0x5c, 0xE5907188, "ldr r7,[r0,#392]",
   29| -                  "arm K: IRQ_ENABLE_SET -> fatal()+exit(1)"))
   30| +        p.append((0x5c, 0xE590718C, "ldr r7,[r0,#396]",
   31| +                  "arm K: IRQ_ENABLE_CLEAR read -> fatal()+exit(1) (#539: was +0x188)"))
   32|          emit(0x60, NOP, "")
   33|          return p
   34|      #  accrual loop -- publishes liveness and a fresh VENDOR_ID every iteration
   35| @@ -400,13 +401,28 @@ class Session:
   36|                  got[k] = int(m.group(1), 16)
   37|          return got
   38|  
   39| -    def close(self):
   40| -        for f in (lambda: os.write(self.fd, b"quit\n"), lambda: time.sleep(0.3),
   41| -                  lambda: os.close(self.fd), lambda: os.waitpid(self.pid, 0)):
   42| -            try:
   43| -                f()
   44| -            except Exception:
   45| -                pass
   46| +    def close(self, patience=5.0):
   47| +        try:
   48| +            os.write(self.fd, b"quit\n")
   49| +        except OSError:
   50| +            pass
   51| +        # Drain through EOF; closing a live master can SIGHUP the child.
   52| +        deadline = time.monotonic() + patience
   53| +        while True:
   54| +            left = deadline - time.monotonic()
   55| +            if left <= 0 or not self.rd(min(0.1, left)):
   56| +                break
   57| +        try:
   58| +            os.close(self.fd)
   59| +        except OSError:
   60| +            pass
   61| +        try:
   62| +            _, st = os.waitpid(self.pid, 0)
   63| +        except OSError:
   64| +            st = None
   65| +        code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
   66| +        sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
   67| +        return dict(exit=code, signal=sig)
   68|  
   69|  
   70|  def plant(s, prog):
   71| @@ -467,8 +483,7 @@ def run_arm(label, mmu_on=False, disable=False, accrue=None, max_drain_s=30.0):
   72|      prog = build(mmu_on=mmu_on, disable_during_accrual=disable)
   73|      s = Session()
   74|      if not s.wait(timeout=120):
   75| -        s.close()
   76| -        return dict(label=label, status="NO-PROMPT")
   77| +        return dict(label=label, status="NO-PROMPT", **s.close())
   78|      plant(s, prog)
   79|      bad, cov, ex = step_and_check(s, prog, PROLOGUE_N)
   80|      #  ACCRUAL.  The SIGALRM timer is stopped at the debugger prompt
   81| @@ -494,11 +509,11 @@ def run_arm(label, mmu_on=False, disable=False, accrue=None, max_drain_s=30.0):
   82|              break
   83|      r = s.regs()
   84|      status = "HOST-DIED" if s.dead else ("SURVIVED" if ok else "INTERRUPT-LOST")
   85| -    s.close()
   86| +    end = s.close()
   87|      return dict(label=label, status=status, regs=r, badis=bad, executed=ex,
   88|                  covered=cov, want={CODE + o for o, *_ in prog},
   89|                  accrued=accrued, mid=mid, out=out, phase=phase,
   90| -                drain_s=time.time() - t0)
   91| +                drain_s=time.time() - t0, **end)
   92|  
   93|  
   94|  #  Arm E walks the drain body in SEGMENTS, each entered by setting pc directly.
   95| @@ -530,8 +545,8 @@ def run_drainenc():
   96|      prog = build()
   97|      s = Session()
   98|      if not s.wait(timeout=120):
   99| -        s.close()
  100| -        return dict(status="NO-PROMPT", badis=[], covered=set(), nsteps=0, executed=[])
  101| +        return dict(status="NO-PROMPT", badis=[], covered=set(), nsteps=0,
  102| +                    executed=[], **s.close())
  103|      plant(s, prog)
  104|      bad, cov, ex = step_and_check(s, prog, PROLOGUE_N)
  105|      for head, n in E_SEGMENTS:
  106| @@ -543,25 +558,24 @@ def run_drainenc():
  107|          cov |= c2
  108|          ex += e2
  109|      status = "HOST-DIED" if s.dead else "SURVIVED"
  110| -    s.close()
  111| -    return dict(status=status, badis=bad, covered=cov, nsteps=len(ex), executed=ex)
  112| +    end = s.close()
  113| +    return dict(status=status, badis=bad, covered=cov, nsteps=len(ex), executed=ex, **end)
  114|  
  115|  
  116|  def run_kill():
  117|      prog = build(kill=True)
  118|      s = Session()
  119|      if not s.wait(timeout=120):
  120| -        s.close()
  121| -        return dict(status="NO-PROMPT", saw=False)
  122| +        return dict(status="NO-PROMPT", saw=False, **s.close())
  123|      plant(s, prog)
  124|      step_and_check(s, prog, PROLOGUE_N + 3)
  125|      died = s.dead
  126|      if not died:
  127|          s.send("reg", timeout=10)
  128|          died = s.dead
  129| -    saw = "ENABLE SET" in s.buf
  130| -    s.close()
  131| -    return dict(status="HOST-DIED" if died else "SURVIVED", saw=saw)
  132| +    end = s.close()
  133| +    saw = "ENABLE CLEAR" in s.buf
  134| +    return dict(status="HOST-DIED" if died else "SURVIVED", saw=saw, **end)
  135|  
  136|  
  137|  def main():
  138| @@ -630,12 +644,17 @@ def main():
  139|          ok &= bool(good)
  140|          print("  %-4s %-46s %s" % ("ok" if good else "FAIL", tag, detail))
  141|  
  142| +    def survived(a):
  143| +        return a["status"] == "SURVIVED" and a.get("exit") == 0
  144| +
  145|      rD, rX, rT = D.get("regs", {}), X.get("regs", {}), T.get("regs", {})
  146| -    ranD = D["status"] == "SURVIVED" and D.get("out") is not None
  147| -    ranX = X["status"] == "SURVIVED" and X.get("out") is not None
  148| +    ranD = survived(D) and D.get("out") is not None
  149| +    ranX = survived(X) and X.get("out") is not None
  150|      row("R0 every arm produced data",
  151| -        ranD and ranX and T["status"] != "NO-PROMPT" and K["status"] != "NO-PROMPT",
  152| -        "D=%s X=%s T=%s K=%s" % (D["status"], X["status"], T["status"], K["status"]))
  153| +        ranD and ranX and survived(T) and survived(E) and K["status"] != "NO-PROMPT",
  154| +        "; ".join("%s=%s exit=%s signal=%s" %
  155| +                  (name, a["status"], a.get("exit"), a.get("signal"))
  156| +                  for name, a in (("D", D), ("X", X), ("T", T), ("E", E), ("K", K))))
  157|      row("C1 liveness: RAM through the same decode",
  158|          rD.get(5) == 0x11223344 and rX.get(5) == 0x11223344,
  159|          "D r5=0x%x  X r5=0x%x" % (rD.get(5, -1), rX.get(5, -1)))
  160| @@ -650,16 +669,18 @@ def main():
  161|          "wrote 0x12345678, read D=0x%08x X=0x%08x" % (rD.get(7, -1), rX.get(7, -1)))
  162|      drain_words = {CODE + o for o in range(0x70, 0xe8, 4)}
  163|      row("E  encodings: prologue AND drain body, as EXECUTED",
  164| -        not D.get("badis") and not X.get("badis") and not E["badis"]
  165| +        survived(E) and not D.get("badis") and not X.get("badis") and not E["badis"]
  166|          and not (drain_words - E["covered"]),
  167|          "%d mismatches; drain offsets not stepped: %s"
  168|          % (len(D.get("badis", [])) + len(X.get("badis", [])) + len(E["badis"]),
  169|             " ".join("0x%x" % a for a in sorted(drain_words - E["covered"])) or "none"))
  170|      row("K  failability: the kill instruction really kills",
  171| -        K["status"] == "HOST-DIED" and D["status"] == "SURVIVED",
  172| -        "K=%s (complaint seen: %s)" % (K["status"], K["saw"]))
  173| +        K["status"] == "HOST-DIED" and K["saw"] and K.get("exit") == 1
  174| +        and survived(D),
  175| +        "K=%s exit=%s signal=%s (complaint seen: %s)" %
  176| +        (K["status"], K.get("exit"), K.get("signal"), K["saw"]))
  177|      row("T  the MMU-ON control cannot see the device",
  178| -        rT.get(6) != VENDOR and rT.get(7) != LOADBACK,
  179| +        survived(T) and rT.get(6) != VENDOR and rT.get(7) != LOADBACK,
  180|          "T r6=0x%x r7=0x%x" % (rT.get(6, -1), rT.get(7, -1)))
  181|      row("L1 the guest ran during the accrual",
  182|          ranD and D["out"][1] not in (None, POISON) and D["out"][1] > 1000,
  183| diff --git a/regress/fbpending_witness.py b/regress/fbpending_witness.py
  184| index 6fdc1bc..2a920aa 100644
  185| --- a/regress/fbpending_witness.py
  186| +++ b/regress/fbpending_witness.py
  187| @@ -2,9 +2,10 @@
  188|  """`fbpending`: a RUNG-3 cold-debugger witness that the emulated footbridge clock
  189|  STOPS for 42.9 s in every 85.9 s, on an UNMODIFIED in-tree `-E cats`.
  190|  
  191| -THE DEFECT.  dev_footbridge.c:73 declares `int pending_timer_interrupts[4]`; the four
  192| -callbacks at :86-92 do `->pending_timer_interrupts[N] ++` with no bound; and
  193| -DEVICE_TICK(footbridge) at :259-277 delivers a tick ONLY under `if (... [i] > 0)`.
  194| +THE DEFECT (as it stood before its fix; the citations are to the pre-fix file and are kept
  195| +as history).  dev_footbridge.c declared `int pending_timer_interrupts[4]`; the four timer
  196| +callbacks did `->pending_timer_interrupts[N] ++` with no bound; and DEVICE_TICK(footbridge)
  197| +delivered a tick ONLY under `if (... [i] > 0)`.
  198|  Nothing decrements the counter except a guest write to TIMER_x_CLEAR, so a guest that
  199|  programs a fast timer and does not acknowledge drives the counter to INT_MAX, where `++`
  200|  is signed overflow (UB) and, in practice, wraps to INT_MIN.  For the next 2^31
  201| @@ -21,7 +22,7 @@ therefore delivered in full.  2^31 / 50e6 = 42.95 s to the wrap and 2^32 / 50e6
  202|  85.90 s to the return, giving the 42.9-in-85.9 duty cycle this probe plots.
  203|  
  204|  THE GUEST-VISIBLE DISCRIMINATOR, and why it needs no interrupt plumbing.  TIMER_1_VALUE
  205| -(dev_footbridge.c:557-562) is READ/WRITE: a read returns d->timer_value[0], a write
  206| +(dev_footbridge.c `case TIMER_1_VALUE`) is READ/WRITE: a read returns d->timer_value[0], a write
  207|  stores `idata & TIMER_MAX_VAL`.  DEVICE_TICK overwrites that same field with
  208|  `random() % footbridge_effective_cycles(load, control, 0)` -- and with load == 1 that
  209|  modulus is 1, so EVERY delivered tick writes exactly 0.  So the guest:
  210| @@ -31,8 +32,9 @@ modulus is 1, so EVERY delivered tick writes exactly 0.  So the guest:
  211|  
  212|  Each 0 is one delivered tick, counted by the guest into RAM.  Pre-wrap that count climbs
  213|  at the device-tick rate; post-wrap it FREEZES and the sentinel the guest wrote survives
  214| -indefinitely.  No interrupt controller, no IRQ enable (which would hit an unrelated
  215| -fatal()+exit(1) at dev_footbridge.c:486-499), no guest OS, no disk image.
  216| +indefinitely.  No interrupt controller, no IRQ enable, no guest OS, no disk image.
  217| +(This used to add "an IRQ enable read would hit an unrelated fatal()+exit(1)"; #539
  218| +removed that exit, and the enable registers play no part in this witness.)
  219|  
  220|  *** WHY A FROZEN COUNTER IS NOT MERELY "THE EMULATOR STOPPED", which is the whole
  221|      difficulty of a negative measurement.  Three quantities run CONCURRENTLY in the same
  222| @@ -71,9 +73,12 @@ ARMS
  223|       against a separate `unassemble` of words that might never run.
  224|    T  negative control.  MMU left on.  Must not return 0x1011 or 0x00345678.
  225|    K  failability control.  Arm A's prologue plus ONE instruction, a guest read of
  226| -     IRQ_ENABLE_SET (footbridge+0x188), which dev_footbridge.c:486-499 answers with
  227| -     fatal() then exit(1).  A probe in which nothing can die proves nothing by
  228| -     surviving; K must kill the host and A must not.
  229| +     IRQ_ENABLE_CLEAR (footbridge+0x18c, write-only per the DC21285), which
  230| +     dev_footbridge.c's `case IRQ_ENABLE_CLEAR` read branch answers with fatal() then
  231| +     exit(1).  A probe in which nothing can die proves nothing by surviving; K must
  232| +     kill the host (its complaint AND exit 1) and A must not (exit 0).  #539 moved this
  233| +     from +0x188, which is a documented read-only register and now answers reads; the
  234| +     bridge is retired by the round that declines +0x18c.
  235|  
  236|  CONTROLS ARE NOT OPTIONAL AND ABSENT DATA MUST FAIL.  Every RAM word is poisoned with
  237|  0xDEADBEEF before the run, every verdict row first requires the values it consults to be
  238| @@ -137,8 +142,8 @@ LASTID = DATA + 0x2c          # last VENDOR_ID read      <- device still dispatc
  239|  POISON = 0xDEADBEEF
  240|  
  241|  SENTINEL = 0x00AB0000         # survives `idata & TIMER_MAX_VAL` (0x00FFFFFF)
  242| -VENDOR   = 0x1011             # dev_footbridge.c:423
  243| -LOADBACK = 0x00345678         # 0x12345678 & TIMER_MAX_VAL, dev_footbridge.c:548
  244| +VENDOR   = 0x1011             # dev_footbridge.c `case VENDOR_ID` (DC21285_VENDOR_ID)
  245| +LOADBACK = 0x00345678         # 0x12345678 & TIMER_MAX_VAL, the TIMER_x_LOAD write arm
  246|  
  247|  EMU_HZ      = 50000000.0
  248|  PREDICT_OFF = 2147483648.0 / EMU_HZ      # 42.95 s: the wrap
  249| @@ -192,8 +197,8 @@ LOOP = [
  250|      (0x74, 0xEAFFFFF3, "b 0x8048",          "re-arm the sentinel"),
  251|  ]
  252|  LANDING = (0x78, NOP, NOPTXT, "landing pad -- planted, never reached")
  253| -KILL    = (0x48, 0xE5907188, "ldr r7,[r0,#392]",
  254| -           "arm K: read IRQ_ENABLE_SET -> fatal()+exit(1) at dev_footbridge.c:492-497")
  255| +KILL    = (0x48, 0xE590718C, "ldr r7,[r0,#396]",
  256| +           "arm K: read IRQ_ENABLE_CLEAR -> fatal()+exit(1) (#539: was +0x188)")
  257|  
  258|  SENT_A = (0xE3A088AB, "mov r8,#0xab0000")     # 0x00AB0000
  259|  SENT_E = (0xE3A08000, "mov r8,#0")            # arm E: the ONE immediate that differs
  260| @@ -339,20 +344,28 @@ class Session:
  261|                  got[k] = int(m.group(1), 16)
  262|          return got
  263|  
  264| -    def close(self):
  265| +    def close(self, patience=5.0):
  266|          try:
  267|              os.write(self.fd, b"quit\n")
  268| -            time.sleep(0.3)
  269|          except OSError:
  270|              pass
  271| +        # Drain through EOF; closing a live master can SIGHUP the child.
  272| +        deadline = time.monotonic() + patience
  273| +        while True:
  274| +            left = deadline - time.monotonic()
  275| +            if left <= 0 or not self.rd(min(0.1, left)):
  276| +                break
  277|          try:
  278|              os.close(self.fd)
  279|          except OSError:
  280|              pass
  281|          try:
  282| -            os.waitpid(self.pid, 0)
  283| -        except Exception:
  284| -            pass
  285| +            _, st = os.waitpid(self.pid, 0)
  286| +        except OSError:
  287| +            st = None
  288| +        code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
  289| +        sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
  290| +        return dict(exit=code, signal=sig)
  291|  
  292|  
  293|  def plant(s, prog):
  294| @@ -400,8 +413,8 @@ def run_witness(head, sentinel, slices, slice_s, label):
  295|      prog = head + prologue(sentinel[0], sentinel[1]) + LOOP + [LANDING]
  296|      s = Session()
  297|      if not s.wait(timeout=120):
  298| -        s.close()
  299| -        return dict(status="NO-PROMPT", label=label, samples=[], regs={}, badis=[], catchup=0)
  300| +        return dict(status="NO-PROMPT", label=label, samples=[], regs={}, badis=[],
  301| +                    catchup=0, **s.close())
  302|      plant(s, prog)
  303|      bad, _, _ = step_and_check(s, prog, PROLOGUE_N)
  304|      r = s.regs()
  305| @@ -424,17 +437,16 @@ def run_witness(head, sentinel, slices, slice_s, label):
  306|      else:
  307|          status = "SURVIVED"
  308|      catchup = s.buf.count(TIMERMSG)
  309| -    s.close()
  310| +    end = s.close()
  311|      return dict(status=status, label=label, regs=r, badis=bad,
  312| -                samples=samples, catchup=catchup)
  313| +                samples=samples, catchup=catchup, **end)
  314|  
  315|  
  316|  def run_kill():
  317|      prog = MMU_OFF + prologue(*SENT_A) + [KILL, (0x4c, NOP, NOPTXT, "")]
  318|      s = Session()
  319|      if not s.wait(timeout=120):
  320| -        s.close()
  321| -        return dict(status="NO-PROMPT", saw_fatal=False, badis=[], nsteps=0)
  322| +        return dict(status="NO-PROMPT", saw_fatal=False, badis=[], nsteps=0, **s.close())
  323|      plant(s, prog)
  324|      bad, _, ex = step_and_check(s, prog, PROLOGUE_N + 1)
  325|      died = s.dead
  326| @@ -442,10 +454,10 @@ def run_kill():
  327|          #  The exit may land between the write and our read; one more poke settles it.
  328|          s.send("reg", timeout=10)
  329|          died = s.dead
  330| -    seen = "ENABLE SET" in s.buf
  331| -    s.close()
  332| +    end = s.close()
  333| +    seen = "ENABLE CLEAR" in s.buf
  334|      return dict(status="HOST-DIED" if died else "SURVIVED", saw_fatal=seen,
  335| -                badis=bad, nsteps=len(ex))
  336| +                badis=bad, nsteps=len(ex), **end)
  337|  
  338|  
  339|  def run_encodings():
  340| @@ -454,17 +466,16 @@ def run_encodings():
  341|      prog = MMU_OFF + prologue(*SENT_E) + LOOP + [LANDING]
  342|      s = Session()
  343|      if not s.wait(timeout=120):
  344| -        s.close()
  345|          return dict(status="NO-PROMPT", regs={}, badis=[], covered=set(), want=set(),
  346| -                    nsteps=0, executed=[])
  347| +                    nsteps=0, executed=[], **s.close())
  348|      plant(s, prog)
  349|      bad, covered, ex = step_and_check(s, prog, PROLOGUE_N + 2 * len(LOOP))
  350|      r = s.regs()
  351|      want = {CODE + off for off, *_ in prog if off != LANDING[0]}
  352|      status = "HOST-DIED" if s.dead else "SURVIVED"
  353| -    s.close()
  354| +    end = s.close()
  355|      return dict(status=status, regs=r, badis=bad, covered=covered, want=want,
  356| -                nsteps=len(ex), executed=ex)
  357| +                nsteps=len(ex), executed=ex, **end)
  358|  
  359|  
  360|  def main():
  361| @@ -557,14 +568,19 @@ def main():
  362|          ok &= bool(good)
  363|          print("  %-4s %-47s %s" % ("ok" if good else "FAIL", tag, detail))
  364|  
  365| +    def survived(a):
  366| +        return a["status"] == "SURVIVED" and a.get("exit") == 0
  367| +
  368|      rA, rE, rT = A["regs"], E["regs"], T["regs"]
  369| -    ranA = A["status"] == "SURVIVED" and len(S) == SLICES
  370| -    ranE = E["status"] == "SURVIVED"
  371| -    ranT = T["status"] == "SURVIVED" and len(T["samples"]) == 1
  372| +    ranA = survived(A) and len(S) == SLICES
  373| +    ranE = survived(E)
  374| +    ranT = survived(T) and len(T["samples"]) == 1
  375|  
  376|      row("R0 every arm produced data", ranA and ranE and ranT and K["status"] != "NO-PROMPT",
  377| -        "A=%s(%d/%d samples) E=%s T=%s K=%s"
  378| -        % (A["status"], len(S), SLICES, E["status"], T["status"], K["status"]))
  379| +        "; ".join("%s=%s exit=%s signal=%s" %
  380| +                  (name, a["status"], a.get("exit"), a.get("signal"))
  381| +                  for name, a in (("A", A), ("E", E), ("T", T), ("K", K)))
  382| +        + "; A samples=%d/%d" % (len(S), SLICES))
  383|      row("C1 liveness: RAM through the same decode",
  384|          rA.get(5) == 0x11223344 and rE.get(5) == 0x11223344,
  385|          "A r5=0x%x  E r5=0x%x" % (rA.get(5, -1), rE.get(5, -1)))
  386| @@ -585,9 +601,10 @@ def main():
  387|          "%d mismatches, %d/%d offsets stepped"
  388|          % (len(E["badis"]), len(E["covered"]), len(E["want"])))
  389|      row("K  failability: the kill instruction really kills",
  390| -        K["status"] == "HOST-DIED" and A["status"] == "SURVIVED",
  391| -        "K=%s (device complaint seen: %s), A=%s"
  392| -        % (K["status"], K["saw_fatal"], A["status"]))
  393| +        K["status"] == "HOST-DIED" and K["saw_fatal"] and K.get("exit") == 1
  394| +        and survived(A),
  395| +        "K=%s exit=%s signal=%s (device complaint seen: %s), A=%s"
  396| +        % (K["status"], K.get("exit"), K.get("signal"), K["saw_fatal"], A["status"]))
  397|      row("T  the MMU-ON control cannot see the device",
  398|          ranT and rT.get(6) != VENDOR and rT.get(7) != LOADBACK,
  399|          "T r6=0x%x r7=0x%x" % (rT.get(6, -1), rT.get(7, -1)))
  400| @@ -646,7 +663,8 @@ def main():
  401|          print("  The emulated footbridge clock delivered NOTHING for %.1f s of continuous"
  402|                % frozen_span)
  403|          print("  free-running guest execution, while the guest kept running and the device")
  404| -        print("  kept answering reads.  That is dev_footbridge.c:86-92 against :265.")
  405| +        print("  kept answering reads.  That is the unbounded callback increment against")
  406| +        print("  DEVICE_TICK's `> 0` test -- the pre-fix dev_footbridge.c, see the header.")
  407|      good = ok and covered and symptom == "ABSENT"
  408|      print("FBPENDING_VERDICT=%s" % ("PASS" if good else "FAIL"))
  409|      print("PROBE_WALL=%.1fs" % (time.time() - t_probe))
  410| diff --git a/regress/footbridge_sites_probe.py b/regress/footbridge_sites_probe.py
  411| index 848d148..f802d02 100644
  412| --- a/regress/footbridge_sites_probe.py
  413| +++ b/regress/footbridge_sites_probe.py
  414| @@ -35,30 +35,74 @@ VALUES, NOT SURVIVAL (rounds 79/80, and m8820x_sites_probe.py's header says the
  415|  A row that only asks "did the host stay up" cannot tell a reachable device from an absent
  416|  one -- an unmapped read survives too, it just returns 0.  So the two device rows assert
  417|  values that ONLY dev_footbridge.c can produce:
  418| -  * A1 reads VENDOR_ID and requires 0x1011 (dev_footbridge.c:423, DC21285_VENDOR_ID).
  419| +  * A1 reads VENDOR_ID and requires 0x1011 (dev_footbridge.c `case VENDOR_ID`, the
  420| +    DC21285_VENDOR_ID assignment).
  421|      Nonzero and specific: the hand-assembled-encoding trap this project has been bitten by
  422|      yields 0 from a wrong register field, and 0 is the one answer this row rejects.
  423|    * A2 writes 0x12345678 to TIMER_1_LOAD and reads back 0x00345678.  THE VANISHING TOP BYTE
  424| -    IS THE HANDLER'S OWN SIGNATURE: dev_footbridge.c:548 stores `idata & TIMER_MAX_VAL`
  425| +    IS THE HANDLER'S OWN SIGNATURE: the TIMER_x_LOAD write arm stores `idata & TIMER_MAX_VAL`
  426|      (0x00FFFFFF, dc21285reg.h:371).  RAM, or any decode that merely absorbed the store,
  427|      would return 0x12345678 unchanged.  This row therefore distinguishes "the device
  428|      handled it" from "the write landed somewhere", which A1 alone cannot.
  429|  
  430|  THE KILL PAIR, which is this probe's own failability control.  Arms L and K differ by
  431| -EXACTLY ONE INSTRUCTION.  Arm K adds a guest read of IRQ_ENABLE_SET (base+0x188), which
  432| -dev_footbridge.c:495-497 answers with fatal() then exit(1) -- an UNFIXED site, used here
  433| -rather than repaired, because a probe that reports SURVIVED for every row is vacuous unless
  434| -something in it can still die.  Arm L must live; arm K must exit 1 and say so.  If both
  435| -survived, the guest instructions are not reaching the device at all and every SURVIVED
  436| -verdict above is worthless; if both died, the probe is killing the host for its own reasons.
  437| -The one-instruction delta is the entire argument.
  438| +EXACTLY ONE INSTRUCTION.  Arm K adds a guest read of IRQ_ENABLE_CLEAR (base+0x18c), which
  439| +dev_footbridge.c's `case IRQ_ENABLE_CLEAR` read branch answers with fatal() then exit(1) --
  440| +an UNFIXED site, used here rather than repaired, because a probe that reports SURVIVED for
  441| +every row is vacuous unless something in it can still die.  Arm L must live; arm K must
  442| +exit 1 and say so.  If both survived, the guest instructions are not reaching the device at
  443| +all and every SURVIVED verdict above is worthless; if both died, the probe is killing the
  444| +host for its own reasons.  The one-instruction delta is the entire argument.
  445| +  #539 moved this arm from +0x188 to +0x18c.  +0x188 (IRQEnable) is a DOCUMENTED READ-ONLY
  446| +  register (DC21285 Table 7-10; 7.3.31: "can only be changed by writing to the EnableSet and
  447| +  EnableClear registers", reset 0) and now answers reads -- rows E0-E6 below.  +0x18c is
  448| +  write-only per 7.3.32, so a kill there is a decline-class site still dying, and the same
  449| +  deletion spilled onto the CLEAR read branch makes K survive with no diagnostic: K1 reds.
  450| +  The bridge is TEMPORARY: the round that declines +0x18c retires it and builds the harness
  451| +  legs (startup rejection + mid-session quit, status reaped) in the same commit.
  452| +
  453| +ARM E -- #539's ACCEPT rows, in a FOURTH arm so that arms L/T/K are byte-identical to what
  454| +they were.  E carries its own C1/A1 (E0 = 0 is also what an ABSENT device returns, so the
  455| +E rows are meaningless unless this arm demonstrably reached the device) and then:
  456| +  E0 read IRQEnable before any write            -> 0            (reset value, 7.3.31)
  457| +  E1 write P=0x2002 to Set, read               -> P            (readable; catches a bit
  458| +                                                                  swap, a constant, a wrong
  459| +                                                                  field, a masked value)
  460| +  E2 write Q=0x60000000 to Set, read           -> P|Q          (pins |=; bit 30 set so a
  461| +                                                                  diagnostic kept for the top
  462| +                                                                  bits fires here)
  463| +  E3 ldrb  +0x188                              -> 0x02         (low byte: len 1 reaches the
  464| +  E6 ldrh  +0x188                              -> 0x2002        same case; the CSR drives
  465| +                                                                  D[31:0] and the SA-110 takes
  466| +                                                                  the lane, DC21285 3.2.x)
  467| +  E5 write P to Clear, read Set                -> Q            (Clear works; = the E2 value
  468| +                                                                  with P removed)
  469| +  E4 no footbridge diagnostic anywhere in arm E (a fatal() kept without its exit)
  470| +Execution order is E0,E1,E2,E3,E6,E5: E6 wants 0x2002, which is true only while P is set.
  471| +P and Q are loaded from RAM (DATA+8, DATA+12), like 0x12345678: neither is a rotated
  472| +immediate.  Values land in r7,r1,r2,r9,fp,ip; r1/r2 are A2's registers in arm L and are
  473| +free here because arm E does not score A2.
  474| +
  475| +CONTRACT (what this detector is designed to catch, and what it is not).  On the SET read
  476| +branch: the exit reinstated (E0 dies), reinstated only when irq_enable == 0 (E0), a wrong
  477| +field/constant/mask/bit-swap (E1, E2), a width guard (E3, E6), a kept diagnostic (E4), a
  478| +diagnostic kept for bits 30/31 (E4; E2 if it exits).  On the CLEAR arms: a broken `&= ~`
  479| +(E5), the exit removed from the CLEAR read too (K1).  NOT COVERED: (a) no row observes the
  480| +CPU IRQ line -- an edit to the write arm's assert condition (`irq_status | irq_enable`) is
  481| +invisible to every row here, because cpu_dyntrans.c suppresses interrupt delivery under
  482| +`step` and CPSR I/F stay set; it needs a free-running arm with a positive delivery control,
  483| +filed with IRQSoft; (b) +0x189..+0x18b: real hardware selects the same CSR by A[10:2] and
  484| +returns lanes 1-3, the model routes them to `default:` and returns 0 -- a device-wide decode
  485| +deviation, filed, not rowed; (c) irq_status and fiq_enable are 0 throughout, so a mutant
  486| +returning either at +0x188 is caught by E1/E2 only through the value, not distinguished
  487| +from a constant 0.
  488|  
  489|  EVERY PLANTED WORD IS CHECKED AGAINST THE DISASSEMBLY THE EMULATOR PRINTS AS IT STEPS IT --
  490|  not against a separate `unassemble`, because the step line is the instruction that actually
  491|  executed.  This project has a recorded incident where a wrong register field made a gate row
  492|  measure the wrong thing for months.
  493|  
  494| -COST, measured: see PROBE_WALL below -- 3 cold-debugger launches, no boot.  A booting-rig row
  495| +COST, measured: see PROBE_WALL below -- 4 cold-debugger launches, no boot.  A booting-rig row
  496|  was deliberately NOT written: no rig in this tree boots a footbridge machine at all, which is
  497|  the gap this probe closes, and adding one would put a load-sensitive wall-clock oracle into a
  498|  battery already carrying ~37.
  499| @@ -100,8 +144,25 @@ BODY = [
  500|      (0x28, 0xE5901300, "ldr r1,[r0,#768]",      "A2: read it back"),
  501|  ]
  502|  KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site")
  503| -KILL_LOAD = (0x2c, 0xE5907188, "ldr r7,[r0,#392]", "arm K: read IRQ_ENABLE_SET (0x188)")
  504| +KILL_LOAD = (0x2c, 0xE590718C, "ldr r7,[r0,#396]", "arm K: read IRQ_ENABLE_CLEAR (0x18c)")
  505|  TAIL = [(0x30, NOP, NOPTXT, "landing pad -- planted, never stepped")]
  506| +P, Q = 0x00002002, 0x60000000           # #539 arm E values; loaded from DATA+8 / DATA+12
  507| +ENABLE = [                              # #539: the ACCEPT rows, order E0,E1,E2,E3,E6,E5
  508| +    (0x2c, 0xE5907188, "ldr r7,[r0,#392]",   "E0: read IRQ_ENABLE_SET before any write"),
  509| +    (0x30, 0xE5948008, "ldr r8,[r4,#8]",     "r8 = P"),
  510| +    (0x34, 0xE5808188, "str r8,[r0,#392]",   "IRQEnableSet <- P"),
  511| +    (0x38, 0xE5901188, "ldr r1,[r0,#392]",   "E1: read back -> P"),
  512| +    (0x3c, 0xE594900C, "ldr r9,[r4,#12]",    "r9 = Q"),
  513| +    (0x40, 0xE5809188, "str r9,[r0,#392]",   "IRQEnableSet <- Q"),
  514| +    (0x44, 0xE5902188, "ldr r2,[r0,#392]",   "E2: read back -> P|Q (pins |=)"),
  515| +    (0x48, 0xE5D09188, "ldrb r9,[r0,#392]",  "E3: BYTE read -> 0x02"),
  516| +    (0x4c, 0xE280AD06, "add sl,r0,#0x180",   "sl = base+0x180 (ldrh offsets cap at 255)"),
  517| +    (0x50, 0xE1DAB0B8, "ldrh fp,[sl,#8]",    "E6: HALFWORD read -> 0x2002"),
  518| +    (0x54, 0xE580818C, "str r8,[r0,#396]",   "IRQEnableClear <- P"),
  519| +    (0x58, 0xE590C188, "ldr ip,[r0,#392]",   "E5: read back -> Q"),
  520| +    (0x5c, NOP, NOPTXT, "landing pad -- planted, never stepped"),
  521| +]
  522| +REGNAME = {10: "sl", 11: "fp", 12: "ip"}   # the emulator's spellings (cpu_arm.h ARM_REG_NAMES)
  523|  
  524|  
  525|  def run_arm(label, prog):
  526| @@ -168,6 +229,8 @@ def run_arm(label, prog):
  527|      else:
  528|          send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
  529|          send("put w 0x%08x, 0x%08x" % (DATA + 4, 0x12345678))
  530| +        send("put w 0x%08x, 0x%08x" % (DATA + 8, P))
  531| +        send("put w 0x%08x, 0x%08x" % (DATA + 12, Q))
  532|          for off, word, _t, _c in prog:
  533|              send("put w 0x%08x, 0x%08x" % (CODE + off, word))
  534|          send("pc=0x%08x" % CODE)
  535| @@ -188,8 +251,9 @@ def run_arm(label, prog):
  536|          if status == "SURVIVED":
  537|              mark = len(buf)
  538|              if send("reg", timeout=30) and not dead[0]:
  539| -                for n in (0, 1, 2, 3, 5, 6, 7):
  540| -                    mm = re.search(r"\br%d\s*=\s*0x([0-9a-fA-F]+)" % n, buf[mark:])
  541| +                for n in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12):
  542| +                    mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)"
  543| +                                   % REGNAME.get(n, "r%d" % n), buf[mark:])
  544|                      if mm:
  545|                          regs[n] = int(mm.group(1), 16)
  546|              else:
  547| @@ -234,7 +298,8 @@ t0 = time.time()
  548|  
  549|  L = run_arm("L  live      (MMU off)",      MMU_OFF + BODY + [KILL_NOP] + TAIL)
  550|  T = run_arm("T  trap ctrl (MMU LEFT ON)",  MMU_NOP + BODY + [KILL_NOP] + TAIL)
  551| -K = run_arm("K  kill      (MMU off,+188)", MMU_OFF + BODY + [KILL_LOAD] + TAIL)
  552| +K = run_arm("K  kill      (MMU off,+18c)", MMU_OFF + BODY + [KILL_LOAD] + TAIL)
  553| +E = run_arm("E  enable    (MMU off,#539)", MMU_OFF + BODY + ENABLE)
  554|  print()
  555|  
  556|  results = []
  557| @@ -288,18 +353,36 @@ results.append(row("A2b", "the value the guest actually stored",
  558|  
  559|  #  ---- the kill pair: this probe's own failability control. ----
  560|  l_ok = L["status"] == "SURVIVED" and L["exit"] == 0 and not L["fatals"]
  561| -k_ok = any("ENABLE SET" in f for f in K["fatals"]) and K["exit"] == 1
  562| +k_ok = any("ENABLE CLEAR" in f for f in K["fatals"]) and K["exit"] == 1
  563|  print("%-4s %-40s %-30s %s"
  564|        % ("I1", "isolation arm SURVIVES untouched",
  565|           "status=%s exit=%s" % (L["status"], L["exit"]), "ok" if l_ok else "FAIL"))
  566|  print("%-4s %-40s %-30s %s"
  567| -      % ("K1", "kill arm dies at 0x188, exit 1",
  568| +      % ("K1", "kill arm dies at 0x18c, exit 1",
  569|           "exit=%s" % K["exit"], "ok" if k_ok else "FAIL"))
  570|  print("      kill arm said: %s" % ((K["fatals"] or ["(nothing)"])[-1]))
  571|  results.append(l_ok)
  572|  results.append(k_ok)
  573|  
  574| -nbad = sum(len(a["badis"]) for a in (L, T, K))
  575| +#  ---- #539: IRQEnable is readable.  Arm E first proves it reached the device (its own C1
  576| +#  and A1: E0 == 0 is ALSO what an absent device returns), then the value rows. ----
  577| +ec1 = row("EC1", "arm E liveness: plain RAM readback", E["regs"].get(5), 0x11223344)
  578| +ea1 = row("EA1", "arm E reaches the device: VENDOR_ID", E["regs"].get(6), 0x1011)
  579| +results += [ec1, ea1]
  580| +results.append(row("E0", "IRQEnable reads 0 before any write", E["regs"].get(7), 0))
  581| +results.append(row("E1", "Set <- P, read back", E["regs"].get(1), P))
  582| +results.append(row("E2", "Set <- Q, read back (|=)", E["regs"].get(2), P | Q))
  583| +results.append(row("E3", "byte read: low byte", E["regs"].get(9), P & 0xff))
  584| +results.append(row("E6", "halfword read: low two bytes", E["regs"].get(11), P & 0xffff))
  585| +results.append(row("E5", "Clear <- P, read Set back", E["regs"].get(12), Q))
  586| +e_ok = E["status"] == "SURVIVED" and E["exit"] == 0 and not E["fatals"]
  587| +print("%-4s %-40s %-30s %s"
  588| +      % ("E4", "arm E: no footbridge diagnostic, exit 0",
  589| +         "status=%s exit=%s fatals=%d" % (E["status"], E["exit"], len(E["fatals"])),
  590| +         "ok" if e_ok else "FAIL"))
  591| +results.append(e_ok)
  592| +
  593| +nbad = sum(len(a["badis"]) for a in (L, T, K, E))
  594|  print("%-4s %-40s %-30s %s"
  595|        % ("D1", "every planted word disassembled as meant",
  596|           "%d mismatches" % nbad, "ok" if nbad == 0 else "FAIL"))
  597| @@ -308,9 +391,9 @@ results.append(nbad == 0)
  598|  #  Named, not indexed.  The first version wrote `results[0] and results[1] ...`, which silently
  599|  #  re-points at different rows the moment a row is inserted above -- the same class as pinning a
  600|  #  row by an id that names a family.
  601| -ctrl_ok = c1 and c2 and c3 and c4
  602| +ctrl_ok = c1 and c2 and c3 and c4 and ec1 and ea1
  603|  print()
  604|  print("ROWS=%d of %d" % (sum(1 for r in results if r), len(results)))
  605|  print("FOOTBRIDGE_SITES_CONTROL=%s" % ("OK" if ctrl_ok else "BAD"))
  606|  print("FOOTBRIDGE_SITES_%s" % ("PASS" if all(results) else "FAIL"))
  607| -print("PROBE_WALL=%.1fs for 3 cold-debugger arms" % (time.time() - t0))
  608| +print("PROBE_WALL=%.1fs for 4 cold-debugger arms" % (time.time() - t0))
  609| diff --git a/src/devices/dev_footbridge.c b/src/devices/dev_footbridge.c
  610| index 9619c86..d01a827 100644
  611| --- a/src/devices/dev_footbridge.c
  612| +++ b/src/devices/dev_footbridge.c
  613| @@ -583,10 +583,12 @@ DEVICE_ACCESS(footbridge)
  614|  			else
  615|  				INTERRUPT_DEASSERT(d->irq);
  616|  		} else {
  617| +			/*  #539: a read of 188h is documented -- IRQEnable is
  618| +			    "read-only ... can only be changed by writing to
  619| +			    the EnableSet and EnableClear registers", reset 0
  620| +			    (DC21285 Table 7-10, 7.3.31).  The value below was
  621| +			    always right; the exit(1) that followed it is gone.  */
  622|  			odata = d->irq_enable;
  623| -			fatal("[ WARNING: footbridge read from "
  624| -			    "ENABLE SET? ]\n");
  625| -			exit(1);
  626|  		}
  627|  		break;
  628|  

    1| diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
    2| index d586c84..db10dc2 100644
    3| --- a/regress/gate_arm.sh
    4| +++ b/regress/gate_arm.sh
    5| @@ -1071,7 +1071,7 @@ done
    6|  #  reads CP15 c1 back and requires bit 0 clear.  Negative-controlled in both directions.
    7|  FBLOG=$LOGDIR/footbridge_sites.log
    8|  python3 footbridge_sites_probe.py "$PMAX" "$STUB" > "$FBLOG" 2>&1 || true
    9| -grep -E "^(  arm |C[0-9]|A[0-9]|I1|K1|D1)" "$FBLOG" | sed 's/^/       /'
   10| +grep -E "^(  arm |C[0-9]|A[0-9]|I1|K1|D1|E[A-Z]?[0-9])" "$FBLOG" | sed 's/^/       /'
   11|  
   12|  if ! grep -q "FOOTBRIDGE_SITES_" "$FBLOG"; then
   13|      note "footbridge probe produced no verdict; last lines follow"
   14| @@ -1084,19 +1084,34 @@ else
   15|            "$(grep -c 'FOOTBRIDGE_SITES_CONTROL=OK' "$FBLOG")" "1"
   16|      check "footbridge: every row green" \
   17|            "$(grep -c 'FOOTBRIDGE_SITES_PASS' "$FBLOG")" "1"
   18| -    #  VALUES, NOT SURVIVAL.  0x1011 is DC21285_VENDOR_ID (dev_footbridge.c:423) and can only
   19| +    #  VALUES, NOT SURVIVAL.  0x1011 is DC21285_VENDOR_ID (dev_footbridge.c `case VENDOR_ID`)
   20| +    #  and is a MODEL value: real hardware packs DeviceID:VendorID into a word read at +0x0,
   21| +    #  so the round that fixes packed config reads changes this pin in the same commit.  It can only
   22|      #  have come back through this device; an unmapped read survives too, it just returns 0.
   23|      check "footbridge: VENDOR_ID 0x1011 through a real guest ldr" \
   24|            "$(grep -cE '^A1 .*got=0x00001011 .*ok$' "$FBLOG")" "1"
   25| -    #  The vanishing top byte IS the handler's signature: :548 stores idata & TIMER_MAX_VAL.
   26| +    #  The vanishing top byte IS the handler's signature: the TIMER_x_LOAD write arm stores
   27| +    #  idata & TIMER_MAX_VAL.
   28|      #  RAM, or any decode that merely absorbed the store, returns 0x12345678 unchanged.
   29|      check "footbridge: TIMER_1_LOAD masked to 24 bits by the handler" \
   30|            "$(grep -cE '^A2 .*got=0x00345678 .*ok$' "$FBLOG")" "1"
   31|      #  THE PROBE'S OWN FAILABILITY CONTROL.  Arms L and K differ by ONE instruction; K reads
   32| -    #  IRQ_ENABLE_SET, an UNFIXED fatal()+exit(1) at :495-497.  Without it, "SURVIVED" on every
   33| -    #  row is satisfied by a probe whose guest code never reached the device at all.
   34| +    #  IRQ_ENABLE_CLEAR (+0x18c, write-only per the DC21285), an UNFIXED fatal()+exit(1) in its
   35| +    #  `case IRQ_ENABLE_CLEAR` read branch.  Without it, "SURVIVED" on every row is satisfied
   36| +    #  by a probe whose guest code never reached the device at all.  #539 moved it here from
   37| +    #  +0x188 (IRQEnable, documented read-only, now readable -- the E rows below); the round
   38| +    #  that declines +0x18c retires this bridge and builds the harness legs in its place.
   39|      check "footbridge: the one-instruction kill arm still dies" \
   40|            "$(grep -cE '^K1 .*ok$' "$FBLOG")" "1"
   41| +    #  #539: IRQEnable (+0x188) is readable -- reset 0, Set ORs, Clear clears, byte and
   42| +    #  halfword reads return the low lanes -- and arm E raises no footbridge diagnostic.
   43| +    #  Seven value/text rows, pinned by count AND by the two that carry the datasheet claims.
   44| +    check "footbridge: IRQEnable ACCEPT rows E0-E6 all green" \
   45| +          "$(grep -cE '^E[0-6] .*ok$' "$FBLOG")" "7"
   46| +    check "footbridge: IRQEnable reads 0 at reset (E0)" \
   47| +          "$(grep -cE '^E0 .*got=0x00000000 .*ok$' "$FBLOG")" "1"
   48| +    check "footbridge: Set ORs and Clear clears (E2 = P|Q)" \
   49| +          "$(grep -cE '^E2 .*got=0x60002002 .*ok$' "$FBLOG")" "1"
   50|      #  The defence against the hand-assembled-encoding trap: every planted word is compared
   51|      #  against the disassembly the emulator printed AS IT STEPPED IT.
   52|      check "footbridge: no planted word failed its disassembly check" \

## 5. THE FULL ENCLOSING FUNCTION AFTER THE EDIT (every exit path and the common tail)
  498| DEVICE_ACCESS(footbridge)
  499| {
  500| 	struct footbridge_data *d = (struct footbridge_data *) extra;
  501| 	uint64_t idata = 0, odata = 0;
  502| 	int timer_nr = 0;
  503| 
  504| 	if (writeflag == MEM_WRITE)
  505| 		idata = memory_readmax64(cpu, data, len);
  506| 
  507| 	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
  508| 		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
  509| 		relative_addr &= ~0x060;
  510| 	}
  511| 
  512| 	switch (relative_addr) {
  513| 
  514| 	case VENDOR_ID:
  515| 		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
  516| 		break;
  517| 
  518| 	case DEVICE_ID:
  519| 		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
  520| 		break;
  521| 
  522| 	case 0x04:
  523| 	case 0x0c:
  524| 	case 0x10:
  525| 	case 0x14:
  526| 	case 0x18:
  527| 		/*  TODO. Written to by Linux.  */
  528| 		break;
  529| 
  530| 	case REVISION:
  531| 		odata = 3;  /*  footbridge revision number  */
  532| 		break;
  533| 
  534| 	case PCI_ADDRESS_EXTENSION:
  535| 		/*  TODO: Written to by Linux.  */
  536| 		if (writeflag == MEM_WRITE && idata != 0)
  537| 			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
  538| 			    "EXTENSION: 0x%llx ]\n", (long long)idata);
  539| 		break;
  540| 
  541| 	case SA_CONTROL:
  542| 		/*  Read by Linux:  */
  543| 		odata = PCI_CENTRAL_FUNCTION;
  544| 		break;
  545| 
  546| 	case UART_DATA:
  547| 		if (writeflag == MEM_WRITE)
  548| 			console_putchar(d->console_handle, idata);
  549| 		break;
  550| 
  551| 	case UART_RX_STAT:
  552| 		/*  TODO  */
  553| 		odata = 0;
  554| 		break;
  555| 
  556| 	case UART_FLAGS:
  557| 		odata = UART_TX_EMPTY;
  558| 		break;
  559| 
  560| 	case IRQ_STATUS:
  561| 		if (writeflag == MEM_READ)
  562| 			odata = d->irq_status & d->irq_enable;
  563| 		else {
  564| 			fatal("[ WARNING: footbridge write to irq status? ]\n");
  565| 			exit(1);
  566| 		}
  567| 		break;
  568| 
  569| 	case IRQ_RAW_STATUS:
  570| 		if (writeflag == MEM_READ)
  571| 			odata = d->irq_status;
  572| 		else {
  573| 			fatal("[ footbridge write to irq_raw_status ]\n");
  574| 			exit(1);
  575| 		}
  576| 		break;
  577| 
  578| 	case IRQ_ENABLE_SET:
  579| 		if (writeflag == MEM_WRITE) {
  580| 			d->irq_enable |= idata;
  581| 			if (d->irq_status & d->irq_enable)
  582| 				INTERRUPT_ASSERT(d->irq);
  583| 			else
  584| 				INTERRUPT_DEASSERT(d->irq);
  585| 		} else {
  586| 			/*  #539: a read of 188h is documented -- IRQEnable is
  587| 			    "read-only ... can only be changed by writing to
  588| 			    the EnableSet and EnableClear registers", reset 0
  589| 			    (DC21285 Table 7-10, 7.3.31).  The value below was
  590| 			    always right; the exit(1) that followed it is gone.  */
  591| 			odata = d->irq_enable;
  592| 		}
  593| 		break;
  594| 
  595| 	case IRQ_ENABLE_CLEAR:
  596| 		if (writeflag == MEM_WRITE) {
  597| 			d->irq_enable &= ~idata;
  598| 			if (d->irq_status & d->irq_enable)
  599| 				INTERRUPT_ASSERT(d->irq);
  600| 			else
  601| 				INTERRUPT_DEASSERT(d->irq);
  602| 		} else {
  603| 			odata = d->irq_enable;
  604| 			fatal("[ WARNING: footbridge read from "
  605| 			    "ENABLE CLEAR? ]\n");
  606| 			exit(1);
  607| 		}
  608| 		break;
  609| 
  610| 	case FIQ_STATUS:
  611| 		if (writeflag == MEM_READ)
  612| 			odata = d->fiq_status & d->fiq_enable;
  613| 		else {
  614| 			fatal("[ WARNING: footbridge write to fiq status? ]\n");
  615| 			exit(1);
  616| 		}
  617| 		break;
  618| 
  619| 	case FIQ_RAW_STATUS:
  620| 		if (writeflag == MEM_READ)
  621| 			odata = d->fiq_status;
  622| 		else {
  623| 			fatal("[ footbridge write to fiq_raw_status ]\n");
  624| 			exit(1);
  625| 		}
  626| 		break;
  627| 
  628| 	case FIQ_ENABLE_SET:
  629| 		if (writeflag == MEM_WRITE)
  630| 			d->fiq_enable |= idata;
  631| 		break;
  632| 
  633| 	case FIQ_ENABLE_CLEAR:
  634| 		if (writeflag == MEM_WRITE)
  635| 			d->fiq_enable &= ~idata;
  636| 		break;
  637| 
  638| 	case TIMER_1_LOAD:
  639| 		if (writeflag == MEM_READ)
  640| 			odata = d->timer_load[timer_nr];
  641| 		else {
  642| 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  643| 			reload_timer_value(cpu, d, timer_nr);
  644| 			/*  debug("[ footbridge: timer %i (1-based), "
  645| 			    "value %i ]\n", timer_nr + 1,
  646| 			    (int)d->timer_value[timer_nr]);  */
  647| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  648| 		}
  649| 		break;
  650| 
  651| 	case TIMER_1_VALUE:
  652| 		if (writeflag == MEM_READ)
  653| 			odata = d->timer_value[timer_nr];
  654| 		else
  655| 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  656| 		break;
  657| 
  658| 	case TIMER_1_CONTROL:
  659| 		if (writeflag == MEM_READ)
  660| 			odata = d->timer_control[timer_nr];
  661| 		else {
  662| 			d->timer_control[timer_nr] = idata;
  663| 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  664| 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  665| 			    and it used to reach fatal()+exit(1) right here, so a
  666| 			    guest selecting the external clock source KILLED THE
  667| 			    HOST.  Arguably likelier than the zero load, since it
  668| 			    is a documented mode rather than a malformed value.
  669| 			    The rate an external clock would actually give is
  670| 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  671| 			    now gives the encoding a defined, survivable meaning
  672| 			    (the unprescaled period), and the real semantics are
  673| 			    filed for a round that has a datasheet.  */
  674| 			if (idata & TIMER_ENABLE) {
  675| 				reload_timer_value(cpu, d, timer_nr);
  676| 			} else {
  677| 				d->pending_timer_interrupts[timer_nr] = 0;
  678| 			}
  679| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  680| 		}
  681| 		break;
  682| 
  683| 	case TIMER_1_CLEAR:
  684| 		/*  #474: a READ must not perform the clear.  This case carried no
  685| 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  686| 		    does -- so a guest READ reloaded the counter, decremented the
  687| 		    pending count and DEASSERTED the interrupt.  A guest that merely
  688| 		    read the register silently acknowledged a pending timer interrupt;
  689| 		    the guest-visible consequence is a LOST interrupt, not a bad value.
  690| 
  691| 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
  692| 		    0x34C/0x36C onto this single case.
  693| 
  694| 		    GUARD THE BODY, KEEP THE break.  An early return here would skip
  695| 		    the function's common tail, which writes odata back on a read, and
  696| 		    would hand a guest an untouched buffer -- a defect this code does
  697| 		    not currently have.  */
  698| 		if (writeflag == MEM_WRITE) {
  699| 			if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
  700| 				reload_timer_value(cpu, d, timer_nr);
  701| 			}
  702| 
  703| 			if (d->pending_timer_interrupts[timer_nr] > 0) {
  704| 				d->pending_timer_interrupts[timer_nr] --;
  705| 			}
  706| 
  707| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  708| 		}
  709| 		break;
  710| 
  711| 	case SDRAM_BA_MASK:
  712| 		if (writeflag == MEM_READ) {
  713| 			fatal("[ footbridge read from sdram_ba_mask ]\n");
  714| 			exit(1);
  715| 		} else {
  716| 			switch (idata) {
  717| 			case SDRAM_MASK_256KB:
  718| 			case SDRAM_MASK_512KB:
  719| 			case SDRAM_MASK_1MB:
  720| 			case SDRAM_MASK_2MB:
  721| 			case SDRAM_MASK_4MB:
  722| 			case SDRAM_MASK_8MB:
  723| 			case SDRAM_MASK_16MB:
  724| 			case SDRAM_MASK_32MB:
  725| 			case SDRAM_MASK_64MB:
  726| 			case SDRAM_MASK_128MB:
  727| 			case SDRAM_MASK_256MB:
  728| 				break;
  729| 			default:
  730| 				fatal("[ footbridge write to sdram_ba_mask "
  731| 				    "%#llx ]\n", (long long)idata);
  732| 				break;
  733| 			}
  734| 		}
  735| 		break;
  736| 	case SDRAM_BA_OFFSET:
  737| 		if (writeflag == MEM_READ) {
  738| 			fatal("[ footbridge read from sdram_ba_offset ]\n");
  739| 			exit(1);
  740| 		} else {
  741| 			if (idata != 0)
  742| 				fatal("[ footbridge write to sdram_ba_offset "
  743| 				    "%#llx ]\n", (long long)idata);
  744| 		}
  745| 		break;
  746| 
  747| 	default:if (writeflag == MEM_READ) {
  748| 			fatal("[ footbridge: read from 0x%x ]\n",
  749| 			    (int)relative_addr);
  750| 		} else {
  751| 			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  752| 			    (int)relative_addr, (long long)idata);
  753| 		}
  754| 	}
  755| 
  756| 	if (writeflag == MEM_READ)
  757| 		memory_writemax64(cpu, data, len, odata);
  758| 
  759| 	return 1;
  760| }

## 6. QUESTIONS
**Q1 -- premise audit, as questions.**
 (a) Is the fix EXACTLY member 4 -- value kept, nothing added, no latch, no message -- and is the comment true
     (quote the datasheet lines above against it)?
 (b) Is `+0x18c` a sound bridge: does `ldr r7,[r0,#396]` (`0xE590718C`) reach `case IRQ_ENABLE_CLEAR`'s read branch
     unmodified (the timer fold is gated to [0x300,0x36C]), and does the K row in each of the THREE probes now
     require the text AND exit 1?
 (c) The new `close()` in drain/witness: it drains via `rd()` until EOF or 5 s, closes the master, then BLOCKS in
     `waitpid` -- is there a state in which the child survives the master close and the probe hangs?  Does
     `survived()` (SURVIVED and exit == 0) change any EXISTING row's verdict on a healthy run?  The witness probe's `run_witness` return dict gained `exit=` -- is every
     consumer of that dict unaffected?
 (d) Arm E: do the seven rows read the registers the words actually write (r7,r1,r2,r9,fp,ip), does anything in
     BODY or the E sequence clobber a register before its dump, and are EC1/EA1 the right controls?
 (e) `gate_arm.sh`: are the three new checks' regexes exact for the probe's output format (`%-4s %-40s got=%-12s
     want=%-12s ok`), and does the `E[A-Z]?[0-9]` excerpt grep match EC1/EA1/E0..E6 and nothing else?
 (f) Citations: every replaced `dev_footbridge.c:NNN` -- is the construct name unique in the file (grep count)?
 (g) `fbpending_drain_probe.py` is CRLF on disk and was written back CRLF -- confirm no line-ending change in the
     diff (the diff shows only content hunks).

**Q2 -- candidate weakenings, against the FIXED code + the shipped rows (which row reds first; which escape?).**
 The twelve in the table (section 3) plus:
 (m) `odata = d->irq_enable ^ 0x2000` (a bit flip inside P)          (n) `odata = ~d->irq_enable`
 (o) the E arm's P/Q RAM words never planted (probe defect: `put w` lines lost) -- which row reds?
 (p) K arm word left at +0x188 in ONE of the three probes (a partial move)
 (q) `close()` reaps but the K row ignores `exit` (the old predicate) -- which row is then vacuous?
 (r) `if (len == 4) odata = d->irq_enable;` (sub-word reads return 0, no death)
 Say for each: caught by (row), escapes, or CANNOT SETTLE from the packet.

**Q3 -- floor and contract.**  (a) Does the table satisfy vacuity floor (a) pre-fix red, (b) verbatim
 reinstatement killed, (c) identity rows, (d) DEPENDS-ON closure -- enumerate the (d) cells from the diff's own
 dominating predicates -- and (e) the contract states what is and is not covered?  (f) The anchor rule: if every
 footbridge offset shifted one word, which row reds?  (g) Is (j)'s disclosure honest, or is there a step-visible
 channel we missed?

**Q4 -- what did the round still not do?**  Records (CHANGELOG block, OUTSTANDING_BUGS, ledger, the pass-1 seat
 record incl. two codex refusals as SEAT FAILURES), propagation to build/, build-asan/, /tmp/gxsec-build
 (two-part clearance after rebuild), gate_arm alone.  Name anything else.

End with the seat record line: model, what you READ, what you RAN (nothing), and -- for file-reading seats --
the md5 of the frozen diff you compared against (1ffb5507 / e8a7c3f4).


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
