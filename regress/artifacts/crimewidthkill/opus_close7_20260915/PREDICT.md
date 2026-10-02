# PREDICT -- #529 closing pass 7, Opus seat.  Written BEFORE any build or run (this file's mtime is the order proof).

Instrument: the shipped regress/crime_width_probe.py (157 rows), frozen at build time as scripts/crime_width_probe.frozen7.py.
Baseline: GXEMUL-SEC working-tree src/devices/dev_sgi_ip32.c (md5 8c1d1545eeddd12fd49f52ccede60262).

## Shipped probe (157 rows)

| leg | prediction | reasoning |
|---|---|---|
| base | 157/157, CONTROL=OK | the fixed build (probe_first13_fix.out) |
| K1_w_imask4w | **157/157** | the only accepted 4W at INTMASK AFTER a refusal is in `rearm once' (counts notices; a silent decline keeps 1). latch x5's prologue runs with the latch CLEAR, so it is accepted there and `latch said' stays 1. `acc imask sw' is in a refusal-free session. |
| K2_w_rev4 | **157/157** | accepted 4-byte REV accesses after a refusal: `rearm once' only (lw/sw 0x00, lwP, swP). `rev pc ctl' and `revP sw pc' are refusal-free sessions. The `lb/lh rev' sessions' window accesses are REFUSED (1/2-byte). |
| K3_w_ctl8r | **157/157** | accepted 8R at CONTROL after a refusal: `rearm once' only. `acc ctl ld' is refusal-free. |
| E1_byp_ctl4r | **157/157** | CONTROL's high half is always 0 (the prelude writes 0x100 on every access) and the arm does nothing on reads. |
| E2_byp_time4 | **157/157** | rows: TIME 4W/4R occur only in ACCEPTS (rearm once, latch x5 prologue); a silent bypass takes no notice; the skipped updates accumulate. |
| E3_byp_revout | **157/157** | REV is rewritten by the prelude before every access reads it; out of the window the arm does nothing; `sw 0x04' lands in REV's low lane, rewritten too. acc8 near (8R) is excluded from the bypass by construction. |

## Discriminator sessions (scripts/disc7.py; my own sessions, NOT part of the shipped probe)

POST = after ONE refused `lb +0x07`; PRE = the same accesses with no refusal first.

| session | base | K1 | K2 | K3 | E1 | E2 | E3 |
|---|---|---|---|---|---|---|---|
| PRE: sw +0x18 0x10000000; ld +0x18 | 0x1000000000000000 | same | same | same | same | same | same |
| PRE: ld +0x08 | 0x100 | same | same | same | same | same | same |
| PRE: lw +0x00 from 0xbfc05180 -> pc | ra 0x80004000 | same | same | same | same | same | same |
| POST: sw +0x18 0x10000000; ld +0x18 | 0x1000000000000000 | **0x0** | base | base | base | base | base |
| POST: ld +0x08 | 0x100 | base | base | **0x0** | base | base | base |
| POST: lw +0x00 from the window -> pc | 0x80004000 | base | **0xbfc05184** (no redirect) | base | base | base | base |
| EQV: REV/CONTROL/sw 0x04 accesses (values) | per base | -- | -- | -- | identical | identical | identical |
| EQV: default-arm text "write to 0x4:" (stepped) | 1 | -- | -- | -- | 1 | 1 | **0** (transcript only) |

TIME same-microsecond (free-running, E2's EQUIVALENT claim):
* T4W: `ld v1,+0x38 ; sw t0(0x0a0b0c0d),+0x38 ; ld v0,+0x38` free-running.  PREDICT: on base, when the sw falls within
  1 us of the previous update (to_add == 0, no truncation), v0's HIGH half reads 0x0a0b0c0d; under E2 it reads 0.  I do not
  know the hit rate -- running it 6x on base and 6x on E2.  If base shows the high half in any run, item 6's "TIME 4W:
  EQUIVALENT (the high half is 0)" is false in that window.
* T4R: `ld v1 ; sd t0(0x0a0b0c0d11111111) ; lw v0` at +0x38, free-running.  PREDICT: base answers 0x0a0b0c0d in the
  same-us window; E2 answers 0.

## ADDENDUM -- written 2026-09-15 ~07:55, BEFORE building F1-F4 (coordinator's mid-pass request: the panel's silent-form disputes)

| leg | prediction | reasoning |
|---|---|---|
| F1_byp_ctl8w_0201 | **157/157** | the only accepted sd 0x0201 at CONTROL is in ACCEPTS (rearm once, latch x5), whose rows count `-- declined.' only; `acc ctl sd' writes 0x01. Guest-EQUIVALENT: for 0x0201 the arm clears DOG (a local), finds no HARD_RESET, and prints the leftover 0x1 -- host log only; the prelude rewrites CONTROL. |
| F1b_byp_ctl4w_0201 | **157/157** | the same for sw 0x0201 (`sw08 msg ctl' writes 0x01, `sw08 halts' 0x800). |
| F3_byp_sw04 | **157/157** | the store lands in REV's low lane, which the prelude rewrites before any read; only the stepped default-arm debug line differs. |
| F4a_byp_imask4r | **155/157 {imask ctl, gate line}, CONTROL=FAIL** | the imask session's accepted `lw +0x18' and the gate session's `lw +0x18' are the reasserting accesses. |
| F4b_byp_istat4r | **156/157 {istat ctl}, CONTROL=FAIL** | the istat session's accepted `lw +0x10'. |

disc7b (fixed +0x04 read-back register; TIME tests as a TIGHT LOOP, since the first pass pays dyntrans translation
between the accesses): CONTROL-text session `sd 0x0201 +0x08; sw 0x0201 +0x08' -> count of "CRIME_CONTROL: unimplemented":
base 2, F1 1, F1b 1, others 2.  T4W/T4R loops: base -- I now expect the high half to show in SOME runs (the same-us
window); E2 -- never.  The six first-pass T4W/T4R runs on base (disc_base.out, disc7.py) all read high half 0.

## ADDENDUM 2 -- written ~08:05, after disc7.py's T4W (first pass) and BEFORE disc7b runs

MEASURED already (disc7.py, logs/disc_base.out vs logs/disc_E2_byp_time4.out): the first-pass free-running `ld; sw; ld` at
+0x38 reads v0 = 0xc6 / 0x108 on base (6/6) and 0x0 on E2 (6/6).  The high half is 0 on BOTH -- the difference is the
SKIPPED UPDATE: a read's odata is taken BEFORE its own crime_update_crime_time(), so an update skipped at the 4W arrives one
access late.  (My PREDICT above expected the discriminator in the high half; it is in the low word.  Recorded as a miss.)
disc7b adds P4R = `ld; lw; ld` at +0x38 (the 4R twin): PREDICT base v0 = a small nonzero multiple of 66 in most runs,
E2 v0 = 0x0 in every run.  P4W again: base nonzero, E2 0x0.  Loops: base -- high half MAY show; E2 -- low word lags.

## ADDENDUM 3 -- ~08:44, after E3 came back 156/157 {free rev said} (predicted 157/157)

MY MUTANT WAS MIS-BUILT, NOT THE ROW WRONG: E3's condition `relative_addr == CRIME_REV && !(len == 8 && R) && pc out of
window` does not restrict the WIDTH, so it also silently bypassed the REFUSED free-running `lb +0x00' from CODE (free_one,
pc 0x800010xx) -- a refusal cell, not an accept cell.  `rev said'/`lb rev' run from the window (not bypassed) and latch
x5's tail lb +0x00 comes after the latch is set, so `free rev said' is the only row that can see it: exactly the red row.
E3b (below) restricts to the accept widths: `relative_addr == CRIME_REV && (len == 4 || (len == 8 && W)) && pc out of
window'.  PREDICT E3b: 157/157; disc7b EQV values identical to base.  (sw +0x04 is F3's alone.)

## ADDENDUM 4 -- ~09:01, BEFORE disc7b runs: a STEPPED candidate row for TIME 4W/4R
`ld +0x38; sw +0x38 0 (or lw +0x38); ld +0x38 -> s1': base LARGE (the arm's update adds 66 x the ~0.5 s debugger
interval since the first tick); E2 SMALL (the first tick's 66-990 only).  Other binaries: LARGE.
