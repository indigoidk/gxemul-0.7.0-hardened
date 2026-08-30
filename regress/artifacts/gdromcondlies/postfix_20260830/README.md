# POST-FIX leg of the `#496` witness — and its banner says the opposite of what it measures

`witness_postfix_run1.out` opens with:

    gdromcondlies WITNESS -- rung 3, on the COMMITTED build, BEFORE any fix.

**That line is FALSE of this run.** The file records the witness measuring the **FIXED**
build (`build/gxemul`, with `#496` applied — the two-part clearance lines at the top of the
log are present and correct). The banner is a fixed string inside the witness script, which
was re-run rather than re-written, so it reprinted its pre-fix caption.

Annotated here rather than edited, for two reasons:

* **The witness is a frozen instrument.** Editing it between the two legs would break the
  one thing that makes the comparison mean anything — *a comparison run owes ONE
  instrument*. The pre-fix 15/15 and this post-fix 11/15 came from byte-identical code, and
  that is worth more than a correct caption.
* **The mislabelled-caption class is exactly what this project keeps paying for**, so the
  correction belongs where a reader will hit it, not silently in the script.

Caught by the fable5 seat on pass 2, under the standing license, while verifying something
else.

## What the run actually shows

    GDROMCOND_WITNESS_RESULT=11/15        (pre-fix: 15/15)

Four rows flipped, and they are exactly the kill rows. Columns are **`got want`** —
verified against the probe's own header line, not assumed:

| row | got | want | reading |
|---|---|---|---|
| `a88 kill` | `exit0` | `exit1` | host now SURVIVES |
| `a88 alt` | `exit0` | `exit1` | a different bad value also survives |
| `cond kill` | `exit0` | `exit1` | host now SURVIVES |
| `a88 says` | `0` | `1` | the OLD message text is gone — `#496` rewrote it |

Still green: all three ACCEPT rows, both quiet rows, all four controls, and
`cond says`/`cond echo` — so the new site-B diagnostic still carries the guest's own byte
and still tracks it.

**This inversion is why the witness is `CLASS_WITNESS` and correctly ungated.** Its kill
rows invert the day the fix lands; gating it would manufacture a regression. The round's
standing coverage is `regress/gdrom_cond_probe.py`, which is a different file with the
opposite oracle — and which may not read survival on its accept side at all.
