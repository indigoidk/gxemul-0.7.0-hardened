# CLOSING PASS 8 -- STOPPED BY THE OWNER, 2026-09-16 ~20:5x

**The owner asked for a pause point and then to close anything still running. The two kill tables were killed
deliberately; they did not fail.** This file says exactly what is measured, what is not, and what must never be cited,
so a future session does not mistake a truncated log for a result.

`RESUME.md` (the measuring seat's own) is unedited and remains the authority on the seat's findings and its pickup
instructions. This file only records the stop.

## HOW IT WAS STOPPED, and why it was safe at that moment

* **Table B had not started.** It waits on `KILL8_DONE`, and Table A never reached it. **Table B is the one that
  mutates the clone and drops a `.MUTANT` sentinel first**, so stopping before it began meant no tree could be left
  mutant. Had the stop come thirty minutes later it would have needed the restore recipe in `RESUME.md`.
* Killed with `pkill -f` from a script named `stopc8.sh` -- **deliberately containing none of the patterns it kills**,
  because this project has recorded `pkill -f <script>` terminating the shell running it (exit 15, before it could
  report its own result).
* **Verified in a SEPARATE invocation**, for the same reason: a cleanup that cannot report its own result is a cleanup
  you have to redo. Result: **0 processes of ours alive**, and all eight trees -- `build/`, `build-asan/`,
  `/tmp/gxsec-build`, `/tmp/gxopusc8`, `/tmp/gxopuscrime`, `/tmp/gxlca530`, `/tmp/gxopuscrimec7`,
  `/tmp/gxopus530c5` -- reporting **no sentinel, p1 CLEAN, p2 FRESH**.

## WHAT IS MEASURED -- 8 legs, each carrying `CRIMEP_DONE`

| leg | score | what it settles |
|---|---|---|
| `base` | 188/188 | the instrument is clean under this table's own conditions |
| `L_dfl4w_hi` | 185/188 | lane axis, default arm, 4-byte write, high lane |
| `L_dfl4w_lo` | 185/188 | ...low lane |
| `L_dfl4r_hi` | 186/188 | ...4-byte read, high lane |
| `L_dfl4r_lo` | 185/188 | ...low lane |
| `W_rev8r_out` | 187/188 | **the POSITIVE CONTROL for the PC-window axis** -- reds `p rev ld` ONLY |
| `W_rev8w_out` | 188/188 | equivalent, and it means equivalence *because* `W_rev8r_out` reds |
| `W_rev4w_out` | 188/188 | likewise |

**Two axes the enumeration never named are therefore measured CLOSED** -- `relative_addr & 4` (the lane) and
`cpu->pc` (the PROM window) -- which makes them RECORDS defects rather than floor gaps. The seat's own
`check_pred8.py` scored these 8 as **PREDICTIONS MATCHED 8, WRONG 0**, against predictions whose mtimes
(`PREDICT.md` 20:04:24) predate the first build log (20:07:03).

## *** WHAT MUST NEVER BE CITED -- four TRUNCATED logs ***

These four were killed mid-probe. **They carry no `CRIMEP_DONE` sentinel, and a preserved log is verified by its
sentinel and not by its existence:**

    logs/probe_G_lane_all.raw     logs/probe_G_lane_ist.raw
    logs/probe_G_lane_tim.raw     logs/probe_W_rev4r_out.raw

A truncated leg is indistinguishable from a hang or a clean sweep if you read only its tail. **Re-run them; do not
read them.**

## WHAT WAS NEVER RUN

* The remaining Table A legs beyond the four above (the landing and re-map shapes).
* **ALL of Table B** -- and Table B is where the verdict turns. It carries the four latch-CLEAR cells
  (INTSTAT 4R, TIME 4W, TIME 4R, plus glm's TIME cell) and codex's HARD_RESET generating-set cells, together with the
  owed rows the seat already built: `t4clear.py` (the gapped shape MINUS the opening refusal) and `ctlreset.py`.

**So closing pass 8 has NO VERDICT, and the seat declined to issue one on a third of the evidence before it was
stopped.** The mutants and the owed rows are built and queued; resuming means re-running Table A's remainder and
Table B, not rebuilding them.

## WHAT THE PASS ALREADY ESTABLISHED, and it does not depend on the unrun legs

**The latch-CLEAR half of the product is open.** glm (GAP) and codex (NO-GO) reached it independently from the
packet; the measuring seat then derived it at cell granularity -- **eight of the 46 ACCEPTS entries are driven
latch-CLEAR by `latch x5` ALONE**, and that session's only three rows are two announce counts and a RAM round trip,
all blind to a silent decline. Open guest-visible cells: **INTSTAT 4R, TIME 4W, TIME 4R**. glm named one member; the
class has four.

That is the K-class's own argument with CLEAR and SET exchanged, and the contract's amended clause -- *"CAUGHT ...
AND THE CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE"* -- fails for those cells **by its own words**.

**#529 is NOT closed and probably owes a repair 14.** That conclusion is safe on the evidence that exists; what the
unrun legs would have settled is whether the specific mutants escape at 188/188, which is the difference between
`GAP` with exact edits and a narrower records finding.


---

## A NEW SHAPE OF THE CHECK-THAT-CANNOT-FAIL, found by the seat while verifying this very stop

**`ps -ef | grep -c "[g]xemul"` returned 1 with NOTHING RUNNING.**

The bracket trick (`[g]xemul`) stops *grep* from matching its own pattern -- that is the part everyone knows. But
`ps` prints the argv of the **`wsl -- bash -c '...'` wrapper**, and that argv contains the literal pattern. So the
count is inflated by one whenever the check is invoked through a shell whose command line carries the pattern.

> **READ THE MATCHED LINES, NEVER THE COUNT.**

*This is the third distinct form of this trap now on record here: `ps -ef` on this machine is argument-blind for
SCRIPT names (so a pattern naming a script can never match and the check answers "dead" always); `pgrep -f` matches
its own wrapper; and now a bracket-tricked `grep -c` counts the wrapper too. The first two answer FALSE-NEGATIVE, this
one answers FALSE-POSITIVE.*

**The stop verification in this file is unaffected, and the reason is worth stating rather than assuming.** It was run
from a SCRIPT FILE (`_scratchpad/verifystop.sh`) via `wsl -- bash /mnt/c/.../verifystop.sh`, so the wrapper's argv is
the script's PATH and contains none of the killed patterns. It returned **0**, and this trap can only inflate a count,
never deflate it -- so 0 is sound in the safe direction. Had it been invoked as `wsl -- bash -c '...'` with the
patterns inline, it would have reported 1 and I would have gone looking for a process that did not exist.

## Owed rows already BUILT for the resume (the seat names three, not two)

    scripts/t4clear.py    the gapped TIME shape MINUS the opening refusal -- the latch-CLEAR row
    scripts/ctlreset.py   the HARD_RESET generating-set row for codex's cell
    scripts/ctl4r.py      the post-latch 4-byte READ at CONTROL -- the row whose absence made C_ctl4r vacuous

*The third is the direct answer to deepseek's finding: `C_ctl4r` scored 188/188 for want of an ORACLE, and this is the
oracle. Resuming means RE-RUNNING, not rebuilding.*
