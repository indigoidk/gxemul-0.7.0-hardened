# AGY JOB 1 — BUILD AND MEASURE a claimed detector escape (#496)

You have build and execute capability and this task needs it. **Measure, do not reason.**

## HOUSEKEEPING — read this first, it is not optional

* **COPY THE TREE. NEVER WRITE TO `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC`.** Work in
  `/tmp/gxagy_r5`. Verify at the end with `git -C /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC status --porcelain`
  and report what it printed.
* Build inside `wsl -d Gentoo` — **the default distro has no `make`.**
* `rm src/devices/dev_dreamcast_gdrom.o` before each build.
* **`MAKE_RC` has been observed reporting 0 on a FAILED build.** Check
  `[ /tmp/gxagy_r5/gxemul -nt /tmp/gxagy_r5/src/devices/dev_dreamcast_gdrom.c ]` explicitly.
* A preserved log is verified by its **completion sentinel** (`GDROMCOND_PROBE_DONE`), not by
  its existence. `tail -1` before citing any number.

## THE CLAIM TO TEST

A round de-fatalised two host kills in `src/devices/dev_dreamcast_gdrom.c` and shipped a
detector `regress/gdrom_cond_probe.py` (16 rows). Its keystone row is:

    R5 cond keep — write ACCEPTED 0xef, then write DECLINED 0x55, then read GDROM_COND
                   back and require 0xef.

The intent is to prove a declined write leaves `d->cond` UNCHANGED.

**A reviewing seat claims R5 is ESCAPABLE by this one-line mutant**, placed in the decline
arm of the `GDROM_COND` case (find it with `grep -n 'unimplemented GDROM_COND'`):

```c
d->cond = 0xef;
```

Its reasoning: after the row's `0xef` anchor, the readback is still `0xef`, so R5 stays
green — while a *fresh* or `0xa0`-anchored decline would fabricate `0xef`, which includes
`COND_DATA_AVAIL` (bit 0x08) and unlocks the GDROM_DATA read path.

## WHAT TO DO

1. Copy `/mnt/c/DocumentNoSnc/cc/GXEMUL/build` to `/tmp/gxagy_r5`, then copy
   `GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c` over the clone's copy. `cmp` them and say so.
2. Build the BASELINE and run the probe:
   `python3 -u <SEC>/regress/gdrom_cond_probe.py /tmp/gxagy_r5/gxemul /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd`
   Report the full row table and `GDROMCOND_PROBE_RESULT`.
3. Apply the mutant, rebuild, re-run, report the table and result.
4. **ANSWER THE QUESTION: does R5 stay green under the mutant?** If it does, the row is
   escapable and the claim is confirmed. If it reds, the claim is refuted — say so plainly.
5. **THEN TEST THE PROPOSED REPAIR.** The repair is to give R5 three pre-states instead of
   one: (a) fresh device `0x00` -> decline -> require `0x00`; (b) accepted `0xa0` -> decline
   -> require `0xa0`; (c) accepted `0xef` -> decline -> require `0xef`. Write those three
   rows into a COPY of the probe in `/tmp` (never into SEC) and measure whether they kill
   the mutant while staying green on the baseline. **Both legs matter** — a row that reds on
   the baseline too is not a detector, it is a broken row.

## REPORT

Verdict line first. Then the two (or four) row tables, the sentinel line for each, and a
plain statement of whether the escape is REAL and whether the repair KILLS it. If you could
not build or run, say so plainly and stop — that is a real answer and I need to know.
