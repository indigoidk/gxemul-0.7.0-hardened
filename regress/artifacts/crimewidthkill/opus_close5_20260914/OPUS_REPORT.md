VERDICT: CLOSES (no FLOOR gap remains in the 141-row test; every 141/141 survivor I built is a JOINT beyond the body-tested generating set or a machine-config lvalue = clause-(e) debt, covered by the DISCLOSED list). CRIME_CLOSE5_OPUS_20260914

CHECKPOINT.md line 1, verbatim:
`# CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED`

# #529 CLOSING PASS 5 -- Opus 5 seat (Agent tool, MEASURING)

I built a fresh baseline from `GXEMUL-SEC`'s working-tree `dev_sgi_ip32.c` in two scratch clones
(`/tmp/gxopuscrimec5`, `/tmp/gxopuscrimec5b`), each `cmp`-clean vs SEC and rebuilt (`rm src/cpus/*.o
src/devices/dev_sgi_ip32.o`; `[ gxemul -nt src ]` verified), ran a FROZEN copy of the shipped
141-row probe, and swept 14 mutants (5 novel + 9 panel P1-P7) plus a 5-run ACCEPTS-augmentation
test. **base = 141/141 CONTROL=OK on both clones.** Both clones restored (`cmp`-clean, no sentinel)
and DELETED. Logs preserved under `opus_close5_20260914/logs/`, scripts under `scripts/`.

## Q1 -- IS `ACCEPTS` EXACTLY THE FUNCTION'S ACCEPTED-ACCESS FLOOR?

Derived from `DEVICE_ACCESS(crime)`'s own branches (not from past findings). An accepted access
(len in {4,8}) takes:
- WIDTH ARM: 8W, 8R, 4W(&4=0 hi lane), 4W(&4 lo), 4R hi, 4R lo -- 6 kinds.
- SWITCH label (reached only by accepted accesses): REV, CONTROL, INTSTAT/INTMASK (shared), DOG,
  TIME, default.
- REV body tests ONE thing: `pc-window` (in/out). It does NOT test len or direction.
- CONTROL(write) body tests DOG(0x200), HARD_RESET(0x800; disclosed -- stops CPUs), leftover!=0.
  ENDIANESS(0x100) is cleared UNCONDITIONALLY -- there is NO `if` on it.
- INTSTAT/INTMASK/DOG/TIME bodies read no idata bits. default distinguishes R/W and both 4-byte lanes.

`ACCEPTS` (43 kinds) crosses {8W,8R,4W,4R} with every label, CONTROL writes x{0x0201,0x0001,0,0x0200}
(DOG x leftover, both widths) plus CONTROL reads, REV window {4R=lwP,4W=swP,8W=sdP}, and the default
arm's six kinds in both lanes. **This covers the whole body-tested floor cross with ONE omission:**

> **`ACCEPTS` OMITS `ldP` (8R at REV from the PROM-probe window).** It has window 4R/4W/8W but not 8R.

No kind it lists is unreachable. No row it feeds (`rearm once`, `latch x5`) is vacuous -- both varied
under many mutants (measured below). So `ACCEPTS` = the body-tested floor MINUS the window-8R cell,
which is a JOINT the REV window branch's body does not distinguish (see Q2 disposition).

## Q2 -- FLOOR GAP HUNT (all MEASURED on my clones, base=141/141)

### Survivors (141/141, guest-visible, all clause-(e) by the JOINT-CELLS bound)
| mutant (source edit) | 141-row | guest-visible discriminator (base -> mutant) | disposition |
|---|---|---|---|
| **P1 / j_win8r** `case CRIME_REV: if(pc-window && len==8 && READ) d->warned=0;` (re-arm inside the window if) | **141/141** | (ld CRIME_REV @pc 0xbfc051xx) then narrow x2: announce count **1 -> 2** | clause-(e): window branch tests only pc, not len/dir |
| **P1b** same, `d->warned |= CRIME_W_LEN;` (pre-set) | **141/141** | pre-silences a later narrow refusal after an 8R-window read | clause-(e) |
| **P2** `case CRIME_CONTROL` write: `if(idata & ENDIANESS) d->warned=0;` | **141/141** | accepted CONTROL write w/0x100 then narrow: announce **1 -> 2** | clause-(e): ENDIANESS is cleared, never branched (not in the generating set) |
| **P2b** same, pre-set | **141/141** | pre-silences after a 0x100 CONTROL write | clause-(e) |
| **P3** `(relative_addr==CRIME_INTSTAT && len==2 ? debug : fatal)(` announce | **141/141** | free-running 2-byte refusal at INTSTAT: fatal **prints -> silent** | clause-(e): multi-axis channel joint (floor rows single axes) |
| **P5** `odata = d->use_fb;` before the decline `goto` | **141/141** | use_fb=1 (graphics O2): refused read answers **0 -> 1** | clause-(e): machine-config lvalue, 0 on the probed machine |

