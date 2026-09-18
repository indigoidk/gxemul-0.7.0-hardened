# #530 closing pass 5 -- the Opus measuring seat WALLED mid-pass; this is the main loop's harvest of its artifacts

*** THE SEAT DID NOT WRITE ITS OWN ANSWER.  It terminated on `You've hit your weekly limit - resets Sep 18, 3am
(America/Chicago)' (HTTP 429, model claude-opus-5, request req_011Cf5QzHhzLGgRN46FzVxp1) at ~09:2x on 2026-09-15, after
building and running every leg below.  A SEAT FAILURE is never agreement: the seat's VERDICT is missing and only these
MEASUREMENTS survive.  They are its own logs, preserved here; the readings in the right-hand column are the MAIN LOOP's,
written 2026-09-16, not the seat's. ***

Instrument: `instrument/lca_isalane_probe.c5.frozen.py` (the shipped 185-row probe).  Mutants: `instrument/mut530c5*.py`
(its own, preserved as run).  Clone `/tmp/gxopus530c5` -- checked by the main loop after the wall: NO `.MUTANT` sentinel,
`dev_lca.c`, `dev_sgi_ip32.c` and `dev_pckbc.c` all cmp-CLEAN against GXEMUL-SEC; every project build tree CLEAN; no
orphan process.

| leg | score | main loop's reading |
|---|---|---|
| base | 185/185 | the instrument is the shipped one |
| **WWtail** | **185/185** | the STORE forward DUPLICATED, gated to the split-tail widths -- glm, kimi-k3 and the kimi CLI seat each predicted exactly this.  ESCAPE |
| **WW6** | **185/185** | the same at len 6 only (glm's form).  ESCAPE |
| WWall | 169/185 | the UNGATED store duplicate: caught, by the stub rows (16 of them) |
| **RD2post** | **161/185** | the read forward duplicated AFTER the packing loop (the first byte is kept).  24 reds -- stub r (16) + rdq (4) + tailq r (4), and NO cmos/iirr2 row: exactly codex's finding that for this form the STUB is the SOLE carrier at lanes 1 and 2, against the flagship ruling's RB1 |
| **RD2z** | **185/185** | the read duplicate gated on the delivered byte being 0 (the kimi CLI seat's GAP 2).  ESCAPE |
| **cdxZL3** | **185/185** | codex's lane-3 x ZERO-data phantom read.  ESCAPE |
| **dNZtail** | **185/185** | a tail fallthrough gated on a NONZERO stored byte (the tail rows store 0).  ESCAPE |
| RWtail | 183/185 | caught (2 rows) |
| W23 | 184/185 | caught (1 row) |
| nox | 181/185 | `dev_pckbc.c`'s stub counter with its `x++` REMOVED: exactly the four `stub<l> live' rows red and every stub access row green -- the LIVENESS rows do what they were added for (the flagship ruling's mandatory control, measured) |

**What this settles for closing pass 5: it is NOT clean.**  Four measured escapes, each guest-visible by the panel's own
derivations, and one carrier violation (RD2post).  The forward-count class as enumerated by repair 5 has only two arms
(the store's phantom read, the load's duplicated forward); the STORE's own duplicate is a third, and the data axis is not
closed at the tail or lane-3 cells.

## *** CORRECTED 2026-09-16 BY THE FINISHING SEAT (OPUS_ANSWER.md section 1).  FOUR CORRECTIONS; THE FIRST IS MINE AND IS MATERIAL. ***

1. **I UNDERSTATED THE BREACH, AND THE WALLED SEAT HAD ALREADY FOUND WHAT I DROPPED.**  I wrote *"WWall 169/185 -- the
   UNGATED store duplicate: caught, by the stub rows (16 of them)"*.  True and materially incomplete: **the 16 stub rows
   are the ONLY reds.**  Not one architectural row moves -- `kbcq * dib`, `iir st*`, `cmos w*`, `tailq w t*` are all
   green.  So for the store-duplicate form the emulator-TODO stub is the **SOLE CARRIER at lanes 0, 1 AND 2 -- twelve
   cells**, a strictly WIDER breach of the ruling's RB1 than the RD2post one I did flag.
   **`logs/PREDICT.out`, written at 07:44 before any build, predicts exactly this**, naming the reason (*"the stub
   counter is direction-blind; kbcq, iir and cmos cannot see a doubled store"*).  *The finding was made before the
   measurement and my harvest lost it -- which is the unread-review class happening inside a single round.*
2. **"after building and running every leg below" IS WRONG, and the error is the interesting kind.**  The walled seat's
   driver was **BACKGROUNDED and ran on unattended** after the wall: batch 1 finished 09:22:59, batch B's probe legs
   landed 09:42 and 10:02, and all nine `discB_*` legs between 10:07 and 10:28.  So it LAUNCHED every leg and READ eight
   of eleven.  **It never saw WW6, RD2post or cdxZL3, and never saw ANY of the 8253 measurement -- which it had itself
   designed, predicted (`PREDICT2.out`) and RUN.**  That output sat unread on disk for a day, and the 8253 question was
   then re-opened as "the open question to measure".  **An UNREAD REVIEW inside a seat's own artifacts, and it cost this
   round a day.**
3. My closing paragraph -- *"the forward-count class as enumerated by repair 5 has only two arms ...; the STORE's own
   duplicate is a third"* -- is right as far as it goes and **short by five**: the space is EIGHT cells
   ({write, read} x {DROP, SWAP, DUPLICATE, ADD-OTHER}), and my "third" is one of the six the contract does not name.
4. Two omissions: `Wpure` was built with **no probe leg** BY DESIGN (`PREDICT2.out` says so; table 6 already scored that
   mutant at 153/185) -- not a gap; and my table omits the `restored`/`restoredB` control binaries, which their drivers
   recorded as byte-identical to `base`.

*Everything else the seat could check in this harvest is accurate, including the RD2post reading (24 reds = `rdq r1-r8`,
`stub0-3 r1-r8`, `tailq r t7/t6/t5/t3`, with no `cmos r*` and no `iirr`/`iirr2`, so the stub IS the sole carrier at lanes
1 and 2 for that form -- exactly codex's prediction).  All eleven scores verified against the raw logs, every log ending
`LCAISALANE_DONE`, and the mutant diffs matching their descriptions.*
