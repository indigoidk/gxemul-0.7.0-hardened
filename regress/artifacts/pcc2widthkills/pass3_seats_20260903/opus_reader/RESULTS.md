# OPUS panel seat -- pcc2widthkills PASS 3 on the 82-row repair

Rig: scratch clone `/tmp/gxopus_p3` (`cp -a` of `build/`), baseline = the round's post-fix
WORKING SET (`GXEMUL-SEC/src/devices/dev_pcc2.c`, md5 `6fdb3880`, cmp-CLEAN before mutant 1),
instrument FROZEN at the shipped probe (md5 `cd22f951` -- byte-identical to
`regress/pcc2_width_probe.py` and to the round's own `pass3c/probe82.frozen.py`).
Baseline rebuilt IN THE CLONE; `[ gxemul -nt src ]` checked on every build.
GXEMUL-SEC, build/, build-asan/ and est/ never written.

    log: kill.log        rows: p3_<tag>.out        predictions: PREDICTIONS.txt (pre-run)

| tag | edit | score | red rows |
|---|---|---|---|
| BASE | -- | **82/82** | -- |
| **MD** (control) | delete `break;` at **GENCTL** -- the same edit shape as MA/MB | **80/82** | `rb genctl` 0xbb, `rb genctl lo` 0x22 |
| **MA** | delete `break;` at **VECBASE** (announce-then-land) | **82/82 SWEEP** | none |
| **MB** | delete `break;` at **IPL** | **82/82 SWEEP** | none |
| **MC** | `writeflag == MEM_WRITE` -> `writeflag <= MEM_WRITE`, all 12 (ONE CHARACTER) | see kill.log | -- |

MD is the negative control the clean sweeps need: the identical `break;` deletion IS caught
at GENCTL, so MA and MB are holes in the detector, not a broken mutator.

Under MA the three VECBASE-touching rows are all green: `op vecbase dcl` 1 (the announce
survives a fall-through by construction), `latch all` 12, and `rb vecbase` 0x50 -- because
that row's wide write is at GENCTL, not VECBASE.
Under MB: `hwr ipl dcl` 1, `latch all` 12, survival + scratch-liveness only.

## FINAL TABLE (kill.log, 15:36 -> 15:59)

    BASE   82/82   -
    MD     80/82   rb genctl (0xbb), rb genctl lo (0x22)      <- CONTROL: the shape IS caught at GENCTL
    MA     82/82   TOTAL SWEEP   (break; deleted at VECBASE)
    MB     82/82   TOTAL SWEEP   (break; deleted at IPL)
    MC     82/82   TOTAL SWEEP   (writeflag == -> <= , ONE CHARACTER, all twelve)

## NON-EQUIVALENCE + PROPOSED-ROW SPECIFICITY (nonequiv.log, 16:00 -> 16:01)

Each proposed row moves under ITS OWN mutant and no other -- so the three sweeps are
non-equivalent AND the three rows are orthogonal:

                    rb vecbase wr   hwr ipl noro   hrd genctl nod
    BASE            0x50            0              0
    MA              **0xb0**        0              0
    MB              0x50            **1**          0
    MC              0x50            0              **1**

`0xb0` is `0xaabb & 0xf0` landing in PCCTWO_VECBASE -- the interrupt vector base that
`DEVICE_ACCESS(mvme187_iack)` adds to `cur_int_vec[]` to answer an interrupt acknowledge.
Not a diagnostic: real state, in the register whose corruption misdirects every vector.

## THE THREE ROWS THAT CLOSE THEM (zero new sessions for two of the three)

    rb vecbase wr   NEW session, copies `rb mask' verbatim:
                    setup(r5="0x50") + program([ST_B(5, VECBASE)])
                      + ["put h 0x%x, 0xaabb" % (PCC2 + VECBASE)]
                      + program([LD_BU(4, VECBASE)], at=CODE + 0x100) + ["print r4"]   want 0x50
    hwr ipl noro    REUSES the existing `hwr ipl' session's t:
                    t.count("write to read-only PCCTWO_IPL")                            want 0
    hrd * nod       REUSES each existing `hrd <nm>' session's t: t.count(DECL)           want 0
                    Six of them (genctl t2ctl t2icr sccerr scctx ipl) close the whole
                    writeflag axis -- see below for why six, not twelve.

All three names are <= 15 chars and <= 14, so the probe's assert and the gate's
`^$v  .*ok$' padded-column pattern both hold.

## RESTORE

Both scripts: part 1 source cmp-CLEAN vs SEC, part 2 rebuilt and `binary -nt source`,
sentinel cleared.  `git status --porcelain` in GXEMUL-SEC identical before and after.