### Confirmation these survivors are clause-(e) and cheaply closeable -- the ACCEPTS-augmentation test
Adding `("ldP",0x00,0), ("sw",0x08,0x0100), ("sd",0x08,0x0100)` to `ACCEPTS` (probe-only, row count
UNCHANGED at 141), measured against the survivor binaries:
```
  aug_base            141/141 CONTROL=OK   (no row disturbed)
  aug_P1_win8r_rearm  140/141  FAILING: rearm once     <- ldP kills the re-arm
  aug_P1b_win8r_preset 140/141 FAILING: latch x5       <- ldP kills the pre-set
  aug_P2_ctl_endi_rearm 140/141 FAILING: rearm once    <- CONTROL 0x100 kills it
  aug_P2b_ctl_endi_preset 140/141 FAILING: latch x5    <- CONTROL 0x100 kills it
```
So ONE tuple (`ldP`) closes P1+P1b and disturbs no other row; the two CONTROL-0x100 tuples close P2+P2b.

### Caught mutants (the floor IS live -- these reddened their predicted rows)
| mutant | 141-row | failing rows |
|---|---|---|
| n_chan_dog `(relative_addr==CRIME_DOG?debug:fatal)` | 140/141 | free dog said |
| n_rearm_deflo re-arm on default 4W LOW lane | 140/141 | rearm once |
| n_ans_ra `odata=relative_addr` | 117/141 | 24 `* v0` answer rows (not `lb/lh rev v0`: REV offset=0 => equiv) |
| n_ans_len `odata=len` | 115/141 | 26 `* v0` rows (incl. `lb/lh rev v0`: len!=0 even at REV) |
| P4 `odata = reg[CRIME_SOFTINT/8]` | 135/141 | imask/istat/gate lb/lh v0 (SOFTINT nonzero in those sessions) |
| P6 pre-set on accepted READ before the switch | 137/141 | time once, time said, top said, latch x5 |
| P7 `d->warned |= CRIME_W_LEN << (relative_addr & 1)` | 137/141 | warm once, rearm once, hi once, mid once |

### Why CLOSES and not GAP
The floor for a pre-set/re-arm latch cell is the accepted-access classes the function's own body
DISTINGUISHES (the CLAUDE.md JOINT-CELLS bound: the cross of dominating predicates with body-tested
lvalues; single-operand marginals and untested-value joints are clause-(e), not floor). At the REV
window branch the body tests only `pc`, so `(window & len==8 & READ)` is a joint the body does not
make -- clause-(e), covered by the DISCLOSED "a latch keyed on a JOINT predicate ... clause (e)"
bullet. P2 (ENDIANESS) is likewise clause-(e) (the bit is cleared, never branched, so it is not in
CONTROL's generating set {DOG, HARD_RESET, leftover}). P3 is a multi-axis channel joint (item 5 rows
single axes). P5 is a machine-config lvalue that is 0 on the probed machine. **No mutant escaped that
is inside the body-tested floor** -- every floor-cell mutant I built (n_chan_dog, n_ans_ra, n_ans_len,
n_rearm_deflo, P4, P6, P7) was killed on its predicted rows. So the 141-row test has no FLOOR gap.

### STRONG RECOMMENDATION (free, measured) -- add `("ldP", 0x00, 0)` to `ACCEPTS`
Even though P1/P1b are clause-(e) by the bound, the window sub-cross is VISIBLY ASYMMETRIC: repair 10
built window {4R, 4W, 8W} and left 8R. That is the exact "one case over" shape the brief warns about,
and it will re-invite this doubt every future pass. Adding `ldP` is one tuple, kills both P1 and P1b,
and (measured) disturbs no other row. I recommend it as an L1-style tidy, not because the floor is open.

### Denominator (so "zero found" != "zero looked for")
Shapes BUILT and SWEPT on the 141-row probe (16 mutant binaries + 5 aug runs, all base=141/141
CONTROL=OK, every leg last=CRIMEP_DONE):
- pre-set/re-arm at cells beyond ACCEPTS: REV-window-8R re-arm (P1) & pre-set (P1b); CONTROL-ENDIANESS
  re-arm (P2) & pre-set (P2b); default-LOW-lane 4W re-arm (n_rearm_deflo, caught); accepted-READ pre-set
  in the accepted path (P6, caught).
