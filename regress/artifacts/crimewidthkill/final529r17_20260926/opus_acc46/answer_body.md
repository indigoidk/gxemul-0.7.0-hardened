## READ versus RAN, in one place

* **Instrument:** `final529r17_20260926/crime_width_probe.r17.py`, **md5 `2fe7123b`**, 226 rows in 68 sessions.  Its code
  equals table 16's `crime_width_probe.table16.py` (`5f770991`) except three row NOTES (comment-stripped diff).  **I did
  NOT use `regress/crime_width_probe.py` (`a0af7c92`, the 204-row repair-14 probe).**  Before the published file existed
  I froze the scratchpad copy `p529/r17/crime_width_probe.r17.py` (`064aca65`, 08:25).  It differs from `2fe7123b` only
  at docstring lines 472-480, below the bucket block, and every measurement below ran on `2fe7123b`.
* **Source:** `GXEMUL-SEC/src/devices/dev_sgi_ip32.c`, md5 `8c1d1545` (the working tree, i.e. the #529 fix).
* **READ:** every session and row of the probe; `DEVICE_ACCESS(crime)` with its tick, reassert, time-update and init
  functions; repair 13's `killtable11_20260916/PRETABLE.out`; `opus_close7_20260915/OPUS_REPORT.md` S1-S3 and
  `MAINLOOP_HARVEST.md`; `repair14_20260916/BUCKETS8_rerun.out`, `opus_adj_work/logs/b12.out` and `opus_pass1.md`
  S4-S5; table 16's run log; and the two 09-25 re-rulings.  A static session map (`smap17.py`, no emulator) gave
  every ACCEPTS entry's matching accesses by session and latch state.
* **RAN,** in a WSL scratch clone only (`/tmp/gxopus_acc46`, a `cp -a` of table 16's clone `/tmp/gxopus_r14`, which was
  only read).  No project tree was written except this file.
  1. `build46.sh`: `dev_sgi_ip32.c` cmp-clean against GXEMUL-SEC; `src/cpus/*.o` removed; base rebuilt as
     **`b5b99e6d`, byte-identical to table 16's base binary** (so table 16's 226/226 base leg is this binary's);
     one measurement-only mutant built as `envmut` `858bfb4c`; the clone was then restored, rebuilt byte-identical to
     base, cmp-clean, binary newer than source, `.MUTANT` cleared.
  2. **The mutant** (`mut46.py`, a 66-line block inserted immediately before `if (len == 8) {`, the placement of table
     16's `G_glm_tim4clear`).  It sends an access named by `$ACC46` straight to `crime_declined` with **no announce and
     the latch untouched**, and marks each hit on stderr.  That is a SILENT decline, keyed on the exact access kind and
     on the latch state at the access.
  3. **Capture:** the full probe on `envmut` with `ACC46` unset gave **226/226, CRIMEP_CONTROL=OK, 1243 s**.  That run is
     the inertness leg, and its 68 transcripts (all clean, one init marker each, zero hits) are the replay cache.
  4. **92 replays,** 46 entries x {latch CLEAR, latch SET}.  Each re-runs every session that holds a matching access in
     that latch state and serves the rest from the capture, on which the mutant is inert by construction.  For the 31
     guest-visible entries, `rearm *` (S38) and `latch *` (S52) were served from the capture **by declaration**, printed
     as `FROMCACHE` in each log.  The derivation: those sessions' rows are two notice counts, a RAM trip and the
     CONTROL-text count, and none of them can move when an access that prints no CONTROL text is declined silently.
     For the 15 entries whose disposition rests on those two sessions (the ten EQUIVALENT, entry 40, and the four
     text-printing CONTROL writes), S38 and S52 were **re-run**.  Every re-run session's observed hit count equals its
     statically predicted match count.
  5. **Order proof:** `PREDICT46.out` (08:48:04) predates `build46.sh` (08:48:10) and every run.  The result:
     {{SCORE}}.

## The unit

An entry is (width, direction, CRIME offset).  At +0x00 the PROM-window flag is also part of it (the `P` kinds), and
for a CONTROL (+0x08) write so is the stored value.  "Declined" means every probe access of that kind, in that latch
state, is sent silently to the common tail.  That is the K form when the latch is SET (a grown accept guard can only be
silent there) and the G6 bypass form when it is CLEAR.  The ANNOUNCED latch-CLEAR form, a grown accept guard that
announces, is caught at all 46 entries by `latch said` (item 6).  That form is not this table's subject and was not
re-measured here.  `[C]` marks a CONTROL row: its kill also reads `CRIMEP_CONTROL=FAIL`.
