# Records, 2026-10-18: `ip30abortkill` closes -- clause (b) measured on the shipped 33-row instrument, 14/33 as named before the run; its residuals move to `ip30abortresidual`; `#560`/`#561`'s held edits get a row; REGRESS held

`#531` (`686d179c`, committed 2026-09-18) took the four guest-reachable `abort()` calls out of
`src/devices/dev_sgi_ip30.c`: the `0x10020` and `0x10028` loads decline silently, their stores keep their effect with
one latched announce (`IP30_W_ISR`), the `0x10030` store is dropped with that same announce, and DEVICE_TICK's bit-50
arm announces once on its own bit.  Its detector, `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (33 rows),
runs in gate 14 since `#566` (`8faf4a16`).  `#566` named three things still owed before the row could close; this
commit discharges them and closes it:

* **CLAUSE (b), MEASURED** (`regress/artifacts/ip30abortkill/close_20261018/`).  HEAD's `dev_sgi_ip30.c` with the
  removed `fatal("IP30 legacy interrupt rewrite: TODO\n"); abort();` pair re-inserted verbatim at all four fixed sites
  -- after DEVICE_TICK's latched bit-50 announce, after the `0x10020` and `0x10028` arms' if/else, after the `0x10030`
  write announce -- built in `#566`'s scratch clone: **14/33**, the six kill rows DEAD and thirteen state rows `died`;
  gate 14's block text on that log, 41 checks and 22 red.  `PREDICT_clause_b.txt`, written before the build, named
  the same 19 red rows and the same 14 green ones; `CLAUSE_B.txt` records the file times, which git does not carry.
  The clone was restored to HEAD and cleared both parts.  `build/` was not touched.
* **THE WITNESS** now leads with the shipped instrument's pair -- PRE-FIX 10/33, POST-FIX 33/33 (`#566`'s legs) --
  and the clause (b) leg; the 21-row pair and the 18-row oracle-correction order proof stay, as history.
* **THE RESIDUALS** move to a new row, `ip30abortresidual` (LOW, open), rather than close with `ip30abortkill`:
  `V7_nocounter` (delete `d->reg_0x20000 += 1000`; 32/32 in kill table 4, on the 32-row instrument -- the shipped
  `acc 20000` row accepts N = 0, so it cannot see it) and the width axis `V8_len4` (`&& len == 4` on the `0x10020`
  write guard; 33/33 in kill table 5), coverage debt disclosed in the probe's CONTRACT and FILED as the floor says;
  and the three questions `#531`'s own block filed under RECORDED, NOT RESOLVED and no row carried -- whether
  `interrupt-status rewrite not implemented` is true at the `0x10020` and `0x10028` write arms, which keep their
  stores; the per-instance latch axis; fall-through after a non-exiting `fatal()`.  The F13 ruling silenced the read
  arms and settled none of them, and this closure does not claim them repaired.  Grok 4.7 dissented (V7/V8 need no
  carrier, as it ruled at `#566`); GPT-6 Astra and GLM 5.3 upheld the carrier, and the three questions decided it.
* **`#560`/`#561`'s HELD EDITS get a row, `heldrecedits` (LOW, open).**  The fixed file's stale comment counts
  (`SIX announce paths`, `five bits on the ISR side`, `All five ISR sites print`) are `#561`'s held places 7-10.  The
  first draft moved them onto `ip30abortresidual`; Grok 4.7 ruled that a split of one held set, and GPT-6 Astra and
  GLM 5.3 that no ledger row carried them at all.  Both are met by one row for all 37 held corrections (`#560`'s 20,
  `#561`'s 17; 29 are `src/` comments), pointing at the bug file's two held lists.
* **REGRESS and the closure review held for the flagship**: the row's `hold_question` asks for 33/33, 10/33 and 14/33
  on the three builds, and whether the closure stands.
* `wiringcliff`'s commits field gains `#566`'s `8faf4a16`.

Closure check (`regress/artifacts/ip30abortkill/close_20261018/`): GPT-6 Astra 2 flags, both taken (the three filed
questions; the Fable record); Grok 4.7 3 flags -- the `#561` split taken, with its `five ISR sites` wording, and the
Fable record taken; the carrier itself overruled 2-1, its dissent recorded on the row; GLM 5.3, packet-fed, 5 flags --
a packet defect (Fact 1's line numbers were diff-output lines, unlabelled) and the file-name wording taken, three
rejected by a grep, by the probe's own `acc 20000` oracle with table 4's V7 log, and by reading `dev_sgi_ip30.c`'s
`five bits on the ISR side` sentence -- plus its point that the carrier overrides Grok's `#566` ruling, taken.
Fable 5.1 was tried once and walled (HTTP 429, `fable5_close531_WALL.txt`): a SEAT FAILURE, recorded as a
`[NOT A SEAT ANSWER]` entry because a review-stage HELD marker would refuse the close (section H,
CLOSED-WHILE-HELD); its question rides on the REGRESS hold.  Confirm (GPT-6 Astra): {CONFIRM}.  Opus 5.5, agy, kimi,
deepseek and minimax deliberately not fired (the owner's 2026-10-17 roster: Fable, Grok, Astra, GLM).  `ledger.json`, `OUTSTANDING_BUGS.md`, `fable_queue.md`, `matrix.html` (the dashboard) and this block only; no
`src/` touched.
