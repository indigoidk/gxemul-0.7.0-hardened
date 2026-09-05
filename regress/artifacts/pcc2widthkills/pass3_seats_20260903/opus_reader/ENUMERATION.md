# pcc2widthkills pass 3 -- the clause-(d) cell table, verified by reading the shipped files

Blocks (12, one latch bit each, from the `PCC2_W_*_LEN` enum):
GENCTL 0x02 | VECBASE 0x03 | PSCALEADJ 0x15 | TxCTL 0x16+0x17 | TxICR 0x1a+0x1b |
SCCERR 0x1c | SCCICR 0x1d | SCCTX 0x1e | SCCRX 0x1f | SCSIICR 0x2f | IPL 0x3e | MASK 0x3f

Even-offset (guest-reachable): GENCTL TxCTL TxICR SCCERR SCCTX IPL = SIX.  Odd-only
(operator): VECBASE PSCALEADJ SCCICR SCCRX SCSIICR MASK = SIX.  6+6=12.  (Re-derived from
mvme_pcctworeg.h, not from the brief.  The brief's premise 3 is CORRECT.)

## The six shapes the brief enumerates

M = measured (log named).  A = argued, with the row that reds.  E = equivalent mutant.
X = UNCOVERED: no row in the 82 can move.

| block | S1 delete | S2 len>2 | S3 kill | S4 alias | S5 fall-through | S6 idata>0xff |
|---|---|---|---|---|---|---|
| GENCTL    | M part1 M_DELETE 72 | A latch all | A latch all lv | A latch all | M t1 M_NOBREAK / rb genctl | M part2 M_IDATA 80 |
| VECBASE   | A latch all | A latch all | M t1 M_OPKILL | A latch all | **X** | A latch all |
| PSCALEADJ | A latch all | A latch all | A op pscale | A latch all | M p3c 81 / op pscale noig | A latch all |
| TxCTL     | A latch all | M part1 73 | A hwr t2ctl | A latch all | A rb t2ctl 0x3->0x0 | A latch all |
| TxICR     | M part1 74 | M part1 74 | A hwr t2icr | A latch all | A rb t2icr 0x13->0x10 | A latch all |
| SCCERR    | A latch all | M part1 76 | A hwr sccerr | A latch all | **E** (arm stores 0; reg is 0 always) | A latch all |
| SCCICR    | A latch all | A latch all | A op sccicr | A latch all | M p3c 81 / rb sccicr 0x18 | A latch all |
| SCCTX     | M p2 M8 75 | M part1 75 | A hwr scctx | M p2 M1 77 | A rb scctx 0x1f->0x18 | A latch all |
| SCCRX     | A latch all | A latch all | A op sccrx | M p2 M1 77 | M p3c 81 / rb sccrx 0x98 | A latch all |
| SCSIICR   | A latch all | A latch all | A op scsiicr | A latch all | M p3c 81 / rb scsiicr 0x98 | A latch all |
| IPL       | A latch all | A latch all | M part1 M_KILL_IPL 71 | A latch all | **X** | A latch all |
| MASK      | M part1 75 / M9 | M p2 M2 75 | M part1 M_KILL_MASK 73 | A latch all | M p2 M6 77 / rb mask | A latch all |

72 cells: 18 M, 51 A, 1 E, **2 X**.

`latch all` is what makes 51 of the 72 argued rather than unmeasured guesswork, and the
argument is STRUCTURAL, not statistical:
  * `d->warned` has exactly ONE writer (`pcc2_width_decline`, `grep -c 'd->warned |='` = 1;
    the other `warned` in the file is a function-static `int` in the OB-11 read path);
  * every bit-set is inside the same `if` as its print, so prints == distinct bits set;
  * the field starts 0 (DEVINIT memset) and no tick or DEVICE_ACCESS path writes it;
  * BLOCKS12 presents 12 DISTINCT blocks, one offset each, in one session.
  => count(DECL) == popcount(d->warned) == |distinct bits named|.  Any collision, any
     silently-accepted block, any silently-accepted VALUE (0x0003 fits a byte) drops it
     below 12.  It cannot inflate.  S1, S2, S4 and S6 therefore red at EVERY block.

S3 is covered at every block by `latch all lv` (exit0 over a session touching all twelve)
plus each block's own survival row.

S5 is the only shape `latch all` cannot see, BY CONSTRUCTION -- the announce survives -- so
it needs a per-arm channel, and that is where the two holes are.

## The SEVENTH shape: `writeflag`, an input with no shape at all

The brief names five inputs (len, writeflag, relative_addr, idata, d->warned) and enumerates
shapes over four.  PRETABLE Section 1 does the same: "GUARD reads: len, writeflag", then
disagreeing states over len x idata only.

  M_NOWRITEFLAG   `writeflag == MEM_WRITE' -> `writeflag <= MEM_WRITE'   (ONE CHARACTER;
                  src/include/memory.h: MEM_READ 0, MEM_WRITE 1, so the conjunct is
                  vacuously true and the DIRECTION SPLIT -- the fix's headline -- is nulled)

  12 cells, 0 measured, 0 covered.  Pass 2's M4 (`== MEM_WRITE' -> `!= MEM_READ') is the
  EQUIVALENT form and was correctly scored so; the non-equivalent form was never built.

Why no row moves: the probe's only wide READS are in `hrd genctl/t2ctl/t2icr/sccerr/scctx',
`wrd sccerr', `val h genctl', `val w sccerr' and `hrd ipl' -- and NOT ONE of those sessions
carries a decline-count row.  Every `*_dcl' and `acc * nod' row lives in a session whose only
non-byte device access is a WRITE.  And every value row is served by the `memcpy' ABOVE the
switch, so it cannot see a guard that fires after it.
