# proberowsubset -- can a probe be made to run ONE row, cheaply?

**PLEASE DO NOT RATIFY.**  I want the design attacked, and in particular I want to know if the
cheap option I have not thought of exists.  If the honest answer is "no cheap retrofit", say that --
an honest negative closes this row as documented-only, which is a real outcome.

**Tree under review: `GXEMUL-SEC/regress/`.**

---

## 1.  THE PROBLEM, measured

These probes are pty drivers.  Each ROW is produced by a `session()` call that forks an emulator,
drives it through the debugger, and scores the transcript.  **No probe can score ONE row**, so
adding a row to a measured detector costs a FULL re-run of every session.

Measured cost: one round re-ran a 12-mutant kill table because five rows were added -- **four hours
where twenty minutes would have done.**  The cost model is
`sessions x boot_cost + total_debugger_commands x round_trip`, and **neither term is rows**.

## 2.  WHY THE OBVIOUS FIX DOES NOT WORK

The obvious retrofit is a filter inside `row()`: skip rows whose name is not selected.  **It saves
nothing.**  In the largest probe, **36 of 39 `session()` calls are at MODULE LEVEL** -- the
expensive work has already happened by the time `row()` is called.

Real selection therefore needs either a label threaded through 36 call sites, or the probe
restructured so sessions are lazy.

**COUNTER-EVIDENCE, and it is why this is worth asking:** a seat that wrote a purpose-built probe
the same week BUILT session selection in from the start and used it immediately -- two sessions
instead of eight.  **Cheap when designed in, expensive to retrofit.**

## 3.  THE SHAPE UNDER DISCUSSION (a small probe, same idiom)

```python
 222| 
 223| C040 = 0x04            #  PCC2_C040
 224| BENIGN = 0x10          #  grok: `acc all' already writes this to GENCTL and survives
 225| 
 226| #  ---- CONTROL: the identical instruction, register and width, with a benign value ---------------
 227| t, alive, how = session(setup(r5="0x%x" % BENIGN) + program([ST_B(5, GENCTL)]))
 228| row("genctl ctl", "alive" if alive else "died(%s)" % how, "alive",
 229|     "CONTROL: same st.b, same GENCTL, benign value -- must survive")
 230| 
 231| ctl_saw_c040 = ("C040 interrupt assertions" in t)
 232| row("genctl ctlq", "no" if not ctl_saw_c040 else "yes", "no",
 233|     "CONTROL: the benign write must NOT reach the C040 arm")
 234| 
 235| #  ---- THE DEFECT ROW ---------------------------------------------------------------------------
 236| #  ORACLE POLARITY is the ladder's: assert the CORRECT behaviour, so this is RED pre-fix and GREEN
 237| #  post-fix with the SAME script.
 238| t2, alive2, how2 = session(setup(r5="0x%x" % C040) + program([ST_B(5, GENCTL)]))
 239| row("c040 kill", "alive" if alive2 else "died(%s)" % how2, "alive",
 240|     "one legal guest st.b of 0x04 to GENCTL must NOT end the host")
 241| 
 242| #  ---- ATTRIBUTION: if it died, it died HERE ----------------------------------------------------
 243| #  Green in both directions by construction; RED only if the host dies WITHOUT this arm's text.
 244| sig = ("C040 interrupt assertions" in t2)
 245| row("c040 attrib", "yes" if (alive2 or sig) else "died-elsewhere", "yes",
 246|     "ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic")
 247| 
 248| for _l in t2.split(chr(10)):
 249|     if "C040" in _l:
```

Every probe in this tree is this shape at a larger scale: module-level `session(...)` calls, each
followed by one or more `row(...)` assertions on its transcript.

## 4.  CONSTRAINTS ON ANY ANSWER

* **UNSET MUST BE BYTE-IDENTICAL TO TODAY.**  These probes are consumed by gates that pin exact row
  counts and exact row names; a selection feature that changes default output breaks them.
* **The gates pin DENOMINATORS.**  One gate names all six of a probe's rows by label and pins a
  35-row total in two separate checks, deliberately, so a LOST row is distinguishable from a
  FAILING one.  **Any selection mechanism must not let a filtered run masquerade as a full one.**
* Four guards were already specified for the feature: a printed denominator, hard-fail on zero
  matches, hard-fail on a name that does not exist, and the unset-is-identical rule above.

## 5.  QUESTIONS

**Q1.  Is there a cheap retrofit that does NOT require touching 36 call sites?**  I have thought of
deferring each session behind a closure keyed by the row name it feeds, but that still means editing
every call site.  **Is there a mechanism that gets selection without a per-site edit** -- and if so,
what does it cost in readability, which matters here because these probes are read by reviewers far
more often than they are edited?

**Q2.  What is the failure mode of the mechanism you propose?**  Specifically: how would a reader
tell a FILTERED run from a FULL one that lost rows, given the gates pin literal denominators?  A
selection feature that can silently produce a short run is worse than the four-hour re-run it
replaces.

**Q3.  Is the honest answer "do not retrofit"?**  The counter-evidence says selection is cheap when
designed in.  **Is the correct disposition to leave existing probes alone and require session
selection in NEW ones?**  If so, say so plainly -- that closes this row as a policy rather than a
code change, and I would rather have that answer than a clever retrofit nobody maintains.

**Verdict line first** -- a one-line disposition -- then the body.
