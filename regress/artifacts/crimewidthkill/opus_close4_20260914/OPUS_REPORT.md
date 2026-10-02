# #529 CLOSING PASS 4 -- the Opus 5 seat (Agent tool, measuring)

*** TRANSCRIBED BY THE MAIN LOOP (Agent seats leave no file; the seat's first turn ended mid-wait and it was RESUMED, not
re-launched).  Verdict and tables VERBATIM in substance.  Re-read before recording: table_c4.out / table_c4b.out (every
leg `last=CRIMEP_DONE', base 131/131 CONTROL=OK) and logs/disc_c4.out (every DISC line quoted below). ***

Liveness `OPUS_SEAT_ALIVE_20260914_CRIME_CLOSE4`; CHECKPOINT line 1 quoted verbatim.

## VERDICT: GAP
Four of five buildable claims are real 131/131 survivors that change guest-visible behaviour; deepseek's literal edit is
DEAD code but its cell is really unrowed.  Simplest exact edit, in the CRIME_INTSTAT/CRIME_INTMASK arm before
`crime_interrupt_reassert(d);`:  `if (writeflag == MEM_WRITE) d->warned = 0;`  -- refuse, accepted `sd` at +0x18,
refuse gives TWO announces instead of one.  The cause is the one pass 3 named, one level down: pass 4 took each branch's
two sides SOMEWHERE (the marginals), not the cross of the access KIND with the case LABEL that the contract promises.

## Per-claim (frozen shipped probe md5 2ee8e3d6...; discriminator = the same guest-only script on base and mutant)
| claim / mutant | 131-row | discriminator base -> mutant | disposition |
|---|---|---|---|
| deepseek c1 (`idata == DOG_ENABLE` after the DOG block) | 131/131 | 1 -> 1 announce | EQUIVALENT (dead: the block already cleared 0x200) |
| live form d2_pre_dog0200 | 131/131 | 1 -> 0 | FLOOR: (DOG set, leftover 0) = 0x0200 unrowed |
| live form d1_rearm_dog0200 | 131/131 | 1 -> 2 | FLOOR (same cell, re-arm side) |
| kimi-k3 c2 (`odata = reg[HARDINT/8]`) | 131/131 | HARDINT 0x20; refused lb/lh +0x08 0x0 -> 0x20 | FLOOR: no refused read in the gate session |
| codex c3 (`relative_addr & 8 ? debug : fatal`) | 131/131 | free-running lb +0x0f: 1 -> 0 | FLOOR: the notice channel pinned at one cell |
| sibling d6_chan_len2 (`len == 2 ? debug : fatal`) | 131/131 | free-running lh +0x06: 1 -> 0 | FLOOR (width axis) |
| kimi CLI c4 (re-arm on a write, INTSTAT/INTMASK arm) | 131/131 | refuse / sd +0x18 / refuse: 1 -> 2 | FLOOR (the verdict edit) |
| sibling d7_rearm_wrev (same, REV arm) | 131/131 | 1 -> 2 | FLOOR |
| sibling d4_pre_wistat (pre-set on a write at +0x10) | 131/131 | 1 -> 0 | FLOOR (pre-set side) |
| sibling d3_rearm_wtime (re-arm on a TIME write) | 130/131 (dog once) | -- | DETECTED, as predicted |
| codex c5 (2W landing keyed on addr bit 1) | 131/131 | sd 0 +0x18, refused sh 0xffff +0x1e, ld +0x18: 0x0 -> 0xffff | CONTRACT BREACH (the DISCLOSED "every bit 0-9 both ways" is false for 2W bit 1) |
| codex 6 (is_32bit, RAM config, use_fb) | not built | -- | MACHINE CONSTANTS on the probe's machine |

## The complete derived enumeration (from DEVICE_ACCESS(crime)'s own tests)
Accepted kinds at each label: {8W, 8R, 4W, 4R} (labels are 8-aligned, so 4-byte accesses there are the high lane); all
six (both lanes) at the default arm; CONTROL additionally x DOG x leftover (0x0201, 0x0001, 0, 0x0200); REV x pc window.
PRE-SET open: REV 8R/4W/8W and window writes; CONTROL 4W 0x0200, 8W, 8R; INTSTAT 8W/4W/8R; INTMASK 4W/8R; DOG 4W/4R;
TIME 8W/4W/4R; default 4W high lane.  RE-ARM open: REV 4W/8W/8R and window writes; CONTROL 4W 0x0200, 8W, 8R; INTSTAT
8W/4W/8R; INTMASK 8W/4W; TIME 4W/4R; default 4W/4R high lane.  LATCH notice CHANNEL (fatal vs debug): the one
free-running refusal (1R +0x07) cannot see a channel keyed on an address bit, width, direction or label.  ANSWER SOURCE:
HARDINT / preserved_CRIME_HARDINT open (every other lvalue the function reads is covered).  LANDING: 2W bit 1 set open.

## Minimal closing set -- ONE diff
1. ONE shared access list used as latch x5's prologue (pre-set) AND as KINDS (re-arm): {8W, 8R, 4W, 4R} at REV (+ sw/sd
   from the probe window), INTSTAT, INTMASK, DOG, TIME; CONTROL 4R, 8R, and 4W/8W at each of 0x0201, 0x0001, 0, 0x0200; the
   default arm's six kinds incl. the high lane at +0x40.  ~40 accesses, NO new rows.
2. Gate session: after HARDINT is latched and before the refused `sh 0x800`, a refused lb and lh at +0x08 -- rows
   `gate lb v0`, `gate lh v0` want 0x0.
3. Landing: a refused `sh 0xffff` at +0x42 before the existing `ld +0x40` (`lo keeps`) -- no new row.
4. Channel: free-running one-refusal sessions with a `said` row each -- single-axis 3 (2R lh +0x1f8; 1W sb +0x27f; 2W
   sh +0x08), plus one per label (REV, INTSTAT, INTMASK, DOG, TIME) = 8.  The label x channel cells may be DISCLOSED as
   clause-(e) debt instead; the single-axis 3 cannot be, because the contract claims address bits and width.

## Wrong statements
Contract items 4/8 ("both sides of every if") -- sides, not their cross with the label, and CONTROL (DOG set, leftover
0) missing; the DISCLOSED address-bit bullet is false for 2W bit 1; item 5's channel is pinned at one cell; item 10 pins
only a refused write under a latched interrupt, never a read's answer; a refused halfword at +0x1e lands on INTMASK
(`relative_addr / 8`), not at +0x1e.

## Could not check
The other open cells were not all built (TIME/DOG 4W/4R pre-set, INTSTAT/INTMASK 4W, 8R at REV/CONTROL/INTSTAT, REV
window writes, default high lane, channel x label); the closing set is not built; batch 1 used the brief's predictions as
its PRETABLE (PRETABLE2.out 02:42:53 predates batch 2).  Scratch clone /tmp/gxopuscrime4 restored (cmp clean, fresh,
byte-identical to baseline, sentinel removed) and deleted.