- answer source: relative_addr (caught), len (caught), SOFTINT (caught), use_fb (survives, clause-(e)).
- notice channel: DOG label (caught), INTSTAT&len2 joint (survives, clause-(e)).
- latch keying: address parity `<< (addr&1)` (P7, caught).
NOT built (out of scope / disclosed): host-death reinstatement & FAULT (tables 1/7, floor (a)/(b));
deeper >=3-axis joints; the RAM-size/2-instance/width-3-5-6-7 disclosures.

## Q3 -- WRONG / IMPRECISE STATEMENTS
1. **Item 9 (probe header AND brief): "every lvalue the function reads is nonzero where a refused
   answer is read, including HARDINT" is FALSE.** `use_fb` (0 here -- P5 survives 141/141 proving
   `odata=use_fb` is equivalent on this machine), `idata` (0 on reads), and `flag_for_128MB` (0 at
   `-M 64`) are lvalues the function reads that are 0 at every rowed refused read. Correct form: every
   lvalue that is NONZERO at a rowed refused read is caught; machine-config lvalues that are 0 on the
   probed machine (`use_fb`, `flag_for_128MB`) are a single-machine-probe limitation and should be
   DISCLOSED (analogous to the function-static-latch disclosure), because `use_fb=1` on a graphics O2
   makes `odata=use_fb` a guest-visible change from 0 to 1.
2. **Disclosure gaps (clause-(e) survivors not explicitly named):** the DISCLOSED list should add
   (a) a latch keyed on the CONTROL ENDIANESS bit (P2 -- guest-REACHABLE, real guests set 0x100),
   (b) multi-axis NOTICE-channel joints (P3), and (c) machine-config answer lvalues (P5). The generic
   "joint predicate ... clause (e)" bullet arguably covers P1/P3, but the window sub-cross asymmetry
   (Q2) is not disclosed and reads as an oversight.
3. **Brief line 20 "closes the cross from ONE list, ACCEPTS":** the cross is closed EXCEPT the
   REV-window-8R (`ldP`) cell -- "closes the cross" is very slightly overstated.
4. Minor: table 8's `x_rearm_rev8r` ("re-arm on an 8R at REV", caught by `rearm once`) is the
   REV-CASE-TOP form (caught by the ordinary `ld 0x00`); it does NOT cover the REV-WINDOW form (P1),
   which needs `ldP`. The record does not claim otherwise but a reader could conflate them.

I could NOT independently re-run all 45 table-8 legs (I re-derived the enumeration and sampled the
cells beyond ACCEPTS plus the panel set). The POSTTABLE's "44 exact / 1 differs" is consistent with
my independent base=141/141 and my caught-mutant rows landing exactly where predicted.

## PANEL MUTANTS (measured for the coordinator)
| id | 141-row | verdict | failing rows / discriminator |
|---|---|---|---|
| P1 (5 seats) win8r re-arm | 141/141 | SURVIVES | ld REV-window then narrow: announce 1->2; killed by adding `ldP` (aug: rearm once) |
| P1b win8r pre-set | 141/141 | SURVIVES | killed by adding `ldP` (aug: latch x5) |
| P2 (3 seats) CONTROL ENDIANESS re-arm | 141/141 | SURVIVES (clause-(e), ENDIANESS not branched) | killed by adding CONTROL 0x100 (aug: rearm once) |
| P2b pre-set | 141/141 | SURVIVES (clause-(e)) | killed by adding CONTROL 0x100 (aug: latch x5) |
| P3 (glm) channel INTSTAT&len2 | 141/141 | SURVIVES -- I AGREE it is DISCLOSE-able (multi-axis channel joint, floor rows single axes) | -- |
| P4 (kimi-k3) odata=SOFTINT | 135/141 | KILLED | imask/istat/gate lb/lh v0 (SOFTINT=BIT in those sessions) |
| P5 (codex) odata=use_fb | 141/141 | SURVIVES -- I AGREE it is a machine-config lvalue; DISCLOSE (also refutes item 9's "every lvalue nonzero") | -- |
| P6 (minimax) pre-set on accepted READ, acc path | 137/141 | KILLED (minimax's 141/141 claim is FALSE) | time once, time said, top said, latch x5 |
| P7 (minimax) latch `<< (addr&1)` | 137/141 | KILLED | warm once, rearm once, hi once, mid once |

**Does adding `ldP` / CONTROL-0x100 kill P1/P2 without disturbing other rows?** YES, measured:
aug_base stays 141/141; each survivor drops to 140/141 with exactly one intended row red (P1/P2 =>
`rearm once`; P1b/P2b => `latch x5`). No other row moved.

Scratch clones `/tmp/gxopuscrimec5` and `/tmp/gxopuscrimec5b` are RESTORED (source cmp-clean vs SEC,
no sentinel) and DELETED.
